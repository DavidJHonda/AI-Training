#!/usr/bin/env node
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.resolve(__dirname, "../..");
const OUT = path.join(ROOT, "course-assets/wheres-the-line");
fs.mkdirSync(OUT, { recursive: true });

const boards = [
  {
    file: "wheres-the-line-two-uses.jpg", format: "EE-2FB", title: "How DraftKings Uses AI",
    artSheet: "scripts/video/assets/editorial-full-bleed/wheres-the-line-draftkings/art-sheet.png",
    cards: [
      ["Targeted Promotions", "DraftKings developed AI to analyze betting habits, account balances, and losses to predict which customers would gamble and lose more after receiving free bets and bonuses.", "DraftKings put the technology into use and continued developing it."],
      ["Customer Protection", "Employees developed AI to analyze betting patterns and identify people who might be developing a gambling problem, so the company could intervene earlier.", "DraftKings chose not to put this predictive technology into use."]
    ]
  },
  {
    file: "wheres-the-line-responsible-choice.jpg", format: "EE-4FB", title: "Making the Responsible Choice",
    artSheet: "scripts/video/assets/editorial-full-bleed/wheres-the-line-responsible-choice/art-sheet.png",
    cards: [
      ["CONSIDER EVERYONE AFFECTED", "Look beyond the people who benefit. Who could be harmed, excluded, or pressured?"],
      ["BE CLEAR WITH PEOPLE", "Explain what the system does and how it affects their choices."],
      ["BUILD IN PROTECTION", "Test for harm, set boundaries, and give people a way to challenge mistakes."],
      ["OWN THE OUTCOME", "Monitor what happens. Change or stop the system when the consequences warrant it."]
    ],
    banner: "A responsible decision considers the people who live with it."
  }
];

function comparisonArt(protection) {
  const accent = protection ? '#0f7a4a' : '#4f2fc4';
  const wash = protection ? '#d8eee4' : '#e4ddfa';
  const id = protection ? 'safe' : 'offer';
  const target = protection ? `
    <path d="M559 92 L632 117 V178 Q632 232 559 261 Q486 232 486 178 V117 Z" fill="white" stroke="${accent}" stroke-width="5"/>
    <path d="M526 174 L550 197 L596 148" fill="none" stroke="${accent}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="628" cy="109" r="29" fill="#fff0c2" stroke="#ac7b15" stroke-width="3"/>
    <path d="M628 94 V112 M628 122 V123" stroke="#ac7b15" stroke-width="5" stroke-linecap="round"/>` : `
    <rect x="495" y="64" width="141" height="223" rx="23" fill="white" stroke="${accent}" stroke-width="4"/>
    <rect x="537" y="77" width="57" height="7" rx="3" fill="${wash}"/>
    <rect x="510" y="110" width="111" height="126" rx="12" fill="${wash}"/>
    <path d="M538 161 H593 V193 H538 Z M534 150 H597 V163 H534 Z" fill="${accent}"/>
    <path d="M565 150 V193 M565 148 C533 149 544 124 556 137 L565 148 C594 148 585 124 574 137 Z" fill="none" stroke="#ffd983" stroke-width="5"/>
    <text x="565" y="218" text-anchor="middle" fill="${accent}" font-family="Jakarta" font-size="17" font-weight="700">BONUS</text>
    <circle cx="565" cy="260" r="8" fill="${wash}"/>`;
  return `<svg viewBox="0 0 744 339" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
   <defs><linearGradient id="${id}" x2="1" y2="1"><stop stop-color="${wash}"/><stop offset="1" stop-color="#f6f5fc"/></linearGradient><filter id="s-${id}" x="-25%" y="-25%" width="150%" height="160%"><feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="${accent}" flood-opacity=".12"/></filter></defs>
   <rect width="744" height="339" fill="url(#${id})"/>
   <ellipse cx="384" cy="296" rx="286" ry="15" fill="${accent}" opacity=".055"/>
   <g stroke="${accent}" stroke-width="4" fill="none" opacity=".45"><path d="M252 170 H305"/><path d="M419 170 H475" ${protection?'stroke-dasharray="9 8"':''}/><path d="M465 161 L475 170 L465 179"/></g>
   <g filter="url(#s-${id})"><rect x="93" y="85" width="158" height="176" rx="16" fill="white"/>
   <rect x="114" y="107" width="70" height="9" rx="4" fill="${accent}" opacity=".6"/>
   <g fill="${accent}"><rect x="114" y="151" width="22" height="42" rx="4" opacity=".35"/><rect x="145" y="131" width="22" height="62" rx="4" opacity=".5"/><rect x="176" y="158" width="22" height="35" rx="4" opacity=".65"/><rect x="207" y="141" width="22" height="52" rx="4" opacity=".8"/></g>
   <path d="M114 218 H229 M114 236 H194" stroke="${accent}" stroke-width="7" stroke-linecap="round" opacity=".18"/>
   <circle cx="362" cy="170" r="57" fill="${accent}"/>
   <g stroke="white" stroke-width="2" opacity=".65"><path d="M337 153 L383 147 L364 193 Z M337 153 L384 180 L364 193 M383 147 L384 180"/></g>
   <g fill="white"><circle cx="337" cy="153" r="8"/><circle cx="383" cy="147" r="8"/><circle cx="364" cy="193" r="8"/><circle cx="384" cy="180" r="6"/></g>
   ${target}</g>
  </svg>`;
}

