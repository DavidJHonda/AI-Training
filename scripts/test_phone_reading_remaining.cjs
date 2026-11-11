// Remaining phone boards. Requires the same Playwright NODE_PATH as other browser tests.
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.BASE_URL||'http://127.0.0.1:8796';
const lessons={
  "llms": [
    "what-is-ai-ask-the-desk",
    "what-is-ai-types",
    "why-learn-ai-everyday"
  ],
  "doesaithink": [
    "does-ai-think-chinese-room",
    "hallucination-glue-on-pizza",
    "does-ai-think-side-by-side"
  ],
  "whatitdoesbest": [
    "where-ai-works-best-built-this-course",
    "where-ai-works-best-strengths-1",
    "where-ai-works-best-strengths-2"
  ],
  "openerprotect": [
    "avoid-traps-opener-read-the-water",
    "avoid-traps-opener-section-map"
  ],
  "peopleskills": [
    "people-skills-why-people-matter",
    "people-skills-matter-more",
    "people-skills-four-ways"
  ],
  "openerfinish": [
    "five-big-ideas"
  ],
  "whydeeper": [
    "why-learn-ai-press",
    "why-learn-ai-thrive"
  ],
  "whybother": [
    "does-school-matter-product-launch",
    "what-school-helps-you-build"
  ],
  "modelselection": [
    "your-home-base-big-three",
    "your-home-base-home-base"
  ],
  "openerrealworld": [
    "navigate-the-future-opener-section-map"
  ],
  "creativethinking": [
    "creative-thinking-creative-professions",
    "creative-thinking-practice-creativity"
  ],
  "aivscode": [
    "ai-is-different-rules",
    "ai-is-different-cooking-analogy",
    "ai-is-different-playlist-formats"
  ],
  "studying": [
    "learn-with-ai-study-toolkit",
    "learn-with-ai-how-it-works",
    "learn-with-ai-four-moves"
  ],
  "choosemodel": [
    "when-you-need-more-choose-tool",
    "when-you-need-more-thinking",
    "when-you-need-more-research"
  ],
  "openerskills": [
    "build-your-skills-opener-section-map"
  ],
  "becurious": [
    "curiosity-stay-curious",
    "curiosity-ai-habits"
  ],
  "aihistory": [
    "whats-an-llm-llm",
    "whats-an-llm-patterns",
    "whats-an-llm-one-word-at-a-time"
  ],
  "openerworkwith": [
    "work-with-ai-opener-same-tool",
    "work-with-ai-opener-section-map"
  ],
  "openerfoundations": [
    "understand-ai-opener-under-hood",
    "understand-ai-opener-section-map"
  ],
  "wherestheline": [
    "wheres-the-line-two-uses",
    "wheres-the-line-responsible-choice"
  ],
  "makeyourmove": [
    "whats-next-careers",
    "whats-next-actions"
  ]
};
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true}),records=[];
 try {
  for(const id of [...Object.keys(lessons),'prediction']) {
   const context=await browser.newContext({viewport:{width:390,height:850},hasTouch:true,reducedMotion:'reduce'});
   await context.route(/script\.google|script\.googleusercontent|\.mp4/,r=>r.abort());
   await context.addInitScript(id=>{localStorage.clear();localStorage.setItem('llm-user-name','Phone Review');localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:id,visited:[id],completed:[]}));},id);
   const page=await context.newPage(),errors=[];
   page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error'&&!m.text().includes('ERR_FAILED'))errors.push(m.text())});
   await page.goto(base+'/index.html',{waitUntil:'networkidle'});
   const toggle=page.locator('.lesson-reading-toggle');
   if(await toggle.count()) {
    assert.equal(await toggle.getAttribute('aria-expanded'),'false');
    assert.equal(await page.locator('.phone-reading-mobile:visible,.answer-lesson-board-mobile:visible').count(),0);
    await toggle.click();
   }
   await page.evaluate(async()=>{await document.fonts.ready;for(const image of document.images){image.loading='eager';await image.decode().catch(()=>{});}});
   const selector=id==='prediction'?'.answer-lesson-board-mobile':'.phone-remaining-board';
   const desktop=id==='prediction'?'.answer-lesson-board-desktop':'.phone-reading-board > .phone-reading-desktop img';
   const count=id==='prediction'?2:lessons[id].length;
   if(id!=='prediction')assert.deepEqual(await page.locator('[data-phone-reading-board]').evaluateAll(ns=>ns.map(n=>n.dataset.phoneReadingBoard)),lessons[id]);
   for(const [width,height] of [[320,850],[390,850],[430,850],[760,850],[761,850],[844,390],[1024,1000],[1280,1000],[1440,1000]]) {
    await page.setViewportSize({width,height});await page.waitForTimeout(200);
    const mobile=width<=760||height<=500;
    assert.equal(await page.locator(selector+':visible').count(),mobile?count:0,id+' '+width);
    assert.equal(await page.locator(desktop+':visible').count(),mobile?0:count,id+' desktop branch '+width);
    if(!mobile&&id!=='prediction')assert.equal(await page.locator(selector+' svg').count(),0,'Phone art stays unmounted on desktop');
    if(mobile){
     const data=await page.locator(selector).evaluateAll(ns=>ns.map(n=>{const r=n.getBoundingClientRect();return {title:n.querySelector('h3').textContent,text:n.innerText,x:r.x,width:r.width,tiny:[...n.querySelectorAll('p,li,h4,dt,dd,th,td,blockquote')].filter(e=>parseFloat(getComputedStyle(e).fontSize)<(e.tagName==='H4'?19:16)&&!e.classList.contains('answer-board-prompt')).map(e=>e.textContent),overflow:[...n.querySelectorAll('*')].filter(e=>!(e instanceof SVGElement)&&!e.matches('.phone-remaining-sheet-scroll')&&e.clientWidth&&e.scrollWidth>e.clientWidth+1).map(e=>e.textContent)}}));
     const snapshot=await page.locator('#main-content').ariaSnapshot();
     for(const b of data){assert.deepEqual(b.tiny,[],id);assert.deepEqual(b.overflow,[],id);assert.ok(b.x>=0&&b.x+b.width<=width,id);assert.equal(snapshot.split('\n').filter(line=>line.includes('heading "'+b.title+'" [level=3]')).length,1,id+' heading announced once');}
     assert.equal(await page.locator('.phone-reading-desktop-source:visible').count(),0);
     records.push({id,width,height,boards:data,scrollWidth:await page.evaluate(()=>document.documentElement.scrollWidth)});
    }
   }
   await page.setViewportSize({width:390,height:850});await page.waitForTimeout(200);
   const board=stem=>page.locator('[data-phone-reading-board="'+stem+'"] .phone-reading-mobile');
   if(id==='llms'){const desk=board('what-is-ai-ask-the-desk');assert.equal(await desk.locator('ol li').count(),0);assert.ok(!(await desk.innerText()).includes('10 History Project Ideas'));assert.deepEqual(await desk.locator('.phone-reading-copy > p').allTextContents(),['Give me 10 ideas for my history project.','Give me 10 ideas for my history project.']);}
   if(id==='aivscode') {
    const rules=board('ai-is-different-rules');assert.equal(await rules.locator('.phone-remaining-condition').count(),2);assert.deepEqual(await rules.locator('.phone-remaining-outcomes h4').allTextContents(),['THEN','ELSE']);assert.equal(await rules.locator('.phone-remaining-outcomes .phone-remaining-arrow').count(),0,'Alternative outcomes are not a sequential process');
    for(const text of ['Password doesn’t match. Please try again.','Written rules return the same result every time.'])assert.ok((await rules.innerText()).includes(text));
    const lastBranch=rules.locator('.phone-remaining-outcomes > section').last();assert.ok(await lastBranch.evaluate(n=>{const line=getComputedStyle(n,'::after'),heading=n.querySelector('h4').getBoundingClientRect(),body=n.querySelector('p').getBoundingClientRect(),end=n.getBoundingClientRect().top+parseFloat(line.top)+parseFloat(line.height);return Math.abs(end-(heading.top+heading.height/2))<0.5&&end<body.top;}),'Branch spine ends at the ELSE heading, above its explanation');
    const playlist=board('ai-is-different-playlist-formats');assert.deepEqual(await playlist.locator('th').allTextContents(),['Song','Artist','Play Order']);assert.deepEqual(await playlist.locator('td').allTextContents(),['Blinding Lights','The Weeknd','1','Levitating','Dua Lipa','2','As It Was','Harry Styles','3']);const sheet=playlist.getByRole('region',{name:'Structured playlist spreadsheet'});await sheet.focus();await page.keyboard.press('ArrowRight');await page.waitForTimeout(200);assert.ok(await sheet.evaluate(n=>n.scrollLeft>0),'Spreadsheet scrolls with the keyboard');assert.ok(await sheet.evaluate(n=>{n.scrollLeft=n.scrollWidth;return n.scrollLeft+n.clientWidth>=n.scrollWidth-1;}),'Last column is reachable');await sheet.evaluate(n=>n.scrollLeft=0);assert.equal(await playlist.locator('del').innerText(),'Shake It Off');for(const text of ['Homecoming mix','start here!','play this last!'])assert.ok((await playlist.innerText()).includes(text));
   }
   if(id==='aihistory'){const flow=board('whats-an-llm-one-word-at-a-time');assert.deepEqual(await flow.locator('.phone-remaining-prediction strong').allTextContents(),['jelly','for','lunch']);assert.equal(await flow.locator('.phone-remaining-arrow').count(),2);assert.deepEqual(await flow.locator('.phone-remaining-context').allTextContents(),['I want to buy peanut butter and','I want to buy peanut butter and jelly','I want to buy peanut butter and jelly for']);}
   if(id==='doesaithink') {
    const chinese=board('does-ai-think-chinese-room');for(const text of ['They look up the whole phrase on a giant chart.','中文句子 → 回覆對照表','如果你看到：','請回覆：','你好嗎？','我很好，謝謝！','RULES ONLY','To anyone outside, it looks like fluent Chinese conversation.','(How are you?)','(I’m fine, thank you!)'])assert.ok((await chinese.innerText()).includes(text),text);
    assert.equal(await chinese.locator('.phone-remaining-chart [lang="zh-Hant"]').count(),5);assert.equal(await chinese.locator('.phone-reading-number').count(),3);assert.deepEqual(await chinese.locator('.phone-reading-number').evaluateAll(ns=>ns.map(n=>getComputedStyle(n).backgroundColor)),['rgb(79, 47, 196)','rgb(79, 47, 196)','rgb(79, 47, 196)']);
    assert.deepEqual(await board('does-ai-think-side-by-side').locator('dt').allTextContents(),['When You Think','What AI Does','When You Think','What AI Does','When You Think','What AI Does']);
   }
   if(id==='whybother')assert.deepEqual(await board('does-school-matter-product-launch').locator('dt').allTextContents(),['Your Coworker','You','Your Coworker','You','Your Coworker','You']);
   if(id==='studying')assert.ok((await board('learn-with-ai-four-moves').innerText()).includes('Generate a 10-question quiz from these sources only. Don’t show the answers yet. Wait for mine, then grade me.'));
   if(id==='whatitdoesbest')for(const [stem,text] of [['where-ai-works-best-strengths-1','Turn a voice memo into a to-do list.'],['where-ai-works-best-strengths-2','Figure out why your science experiment gave unexpected results.']])assert.ok((await board(stem).innerText()).includes(text));
   if(id.startsWith('opener')&&id!=='openerfinish')assert.equal(await page.locator('.phone-remaining-board > .phone-reading-stack > li').count(),3);
   if(id==='choosemodel')for(const text of ['only two people know how to edit video.','Texas A&M in College Station versus UT Austin?','undergraduate research opportunities, admissions requirements, and costs. Show your sources.'])assert.ok((await page.locator('#main-content').innerText()).includes(text));
   if(id==='wherestheline')for(const text of ['DraftKings put the technology into use and continued developing it.','DraftKings chose not to put this predictive technology into use.','DraftKings disputes targeting customers based on losses.'])assert.ok((await page.locator('#main-content').innerText()).includes(text));
   if(id==='openerfinish') {
    const poster=board('five-big-ideas');assert.equal(await poster.locator('li[aria-label="word, selected"] strong').innerText(),'word');assert.deepEqual(await poster.locator('h4').allTextContents(),['1AI predicts. It doesn’t think.','2Fluent isn’t the same as true.','3The more you know, the more it gives.','4You make the call.','5The better AI gets, the more you matter.']);
    for(const text of ['20% off a $60 hoodie.','$52.','$48','Now you’re smarter than the tool.'])assert.ok((await poster.innerText()).includes(text));
    for(const name of ['Save image','Download PDF']){const link=page.getByRole('link',{name,exact:true});assert.equal(await link.count(),1);assert.ok((await link.getAttribute('href')).includes('five-big-ideas'));}
   }
   // Verify the complete lesson remains operable around the reflowed boards.
   const field=page.locator('#main-content textarea:visible,#main-content input[type="text"]:visible').first();
   if(await field.count()){const old=await field.inputValue();await field.fill('Phone readability check');assert.equal(await field.inputValue(),'Phone readability check');await field.fill(old);}
   if(await toggle.count()){await toggle.click();assert.equal(await page.locator(selector+':visible').count(),0);await toggle.click();assert.equal(await page.locator(selector+':visible').count(),count);}
   const next=page.getByRole('button',{name:/Mark as complete|Next Lesson/}).last();assert.equal(await next.count(),1,id+' next lesson remains reachable');
   await page.emulateMedia({media:'print'});assert.equal(await page.locator(selector+':visible').count(),0);assert.equal(await page.locator(desktop+':visible').count(),count);
   await page.emulateMedia({media:'screen'});await next.click();await page.waitForFunction(id=>JSON.parse(localStorage.getItem('llm-explorer-progress')).activeSection!==id,id);assert.deepEqual(errors,[],id);await context.close();console.log('PASS',id,count,'boards');
  }
  // A short fine-pointer desktop window must keep the desktop representation.
  const ctx=await browser.newContext({viewport:{width:844,height:390},hasTouch:false});await ctx.route(/script\.google|script\.googleusercontent|\.mp4/,r=>r.abort());await ctx.addInitScript(()=>{localStorage.clear();localStorage.setItem('llm-user-name','Phone Review');localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'prediction',visited:['prediction'],completed:[]}));});const p=await ctx.newPage();await p.goto(base+'/index.html',{waitUntil:'networkidle'});await p.locator('.lesson-reading-toggle').click();assert.equal(await p.locator('.answer-lesson-board-desktop:visible').count(),2);await ctx.close();
  if(process.env.PHONE_REMAINING_OUTPUT){fs.mkdirSync(process.env.PHONE_REMAINING_OUTPUT,{recursive:true});fs.writeFileSync(path.join(process.env.PHONE_REMAINING_OUTPUT,'phone-checks.json'),JSON.stringify(records,null,2));}
  console.log('PASS: 47 adapted boards, two reference boards, 22 pages, phone widths, coarse landscape, breakpoints, visible accessible representations, exact examples and relationships, reading toggles, input fields, navigation and print.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
