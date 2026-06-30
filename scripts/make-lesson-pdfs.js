// Driven by scripts/make-lesson-pdfs.sh. Renders each lesson at ?print=lesson:<id>
// (content only: no TRY IT / LAB / nav) and prints it to a SINGLE continuous-height
// PDF page so no box is ever split across a page break. Text stays selectable for
// NotebookLM. Usage (via the .sh wrapper): node make-lesson-pdfs.js PORT DBG OUT [id...]
const http = require("http");
const fs = require("fs");
const PORT = process.argv[2] || "8765";
const DBG = process.argv[3] || "9333";
const OUT = process.argv[4] || "packets/lessons";
const only = process.argv.slice(5);
const BASE = "http://127.0.0.1:" + PORT + "/index.html";
const WIDTH = 960; // CSS px the lesson lays out at (paperWidth = WIDTH/96 in)

const getJSON = (p) => new Promise((res, rej) => {
  http.get("http://127.0.0.1:" + DBG + p, (r) => { let d = ""; r.on("data", (c) => d += c); r.on("end", () => res(JSON.parse(d))); }).on("error", rej);
});
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const target = (await getJSON("/json")).find((t) => t.type === "page");
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  let id = 0; const pend = {};
  const send = (m, p = {}) => new Promise((r) => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method: m, params: p })); });
  const ev = (e) => send("Runtime.evaluate", { expression: e, returnByValue: true }).then((r) => r.result && r.result.result && r.result.result.value);
  await new Promise((r) => ws.addEventListener("open", r));
  ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; } });

  await send("Page.enable"); await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride", { width: WIDTH, height: 1400, deviceScaleFactor: 1, mobile: false });

  // Pull the lesson id list from the live SECTION_GROUPS (openers included; each gets a
  // distinct PDF name via lessonSlug's OPENER_PDF_NAMES map).
  await send("Page.navigate", { url: BASE }); await sleep(2500);
  let ids = JSON.parse(await ev("JSON.stringify(SECTION_GROUPS.flatMap(function(g){return g.sections;}))"));
  if (only.length) ids = only;
  console.log("Generating " + ids.length + " lesson PDF(s) into " + OUT + " ...");

  for (const lid of ids) {
    await send("Page.navigate", { url: BASE + "?print=lesson:" + lid }); await sleep(2200);
    await send("Emulation.setEmulatedMedia", { media: "print" });
    // Override the global @page { margin: 1.6cm } so the page is pure content height
    // (otherwise the CSS margin shrinks the printable area and content spills to p2).
    await ev("(function(){var s=document.createElement('style');s.textContent='@page{margin:0}';document.head.appendChild(s);})()");
    // Wait for images to finish loading/laying out, else the measured height runs
    // short of the real print height and a sliver spills onto a 2nd page.
    for (let k = 0; k < 30; k++) {
      const ready = await ev('Array.prototype.every.call(document.images, function(i){return i.complete && i.naturalHeight>0;})');
      if (ready) break;
      await sleep(200);
    }
    await sleep(300);
    const h = await ev('Math.ceil(Math.max(document.body.scrollHeight, (document.querySelector(".course-packet")||document.body).getBoundingClientRect().bottom))');
    const H = (h || 1200) + 40; // buffer so nothing spills to a 2nd page
    const pdf = await send("Page.printToPDF", { printBackground: true, marginTop: 0, marginBottom: 0, marginLeft: 0, marginRight: 0, paperWidth: WIDTH / 96, paperHeight: H / 96, preferCSSPageSize: false });
    var fname = (await ev('lessonSlug("' + lid + '")')) || lid; // filename = lesson title slug
    fs.writeFileSync(OUT + "/" + fname + ".pdf", Buffer.from(pdf.result.data, "base64"));
    await send("Emulation.setEmulatedMedia", { media: "" });
    console.log("  " + fname + ".pdf  (" + H + "px tall)");
  }
  ws.close();
  process.exit(0);
})().catch((e) => { console.error(e); process.exit(1); });
