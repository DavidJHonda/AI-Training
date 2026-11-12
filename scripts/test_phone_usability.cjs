// Run against scripts/serve-site.py with the same Playwright NODE_PATH as the other phone tests.
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const base = process.env.BASE_URL || 'http://127.0.0.1:8878';
const output = process.env.PHONE_USABILITY_OUTPUT;
const dependencies = process.env.PHONE_USABILITY_DEPENDENCIES;
const results = [];

async function openContext(browser, width, height, touch) {
  const context = await browser.newContext({viewport:{width,height},hasTouch:touch,reducedMotion:'reduce'});
  context.posts = [];
  await context.addInitScript(() => {
    if (!localStorage.getItem('phone-usability-test')) {
      localStorage.clear(); sessionStorage.clear();
      localStorage.setItem('phone-usability-test','1');
      localStorage.setItem('llm-user-name','Phone Review');
      localStorage.setItem('llm-student-id','phone-usability-test');
      localStorage.setItem('llm-student-profile',JSON.stringify({firstName:'Phone Review',country:'United States',studentId:'phone-usability-test'}));
      localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'llms',visited:['llms'],completed:[]}));
    }
    window.copiedPhonePrompts = [];
    Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>window.copiedPhonePrompts.push(text)}});
  });
  await context.route('**/*', route => {
    const request = route.request(), url = new URL(request.url());
    if (dependencies) {
      const dependency = JSON.parse(fs.readFileSync(path.join(dependencies,'manifest.json')))[url.href];
      if (dependency) return route.fulfill({status:200,contentType:'application/javascript',body:fs.readFileSync(path.join(dependencies,dependency.file))});
    }
    if (!['GET','HEAD'].includes(request.method())) {
      const payload = JSON.parse(request.postData() || '{}'); context.posts.push(payload);
      return route.fulfill({status:200,contentType:'text/plain',body:payload.eventType==='review'?(context.failReviews?'test-error':'review-ok'):'ok'});
    }
    if (/script\.google|script\.googleusercontent/.test(url.hostname)) return route.fulfill({status:200,contentType:'application/json',body:'{"reviews":[],"ratingSummary":{"total":0,"average":null}}'});
    if (/\.mp4$/.test(url.pathname)) return route.abort();
    // Check app handoffs without loading accounts or sending anything to an external service.
    if (request.isNavigationRequest() && url.origin!==new URL(base).origin) return route.fulfill({status:200,contentType:'text/html',body:'<title>App handoff check</title>'});
    return route.continue();
  });
  return context;
}

async function navigate(page, group, lesson) {
  const selects = page.locator('.mobile-course-nav select');
  const value = await selects.first().locator('option').evaluateAll((options,label)=>options.find(o=>o.textContent.includes(label)).value,group);
  await selects.first().selectOption(value);
  await selects.nth(1).selectOption(lesson);
  await page.waitForFunction(id=>JSON.parse(localStorage.getItem('llm-explorer-progress')).activeSection===id,lesson);
}

async function fits(page) {
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'The complete page must fit without sideways scrolling');
}

