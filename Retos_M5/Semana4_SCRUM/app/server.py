"""Mochi Monchi: incremento académico local. Python 3.11+, sin paquetes externos."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import sqlite3
from typing import Any
from urllib.parse import urlsplit
import uuid
import webbrowser

ROOT = Path(__file__).resolve().parent
MAX_BODY = 32_768


class ValidationError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def text(value: Any, label: str, maximum: int) -> str:
    if not isinstance(value, str) or len(value) > maximum:
        raise ValidationError(f"{label}: debe ser texto de hasta {maximum} caracteres.")
    return value.strip()


def request_id(value: Any) -> str:
    try:
        if not isinstance(value, str):
            raise ValueError
        return str(uuid.UUID(value))
    except (ValueError, AttributeError) as exc:
        raise ValidationError("El identificador de envío no es válido.") from exc


class Store:
    """Una conexión por operación; cada venta es una transacción indivisible."""

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.execute("PRAGMA journal_mode=WAL")
            version = db.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, 1):
                raise RuntimeError("Versión de base de datos no compatible; no se modificó.")
            db.executescript("""
                CREATE TABLE IF NOT EXISTS products(
                    id INTEGER PRIMARY KEY, name TEXT NOT NULL,
                    price_cents INTEGER NOT NULL CHECK(price_cents > 0));
                CREATE TABLE IF NOT EXISTS ingredients(
                    id INTEGER PRIMARY KEY, name TEXT NOT NULL, unit TEXT NOT NULL,
                    stock INTEGER NOT NULL CHECK(stock >= 0),
                    low_at INTEGER NOT NULL CHECK(low_at >= 0));
                CREATE TABLE IF NOT EXISTS recipes(
                    product_id INTEGER REFERENCES products(id),
                    ingredient_id INTEGER REFERENCES ingredients(id),
                    amount INTEGER NOT NULL CHECK(amount > 0),
                    PRIMARY KEY(product_id, ingredient_id));
                CREATE TABLE IF NOT EXISTS orders(
                    id TEXT PRIMARY KEY, created_at TEXT NOT NULL,
                    business_date TEXT NOT NULL, note TEXT NOT NULL,
                    total_cents INTEGER NOT NULL CHECK(total_cents > 0),
                    fingerprint TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS order_lines(
                    order_id TEXT REFERENCES orders(id),
                    product_id INTEGER REFERENCES products(id),
                    quantity INTEGER NOT NULL CHECK(quantity > 0),
                    unit_price_cents INTEGER NOT NULL,
                    PRIMARY KEY(order_id, product_id));
                CREATE TABLE IF NOT EXISTS feedback(
                    id TEXT PRIMARY KEY, business_date TEXT NOT NULL,
                    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                    comment TEXT NOT NULL);
                PRAGMA user_version=1;
            """)
            db.execute("BEGIN IMMEDIATE")
            if not db.execute("SELECT 1 FROM products LIMIT 1").fetchone():
                db.executemany("INSERT INTO products VALUES(?,?,?)", [
                    (1, "Mochi de fresa", 3500), (2, "Mochi de mango", 3500),
                    (3, "Mochi de matcha", 4000)])
                db.executemany("INSERT INTO ingredients VALUES(?,?,?,?,?)", [
                    (1, "Masa de arroz", "g", 600, 200),
                    (2, "Crema", "g", 300, 100), (3, "Fresa", "g", 200, 60),
                    (4, "Mango", "g", 200, 60), (5, "Matcha", "g", 80, 30),
                    (6, "Empaque individual", "pza", 20, 5)])
                for product, filling in [(1, 3), (2, 4), (3, 5)]:
                    db.executemany("INSERT INTO recipes VALUES(?,?,?)", [
                        (product, 1, 40), (product, 2, 20),
                        (product, filling, 15), (product, 6, 1)])
            db.commit()

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            yield db
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def place_order(self, payload: Any) -> dict:
        if not isinstance(payload, dict):
            raise ValidationError("El pedido debe ser un objeto JSON.")
        key = request_id(payload.get("request_id"))
        note = text(payload.get("note", ""), "Nota", 240)
        lines = payload.get("lines")
        if not isinstance(lines, list) or not 1 <= len(lines) <= 30:
            raise ValidationError("Agrega entre 1 y 30 renglones al pedido.")
        quantities: dict[int, int] = {}
        for line in lines:
            if not isinstance(line, dict):
                raise ValidationError("Cada renglón debe indicar producto y cantidad.")
            pid, qty = line.get("product_id"), line.get("quantity")
            if type(pid) is not int or type(qty) is not int or not 1 <= qty <= 99:
                raise ValidationError("Producto y cantidad deben ser enteros; cantidad de 1 a 99.")
            quantities[pid] = quantities.get(pid, 0) + qty
            if quantities[pid] > 99:
                raise ValidationError("El máximo por producto es de 99 unidades.")
        canonical = json.dumps([sorted(quantities.items()), note], ensure_ascii=False)
        fingerprint = hashlib.sha256(canonical.encode()).hexdigest()
        with self.connection() as db:
            # Reservar escritura antes de consultar existencias evita sobreventa concurrente.
            db.execute("BEGIN IMMEDIATE")
            previous = db.execute("SELECT * FROM orders WHERE id=?", (key,)).fetchone()
            if previous:
                if previous["fingerprint"] != fingerprint:
                    raise ValidationError("Este envío ya se usó para otro pedido.", 409)
                return {"id": key, "total_cents": previous["total_cents"], "replayed": True}
            needs: dict[int, int] = {}
            total = 0
            prices: dict[int, int] = {}
            for pid, qty in quantities.items():
                product = db.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
                if not product:
                    raise ValidationError("El producto seleccionado no existe.")
                recipe = db.execute("SELECT * FROM recipes WHERE product_id=?", (pid,)).fetchall()
                if not recipe:
                    raise ValidationError("El producto no tiene receta y no puede venderse.", 409)
                prices[pid] = product["price_cents"]
                total += prices[pid] * qty  # Nunca aceptar precios o totales del navegador.
                for ingredient in recipe:
                    iid = ingredient["ingredient_id"]
                    needs[iid] = needs.get(iid, 0) + ingredient["amount"] * qty
            shortages = []
            for iid, amount in needs.items():
                item = db.execute("SELECT * FROM ingredients WHERE id=?", (iid,)).fetchone()
                if item["stock"] < amount:
                    shortages.append(f"{item['name']}: {item['stock']} {item['unit']} disponibles, {amount} requeridos")
            if shortages:
                raise ValidationError("No se guardó el pedido. Stock insuficiente. " + "; ".join(shortages), 409)
            now = datetime.now().astimezone()
            db.execute("INSERT INTO orders VALUES(?,?,?,?,?,?)",
                       (key, now.isoformat(timespec="seconds"), now.date().isoformat(), note, total, fingerprint))
            for pid, qty in quantities.items():
                db.execute("INSERT INTO order_lines VALUES(?,?,?,?)", (key, pid, qty, prices[pid]))
            for iid, amount in needs.items():
                db.execute("UPDATE ingredients SET stock=stock-? WHERE id=?", (amount, iid))
            db.commit()
        return {"id": key, "total_cents": total, "replayed": False}

    def record_feedback(self, payload: Any) -> dict:
        if not isinstance(payload, dict):
            raise ValidationError("La valoración debe ser un objeto JSON.")
        key = request_id(payload.get("request_id"))
        rating = payload.get("rating")
        if type(rating) is not int or not 1 <= rating <= 5:
            raise ValidationError("La valoración debe ser un entero de 1 a 5.")
        comment = text(payload.get("comment", ""), "Comentario", 500)
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT * FROM feedback WHERE id=?", (key,)).fetchone()
            if old and (old["rating"] != rating or old["comment"] != comment):
                raise ValidationError("Este envío ya se usó para otra valoración.", 409)
            if not old:
                db.execute("INSERT INTO feedback VALUES(?,?,?,?)",
                           (key, datetime.now().date().isoformat(), rating, comment))
            db.commit()
        return {"id": key, "replayed": bool(old)}

    def state(self) -> dict:
        today = datetime.now().date().isoformat()
        with self.connection() as db:
            db.execute("BEGIN")  # Un estado coherente, incluso si otro navegador está vendiendo.
            stock = [dict(row) for row in db.execute("SELECT * FROM ingredients ORDER BY id")]
            products = []
            for row in db.execute("SELECT * FROM products ORDER BY id"):
                product = dict(row)
                recipe = [dict(r) for r in db.execute("""
                    SELECT i.name, i.unit, i.stock, r.amount FROM recipes r
                    JOIN ingredients i ON i.id=r.ingredient_id WHERE r.product_id=?
                    ORDER BY i.id""", (row["id"],))]
                product["available"] = min((r["stock"] // r["amount"] for r in recipe), default=0)
                product["recipe"] = recipe
                products.append(product)
            orders = [dict(row) for row in db.execute("""SELECT id,created_at,note,total_cents
                FROM orders WHERE business_date=? ORDER BY rowid DESC LIMIT 30""", (today,))]
            for order in orders:
                order["lines"] = [dict(row) for row in db.execute("""
                    SELECT p.name,l.quantity,l.unit_price_cents FROM order_lines l
                    JOIN products p ON p.id=l.product_id WHERE l.order_id=?""", (order["id"],))]
            summary = dict(db.execute("""SELECT COUNT(*) AS orders,
                COALESCE(SUM(total_cents),0) AS sales_cents FROM orders WHERE business_date=?""", (today,)).fetchone())
            feedback = dict(db.execute("""SELECT COUNT(*) AS count, AVG(rating) AS average
                FROM feedback WHERE business_date=?""", (today,)).fetchone())
        return {"business_date": today, "products": products, "stock": stock,
                "orders": orders, "summary": summary, "feedback": feedback, "demo": True}


def make_server(store: Store, host: str = "127.0.0.1", port: int = 8765,
                token: str | None = None) -> ThreadingHTTPServer:
    access_key = token or secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(5)

        def log_message(self, *_):
            pass

        def send_bytes(self, status: int, body: bytes, mime: str):
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def send_json(self, status: int, payload: Any):
            self.send_bytes(status, json.dumps(payload, ensure_ascii=False).encode(), "application/json; charset=utf-8")

        def authorized(self) -> bool:
            actual = self.headers.get("Authorization", "")
            if not secrets.compare_digest(actual.encode(), f"Bearer {access_key}".encode()):
                self.send_json(401, {"error": "Abre el enlace completo que aparece en la terminal del servidor."})
                return False
            return True

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/api/state":
                if not self.authorized():
                    return
                try:
                    self.send_json(200, store.state())
                except sqlite3.Error:
                    self.send_json(503, {"error": "No se pudo leer la base de datos. Reintenta."})
                return
            assets = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"),
                      "/style.css": ("style.css", "text/css")}
            if path not in assets:
                self.send_json(404, {"error": "Recurso no encontrado."})
                return
            name, mime = assets[path]
            self.send_bytes(200, (ROOT / name).read_bytes(), mime + "; charset=utf-8")

        def do_POST(self):
            if not self.authorized():
                return
            path = urlsplit(self.path).path
            if path not in ("/api/orders", "/api/feedback"):
                self.send_json(404, {"error": "Recurso no encontrado."})
                return
            try:
                if self.headers.get("Transfer-Encoding"):
                    raise ValidationError("La petición debe indicar Content-Length.")
                if self.headers.get_content_type() != "application/json":
                    raise ValidationError("Se requiere Content-Type: application/json.", 415)
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                except ValueError as exc:
                    raise ValidationError("Content-Length no válido.") from exc
                if not 0 < length <= MAX_BODY:
                    raise ValidationError("El cuerpo está vacío o supera 32 KiB.", 413)
                payload = json.loads(self.rfile.read(length))
                result = store.place_order(payload) if path == "/api/orders" else store.record_feedback(payload)
                self.send_json(200 if result["replayed"] else 201, result)
            except (json.JSONDecodeError, UnicodeDecodeError):
                self.send_json(400, {"error": "El cuerpo no contiene JSON válido en UTF-8."})
            except ValidationError as exc:
                self.send_json(exc.status, {"error": str(exc)})
            except sqlite3.Error:
                self.send_json(503, {"error": "No se pudo completar la operación. Reintenta el mismo envío."})

    server = ThreadingHTTPServer((host, port), Handler)
    server.access_key = access_key
    server.daemon_threads = True
    return server


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", choices=["127.0.0.1", "0.0.0.0"])
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--db", type=Path, default=ROOT.parent / "data" / "mochi.sqlite3")
    parser.add_argument("--open", action="store_true", help="Abrir el navegador local")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("El puerto debe estar entre 1 y 65535.")
    try:
        server = make_server(Store(args.db), args.host, args.port)
    except (OSError, sqlite3.Error, RuntimeError) as exc:
        parser.exit(1, f"No se pudo iniciar: {exc}\n")
    url = f"http://127.0.0.1:{args.port}/#{server.access_key}"
    print("Mochi Monchi | datos de demostración, no operación comercial")
    print(f"Abre: {url}\nBase de datos: {args.db.resolve()}\nDetener: Ctrl+C", flush=True)
    if args.host == "0.0.0.0":
        print("Modo LAN: sustituye 127.0.0.1 por la IP privada del servidor en otro dispositivo.")
        print("Sólo red confiable. HTTP sin cifrado; no exponer a Internet ni abrir puertos del router.")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