function editorialHtml(board) {
  const artData = fs.readFileSync(path.join(ROOT, board.artSheet)).toString("base64");
  const credit = process.env.SKIP_COURSE_CREDIT === "1" ? "" : "besmarterthanthetool.com";
  return `<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face{font-family:Jakarta;src:url(file://${ROOT}/scripts/video/assets/fonts/PlusJakartaSans-wght.ttf)}
  *{box-sizing:border-box}html,body{margin:0;background:white}body{font-family:Jakarta,Arial,sans-serif;color:#0e0a1f}
  .board{width:1600px;background:#eae7fd;border-radius:22px;padding:40px 40px 10px;overflow:hidden}
  h1{font-size:56px;line-height:1.08;letter-spacing:-.03em;margin:0 0 26.52px;font-weight:700}
  .grid{display:grid;grid-template-columns:744px 744px;gap:32px}
  .card{background:#fff;border-radius:14px;overflow:hidden;position:relative;box-shadow:0 8px 24px rgba(35,25,83,.08)}
  .card:after{content:'';position:absolute;inset:0;border:1px solid rgba(79,47,196,.22);border-radius:14px;pointer-events:none}.card:nth-child(2):after{border-color:rgba(15,122,74,.22)}
  .art{display:block;width:744px;height:339px;background-image:url('data:image/png;base64,${artData}');background-size:1488px auto;background-repeat:no-repeat;border-bottom:1px solid rgba(79,47,196,.2);position:relative}.art:after{content:'';position:absolute;inset:0;background:#4f2fc4;opacity:.10}.art0{background-position:0 -169px}.art1{background-position:-744px -169px}.card:nth-child(2) .art{border-color:rgba(15,122,74,.2)}.card:nth-child(2) .art:after{background:#0f7a4a}
  .text{padding:32px 34px 34px}.label{font-size:40px;line-height:48px;letter-spacing:-.02em;font-weight:700;color:#4f2fc4;margin-bottom:14px;white-space:nowrap}.card:nth-child(2) .label{color:#0f7a4a}
  .copy{font-size:29px;line-height:41px;font-weight:500;color:#3a3550}
  .did{margin-top:22px;padding-top:20px;border-top:1px solid rgba(79,47,196,.18)}.card:nth-child(2) .did{border-top-color:rgba(15,122,74,.18)}
  .did-label{font-size:22px;line-height:28px;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:#4f2fc4;margin-bottom:8px}.card:nth-child(2) .did-label{color:#0f7a4a}
  .banner{margin-top:40px;background:#ffe39a;border-radius:14px;height:88px;display:flex;align-items:center;justify-content:center;gap:24px;text-align:center;font-size:32px;line-height:1.4;font-weight:500;white-space:nowrap}
  .check{width:44px;height:44px;border-radius:50%;background:#4f2fc4;color:white;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:700;flex:none}
  .credit{font-size:20px;line-height:24px;min-height:24px;font-weight:500;color:#615b78;text-align:right;margin-top:6px}
  .grid + .credit{margin-top:14px}
  </style></head><body><div class="board"><h1>${board.title}</h1><div class="grid">${board.cards.map((c,i)=>`<div class="card"><div class="art art${i}"></div><div class="text"><div class="label">${c[0]}</div><div class="copy">${c[1]}</div>${c[2]?`<div class="did"><div class="did-label">What They Did</div><div class="copy">${c[2]}</div></div>`:''}</div></div>`).join('')}</div>${board.banner?`<div class="banner"><span class="check">✓</span>${board.banner}</div>`:''}<div class="credit">${credit}</div></div></body></html>`;
}

