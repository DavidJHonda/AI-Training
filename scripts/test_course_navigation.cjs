// Sweep every routed lesson, including collapsed reading, without reporting data.
const assert = require('node:assert/strict');
const {chromium,webkit} = require('playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:8893';
const engine = process.env.BROWSER === 'webkit' ? webkit : chromium;
(async()=>{
 const browser=await engine.launch(engine===chromium?{channel:'chrome',headless:true}:{headless:true});
 const sizes=engine===webkit?[['ipad-webkit',820,1180]]:[['ipad',820,1180],['phone',390,844],['desktop',1440,1000]];
 try {
  for(const [name,width,height] of sizes){
   const context=await browser.newContext({viewport:{width,height},hasTouch:name!=='desktop'});
   await context.route(/script\.google|script\.googleusercontent|\.mp4/,r=>r.abort());
   await context.addInitScript(()=>localStorage.setItem('llm-user-name','Navigation Review'));
   const page=await context.newPage(),errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(base+'/course');await page.waitForSelector('#main-content');
   const groups=await page.evaluate(()=>SECTION_GROUPS);
   let count=0;
   for(const group of groups){
    await page.locator('select[aria-label="Choose a course section"]').selectOption(group.sections[0],{force:true});
    for(const id of group.sections){
     await page.locator('select[aria-label^="Choose a lesson"]').selectOption(id,{force:true});
     await page.waitForTimeout(100);
     const toggle=page.locator('.lesson-reading-toggle');
     if(await toggle.count())await toggle.click({force:true});
     await page.waitForTimeout(100);
     assert.equal(await page.getByText('This lesson hit a snag.',{exact:true}).count(),0,name+' '+id);
     assert.equal(await page.locator('#course-runtime-error').count(),0,name+' '+id);
     assert.deepEqual(errors,[],name+' '+id);
     count++;
    }
   }
   assert.equal(count,57);
   console.log('PASS: '+count+' lessons and reading disclosures at '+name+' dimensions');
   await context.close();
  }
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
