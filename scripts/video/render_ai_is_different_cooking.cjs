#!/usr/bin/env node
// AI is Different: canonical Editorial Explainer, Two-Card Full-Bleed (EE-2FB).
// Rebuild: node scripts/video/render_ai_is_different_cooking.cjs
// Text-only Notebook upload: add --upload-variant; canonical JPG stays unchanged.
// Text and layout are deterministic; the two text-free art inputs are ImageGen outputs.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const {execFileSync} = require('node:child_process');
const deps = process.env.CODEX_NODE_MODULES || '/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium} = require(path.join(deps,'playwright'));
const sharp = require(path.join(deps,'sharp'));
const root = path.resolve(__dirname,'../..');
const uploadVariant = process.argv.includes('--upload-variant');
const relative = uploadVariant ? 'gemini-notebook/ai-is-different/assets/ai-is-different-cooking-analogy-faceless.jpg' : 'course-assets/ai-is-different/ai-is-different-cooking-analogy.jpg';
const reportDir = path.join(root,uploadVariant ? 'tmp/ai-is-different-cooking-upload' : 'tmp/ai-is-different-cooking');
const cards = [
 {title:'Rule-Based Software',art:'cooking-robot.png',takeaway:'Same recipe. Same result every time.',body:'Rule-based software is like a cooking robot following a recipe. Someone wrote the steps. The robot measures the ingredients, follows the instructions, and repeats the process.'},
 {title:'AI',art:'chef-station.png',takeaway:'Learned patterns. Different dishes.',body:'AI is like a chef who learned from preparing many different dishes. The chef recognizes patterns: which ingredients work together, how cooking methods affect food, and what substitutions might work. The chef doesn’t need a recipe.'}
];
const escape = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
function html(){
 const font=fs.readFileSync(path.join(root,'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf')).toString('base64');
 return `<!doctype html><html lang="en"><meta charset="utf-8"><style>
 @font-face{font-family:Jakarta;src:url(data:font/ttf;base64,${font}) format('truetype');font-weight:200 800}
 *{box-sizing:border-box}html,body{margin:0;background:white}body{font-family:Jakarta,sans-serif;color:#0e0a1f}
 .board{width:1600px;padding:31px 40px 40px;background:#eae7fd;border-radius:22px;position:relative;overflow:hidden}
 h1{margin:0 0 26px;font-size:56px;line-height:61px;font-weight:700;letter-spacing:-.03em}
 .cards{display:grid;grid-template-columns:744px 744px;gap:32px}
 .card{--accent:#4f2fc4;--border:rgba(79,47,196,.22);--divider:rgba(79,47,196,.2);background:white;border-radius:14px;overflow:hidden;position:relative;box-shadow:0 8px 24px rgba(35,25,83,.08)}
 .card:nth-child(2){--accent:#1652f0;--border:rgba(22,82,240,.22);--divider:rgba(22,82,240,.2)}
 .card:after{content:'';position:absolute;inset:0;border:1px solid var(--border);border-radius:14px;pointer-events:none}
 .art{height:339px;width:744px;position:relative}.art img{display:block;width:100%;height:100%;object-fit:cover}
 .art:after{content:'';position:absolute;left:0;right:0;bottom:0;border-bottom:1px solid var(--divider)}
 .text{padding:32px 34px 34px}h2{margin:0 0 14px;color:var(--accent);font-size:40px;font-weight:700;line-height:48px;letter-spacing:-.02em;white-space:nowrap}
 p{margin:0;font-size:29px;line-height:41px;font-weight:500;color:#3a3550}
 .card-takeaway{margin-top:24px;padding-top:24px;border-top:1px solid var(--divider);color:var(--accent);font-weight:700}
 .credit{position:absolute;right:40px;bottom:8px;font-size:20px;line-height:24px;font-weight:500;color:#615b78}
 </style><div class="board"><h1>A Cooking Analogy</h1><div class="cards">${cards.map(c=>{
 const art=fs.readFileSync(path.join(root,'scripts/video/assets/ai-is-different',c.art)).toString('base64');
 return `<section class="card"><div class="art">${uploadVariant ? '' : `<img alt="" src="data:image/png;base64,${art}">`}</div><div class="text"><h2>${escape(c.title)}</h2><p class="description">${escape(c.body)}</p><p class="card-takeaway">${escape(c.takeaway)}</p></div></section>`;
 }).join('')}</div><div class="credit">besmarterthanthetool.com</div></div></html>`;
}
(async()=>{
 fs.mkdirSync(reportDir,{recursive:true});
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1600,height:1500},deviceScaleFactor:1});
  await page.setContent(html(),{waitUntil:'load'});
  await page.evaluate(async()=>{await document.fonts.ready;const descriptions=[...document.querySelectorAll(".description")];const descriptionHeight=Math.max(...descriptions.map(n=>n.getBoundingClientRect().height));descriptions.forEach(n=>n.style.height=descriptionHeight+"px");const texts=[...document.querySelectorAll('.text')];const height=Math.max(...texts.map(n=>n.getBoundingClientRect().height));texts.forEach(n=>n.style.height=height+'px');});
  const measures=await page.evaluate(()=>{
   const rect=n=>{const r=n.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
   return {board:rect(document.querySelector('.board')),title:rect(document.querySelector('h1')),cards:[...document.querySelectorAll('.card')].map(rect),art:[...document.querySelectorAll('.art')].map(rect),text:[...document.querySelectorAll('.text')].map(rect),takeaways:[...document.querySelectorAll('.card-takeaway')].map(rect),headings:[...document.querySelectorAll('h2')].map(n=>({size:getComputedStyle(n).fontSize,overflow:n.scrollWidth>n.clientWidth})),body:[...document.querySelectorAll('p')].map(n=>({size:getComputedStyle(n).fontSize,line:getComputedStyle(n).lineHeight,overflow:n.scrollWidth>n.clientWidth}))};
  });
  assert.equal(measures.board.width,1600);assert.equal(measures.title.x,40);assert.equal(measures.title.y,31);
  measures.art.forEach(r=>{assert.equal(r.width,744);assert.equal(r.height,339);});
  assert.equal(measures.cards[1].x-measures.cards[0].right,32);
  assert.equal(measures.text[0].height,measures.text[1].height);
  assert.equal(measures.takeaways[0].y,measures.takeaways[1].y);
  assert.equal(measures.board.bottom-measures.cards[0].bottom,40);
  assert.ok(measures.headings.every(h=>h.size==='40px'&&!h.overflow));
  assert.ok(measures.body.every(p=>p.size==='29px'&&p.line==='41px'&&!p.overflow));
  const png=await page.locator('.board').screenshot({type:'png'});
  const file=path.join(root,relative);
  await sharp(png).jpeg({quality:95,chromaSubsampling:'4:4:4',optimiseCoding:true}).toFile(file);
  if (!uploadVariant) execFileSync('bash',[path.join(root,'scripts/finalize-course-asset.sh'),file],{cwd:root});
  const metadata=await sharp(file).metadata();
  if (!uploadVariant) {
  const manifestPath=path.join(root,'course-assets/manifest.json');const manifest=JSON.parse(fs.readFileSync(manifestPath,'utf8'));
  const asset={new:relative,sha256:crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),bytes:fs.statSync(file).size,width:metadata.width,height:metadata.height,reference_files:['index.html','lessons/ai-is-different.md'],generator:'scripts/video/render_ai_is_different_cooking.cjs',purpose:'EE-2FB cooking analogy: written recipe steps versus learned patterns.'};
  manifest.generated_assets=(manifest.generated_assets||[]).filter(a=>a.new!==relative);manifest.generated_assets.push(asset);
  fs.writeFileSync(manifestPath,JSON.stringify(manifest,null,2)+'\n');
  }
  fs.writeFileSync(path.join(reportDir,'measurements.json'),JSON.stringify(measures,null,2)+'\n');
  console.log(`${relative}: ${metadata.width}x${metadata.height}; EE-2FB geometry, typography, and equal card heights verified.`);
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
