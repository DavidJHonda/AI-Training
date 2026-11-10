// Refresh upload stills from the current lesson's shared demonstration renderer.
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../..');
const output=path.join(root,'gemini-notebook/how-ai-answers/assets');
const states=[
 [0,'first-prediction','Possible next tokens'],
 [1,'you-selected','AI selected You'],
 [2,'name-prediction','Possible next tokens'],
 [3,'spot-selected','AI selected Spot']
];
(async()=>{
 execFileSync(process.execPath,[path.join(__dirname,'preview_how_ai_answers.cjs')],{stdio:'inherit'});
 const html=fs.readFileSync(path.join(root,'previews/how-ai-answers.html'));
 const server=http.createServer((req,res)=>{res.setHeader('Content-Type','text/html; charset=utf-8');res.end(html);});
 let browser;
 try{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  browser=await chromium.launch({channel:'chrome',headless:true});
  const page=await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
  await page.goto(`http://127.0.0.1:${server.address().port}/?capture=1&step=0`,{waitUntil:'networkidle'});
  // Enlarge the shared scene for a readable 720p upload, without changing the lesson.
  await page.addStyleTag({content:".capture .answer-build-scene{width:760px;transform:scale(1.5);transform-origin:center}.capture .answer-build-prediction{max-width:none}"});
  await page.evaluate(()=>document.fonts.ready);
  fs.mkdirSync(output,{recursive:true});
  for(const [step,name,label] of states){
   await page.evaluate(n=>window.setAnswerScene(n),step);
   await page.locator(`.answer-build-scene[data-step="${step}"]`).waitFor();
   assert.equal(await page.locator('.answer-build-label').innerText(),label);
   assert.equal(await page.locator('button').count(),0);
   assert.ok(await page.locator('.answer-build-scene').evaluate(el=>{const r=el.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight&&r.left>=0&&r.right<=innerWidth&&el.scrollWidth<=el.clientWidth;}));
   const file=path.join(output,`how-ai-answers-${name}.jpg`);
   await page.screenshot({path:file,type:'jpeg',quality:95});
   console.log(file);
  }
 }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);process.exitCode=1;});
