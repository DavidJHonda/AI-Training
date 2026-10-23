#!/usr/bin/env node
// Evaluation Matters: EE-2FB / EE-3FB with approved copy and stage-colored artwork.
// Run: node scripts/video/render_evaluation_cards.cjs
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const deps = process.env.CODEX_NODE_MODULES || '/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const { chromium } = require(path.join(deps, 'playwright'));
const sharp = require(path.join(deps, 'sharp'));
const root = path.resolve(__dirname, '../..');
const out = path.join(root, 'course-assets/evaluation-matters');
const reportDir = path.join(root, 'tmp/evaluation-cards-spec');
const selected = process.argv.indexOf('--board');
const boards = require('./assets/evaluation-blue-cards/boards.json').filter(b=>selected<0||b.id===process.argv[selected+1]);
assert.ok(boards.length,'Unknown board');
const escape = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
function html(board) {
  const font = fs.readFileSync(path.join(root, 'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf')).toString('base64');
  const accent = board.accent || "#1652f0", rgb = board.rgb || "22,82,240";
  return `<!doctype html><meta charset="utf-8"><style>
    @font-face{font-family:Jakarta;src:url(data:font/ttf;base64,${font}) format('truetype');font-weight:200 800;font-style:normal}
    *{box-sizing:border-box}html,body{margin:0;background:white}
    body{font-family:Jakarta,sans-serif;color:#0e0a1f}
    .board{width:1600px;padding:31px 40px 40px;background:#eae7fd;border-radius:22px;position:relative;overflow:hidden}
    h1{margin:0 0 26px;font-size:56px;line-height:61px;font-weight:700;letter-spacing:-.03em}
    h1.numbered{position:relative;padding-left:78px}
    .step-marker{position:absolute;left:0;top:8px;width:58px;height:58px;border-radius:50%;background:${accent};color:white;font-size:26px;font-weight:800;letter-spacing:0;line-height:58px;text-align:center}
    .intro{margin-bottom:0}
    .intro-label,.intro h3{font-size:20px;line-height:28px;font-weight:800;color:#1652f0;margin:0}
    .intro-label{margin-bottom:12px;font-size:28px;line-height:36px;font-weight:700;letter-spacing:.02em}
    .intro-grid{display:grid;grid-template-columns:1fr 1fr;gap:32px}
    .intro-grid>div{background:white;border-radius:14px;padding:32px 34px 34px}
    .connector{display:flex;align-items:center;gap:24px;margin:32px 0;font-size:29px;line-height:41px;font-weight:700;color:#0e0a1f;text-align:center}
    .connector:before,.connector:after{content:'';height:1px;background:rgba(${rgb},.22);flex:1}
    .connector span{max-width:1250px}
    .intro h3{margin-bottom:14px;font-size:40px;line-height:48px;font-weight:700;letter-spacing:-.02em;white-space:nowrap}
    .transition{margin:0 0 12px}
    .transition-heading{font-size:28px;line-height:36px;font-weight:700;letter-spacing:.02em;color:${accent};margin:0}
    .cards{display:grid;grid-template-columns:${board.cards.length===2?'744px 744px':'485px 486px 485px'};gap:32px}
    .card{--accent:#4f2fc4;--border:rgba(79,47,196,.22);--divider:rgba(79,47,196,.2);background:white;border-radius:14px;overflow:hidden;position:relative;box-shadow:0 8px 24px rgba(35,25,83,.08)}
    .card:after{content:'';position:absolute;inset:0;border:1px solid var(--border);border-radius:14px;pointer-events:none}
    .art{height:${board.cards.length===2?339:273}px;width:100%;position:relative}
    .art img{display:block;width:100%;height:100%;object-fit:cover}
    .art:before{content:'';position:absolute;inset:0;background:var(--accent);opacity:.10;z-index:1}
    .art:after{content:'';position:absolute;left:0;right:0;bottom:0;border-bottom:1px solid var(--divider)}
    .text{padding:32px 34px 34px}
    h2{margin:0 0 14px;color:var(--accent);font-size:40px;font-weight:700;line-height:48px;letter-spacing:-.02em;white-space:nowrap}
    p{margin:0;font-size:29px;line-height:41px;font-weight:500;color:#3a3550}
    .banner{margin-top:40px;height:88px;border-radius:14px;background:#ffe39a;display:flex;align-items:center;justify-content:center}
    .lockup{display:flex;gap:24px;align-items:center;white-space:nowrap}
    .check{width:44px;height:44px;flex-shrink:0}
    .takeaway{font-size:32px;line-height:32px;font-weight:500}
    .credit{position:absolute;right:40px;bottom:8px;font-size:20px;line-height:24px;font-weight:500;color:#615b78}
  </style><div class="board"><h1 class="${board.step?'numbered':''}">${board.step?`<span class="step-marker">${board.step}</span>`:''}${escape(board.title)}</h1>${board.intro?`<section class="intro"><div class="intro-label">${escape(board.intro.label)}</div><div class="intro-grid">${board.intro.sections.map(c=>`<div><h3>${escape(c.heading)}</h3><p>${escape(c.body)}</p></div>`).join('')}</div></section>`:''}${board.connector?`<div class="connector"><span>${escape(board.connector)}</span></div>`:''}${board.transition?`<div class="transition"><div class="transition-heading">${escape(board.transition.heading)}</div>${board.transition.body?`<p>${escape(board.transition.body)}</p>`:''}</div>`:''}<div class="cards">${board.cards.map(c=>{
    const art = c.art ? fs.readFileSync(path.join(root, `scripts/video/assets/${board.artDirectory || 'evaluation-blue-cards'}/${c.art}.png`)).toString('base64') : null;
    return `<section class="card" style="--accent:${accent};--border:rgba(${rgb},.22);--divider:rgba(${rgb},.2)">${art?`<div class="art"><img src="data:image/png;base64,${art}"></div>`:''}<div class="text"><h2>${escape(c.heading)}</h2><p class="description">${escape(c.body)}</p></div></section>`;
  }).join('')}</div>${board.banner?`<div class="banner"><div class="lockup"><svg class="check" viewBox="0 0 44 44"><circle cx="22" cy="22" r="22" fill="#4f2fc4"/><path d="m12 22 7 7 13-14" fill="none" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="takeaway">${escape(board.banner)}</span></div></div>`:''}<div class="credit">besmarterthanthetool.com</div></div>`;
}

