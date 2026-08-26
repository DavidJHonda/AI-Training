import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(scriptDir, "..");
const sourcePath = path.join(root, "docs/labs/career-field-explorer-prototype.html");
const outputDir = path.join(root, "docs/labs/career-field-explorer");

const stages = [
  {
    number: 1,
    slug: "your-choices",
    lesson: "Your Choices",
    hero: "Start with three career fields and a clear purpose. The first version only needs to make exploration feel possible.",
    fields: "Three examples give the app a useful shape. Later checkpoints will make the information editable, sourced, and personal."
  },
  {
    number: 2,
    slug: "ai-tips",
    lesson: "AI Tips",
    hero: "Turn a static first draft into a tool you can shape. Edit each field without touching the code.",
    fields: "Use the edit control to replace the examples with fields you genuinely want to investigate."
  },
  {
    number: 3,
    slug: "habits-for-the-road",
    lesson: "Habits for the Road",
    hero: "Make the explorer safer and more trustworthy. Add sources, dates, and only the information the task needs.",
    fields: "Edit every field, then add an official source and the date you checked it. Do not enter private information."
  },
  {
    number: 4,
    slug: "people-skills",
    lesson: "People Skills",
    hero: "A useful tool starts with the person using it. Choose what matters before comparing the fields.",
    fields: "Keep refining the three fields after another person tries the explorer and tells you what was unclear."
  },
  {
    number: 5,
    slug: "creative-thinking",
    lesson: "Creative Thinking",
    hero: "Put the same evidence into a more useful shape. Compare fields through the priorities that matter to you.",
    fields: "Include at least one field or pathway you had not seriously considered before this project."
  },
  {
    number: 6,
    slug: "skills-that-matter",
    lesson: "Skills That Matter",
    hero: "A comparison can organize evidence without pretending to make the decision. Keep judgment with the student.",
    fields: "Improve weak claims, keep missing evidence visible, and resist turning the comparison into a score."
  },
  {
    number: 7,
    slug: "be-curious",
    lesson: "Be Curious",
    hero: "Curiosity turns a comparison into a next question. Choose one field that deserves another hour of investigation.",
    fields: "Each field needs one honest unanswered question and one low-risk action that could teach you something real."
  },
  {
    number: 8,
    slug: "make-your-move",
    lesson: "Make Your Move",
    hero: "Finish a tool you can actually keep using. Save the work, export the exploration, and take one real next step.",
    fields: "Review the evidence, make the language your own, and leave the app ready for another person to use."
  }
];

function stageCss(stage) {
  const hidden = [];
  if (stage < 2) hidden.push(".icon-button[data-edit]", "dialog");
  if (stage < 3) hidden.push(".source-block", ".field:has(#editSource)", ".field:has(#editDate)", ".field:has(#editUrl)", ".status-item:nth-child(3)", "#fields .section-count");
  if (stage < 4) hidden.push("#priorities", ".status-item:nth-child(2)");
  if (stage < 5) hidden.push("#comparison");
  if (stage < 6) hidden.push(".judgment-note");
  if (stage < 7) hidden.push("#next-step");
  if (stage < 8) hidden.push(".actions", ".save-state");

  const visibleStatus = stage < 3 ? 1 : stage < 4 ? 2 : 3;
  return `
    /* Generated recovery checkpoint ${stage}. */
    body[data-checkpoint="${stage}"] .status-strip {
      grid-template-columns: repeat(${visibleStatus}, minmax(0, 1fr));
    }
    ${hidden.length ? `body[data-checkpoint="${stage}"] :is(${hidden.join(", ")}) { display: none !important; }` : ""}
    .checkpoint-banner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin: 0 0 18px;
      padding: 12px 16px;
      border: 1px solid var(--rule);
      border-radius: 14px;
      background: rgba(255,255,255,0.9);
      color: var(--ink-soft);
      box-shadow: var(--shadow-soft);
      font-size: 13px;
      font-weight: 750;
    }
    .checkpoint-banner strong { color: var(--primary-deep); }
    .judgment-note {
      margin: 0 0 16px;
      padding: 16px 18px;
      border-left: 4px solid var(--primary);
      border-radius: 12px;
      background: var(--primary-faint);
      color: var(--ink-soft);
      font-size: 14px;
      line-height: 1.6;
    }
    .judgment-note strong { color: var(--ink); }
    @media (max-width: 560px) {
      .checkpoint-banner { align-items: flex-start; flex-direction: column; gap: 4px; }
    }
    @media print { .checkpoint-banner { display: none !important; } }
  `;
}

function buildStage(source, config) {
  const stage = config.number;
  let html = source;
  html = html.replace("<!doctype html>", `<!doctype html>\n<!-- Generated recovery file for checkpoint ${stage}: ${config.lesson}. -->`);
  html = html.replace("<title>Career Field Explorer</title>", `<title>Career Field Explorer · Checkpoint ${stage}</title>`);
  html = html.replace("  </style>", `${stageCss(stage)}\n  </style>`);
  html = html.replace("<body>", `<body data-checkpoint="${stage}">`);
  html = html.replace(
    "    <header class=\"hero\">",
    `    <div class="checkpoint-banner"><strong>Checkpoint ${stage} of 8 · ${config.lesson}</strong><span>Recovery build</span></div>\n\n    <header class="hero">`
  );
  html = html.replace(
    "Compare three career fields, notice the tradeoffs, and choose one useful next step. You are not choosing a career today.",
    config.hero
  );
  html = html.replace(
    "Start with the examples, then edit every field to reflect what you genuinely want to investigate.",
    config.fields
  );
  html = html.replace(
    'const STORAGE_KEY = "career-field-explorer-prototype-v1";',
    'const STORAGE_KEY = "career-field-explorer-course-build-v1";'
  );
  html = html.replace(
    '      <div id="comparisonContent"></div>',
    '      <div class="judgment-note"><strong>No total, score, or winner.</strong> Use the labels to organize evidence, then make the human call yourself.</div>\n      <div id="comparisonContent"></div>'
  );

  if (stage < 4) {
    html = html.replace('<p class="section-kicker">Step 2</p>\n          <h2>Explore three fields</h2>', '<p class="section-kicker">Step 1</p>\n          <h2>Explore three fields</h2>');
  }

  if (stage === 5) {
    html = html.replace("Compare without scoring", "Build a first comparison");
    html = html.replace(
      "For each priority, record what the evidence currently suggests. “Need evidence” is a useful answer.",
      "Make a first-pass comparison. The next checkpoint will test whether these labels create too much certainty."
    );
    html = html.replaceAll("Looks promising", "Strong fit");
    html = html.replaceAll("Need evidence", "Unsure");
    html = html.replaceAll("Possible tension", "Weak fit");
  }

  return html;
}

fs.mkdirSync(outputDir, { recursive: true });
const source = fs.readFileSync(sourcePath, "utf8");

fs.writeFileSync(
  path.join(outputDir, "reference.html"),
  source.replace("<!doctype html>", "<!doctype html>\n<!-- Approved Career Field Explorer reference build. -->"),
  "utf8"
);

for (const stage of stages) {
  const filename = `${String(stage.number).padStart(2, "0")}-${stage.slug}-recovery.html`;
  // LAB 13 has a deliberately broader, simpler six-field recovery build. Preserve
  // that reviewed checkpoint instead of regenerating it from the three-field final.
  if (stage.number === 1 && fs.existsSync(path.join(outputDir, filename))) continue;
  fs.writeFileSync(path.join(outputDir, filename), buildStage(source, stage), "utf8");
}

console.log(`Built ${stages.length} recovery checkpoints and the frozen reference in ${outputDir}`);