(async () => {
  const browser = await chromium.launch({channel:'chrome',headless:true});
  try {
    for (const [width,height] of [[320,850],[390,850],[430,850],[844,390]]) {
      const context = await openContext(browser,width,height,true), page = await context.newPage(), errors = [];
      page.on('pageerror',error=>errors.push(error.message));
      await page.goto(base+'/course',{waitUntil:'networkidle'});
      await page.locator('.lab-step-row').first().waitFor();
      assert.equal(await page.locator('.desktop-section-map:visible,.desktop-lesson-nav:visible').count(),0);
      assert.equal(await page.locator('.mobile-course-nav:visible').count(),1);
      assert.equal(await page.locator('.sticky-lesson-bar').isVisible(),false,'The offscreen phone bar stays out of focus and accessibility navigation');
      assert.equal(await page.getByRole('button',{name:/^Previous lesson/}).count(),1);
      const navigation = await page.locator('.mobile-course-nav').ariaSnapshot();
      assert.equal(navigation.split('\n').filter(line=>line.includes('combobox')).length,2);
      const sizes = await page.locator('.lab-step-row').first().evaluate(row=>({
        body:parseFloat(getComputedStyle(row.querySelector(':scope > div > span:nth-child(2)')).fontSize),
        title:parseFloat(getComputedStyle(row.querySelector(':scope > div > :first-child')).fontSize),
        toggle:row.querySelector('button').getBoundingClientRect().toJSON()
      }));
      assert.ok(sizes.body>=16 && sizes.title>=20 && sizes.toggle.width>=44 && sizes.toggle.height>=44);
      const toggle = page.locator('.lab-step-row > button').first();
      await toggle.click(); assert.equal(await toggle.getAttribute('aria-pressed'),'true');
      const prompt = page.locator('.lab-prompt').first(), text = await prompt.locator('.lab-prompt-text').innerText();
      assert.ok(await prompt.locator('.lab-prompt-text').evaluate(n=>parseFloat(getComputedStyle(n).fontSize)>=16));
      await prompt.getByRole('button',{name:'Copy Prompt',exact:true}).click();
      assert.equal(await page.evaluate(()=>window.copiedPhonePrompts.at(-1)),text);
      await page.reload({waitUntil:'networkidle'});
      assert.equal(await page.locator('.lab-step-row > button').first().getAttribute('aria-pressed'),'true','Checklist state survives reload');
      const saved = await page.evaluate(()=>localStorage.getItem('llm-explorer-progress'));
      const popupPromise = page.waitForEvent('popup');
      await page.locator('.lab-action-button[href="https://chatgpt.com"]').first().click();
      const app = await popupPromise; await app.waitForLoadState(); assert.ok(app.url().startsWith('https://chatgpt.com')); await app.close();
      assert.equal(await page.evaluate(()=>localStorage.getItem('llm-explorer-progress')),saved,'Opening an app preserves the course position');
      await fits(page);
      if (width<=600) {
        const cards = await page.locator('.lesson-navigation > button').evaluateAll(xs=>xs.map(n=>n.getBoundingClientRect().toJSON()));
        assert.ok(cards.length===2 && cards[0].x===cards[1].x && cards[1].y>=cards[0].y+cards[0].height);
      }
      await page.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));
      await page.waitForFunction(()=>document.querySelector('.sticky-lesson-bar').getBoundingClientRect().top>=0);
      assert.ok(await page.locator('.sticky-lesson-bar button').evaluateAll(xs=>xs.every(n=>n.getBoundingClientRect().width>=44&&n.getBoundingClientRect().height>=44)));
      await navigate(page,'Understand AI','tokens');
      const options = page.locator('.interactive-box .scenario-row-body').first();
      await options.locator('button').first().click(); await options.locator('button').last().click();
      assert.ok(await page.locator('.activity-scenario .feedback-grid:visible').count()>0); await fits(page);
      await navigate(page,'Finish Smarter','whatyoulearned');
      await page.getByRole('button',{name:'Start the Final',exact:true}).click();
      const first = page.locator('[role=radiogroup]').first(); await first.locator('[role=radio]').first().click();
      const attempt = await page.evaluate(()=>JSON.parse(localStorage.getItem('final-exam-unfinished:v1')));
      await page.reload({waitUntil:'networkidle'}); await page.getByRole('button',{name:'Continue the Final',exact:true}).click();
      assert.deepEqual(await page.evaluate(()=>JSON.parse(localStorage.getItem('final-exam-unfinished:v1')).answers),attempt.answers);
      await page.getByRole('button',{name:'Submit the Final',exact:true}).click();
      await page.getByRole('button',{name:'Keep answering',exact:true}).click();
      await page.waitForFunction(()=>!!document.activeElement.closest('[id^="final-question-"]'));
      const bank = await page.evaluate(()=>FINAL_BANK.map(q=>({id:q.id,correct:q.correct})));
      for (const question of bank) await page.locator('#final-question-'+question.id+' [role=radio]').nth(question.correct).click();
      await page.getByRole('button',{name:'Submit the Final',exact:true}).click();
      await page.getByRole('textbox',{name:'First name on the certificate'}).fill('Alexandra');
      await page.getByRole('textbox',{name:'Last name on the certificate'}).fill('Montgomery-Washington');
      await page.getByRole('button',{name:'Make my certificate',exact:true}).click();
      const certificate = page.locator('.certificate-block .certificate-doc'); await certificate.waitFor();
      const sections = await certificate.locator(':scope > div').evaluateAll(xs=>xs.map(n=>n.getBoundingClientRect().toJSON()));
      assert.ok(sections[1].y>=sections[0].y+sections[0].height-1 && sections[2].y>=sections[1].y+sections[1].height-1,'Certificate sections do not overlap');
      assert.ok(await certificate.locator('.certificate-caption,.certificate-date,.certificate-site').evaluateAll(xs=>xs.every(n=>parseFloat(getComputedStyle(n).fontSize)>=16)));
      assert.equal((await certificate.ariaSnapshot()).split('Alexandra Montgomery-Washington').length-1,1);
      const record = await page.evaluate(()=>JSON.parse(localStorage.getItem('final-exam')));
      const printPromise = page.waitForEvent('popup'); await page.getByRole('button',{name:'Print or save as PDF',exact:true}).click();
      const print = await printPromise; await print.locator('.certificate-doc').waitFor(); assert.ok(await print.locator('.certificate-student-name').innerText()==='Alexandra Montgomery-Washington'); await fits(print); await print.close();
      await page.getByRole('button',{name:'Take it again',exact:true}).first().click();
      await page.getByRole('button',{name:'Submit the Final',exact:true}).click(); await page.getByRole('button',{name:'Submit anyway',exact:true}).click();
      assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('final-exam')).bestScore),100);
      assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('final-exam')).completionDate),record.completionDate);
      assert.equal(await certificate.count(),1,'A weaker retry retains the earned certificate'); await fits(page);
      if (width===390) {
        await navigate(page,'Start Smarter','aivscode');
        const downloadPromise = page.waitForEvent('download'); await page.getByRole('button',{name:'Download Notes',exact:true}).click();
        const download = await downloadPromise, bytes = fs.readFileSync(await download.path());
        const expected = fs.readFileSync(path.join(__dirname,'../packets/ai-replaces-school-notes.png'));
        assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),crypto.createHash('sha256').update(expected).digest('hex'));
        await navigate(page,'Finish Smarter','reviews');
        await page.getByRole('radio',{name:'4 out of 5',exact:true}).click(); context.failReviews=true;
        await page.getByRole('button',{name:'Submit my rating',exact:true}).click(); await page.locator('.course-review-form [role=alert]').waitFor();
        context.failReviews=false; await page.getByRole('button',{name:'Try again',exact:true}).click(); await page.getByRole('button',{name:'Edit my review',exact:true}).waitFor(); await fits(page);
      }
      assert.deepEqual(errors,[]); results.push({width,height,overflow:'none',certificate:'no overlap',savedProgress:'preserved',externalSubmissions:0,interceptedPosts:context.posts.length});
      await context.close(); console.log('PASS phone usability',width,height);
    }
    // Larger existing controls and game numerals must retain their original typography.
    for (const [width,height] of [[320,850],[390,420],[844,390]]) {
      const context=await openContext(browser,width,height,true),page=await context.newPage();
      for (const id of ['prompting','vectorspace','bigupside']) {
        await context.addInitScript(id=>localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:id,visited:[id],completed:[]})),id);
        await page.goto(base+'/course',{waitUntil:'networkidle'});
        const reading=page.locator('.lesson-reading-toggle');if(await reading.count()&&await reading.getAttribute('aria-expanded')==='false')await reading.click();
        await page.locator('.interactive-box').first().waitFor();
        if(id==='prompting')assert.ok(await page.locator('.rubric-points-field input').first().evaluate(n=>parseFloat(getComputedStyle(n).fontSize)>=20),'Preserve the existing 20px rubric inputs');
        if(id==='vectorspace') {
          assert.ok(await page.locator('.g2048-score .val').first().evaluate(n=>parseFloat(getComputedStyle(n).fontSize)>=24),'Preserve large game scores');
          const before=await page.locator('.g2048-scoreval').innerText();
          await page.locator('.g2048').getByRole('button',{name:'→',exact:true}).tap();
          assert.ok(await page.locator('.g2048-howto li').evaluateAll(xs=>xs.every(n=>parseFloat(getComputedStyle(n).fontSize)>=16)));
          assert.ok(before.length>0);
        }
        if(id==='bigupside')for(const field of await page.locator('.phone-text-field').all()) {
          await field.fill('Environmental engineering');assert.ok(await field.evaluate(n=>parseFloat(getComputedStyle(n).fontSize)>=16));await field.focus();await page.keyboard.press('Tab');
        }
        await fits(page);
      }
      await context.close();
    }
    for (const [width,height,touch,phone] of [[760,850,true,true],[761,850,false,false],[844,390,false,false],[1280,1000,false,false]]) {
      const context=await openContext(browser,width,height,touch),page=await context.newPage(); await page.goto(base+'/course',{waitUntil:'networkidle'}); await page.locator('.lab-step-row').first().waitFor();
      const font=await page.locator('.lab-prompt-text').first().evaluate(n=>parseFloat(getComputedStyle(n).fontSize)); assert.equal(font>=16,phone,'Phone styles follow the established breakpoint and pointer convention'); await context.close();
    }
    if (output) { fs.mkdirSync(output,{recursive:true}); fs.writeFileSync(path.join(output,'phone-usability-checks.json'),JSON.stringify(results,null,2)); }
    console.log('PASS: phone activities, touch targets, navigation, exact prompt copying, app handoff, downloads, unfinished Finals, grading, retry, certificate flow and intercepted review submission. No external submissions.');
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exit(1)});
