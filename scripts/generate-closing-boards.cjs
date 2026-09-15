#!/usr/bin/env node
// Generate the canonical page/video closing JPGs from index.html's CloseBoard
// component and CLOSE_BOARDS copy. The compact white canvas preserves the live
// desktop lettering and spacing; the page keeps the HTML component on phones.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const { spawn } = require("node:child_process");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.resolve(__dirname, "..");
const PORT = Number(process.env.CLOSE_BOARD_PORT || 8790);
const OUTPUT_ROOT = process.env.CLOSE_BOARD_OUTPUT_ROOT
  ? path.resolve(ROOT, process.env.CLOSE_BOARD_OUTPUT_ROOT)
  : ROOT;
const OUTPUT_REPORT = OUTPUT_ROOT === ROOT
  ? path.join(ROOT, "tmp", "closing-board-generation.json")
  : path.join(OUTPUT_ROOT, "closing-board-generation.json");
const lessonArg = process.argv.indexOf("--lesson");
const ONLY_SECTION = lessonArg >= 0 ? process.argv[lessonArg + 1] : null;

const ASSETS = {
  welcome: "course-assets/welcome/welcome-4-close.jpg",
  whydeeper: "course-assets/why-learn-ai/why-learn-ai-3-close.jpg",
  llms: "course-assets/what-is-ai/what-is-ai-4-close.jpg",
  aihistory: "course-assets/how-an-llm-works/how-an-llm-works-5-close.jpg",
  doesaithink: "course-assets/does-ai-think/does-ai-think-3-close.jpg",
  control: "course-assets/what-you-can-control/what-you-can-control-3-close.jpg",
  whybother: "course-assets/beyond-the-average/does-school-matter-3-close.jpg",
  studying: "course-assets/learn-with-ai/learn-with-ai-4-close.jpg",
  openerworkwith: "course-assets/work-with-ai-opener/opener-work-4-close.jpg",
  aivscode: "course-assets/ai-is-different/ai-is-different-6-close.jpg",
  whatitdoesbest: "course-assets/where-ai-works-best/where-ai-works-best-6-close.jpg",
  modelselection: "course-assets/your-home-base/which-app-4-close.jpg",
  questionsvaluable: "course-assets/questions-matter/questions-matter-4-close.jpg",
  prompting: "course-assets/art-of-prompting/art-of-prompting-3-close.jpg",
  prompt: "course-assets/context-window/context-window-5-close.jpg",
  evaluating: "course-assets/evaluate-the-results/evaluate-the-results-6-close.jpg",
  critical: "course-assets/critical-thinking/critical-thinking-4-close.jpg",
  openerfoundations: "course-assets/understand-ai-opener/opener-understand-3-close.jpg",
  training: "course-assets/training/training-close.jpg",
  aiismath: "course-assets/ai-is-math/ai-is-math-6-close.jpg",
  tokens: "course-assets/tokens/tokens-5-close.jpg",
  embeddings: "course-assets/embeddings/embeddings-3-close.jpg",
  attention: "course-assets/transformer/transformer-close.jpg",
  layers: "course-assets/layers/layers-4-close.jpg",
  vectorspace: "course-assets/vector-space/vector-space-close.jpg",
  prediction: "course-assets/how-ai-answers/how-ai-answers-9-close.jpg",
  inference: "course-assets/one-more-thing/one-more-thing-4-close.jpg",
  openerprotect: "course-assets/avoid-traps-opener/opener-avoid-4-close.jpg",
  hallucination: "course-assets/hallucination/hallucination-5-close.jpg",
  trainingbias: "course-assets/training-bias/training-bias-6-close.jpg",
  documenttrap: "course-assets/document-trap/document-trap-4-close.jpg",
  mindtrap: "course-assets/mind-trap/mind-trap-3-close.jpg",
  flattery: "course-assets/flattery-trap/flattery-trap-5-close.jpg",
  engagementtrap: "course-assets/engagement-trap/engagement-trap-4-close.jpg",
  supporttrap: "course-assets/support-trap/support-trap-4-close.jpg",
  faketrap: "course-assets/fake-trap/fake-trap-5-close.jpg",
  openerrealworld: "course-assets/embrace-the-future-opener/opener-embrace-3-close.jpg",
  whatpeoplesay: "course-assets/loudest-voices/loudest-voices-3-close.jpg",
  paceofchange: "course-assets/pace-of-change/pace-of-change-5-close.jpg",
  bigdownside: "course-assets/big-downside/big-downside-6-close.jpg",
  bigupside: "course-assets/big-upside/big-upside-4-close.jpg",
  agents: "course-assets/rise-of-agents/rise-of-agents-5-close.jpg",
  workchanges: "course-assets/work-changes/work-changes-5-close.jpg",
  computecost: "course-assets/data-centers/data-centers-3-close.jpg",
  unexpected: "course-assets/unexpected-results/unexpected-results-2-close.jpg",
  choosemodel: "course-assets/your-choices/your-choices-4-close.jpg",
  aitips: "course-assets/next-level-moves/next-level-moves-5-close.jpg",
  creativethinking: "course-assets/creative-thinking/creative-thinking-3-close.jpg",
  peopleskills: "course-assets/people-skills/people-skills-3-close.jpg",
  becurious: "course-assets/curious-and-flexible/curious-and-flexible-3-close.jpg",
  makeyourmove: "course-assets/make-your-move/make-your-move-4-close.jpg",
  openerskills: "course-assets/build-your-skills-opener/opener-build-3-close.jpg",
  integrity: "course-assets/honesty-and-privacy/honesty-and-privacy-5-close.jpg"
};

