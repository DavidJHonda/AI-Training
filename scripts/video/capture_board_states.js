// CDP worker: capture a lesson board at deviceScaleFactor 4 in N+1 highlight
// states (state-0 = none, state-k = item k highlighted) for the highlight-state
// Ken Burns recipe (see README.md). Writes state-*.png + rects.json to OUTDIR.
//
// Usage (drive it like capture-board.js — server + headless chrome already up):
//   node capture_board_states.js PORT DBG LESSON "HEADLINE" "Label1||Label2||..." CANW CANH BANDW OUTDIR [STATES.json]
//
// Without STATES.json: states are 0..N, one per label (whole-card highlight).
// With STATES.json: {"states":[{"panels":["Label"],"elements":["exact text"]},...]}
// — each state rings the named panels (card treatment + label chip) and draws a
// 2.5px ring on each named element (chip/bubble/row/line, matched by exact
// textContent; box-shadow only, so zero layout shift). rects.json then also
// carries an "elements" map for camera targeting.
// An element entry may be {"text": "...", "ring": "#color"} — owner rule
// 2026-08-02: inside an accent-colored container the ring adopts the
// container's accent; bare-string entries keep the purple default.
//
// Item detection: for each label, the innermost element with that exact text is
// the label leaf; the highlight target ("card") is the highest ancestor that
// contains no other label's leaf. Cards with an inline background (real cards)
// get a 3px primary ring; background-less targets (rows in a shared white card,
// e.g. NumberedRows) get a white-filled rounded ring (owner call 2026-08-02: no
// tint — ring on white, matching the card treatment) with margin/padding
// compensation so text never reflows. Labels get the app's chip treatment.
const http = require("http");
const fs = require("fs");
const [PORT, DBG, LESSON, HEADLINE, LABELS, CANW, CANH, BANDW, OUTDIR, STATESJSON] = process.argv.slice(2);
const STATES = STATESJSON ? JSON.parse(fs.readFileSync(STATESJSON, "utf8")).states : null;
const BASE = `http://127.0.0.1:${PORT}/index.html`;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const getJSON = (path) => new Promise((res, rej) => {
  http.get({ host: "127.0.0.1", port: DBG, path }, (r) => {
    let b = ""; r.on("data", (c) => (b += c)); r.on("end", () => res(JSON.parse(b)));
  }).on("error", rej);
});

