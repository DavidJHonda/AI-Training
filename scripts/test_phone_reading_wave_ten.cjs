// Tenth phone-readability batch. Run with the same Playwright NODE_PATH as other browser tests.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  workchanges: ['workAssignment','workWays'],
  computecost: ['computeMath','computeNeighbors','computeDemand'],
  unexpected: ['unexpectedPlans']
};
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const records = [];
  try {
    for (const [id, kinds] of Object.entries(lessons)) {
      const context = await browser.newContext({ viewport: { width: 390, height: 850 }, hasTouch: true, reducedMotion: 'reduce' });
      await context.route(/script\.google|script\.googleusercontent|\.mp4/, r => r.abort());
      await context.addInitScript(id => {
        if (sessionStorage.getItem('phone-wave-ten-initialized')) return;
        sessionStorage.setItem('phone-wave-ten-initialized', 'true');
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
      if(id==='workchanges') {
        const assignment=page.locator('[data-phone-reading-board="workAssignment"] .phone-reading-mobile');
        assert.deepEqual(await assignment.locator('h4').allTextContents(),['THE ASSIGNMENT','Detail Work','Analysis & Recommendation']);
        assert.deepEqual(await assignment.locator('.phone-reading-label').allTextContents(),['STAGE 1','STAGE 2']);
        assert.equal(await assignment.locator('.phone-ten-arrow').count(),1);
        assert.deepEqual(await assignment.locator('ul li').allTextContents(),['Read and organize 500 reviews','Find the recurring themes','Build the spreadsheet','Draft the initial summary','Check and improve AI’s work','Investigate why the problems are happening','Compare possible fixes','Recommend the fix and present the findings']);
        const text=await assignment.innerText();for(const phrase of ['We’re getting bad customer feedback on our new product. Read the last 500 reviews','Before AI, you did all of this yourself.','AI organizes and summarizes the information.','You check the work and decide what to do.'])assert.ok(text.includes(phrase),phrase);
        const ways=await page.locator('[data-phone-reading-board="workWays"] .phone-reading-mobile').innerText();for(const phrase of ['Automate','Augment','It sorted the reviews, grouped the ideas, and created the first summary.','AI helped you explore more explanations, compare more options, and improve your recommendation.','The work still has your name on it. You own the outcome.'])assert.ok(ways.includes(phrase),phrase);
        for(const [label,value] of [['What I checked','I checked the two-star reviews.'],['What I changed or rejected','I rejected the surface explanation.'],['Why I chose this recommendation','I chose the fix supported by the reviews.']])await page.getByLabel(label,{exact:true}).fill(value);
        await page.getByRole('button',{name:'Mark step 1 complete',exact:true}).click();
        await page.reload({waitUntil:'networkidle'});
        assert.equal(await page.getByLabel('What I checked',{exact:true}).inputValue(),'I checked the two-star reviews.');
        assert.equal(await page.getByRole('button',{name:'Mark step 1 incomplete',exact:true}).getAttribute('aria-pressed'),'true');
        const toggle=page.locator('.lesson-reading-toggle');if(await toggle.getAttribute('aria-expanded')==='false')await toggle.click();
        assert.ok((await page.locator('#main-content').innerText()).includes('All 100 reviews, one copy.'));
      } else if(id==='computecost') {
        const math=page.locator('[data-phone-reading-board="computeMath"] .phone-reading-mobile');
        assert.deepEqual(await math.locator('h4').allTextContents(),['One Token','A Short Answer','A Longer Conversation']);
        assert.deepEqual(await math.locator('.phone-ten-total').allTextContents(),['≈ 2 trillion calculations','≈ 200 trillion calculations','≈ 2 quadrillion calculations']);
        for(const phrase of ['Spot','ONE PASS','ABOUT 100 TOKENS','ABOUT 1,000 TOKENS','our example model’s trillion weights','AI across the conversation','In this example, even a short answer takes trillions of calculations.'])assert.ok((await math.innerText()).includes(phrase),phrase);
        const neighbors=await page.locator('[data-phone-reading-board="computeNeighbors"] .phone-reading-mobile').innerText();for(const phrase of ['4.4%','in 2023','Berkeley Lab projected 6.7–12% by 2028.','In some places','about a million gallons on a hot day.','Others recycle or reuse it.','24 hours a day.','In some towns','Construction employs many people','only 100 to 200 permanent workers.','about the staff of a big supermarket.'])assert.ok(neighbors.includes(phrase),phrase);
        const demand=await page.locator('[data-phone-reading-board="computeDemand"] .phone-reading-mobile').innerText();for(const phrase of ['More Power','Better Cooling','More Efficient Chips','Some cooling designs reuse water','More power meets demand. Better efficiency reduces the resources needed per task.'])assert.ok(demand.includes(phrase),phrase);
        assert.equal(await page.locator('img[src*="data-centers-data-center.jpg"]:visible').count(),1);
        for(const answer of ['How many are construction jobs, and how many stay after it opens?','How much electricity will the whole facility need?','Who pays for any new power lines or other grid upgrades?'])await page.getByRole('button',{name:answer,exact:true}).click();
        assert.ok((await page.locator('#main-content').innerText()).includes('Know what to ask.'));
        await page.getByRole('button',{name:/^40 quintillion/}).click();assert.ok((await page.locator('#main-content').innerText()).includes('Click the button again to see a different celebration!'));
      } else {
        const plans=page.locator('[data-phone-reading-board="unexpectedPlans"] .phone-reading-mobile');assert.deepEqual(await plans.locator('h4').allTextContents(),['Text Messaging','Cane Toads']);
        for(const phrase of ['SMS was built to send short messages over mobile networks.','Its creators did not expect it to take off the way it did.','Young people helped turn texting into an everyday way to stay in touch.','Australia imported cane toads to eat beetles destroying sugarcane.','They barely controlled the pests, poisoned native animals, and spread across the country.'])assert.ok((await plans.innerText()).includes(phrase),phrase);
        for(const answer of ['About 20,000','They smuggled rats in from outside the city','Temperature regulation','Get lots of cats','About 15,000'])await page.getByRole('button',{name:answer,exact:true}).click();
        for(const phrase of ['20,114 tails in a single day.','rat import business.','about 17% of its heat loss','incentives point the right way.','about 15,000 in a single year under ideal conditions.'])assert.ok((await page.locator('#main-content').innerText()).includes(phrase),phrase);
        assert.equal(await page.getByRole('button',{name:'Play The Hanoi Rat Story (optional video, 4 minutes 28 seconds)',exact:true}).count(),1);
        assert.equal(await page.locator('a[href="group-exercises/unexpected-results/what-happened-next.html"]').count(),1);
      }
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('.phone-reading-mobile:visible').count(), 0);
      assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), kinds.length);
      assert.deepEqual(errors, []);
      await context.close();
    }
    if (process.env.PHONE_WAVE_OUTPUT) { fs.mkdirSync(process.env.PHONE_WAVE_OUTPUT, { recursive: true }); fs.writeFileSync(path.join(process.env.PHONE_WAVE_OUTPUT, 'phone-checks.json'), JSON.stringify(records, null, 2)); }
    console.log('PASS: six boards; phone, landscape, breakpoints, readable HTML, complete assignment and task lists, exact calculation totals and resource qualifications, historical outcomes, accessible representations, persistent lab notes/checklist, town and rat quizzes, print and no runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
