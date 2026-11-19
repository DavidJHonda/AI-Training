// Run with NODE_PATH pointing to Playwright and scripts/serve-site.py on BASE_URL.
// All reporting requests are intercepted; no enrollment, feedback, or email is sent.
const assert = require('node:assert/strict');
const {chromium, webkit} = require('playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:8893';
const engine = process.env.BROWSER === 'webkit' ? webkit : chromium;
(async () => {
  const browser = await engine.launch(engine === chromium ? {channel:'chrome',headless:true} : {headless:true});
  async function context(seed = {}) {
    const c = await browser.newContext({viewport:{width:820,height:1180},hasTouch:true});
    await c.route(/script\.google|script\.googleusercontent|\.mp4/, r => r.abort());
    await c.addInitScript(seed => {
      if (sessionStorage.getItem('resilience-seeded')) return;
      localStorage.setItem('llm-user-name','Review');
      for (const [key,value] of Object.entries(seed)) localStorage.setItem(key,value);
      sessionStorage.setItem('resilience-seeded','1');
    },seed);
    return c;
  }
  async function open(c) {
    const p = await c.newPage();
    await p.goto(base+'/course');
    await p.waitForSelector('#main-content');
    return p;
  }
  async function progress(p) { return p.evaluate(() => JSON.parse(localStorage.getItem('llm-explorer-progress'))); }
  async function navigate(p, id) {
    const group = await p.evaluate(id => SECTION_GROUPS.find(g=>g.sections.includes(id)).sections[0], id);
    await p.locator('select[aria-label="Choose a course section"]').selectOption(group,{force:true});
    await p.locator('select[aria-label^="Choose a lesson"]').selectOption(id,{force:true});
  }
  try {
    // Uncaught errors and rejected promises must leave the same React root in place.
    let c = await context(), p = await open(c);
    await p.evaluate(() => { window.reviewRoot = document.getElementById('root'); setTimeout(()=>{throw Error('Review <img src=x onerror=alert(1)>')},0); });
    await p.locator('#course-runtime-error').waitFor();
    assert(await p.evaluate(()=>document.getElementById('root')===window.reviewRoot));
    assert.equal(await p.locator('#course-runtime-error img').count(),0);
    assert.match(await p.locator('#course-runtime-error pre').textContent(),/Review <img/);
    if(process.env.REVIEW_SCREENSHOTS) await p.screenshot({path:process.env.REVIEW_SCREENSHOTS+'/course-error-'+engine.name()+'.png'});
    await navigate(p,'openerskills');
    assert.equal((await progress(p)).activeSection,'openerskills');
    await p.getByRole('button',{name:'Dismiss error'}).click();
    await p.evaluate(()=>{void Promise.reject(Error('Review rejected action'));});
    await p.locator('#course-runtime-error').waitFor();
    assert.match(await p.locator('#course-runtime-error pre').textContent(),/Review rejected action/);
    await p.getByRole('button',{name:'Reload course'}).click();
    await p.waitForSelector('#main-content');
    assert.equal(await p.locator('#course-runtime-error').count(),0);
    await c.close();
    console.log('PASS: uncaught errors preserve navigation, escape diagnostics, and allow reload');

    // Bad shapes and old IDs recover while keeping valid earned credit.
    for (const raw of ['null','[]','{broken',JSON.stringify({activeSection:'openerskills',completed:{},visited:4}),JSON.stringify({activeSection:'engagementtrap',completed:['welcome','welcome',null,'obsolete'],visited:['control',{}]})]) {
      c = await context({'llm-explorer-progress':raw}); p = await open(c);
      assert.equal(await p.locator('#course-runtime-error').count(),0);
      await navigate(p,'critical');
      const saved = await progress(p);
      assert(Array.isArray(saved.completed)); assert(Array.isArray(saved.visited));
      assert.equal(saved.activeSection,'critical');
      if(raw.includes('obsolete')) assert.deepEqual(saved.completed,['welcome']);
      await c.close();
    }
    console.log('PASS: invalid progress recovers and valid completions survive');

    // A full/blocked store must not roll back progress that is still in memory.
    c = await context({'llm-explorer-progress':JSON.stringify({activeSection:'welcome',visited:['welcome'],completed:[]})});
    p = await open(c);
    await p.evaluate(()=>{Storage.prototype.setItem=function(){throw new DOMException('Full','QuotaExceededError');};});
    await p.locator('.lesson-navigation button').last().click();
    await p.locator('.lesson-navigation button').last().click();
    assert.equal(await p.locator('select[aria-label^="Choose a lesson"]').inputValue(),'whydeeper');
    assert.equal(await p.locator('#course-runtime-error').count(),0);
    assert.equal(await p.locator('.course-user-progress').innerText().then(t=>/2\s+of 54/.test(t)),true);
    await c.close();
    console.log('PASS: storage write failures retain in-memory progress');

    // Deliberately suppress storage notifications in tab B to verify read-before-write.
    c = await context(); const a = await open(c), b = await c.newPage();
    await b.addInitScript(()=>{
      const add = window.addEventListener.bind(window);
      window.addEventListener = (name,handler,options) => { if(name!=='storage') add(name,handler,options); };
    });
    await b.goto(base+'/course'); await b.waitForSelector('#main-content');
    await a.locator('.lesson-navigation button').last().click();
    assert.deepEqual((await progress(a)).completed,['welcome']);
    await navigate(b,'openerskills');
    assert.deepEqual((await progress(b)).completed,['welcome']);
    await b.locator('.lesson-navigation button').last().click();
    assert.deepEqual((await progress(b)).completed,['welcome','openerskills']);
    // A receives new credit without being moved out of the lesson it is reading.
    await a.waitForFunction(()=>/2\s+of 54/.test(document.querySelector('.course-user-progress').innerText));
    assert.equal(await a.locator('select[aria-label^="Choose a lesson"]').inputValue(),'llms');
    await a.locator('.lesson-navigation button').last().click();
    assert((await progress(a)).completed.includes('llms'),'Complete credits the visible lesson, not the other tab’s lesson');
    await a.evaluate(()=>localStorage.setItem('final-exam',JSON.stringify({bestScore:88})));
    await navigate(b,'tokens');
    // Reconciliation must use the latest final score even before a storage event.
    await b.reload(); await b.waitForSelector('#main-content');
    assert((await progress(b)).completed.includes('whatyoulearned'));
    await a.evaluate(()=>{localStorage.removeItem('final-exam');localStorage.removeItem('llm-explorer-progress');});
    await navigate(b,'openerskills');
    assert.deepEqual((await progress(b)).completed,[],'An older tab cannot resurrect reset credit');
    await c.close();
    console.log('PASS: stale tabs preserve new progress, normal tabs synchronize, and reset stays reset');

    // Missing downloads and missing individual entries stay local to activities.
    c = await context(); let block = true;
    await c.route('**/group-activities-data.js*',r=>block?r.abort():r.continue());
    p = await open(c); const errors=[]; p.on('pageerror',e=>errors.push(e.message));
    const discussionIds = await p.evaluate(()=>SECTIONS.filter(s=>SECTION_COMPONENTS[s.id].toString().includes('activityId:')).map(s=>s.id));
    for (const id of [...discussionIds,'forgroups']) {
      await navigate(p,id);
      assert.equal(await p.getByText('This lesson hit a snag.',{exact:true}).count(),0,id);
      assert.equal(await p.locator('#course-runtime-error').count(),0,id);
    }
    await navigate(p,'critical');
    assert.equal(await p.locator('.activities-unavailable').count(),1);
    await p.locator('#critical-discussion > summary').click();
    if(process.env.REVIEW_SCREENSHOTS) await p.screenshot({path:process.env.REVIEW_SCREENSHOTS+'/course-retry-'+engine.name()+'.png'});
    await p.getByRole('button',{name:'Try loading activities again'}).click();
    await p.getByRole('button',{name:'Try loading activities again'}).waitFor();
    assert.equal(await p.locator('.activities-unavailable').count(),1,'Failed retry stays recoverable');
    const before = await progress(p); block = false;
    await p.getByRole('button',{name:'Try loading activities again'}).click();
    await p.locator('.discussion-questions li').first().waitFor();
    assert.equal(await p.locator('.activities-unavailable').count(),0);
    assert.deepEqual(await progress(p),before,'Retry leaves lesson progress alone');
    await p.evaluate(()=>{window.COURSE_GROUP_ACTIVITIES=window.COURSE_GROUP_ACTIVITIES.filter(a=>a.id!=='critical-discussion');});
    await navigate(p,'welcome'); await navigate(p,'critical');
    assert.equal(await p.locator('.activities-unavailable').count(),1,'Missing entry also gets retry');
    await p.locator('#critical-discussion > summary').click();
    if(process.env.REVIEW_SCREENSHOTS) await p.screenshot({path:process.env.REVIEW_SCREENSHOTS+'/course-retry-'+engine.name()+'.png'});
    await p.getByRole('button',{name:'Try loading activities again'}).click();
    await p.locator('.discussion-questions li').first().waitFor();
    assert.deepEqual(errors,[]);
    block = true;
    await p.goto(base+'/group-exercises/group-session.html?id=critical-discussion');
    await p.getByRole('button',{name:'Reload activities'}).waitFor();
    block = false;
    await p.getByRole('button',{name:'Reload activities'}).click();
    await p.locator('.discussion-questions li').first().waitFor();
    assert.deepEqual(errors,[]);
    await c.close();
    console.log('PASS: missing activity data cannot break lessons or the directory; retries restore questions');
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
