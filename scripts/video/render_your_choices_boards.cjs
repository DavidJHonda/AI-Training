#!/usr/bin/env node
// Know the App: canonical EE-2FB layout, with the approved example subsection.
// Run: node scripts/video/render_your_choices_boards.cjs
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const deps = process.env.CODEX_NODE_MODULES || '/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const { chromium } = require(path.join(deps, 'playwright'));
const sharp = require(path.join(deps, 'sharp'));
const root = path.resolve(__dirname, '../..');
const out = path.join(root, 'course-assets/your-choices');
const reportDir = path.join(root, 'tmp/your-choices-spec');
const boards = [
  {
    id: 'choose-tool', title: 'Which Model?',
    cards: [
      ['Everyday Model', 'Quick questions and simple tasks.', '“Suggest a funny movie to watch tonight.”'],
      ['More Capable Model', 'More demanding tasks with details to work through.', '“Help me plan a summer business, including costs, pricing, and how many customers I’ll need.”']
    ],
    banner: 'Start with the default. Try a more capable model when needed.'
  },
  {
    id: 'thinking', title: 'How Much Thinking?',
    cards: [
      ['Less Thinking', 'AI spends less time working through your task. Useful for less complicated and routine work.', '“Turn these notes from our group meeting into a clear checklist.”'],
      ['More Thinking', 'AI spends more time working through steps, weighing options, and checking its answer. Useful for tasks that require analysis like coding, planning, and problems with steps.', '“Help us divide this project among four people. We have one week, different schedules, and only two people know how to edit video.”']
    ],
    banner: 'Give AI more time when the task needs more working through.'
  },
  {
    id: 'research', title: 'How Much Research?',
    cards: [
      ['Regular Chat', 'Get an answer to a question.', '“I live in Dallas. How long would it take me to drive to Texas A&M in College Station versus UT Austin?”'],
      ['Deep Research', 'Get information from many websites, compare what they say, and build a report that shows sources.', '“I want to study physics and am considering Texas A&M and UT Austin. Compare their physics programs, undergraduate research opportunities, admissions requirements, and costs. Show your sources.”']
    ],
    banner: 'Use deeper research when you need to compare information across sources.'
  }
];
const escape = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
function html(board) {
  const font = fs.readFileSync(path.join(root, 'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf')).toString('base64');
  return `<!doctype html><meta charset="utf-8"><style>
    @font-face{font-family:Jakarta;src:url(data:font/ttf;base64,${font}) format('truetype');font-weight:200 800;font-style:normal}
    *{box-sizing:border-box}html,body{margin:0;background:white}
    body{font-family:Jakarta,sans-serif;color:#0e0a1f}
    .board{width:1600px;padding:31px 40px 40px;background:#eae7fd;border-radius:22px;position:relative;overflow:hidden}
    h1{margin:0 0 26px;font-size:56px;line-height:61px;font-weight:700;letter-spacing:-.03em}
    .cards{display:grid;grid-template-columns:744px 744px;gap:32px}
    .card{--accent:#4f2fc4;--border:rgba(79,47,196,.22);--divider:rgba(79,47,196,.2);background:white;border-radius:14px;overflow:hidden;position:relative;box-shadow:0 8px 24px rgba(35,25,83,.08)}
    .card:nth-child(2){--accent:#1652f0;--border:rgba(22,82,240,.22);--divider:rgba(22,82,240,.2)}
    .card:after{content:'';position:absolute;inset:0;border:1px solid var(--border);border-radius:14px;pointer-events:none}
    .art{height:339px;width:744px;position:relative}
    .art img{display:block;width:100%;height:100%;object-fit:cover}
    .art:after{content:'';position:absolute;left:0;right:0;bottom:0;border-bottom:1px solid var(--divider)}
    .text{padding:32px 34px 34px}
    h2{margin:0 0 14px;color:var(--accent);font-size:40px;font-weight:700;line-height:48px;letter-spacing:-.02em;white-space:nowrap}
    p{margin:0;font-size:29px;line-height:41px;font-weight:500;color:#3a3550}
    .example{margin-top:63px;border-top:1px solid var(--divider);padding-top:20px}
    .example-label{font-size:22px;line-height:28px;font-weight:700;color:var(--accent);margin-bottom:12px}
    .banner{margin-top:40px;height:88px;border-radius:14px;background:#ffe39a;display:flex;align-items:center;justify-content:center}
    .lockup{display:flex;gap:24px;align-items:center;white-space:nowrap}
    .check{width:44px;height:44px;flex-shrink:0}
    .takeaway{font-size:32px;line-height:32px;font-weight:500}
    .credit{position:absolute;right:40px;bottom:8px;font-size:20px;line-height:24px;font-weight:500;color:#615b78}
  </style><div class="board"><h1>${escape(board.title)}</h1><div class="cards">${board.cards.map((c,i)=>{
    const art = fs.readFileSync(path.join(root, `scripts/video/assets/your-choices/${board.id}-${i}.png`)).toString('base64');
    return `<section class="card"><div class="art"><img src="data:image/png;base64,${art}"></div><div class="text"><h2>${escape(c[0])}</h2><p class="description">${escape(c[1])}</p><div class="example"><div class="example-label">EXAMPLE</div><p>${escape(c[2])}</p></div></div></section>`;
  }).join('')}</div><div class="banner"><div class="lockup"><svg class="check" viewBox="0 0 44 44"><circle cx="22" cy="22" r="22" fill="#4f2fc4"/><path d="m12 22 7 7 13-14" fill="none" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="takeaway">${escape(board.banner)}</span></div></div><div class="credit">besmarterthanthetool.com</div></div>`;
}

