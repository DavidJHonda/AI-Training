// Page-faithful board capture — do not run directly, use the .sh.
//
// capture-board.sh wraps its target in a white composition card sized for a single
// compact element. Some lesson boards are full-bleed page blocks (a peach Illustration
// band, a lavender ShowcaseBox), and the white card doesn't just look different — it
// DROPS the band and the eyebrow, so the video gets a board the reader never sees.
// That is what was wrong with opener-work-1-refrain (2026-07-28): a white card where
// the page shows a peach Illustration titled "WHAT MAKES AI USE GOOD?".
//
// This composes the element straight onto the page background at 1600x900 instead,
// keeping whatever wrapper the page gives it, and matching the close boards.
//
// Add a lesson by adding a BOARDS entry: the section id (for ?print=lesson:<id>) and
// the find strings. Match strings from opposite ends of the block — the composer takes
// the INNERMOST element containing all of them, so one string usually grabs a heading.
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

// section: the id used by ?print=lesson:<id>, NOT the asset slug.
// width:   CSS px for the composed block inside the 800x450 canvas.
const BOARDS = [
  // "WHY GO DEEPER?" pulls the match up to the Illustration wrapper — without it the
  // innermost hit is the bare serif text, losing the peach card and the eyebrow.
  { section: "welcome", out: "welcome-1-why-go-deeper.jpg", width: 660,
    find: ["WHY GO DEEPER?", "Everyone has AI.", "be smarter than the tool."] },
  { section: "welcome", out: "welcome-2-your-path.jpg", width: 720,
    find: ["Here’s your path.", "Work", "Build", "personal edge."] },
  // The two tool pills live in the same lavender ShowcaseBox as the headline and the
  // intro line; matching all three forces the band, not just the pill row.
  { section: "welcome", out: "welcome-3-what-youll-need.jpg", width: 520,
    find: ["What you’ll need", "Nothing to install.", "free version"] },
  // Same Illustration-wrapper trick as welcome-1: lead with the eyebrow or the capture
  // collapses to the bare serif lines and loses the peach band the reader sees.
  { section: "openerworkwith", out: "opener-work-1-refrain.jpg", width: 740,
    find: ["WHAT MAKES AI USE GOOD?", "Don’t just ask.", "It multiplies it."] },

  // ai-is-math, recut 2026-07-28 after the flow rework. Four boxes now share one
  // shape (THE QUESTION card, then Possible Outcomes, then The Math), so each find
  // list needs a string unique to its own box: the bare formula carries no numbers,
  // and the three worked examples are told apart by question line plus result.
  { section: "aiismath", out: "ai-is-math-1-formula.jpg", width: 660,
    find: ["The Math", "Ways it happens", "Total outcomes", "Probability"] },
  { section: "aiismath", out: "ai-is-math-2-one-coin.jpg", width: 700,
    find: ["Toss a coin. How likely", "Possible Outcomes", "Probability (50%)"] },
  { section: "aiismath", out: "ai-is-math-3-two-coins.jpg", width: 720,
    find: ["Toss 2 coins. How likely is it that", "Possible Outcomes", "Probability (25%)"] },
  { section: "aiismath", out: "ai-is-math-4-update.jpg", width: 720,
    find: ["Someone peeks", "Possible Outcomes", "Probability (50%)"] },
  // Three stacked cards run tall; a wider stage keeps the text big instead of
  // shrinking it to 0.50 and leaving the portrait shape that makes the engine pan.
  { section: "aiismath", out: "ai-is-math-5-tying.jpg", width: 1180, vw: 1280,
    find: ["It’s May 21st", "Autoregressive Generation", "Picking the next word"] },

  // learn-with-ai, 2026-07-28: the kit's 3-habits board was TITLES ONLY, so the video
  // recited five habit names and taught none of them. This is the extended block with
  // each habit's reason. It runs wide rather than tall, so it needs the roomier stage.
  { section: "studying", out: "learn-with-ai-3-habits.jpg", width: 1180, vw: 1280,
    find: ["One notebook per subject", "Trace it back to learn it", "Reading the original material"] },

  // opener-work close: the old spec matched "replace your thinking||multiplies it",
  // which ALSO appears inside the refrain Illustration, so the capture grabbed that
  // instead and shipped a kit board with no pill at all. Leading with the PILL text
  // (one contiguous string, only present in the CloseBoard) forces the right element.
  { section: "openerworkwith", out: "opener-work-3-close.jpg", width: 560, vw: 704,
    find: ["Don\u2019t just use AI. Work with it.", "It doesn\u2019t replace your thinking. It multiplies it."] },
];

const compose = (preds, width, vw) => `(function(){
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
  wrap.style.cssText = "position:fixed;top:0;left:0;width:${vw}px;height:${Math.round(vw*9/16)}px;background:"+pageBg+
    ";display:flex;align-items:center;justify-content:center;z-index:99999;";
  wrap.appendChild(slot);
  document.body.appendChild(wrap);
  window.scrollTo(0,0);
  var cap = ${Math.round(vw*9/16) - 40};
  var h = slot.getBoundingClientRect().height;
  if (h > cap) { slot.style.zoom = String(cap/h); }
  return "OK h=" + Math.round(h) + (h > cap ? " (scaled " + (cap/h).toFixed(2) + ")" : " (fits)");
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
    await send("Page.navigate", { url: `http://127.0.0.1:${PORT}/index.html?print=lesson:${b.section}` });
    await sleep(2800);
    const vw = b.vw || 800;
    await send("Emulation.setDeviceMetricsOverride", { width: vw, height: Math.round(vw * 9 / 16), deviceScaleFactor: 1600 / vw, mobile: false });
    await sleep(400);
    const r = await send("Runtime.evaluate", { expression: compose(b.find, b.width, vw), returnByValue: true });
    const msg = r.result && r.result.result && r.result.result.value;
    console.log(`  ${b.out}: ${msg}`);
    if (msg === "NOT FOUND") { ws.close(); process.exit(1); }
    await sleep(400);
    const shot = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(`${OUTDIR}/${b.out.replace(/\.jpg$/, ".png")}`, Buffer.from(shot.result.data, "base64"));
  }
  ws.close(); process.exit(0);
})();