function fourCardFullBleedHtml(board) {
  const artData = fs.readFileSync(path.join(ROOT, board.artSheet)).toString("base64");
  const credit = process.env.SKIP_COURSE_CREDIT === "1" ? "" : "besmarterthanthetool.com";
  return `<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face{font-family:Jakarta;src:url(file://${ROOT}/scripts/video/assets/fonts/PlusJakartaSans-wght.ttf)}
  *{box-sizing:border-box}html,body{margin:0;background:white}body{font-family:Jakarta,Arial,sans-serif;color:#0e0a1f}
  .board{width:1600px;background:#eae7fd;border-radius:22px;padding:40px 40px 10px;overflow:hidden}
  h1{font-size:56px;line-height:1.08;letter-spacing:-.03em;margin:0 0 26.52px;font-weight:700}
  .grid{display:grid;grid-template-columns:744px 744px;gap:32px}
  .card{background:#fff;border-radius:14px;overflow:hidden;position:relative;box-shadow:0 8px 24px rgba(35,25,83,.08)}
  .card:after{content:'';position:absolute;inset:0;border:1px solid color-mix(in srgb,var(--accent) 22%,white);border-radius:14px;pointer-events:none}
  .art{width:744px;height:339px;background-image:url('data:image/png;base64,${artData}');background-size:1488px 992px;background-repeat:no-repeat;border-bottom:1px solid color-mix(in srgb,var(--accent) 20%,white);position:relative}
  .art:after{content:'';position:absolute;inset:0;background:var(--accent);opacity:.10}
  .card:nth-child(1){--accent:#4f2fc4}.card:nth-child(2){--accent:#1652f0}.card:nth-child(3){--accent:#0e8f86}.card:nth-child(4){--accent:#a9760c}
  .card:nth-child(1) .art{background-position:0 -78px}.card:nth-child(2) .art{background-position:-744px -78px}.card:nth-child(3) .art{background-position:0 -574px}.card:nth-child(4) .art{background-position:-744px -574px}
  .text{padding:32px 34px 34px;height:252px}.label{font-size:40px;line-height:48px;letter-spacing:-.02em;font-weight:700;color:var(--accent);margin-bottom:14px;white-space:nowrap}.copy{font-size:29px;line-height:41px;font-weight:500;color:#3a3550}
  .credit{font-size:20px;line-height:24px;min-height:24px;font-weight:500;color:#615b78;text-align:right;margin-top:6px}
  </style></head><body><div class="board"><h1>${board.title}</h1><div class="grid">${board.cards.map(c=>`<div class="card"><div class="art"></div><div class="text"><div class="label">${c[0].replace(/\b\w/g, letter => letter.toUpperCase()).toLowerCase().replace(/(^|\s)\S/g, letter => letter.toUpperCase())}</div><div class="copy">${c[1]}</div></div></div>`).join('')}</div><div class="credit">${credit}</div></div></body></html>`;
}

