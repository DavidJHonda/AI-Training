// Ninth phone-readability batch. Run with the same Playwright NODE_PATH as other browser tests.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  paceofchange: ['paceComparison','paceAcceleration','paceFuture'],
  bigdownside: ['downsideLayers','downsideJailbreak','downsideVoice','downsideCyberattack'],
  bigupside: ['upsideProtein','upsideCancer','upsideReading','upsideFlood']
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
        await page.waitForTimeout(250);
        const mobile = width <= 760 || height <= 500;
        assert.equal(await page.locator('.phone-reading-mobile:visible').count(), mobile ? kinds.length : 0);
        assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), mobile ? 0 : kinds.length);
        if(!mobile)assert.equal(await page.locator('.phone-reading-mobile svg').count(),0,'Phone artwork stays unmounted on desktop');
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
      await page.waitForTimeout(250);
      if(id==='paceofchange') {
        const comparison=page.locator('[data-phone-reading-board="paceComparison"] .phone-reading-mobile');
        assert.deepEqual(await comparison.locator('h4').allTextContents(),['Answering','Images','Context Window','Doing']);
        for(const row of await comparison.locator('.phone-nine-comparison').all())assert.deepEqual(await row.locator('.phone-reading-label').allTextContents(),['2023','2026']);
        const text=await comparison.innerText();for(const phrase of ['the instant you hit enter','sometimes for minutes.','new dog Spot','a bonus leg and the ears of a rabbit.','full video with sound and dialogue.','a whole novel series','wished you luck.','book, build, and fix while you watch.'])assert.ok(text.includes(phrase),phrase);
        const future=await page.locator('[data-phone-reading-board="paceFuture"] .phone-reading-mobile').innerText();for(const phrase of ['Recursive Self-Improvement (RSI)','Artificial General Intelligence (AGI)','Artificial Superintelligence (ASI)','little or no human direction.','There is no agreed definition or test.','nearly every cognitive field.'])assert.ok(future.includes(phrase),phrase);
        await page.getByRole('button',{name:'Lock in my guesses',exact:true}).click();assert.equal(await page.locator('#doubling-guess-2027').getAttribute('aria-invalid'),'true');
        for(const [year,guess] of [[2027,'8'],[2029,'512'],[2031,'32768']])await page.getByLabel('End of '+year,{exact:true}).fill(guess);
        await page.getByRole('button',{name:'Lock in my guesses',exact:true}).click();
        for(const year of [2027,2029,2031]){await page.getByRole('button',{name:'Continue to '+year,exact:true}).click();await page.waitForFunction(year=>document.querySelector('[data-year="'+year+'"] .doubling-answer'),year);}
        assert.deepEqual(await page.locator('.doubling-answer .doubling-total').allTextContents(),['8','512','32,768']);assert.ok((await page.locator('#main-content').innerText()).includes('A picture of the pace, not a prediction.'));
        await page.getByRole('button',{name:'Play again',exact:true}).click();assert.equal(await page.locator('#doubling-guess-2027').inputValue(),'');
      } else if(id==='bigdownside') {
        const layers=await page.locator('[data-phone-reading-board="downsideLayers"] .phone-reading-mobile').innerText();for(const phrase of ['Safety Training','Screen for Harm','Limit What AI Can Do','sending money or deleting files.','Each layer helps. No layer catches everything.'])assert.ok(layers.includes(phrase),phrase);
        const scene=page.locator('[data-phone-reading-board="downsideJailbreak"] .phone-reading-mobile');assert.equal(await scene.locator('svg').count(),1);assert.deepEqual(await scene.locator('.phone-nine-scene-key p').allTextContents(),['GUARDRAILS','Defenders must protect many paths.','An attacker needs only one opening.']);
        const voice=page.locator('[data-phone-reading-board="downsideVoice"] .phone-reading-mobile');assert.deepEqual(await voice.locator('h4').allTextContents(),['1Voice Clip','2Voice Cloned','3Fake Call','4Call Back']);assert.equal(await voice.locator('.phone-nine-arrow').count(),3);assert.ok((await voice.innerText()).includes('Hang up. Call the person back on the real number you already have.'));
        const cyber=page.locator('[data-phone-reading-board="downsideCyberattack"] .phone-reading-mobile');assert.deepEqual(await cyber.locator('h4').allTextContents(),['Assignment','Boundary Crossed','Harm']);assert.equal(await cyber.locator('.phone-nine-arrow').count(),2);for(const phrase of ['unauthorized ways to communicate','Hugging Face, an AI platform','private information.','The AI pursued the goal, even when that meant cheating.'])assert.ok((await cyber.innerText()).includes(phrase),phrase);
        const options=['Hard to understand and control','People can misuse AI','AI can take the wrong route'];for(let i=0;i<6;i++)await page.locator('.scenario-row-body').nth(i).getByRole('button',{name:options[i%3],exact:true}).click();assert.equal(await page.locator('button[aria-pressed="true"]').filter({hasText:/Hard to understand|People can misuse|AI can take/}).count(),6);
      } else {
        const protein=await page.locator('[data-phone-reading-board="upsideProtein"] .phone-reading-mobile').innerText();for(const phrase of ['Experiments','About 200,000','determined through decades of experiments.','AlphaFold AI','Over 200 million','predicted and shared free.'])assert.ok(protein.includes(phrase),phrase);
        for(const [kind,titles] of [['upsideCancer',['AI Flags','Doctors Review']],['upsideReading',['Point the Camera','Hear the Words']],['upsideFlood',['Earlier Warning','Time to Act']]])assert.deepEqual(await page.locator('[data-phone-reading-board="'+kind+'"] h4').allTextContents(),titles);
        assert.ok((await page.locator('#main-content').innerText()).includes('A prediction isn’t a finished medicine. Scientists still have to test ideas and do the research.'));
        assert.ok((await page.locator('[data-phone-reading-board="upsideFlood"] .phone-reading-mobile').innerText()).includes('days ahead.'));
        assert.ok((await page.locator('[data-phone-reading-board="upsideFlood"] .phone-reading-mobile').innerText()).includes('before the water arrives.'));
        assert.equal(await page.getByRole('button',{name:'Enter Interest First',exact:true}).count(),1);await page.getByLabel('Enter your interest here',{exact:false}).fill('animals');assert.ok((await page.locator('#main-content').innerText()).includes('Find one real example of AI already helping people in animals.'));
        await page.getByRole('button',{name:'Mark step 1 complete',exact:true}).click();assert.equal(await page.getByRole('button',{name:'Mark step 1 incomplete',exact:true}).getAttribute('aria-pressed'),'true');
      }
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('.phone-reading-mobile:visible').count(), 0);
      assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), kinds.length);
      assert.deepEqual(errors, []);
      await context.close();
    }
    if (process.env.PHONE_WAVE_OUTPUT) { fs.mkdirSync(process.env.PHONE_WAVE_OUTPUT, { recursive: true }); fs.writeFileSync(path.join(process.env.PHONE_WAVE_OUTPUT, 'phone-checks.json'), JSON.stringify(records, null, 2)); }
    console.log('PASS: eleven boards; phone, landscape, breakpoints, readable HTML, complete year comparisons and qualifications, connected scam and cyberattack flows, preserved benefit relationships, accessible representations, all three lesson activities, print and no runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
