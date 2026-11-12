// Seventh phone-readability batch. Run with the same Playwright NODE_PATH as other browser tests.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  trainingbias: ['biasMechanisms','biasQuestions'],
  documenttrap: ['documentIncomplete','documentMoves'],
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
        assert.deepEqual(await page.locator('[data-phone-reading-board="biasMechanisms"] h4').allTextContents(),['Shows Up Too Often','Gets Left Out']);
        const questions=page.locator('[data-phone-reading-board="biasQuestions"] .phone-reading-mobile');
        for(const phrase of ['“What’s missing from this answer?”','“Show me examples that don’t fit the pattern you just gave.”','“Answer again, leaving out the most famous examples.”'])assert.ok((await questions.innerText()).includes(phrase));
        const sample = page.locator('p').filter({ hasText: 'gets all its study advice from websites written by science teachers' });
        assert.ok(await sample.isVisible());
        assert.match(await sample.innerText(), /The AI tells you, based on what it learned, “Three hours\.”/);
        const checks=page.getByRole('button',{name:/^Mark step [0-9]+ (incomplete|complete)$/});assert.equal(await checks.count(),4);await checks.first().click();assert.equal(await checks.first().getAttribute('aria-pressed'),'true');await checks.first().click();assert.equal(await checks.first().getAttribute('aria-pressed'),'false');
      } else if(id==='documenttrap') {
        assert.equal(await page.locator('[data-phone-reading-board="documentFlow"]').count(),0);
        assert.deepEqual(await page.locator('[data-phone-reading-board="documentMoves"] .phone-reading-mobile h4').allTextContents(),['Name the Section','Ask One Thing','Share What Matters','Ask for the Quote']);
        assert.equal(await page.locator('[data-phone-reading-board="documentMoves"] .phone-reading-mobile').locator('.phone-reading-number, ol').count(),0);
        const tree=await page.locator('#main-content').ariaSnapshot();
        assert.equal(tree.includes('heading "Split, Search, Load" [level=3]'),false);
        assert.equal(tree.includes('heading "Four moves for better retrieval" [level=3]'),false);
        for(const kind of ['documentMoves']) {
          const wrapper=page.locator('[data-phone-reading-board="'+kind+'"]');
          const source=await wrapper.locator('.phone-reading-desktop').textContent();
          for(const p of await wrapper.locator('.phone-reading-mobile .phone-reading-copy > p').allTextContents())assert.ok(source.includes(p),kind+': '+p);
        }
        const moves=page.locator('.activity-scenario');
        assert.equal(await moves.count(),6);
        for(const [i,good] of [true,false,true,true,false,true].entries()) {
          await moves.nth(i).getByRole('button',{name:good?'Good Move':'Not So Good',exact:true}).click();
          assert.ok(await moves.nth(i).getByText('Correct',{exact:true}).isVisible());
        }
        for(const feedback of ['A section heading tells AI where to look in those 500 pages.','The passage is now part of your question.','Reading the original lets you check both the wording and what it means in context.'])assert.ok((await page.locator('#main-content').innerText()).includes(feedback));
      } else {
        const comparison=page.locator('[data-phone-reading-board="trustComparison"] .phone-reading-mobile');
        assert.deepEqual(await comparison.locator('h4').allTextContents(),['YOU','Your Mom','The Chatbot']);
        for(const phrase of ['Should I choose Michigan or Indiana?','Indiana. You seemed more comfortable there','Michigan. It offers world-class academics','Your mom knows you. She’s seen how you go quiet when you’re stuck, and she has a stake in what happens to you.','The chatbot knows what you typed. It’s never seen how you act when you’re stuck, and it has no stake in which school you choose.'])assert.ok((await comparison.innerText()).includes(phrase));
        assert.deepEqual(await comparison.locator('.phone-reading-fact strong').allTextContents(), ['The Truth', 'The Truth']);
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
    console.log('PASS: study-time example and six boards; phone, landscape, breakpoints, readable HTML, exact prompts, original scenes, document tips and six choices, complete trust comparison, accessible representations, shared document data, lesson activities, print and no runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
