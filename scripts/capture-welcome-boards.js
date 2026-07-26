// One-off board capture for the Welcome lesson — do not run directly, use the .sh.
//
// capture-board.sh wraps its target in a white composition card sized for a single
// compact element. Welcome's two content boards are full-bleed lesson blocks (the
// peach quote card, and the five-step ShowcaseBox), and the white card makes both
// worse. This composes the element straight onto the page background at 1600x900,
// matching lessons/welcome-3-close.jpg.
//
// The five-step grid renders 3+2 here because .numcols-3 breaks at 700px and this
// viewport is 800 — the same shape a reader sees on the page. Keep those in step.
const http = require("http");
const fs = require("fs");
const [PORT, DBG, OUTDIR] = process.argv.slice(2);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const getJSON = (p) => new Promise((res, rej) => {
  http.get({ host: "127.0.0.1", port: DBG, path: p }, (r) => {
    let b = ""; r.on("data", (c) => (b += c)); r.on("end", () => res(JSON.parse(b)));
  }).on("error", rej);
});

// width: CSS px for the composed block inside the 800x450 canvas.
const BOARDS = [
  // "WHY GO DEEPER?" pulls the match up to the Illustration wrapper — without it the
  // innermost hit is the bare serif text, losing the peach card and the eyebrow.
  { out: "welcome-1-why-go-deeper.jpg", width: 660,
    find: ["WHY GO DEEPER?", "Everyone has AI.", "be smarter than the tool."] },
  { out: "welcome-2-your-path.jpg", width: 720,
    find: ["Here’s your path.", "Work", "Build", "personal edge."] },
];

const compose = (preds, width) => `(function(){
  var host = document.getElementById("__boardwrap");
  if (host) host.remove();
  var preds = ${JSON.stringify(preds)};
  var divs = Array.prototype.slice.call(document.querySelectorAll("div"));
  var cands = divs.filter(function(d){ var t=d.textContent||""; return preds.every(function(p){return t.indexOf(p)!==-1;}); });
  if (!cands.length) return "NOT FOUND";
  cands.sort(function(a,b){ return a.textContent.length - b.textContent.length; });
  var min = cands[0].textContent.length;
  var depth = function(e){ var d=0; while ((e=e.parentElement)) d++; return d; };
  var best = cands.filter(function(c){ return c.textContent.length === min; });
  best.sort(function(a,b){ return depth(b)-depth(a); });
  var el = best[0];
  var pageBg = getComputedStyle(document.body).backgroundColor || "#f2f1f7";
  var slot = document.createElement("div");
  slot.style.cssText = "width:${width}px;";
  el.style.margin = "0";
  slot.appendChild(el);
  var wrap = document.createElement("div");
  wrap.id = "__boardwrap";
  wrap.style.cssText = "position:fixed;top:0;left:0;width:800px;height:450px;background:"+pageBg+
    ";display:flex;align-items:center;justify-content:center;z-index:99999;";
  wrap.appendChild(slot);
  document.body.appendChild(wrap);
  window.scrollTo(0,0);
  var h = slot.getBoundingClientRect().height;
  if (h > 410) { slot.style.zoom = String(410/h); }
  return "OK h=" + Math.round(h) + (h > 410 ? " (scaled " + (410/h).toFixed(2) + ")" : " (fits)");
})()`;

(async () => {
  const t = (await getJSON("/json")).find((x) => x.type === "page");
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  let id = 0; const pend = {};
  const send = (m, p = {}) => new Promise((r) => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p })); });
  await new Promise((r) => ws.addEventListener("open", r));
  ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; } });
  await send("Page.enable"); await send("Runtime.enable");

  for (const b of BOARDS) {
    // Reload per board: composing moves the element out of the document.
    await send("Page.navigate", { url: `http://127.0.0.1:${PORT}/index.html?print=lesson:welcome` });
    await sleep(2800);
    await send("Emulation.setDeviceMetricsOverride", { width: 800, height: 450, deviceScaleFactor: 2, mobile: false });
    await sleep(400);
    const r = await send("Runtime.evaluate", { expression: compose(b.find, b.width), returnByValue: true });
    const msg = r.result && r.result.result && r.result.result.value;
    console.log(`  ${b.out}: ${msg}`);
    if (msg === "NOT FOUND") { ws.close(); process.exit(1); }
    await sleep(400);
    const shot = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(`${OUTDIR}/${b.out.replace(/\.jpg$/, ".png")}`, Buffer.from(shot.result.data, "base64"));
  }
  ws.close(); process.exit(0);
})();
