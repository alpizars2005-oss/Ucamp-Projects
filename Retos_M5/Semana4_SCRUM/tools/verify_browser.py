"""Ejecuta el navegador contra la aplicación real y captura evidencia reproducible.

Requiere Playwright y Chromium sólo para verificar; la aplicación no los necesita.
"""
from datetime import datetime, timezone
import json
import http.client
import os
from pathlib import Path
import shutil
import sys
import tempfile
import threading

from playwright.sync_api import sync_playwright, expect

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "app"))
from server import Store, make_server


def main():
    out = BASE / "evidencias"
    out.mkdir(exist_ok=True)
    report = {"executed_at_utc": datetime.now(timezone.utc).isoformat(),
              "environment": "Chromium headless; dos contextos de navegador, no dos teléfonos físicos",
              "data": "Precios, recetas, pedidos y valoraciones sintéticos", "checks": []}
    errors = []
    bridge_mode = os.environ.get("MOCHI_BROWSER_BRIDGE") == "1"
    if bridge_mode:
        report["environment"] += "; UI renderizada en memoria con puente HTTP y almacenamiento de sesión de prueba; navegación nativa no evaluada localmente"
    def open_app(page, server, directory, session=None):
        if not bridge_mode:
            page.goto(f"http://127.0.0.1:{server.server_port}/#{server.access_key}")
            return
        def transport(path, options):
            assert path in ("/api/state", "/api/orders", "/api/feedback")
            conn = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
            try:
                conn.request(options.get("method", "GET"), path, options.get("body", "").encode("utf-8") if options.get("body") is not None else None, options.get("headers", {}))
                response = conn.getresponse()
                return {"status": response.status, "body": response.read().decode("utf-8")}
            finally:
                conn.close()
        page.expose_function("localTransport", transport)
        storage = json.dumps(session or {"mochi-key": server.access_key})
        bridge = "Object.defineProperty(window, 'sessionStorage', {value: {__items: " + storage + ", getItem(k) {return this.__items[k] ?? null;}, setItem(k,v) {this.__items[k]=String(v);}, removeItem(k) {delete this.__items[k];}}});"
        bridge += """window.fetch = async (path, options = {}) => {
            const result = await window.localTransport(path, {method:options.method, headers:options.headers, body:options.body});
            if (window.__loseNextOrderResponse && path === '/api/orders') {
                window.__loseNextOrderResponse = false; throw new Error('Respuesta perdida de prueba');
            }
            return new Response(result.body, {status:result.status,headers:{'Content-Type':'application/json'}});
        };"""
        html = (BASE / "app/index.html").read_text(encoding="utf-8")
        html = html.replace('<link rel="stylesheet" href="/style.css">', '<style>' + (BASE / 'app/style.css').read_text() + '</style>')
        html = html.replace('<script src="/app.js" defer></script>', '')
        html = html.replace('</body>', '<script>' + bridge + (BASE / 'app/app.js').read_text() + '</script></body>')
        page.set_content(html)
    with tempfile.TemporaryDirectory() as temp, sync_playwright() as p:
        store = Store(Path(temp) / "demo.sqlite3")
        server = make_server(store, port=0, token="browser-fixture-not-a-real-secret")
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        executable = shutil.which("chromium") or shutil.which("chromium-browser")
        browser = p.chromium.launch(**({"executable_path": executable} if executable else {}), args=["--no-sandbox"])
        try:
            context = browser.new_context(viewport={"width": 1440, "height": 1080}, locale="es-MX")
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            url = f"http://127.0.0.1:{server.server_port}/#{server.access_key}"
            open_app(page, server, temp)
            expect(page.locator("#catalog .product")).to_have_count(3)
            report["checks"].append("Catálogo visible con tres productos y precios")
            page.get_by_role("button", name="Agregar Mochi de fresa", exact=True).click(click_count=2)
            page.get_by_role("button", name="Agregar Mochi de matcha", exact=True).click()
            page.locator("#note").fill("Pedido de prueba · entregar juntos")
            expect(page.locator("#total")).to_have_text("$110.00")
            page.screenshot(path=str(out / "01_pedido_revision.png"), full_page=True)
            report["checks"].append("Revisión de 2 fresa + 1 matcha = $110.00 MXN")
            page.locator("#confirm").click()
            expect(page.locator("#notice")).to_contain_text("confirmado")
            initial_sale = store.state()
            assert [i["stock"] for i in initial_sale["stock"]] == [480, 240, 170, 200, 65, 17]
            assert initial_sale["summary"] == {"orders": 1, "sales_cents": 11000}
            report["first_sale"] = initial_sale
            report["checks"].append("Confirmación persistida y descuento exacto de ingredientes y empaques")
            page.screenshot(path=str(out / "02_pedido_confirmado.png"), full_page=True)
            for _ in range(10):
                page.get_by_role("button", name="Agregar Mochi de fresa", exact=True).click()
            page.locator("#note").fill("Segundo pedido sintético: prueba de alertas")
            page.locator("#confirm").click()
            expect(page.locator("#order-count")).to_have_text("2")
            page.locator('[data-view="stock-view"]').click()
            expect(page.locator(".stock-badge.low")).to_have_count(3)
            page.screenshot(path=str(out / "03_inventario_alertas.png"), full_page=True)
            report["checks"].append("Tres alertas de stock bajo tras el segundo pedido, sin existencias negativas")
            mobile = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True,
                                         device_scale_factor=1, has_touch=True, locale="es-MX")
            phone = mobile.new_page()
            phone.on("pageerror", lambda error: errors.append(str(error)))
            open_app(phone, server, temp)
            phone.locator('[data-view="stock-view"]').click()
            expect(phone.locator("#stock")).to_contain_text("80 g")
            assert phone.evaluate("document.documentElement.scrollWidth <= innerWidth")
            phone.screenshot(path=str(out / "05_vista_movil.png"), full_page=True)
            report["checks"].append("Segundo navegador comparte el inventario; interfaz de 390 px sin desbordamiento horizontal")
            # El segundo navegador permanece abierto para observar el siguiente cambio.
            page.locator('[data-view="close-view"]').click()
            page.locator("#rating").select_option("4")
            page.locator("#comment").fill("PRUEBA SINTÉTICA: las alertas son visibles. Priorizar cancelación con devolución de stock.")
            page.locator("#save-feedback").click()
            expect(page.locator("#feedback-count")).to_have_text("1")
            expect(phone.locator("#feedback-count")).to_have_text("1", timeout=8000)
            page.screenshot(path=str(out / "04_cierre_y_feedback.png"), full_page=True)
            report["checks"].append("Valoración 4/5 y comentario guardados; segundo navegador se actualiza por consulta periódica")
            before = store.state()
            page.locator('[data-view="orders-view"]').click()
            for _ in range(3):
                page.get_by_role("button", name="Agregar Mochi de matcha", exact=True).click()
            page.locator("#confirm").click()
            expect(page.locator("#notice")).to_contain_text("Stock insuficiente")
            assert store.state() == before
            page.screenshot(path=str(out / "06_rechazo_sin_stock.png"), full_page=True)
            report["checks"].append("Pedido sin stock rechazado desde la interfaz; no cambia ni pedidos ni inventario")
            report["final_demo_state"] = before
            mobile.close()
            context.close()
            # Escenario adicional aislado: respuesta perdida, recarga y reintento.
            isolated_store = Store(Path(temp) / "retry.sqlite3")
            isolated = make_server(isolated_store, port=0, token="isolated-fixture-not-a-secret")
            isolated_thread = threading.Thread(target=isolated.serve_forever, daemon=True)
            isolated_thread.start()
            try:
                extra = browser.new_context(viewport={"width":1280,"height":900})
                retry = extra.new_page()
                retry.on("pageerror", lambda error: errors.append(str(error)))
                open_app(retry, isolated, temp)
                retry.get_by_role("button", name="Agregar Mochi de fresa", exact=True).click()
                retry.locator("#note").fill('<img src=x onerror="alert(1)">')
                def lose_response(route):
                    response = route.fetch()
                    assert response.status == 201
                    route.abort()
                if bridge_mode:
                    retry.evaluate("window.__loseNextOrderResponse = true")
                else:
                    retry.route("**/api/orders", lose_response, times=1)
                retry.locator("#confirm").click()
                expect(retry.locator("#confirm")).to_have_text("Reintentar el mismo envío")
                assert isolated_store.state()["summary"]["orders"] == 1
                if bridge_mode:
                    saved_session = retry.evaluate("sessionStorage.__items")
                    retry.close()
                    retry = extra.new_page()
                    retry.on("pageerror", lambda error: errors.append(str(error)))
                    open_app(retry, isolated, temp, saved_session)
                else:
                    retry.reload()
                expect(retry.locator("#confirm")).to_have_text("Reintentar el mismo envío")
                retry.locator("#confirm").click()
                expect(retry.locator("#notice")).to_contain_text("no duplicó")
                assert isolated_store.state()["summary"]["orders"] == 1
                report["checks"].append("Respuesta perdida + " + ("restauración de sesión simulada" if bridge_mode else "recarga") + " + reintento: una sola venta y un solo descuento")
                retry.locator('[data-view="close-view"]').click()
                expect(retry.locator(".order-note")).to_have_text('<img src=x onerror="alert(1)">')
                expect(retry.locator("#history img")).to_have_count(0)
                report["checks"].append("Nota con HTML se muestra como texto, no como contenido ejecutable")
                extra.close()
            finally:
                isolated.shutdown(); isolated.server_close(); isolated_thread.join()
            assert not errors, errors
            report["javascript_errors"] = errors
            report["result"] = "PASS"
            (out / "verificacion_navegador.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"result": report["result"], "browser_checks": len(report["checks"]),
                              "screenshots": 6, "javascript_errors": errors}, ensure_ascii=False))
        finally:
            browser.close(); server.shutdown(); server.server_close(); thread.join()


if __name__ == "__main__":
    main()
