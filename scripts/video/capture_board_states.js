// CDP worker: capture a lesson board at deviceScaleFactor 4 in N+1 highlight
// states (state-0 = none, state-k = item k highlighted) for the highlight-state
// Ken Burns recipe (see README.md). Writes state-*.png + rects.json to OUTDIR.
//
// Usage (drive it like capture-board.js — server + headless chrome already up):
//   node capture_board_states.js PORT DBG LESSON "HEADLINE" "Label1||Label2||..." CANW CANH BANDW OUTDIR [STATES.json]
//
// Without STATES.json: states are 0..N, one per label (whole-card highlight).
// With STATES.json: {"states":[{"panels":["Label"],"elements":["exact text"]},...]}
// — each state rings the named panels (outline only) and draws a
// 2.5px ring on each named element (chip/bubble/row/line, matched by exact
// textContent; box-shadow only, so zero layout shift). rects.json then also
// carries an "elements" map for camera targeting.
// An element entry may be {"text": "...", "ring": "#color"} — owner rule
// 2026-08-02: inside an accent-colored container the ring adopts the
// container's accent; bare-string entries keep the purple default.
// An element entry may add {"row": true}: the ring target walks UP from the
// innermost text match to the outermost ancestor with the SAME textContent —
// the bullet-row case where a CSS-dot span carries no text, so the row div and
// its text span match identically and innermost-wins rings the text alone,
// leaving the dot outside the boundary (owner-rejected, evaluate-the-results
// 2026-08-03; flagged as "needs the capture script" in README).
// An element entry may add {"mark": true}: the target is a SENTENCE (or any
// substring) inside a paragraph, not a DOM element. At compose time the text
// node containing it is split and the match wrapped in a neutral inline span
// (no style — zero visual change, zero layout shift); the active state draws
// an outline only. It never shades the text or its background.
// A panel entry may likewise be {"label": "...", "ring": "#color"} — owner rule
// 2026-08-03 (which-app): a card with its own accent color gets its accent as
// the ring, not the primary purple; bare-string panels keep the default.
//
// Item detection: for each label, the innermost element with that exact text is
// the label leaf; the highlight target ("card") is the highest ancestor that
// contains no other label's leaf. All targets get an outline without changing
// text, backgrounds, spacing, or layout. Existing shadows are retained.
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
  // WRAP_UP: walk N ancestors up from the innermost match, so the capture keeps
  // the lesson's own wrapper (e.g. the ShowcaseBox lavender band) instead of
  // lifting the inner grid onto the canvas — owner rule 2026-08-04: source
  // boards are the actual lesson boards, no reformatting.
  var up = ${Number(process.env.WRAP_UP || 0)};
  for (var u = 0; u < up; u++) {
    if (band.parentElement && band.parentElement !== document.body) band = band.parentElement;
  }
  // BANDW 0 = NATURAL width (owner rule 2026-08-04): pin the width the lesson
  // actually renders. The print page this script captures from has no shell, so
  // clamp the measured width to the app column every student sees: the course
  // root caps at maxWidth 1080 with 32px side padding, and #main-content adds
  // 56px padding + 1px border => 1080 - 64 - 112 - 2 = 902. If the shell's
  // widths change in index.html, update APP_COLUMN here. Overriding to any
  // other width re-wraps the text and ships a board that differs from the
  // lesson's (owner-flagged, evaluate-the-results 2026-08-04).
  var APP_COLUMN = 902;
  var bw = ${Number(BANDW)} > 0 ? ${Number(BANDW)} : Math.min(band.getBoundingClientRect().width, APP_COLUMN);
  band.style.width = bw + "px";
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
  var elemTexts = []; var ringColors = {}; var rowFlags = {}; var markFlags = {};
  if (stateSpec) stateSpec.forEach(function(s){ (s.elements||[]).forEach(function(e){
    var t = (typeof e === "string") ? e : e.text;
    if (typeof e !== "string" && e.ring) ringColors[t] = e.ring;
    if (typeof e !== "string" && e.row) rowFlags[t] = true;
    if (typeof e !== "string" && e.mark) markFlags[t] = true;
    if (elemTexts.indexOf(t) < 0) elemTexts.push(t); }); });
  window.__elems = {}; var missing = [];
  elemTexts.forEach(function(t){
    if (markFlags[t]) {
      var walker = document.createTreeWalker(band, NodeFilter.SHOW_TEXT);
      var node = null, at = -1, n;
      while ((n = walker.nextNode())) {
        var i = n.textContent.indexOf(t);
        if (i >= 0) { node = n; at = i; break; }
      }
      if (!node) { missing.push(t); return; }
      var range = document.createRange();
      range.setStart(node, at); range.setEnd(node, at + t.length);
      var span = document.createElement("span");
      range.surroundContents(span);
      window.__elems[t] = { el: span, style: "" };
      return;
    }
    var els = Array.prototype.slice.call(band.querySelectorAll("*")).filter(function(d){
      return d.textContent === t && !Array.prototype.some.call(d.children, function(c){ return c.textContent === t; }); });
    if (!els.length) { missing.push(t); return; }
    var el = els[0];
    if (rowFlags[t]) {
      while (el.parentElement && el.parentElement !== band && el.parentElement.textContent === t) el = el.parentElement;
    }
    window.__elems[t] = { el: el, style: el.getAttribute("style") || "" };
  });
  if (missing.length) return "ELEMENT NOT FOUND: " + missing.join(" // ");
  function applyPanel(it, ringColor) {
    var ring = ringColor || "#6e51ff";
    // Outline only: preserve all heading, background, padding, and margin styles.
    it.card.style.boxShadow = (it.card.style.boxShadow ? it.card.style.boxShadow + ", " : "") + "0 0 0 3px " + ring;
    it.card.style.position = "relative";
    it.card.style.zIndex = "3";
  }
  window.__setHL = function(k){
    window.__items.forEach(function(it){
      it.leaf.setAttribute("style", it.leafStyle);
      it.card.setAttribute("style", it.cardStyle);
    });
    Object.keys(window.__elems).forEach(function(t){ window.__elems[t].el.setAttribute("style", window.__elems[t].style); });
    if (stateSpec) {
      var s = stateSpec[k] || {};
      (s.panels || []).forEach(function(pn){
        var lb = (typeof pn === "string") ? pn : pn.label;
        var i = labels.indexOf(lb);
        if (i >= 0) applyPanel(window.__items[i], (typeof pn === "string") ? null : pn.ring); });
      (s.elements || []).forEach(function(en){ var t = (typeof en === "string") ? en : en.text;
        var e = window.__elems[t];
        var rc = ringColors[t] || "#6e51ff";
        // outline+offset, not box-shadow: the shadow ring hugs the text box so
        // glyphs touch the line (owner-flagged 2026-08-02). outline-offset
        // paints the ring outside the bounds with breathing room, zero layout
        // shift; borderRadius on a bg-less div shifts nothing either.
        e.el.style.outline = "2.5px solid " + rc;
        e.el.style.outlineOffset = "6px";
        e.el.style.borderRadius = "6px";
        // Same paint-order fix as panels: the offset pushes the ring outside
        // the element's bounds, where a following sibling's background can
        // cover it (owner-flagged 2026-08-05, tutor-card section ring).
        e.el.style.position = "relative";
        e.el.style.zIndex = "3"; });
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
