// Merged lesson: preserve earned progress, both concepts, and the shared activities.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const http = require('node:http');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || '/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const migrate = vm.runInNewContext(html.slice(html.indexOf('function reconcileCourseProgress('), html.indexOf('const FINAL_BADGES')) + '\nreconcileCourseProgress', {isOptionalLesson: id => ['reviews','resources','forgroups'].includes(id)});
const plain = value => JSON.parse(JSON.stringify(value));
const saved = {activeSection:'engagementtrap', visited:['mindtrap','flattery','engagementtrap'], completed:['flattery','engagementtrap','reviews','whatyoulearned'], testYourselfQuiz:{saved:true}};
const original = plain(saved);
const migrated = migrate(saved, false);
assert.deepEqual(plain(migrated), {...saved, activeSection:'flattery', visited:['mindtrap','flattery'], completed:['flattery']});
assert.deepEqual(saved,original);
assert.equal(migrate(migrated,false),migrated);
assert.deepEqual(plain(migrate({completed:['engagementtrap']},true).completed),['flattery','whatyoulearned']);
const server = http.createServer((req,res) => {
  const file = path.resolve(root, '.' + new URL(req.url,'http://localhost').pathname);
  if (!file.startsWith(root+path.sep)) {res.writeHead(404);return res.end();}
  fs.readFile(file,(err,data) => {
    if (err) {res.writeHead(404);return res.end();}
    res.setHeader('Content-Type', {'.html':'text/html','.js':'application/javascript','.jpg':'image/jpeg','.css':'text/css'}[path.extname(file)] || 'application/octet-stream');
    res.end(data);
  });
});
(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  let browser;
  const errors=[];
  try {
    browser=await chromium.launch({channel:'chrome',headless:true});
    const page=await browser.newPage({viewport:{width:1280,height:900},reducedMotion:'reduce'});
    page.on('pageerror',error=>errors.push(error.message));
    await page.route(/script\.google|script\.googleusercontent|\.mp4/,r=>r.abort());
    await page.addInitScript(saved=>{
      if(localStorage.getItem('merge-test'))return;
      localStorage.setItem('merge-test','1');
      localStorage.setItem('llm-user-name','Preview');
      localStorage.setItem('llm-explorer-progress',JSON.stringify(saved));
    },saved);
    const url=`http://127.0.0.1:${server.address().port}/index.html`;
    await page.goto(url,{waitUntil:'domcontentloaded'});
    await page.getByRole('heading',{name:'Flattery & Engagement',exact:true}).waitFor();
    await page.waitForFunction(()=>JSON.parse(localStorage.getItem('llm-explorer-progress')).activeSection==='flattery');
    assert.deepEqual(await page.evaluate(()=>window.validate()),{errors:[],warnings:[],sectionCount:57});
    assert.equal(await page.getByRole('button',{name:'Watch the video overview for this lesson'}).count(),0);
    assert.equal(await page.getByRole('button',{name:/^Mark step \d complete$/}).count(),5);
    assert.equal(await page.locator('img[src*="flattery-trap-"]').count(),5);
    assert.equal(await page.locator('img[src*="engagement-trap-"]').count(),1);
    for (const text of ['The Flattery Trap is treating AI’s approval as honest evaluation.','The Engagement Trap is spending time you never decided to spend.','So when do you close it?']) {
      assert.ok(await page.getByText(text,{exact:true}).isVisible());
    }
    assert.equal(await page.getByText('Where Does Your Time Go?',{exact:true}).count(),0);
    for(let i=1;i<=5;i++) await page.getByRole('button',{name:`Mark step ${i} complete`,exact:true}).click();
    assert.equal(await page.getByRole('button',{name:/^Mark step \d incomplete$/}).count(),5);
    await page.getByRole('button',{name:'When the AI stops offering follow-ups.',exact:true}).click();
    await page.getByText('Did the chat stop when the original question was answered?',{exact:true}).waitFor();
    await page.getByRole('button',{name:'After 30 minutes, no matter what.',exact:true}).click();
    await page.getByText('Sometimes two minutes is right. Sometimes an hour is. What’s the real test?',{exact:true}).waitFor();
    await page.getByRole('button',{name:'When you got what you came for.',exact:true}).click();
    await page.getByText('You came with a question. You have the answer. Everything offered after that is a new choice. Say yes only if you actually want it.',{exact:true}).waitFor();
    if(process.env.MERGE_QA_DIR){
      fs.mkdirSync(process.env.MERGE_QA_DIR,{recursive:true});
      await page.getByRole('heading',{name:'Flattery & Engagement',exact:true}).scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(process.env.MERGE_QA_DIR,'desktop.png')});
      await page.getByText('When Useful Help Keeps Going',{exact:true}).scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(process.env.MERGE_QA_DIR,'desktop-seam.png')});
    }
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(()=>document.fonts.ready);
    await page.waitForFunction(()=>document.documentElement.scrollWidth<=window.innerWidth,{},{timeout:3000}).catch(async error=>{console.log(await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,overflow:[...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(-20).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,80),right:e.getBoundingClientRect().right}))})));throw error;});
    if(process.env.MERGE_QA_DIR) {
      await page.getByRole('heading',{name:'Flattery & Engagement',exact:true}).scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(process.env.MERGE_QA_DIR,'mobile.png')});
      await page.getByText('So when do you close it?',{exact:true}).scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(process.env.MERGE_QA_DIR,'mobile-question.png')});
    }
    await page.getByRole('button',{name:/Next up: Support Trap/}).click();
    await page.getByRole('heading',{name:'Support Trap',exact:true}).waitFor();
    await page.goto(url+'?print=lesson:engagementtrap',{waitUntil:'domcontentloaded'});
    await page.getByRole('heading',{name:'Flattery & Engagement',exact:true}).waitFor();
    await page.goto(url+'?print=avoid-traps',{waitUntil:'domcontentloaded'});
    await page.getByRole('heading',{name:'Flattery & Engagement',exact:true}).waitFor();
    assert.equal(await page.getByRole('heading',{name:'Engagement Trap',exact:true}).count(),0);
    assert.deepEqual(errors,[]);
    console.log('PASS: progress migration, structure, five lab steps, all stopping choices, mobile layout, next navigation, and legacy/group print routes.');
  } finally {if(browser)await browser.close();server.closeAllConnections();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);process.exitCode=1;});
