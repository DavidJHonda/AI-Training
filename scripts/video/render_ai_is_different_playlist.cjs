#!/usr/bin/env node
// Canonical playlist comparison board. Exact table and labels; ImageGen notes.
// Rebuild: node scripts/video/render_ai_is_different_playlist.cjs
// Shared lesson/video asset. Do not regenerate it with the legacy structured-data renderer.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const deps = process.env.CODEX_NODE_MODULES || '/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium} = require(path.join(deps, 'playwright'));
const sharp = require(path.join(deps, 'sharp'));
const root = path.resolve(__dirname, '../..');
const relative = 'course-assets/ai-is-different/ai-is-different-playlist-formats.jpg';
const font = fs.readFileSync(path.join(root, 'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf')).toString('base64');
const art = fs.readFileSync(path.join(root, 'scripts/video/assets/ai-is-different/playlist/handwritten-notes.png')).toString('base64');
const html = `<!doctype html><html lang="en"><meta charset="utf-8"><style>
@font-face{font-family:Jakarta;src:url(data:font/ttf;base64,${font});font-weight:200 800}
*{box-sizing:border-box}body{margin:0;font-family:Jakarta,sans-serif;color:#0e0a1f}
.board{width:1600px;padding:31px 40px 40px;background:#eae7fd;border-radius:22px;position:relative}
h1{font-size:56px;line-height:61px;letter-spacing:-.03em;font-weight:700;margin:0 0 26px}
.sheet{background:white;border-radius:18px;padding:34px;display:grid;grid-template-columns:710px 710px;gap:32px}
h2{font-size:40px;line-height:48px;font-weight:700;letter-spacing:-.02em;margin:0 0 8px;color:#4f2fc4}
.column:last-child h2{color:#1652f0}
.format{font-size:29px;line-height:41px;font-weight:600;color:#3a3550;margin:0 0 24px}
.evidence{height:400px;display:flex;align-items:center}
img{width:710px;height:400px;object-fit:contain;display:block;border-radius:8px}
table{border-collapse:collapse;width:100%;table-layout:fixed;font-size:29px;line-height:38px;border:1px solid #d9d3ef}
th{font-weight:700;text-align:left;background:#f0edfc;color:#4f2fc4;height:100px}
th,td{padding:18px;border-bottom:1px solid #d9d3ef;border-right:1px solid #d9d3ef}
td{height:94px;font-weight:500;color:#3a3550}th:last-child,td:last-child{text-align:center}
tbody tr:nth-child(even){background:#faf9fe}
.credit{position:absolute;right:40px;bottom:8px;font-size:20px;line-height:24px;color:#615b78}
</style><div class="board"><h1>Same Playlist. Different Formats.</h1><div class="sheet">
<section class="column"><h2>Traditional Software</h2><h3 class="format">Structured Data</h3><div class="evidence"><table><colgroup><col style="width:38%"><col style="width:36%"><col style="width:26%"></colgroup><thead><tr><th>Song</th><th>Artist</th><th>Play Order</th></tr></thead><tbody><tr><td>Blinding Lights</td><td>The Weeknd</td><td>1</td></tr><tr><td>Levitating</td><td>Dua Lipa</td><td>2</td></tr><tr><td>As It Was</td><td>Harry Styles</td><td>3</td></tr></tbody></table></div></section>
<section class="column"><h2>AI</h2><h3 class="format">Unstructured Data</h3><div class="evidence"><img src="data:image/png;base64,${art}" alt="Handwritten playlist with arrows and a crossed-out song"></div></section>
</div><div class="credit">besmarterthanthetool.com</div></div></html>`;
(async()=>{
 const browser = await chromium.launch({channel:'chrome',headless:true});
 try {
  const page = await browser.newPage({viewport:{width:1600,height:1100},deviceScaleFactor:1});
  await page.setContent(html); await page.evaluate(()=>document.fonts.ready);
  const geometry = await page.evaluate(()=>({width:document.querySelector('.board').getBoundingClientRect().width,overflow:[...document.querySelectorAll('h1,h2,h3,th,td')].filter(e=>e.scrollWidth>e.clientWidth).map(e=>e.textContent)}));
  assert.equal(geometry.width,1600);assert.deepEqual(geometry.overflow,[]);
  const png = await page.locator('.board').screenshot();
  const file = path.join(root,relative);
  await sharp(png).jpeg({quality:95,chromaSubsampling:'4:4:4',optimiseCoding:true}).toFile(file);
  const meta = await sharp(file).metadata();
  const manifestPath = path.join(root,'course-assets/manifest.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath,'utf8'));
  const asset = {new:relative,sha256:crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),bytes:fs.statSync(file).size,width:meta.width,height:meta.height,reference_files:['index.html','lessons/ai-is-different.md','gemini-notebook/upload-sets.json'],generator:'scripts/video/render_ai_is_different_playlist.cjs',purpose:'Same three songs in structured fields and unstructured handwritten notes. Shared page/preparation board.'};
  manifest.generated_assets=(manifest.generated_assets||[]).filter(a=>a.new!==relative);manifest.generated_assets.push(asset);
  fs.writeFileSync(manifestPath,JSON.stringify(manifest,null,2)+'\n');
  console.log(`${relative}: ${meta.width}x${meta.height}; no text overflow.`);
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
