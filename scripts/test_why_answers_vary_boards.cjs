const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('node:fs'),assert=require('node:assert/strict');
(async()=>{
const browser=await chromium.launch({channel:'chrome',headless:true});
try{
 const page=await browser.newPage({viewport:{width:1280,height:1000}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.route(/script\.google|script\.googleusercontent|\.mp4/,r=>r.abort());
 await page.addInitScript(()=>{localStorage.setItem('llm-user-name','Preview');localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'inference',visited:['inference'],completed:[]}));});
 await page.goto((process.env.BASE_URL || 'http://127.0.0.1:8797')+'/index.html',{waitUntil:'domcontentloaded'});
 const toggle=page.locator('.lesson-reading-toggle');if(await toggle.getAttribute('aria-expanded')==='false')await toggle.click();
 await page.locator('.vary-board').first().waitFor();await page.evaluate(()=>document.fonts.ready);
 fs.mkdirSync('output/why-answers-vary-mobile',{recursive:true});
 for(const width of [1280,761,760,390,320]){
  await page.setViewportSize({width,height:1000});
  for(const kind of ['overview','sampling','temperature']){
   const board=page.locator(`[data-vary-board="${kind}"]`);
   assert.equal(await board.locator('.vary-board-mobile').isVisible(),width<=760);
   assert.equal(await board.locator('.vary-board-desktop').isVisible(),width>760);
   const overflow=await board.evaluate(n=>[...n.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().width>0 && e.scrollWidth>e.clientWidth+1 && !(e instanceof SVGElement)).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,45),w:e.clientWidth,scroll:e.scrollWidth})));
   assert.deepEqual(overflow,[],`No clipped content: ${width}px ${kind}`);
   if(width<=760){
    const textSizes=await board.locator('.vary-board-mobile p, .vary-board-odds li').evaluateAll(nodes=>nodes.map(n=>parseFloat(getComputedStyle(n).fontSize)));
    assert.ok(textSizes.every(size=>size>=16),'Body text stays at least 16px');
   }
   await board.screenshot({path:`output/why-answers-vary-mobile/${width}-${kind}.png`,style:'.no-print:has(> .sticky-inner) { visibility: hidden !important; }'});
  }
 }
 const temperature=page.locator('[data-vary-board="temperature"] .vary-board-mobile');
 const expected=[[36,21,15,6,3,19],[22,17,14,9,6,32],[16,14,13,10,8,39]];
 for(let i=0;i<3;i++){
  const card=temperature.locator('.vary-board-card').nth(i);
  assert.deepEqual(await card.locator('.vary-board-odds strong').allTextContents(),expected[i].map(n=>n+'%'));
  const widths=await card.locator('.vary-board-bar > span').evaluateAll(nodes=>nodes.map(n=>parseFloat(n.style.width)));
  widths.forEach((width,j)=>assert.ok(Math.abs(width-expected[i][j]/40*100)<0.001,'Every bar uses the shared 40% maximum scale'));
 }
 assert.deepEqual(await page.locator('.vary-board-picks li').allTextContents(),['Max','Spot','Buddy','Rex','Max']);
 assert.deepEqual(errors,[]);
 await page.emulateMedia({media:'print'});
 assert.equal(await page.locator('.vary-board-mobile:visible').count(),0);
 assert.equal(await page.locator('.vary-board-desktop:visible').count(),3);
 const landscape=await browser.newPage({viewport:{width:844,height:390},hasTouch:true});
 await landscape.goto((process.env.BASE_URL || 'http://127.0.0.1:8797')+'/index.html?print=lesson:inference',{waitUntil:'domcontentloaded'});
 await landscape.locator('.vary-board').first().waitFor();
 assert.equal(await landscape.locator('.vary-board-mobile:visible').count(),3,'Landscape phones also get readable cards');
 assert.equal(await landscape.locator('.vary-board-desktop:visible').count(),0);
 console.log('PASS: desktop and phone layouts, readable text, no clipping, unchanged odds and bar scale, sampling sequence, print, and no runtime errors');
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
