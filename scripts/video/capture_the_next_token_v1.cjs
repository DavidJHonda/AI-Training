// Capture the existing live temperature component; no page or source asset edits.
const {chromium}=require('/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('node:path');
const root=path.resolve(__dirname,'../..');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try {
  const page=await browser.newPage({viewport:{width:1280,height:900},deviceScaleFactor:2});
  await page.goto('file://'+root+'/previews/temperature.html?capture=1&step=0');
  await page.locator('.temperature-scene').waitFor();
  await page.evaluate(()=>document.fonts.ready);
  for(let step=0;step<4;step++){
   await page.evaluate(n=>window.setTemperatureScene(n),step);
   await page.locator(`.temperature-scene[data-step="${step}"]`).waitFor();
   await page.locator('.temperature-scene').screenshot({path:root+`/video-audit/the-next-token-build-2026-10-09-v1/temperature-${step}.png`,animations:'disabled'});
  }
  console.log('Captured four current TemperatureScene states.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
