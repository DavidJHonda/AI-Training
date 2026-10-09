// Run with node scripts/test_temperature_demo.cjs. Uses the shared guided shell.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {spawn} = require('node:child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || '/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const base=process.env.BASE_URL || 'http://127.0.0.1:8792';
(async()=>{
 const server=process.env.BASE_URL ? null : spawn('python3',['-m','http.server','8792','--bind','127.0.0.1'],{stdio:'ignore'});
 let browser;
 try {
  browser=await chromium.launch({channel:'chrome',headless:true});
  const page=await browser.newPage({viewport:{width:1280,height:1100}});
  const errors=[]; page.on('pageerror',e=>errors.push(e.message));
  await page.route(/script\.google|script\.googleusercontent|\.mp4/,r=>r.abort());
  await page.addInitScript(()=>{localStorage.setItem('llm-user-name','Preview');localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'inference',visited:['inference'],completed:[]}));});
  await page.goto(base);
  const demo=page.locator('.guided-demo[data-kind="temperature"]');
  await demo.waitFor();
  await page.evaluate(()=>document.fonts.ready);
  await page.addStyleTag({content:'.sticky-lesson-bar{visibility:hidden!important}'});
  fs.mkdirSync('tmp/temperature-demo',{recursive:true});
  assert.equal(await page.locator('img[src*="the-next-token-temperature"]').count(),0);
  assert.equal(await page.getByText('Two important points:',{exact:true}).count(),0);
  assert.equal(await page.getByText('How Big Is 2 Quadrillion?',{exact:false}).count(),0,'Scale quiz replaced');
  assert.equal(await page.getByText('Match the Concepts',{exact:false}).count(),1);
  for(const width of [1280,540,390,320]) {
   await page.setViewportSize({width,height:1100});
   let geometry;
   for(let step=0;step<4;step++) {
    if(step){await demo.getByRole('button',{name:'See It',exact:true}).focus();await page.keyboard.press(step%2?'Enter':'Space');}
    assert.equal(await demo.locator('.temperature-scene').getAttribute('data-step'),String(step));
    assert.equal(await demo.locator('.temperature-value:not(.is-pending)').count(),6*Math.min(step+1,3));
    assert.equal(await demo.locator('tr.is-focus').count(),step===3?1:0,'Final comparison highlighted only on reveal');
    assert.equal(await demo.getByText('Your prompt',{exact:true}).count(),0);
    assert.equal(await demo.locator('.temperature-context').count(),0);
    assert.equal(await demo.locator('.temperature-reply').innerText(),'Answer so far\nYou could name him ___');
    for(let col=0;col<=Math.min(step,2);col++) {
     const values=await demo.locator(`td.temperature-column-${col} .temperature-value`).allTextContents();
     assert.equal(values.reduce((sum,v)=>sum+parseInt(v),0),100,'Each complete distribution totals 100%');
    }
    const current=await demo.evaluate(el=>{
     const r=el.getBoundingClientRect(),controls=el.querySelector('.guided-demo-controls').getBoundingClientRect(),scene=el.querySelector('.temperature-scene').getBoundingClientRect();
     return {controls:controls.top-r.top,scene:scene.top-r.top,height:r.height,fits:el.scrollWidth<=el.clientWidth && r.right<=innerWidth};
    });
    assert.ok(current.fits,`No horizontal overflow at ${width}/${step}`);
    if(geometry) for(const field of ['controls','scene','height']) assert.ok(Math.abs(current[field]-geometry[field])<1,`Stable ${field} at ${width}/${step}`);
    geometry=current;
    await demo.screenshot({path:`tmp/temperature-demo/${width}-${step}.png`,animations:'disabled'});
   }
   const replay=demo.getByRole('button',{name:'Replay',exact:true});
   assert.ok(await replay.evaluate(el=>el===document.activeElement),'Completion focuses Replay');
   await page.keyboard.press('Enter');
   assert.equal(await demo.locator('.temperature-scene').getAttribute('data-step'),'0');
   assert.ok(await demo.getByRole('button',{name:'See It',exact:true}).evaluate(el=>el===document.activeElement),'Replay focuses See It');
  }
  await page.emulateMedia({reducedMotion:'reduce'});
  assert.ok(await demo.locator('.temperature-bar > span').first().evaluate(el=>parseFloat(getComputedStyle(el).transitionDuration)<=0.00001),'Reduced motion has no perceptible animation');
  await page.addStyleTag({content:'.guided-demo-instruction-text p{font-size:34px!important}'});
  for(let step=0;step<4;step++) {
   if(step) await demo.getByRole('button',{name:'See It',exact:true}).click();
   assert.ok(await demo.locator('.guided-demo-instruction-text').evaluate(el=>el.scrollHeight<=el.clientHeight),'Enlarged instructions are not clipped');
  }
  await page.setViewportSize({width:960,height:1200});
  await page.goto(base+'/?print=lesson:inference');
  await demo.waitFor();
  assert.equal(await demo.locator('.temperature-scene').getAttribute('data-step'),'3');
  assert.equal(await demo.getByRole('button').count(),0);
  assert.equal(await demo.locator('.temperature-value:not(.is-pending)').count(),18);
  await demo.screenshot({path:'tmp/temperature-demo/print.png'});
  await page.goto(base+'/previews/temperature.html');
  await demo.waitFor();
  assert.equal(await demo.locator('.temperature-scene').getAttribute('data-step'),'0');
  await page.goto(base+'/previews/temperature.html?capture=1&step=3');
  await page.locator('.temperature-scene[data-step="3"]').waitFor();
  assert.equal(await page.getByRole('button').count(),0);
  assert.deepEqual(errors,[]);
  console.log('Temperature demo passed: all four states, keyboard/replay focus, stable layout at four widths, probability totals, reduced motion, enlarged text, and completed print view.');
 }finally{if(browser)await browser.close();if(server)server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
