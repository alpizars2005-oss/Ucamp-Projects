"""Pruebas del incremento: reglas del negocio y límites de la API local."""
import concurrent.futures
from datetime import datetime
import http.client
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import unittest
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
from server import Store, ValidationError, make_server


def order(lines=None, **overrides):
    result = {"request_id": str(uuid.uuid4()), "lines": lines if lines is not None else [
        {"product_id": 1, "quantity": 2}, {"product_id": 3, "quantity": 1}], "note": "Entregar juntos"}
    return result | overrides


def feedback(**overrides):
    return {"request_id": str(uuid.uuid4()), "rating": 4, "comment": "Dato sintético de prueba"} | overrides


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = Store(Path(self.temp.name) / "test.sqlite3")

    def assert_invalid(self, payload):
        with self.assertRaises(ValidationError):
            self.store.place_order(payload)
        self.assertEqual(self.store.state()["summary"]["orders"], 0)

    def test_catalog_and_prices(self):
        state = self.store.state()
        self.assertEqual([p["price_cents"] for p in state["products"]], [3500, 3500, 4000])
        self.assertEqual(len(state["stock"]), 6)

    def test_availability_uses_complete_recipe(self):
        self.assertEqual([p["available"] for p in self.store.state()["products"]], [13, 13, 5])

    def test_server_calculates_total_not_client(self):
        result = self.store.place_order(order(total_cents=1))
        self.assertEqual(result["total_cents"], 11000)

    def test_sale_deducts_ingredients_and_packaging(self):
        self.store.place_order(order())
        self.assertEqual([i["stock"] for i in self.store.state()["stock"]], [480, 240, 170, 200, 65, 17])

    def test_note_and_lines_are_persisted(self):
        self.store.place_order(order())
        saved = self.store.state()["orders"][0]
        self.assertEqual(saved["note"], "Entregar juntos")
        self.assertEqual(len(saved["lines"]), 2)

    def test_database_survives_restart_without_reseeding(self):
        self.store.place_order(order())
        restarted = Store(self.store.path)
        self.assertEqual(restarted.state(), self.store.state())

    def test_empty_order_is_rejected(self):
        self.assert_invalid(order([]))

    def test_zero_quantity_is_rejected(self):
        self.assert_invalid(order([{"product_id": 1, "quantity": 0}]))

    def test_negative_quantity_is_rejected(self):
        self.assert_invalid(order([{"product_id": 1, "quantity": -1}]))

    def test_fractional_quantity_is_rejected(self):
        self.assert_invalid(order([{"product_id": 1, "quantity": 1.5}]))

    def test_boolean_quantity_is_rejected(self):
        self.assert_invalid(order([{"product_id": 1, "quantity": True}]))

    def test_boolean_product_is_rejected(self):
        self.assert_invalid(order([{"product_id": True, "quantity": 1}]))

    def test_unknown_product_is_rejected(self):
        self.assert_invalid(order([{"product_id": 999, "quantity": 1}]))

    def test_non_object_payload_is_rejected(self):
        self.assert_invalid([])

    def test_malformed_line_is_rejected(self):
        self.assert_invalid(order(["fresa"]))

    def test_duplicate_lines_are_aggregated(self):
        self.store.place_order(order([{"product_id": 1, "quantity": 1}, {"product_id": 1, "quantity": 2}]))
        state = self.store.state()
        self.assertEqual(state["orders"][0]["lines"][0]["quantity"], 3)
        self.assertEqual(state["summary"]["sales_cents"], 10500)

    def test_quantity_limit_after_aggregation(self):
        self.assert_invalid(order([{"product_id": 1, "quantity": 60}, {"product_id": 1, "quantity": 60}]))

    def test_long_note_is_rejected(self):
        self.assert_invalid(order(note="x" * 241))

    def test_invalid_request_id_is_rejected(self):
        self.assert_invalid(order(request_id="not-a-uuid"))

    def test_stock_shortage_rolls_back_whole_order(self):
        before = self.store.state()
        with self.assertRaises(ValidationError) as error:
            self.store.place_order(order([{"product_id": 1, "quantity": 1}, {"product_id": 3, "quantity": 6}]))
        self.assertEqual(error.exception.status, 409)
        self.assertEqual(self.store.state(), before)

    def test_shared_ingredient_shortage_is_aggregated(self):
        self.assert_invalid(order([{"product_id": 1, "quantity": 10}, {"product_id": 2, "quantity": 10}]))

    def test_missing_recipe_blocks_sale(self):
        with self.store.connection() as db:
            db.execute("DELETE FROM recipes WHERE product_id=1")
        self.assert_invalid(order())

    def test_retry_does_not_duplicate_or_deduct_twice(self):
        payload = order()
        first = self.store.place_order(payload)
        before = self.store.state()
        second = self.store.place_order(payload)
        self.assertFalse(first["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(self.store.state(), before)

    def test_reusing_id_with_other_order_is_rejected(self):
        payload = order()
        self.store.place_order(payload)
        with self.assertRaises(ValidationError):
            self.store.place_order(payload | {"note": "different"})
        self.assertEqual(self.store.state()["summary"]["orders"], 1)

    def test_concurrent_identical_requests_create_one_order(self):
        payload = order()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(self.store.place_order, [payload] * 4))
        self.assertEqual(sum(not r["replayed"] for r in results), 1)
        self.assertEqual(self.store.state()["summary"]["orders"], 1)

    def test_concurrent_sales_cannot_oversell(self):
        with self.store.connection() as db:
            db.execute("UPDATE ingredients SET stock=1 WHERE id=6")
        def buy(_):
            try:
                self.store.place_order(order([{"product_id": 1, "quantity": 1}]))
                return True
            except ValidationError:
                return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(buy, range(2)))
        self.assertEqual(sum(results), 1)
        self.assertEqual(self.store.state()["stock"][-1]["stock"], 0)

    def test_low_stock_threshold_is_available_to_interface(self):
        self.store.place_order(order([{"product_id": 1, "quantity": 10}]))
        masa = self.store.state()["stock"][0]
        self.assertEqual(masa["stock"], masa["low_at"])

    def test_feedback_persists_rating_and_comment(self):
        payload = feedback()
        self.store.record_feedback(payload)
        self.assertEqual(self.store.state()["feedback"], {"count": 1, "average": 4.0})
        with self.store.connection() as db:
            self.assertEqual(db.execute("SELECT comment FROM feedback").fetchone()[0], payload["comment"])

    def test_feedback_bounds(self):
        for bad in [0, 6, True, 1.5, "4", None]:
            with self.subTest(rating=bad), self.assertRaises(ValidationError):
                self.store.record_feedback(feedback(rating=bad))

    def test_feedback_retry_is_idempotent(self):
        payload = feedback()
        self.store.record_feedback(payload)
        self.assertTrue(self.store.record_feedback(payload)["replayed"])
        self.assertEqual(self.store.state()["feedback"]["count"], 1)

    def test_feedback_conflicting_retry_is_rejected(self):
        payload = feedback()
        self.store.record_feedback(payload)
        with self.assertRaises(ValidationError):
            self.store.record_feedback(payload | {"rating": 5})

    def test_daily_summary_excludes_other_dates(self):
        self.store.place_order(order())
        with self.store.connection() as db:
            db.execute("UPDATE orders SET business_date='2000-01-01'")
        self.assertEqual(self.store.state()["summary"], {"orders": 0, "sales_cents": 0})

    def test_unknown_schema_version_is_not_overwritten(self):
        with self.store.connection() as db:
            db.execute("PRAGMA user_version=99")
        with self.assertRaises(RuntimeError):
            Store(self.store.path)


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.store = Store(Path(cls.temp.name) / "api.sqlite3")
        cls.server = make_server(cls.store, port=0, token="test-key-not-a-real-secret")
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(); cls.temp.cleanup()

    def call(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        try:
            conn.request(method, path, body, headers or {})
            response = conn.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            conn.close()

    def auth(self):
        return {"Authorization": "Bearer test-key-not-a-real-secret", "Content-Type": "application/json"}

    def test_state_requires_access_key(self):
        self.assertEqual(self.call("GET", "/api/state")[0], 401)

    def test_wrong_access_key_is_rejected(self):
        self.assertEqual(self.call("GET", "/api/state", headers={"Authorization": "Bearer wrong"})[0], 401)

    def test_authorized_state_is_json(self):
        status, headers, body = self.call("GET", "/api/state", headers=self.auth())
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(body)["products"]), 3)
        self.assertNotIn("Access-Control-Allow-Origin", headers)

    def test_static_html_has_security_headers(self):
        status, headers, body = self.call("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b"Mochi Monchi", body)
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])

    def test_static_allowlist_blocks_database_and_traversal(self):
        for path in ["/../server.py", "/server.py", "/data/mochi.sqlite3", "/%2e%2e/server.py"]:
            with self.subTest(path=path):
                self.assertEqual(self.call("GET", path)[0], 404)

    def test_bad_json_is_rejected(self):
        self.assertEqual(self.call("POST", "/api/orders", "{bad}", self.auth())[0], 400)

    def test_bad_utf8_is_rejected(self):
        self.assertEqual(self.call("POST", "/api/orders", b"\xff", self.auth())[0], 400)

    def test_wrong_content_type_is_rejected(self):
        headers = self.auth() | {"Content-Type": "text/plain"}
        self.assertEqual(self.call("POST", "/api/orders", "{}", headers)[0], 415)

    def test_body_size_limit(self):
        self.assertEqual(self.call("POST", "/api/orders", "x" * 32769, self.auth())[0], 413)

    def test_order_http_status_and_retry(self):
        payload = json.dumps(order())
        self.assertEqual(self.call("POST", "/api/orders", payload, self.auth())[0], 201)
        self.assertEqual(self.call("POST", "/api/orders", payload, self.auth())[0], 200)

    def test_unknown_endpoint_is_rejected(self):
        self.assertEqual(self.call("POST", "/api/unknown", "{}", self.auth())[0], 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