(async()=>{
  fs.mkdirSync(reportDir, {recursive:true});
  const browser = await chromium.launch({executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
  const reports = [];
  try {
    for(const board of boards) {
      const page = await browser.newPage({viewport:{width:1600,height:1600},deviceScaleFactor:1});
      fs.writeFileSync(path.join(reportDir, board.id+'.html'),html(board));
      await page.setContent(html(board), {waitUntil:'load'});
      await page.evaluate(async()=>{
        await document.fonts.ready;
        if(!document.fonts.check('700 40px Jakarta')) throw new Error('Course font did not load');
        const descriptions = [...document.querySelectorAll('.description')];
        const height = Math.max(...descriptions.map(e=>e.getBoundingClientRect().height));
        descriptions.forEach(e=>e.style.height=`${height}px`);
        const texts = [...document.querySelectorAll('.text')];
        const textHeight = Math.max(...texts.map(e=>e.getBoundingClientRect().height));
        texts.forEach(e=>e.style.height=`${textHeight}px`);
      });
      const measures = await page.evaluate(()=>{
        const rect = e => {const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom,right:r.right};};
        const get = s => document.querySelector(s)?rect(document.querySelector(s)):null;
        return {
          board:get('.board'),title:get('h1'),cards:[...document.querySelectorAll('.card')].map(rect),
          art:[...document.querySelectorAll('.art')].map(rect),text:[...document.querySelectorAll('.text')].map(rect),
          banner:get('.banner'),check:get('.check'),lockup:get('.lockup'),
          marker:document.querySelector('.step-marker')?get('.step-marker'):null,
          headings:[...document.querySelectorAll('h2,.intro h3')].map(e=>({overflow:e.scrollWidth>e.clientWidth,size:getComputedStyle(e).fontSize})),
          description:[...document.querySelectorAll('.description')].map(e=>({size:getComputedStyle(e).fontSize,line:getComputedStyle(e).lineHeight})),
          bannerType:document.querySelector('.takeaway')?{size:getComputedStyle(document.querySelector('.takeaway')).fontSize,weight:getComputedStyle(document.querySelector('.takeaway')).fontWeight}:null
        };
      });
      assert.equal(measures.board.width,1600);
      assert.equal(measures.title.x,40);assert.equal(measures.title.y,31);
      if(board.step){assert.equal(measures.marker.width,58);assert.equal(measures.marker.height,58);assert.equal(measures.marker.x,40);assert.equal(measures.marker.y,39);}
      for(const [i,a] of measures.art.entries()){assert.equal(a.width,board.cards.length===2?744:[485,486,485][i]);assert.equal(a.height,board.cards.length===2?339:273);}
      assert.equal(measures.cards[1].x-measures.cards[0].right,32);
      assert.equal(measures.text[0].height,measures.text[1].height);
      if(board.banner){
        assert.equal(measures.banner.y-measures.cards[0].bottom,40);
        assert.equal(measures.banner.height,88);
        assert.equal(measures.board.bottom-measures.banner.bottom,40);
        assert.equal(measures.check.width,44);assert.equal(measures.check.height,44);
        assert.ok(measures.lockup.width<=measures.banner.width-68,'Takeaway overflows safe horizontal padding');
        assert.deepEqual(measures.bannerType,{size:'32px',weight:'500'});
      }else{
        assert.equal(measures.banner,null);
        assert.equal(measures.board.bottom-measures.cards[0].bottom,40);
      }
      assert.ok(measures.headings.every(h=>!h.overflow&&h.size==='40px'));
      assert.ok(measures.description.every(p=>p.size==='29px'&&p.line==='41px'));
      const png = await page.locator('.board').screenshot({type:'png'});
      const file = path.join(out,`evaluation-matters-${board.id}.jpg`);
      await sharp(png).jpeg({quality:95,chromaSubsampling:'4:4:4',optimiseCoding:true}).toFile(file);
      const metadata = await sharp(file).metadata();
      assert.equal(metadata.chromaSubsampling,'4:4:4');
      reports.push({id:board.id,...measures,export:{width:metadata.width,height:metadata.height,sampling:metadata.chromaSubsampling}});
      console.log(`${board.id}: ${metadata.width}×${metadata.height}; EE full-bleed geometry and export checks passed`);
      await page.close();
    }
    fs.writeFileSync(path.join(reportDir,'measurements.json'),JSON.stringify(reports,null,2)+'\n');
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