function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

function jpegDimensions(file) {
  const data = fs.readFileSync(file);
  let offset = 2;
  while (offset + 9 < data.length) {
    if (data[offset] !== 0xff) { offset += 1; continue; }
    const marker = data[offset + 1];
    if (marker >= 0xc0 && marker <= 0xc3) {
      return { height: data.readUInt16BE(offset + 5), width: data.readUInt16BE(offset + 7) };
    }
    if (marker === 0xd8 || marker === 0xd9) { offset += 2; continue; }
    const length = data.readUInt16BE(offset + 2);
    if (!length) break;
    offset += length + 2;
  }
  throw new Error(`Could not read JPEG dimensions: ${file}`);
}

function updateAssetManifest(report) {
  const manifestPath = path.join(ROOT, "course-assets", "manifest.json");
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  const byPath = new Map(report.map((item) => [item.src, item]));
  for (const item of manifest.assets || []) {
    const generated = byPath.get(item.new);
    if (!generated) continue;
    item.sha256 = generated.sha256;
    item.bytes = generated.bytes;
    item.variant = "canonical-close-board-generated-from-live-component";
  }
  manifest.description = "Canonical source assets are retained where applicable; generated artifacts and replacements are recorded separately. Paths are relative to the repository root.";
  manifest.generated_assets = (manifest.generated_assets || []).filter((item) => !byPath.has(item.new));
  for (const item of report) {
    manifest.generated_assets.push({
      new: item.src,
      sha256: item.sha256,
      bytes: item.bytes,
      width: item.width,
      height: item.height,
      reference_files: ["index.html", "scripts/video/make_close_board.py"],
      generator: "scripts/generate-closing-boards.cjs",
      purpose: "Canonical white-background lesson closing shared by the page and future video builds."
    });
  }
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n");
}

function htmlWithLiveCloseBoards() {
  const source = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");
  const start = source.indexOf("function closeBoard(sectionId) {");
  const end = source.indexOf("\nconst USING_THIS_COURSE_POLICY", start);
  if (start < 0 || end < 0) throw new Error("Could not locate closeBoard() in index.html");
  const replacement = `function closeBoard(sectionId) {
  var copy = CLOSE_BOARDS[sectionId];
  return copy ? React.createElement(CloseBoard, copy) : null;
}
`;
  return source.slice(0, start) + replacement + source.slice(end);
}

