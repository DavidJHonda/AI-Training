const {chromium}=require('/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const page=await browser.newPage({viewport:{width:1440,height:1100}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const response=await page.goto('http://127.0.0.1:8765/video-audit/layers-build-v12-2026-10-12/review.html');
 await page.waitForFunction(()=>{const v=document.querySelector('video');return v.readyState>=2&&v.seekable.length&&v.seekable.end(0)>205;});
 const meta=await page.locator('video').evaluate(v=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight,src:v.currentSrc,error:v.error}));
 if(response.status()!==200||Math.abs(meta.duration-206.1)>.1||meta.width!==1280||meta.height!==720||meta.error)throw Error(JSON.stringify(meta));
 for(const [name,seconds] of [['Review revised example',106],['Review conclusion',149],['Play from start',0]]){
  await page.getByRole('button',{name,exact:true}).click();
  await page.waitForFunction(t=>Math.abs(document.querySelector('video').currentTime-t)<1,seconds);
  await page.locator('video').evaluate(v=>v.pause());
 }
 await page.locator('video').evaluate(v=>v.currentTime=114);
 await page.waitForFunction(()=>!document.querySelector('video').seeking);
 await page.screenshot({path:__dirname+'/review-browser.png',fullPage:true});
 await browser.close();
 if(errors.length)throw Error(errors.join('\n'));
 fs.writeFileSync(__dirname+'/browser-check.json',JSON.stringify({status:response.status(),meta,controls:'all three seek/play controls verified',errors},null,2)+'\n');
 console.log(JSON.stringify(meta));
})().catch(e=>{console.error(e);process.exit(1)});
