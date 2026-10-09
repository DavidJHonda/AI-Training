// Verify matching behavior in the lesson and generated review preview.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {spawn}=require('node:child_process');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || '/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const base=process.env.BASE_URL || 'http://127.0.0.1:8794';
(async()=>{
 const server=process.env.BASE_URL?null:spawn('python3',['-m','http.server','8794','--bind','127.0.0.1'],{stdio:'ignore'});
 let browser;
 try {
  browser=await chromium.launch({channel:'chrome',headless:true});
  const page=await browser.newPage({viewport:{width:1280,height:1100}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route(/script\.google|script\.googleusercontent|\.mp4/,r=>r.abort());
  await page.addInitScript(()=>{localStorage.setItem('llm-user-name','Preview');localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'inference',visited:['inference'],completed:[]}));});
  await page.goto(base);
  const game=page.locator('.concept-match');await game.waitFor();
  await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.getByText('How Big Is 2 Quadrillion?',{exact:false}).count(),0);
  const expected=[
   ['training','AI makes guesses, gets feedback, and adjusts its weights.'],
   ['probability','How likely something is to happen. A better chance isn’t a guarantee.'],
   ['tokens','Pieces of text: a word, part of a word, or punctuation.'],
   ['embeddings','Lists of numbers that help AI work with meaning.'],
   ['attention','Helps AI connect words and figure out what they mean in context.'],
   ['layers','Repeated steps that build meaning by updating each token’s numbers.'],
   ['vector-space','A map made of numbers. Similar meanings tend to land near each other.'],
   ['inference','AI uses what it learned to build an answer, one token at a time.'],
   ['sampling','Picking the next token using the odds. The top choice doesn’t always win.'],
   ['temperature','Changes the odds, giving less likely tokens more or less of a chance.']
  ];
  fs.mkdirSync('tmp/concept-matching',{recursive:true});
  await page.addStyleTag({content:'.sticky-lesson-bar{visibility:hidden!important}'});
  for(const width of (process.env.CHECK_WIDTH?[Number(process.env.CHECK_WIDTH)]:[1280,390,320])){
   await page.setViewportSize({width,height:1100});
   const seen=new Set();
   for(let round=0;round<2;round++){
    assert.equal(await game.getAttribute('data-round'),String(round));
    assert.equal(await game.locator('[data-concept]').count(),5);
    assert.equal(await game.locator('[data-description]').count(),5);
    const ids=await game.locator('[data-concept]').evaluateAll(nodes=>nodes.map(n=>n.dataset.concept));
    const descriptions=await game.locator('[data-description]').evaluateAll(nodes=>nodes.map(n=>n.dataset.description));
    assert.deepEqual([...descriptions].sort(),[...ids].sort(),'Every concept has exactly one description');
    ids.forEach((id,i)=>{assert.notEqual(id,descriptions[i],'No direct row matches');assert.ok(!seen.has(id),'No repeat concepts across rounds');seen.add(id);});
    const concepts=ids.map(id=>expected.find(item=>item[0]===id));
    assert.equal(await game.locator('h4,.concept-match-selection').count(),0,'No column headings or subtext');
    if(width>540){
      const columns=await game.evaluate(el=>['[data-concept]','[data-description]'].map(selector=>[...el.querySelectorAll(selector)].map(n=>({top:n.getBoundingClientRect().top,height:n.getBoundingClientRect().height}))));
      columns[0].forEach((r,i)=>{assert.ok(Math.abs(r.top-columns[1][i].top)<1);assert.ok(Math.abs(r.height-columns[1][i].height)<1);});
    }

    for(const [id,description] of concepts)assert.equal(await game.locator(`[data-description="${id}"]`).innerText(),description);
    assert.ok(await game.evaluate(el=>el.scrollWidth<=el.clientWidth && el.getBoundingClientRect().right<=innerWidth),'Matching activity fits the viewport');
    await game.screenshot({path:`tmp/concept-matching/${width}-round-${round+1}.png`});
    // Wrong matches must not lock either card or advance progress.
    const first=game.locator(`[data-concept="${concepts[0][0]}"]`);
    await first.focus();await page.keyboard.press('Enter');
    assert.equal(await first.getAttribute('aria-pressed'),'true');
    const wrong=game.locator(`[data-description="${concepts[1][0]}"]`);
    await wrong.focus();await page.keyboard.press('Space');
    assert.match(await game.getByRole('status').innerText(),/^Not quite\./);
    assert.equal(await game.locator('[data-description]:disabled').count(),0);
    assert.equal(await first.isEnabled(),true);
    // Pair each approved description through native keyboard controls.
    for(const [id] of concepts){
     const concept=game.locator(`[data-concept="${id}"]`);
     const description=game.locator(`[data-description="${id}"]`);
     const beforeConcept=await concept.boundingBox(),beforeDescription=await description.boundingBox();
     const originalConceptText=await concept.innerText(),originalDescriptionText=await description.innerText();
     await concept.focus();await page.keyboard.press('Enter');
     await description.focus();await page.keyboard.press('Space');
     assert.ok(await concept.isDisabled());assert.ok(await description.isDisabled());
     assert.equal(await concept.innerText(),originalConceptText,'Matching does not add concept text');
     assert.equal(await description.innerText(),originalDescriptionText,'Matching does not add description text');
     for(const [card,before] of [[concept,beforeConcept],[description,beforeDescription]]){
      const after=await card.boundingBox();
      assert.equal(after.width,before.width,'Matched card keeps its width');
      assert.equal(after.height,before.height,'Matched card keeps its height');
     }
     assert.equal(await concept.getAttribute('aria-pressed'),'false');
    }
    assert.equal(await game.locator('[data-description]:disabled').count(),5);
    await game.screenshot({path:`tmp/concept-matching/${width}-matched-${round+1}.png`});
    const advance=game.getByRole('button',{name:round?'Try Again':'Next Five',exact:true});
    assert.ok(await advance.evaluate(el=>el===document.activeElement),'Focus moves to next-round/restart action');
    await page.keyboard.press('Enter');
    assert.equal(await game.locator('[data-concept]:disabled').count(),0);
    assert.ok(await game.locator('[data-concept]').first().evaluate(el=>el===document.activeElement),'Focus returns to available concept');
   }
   assert.equal(seen.size,10,'All ten concepts reviewed');
  }
  await page.goto(base+'/previews/concept-matching.html');await game.waitFor();
  assert.equal(await game.getAttribute('data-round'),'0');
  await page.setViewportSize({width:1280,height:1100});
  async function beginDrag(id){
    const source=game.locator(`[data-concept="${id}"]`);await source.scrollIntoViewIfNeeded();
    const box=await source.boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();
    await page.mouse.move(box.x+box.width/2+12,box.y+box.height/2+12,{steps:3});
    assert.equal(await page.locator('.concept-match-drag').count(),1);
  }
  async function hoverDescription(id){
    const target=game.locator(`[data-description="${id}"]`);const box=await target.boundingBox();
    await page.mouse.move(box.x+box.width/2,box.y+box.height/2,{steps:8});
    return target;
  }
  const dragIds=await game.locator('[data-concept]').evaluateAll(nodes=>nodes.map(n=>n.dataset.concept));
  await beginDrag(dragIds[0]);
  const wrongDrop=await hoverDescription(dragIds[1]);
  assert.ok((await wrongDrop.getAttribute('class')).includes('is-drop-target'));
  await page.screenshot({path:'tmp/concept-matching/drag-target.png'});
  await page.mouse.up();
  assert.match(await game.getByRole('status').innerText(),/^Not quite/);
  assert.ok(await wrongDrop.evaluate(el=>el.matches(':hover')),'Pointer remains over the wrong drop');
  assert.equal(await wrongDrop.evaluate(el=>getComputedStyle(el).borderTopColor),'rgb(212, 51, 74)','Wrong drop turns red immediately under the stationary pointer');
  await page.screenshot({path:'tmp/concept-matching/wrong-drop-released.png'});

  assert.equal(await game.locator('[data-description]:disabled').count(),0);
  await beginDrag(dragIds[0]);await hoverDescription(dragIds[0]);await page.mouse.up();
  assert.ok(await game.locator(`[data-concept="${dragIds[0]}"]`).isDisabled());
  assert.ok(await game.locator(`[data-description="${dragIds[0]}"]`).isDisabled());
  assert.equal(await page.locator('.concept-match-drag').count(),0);
  await beginDrag(dragIds[1]);await page.mouse.move(5,5);await page.mouse.up();
  assert.equal(await game.locator('[data-description]:disabled').count(),1,'Outside drop does not match');
  await beginDrag(dragIds[1]);await page.keyboard.press('Escape');await page.mouse.up();
  assert.equal(await page.locator('.concept-match-drag').count(),0,'Escape removes drag preview');
  await game.locator(`[data-concept="${dragIds[1]}"]`).focus();await page.keyboard.press('Enter');
  assert.equal(await game.locator(`[data-concept="${dragIds[1]}"]`).getAttribute('aria-pressed'),'true','Keyboard selection works after cancelled drag');
  // Touch uses the same drop behavior and can scroll down to descriptions.
  const touch=await browser.newPage({viewport:{width:390,height:844},hasTouch:true,isMobile:true});
  touch.on('pageerror',e=>errors.push(e.message));
  await touch.goto(base+'/previews/concept-matching.html');
  const tg=touch.locator('.concept-match');await tg.waitFor();
  const cdp=await touch.context().newCDPSession(touch);
  async function touchStart(id){
    const source=tg.locator(`[data-concept="${id}"]`);await source.scrollIntoViewIfNeeded();
    const box=await source.boundingBox();const point={x:Math.round(box.x+box.width/2),y:Math.round(box.y+box.height/2),id:1};
    await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[point]});
    await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{...point,x:point.x+12}]});
  }
  const touchIds=await tg.locator('[data-concept]').evaluateAll(nodes=>nodes.map(n=>n.dataset.concept));
  await touchStart(touchIds[0]);
  const before=await touch.evaluate(()=>scrollY);
  await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:200,y:830,id:1}]});
  await touch.waitForFunction(y=>scrollY>y,before);
  await tg.locator(`[data-description="${touchIds[0]}"]`).scrollIntoViewIfNeeded();
  const dropBox=await tg.locator(`[data-description="${touchIds[0]}"]`).boundingBox();
  await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:Math.round(dropBox.x+dropBox.width/2),y:Math.round(dropBox.y+dropBox.height/2),id:1}]});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  assert.ok(await tg.locator(`[data-description="${touchIds[0]}"]`).isDisabled(),'Touch drop matches');
  await touchStart(touchIds[1]);
  await cdp.send('Input.dispatchTouchEvent',{type:'touchCancel',touchPoints:[]});
  assert.equal(await touch.locator('.concept-match-drag').count(),0,'Touch cancellation clears drag');
  assert.equal(await tg.locator('[data-description]:disabled').count(),1);
  await touch.close();
  await page.goto(base+'/?print=lesson:inference');
  await game.waitFor({state:'attached'});
  await page.emulateMedia({media:'print'});
  assert.equal(await game.isVisible(),false,'Practice excluded from content-only print');
  assert.deepEqual(errors,[]);
  console.log('Concept matching passed: approved copy, shuffled rounds with no direct row matches, all ten concepts exactly once, wrong-answer recovery, locked correct pairs, keyboard focus, replay, mouse/touch dragging, drop highlighting, cancellation, edge scrolling, mobile layout, preview, and print exclusion.');
 }finally{if(browser)await browser.close();if(server)server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
