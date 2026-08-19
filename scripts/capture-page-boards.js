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
  // Welcome uses the same navy-and-gold creed treatment as the five opener lessons.
  // Matching the eyebrow and closing keeps the full shared OpenerCreed wrapper.
  { section: "welcome", out: "welcome-1-why-go-deeper.jpg", width: 660,
    find: ["WHY GO DEEPER?", "Everyone has AI.", "be smarter than the tool."] },
  { section: "welcome", out: "welcome-2-your-path.jpg", width: 720,
    find: ["Here’s your path.", "Work", "Build", "personal edge."] },
  // The three toolkit cards live in the same lavender ShowcaseBox as the headline.
  // Match the heading plus every card so the capture keeps the complete course setup.
  { section: "welcome", out: "welcome-3-what-youll-need.jpg", width: 1180, vw: 1280,
    find: ["Your course toolkit", "A computer", "ChatGPT for Teens", "Google account"] },
  // Same Illustration-wrapper trick as welcome-1: lead with the eyebrow or the capture
  // collapses to the bare serif lines and loses the peach band the reader sees.
  { section: "openerworkwith", out: "opener-work-1-refrain.jpg", width: 740,
    find: ["WHAT MAKES AI USE GOOD?", "Don’t just ask.", "It multiplies it."] },
  // Third instance of the same trick. This board shipped as bare serif lines on the
  // generic white composition card — no eyebrow, no peach band — because it was cut
  // with capture-board.sh instead of from the page. Section id is openerfoundations.
  { section: "openerfoundations", out: "opener-understand-1-kind.jpg", width: 740,
    find: ["WHAT KIND OF THING IS AI?", "It’s not magic.", "it’s its own kind of thing."] },

  // AI Is Math boards 1–5 are now deterministic 1600×900 boards built by
  // render_ai_is_math_board_alternatives.py. Do not recapture their accessible-only
  // HTML fallbacks here or the small legacy layouts will overwrite the canonicals.

  // learn-with-ai, 2026-07-28: the kit's 3-habits board was TITLES ONLY, so the video
  // recited five habit names and taught none of them. This is the extended block with
  // each habit's reason. It runs wide rather than tall, so it needs the roomier stage.
  { section: "studying", out: "learn-with-ai-3-habits.jpg", width: 1180, vw: 1280,
    find: ["One notebook per subject", "Trace it back to learn it", "Reading the original material"] },

  // NO CLOSE BOARDS BELONG IN THIS FILE (2026-07-30). Every close board in the
  // catalogue is generated from CLOSE_BOARDS by scripts/video/make_close_board.py,
  // the owner standard of 2026-07-18: 3840x2160, pill auto-fitted to 0.563 of frame
  // width. opener-work-3-close, training-close and where-ai-works-best-5-close used
  // to be captured here at 560/704 and were removed, because a capture at a fixed
  // stage cannot hold the pill fraction constant across different pill lengths --
  // which is the whole point of the standard. Re-adding one silently downgrades that
  // board to 1600x900 and knocks its pill off 56%.


  // tokens: the UN grid, the lesson's own answer to "why chunks at all". It was
  // never captured, so the video argued for reusable chunks with nothing on screen.
  // "Plus thousands more" is the only string unique to the box — the un/believable
  // pairs also appear in the body paragraph just above it.
  // Narrow slot on the default stage on purpose: at the roomy 1180/1280 used by the
  // tall boards, twelve short chips land in one row and the block fills barely half
  // the frame. Forcing the wrap to three rows fills it the way the other kit boards do.
  { section: "tokens", out: "tokens-1-chunks.jpg", width: 640,
    find: ["One chunk, thousands of words", "Plus thousands more", "unplug"] },

  // tokens: tokenization defined. The video's 1:26-1:47 narration beat is strong
  // but its screen shows junk lettering; the definition paragraph became this board
  // so the kit can put the real content under the real words. Board 2 in the kit order.
  // wrapUp 1: the "your words → …" header row was cut 2026-08-06, so the innermost
  // match is now the card grid — walk up to keep the lavender band (owner rule:
  // boards match the page design).
  { section: "tokens", out: "tokens-2-tokenization.jpg", width: 640, wrapUp: 1,
    find: ["no AI involved", "the space before a word"] },

  // critical-thinking: the kit board was titles-only ("Five habits. Each one is a
  // question you ask.") so the video recited five question names and taught none of
  // them. This is the lesson's own block, each habit with the reason under it.
  { section: "critical", out: "critical-thinking-4-five-questions.jpg", width: 1180, vw: 1280,
    find: ["Is it actually right?", "What\u2019s my call?", "the consequences are yours"] },

  // evaluate-the-results: same problem, but the lesson block is too tall for one
  // frame, so it splits the way the lesson reads. Steps 1-3 are the seconds-long
  // tier; step 4 is the decision gate; step 5 already exists as 2-dig.
  { section: "evaluating", out: "evaluate-the-results-1-steps.jpg", width: 1180, vw: 1280,
    keep: [0, 4],
    find: ["How you evaluate the results", "This might sound obvious", "Leave the chat."] },
  { section: "evaluating", out: "evaluate-the-results-2-decide.jpg", width: 1180, vw: 1280,
    keep: [4, 5],
    find: ["How you evaluate the results", "This might sound obvious", "Leave the chat."] },

  // The five trap lessons share one two-column comparison block, and its grid is
  // repeat(auto-fit, minmax(min(100%, 340px), 1fr)) in all five — so it needs roughly
  // 700px of inner width to stay two columns, and silently stacks below that. Cut
  // through a narrow slot, mind-trap / engagement-trap / flattery-trap collapsed to
  // one column AND then got scaled down to fit 900px tall, which is why their type
  // was so much smaller than support-trap's and fake-trap's. The wide stage keeps the
  // two columns the lesson actually shows. Never cut one of these narrow.
  { section: "mindtrap", out: "mind-trap-1-answers.jpg", width: 1180, vw: 1280, card: true,
    find: ["Should I go to the University of Michigan or Indiana University?", "Your Mom", "Searched eighteen years of knowing you"] },
  { section: "engagementtrap", out: "engagement-trap-1-choice.jpg", width: 1180, vw: 1280, card: true,
    find: ["How tall is Mount Everest?", "You end the conversation", "The Engagement Trap"] },
  { section: "flattery", out: "flattery-trap-1-responses.jpg", width: 1180, vw: 1280, card: true,
    find: ["The American Dream is something that many people have thought about", "The Flattery Trap", "What you needed"] },

  // questions-matter: the kit's 3-qualities board was the TRY IT quiz caught in its
  // answered state — three red NOT QUITE cards and one green CORRECT, i.e. an answer
  // key, not a teaching board. This is the lesson's own four-qualities block, each
  // quality with its reason and its bad/better pair. "Homework doesn't help students
  // learn" is the discriminator: the four quality NAMES also appear on every quiz
  // round below, so a find list of bare titles matches the quiz instead.
  { section: "questionsvaluable", out: "questions-matter-3-qualities.jpg", width: 1180, vw: 1280,
    find: ["Homework doesn’t help students learn", "Should I join the debate team?", "On Target"] },
];

