// Driven by scripts/make-lesson-texts.sh. Renders each lesson at ?print=lesson:<id>
// and serializes the DOM to plain markdown (headings, paragraphs, lists) instead of
// printing a styled PDF. TRY IT / LAB / nav / video pill are skipped, so the file is
// pure lesson information for NotebookLM. Usage: node make-lesson-texts.js PORT DBG OUT [id...]
const http = require("http");
const fs = require("fs");
const PORT = process.argv[2] || "8766";
const DBG = process.argv[3] || "9334";
const OUT = process.argv[4] || "lessons";
const only = process.argv.slice(5);
const BASE = "http://127.0.0.1:" + PORT + "/index.html";

const getJSON = (p) => new Promise((res, rej) => {
  http.get("http://127.0.0.1:" + DBG + p, (r) => { let d = ""; r.on("data", (c) => d += c); r.on("end", () => res(JSON.parse(d))); }).on("error", rej);
});
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Runs in the page: walk the packet DOM and emit markdown. Kept as a string so the
// whole thing evaluates in one Runtime.evaluate call.
const EXTRACT = `(function () {
  var root = document.querySelector(".course-packet--content-only") || document.body;
  var SKIP = ".interactive-box--try,.interactive-box--lab,.lesson-mechanics,.no-print,nav,button,script,style";
  function skippable(el) { return el.matches && el.matches(SKIP); }
  function inline(node) {
    var t = "";
    node.childNodes.forEach(function (c) {
      if (c.nodeType === 3) { t += c.textContent; return; }
      if (c.nodeType !== 1 || skippable(c)) return;
      var tag = c.tagName;
      if (tag === "BR") { t += " "; return; }
      if (tag === "IMG" || tag === "SVG" || tag === "CANVAS" || tag === "VIDEO") return;
      var inner = inline(c);
      if (!inner.trim()) { t += inner; return; }
      // Pad between adjacent element fragments (e.g. a list-number span then a text
      // span) so words don't run together; never pad before punctuation.
      if (t && !/\\s$/.test(t) && /^[A-Za-z0-9(“"']/.test(inner.trim()) && c.previousSibling && c.previousSibling.nodeType === 1) t += " ";
      if (tag === "STRONG" || tag === "B") t += "**" + inner.trim() + "**";
      else if (tag === "EM" || tag === "I") t += "*" + inner.trim() + "*";
      else if (tag === "CODE") t += "\`" + inner.trim() + "\`";
      else t += inner;
    });
    return t;
  }
  function clean(s) { return s.replace(/\\s+/g, " ").trim(); }
  var out = [];
  function walk(el) {
    if (el.nodeType !== 1 || skippable(el)) return;
    var cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") return;
    var tag = el.tagName, s;
    if (/^H[1-6]$/.test(tag)) { s = clean(inline(el)); if (s) out.push({ t: "h", l: +tag[1], s: s }); return; }
    if (tag === "P") { s = clean(inline(el)); if (s) out.push({ t: "p", s: s }); return; }
    if (tag === "LI") { s = clean(inline(el)); if (s) out.push({ t: "li", s: s }); return; }
    if (tag === "IMG" || tag === "SVG" || tag === "CANVAS" || tag === "VIDEO") return;
    if (tag === "UL" || tag === "OL" || tag === "TABLE" || tag === "TBODY" || tag === "TR") {
      Array.prototype.forEach.call(el.children, walk); return;
    }
    // Mixed content (text nodes alongside child elements, e.g. KeyInsight): one paragraph.
    var hasText = Array.prototype.some.call(el.childNodes, function (c) { return c.nodeType === 3 && c.textContent.trim(); });
    if (el.childElementCount > 0 && hasText) { s = clean(inline(el)); if (s) out.push({ t: "p", s: s }); return; }
    if (el.childElementCount === 0) {
      s = clean(el.textContent || "");
      if (!s) return;
      // Uppercase leaf blocks are kickers/eyebrows -> subheadings.
      if (cs.textTransform === "uppercase") out.push({ t: "h", l: 2, s: s });
      else out.push({ t: "p", s: s });
      return;
    }
    Array.prototype.forEach.call(el.children, walk);
  }
  walk(root);
  var md = [];
  out.forEach(function (b) {
    if (b.t === "h") md.push("\\n" + "#".repeat(Math.min(6, b.l)) + " " + b.s + "\\n");
    else if (b.t === "li") md.push("- " + b.s);
    else md.push(b.s + "\\n");
  });
  return md.join("\\n").replace(/(\\d)\\.(?=[A-Za-z])/g, "$1. ").replace(/\\n{3,}/g, "\\n\\n").trim() + "\\n";
})()`;

(async () => {
  const target = (await getJSON("/json")).find((t) => t.type === "page");
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  let id = 0; const pend = {};
  const send = (m, p = {}) => new Promise((r) => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p })); });
  const ev = (e) => send("Runtime.evaluate", { expression: e, returnByValue: true }).then((r) => r.result && r.result.result && r.result.result.value);
  await new Promise((r) => ws.addEventListener("open", r));
  ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; } });

  await send("Page.enable"); await send("Runtime.enable");

  await send("Page.navigate", { url: BASE }); await sleep(2500);
  let ids = JSON.parse(await ev("JSON.stringify(SECTION_GROUPS.flatMap(function(g){return g.sections;}))"));
  if (only.length) ids = only;
  console.log("Generating " + ids.length + " lesson text file(s) into " + OUT + " ...");

  for (const lid of ids) {
    await send("Page.navigate", { url: BASE + "?print=lesson:" + lid }); await sleep(2200);
    const md = await ev(EXTRACT);
    const fname = (await ev('lessonSlug("' + lid + '")')) || lid;
    if (!md || md.length < 200) { console.log("  !! " + fname + ".md came out suspiciously short (" + (md ? md.length : 0) + " chars) — check it"); }
    fs.writeFileSync(OUT + "/" + fname + ".md", md || "");
    console.log("  " + fname + ".md  (" + (md ? md.length : 0) + " chars)");
  }
  ws.close();
  process.exit(0);
})().catch((e) => { console.error(e); process.exit(1); });
