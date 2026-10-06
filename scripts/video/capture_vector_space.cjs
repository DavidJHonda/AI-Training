// Capture shared scene states plus the actual browser animation for IT.
const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../..'),out=path.join(root,'video-audit/vector-space-maps-2026-10-04/frames');
(async()=>{fs.mkdirSync(out,{recursive:true});const browser=await chromium.launch({channel:'chrome',headless:true});try{
const page=await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
await page.goto((process.env.BASE_URL||'http://127.0.0.1:8765')+'/previews/vector-space-maps.html?capture=1');
await page.waitForFunction(()=>typeof window.setVectorScene==='function');await page.evaluate(()=>document.fonts.ready);
for(const [kind,last] of [['cities',4],['drinks',6],['context',1]])for(let step=0;step<=last;step++){
 await page.evaluate(([k,s])=>window.setVectorScene(k,s),[kind,step]);
 await page.waitForFunction(([k,s])=>document.querySelector('.vs-map-frame').dataset.map===k&&document.querySelector('.vs-map-frame').dataset.step===String(s),[kind,step]);
 await page.evaluate(()=>document.getAnimations().forEach(a=>a.finish()));
 const frame=page.locator('.vs-map-frame');const box=await frame.boundingBox();if(box.y<0||box.y+box.height>721)throw new Error(kind+' exceeds video canvas: '+JSON.stringify(box));
 await page.screenshot({path:path.join(out,`${kind}-${step}.png`)});
}
// Flush the starting layout, then pause the CSS animation at each frame time.
await page.evaluate(()=>window.setVectorScene('context',0));await page.waitForFunction(()=>document.querySelector('.vs-map-frame').dataset.step==='0');await page.evaluate(()=>document.getAnimations().forEach(a=>a.finish()));
await page.evaluate(()=>getComputedStyle(document.querySelector('.vs-map-it')).transform);
await page.evaluate(()=>window.setVectorScene('context',1));await page.waitForFunction(()=>document.querySelector('.vs-map-frame').dataset.step==='1');
await page.evaluate(()=>{getComputedStyle(document.querySelector('.vs-map-it')).transform;window.vectorAnimations=document.getAnimations();window.vectorAnimations.forEach(a=>a.pause());});
if(!await page.evaluate(()=>window.vectorAnimations.some(a=>a.effect.target.matches('.vs-map-it'))))throw new Error('IT transition missing');
for(let n=0;n<49;n++){
 await page.evaluate(t=>window.vectorAnimations.forEach(a=>a.currentTime=t),n/30*1000);
 await page.screenshot({path:path.join(out,`context-motion-${String(n).padStart(3,'0')}.png`)});
}
console.log('Captured 14 shared states and 49 browser-animation frames.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