const compose = (preds, width, vw, keep, card, wrapUp) => `(function(){
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
  // wrapUp: walk N ancestors up so the capture keeps the lesson's own wrapper
  // (same owner rule as the other two capture tools, 2026-08-04/06).
  var up = ${Number(wrapUp || 0)};
  for (var u = 0; u < up; u++) {
    if (el.parentElement && el.parentElement !== document.body) el = el.parentElement;
  }
  // Optional child slice: some lesson blocks are one tall flex column of cards that
  // has to become two boards (a heading plus N cards each). keep:[a,b] drops every
  // child outside that range so the halves keep full-size text instead of being
  // scaled down to fit one frame. Indices are into the matched element's children.
  var keep = ${JSON.stringify(keep || null)};
  if (keep) {
    var kids = Array.prototype.slice.call(el.children);
    kids.forEach(function(c, i){ if (i < keep[0] || i >= keep[1]) c.remove(); });
  }
  var pageBg = getComputedStyle(document.body).backgroundColor || "#f2f1f7";
  var slot = document.createElement("div");
  slot.style.cssText = "width:${width}px;";
  el.style.margin = "0";
  // card:true reproduces capture-board.sh's white composition card at THIS stage
  // width. capture-board.sh can only card a board on its fixed 800px stage, which is
  // too narrow for any block whose grid needs ~700px of inner width to stay in two
  // columns — so a wide two-column board could previously have the card or the
  // columns, never both. Same card styling, so the two tools' output is comparable.
  if (${card ? "true" : "false"}) {
    var cardEl = document.createElement("div");
    cardEl.style.cssText = "background:#fff;border-radius:14px;box-shadow:0 8px 22px rgba(14,10,31,0.05);" +
      "padding:24px 28px;box-sizing:border-box;width:100%;";
    cardEl.appendChild(el);
    slot.appendChild(cardEl);
  } else {
    slot.appendChild(el);
  }
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
    // BOARD_FILTER=<out-name substring> recaptures just the matching boards.
    if (process.env.BOARD_FILTER && !b.out.includes(process.env.BOARD_FILTER)) continue;
    // Reload per board: composing moves the element out of the document.
    await send("Page.navigate", { url: `http://127.0.0.1:${PORT}/index.html?print=lesson:${b.section}` });
    await sleep(2800);
    const vw = b.vw || 800;
    await send("Emulation.setDeviceMetricsOverride", { width: vw, height: Math.round(vw * 9 / 16), deviceScaleFactor: 1600 / vw, mobile: false });
    await sleep(400);
    const r = await send("Runtime.evaluate", { expression: compose(b.find, b.width, vw, b.keep, b.card, b.wrapUp), returnByValue: true });
    const msg = r.result && r.result.result && r.result.result.value;
    console.log(`  ${b.out}: ${msg}`);
    if (msg === "NOT FOUND") { ws.close(); process.exit(1); }
    await sleep(400);
    const shot = await send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(`${OUTDIR}/${b.out.replace(/\.jpg$/, ".png")}`, Buffer.from(shot.result.data, "base64"));
  }
  ws.close(); process.exit(0);
})();
