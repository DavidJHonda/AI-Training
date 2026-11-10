// Verify all authored paths and the learner's choose / undo / restart flow.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const {chromium}=require('playwright');
const html=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
const context={};
vm.runInNewContext(html.slice(html.indexOf('var AI_CLUB_BRANCHES ='),html.indexOf('function PredictionLoopTryIt(')),context);
let leaves=0;
function walk(tokens){
 const options=context.aiClubChoices(tokens);
 if(tokens.length===5){assert.equal(options.length,0);leaves++;return;}
 assert.equal(options.length,3,'Every unfinished path offers three choices');
 assert.equal(options.reduce((sum,o)=>sum+o.probability,0),100);
 assert.equal(new Set(options.map(o=>o.token)).size,3);
 for(const option of options){assert.match(option.token,/^\S+$/);walk(tokens.concat(option.token));}
}
walk([]);
assert.equal(leaves,243);
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
   localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'prediction',visited:['prediction'],completed:[]}));
  });
  await page.goto(base+'/index.html',{waitUntil:'domcontentloaded'});
  const club=page.locator('.club-builder');await club.waitFor();
  fs.mkdirSync(output,{recursive:true});
  const choose=async token=>{await club.getByRole('button',{name:new RegExp('^'+token+', \\d+ percent$')}).click();};
  const choices=()=>club.locator('.club-builder-word').allTextContents();
  const answer=()=>club.locator('.club-builder-answer').innerText();
  const restart=()=>club.getByRole('button',{name:'Try Another Direction',exact:true}).click();
  assert.deepEqual(await choices(),['The','Humans','Less']);
  assert.equal(await club.getByRole('button',{name:'Undo',exact:true}).isDisabled(),true);
  // Compare different starts, then different continuations of the same start.
  await choose('The');assert.deepEqual(await choices(),['League','Robots','Curious']);
  await choose('League');assert.deepEqual(await choices(),['of','for','Exploring']);
  await club.getByRole('button',{name:'Undo',exact:true}).click();
  assert.equal(await answer(),'The');
  await choose('Robots');assert.deepEqual(await choices(),['Ate','Stole','Did']);
  await choose('Ate');await choose('My');await choose('Homework');
  assert.equal(await answer(),'The Robots Ate My Homework');
  assert.equal(await club.locator('.club-builder-choice').count(),0,'Stops at five words');
  assert.equal(await club.getByRole('button',{name:'Try Another Direction'}).evaluate(n=>n===document.activeElement),true);
  await club.getByRole('button',{name:'Undo',exact:true}).click();
  assert.equal(await answer(),'The Robots Ate My');
  assert.deepEqual(await choices(),['Homework','Lunch','Notes']);
  await choose('Lunch');await restart();
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
  }
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
  await page.setViewportSize({width:1280,height:1100});
  await club.screenshot({path:path.join(output,'1280-complete.png')});
  assert.deepEqual(errors,[]);
  console.log('PASS: all 243 five-word paths, changing branches, examples, Undo, restart, keyboard focus, four viewport sizes, and no runtime errors.');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
