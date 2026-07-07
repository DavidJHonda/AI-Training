// CDP worker for capture-board.sh — do not run directly.
// Loads a lesson, finds the innermost element containing ALL the given strings,
// composes it on the standard board canvas (page bg + centered white card, 800x450
// CSS at deviceScaleFactor 2 = 1600x900 px), and screenshots it.
const http = require("http");
const fs = require("fs");
const [PORT, DBG, LESSON, PREDS, OUTPNG, TITLE, CARDW] = process.argv.slice(2);
const BASE = `http://127.0.0.1:${PORT}/index.html`;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const getJSON = (path) => new Promise((res, rej) => {
  http.get({ host: "127.0.0.1", port: DBG, path }, (r) => {
    let b = ""; r.on("data", (c) => (b += c)); r.on("end", () => res(JSON.parse(b)));
  }).on("error", rej);
});

const COMPOSE = `(function(){
  var preds = ${JSON.stringify(PREDS.split("||"))};
  var divs = Array.prototype.slice.call(document.querySelectorAll("div"));
  var cands = divs.filter(function(d){ var t = d.textContent || ""; return preds.every(function(p){ return t.indexOf(p) !== -1; }); });
  if (!cands.length) return "NOT FOUND";
  // Innermost match: shortest textContent, then greatest DOM depth (skips
  // padded wrappers that would otherwise squeeze grids into one column).
  cands.sort(function(a, b){ return a.textContent.length - b.textContent.length; });
  var min = cands[0].textContent.length;
  var depth = function(e){ var d = 0; while ((e = e.parentElement)) d++; return d; };
  var best = cands.filter(function(c){ return c.textContent.length === min; });
  best.sort(function(a, b){ return depth(b) - depth(a); });
  var el = best[0];
  var card = document.createElement("div");
  card.style.cssText = "background:#fff;border-radius:14px;box-shadow:0 8px 22px rgba(14,10,31,0.05);width:${Number(CARDW)}px;padding:24px 28px;box-sizing:border-box;";
  var title = ${JSON.stringify(TITLE || "")};
  if (title) {
    var h = document.createElement("div");
    h.style.cssText = 'font-family:"Plus Jakarta Sans",system-ui,sans-serif;font-size:17px;font-weight:800;color:#0e0a1f;letter-spacing:-0.01em;margin-bottom:14px;';
    h.textContent = title;
    card.appendChild(h);
  }
  el.style.marginBottom = "0";
  card.appendChild(el);
  var wrap = document.createElement("div");
  wrap.style.cssText = "position:fixed;top:0;left:0;width:800px;height:450px;background:#f6f5fb;display:flex;align-items:center;justify-content:center;z-index:99999;";
  wrap.appendChild(card);
  document.body.appendChild(wrap);
  window.scrollTo(0, 0);
  var rh = card.getBoundingClientRect().height;
  if (rh > 434) card.style.zoom = String(434 / rh);
  return "OK card-height=" + Math.round(rh) + (rh > 434 ? " (zoomed to fit — consider a wider card or a one-off page)" : "");
})()`;

(async () => {
  const target = (await getJSON("/json")).find((t) => t.type === "page");
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  let id = 0; const pend = {};
  const send = (m, p = {}) => new Promise((r) => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p })); });
  await new Promise((r) => ws.addEventListener("open", r));
  ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; } });
  await send("Page.enable"); await send("Runtime.enable");
  await send("Page.navigate", { url: BASE + "?print=lesson:" + LESSON }); await sleep(2800);
  await send("Emulation.setDeviceMetricsOverride", { width: 800, height: 450, deviceScaleFactor: 2, mobile: false });
  await sleep(400);
  const r = await send("Runtime.evaluate", { expression: COMPOSE, returnByValue: true });
  const msg = r.result && r.result.result && r.result.result.value;
  console.log("  " + msg);
  if (msg === "NOT FOUND") { ws.close(); process.exit(1); }
  await sleep(500);
  const shot = await send("Page.captureScreenshot", { format: "png" });
  fs.writeFileSync(OUTPNG, Buffer.from(shot.result.data, "base64"));
  ws.close();
  process.exit(0);
})();
