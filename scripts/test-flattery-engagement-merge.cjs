// Flattery lesson: preserve earned progress and all five exercise steps after removing Engagement.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const http = require('node:http');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || '/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.join(__dirname, '..');
const indexFile = process.env.COURSE_INDEX_FILE || path.join(root, 'index.html');
const html = fs.readFileSync(indexFile, 'utf8');
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
  fs.readFile(file === path.join(root,'index.html') ? indexFile : file,(err,data) => {
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
    await page.getByRole('heading',{name:'Flattery Trap',level:1,exact:true}).waitFor();
    await page.waitForFunction(()=>JSON.parse(localStorage.getItem('llm-explorer-progress')).activeSection==='flattery');
    assert.deepEqual(await page.evaluate(()=>window.validate()),{errors:[],warnings:[],sectionCount:57});
    assert.equal(await page.locator('video source').getAttribute('src'),'course-assets/flattery-trap/flattery-trap.mp4?v=20261113ship21');
    await page.getByRole('button',{name:'Read the lesson',exact:true}).click();
    assert.equal(await page.getByRole('button',{name:/^Mark step \d complete$/}).count(),5);
    const lessonImages = page.locator('img[src*="course-assets/flattery-trap/"]');
    assert.equal(await lessonImages.count(),5);
    await page.waitForFunction(() => [...document.querySelectorAll('img[src*="course-assets/flattery-trap/"]')].every(img => img.complete && img.naturalWidth > 0));
    for (const text of ['The Flattery Trap is treating AI’s approval as honest evaluation.','OpenAI now tests ChatGPT for sycophancy. But you’ll still see it.']) {
      assert.ok(await page.getByText(text,{exact:true}).isVisible());
    }
    assert.equal(await page.getByText('Where Does Your Time Go?',{exact:true}).count(),0);
    for(let i=1;i<=5;i++) await page.getByRole('button',{name:`Mark step ${i} complete`,exact:true}).click();
    assert.equal(await page.getByRole('button',{name:/^Mark step \d incomplete$/}).count(),5);
    assert.equal(await page.getByText('So when do you close it?',{exact:true}).count(),0);
    assert.equal(await page.getByText('When Useful Help Keeps Going',{exact:true}).count(),0);
    if(process.env.MERGE_QA_DIR){
      fs.mkdirSync(process.env.MERGE_QA_DIR,{recursive:true});
      await page.getByRole('heading',{name:'Flattery Trap',level:1,exact:true}).scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(process.env.MERGE_QA_DIR,'desktop.png')});
      await page.getByText('Make Feedback Useful',{exact:true}).scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(process.env.MERGE_QA_DIR,'desktop-seam.png')});
    }
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(()=>document.fonts.ready);
    await page.waitForFunction(()=>document.documentElement.scrollWidth<=window.innerWidth,{},{timeout:3000}).catch(async error=>{console.log(await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,overflow:[...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(-20).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,80),right:e.getBoundingClientRect().right}))})));throw error;});
    if(process.env.MERGE_QA_DIR) {
      await page.getByRole('heading',{name:'Flattery Trap',level:1,exact:true}).scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(process.env.MERGE_QA_DIR,'mobile.png')});
      await page.getByText('OpenAI now tests ChatGPT for sycophancy. But you’ll still see it.',{exact:true}).scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(process.env.MERGE_QA_DIR,'mobile-question.png')});
    }
    await page.getByRole('button',{name:/Next up: Support Trap/}).click();
    await page.getByRole('heading',{name:'Support Trap',exact:true}).waitFor();
    await page.goto(url+'?print=lesson:engagementtrap',{waitUntil:'domcontentloaded'});
    await page.getByRole('heading',{name:'Flattery Trap',level:1,exact:true}).waitFor();
    await page.goto(url+'?print=avoid-traps',{waitUntil:'domcontentloaded'});
    await page.getByRole('heading',{name:'Flattery Trap',level:1,exact:true}).waitFor();
    assert.equal(await page.getByRole('heading',{name:'Engagement Trap',exact:true}).count(),0);
    assert.deepEqual(errors,[]);
    console.log('PASS: progress migration, structure, five lab steps, Engagement removal, mobile layout, next navigation, and legacy/group print routes.');
  } finally {if(browser)await browser.close();server.closeAllConnections();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);process.exitCode=1;});
