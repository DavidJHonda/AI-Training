// Run with the same Playwright NODE_PATH as the other browser regressions.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const base=process.env.BASE_URL||'http://127.0.0.1:8878';
const evidence=process.env.PRE_COURSE_OUTPUT;
const proposed=process.env.PRE_COURSE_SOURCE;
const results=[];
const progress={activeSection:'tokens',visited:['welcome','llms','tokens'],completed:['welcome','llms'],testYourselfQuiz:null};
async function context(browser,size,returning=false){
 const c=await browser.newContext({viewport:size,hasTouch:size.width<1000,reducedMotion:'reduce',locale:'en-US'});c.submissions=[];
 await c.route('**/*',route=>{
  const req=route.request(),u=new URL(req.url());
  if(!['GET','HEAD'].includes(req.method())){c.submissions.push({url:req.url(),body:req.postData()});return route.fulfill({status:200,contentType:'text/plain',body:'ok'});}
  if(/script\.google|script\.googleusercontent/.test(u.hostname))return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({reviews:[],ratingSummary:{total:0,average:null},nextCursor:null})});
  if(/\.mp4$/.test(u.pathname))return route.abort();
  if(proposed&&u.hostname==='127.0.0.1'){let name=u.pathname.slice(1);if(name==='course'||name.startsWith('course/'))name='index.html';const file=path.join(proposed,name);if(fs.existsSync(file)&&fs.statSync(file).isFile())return route.fulfill({status:200,contentType:name.endsWith('.html')?'text/html':name.endsWith('.css')?'text/css':'application/javascript',body:fs.readFileSync(file)});}
  return route.continue();
 });
 if(returning)await c.addInitScript(progress=>{localStorage.setItem('llm-user-name','Phone Review');localStorage.setItem('llm-student-id','phone-entry-review');localStorage.setItem('llm-student-profile',JSON.stringify({firstName:'Phone Review',country:'United States',studentId:'phone-entry-review'}));localStorage.setItem('llm-explorer-progress',JSON.stringify(progress));},progress);
 return c;
}
async function ready(page){await page.evaluate(async()=>{await document.fonts.ready;for(const i of document.images){i.loading='eager';await i.decode().catch(()=>{});}});}
async function settledFrame(page){await page.waitForFunction(()=>{const f=document.querySelector('.start-dialog iframe');if(!f?.contentDocument?.querySelector('.gate-hint'))return false;const phone=matchMedia('(max-width:760px), (pointer:coarse) and (max-height:500px)').matches;return f.contentDocument.body.classList.contains('entry-phone')===phone;});await page.waitForTimeout(150);}
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try {
  for(const [width,height,touch] of [[320,850,true],[390,850,true],[430,850,true],[760,850,true],[761,850,true],[844,390,true],[390,420,true],[1024,1000,false],[1280,1000,false],[1440,1000,false]]){
   const c=await context(browser,{width,height}),p=await c.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
   await p.goto(base+'/',{waitUntil:'networkidle'});assert.ok(p.url().endsWith('/landing.html'));
   await ready(p);const phone=width<=760||touch&&height<=500;
   assert.equal(await p.locator('.course-preview-phone:visible').count(),phone?1:0);
   assert.equal(await p.locator('.course-preview-desktop:visible').count(),phone?0:1);
   if(phone){
    assert.equal(await p.locator('.course-preview-steps > li').count(),3);
    const source=fs.readFileSync(path.join(proposed||process.cwd(),'index.html'),'utf8');const start=source.indexOf('var REMAINING_PHONE_BOARDS = '),end=source.indexOf('\n};',start)+3;const board=new Function('React',source.slice(start,end)+';return REMAINING_PHONE_BOARDS["whats-an-llm-one-word-at-a-time"];')({createElement(){return {};}});
    assert.deepEqual(await p.locator('.course-preview-steps > li > div > p:first-child').allTextContents(),board.cards.map(c=>c.title));
    assert.deepEqual(await p.locator('.course-preview-token strong').allTextContents(),board.cards.map(c=>c.token));
    assert.equal(await p.locator('.course-preview-takeaway').innerText(),board.takeaway);
    const facts=await p.locator('.course-benefit-grid > div').evaluateAll(ns=>ns.map(n=>{const r=n.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,body:parseFloat(getComputedStyle(n.querySelector('dd')).fontSize),heading:parseFloat(getComputedStyle(n.querySelector('dt')).fontSize)};}));
    assert.equal(new Set(facts.map(x=>x.x)).size,1);assert.ok(facts.every((x,i)=>x.body>=16&&x.heading>=20&&(!i||x.y>facts[i-1].y)));
    for(const n of await p.locator('.course-how p,.course-group p,.course-faq details p').evaluateAll(ns=>ns.map(n=>parseFloat(getComputedStyle(n).fontSize))))assert.ok(n>=16);
    const aria=await p.locator('.course-lesson-preview').ariaSnapshot();assert.equal(aria.split('\n').filter(x=>x.includes('heading "One Word at a Time"')).length,1);
   }
   await p.emulateMedia({media:'print'});assert.equal(await p.locator('.course-preview-phone:visible').count(),0);assert.equal(await p.locator('.course-preview-desktop:visible').count(),1);await p.emulateMedia({media:'screen'});
   const trigger=p.getByRole('link',{name:'Start the Course',exact:true}).first();await trigger.click();const frame=p.frameLocator('.start-dialog iframe');await frame.getByRole('combobox',{name:'Country'}).waitFor();await settledFrame(p);
   assert.equal(await frame.getByRole('button',{name:'Let’s go'}).isDisabled(),true);
   await frame.getByRole('textbox',{name:'First name or nickname'}).fill('Phone Review');await frame.getByRole('combobox',{name:'Country'}).fill('United States');assert.equal(await frame.getByRole('button',{name:'Let’s go'}).isDisabled(),true,'Typed text must be selected as a valid country');
   await frame.getByRole('option',{name:'United States',exact:true}).click();assert.equal(await frame.getByRole('button',{name:'Let’s go'}).isEnabled(),true);
   const metrics=await p.frames()[1].evaluate(()=>({viewport:innerHeight,document:document.documentElement.scrollHeight,font:parseFloat(getComputedStyle(document.querySelector('.gate-hint')).fontSize)}));
   if(phone){assert.ok(metrics.document<=metrics.viewport+1,'No internal iframe scrolling');assert.ok(metrics.font>=16);}
   else assert.equal(metrics.font,13,'Desktop embedded form keeps its original typography');
   await frame.getByRole('button',{name:'Let’s go'}).scrollIntoViewIfNeeded();const rect=await frame.getByRole('button',{name:'Let’s go'}).boundingBox();assert.ok(rect.y>=0&&rect.y+rect.height<=height);
   await frame.getByRole('textbox',{name:'First name or nickname'}).focus();await p.keyboard.press('Escape');await p.waitForFunction(()=>!document.querySelector('.start-dialog').open);assert.equal(await trigger.evaluate(n=>n===document.activeElement),true);
   // Resizing must preserve the same form values and iframe instance.
   await trigger.click();await frame.getByRole('textbox',{name:'First name or nickname'}).fill('Keep my name');const originalFrame=p.frames()[1];await p.setViewportSize({width:width===1280?390:1280,height:1000});await settledFrame(p);assert.equal(p.frames()[1],originalFrame);assert.equal(await frame.getByRole('textbox',{name:'First name or nickname'}).inputValue(),'Keep my name');assert.equal(await frame.getByRole('combobox',{name:'Country'}).inputValue(),'United States');await p.getByRole('button',{name:'Close course entry'}).click();await p.setViewportSize({width,height});
   for(const slug of ['whats-an-llm','why-learn-ai','for-groups']){
    await p.goto(base+'/course/'+slug,{waitUntil:'networkidle'});await ready(p);assert.equal(await p.locator('.course-guest-shell').count(),1);
    if(phone){assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Guest page fits the viewport');assert.equal(await p.locator('.desktop-section-map:visible,.desktop-lesson-nav:visible').count(),0);assert.equal(await p.locator('.mobile-course-nav:visible').count(),1);const label=await p.locator('.course-cta > span').evaluate(n=>({height:n.getBoundingClientRect().height,line:parseFloat(getComputedStyle(n).lineHeight)}));assert.ok(label.height<label.line*1.5,'Start label stays on one line');}
    const next=p.locator('.guest-lesson-navigation > button').last();await next.click();await p.getByRole('heading',{name:'Ready for the rest?'}).waitFor();await p.getByRole('button',{name:slug==='for-groups'?'Keep browsing activities':'Keep trying the lesson'}).click();
    if(slug==='for-groups'){await p.locator('input[aria-label="Search activities"]').fill('One Word at a Time');await p.waitForFunction(()=>document.querySelectorAll('.group-directory-rows > li').length===1);assert.equal(await p.locator('.group-directory-rows > li').count(),1);await p.locator('input[aria-label="Search activities"]').fill('');await p.selectOption('select[aria-label="Course section"]','Build Your Skills');await p.waitForFunction(()=>document.querySelectorAll('.group-directory-section').length===1);assert.equal(await p.locator('.group-directory-section').count(),1);}
   }
   assert.deepEqual(errors,[]);assert.equal(c.submissions.length,0,'Read-only flow sent no data');results.push({width,height,phone,entry:metrics,phoneOverflow:phone?'none':'not a phone viewport',errors});await c.close();console.log('PASS',width,height);
  }
  // New enrollment is exercised only against intercepted local responses.
  const fresh=await context(browser,{width:390,height:850}),p=await fresh.newPage();await p.goto(base+'/landing.html');await p.getByRole('link',{name:'Start the Course',exact:true}).first().click();let f=p.frameLocator('iframe');await f.getByRole('textbox',{name:'First name or nickname'}).fill('Phone Review');await f.getByRole('combobox',{name:'Country'}).fill('United');await f.getByRole('option',{name:'United States',exact:true}).click();await f.getByRole('button',{name:'Let’s go'}).click();await p.waitForURL(base+'/course');assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem('llm-explorer-progress')).activeSection),'welcome');assert.equal(fresh.submissions.length,1);assert.equal(JSON.parse(fresh.submissions[0].body).eventType,'enrollment');await fresh.close();
  const returning=await context(browser,{width:390,height:850},true),rp=await returning.newPage();await rp.goto(base+'/landing.html');const saved=await rp.evaluate(()=>localStorage.getItem('llm-explorer-progress'));await rp.getByRole('link',{name:'Continue the Course',exact:true}).first().click();await rp.waitForURL(base+'/course');assert.equal(await rp.evaluate(()=>localStorage.getItem('llm-explorer-progress')),saved);assert.equal(await rp.locator('.course-guest-shell').count(),0);
  await rp.goto(base+'/course/whats-an-llm');await rp.locator('.course-cta').click();await rp.locator('.sample-start').click();f=rp.frameLocator('iframe');await f.getByRole('textbox',{name:'First name or nickname'}).waitFor();assert.equal(await f.getByRole('textbox',{name:'First name or nickname'}).inputValue(),'Phone Review');assert.equal(await f.getByRole('combobox',{name:'Country'}).inputValue(),'United States');await f.getByRole('button',{name:'Let’s go'}).click();await rp.waitForURL(base+'/course');assert.equal(await rp.evaluate(()=>localStorage.getItem('llm-explorer-progress')),saved);assert.equal(returning.submissions.length,0,'Unchanged returning details do not enroll again');await returning.close();
  // A short desktop window with a fine pointer keeps the original desktop branches.
  const fine=await browser.newContext({viewport:{width:844,height:390},hasTouch:false});await fine.route(/\.mp4|script\.google/,r=>r.abort());const fp=await fine.newPage();await fp.goto(base+'/landing.html');assert.equal(await fp.locator('.course-preview-phone:visible').count(),0);await fp.getByRole('link',{name:'Start the Course',exact:true}).first().click();await settledFrame(fp);assert.equal(await fp.frames()[1].evaluate(()=>getComputedStyle(document.querySelector('.gate-hint')).fontSize),'13px');await fine.close();
  if(evidence){fs.mkdirSync(evidence,{recursive:true});fs.writeFileSync(path.join(evidence,'phone-functional-checks.json'),JSON.stringify({results,newEnrollment:'PASS with intercepted local response',returningProgress:'preserved byte-for-byte',repeatEnrollment:'no duplicate POST'},null,2));}
  console.log('PASS: public phone layout, exact board wording, accessible visibility, form validation, resizing, keyboard escape/focus, guest navigation, filters, new enrollment and returning progress. No external submissions.');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
