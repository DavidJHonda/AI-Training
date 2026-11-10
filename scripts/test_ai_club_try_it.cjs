// Verify all branches, manual rebuilding, comparison, and learner controls.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const html=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
const context={};
vm.runInNewContext(html.slice(html.indexOf('var AI_CLUB_BRANCHES ='),html.indexOf('function PredictionLoopTryIt(')),context);
let leaves=0;
const possibleNames=new Set();
function walk(tokens){
 const options=context.aiClubChoices(tokens);
 if(tokens.length===5){assert.equal(options.length,0);leaves++;possibleNames.add(tokens.join(' '));return;}
 assert.equal(options.length,3,'Every unfinished path offers three choices');
 assert.equal(options.reduce((sum,o)=>sum+o.probability,0),100);
 assert.equal(new Set(options.map(o=>o.token)).size,3);
 if(tokens.length<4){
  const nextDistributions=options.map(option=>JSON.stringify(
   context.aiClubChoices(tokens.concat(option.token)).map(next=>[next.token,next.probability]).sort((a,b)=>a[0].localeCompare(b[0]))));
  assert.equal(new Set(nextDistributions).size,3,`Every choice changes the next distribution after: ${tokens.join(' ') || '(start)'}`);
 }
 for(const option of options){assert.match(option.token,/^\S+$/);walk(tokens.concat(option.token));}
}
walk([]);
assert.equal(leaves,243);
assert.equal(context.AI_CLUB_STRANGE_NAMES.length,10);
for(const item of context.AI_CLUB_STRANGE_NAMES){
 assert.ok(possibleNames.has(item.name),`Featured name is buildable: ${item.name}`);
 assert.ok(item.name.includes(item.highlight),'Purple emphasis is part of the name');
}
const base=process.env.BASE_URL || 'http://127.0.0.1:8797';
const output=path.join(__dirname,'../output/ai-club-try-it');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try {
  const page=await browser.newPage({viewport:{width:1280,height:1100}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route(/script\.google|script\.googleusercontent|\.mp4/,route=>route.abort());
  await page.addInitScript(()=>{
   localStorage.setItem('llm-user-name','Preview');
   localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'inference',visited:['inference'],completed:[]}));
  });
  await page.goto(base+'/index.html',{waitUntil:'domcontentloaded'});
  const club=page.locator('.club-builder');await club.waitFor();
  assert.equal(await page.locator('.concept-match').count(),0,'Matching activity belongs in How AI Answers');
  fs.mkdirSync(output,{recursive:true});
  const choose=async token=>{await club.getByRole('button',{name:new RegExp('^'+token+', \\d+ percent$')}).click();};
  const choices=()=>club.locator('.club-builder-word').allTextContents();
  const answer=async ()=>(await club.locator('.club-builder-answer').innerText()).trim();
  const restart=()=>club.getByRole('button',{name:'Build another name',exact:true}).click();
  assert.deepEqual(await choices(),['The','Humans','Less']);
  assert.equal(await club.locator('.club-builder-slot').count(),5);
  const possibilities=club.locator('.club-builder-possibilities');
  assert.equal(await possibilities.count(),0,'Examples stay hidden until the first complete name');
  await club.screenshot({path:path.join(output,'1280-empty-slots.png')});
  assert.equal(await club.getByRole('button',{name:'Undo last word',exact:true}).isDisabled(),true);
  // Compare different starts, then different continuations of the same start.
  await choose('The');assert.deepEqual(await choices(),['League','Robots','Curious']);
  assert.equal(await club.locator('.club-builder-slot').count(),4);
  await choose('League');assert.deepEqual(await choices(),['of','for','Exploring']);
  await club.getByRole('button',{name:'Undo last word',exact:true}).click();
  assert.equal(await answer(),'The');
  await choose('Robots');assert.deepEqual(await choices(),['Ate','Stole','Did']);
  await choose('Ate');await choose('My');await choose('Homework');
  assert.equal(await answer(),'The Robots Ate My Homework');
  assert.equal(await club.locator('.club-builder-choice').count(),0,'Stops at five words');
  assert.equal(await club.locator('.club-builder-slot').count(),0);
  assert.equal(await club.getByRole('button',{name:'Build another name',exact:true}).evaluate(n=>n===document.activeElement),true);
  assert.equal(await possibilities.evaluate(n=>n.open),false,'Examples start collapsed');
  await possibilities.locator('summary').focus();await page.keyboard.press('Enter');
  assert.equal(await possibilities.evaluate(n=>n.open),true,'Disclosure opens with keyboard');
  assert.equal(await possibilities.locator('li').count(),10);
  const nameList=possibilities.getByRole('region',{name:'Ten strange club names'});
  assert.equal(await nameList.evaluate(n=>{
   const box=n.getBoundingClientRect(),rows=[...n.querySelectorAll('li')].map(row=>row.getBoundingClientRect());
   return rows.filter(row=>row.bottom<=box.bottom).length===5 && rows[5].top<box.bottom && rows[5].bottom>box.bottom;
  }),true,'Five full names and part of the sixth signal more below');
  await nameList.focus();await page.keyboard.press('End');
  await page.waitForFunction(()=>{const n=document.querySelector('.club-builder-name-list');return n.scrollTop+n.clientHeight>=n.scrollHeight-2;});
  await nameList.evaluate(n=>{n.scrollTop=0;});
  await club.screenshot({path:path.join(output,'1280-strange-possibilities.png')});
  await club.getByRole('button',{name:'Undo last word',exact:true}).click();
  assert.equal(await answer(),'The Robots Ate My');
  assert.equal(await club.locator('.club-builder-slot').count(),1,'Undo restores the empty slot');
  assert.deepEqual(await choices(),['Homework','Lunch','Notes']);
  await choose('Lunch');await restart();
  assert.equal(await possibilities.evaluate(n=>n.open),true,'Examples remain available and open during rebuilding');
  // Revising a word changes both the displayed odds and the leading continuation.
  await choose('Humans');await choose('Teach');await choose('Robots');await choose('New');
  assert.deepEqual(await choices(),['Tricks','Skills','Habits']);
  assert.deepEqual(await club.locator('.club-builder-probability').allTextContents(),['55%','30%','15%']);
  await club.getByRole('button',{name:'Undo last word',exact:true}).click();await choose('Unexpected');
  assert.deepEqual(await choices(),['Habits','Tricks','Skills']);
  assert.deepEqual(await club.locator('.club-builder-probability').allTextContents(),['60%','25%','15%']);
  assert.deepEqual(await club.locator('.club-builder-choice-bar > span').evaluateAll(nodes=>nodes.map(n=>n.style.width)),['60%','25%','15%']);
  await choose('Habits');await restart();
  for(const words of [
   ['The','League','of','Curious','Machines'],
   ['Humans','First','Robots','Bring','Snacks'],
   ['Less','Hype','More','Human','Intelligence']
  ]){
   for(const token of words)await choose(token);
   assert.equal(await answer(),words.join(' '));
   assert.equal(await club.locator('.club-builder-count').innerText(),'5 of 5 words');
   await restart();
   assert.equal(await club.locator('.club-builder-count').innerText(),'0 of 5 words');
   assert.equal(await club.locator('.club-builder-slot').count(),5,'Build another name restores five slots');
  }
  // Rebuilding clears the slots and keeps the immediately previous name.
  assert.equal(await club.getByRole('button',{name:'Pick for me',exact:true}).count(),0);
  assert.deepEqual(await club.locator('.club-builder-choice-bar > span').evaluateAll(nodes=>nodes.map(n=>n.style.width)),
    await club.locator('.club-builder-probability').allTextContents());
  for(const token of ['Less','Fear','More','Human','Intelligence']) await choose(token);
  const firstName=await answer();
  assert.equal(await club.locator('.club-builder-finish button').count(),1);
  await restart();
  assert.equal(await club.locator('.club-builder-previous').innerText(),firstName);
  assert.equal(await answer(),'');
  assert.equal(await club.locator('.club-builder-slot').count(),5);
  assert.deepEqual(await choices(),['The','Humans','Less']);
  assert.equal(await club.locator('.club-builder-choice').first().evaluate(n=>n===document.activeElement),true);
  for(const token of ['The','League','of','Curious','Machines']) await choose(token);
  const secondName=await answer();
  assert.notEqual(secondName,firstName);
  assert.equal(await club.locator('.club-builder-previous').innerText(),firstName);
  const order=await club.evaluate(root=>{
   const question=root.querySelector('.club-builder-question'), finish=root.querySelector('.club-builder-finish'), previous=root.querySelector('.club-builder-previous'), answer=root.querySelector('.club-builder-answer');
   return [question,finish,previous].every((node,i)=>Boolean(node.compareDocumentPosition([finish,previous,answer][i]) & Node.DOCUMENT_POSITION_FOLLOWING));
  });
  assert.equal(order,true,'Completion order: question, action, previous name, current answer');
  await club.screenshot({path:path.join(output,'1280-comparison.png')});
  await club.getByRole('button',{name:'Undo last word',exact:true}).click();
  assert.equal(await club.locator('.club-builder-count').innerText(),'4 of 5 words');
  await choose('Machines');
  await restart();
  assert.equal(await club.locator('.club-builder-previous').innerText(),secondName);
  // Keyboard-only selection remains usable as the choices are replaced.
  await club.getByRole('button',{name:'The, 40 percent'}).focus();
  await page.keyboard.press('Enter');
  assert.equal(await answer(),'The');
  assert.equal(await club.locator('.club-builder-choice').first().evaluate(n=>n===document.activeElement),true);
  await page.keyboard.press('Space');
  assert.equal(await answer(),'The League');
  for(const width of [1280,650,390,320]){
   await page.setViewportSize({width,height:1100});
   assert.equal(await club.evaluate(n=>n.scrollWidth<=n.clientWidth && n.getBoundingClientRect().right<=innerWidth),true,`No overflow at ${width}`);
   await club.screenshot({path:path.join(output,`${width}-choices.png`)});
  }
  await choose('Exploring');await choose('Machine');await choose('Intelligence');
  assert.equal(await answer(),'The League Exploring Machine Intelligence');
  assert.equal(await club.evaluate(n=>n.scrollWidth<=n.clientWidth),true,'Long completed name fits narrow screen');
  await club.screenshot({path:path.join(output,'320-complete.png')});
  assert.equal(await nameList.evaluate(n=>n.scrollWidth<=n.clientWidth),true,'Names wrap without horizontal scrolling on mobile');
  await possibilities.locator('summary').focus();await page.keyboard.press('Enter');
  assert.equal(await possibilities.evaluate(n=>n.open),false,'Disclosure can be collapsed with keyboard');
  await page.setViewportSize({width:1280,height:1100});
  await club.screenshot({path:path.join(output,'1280-complete.png')});
  assert.deepEqual(errors,[]);
  console.log('PASS: all 243 paths, valid probabilities, manual choices, rebuilding with previous-name comparison, Undo, restart, keyboard focus, four viewport sizes, and no runtime errors.');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