function html(board) {
  if (board.format === "EE-2FB") return editorialHtml(board);
  if (board.format === "EE-4FB") return fourCardFullBleedHtml(board);
  const cards = board.cards.map((c, i) => `<div class="card c${i}"><div class="label">${c[0]}</div><div class="copy">${c[1]}</div></div>`).join("");
  return `<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face{font-family:Jakarta;src:url(file://${ROOT}/scripts/video/assets/fonts/PlusJakartaSans-wght.ttf)}
  *{box-sizing:border-box}html,body{margin:0;background:white}body{font-family:Jakarta,Arial,sans-serif}
  .board{width:1600px;background:#eae7fd;border-radius:26px;padding:40px 40px 34px;color:#0e0a1f;position:relative;overflow:hidden}
  h1{font-size:56px;line-height:1.08;letter-spacing:-2.2px;margin:0 0 30px;font-weight:800}
  .grid{display:grid;grid-template-columns:repeat(${board.cards.length},1fr);gap:28px}
  .card{background:#fff;border-radius:18px;padding:30px 30px 34px;min-height:${board.cards.length===4?260:300}px;box-shadow:0 8px 24px rgba(35,25,83,.08);border-top:10px solid #5b43d6}
  .c1{border-top-color:#2563eb}.c2{border-top-color:#1f9d68}.c3{border-top-color:#d58b15}
  .label{font-size:23px;line-height:1.2;letter-spacing:1.5px;font-weight:800;color:#5b43d6;margin-bottom:18px}
  .c1 .label{color:#2563eb}.c2 .label{color:#187f56}.c3 .label{color:#a76500}
  .copy{font-size:${board.cards.length===4?28:30}px;line-height:1.45;font-weight:500;color:#302b49}
  .note{font-size:28px;line-height:1.45;font-weight:600;background:#fff;border-radius:16px;padding:22px 28px;margin-top:24px;color:#302b49}
  .banner{margin-top:26px;background:#ffe08b;border-radius:15px;min-height:78px;padding:17px 64px;display:flex;align-items:center;justify-content:center;text-align:center;font-size:31px;line-height:1.3;font-weight:600}
  .banner:before{content:'✓';width:44px;height:44px;border-radius:50%;background:#6847ee;color:#fff;display:inline-flex;align-items:center;justify-content:center;margin-right:20px;flex:0 0 auto;font-weight:800}
  .credit{font-size:20px;font-weight:600;color:#615b78;text-align:right;margin-top:12px}
  </style></head><body><div class="board"><h1>${board.title}</h1><div class="grid">${cards}</div>${board.note?`<div class="note">${board.note}</div>`:""}${board.banner?`<div class="banner">${board.banner}</div>`:""}<div class="credit">besmarterthanthetool.com</div></div></body></html>`;
}

(async()=>{
  const requested = new Set(process.argv.slice(2));
  const selected = requested.size ? boards.filter(board => requested.has(board.file)) : boards;
  if (requested.size && selected.length !== requested.size) {
    throw new Error("Unknown board filename requested");
  }
  const browser = await chromium.launch({executablePath:"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",headless:true});
  try {
    for (const board of selected) {
      const page = await browser.newPage({viewport:{width:1600,height:1400},deviceScaleFactor:1});
      await page.setContent(html(board), {waitUntil:"load"});
      await page.evaluate(()=>document.fonts.ready);
      await page.locator(".board").screenshot({path:path.join(OUT,board.file),type:"jpeg",quality:96});
      await page.close();
      console.log(board.file);
    }
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exit(1)});
