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
  await page.addInitScript(()=>{localStorage.setItem('llm-user-name','Preview');localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'prediction',visited:['prediction'],completed:[]}));});
  await page.goto(base+'/index.html',{waitUntil:'domcontentloaded'});
  const game=page.locator('.concept-match');await game.waitFor();
  assert.equal(await page.locator('.club-builder').count(),0,'Club activity belongs in Why Answers Vary');
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
   ['next-token-prediction','Calculates how likely each possible next token is, using the question and the answer so far.'],
   ['end-of-answer-token','A special token that signals the answer is complete.']
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
  // Recreate the exact reported layout; complete both rounds with real clicks/taps.
  const fixture=`
   mixedConceptDeck=function(){
    var first=['embeddings','vector-space','tokens','inference','attention'];
    return first.map(id=>UNDERSTAND_AI_CONCEPTS.find(c=>c.id===id)).concat(UNDERSTAND_AI_CONCEPTS.filter(c=>!first.includes(c.id)));
   };
   mixedDescriptionIds=function(items){
    return items[0].id==='embeddings'?['tokens','inference','attention','vector-space','embeddings']:items.map(c=>c.id).slice(1).concat(items[0].id);
   };
  `;
  for(const mode of ['mouse','touch']){
   const input=await browser.newPage(mode==='touch'?{viewport:{width:390,height:844},hasTouch:true,isMobile:true}:{viewport:{width:1280,height:650}});
   input.on('pageerror',e=>errors.push(e.message));
   await input.route('**/previews/concept-matching.html',route=>{
    const html=fs.readFileSync('previews/concept-matching.html','utf8');
    const marker="ReactDOM.createRoot(document.getElementById('preview'))";
    assert.ok(html.includes(marker));
    return route.fulfill({contentType:'text/html',body:html.replace(marker,fixture+marker)});
   });
   await input.goto(base+'/previews/concept-matching.html',{waitUntil:'domcontentloaded'});
   const g=input.locator('.concept-match');await g.waitFor();
   const select=async locator=>mode==='touch'?locator.tap():locator.click();
   const concept=id=>g.locator(`[data-concept="${id}"]`);
   const description=id=>g.locator(`[data-description="${id}"]`);
   assert.ok(await input.getByText('Select a concept, then select its description.',{exact:true}).isVisible());
   await select(description('embeddings'));
   assert.equal(await g.locator('[data-concept]:disabled').count(),0,'Description alone cannot match');
   for(const id of ['tokens','inference','attention']){
    await select(concept(id));await select(description(id));
    assert.ok(await concept(id).isDisabled());
   }
   assert.equal(await g.locator('[data-concept]:disabled').count(),3);
   // Switching selection and recovering from a wrong answer must not require a second click.
   await select(concept('vector-space'));await select(concept('embeddings'));
   assert.equal(await concept('vector-space').getAttribute('aria-pressed'),'false');
   await select(description('vector-space'));
   assert.match(await g.getByRole('status').innerText(),/^Not quite/);
   assert.equal(await concept('embeddings').getAttribute('aria-pressed'),'true');
   assert.ok((await concept('embeddings').getAttribute('class')).includes('is-selected'));
   assert.equal(await g.locator('[data-concept]:disabled').count(),3);
   await select(description('embeddings'));
   assert.ok(await concept('embeddings').isDisabled(),'Fourth pair matches without reselecting');
   await select(concept('vector-space'));
   await description('vector-space').scrollIntoViewIfNeeded();
   assert.equal(await concept('vector-space').getAttribute('aria-pressed'),'true','Selection survives scrolling');
   await select(description('vector-space'));
   assert.ok(await concept('vector-space').isDisabled(),'Last pair matches on first selection');
   assert.equal(await g.locator('[data-description]:disabled').count(),5);
   await select(g.getByRole('button',{name:'Next Five',exact:true}));
   const remaining=await g.locator('[data-concept]').evaluateAll(nodes=>nodes.map(n=>n.dataset.concept));
   for(const id of remaining){await select(concept(id));await select(description(id));assert.ok(await concept(id).isDisabled());}
   assert.match(await g.locator('.concept-match-heading').innerText(),/10 of 10 matched/);
   await select(g.getByRole('button',{name:'Try Again',exact:true}));
   assert.equal(await g.locator('[data-concept]:disabled').count(),0);
   await input.close();
  }
  await page.goto(base+'/index.html?print=lesson:prediction',{waitUntil:'domcontentloaded'});
  await game.waitFor({state:'attached'});
  await page.emulateMedia({media:'print'});
  assert.equal(await game.isVisible(),false,'Practice excluded from content-only print');
  assert.deepEqual(errors,[]);
  console.log('Concept matching passed: both rounds, all ten concepts, keyboard controls, mouse clicks, touch taps, exact final-two regression, wrong-answer recovery, selection through scrolling, restart, mobile layout, preview, and print exclusion.');
 }finally{if(browser)await browser.close();if(server)server.kill();}
})().catch(e=>{console.error(e);process.exitCode=1;});
