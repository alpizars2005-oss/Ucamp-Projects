"use strict";
const $ = (id) => document.getElementById(id);
const money = (cents) => new Intl.NumberFormat("es-MX", {style:"currency",currency:"MXN"}).format(cents / 100);
let state = null, cart = new Map(), busy = false, feedbackBusy = false;
let accessKey = location.hash.slice(1) || sessionStorage.getItem("mochi-key") || "";
if (location.hash) { sessionStorage.setItem("mochi-key", accessKey); history.replaceState(null, "", location.pathname); }
function saved(key) { try { return JSON.parse(sessionStorage.getItem(key)); } catch { return null; } }
let pendingOrder = saved("mochi-pending-order"), pendingFeedback = saved("mochi-pending-feedback");
if (pendingOrder && Array.isArray(pendingOrder.lines)) {
  cart = new Map(pendingOrder.lines.map((line) => [line.product_id, line.quantity]));
  $("note").value = pendingOrder.note;
}
function uuid() {
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  bytes[6] = (bytes[6] & 15) | 64; bytes[8] = (bytes[8] & 63) | 128;
  const s = Array.from(bytes, x => x.toString(16).padStart(2, "0")).join("");
  return `${s.slice(0,8)}-${s.slice(8,12)}-${s.slice(12,16)}-${s.slice(16,20)}-${s.slice(20)}`;
}
function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function notice(message, error = false) {
  $("notice").textContent = message; $("notice").className = error ? "error" : ""; $("notice").hidden = false;
}
async function api(path, payload) {
  const control = new AbortController(), timer = setTimeout(() => control.abort(), 10000);
  try {
    const response = await fetch(path, {
      method: payload === undefined ? "GET" : "POST",
      headers: {"Authorization": `Bearer ${accessKey}`, "Content-Type": "application/json"},
      body: payload === undefined ? undefined : JSON.stringify(payload), signal: control.signal
    });
    const data = await response.json();
    if (!response.ok) { const error = new Error(data.error || "No se pudo completar la operación."); error.status = response.status; throw error; }
    return data;
  } finally { clearTimeout(timer); }
}
function button(text, label, action, className) {
  const node = el("button", text, className); node.type = "button"; node.setAttribute("aria-label", label);
  node.addEventListener("click", action); return node;
}
function alterCart(id, delta) {
  if (busy || pendingOrder) return;
  const qty = Math.min(99, (cart.get(id) || 0) + delta);
  if (qty <= 0) cart.delete(id); else cart.set(id, qty);
  renderCart();
}
function renderCatalog() {
  $("catalog").replaceChildren();
  state.products.forEach((p) => {
    const card = el("article", undefined, "product");
    const top = el("div", undefined, "product-top"), title = el("div");
    title.append(el("h3", p.name), el("p", p.available > 0 ? `Hasta ${p.available} disponibles con el stock actual` : "Sin insumos suficientes", `availability${p.available ? "" : " sold-out"}`));
    top.append(title, el("span", money(p.price_cents), "price"));
    const bottom = el("div", undefined, "product-bottom"), details = el("details");
    details.append(el("summary", "Receta por unidad"), el("p", p.recipe.map(r => `${r.amount} ${r.unit} de ${r.name.toLowerCase()}`).join(" · ")));
    const add = button("+ Agregar", `Agregar ${p.name}`, () => alterCart(p.id, 1), "add");
    add.disabled = !p.available || busy || Boolean(pendingOrder);
    bottom.append(details, add); card.append(top, bottom); $("catalog").append(card);
  });
}
function renderCart() {
  $("cart").replaceChildren(); let total = 0;
  if (!cart.size) $("cart").append(el("p", "Agrega un producto del catálogo.", "empty"));
  for (const [id, qty] of cart) {
    const product = state?.products.find(p => p.id === id); if (!product) continue;
    total += product.price_cents * qty;
    const row = el("div", undefined, "cart-line"), head = el("div", undefined, "cart-line-head");
    head.append(el("strong", product.name), el("span", money(product.price_cents * qty)));
    const controls = el("div", undefined, "quantity-controls");
    const minus = button("−", `Quitar una unidad de ${product.name}`, () => alterCart(id, -1));
    const plus = button("+", `Añadir una unidad de ${product.name}`, () => alterCart(id, 1));
    const remove = button("Quitar", `Eliminar ${product.name}`, () => { if (!busy && !pendingOrder) { cart.delete(id); renderCart(); } }, "remove");
    [minus, plus, remove].forEach(b => b.disabled = busy || Boolean(pendingOrder));
    controls.append(minus, el("span", String(qty)), plus, remove); row.append(head, controls); $("cart").append(row);
  }
  $("total").textContent = money(total);
  $("confirm").disabled = busy || !cart.size || !state;
  $("confirm").textContent = busy ? "Confirmando…" : pendingOrder ? "Reintentar el mismo envío" : "Confirmar pedido";
  $("note").disabled = busy || Boolean(pendingOrder);
}
function renderStock() {
  $("stock").replaceChildren();
  state.stock.forEach(i => {
    const row = el("tr"), badge = el("span", !i.stock ? "Agotado" : i.stock <= i.low_at ? "Stock bajo" : "Disponible", `stock-badge${!i.stock ? " empty-stock" : i.stock <= i.low_at ? " low" : ""}`);
    const status = el("td"); status.append(badge);
    row.append(el("td", i.name), el("td", `${i.stock} ${i.unit}`), el("td", `${i.low_at} ${i.unit}`), status); $("stock").append(row);
  });
}
function renderSummary() {
  $("order-count").textContent = state.summary.orders; $("sales").textContent = money(state.summary.sales_cents);
  $("feedback-count").textContent = state.feedback.count;
  $("history").replaceChildren();
  if (!state.orders.length) $("history").append(el("p", "Todavía no hay pedidos confirmados hoy.", "empty"));
  state.orders.forEach(o => {
    const card = el("article", undefined, "history-order"), header = el("header");
    header.append(el("strong", `Pedido ${o.id.slice(0, 8)}`), el("strong", money(o.total_cents)));
    card.append(header, el("small", new Date(o.created_at).toLocaleTimeString("es-MX", {hour:"2-digit",minute:"2-digit"})), el("p", o.lines.map(l => `${l.quantity} × ${l.name}`).join(" · ")));
    if (o.note) card.append(el("p", o.note, "order-note"));
    $("history").append(card);
  });
}
async function refresh() {
  try {
    state = await api("/api/state");
    $("business-date").textContent = `TURNO · ${state.business_date} · fecha del servidor`;
    $("connection").textContent = "● Conectado al servidor";
    renderCatalog(); renderStock(); renderSummary(); renderCart();
    return true;
  } catch (error) {
    $("connection").textContent = "Sin conexión · datos sin actualizar";
    if (!state || error.status === 401) notice(error.status === 401 ? error.message : "No se pudo conectar. Mantén abierta la terminal y revisa el enlace de acceso.", true);
    return false;
  }
}
$("confirm").addEventListener("click", async () => {
  if (busy || !cart.size) return;
  busy = true;
  if (!pendingOrder) pendingOrder = {request_id: uuid(), lines: Array.from(cart, ([product_id, quantity]) => ({product_id, quantity})), note: $("note").value};
  sessionStorage.setItem("mochi-pending-order", JSON.stringify(pendingOrder));
  renderCart(); renderCatalog();
  try {
    const result = await api("/api/orders", pendingOrder);
    cart.clear(); $("note").value = ""; pendingOrder = null; sessionStorage.removeItem("mochi-pending-order");
    notice(`Pedido ${result.id.slice(0,8)} confirmado · ${money(result.total_cents)}. Inventario actualizado${result.replayed ? "; el reintento no duplicó la venta" : ""}.`);
    await refresh();
  } catch (error) {
    if (error.status && error.status < 500) { pendingOrder = null; sessionStorage.removeItem("mochi-pending-order"); }
    notice(pendingOrder ? "No se recibió confirmación. Reintenta el mismo envío para comprobar su estado sin duplicar la venta." : error.message, true);
    await refresh();
  } finally { busy = false; renderCart(); renderCatalog(); }
});
function feedbackControls() {
  $("rating").disabled = feedbackBusy || Boolean(pendingFeedback);
  $("comment").disabled = feedbackBusy || Boolean(pendingFeedback);
  $("save-feedback").disabled = feedbackBusy;
  $("save-feedback").textContent = feedbackBusy ? "Guardando…" : pendingFeedback ? "Reintentar valoración" : "Guardar valoración";
}
if (pendingFeedback) { $("rating").value = pendingFeedback.rating; $("comment").value = pendingFeedback.comment; }
feedbackControls();
$("feedback-form").addEventListener("submit", async (event) => {
  event.preventDefault(); if (feedbackBusy) return;
  if (!pendingFeedback) pendingFeedback = {request_id:uuid(),rating:Number($("rating").value),comment:$("comment").value};
  sessionStorage.setItem("mochi-pending-feedback", JSON.stringify(pendingFeedback));
  feedbackBusy = true; feedbackControls();
  try {
    await api("/api/feedback", pendingFeedback);
    pendingFeedback = null; sessionStorage.removeItem("mochi-pending-feedback"); $("feedback-form").reset();
    notice("Valoración guardada. Quedó registrada para revisar el siguiente turno."); await refresh();
  } catch (error) {
    if (error.status && error.status < 500) { pendingFeedback = null; sessionStorage.removeItem("mochi-pending-feedback"); }
    notice(pendingFeedback ? "No se recibió confirmación. Reintenta la misma valoración; no se duplicará." : error.message, true);
  } finally { feedbackBusy = false; feedbackControls(); }
});
document.querySelectorAll(".nav").forEach(button => button.addEventListener("click", () => {
  document.querySelectorAll(".view").forEach(section => section.hidden = section.id !== button.dataset.view);
  document.querySelectorAll(".nav").forEach(b => { b.classList.toggle("active", b === button); if (b === button) b.setAttribute("aria-current","page"); else b.removeAttribute("aria-current"); });
}));
refresh(); setInterval(refresh, 5000);
