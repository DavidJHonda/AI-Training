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
const ONLY_SECTIONS = ONLY_SECTION ? new Set(ONLY_SECTION.split(",").filter(Boolean)) : null;

const ASSETS = {
  welcome: "course-assets/welcome/welcome-close.jpg",
  whydeeper: "course-assets/why-learn-ai/why-learn-ai-close.jpg",
  llms: "course-assets/what-is-ai/what-is-ai-close.jpg",
  aihistory: "course-assets/how-an-llm-works/how-an-llm-works-close.jpg",
  doesaithink: "course-assets/does-ai-think/does-ai-think-close.jpg",
  control: "course-assets/what-you-can-control/what-you-can-control-close.jpg",
  whybother: "course-assets/beyond-the-average/beyond-the-average-close.jpg",
  studying: "course-assets/learn-with-ai/learn-with-ai-close.jpg",
  openerworkwith: "course-assets/work-with-ai-opener/work-with-ai-opener-close.jpg",
  aivscode: "course-assets/ai-is-different/ai-is-different-close.jpg",
  whatitdoesbest: "course-assets/where-ai-works-best/where-ai-works-best-close.jpg",
  modelselection: "course-assets/your-home-base/your-home-base-close.jpg",
  questionsvaluable: "course-assets/questions-matter/questions-matter-close.jpg",
  prompting: "course-assets/art-of-prompting/art-of-prompting-close.jpg",
  prompt: "course-assets/context-window/context-window-close.jpg",
  evaluating: "course-assets/evaluate-the-results/evaluate-the-results-close.jpg",
  critical: "course-assets/critical-thinking/critical-thinking-close.jpg",
  openerfoundations: "course-assets/understand-ai-opener/understand-ai-opener-close.jpg",
  training: "course-assets/training/training-close.jpg",
  aiismath: "course-assets/ai-is-math/ai-is-math-close.jpg",
  tokens: "course-assets/tokens/tokens-close.jpg",
  embeddings: "course-assets/embeddings/embeddings-close.jpg",
  attention: "course-assets/transformer/transformer-close.jpg",
  layers: "course-assets/layers/layers-close.jpg",
  vectorspace: "course-assets/vector-space/vector-space-close.jpg",
  prediction: "course-assets/how-ai-answers/how-ai-answers-close.jpg",
  inference: "course-assets/one-more-thing/one-more-thing-close.jpg",
  openerprotect: "course-assets/avoid-traps-opener/avoid-traps-opener-close.jpg",
  hallucination: "course-assets/hallucination/hallucination-close.jpg",
  trainingbias: "course-assets/training-bias/training-bias-close.jpg",
  documenttrap: "course-assets/document-trap/document-trap-close.jpg",
  mindtrap: "course-assets/mind-trap/mind-trap-close.jpg",
  flattery: "course-assets/flattery-trap/flattery-trap-close.jpg",
  engagementtrap: "course-assets/engagement-trap/engagement-trap-close.jpg",
  supporttrap: "course-assets/support-trap/support-trap-close.jpg",
  faketrap: "course-assets/fake-trap/fake-trap-close.jpg",
  openerrealworld: "course-assets/embrace-the-future-opener/embrace-the-future-opener-close.jpg",
  whatpeoplesay: "course-assets/loudest-voices/loudest-voices-close.jpg",
  paceofchange: "course-assets/pace-of-change/pace-of-change-close.jpg",
  bigdownside: "course-assets/big-downside/big-downside-close.jpg",
  bigupside: "course-assets/big-upside/big-upside-close.jpg",
  agents: "course-assets/rise-of-agents/rise-of-agents-close.jpg",
  workchanges: "course-assets/work-changes/work-changes-close.jpg",
  computecost: "course-assets/data-centers/data-centers-close.jpg",
  unexpected: "course-assets/unexpected-results/unexpected-results-close.jpg",
  choosemodel: "course-assets/your-choices/your-choices-close.jpg",
  aitips: "course-assets/next-level-moves/next-level-moves-close.jpg",
  creativethinking: "course-assets/creative-thinking/creative-thinking-close.jpg",
  peopleskills: "course-assets/people-skills/people-skills-close.jpg",
  becurious: "course-assets/curious-and-flexible/curious-and-flexible-close.jpg",
  makeyourmove: "course-assets/make-your-move/make-your-move-close.jpg",
  openerskills: "course-assets/build-your-skills-opener/build-your-skills-opener-close.jpg",
  integrity: "course-assets/honesty-and-privacy/honesty-and-privacy-close.jpg"
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
    const selectedAssets = Object.entries(ASSETS).filter(([section]) => !ONLY_SECTIONS || ONLY_SECTIONS.has(section));
    if (ONLY_SECTIONS && selectedAssets.length !== ONLY_SECTIONS.size) {
      const unknown = [...ONLY_SECTIONS].filter((section) => !ASSETS[section]);
      throw new Error(`Unknown closing-board lesson${unknown.length === 1 ? "" : "s"}: ${unknown.join(", ")}`);
    }
    for (const [section, relativePath] of selectedAssets) {
      const target = path.join(OUTPUT_ROOT, relativePath);
      const establishedDimensions = fs.existsSync(target) ? jpegDimensions(target) : null;
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
        // Capture the board on an isolated white stage. Chromium rounds an
        // element screenshot's clip to device pixels; at 3x, that occasionally
        // included one CSS pixel from the following lesson block. The stage's
        // white padding makes that rounding harmless without altering the
        // board's measured dimensions or any content positions.
        const stage = document.createElement("div");
        stage.id = "closing-board-capture-stage";
        Object.assign(stage.style, {
          position: "fixed",
          left: "0",
          top: "0",
          width: `${width}px`,
          background: "#ffffff",
          boxSizing: "content-box",
          overflow: "hidden",
          zIndex: "2147483647"
        });
        document.body.appendChild(stage);
        stage.appendChild(element);
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
      const canvasWidth = establishedDimensions ? establishedDimensions.width / 3 : after.width;
      const canvasHeight = establishedDimensions ? establishedDimensions.height / 3 : after.height;
      if (after.width > canvasWidth + 0.5 || after.height > canvasHeight + 0.5) {
        throw new Error(`${section}: closing board ${after.width}x${after.height} exceeds its established ${canvasWidth}x${canvasHeight} CSS-pixel canvas`);
      }
      const stage = page.locator("#closing-board-capture-stage");
      await stage.evaluate((element, dimensions) => {
        element.style.width = `${dimensions.width}px`;
        element.style.height = `${dimensions.height}px`;
      }, { width: canvasWidth, height: canvasHeight });
      fs.mkdirSync(path.dirname(target), { recursive: true });
      await stage.screenshot({ path: target, type: "jpeg", quality: 98 });
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