(async () => {
  fs.mkdirSync(path.dirname(OUTPUT_REPORT), { recursive: true });
  const server = spawn("python3", ["-m", "http.server", String(PORT), "--bind", "127.0.0.1"], { cwd: ROOT, stdio: "ignore" });
  let browser;
  try {
    await new Promise((resolve) => setTimeout(resolve, 700));
    browser = await chromium.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: true });
    const page = await browser.newPage({ viewport: { width: 960, height: 1200 }, deviceScaleFactor: 3 });
    const generatedSource = htmlWithLiveCloseBoards();
    await page.route("**/*", (route) => {
      const url = route.request().url();
      if (/script\.google\.com|script\.googleusercontent\.com|\.mp4(?:\?|$)/.test(url)) return route.abort();
      if (url.startsWith(`http://127.0.0.1:${PORT}/index.html`)) return route.fulfill({ contentType: "text/html", body: generatedSource });
      return route.continue();
    });

    const report = [];
    const selectedAssets = Object.entries(ASSETS).filter(([section]) => !ONLY_SECTION || section === ONLY_SECTION);
    if (ONLY_SECTION && !selectedAssets.length) throw new Error(`Unknown closing-board lesson: ${ONLY_SECTION}`);
    for (const [section, relativePath] of selectedAssets) {
      await page.goto(`http://127.0.0.1:${PORT}/index.html?print=lesson:${section}`, { waitUntil: "networkidle" });
      await page.evaluate(() => document.fonts.ready);
      const board = page.locator(".close-board:visible").last();
      await board.waitFor({ state: "visible" });
      const before = await board.evaluate((element) => {
        const children = Array.from(element.children).map((child) => {
          const rect = child.getBoundingClientRect();
          return { width: rect.width, height: rect.height };
        });
        return { width: element.getBoundingClientRect().width, height: element.getBoundingClientRect().height, children };
      });
      const compactWidth = Math.min(before.width, Math.ceil(Math.max(400, ...before.children.map((child) => child.width + 40))));
      await board.evaluate((element, width) => {
        Object.assign(element.style, {
          width: `${width}px`,
          margin: "0 auto",
          background: "#ffffff",
          boxSizing: "border-box"
        });
      }, compactWidth);
      const after = await board.evaluate((element) => {
        const children = Array.from(element.children).map((child) => {
          const rect = child.getBoundingClientRect();
          return { width: rect.width, height: rect.height };
        });
        const rect = element.getBoundingClientRect();
        return { width: rect.width, height: rect.height, children };
      });
      before.children.forEach((child, index) => {
        const rendered = after.children[index];
        if (Math.abs(child.width - rendered.width) > 0.5 || Math.abs(child.height - rendered.height) > 0.5) {
          throw new Error(`${section}: compact canvas changed child ${index + 1} from ${JSON.stringify(child)} to ${JSON.stringify(rendered)}`);
        }
      });
      const target = path.join(OUTPUT_ROOT, relativePath);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      await board.screenshot({ path: target, type: "jpeg", quality: 98 });
      const dimensions = jpegDimensions(target);
      report.push({ section, src: relativePath, cssWidth: after.width, cssHeight: after.height, width: dimensions.width, height: dimensions.height, bytes: fs.statSync(target).size, sha256: sha256(target) });
      console.log(`${section}: ${relativePath} (${dimensions.width}x${dimensions.height})`);
    }
    fs.writeFileSync(OUTPUT_REPORT, JSON.stringify(report, null, 2) + "\n");
    if (OUTPUT_ROOT === ROOT) updateAssetManifest(report);
    console.log(`Wrote ${OUTPUT_REPORT}`);
  } finally {
    if (browser) await browser.close();
    server.kill();
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });

module.exports = { ASSETS };