const COMPOSE = `(function(){
  var headline = ${JSON.stringify(HEADLINE)};
  var labels = ${JSON.stringify(LABELS.split("||"))};
  var divs = Array.prototype.slice.call(document.querySelectorAll("div"));
  var preds = [headline].concat(labels);
  var cands = divs.filter(function(d){ var t = d.textContent || ""; return preds.every(function(p){ return t.indexOf(p) !== -1; }); });
  if (!cands.length) return "NOT FOUND";
  cands.sort(function(a, b){ return a.textContent.length - b.textContent.length; });
  var min = cands[0].textContent.length;
  var depth = function(e){ var d = 0; while ((e = e.parentElement)) d++; return d; };
  var best = cands.filter(function(c){ return c.textContent.length === min; });
  best.sort(function(a, b){ return depth(b) - depth(a); });
  var band = best[0];
  band.style.width = ${Number(BANDW)} + "px";
  band.style.boxSizing = "border-box";
  band.style.marginBottom = "0";
  var wrap = document.createElement("div");
  wrap.style.cssText = "position:fixed;top:0;left:0;width:${Number(CANW)}px;height:${Number(CANH)}px;background:#f6f5fb;display:flex;align-items:center;justify-content:center;z-index:99999;";
  wrap.appendChild(band);
  document.body.appendChild(wrap);
  window.scrollTo(0, 0);
  var leaves = labels.map(function(lb){
    var els = Array.prototype.slice.call(band.querySelectorAll("*")).filter(function(d){
      return d.textContent === lb && !Array.prototype.some.call(d.children, function(c){ return c.textContent === lb; }); });
    return els[0] || null;
  });
  if (leaves.some(function(l){ return !l; })) return "LABEL NOT FOUND";
  window.__items = leaves.map(function(leaf){
    var card = leaf;
    while (card.parentElement && card.parentElement !== band) {
      var p = card.parentElement;
      var holdsOther = leaves.some(function(o){ return o !== leaf && p.contains(o); });
      if (holdsOther) break;
      card = p;
    }
    return { leaf: leaf, card: card,
             leafStyle: leaf.getAttribute("style") || "",
             cardStyle: card.getAttribute("style") || "" };
  });
  var stateSpec = ${JSON.stringify(STATES)};
  var elemTexts = []; var ringColors = {};
  if (stateSpec) stateSpec.forEach(function(s){ (s.elements||[]).forEach(function(e){
    var t = (typeof e === "string") ? e : e.text;
    if (typeof e !== "string" && e.ring) ringColors[t] = e.ring;
    if (elemTexts.indexOf(t) < 0) elemTexts.push(t); }); });
  window.__elems = {}; var missing = [];
  elemTexts.forEach(function(t){
    var els = Array.prototype.slice.call(band.querySelectorAll("*")).filter(function(d){
      return d.textContent === t && !Array.prototype.some.call(d.children, function(c){ return c.textContent === t; }); });
    if (!els.length) { missing.push(t); return; }
    window.__elems[t] = { el: els[0], style: els[0].getAttribute("style") || "" };
  });
  if (missing.length) return "ELEMENT NOT FOUND: " + missing.join(" // ");
  function applyPanel(it) {
    var isCard = (it.card.style.background || "").length > 0;
    if (isCard) {
      it.card.style.boxShadow = (it.card.style.boxShadow ? it.card.style.boxShadow + ", " : "") + "0 0 0 3px #6e51ff";
    } else {
      it.card.style.background = "#fff";
      it.card.style.borderRadius = "12px";
      it.card.style.boxShadow = "0 0 0 3px #6e51ff";
      it.card.style.padding = "18px 16px";
      it.card.style.margin = "0 -16px";
      it.card.style.borderBottom = "none";
    }
    var lc = it.leaf.style.color;
    var chipColor = "#6e51ff", chipBg = "#6e51ff22";
    if (lc && lc.charAt(0) === "#" && lc.length === 7) { chipColor = lc; chipBg = lc + "22"; }
    else if (lc && lc.indexOf("rgb(") === 0) { chipColor = lc; chipBg = lc.replace("rgb(", "rgba(").replace(")", ", 0.13)"); }
    it.leaf.style.background = chipBg;
    it.leaf.style.color = chipColor;
    it.leaf.style.padding = "2px 10px";
    it.leaf.style.borderRadius = "7px";
    it.leaf.style.display = "inline-block";
    it.leaf.style.alignSelf = "flex-start";
  }
  window.__setHL = function(k){
    window.__items.forEach(function(it){
      it.leaf.setAttribute("style", it.leafStyle);
      it.card.setAttribute("style", it.cardStyle);
    });
    Object.keys(window.__elems).forEach(function(t){ window.__elems[t].el.setAttribute("style", window.__elems[t].style); });
    if (stateSpec) {
      var s = stateSpec[k] || {};
      (s.panels || []).forEach(function(lb){ var i = labels.indexOf(lb); if (i >= 0) applyPanel(window.__items[i]); });
      (s.elements || []).forEach(function(en){ var t = (typeof en === "string") ? en : en.text;
        var e = window.__elems[t];
        var rc = ringColors[t] || "#6e51ff";
        e.el.style.boxShadow = (e.el.style.boxShadow ? e.el.style.boxShadow + ", " : "") + "0 0 0 2.5px " + rc; });
    } else if (k > 0) {
      applyPanel(window.__items[k-1]);
    }
    return "HL" + k;
  };
  var r = band.getBoundingClientRect();
  var rects = window.__items.map(function(it){ var b = it.card.getBoundingClientRect();
    return { x: b.x, y: b.y, w: b.width, h: b.height }; });
  var erects = {};
  Object.keys(window.__elems).forEach(function(t){ var b = window.__elems[t].el.getBoundingClientRect();
    erects[t] = { x: b.x, y: b.y, w: b.width, h: b.height }; });
  return JSON.stringify({ band: { x: r.x, y: r.y, w: r.width, h: r.height }, cards: rects, elements: erects });
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
  await send("Emulation.setDeviceMetricsOverride", { width: Number(CANW), height: Number(CANH), deviceScaleFactor: 4, mobile: false });
  await sleep(400);
  const r = await send("Runtime.evaluate", { expression: COMPOSE, returnByValue: true });
  const msg = r.result && r.result.result && r.result.result.value;
  if (!msg || msg === "NOT FOUND" || msg === "LABEL NOT FOUND") { console.error("compose failed: " + msg); ws.close(); process.exit(1); }
  fs.writeFileSync(OUTDIR + "/rects.json", msg);
  console.log("rects: " + msg);
  await sleep(300);
  const n = STATES ? STATES.length - 1 : LABELS.split("||").length;
  for (let k = 0; k <= n; k++) {
    const h = await send("Runtime.evaluate", { expression: `window.__setHL(${k})`, returnByValue: true });
    console.log(h.result && h.result.result && h.result.result.value);
    await sleep(250);
    const shot = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(`${OUTDIR}/state-${k}.png`, Buffer.from(shot.result.data, "base64"));
  }
  ws.close();
  process.exit(0);
})();
