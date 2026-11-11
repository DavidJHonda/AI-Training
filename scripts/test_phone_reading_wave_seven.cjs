// Seventh phone-readability batch. Run with the same Playwright NODE_PATH as other browser tests.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  trainingbias: ['biasWrongPattern','biasMechanisms','biasQuestions'],
  documenttrap: ['documentIncomplete','documentFlow','documentMoves'],
  mindtrap: ['trustComparison','trustEliza']
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
      if(id==='trainingbias') {
        assert.deepEqual(await page.locator('[data-phone-reading-board="biasMechanisms"] h4').allTextContents(),['Defaults','Blind Spots','Wrong Patterns']);
        const questions=page.locator('[data-phone-reading-board="biasQuestions"] .phone-reading-mobile');
        for(const phrase of ['“What’s missing from this answer?”','“Show me examples that don’t fit the pattern you just gave.”','“Answer again, leaving out the most famous examples.”','The model often has the rest of the picture. It just doesn’t lead with it.'])assert.ok((await questions.innerText()).includes(phrase));
        assert.equal(await page.locator('[data-phone-reading-board="biasWrongPattern"] .phone-reading-mobile [role="img"]').count(),1);
        const checks=page.getByRole('button',{name:/^Mark step [0-9]+ (incomplete|complete)$/});assert.equal(await checks.count(),4);await checks.first().click();assert.equal(await checks.first().getAttribute('aria-pressed'),'true');await checks.first().click();assert.equal(await checks.first().getAttribute('aria-pressed'),'false');
      } else if(id==='documenttrap') {
        assert.deepEqual(await page.locator('[data-phone-reading-board="documentFlow"] .phone-reading-mobile h4').allTextContents(),['1Split','2Search','3Load']);
        assert.equal(await page.locator('[data-phone-reading-board="documentFlow"] .phone-seven-flow-arrow').count(),2);
        assert.deepEqual(await page.locator('[data-phone-reading-board="documentMoves"] .phone-reading-mobile h4').allTextContents(),['Name the Section','Ask One Thing','Share What Matters','Ask for the Quote']);
        assert.equal(await page.locator('[data-phone-reading-board="documentMoves"] .phone-reading-mobile').locator('.phone-reading-number, ol').count(),0);
        const tree=await page.locator('#main-content').ariaSnapshot();
        assert.equal(tree.split('heading "Split, Search, Load" [level=3]').length-1,1);
        assert.equal(tree.includes('heading "Four moves for better retrieval" [level=3]'),false);
        for(const kind of ['documentFlow','documentMoves']) {
          const wrapper=page.locator('[data-phone-reading-board="'+kind+'"]');
          const source=await wrapper.locator('.phone-reading-desktop').textContent();
          for(const p of await wrapper.locator('.phone-reading-mobile .phone-reading-copy > p').allTextContents())assert.ok(source.includes(p),kind+': '+p);
        }
        for(const answer of ['Ask two questions in two messages: pets first, then the deposit.','Paste the two paragraphs into your message, then ask your question.','Are there any conditions or exceptions anywhere in the document that could stop the renewal? Quote any you find.'])await page.getByRole('button',{name:answer,exact:true}).click();
        for(const feedback of ['One question, one target.','Put the evidence in the message.','Search for what could change the answer.'])assert.ok((await page.locator('#main-content').innerText()).includes(feedback));
      } else {
        const comparison=page.locator('[data-phone-reading-board="trustComparison"] .phone-reading-mobile');
        assert.deepEqual(await comparison.locator('h4').allTextContents(),['YOU','Your Mom','The Chatbot']);
        for(const phrase of ['Should I choose Michigan or Indiana?','Indiana. You seemed more comfortable there','Michigan. It offers world-class academics','KNOWS','Your history.','NOTICES','How you act when you are stuck.','SEES','What you typed.','MATCHES','Common patterns.','Shares the outcome.','Does not share the outcome.'])assert.ok((await comparison.innerText()).includes(phrase));
        assert.equal((await comparison.innerText()).split('STAKE').length-1,2);
        const eliza=page.locator('[data-phone-reading-board="trustEliza"] .phone-reading-mobile');
        assert.deepEqual(await eliza.locator('h4').allTextContents(),['AI Sounds Like One','Your Brain Looks for a Person']);
        assert.equal(await eliza.locator('.phone-seven-flow-arrow').count(),1);
        for(const phrase of ['“I think”','“I feel.”','But those are generated words.','Sounding human does not make AI human.'])assert.ok((await eliza.innerText()).includes(phrase));
        for(const answer of ['AI just did, and that’s fine. Take the pick.','You, after AI helps build a checklist and someone who knows cars inspects the car.','You, with your coach and your parents, after AI helps map the trade-offs.'])await page.getByRole('button',{name:answer,exact:true}).click();
        for(const feedback of ['Let it pick.','Use it, then decide with people.','Gather here, decide there.'])assert.ok((await page.locator('#main-content').innerText()).includes(feedback));
      }
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('.phone-reading-mobile:visible').count(), 0);
      assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), kinds.length);
      assert.deepEqual(errors, []);
      await context.close();
    }
    if (process.env.PHONE_WAVE_OUTPUT) { fs.mkdirSync(process.env.PHONE_WAVE_OUTPUT, { recursive: true }); fs.writeFileSync(path.join(process.env.PHONE_WAVE_OUTPUT, 'phone-checks.json'), JSON.stringify(records, null, 2)); }
    console.log('PASS: eight boards; phone, landscape, breakpoints, readable HTML, exact prompts, original scenes, ordered retrieval, complete trust comparison, accessible representations, shared retrieval data, lesson activities, print and no runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