(async()=>{
  fs.mkdirSync(reportDir, {recursive:true});
  const browser = await chromium.launch({executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
  const reports = [];
  try {
    for(const board of boards) {
      const page = await browser.newPage({viewport:{width:1600,height:1600},deviceScaleFactor:1});
      await page.setContent(html(board), {waitUntil:'load'});
      await page.evaluate(async()=>{
        await document.fonts.ready;
        if(!document.fonts.check('700 40px Jakarta')) throw new Error('Course font did not load');
        // Align separators against the longer explanation; preserve an extra 41px
        // blank line in addition to the normal 22px subsection gap.
        const descriptions = [...document.querySelectorAll('.description')];
        const height = Math.max(...descriptions.map(e=>e.getBoundingClientRect().height));
        descriptions.forEach(e=>e.style.height=`${height}px`);
        const texts = [...document.querySelectorAll('.text')];
        const textHeight = Math.max(...texts.map(e=>e.getBoundingClientRect().height));
        texts.forEach(e=>e.style.height=`${textHeight}px`);
      });
      const measures = await page.evaluate(()=>{
        const rect = e => {const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom,right:r.right};};
        const get = s => rect(document.querySelector(s));
        return {
          board:get('.board'),title:get('h1'),cards:[...document.querySelectorAll('.card')].map(rect),
          art:[...document.querySelectorAll('.art')].map(rect),text:[...document.querySelectorAll('.text')].map(rect),
          banner:get('.banner'),check:get('.check'),lockup:get('.lockup'),
          headings:[...document.querySelectorAll('h2')].map(e=>({overflow:e.scrollWidth>e.clientWidth,size:getComputedStyle(e).fontSize})),
          description:[...document.querySelectorAll('.description')].map(e=>({size:getComputedStyle(e).fontSize,line:getComputedStyle(e).lineHeight})),
          bannerType:{size:getComputedStyle(document.querySelector('.takeaway')).fontSize,weight:getComputedStyle(document.querySelector('.takeaway')).fontWeight}
        };
      });
      assert.equal(measures.board.width,1600);
      assert.equal(measures.title.x,40);assert.equal(measures.title.y,31);
      for(const a of measures.art){assert.equal(a.width,744);assert.equal(a.height,339);}
      assert.equal(measures.cards[1].x-measures.cards[0].right,32);
      assert.equal(measures.text[0].height,measures.text[1].height);
      assert.equal(measures.banner.y-measures.cards[0].bottom,40);
      assert.equal(measures.banner.height,88);
      assert.equal(measures.board.bottom-measures.banner.bottom,40);
      assert.equal(measures.check.width,44);assert.equal(measures.check.height,44);
      assert.ok(measures.lockup.width<=measures.banner.width-68,'Takeaway overflows safe horizontal padding');
      assert.ok(measures.headings.every(h=>!h.overflow&&h.size==='40px'));
      assert.ok(measures.description.every(p=>p.size==='29px'&&p.line==='41px'));
      assert.deepEqual(measures.bannerType,{size:'32px',weight:'500'});
      const png = await page.locator('.board').screenshot({type:'png'});
      const file = path.join(out,`your-choices-${board.id}.jpg`);
      await sharp(png).jpeg({quality:95,chromaSubsampling:'4:4:4',optimiseCoding:true}).toFile(file);
      const metadata = await sharp(file).metadata();
      assert.equal(metadata.chromaSubsampling,'4:4:4');
      reports.push({id:board.id,...measures,export:{width:metadata.width,height:metadata.height,sampling:metadata.chromaSubsampling}});
      console.log(`${board.id}: ${metadata.width}×${metadata.height}; EE-2FB geometry and export checks passed`);
      await page.close();
    }
    fs.writeFileSync(path.join(reportDir,'measurements.json'),JSON.stringify(reports,null,2)+'\n');
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
