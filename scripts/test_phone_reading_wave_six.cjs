// Sixth phone-readability batch. Run with the same Playwright NODE_PATH as other browser tests.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  prompt: ['contextQuestion','contextSources','contextHeadStart','contextOutside'],
  evaluating: ['evaluationProcess','evaluationQuick','evaluationCloser','evaluationMove'],
  hallucination: ['hallucinationExample','hallucinationWhy','hallucinationCheck']
};
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const records = [];
  try {
    for (const [id, kinds] of Object.entries(lessons)) {
      const context = await browser.newContext({ viewport: { width: 390, height: 850 }, hasTouch: true, reducedMotion: 'reduce' });
      await context.route(/script\.google|script\.googleusercontent|\.mp4/, r => r.abort());
      await context.addInitScript(id => {
        localStorage.clear(); localStorage.setItem('llm-user-name', 'Phone Review');
        localStorage.setItem('llm-explorer-progress', JSON.stringify({ activeSection: id, visited: [id], completed: [] }));
      }, id);
      const page = await context.newPage(), errors = [];
      page.on('pageerror', e => errors.push(e.message));
      await page.goto(base + '/index.html', { waitUntil: 'networkidle' });
      const toggle = page.locator('.lesson-reading-toggle');
      if (await toggle.count() && await toggle.getAttribute('aria-expanded') === 'false') await toggle.click();
      await page.evaluate(async () => { await document.fonts.ready; for (const image of document.images) { image.loading = 'eager'; await image.decode().catch(() => {}); } });
      assert.deepEqual(await page.locator('[data-phone-reading-board]').evaluateAll(nodes => nodes.map(n => n.dataset.phoneReadingBoard)), kinds);
      for (const [width, height] of [[320, 850], [390, 850], [430, 850], [760, 850], [761, 850], [844, 390], [1024, 1000], [1280, 1000], [1440, 1000]]) {
        await page.setViewportSize({ width, height });
        const mobile = width <= 760 || height <= 500;
        assert.equal(await page.locator('.phone-reading-mobile:visible').count(), mobile ? kinds.length : 0);
        assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), mobile ? 0 : kinds.length);
        if (mobile) {
          const boards = await page.locator('.phone-reading-mobile').evaluateAll(nodes => nodes.map(n => {
            const r = n.getBoundingClientRect();
            return { title: n.querySelector('h3').textContent, kind: n.parentElement.dataset.phoneReadingBoard, x: r.x, y: r.y + scrollY, width: r.width, height: r.height, text: n.innerText,
              tiny: [...n.querySelectorAll('p,li,h4')].filter(e => parseFloat(getComputedStyle(e).fontSize) < (e.tagName === 'H4' ? 20 : 16)).map(e => e.textContent),
              overflow: [...n.querySelectorAll('*')].filter(e => !(e instanceof SVGElement) && e.clientWidth && e.scrollWidth > e.clientWidth + 1).map(e => e.textContent) };
          }));
          for (const board of boards) { assert.deepEqual(board.tiny, []); assert.deepEqual(board.overflow, []); assert.ok(board.x >= 0 && board.x + board.width <= width); }
          const accessibility = await page.locator('#main-content').ariaSnapshot();
          for (const board of boards) {
            assert.equal(accessibility.split('\n').filter(line => line.includes('heading "' + board.title + '" [level=3]')).length, 1, board.title + ' announced once');
          }
          assert.equal(await page.locator('.phone-reading-desktop-source:visible').count(), 0);
          const geometry = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth, overflow: [...document.querySelectorAll('body *')].filter(e => !(e instanceof SVGElement) && e.children.length === 0 && e.getBoundingClientRect().width && e.getBoundingClientRect().right > innerWidth + 1).map(e => ({ tag: e.tagName, text: e.textContent.slice(0, 100), right: e.getBoundingClientRect().right })) }));
          records.push({ id, width, height, boards, geometry });
        }
      }
      await page.setViewportSize({ width: 390, height: 850 });
      if(id==='prompt') {
        const question=page.locator('[data-phone-reading-board="contextQuestion"] .phone-reading-mobile');
        const copy=await question.innerText();for(const phrase of ['What car should I buy after I graduate from college?','Luke’s AI','Nate’s AI','Jeep Cherokee','Ford Raptor','insurance, and fuel costs','Same question. Different context. Different answer.'])assert.ok(copy.includes(phrase));
        assert.equal(copy.split('What car should I buy').length-1,1);
        const graph=page.locator('[data-phone-reading-board="contextSources"] .phone-reading-mobile');
        assert.deepEqual(await graph.locator('.phone-six-source-group').allTextContents(),['FROM THIS CHAT','PERSONALIZATION AND MEMORY','PROJECT CONTEXT']);
        assert.deepEqual(await graph.locator('.phone-six-source').allTextContents(),['Your current prompt','Earlier messages and answers','Personalization','Saved Memory','Projects']);
        assert.equal(await graph.locator('.phone-six-destination').count(),1);assert.equal(await graph.locator('ol').count(),0);
        assert.equal(await graph.locator('.phone-six-source').evaluateAll(ns=>ns.every(n=>n.getAttribute('aria-describedby')==='phone-six-context-destination')),true);
        const headStart=await page.locator('[data-phone-reading-board="contextHeadStart"] .phone-reading-mobile').innerText();
        assert.equal(headStart.split('EXAMPLE').length-1,3);for(const value of ['explain new coding terms','You mention that you love pickup trucks','A summer job project holds your resume','you’ve applied','prepare for interviews'])assert.ok(headStart.includes(value));
        const checks=page.getByRole('button',{name:/^Mark step [0-9]+ (incomplete|complete)$/});assert.equal(await checks.count(),7);await checks.first().click();assert.equal(await checks.first().getAttribute('aria-pressed'),'true');
        // The existing canvas remains keyboard reachable; no external lab links are followed.
        const canvas=page.locator('canvas.dino-game-canvas');assert.equal(await canvas.count(),1);await canvas.focus();assert.equal(await canvas.evaluate(n=>n===document.activeElement),true);
      } else if(id==='evaluating') {
        assert.deepEqual(await page.locator('[data-phone-reading-board="evaluationProcess"] h4').allTextContents(),['1Do a Quick Review','2Take a Closer Look','3Make Your Move']);
        assert.ok((await page.locator('[data-phone-reading-board="evaluationProcess"] .phone-reading-mobile').innerText()).includes('If needed, dig deeper. Choose the checks that fit.'));
        assert.deepEqual(await page.locator('[data-phone-reading-board="evaluationQuick"] h4').allTextContents(),['1Read','2Understand','3Validate']);
        const closer=page.locator('[data-phone-reading-board="evaluationCloser"] .phone-reading-mobile');
        assert.deepEqual(await closer.locator('h4').allTextContents(),['What Kind of Task','How Much Is Riding on It','Check the Sources','Challenge the Answer','Check It Yourself']);
        const closerText=await closer.innerText();assert.ok(closerText.indexOf('DOES IT NEED A CLOSER LOOK?')<closerText.indexOf('What Kind of Task'));assert.ok(closerText.indexOf('The more that depends')<closerText.indexOf('WAYS TO TAKE A CLOSER LOOK'));assert.ok(closerText.indexOf('WAYS TO TAKE A CLOSER LOOK')<closerText.indexOf('Check the Sources'));
        const tree=await page.locator('#main-content').ariaSnapshot();
        for(const title of ['Do a Quick Review','Take a Closer Look. Does It Need a Closer Look?','Make Your Move'])assert.equal(tree.includes('heading \"'+title+'\" [level=3]'),false,'Hidden desktop transcript: '+title);
        const moves=page.locator('[data-phone-reading-board="evaluationMove"] .phone-reading-mobile');assert.deepEqual(await moves.locator('h4').allTextContents(),['Use It','Fix It','Walk Away']);assert.equal(await moves.locator('ol, .phone-six-flow-arrow, .phone-reading-number').count(),0);
        // The same item objects supply the original accessible desktop transcript.
        for(const kind of ['evaluationQuick','evaluationCloser','evaluationMove']) {
          const wrapper=page.locator('[data-phone-reading-board="'+kind+'"]');
          const phone=await wrapper.locator('.phone-reading-mobile').textContent();
          const source=await wrapper.locator('.phone-reading-desktop').textContent();
          for(const p of await wrapper.locator('.phone-reading-mobile .phone-reading-copy > p').allTextContents())assert.ok(source.includes(p),kind+': '+p);
        }
        await page.getByRole('button',{name:'Dig deeper',exact:true}).nth(1).click();assert.ok((await page.locator('#main-content').innerText()).includes('Details need evidence.'));
      } else {
        const example=page.locator('[data-phone-reading-board="hallucinationExample"] .phone-reading-mobile');const text=await example.innerText();
        for(const phrase of ['Will my hype playlist on Spotify help me study for chemistry, or will it distract me?','2022 Stanford study','1,200 high school students','18%','60 decibels','Want me to help you build a study playlist?','The study does not exist.'])assert.ok(text.includes(phrase));
        assert.deepEqual(await example.locator('.phone-reading-card h4').allTextContents(),['You','AI']);
        assert.equal(await example.locator('.phone-reading-stack + .phone-reading-takeaway').innerText(),'The study does not exist.');
        assert.equal(await page.locator('[data-phone-reading-board="hallucinationWhy"] .phone-six-flow > li').count(),4);
        assert.equal(await page.getByRole('heading',{name:'Probable does not equal True',exact:true}).count(),1);
        assert.deepEqual(await page.locator('[data-phone-reading-board="hallucinationCheck"] h4').allTextContents(),['1Notice the Claim','2Find the Source','3Check the Match']);
        const answers=['A study that doesn’t exist','AI learns how credible answers sound','Yes, one detail can be invented','Neither of the above','All of the above'];
        for(const answer of answers)await page.getByRole('button',{name:answer,exact:true}).click();
        assert.equal(await page.locator('.hallucination-quiz-question').count(),5);
      }
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('.phone-reading-mobile:visible').count(), 0);
      assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), kinds.length);
      assert.deepEqual(errors, []);
      await context.close();
    }
    if (process.env.PHONE_WAVE_OUTPUT) { fs.mkdirSync(process.env.PHONE_WAVE_OUTPUT, { recursive: true }); fs.writeFileSync(path.join(process.env.PHONE_WAVE_OUTPUT, 'phone-checks.json'), JSON.stringify(records, null, 2)); }
    console.log('PASS: eleven boards; phone, landscape, breakpoints, readable text, exact examples/numbers, parallel source graph, ordered flows, alternative actions, accessible representations, shared evaluation data, lesson interactions, print and no runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
