const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const source = html.slice(html.indexOf('function HallucinationSection('), html.indexOf('function CriticalThinkingSection('));
const componentNames = ['LessonHeader','BodyP','SectionKicker','InteractiveBox','DinoGameDemo',
  'ActivityCounter','CopyableLabPrompt','LessonRule','NextLessonGate'];
const context = {
  React: {createElement: (type,props,...children) => ({type,props:props||{},children:children.flat(Infinity)})},
  useState: initial => [initial,()=>{}],
  closeBoard: id => ({type:'closeBoard',props:{id},children:[]}),
  BOX_CARD_TITLE:24, BOX_TEXT:20,
  ...Object.fromEntries(componentNames.map(name=>[name,name])),
};
vm.createContext(context);
vm.runInContext(source,context);
const tree=context.HallucinationSection({});
const children=tree.children;
const position=children.findIndex(n=>n.props?.src==='illustrations/hallucination-check-claim-v1.jpg');
assert.ok(position>0);
assert.equal(children[position+1].props.className,'md-source');
assert.equal(children[position+2].type,'closeBoard');
const json=JSON.stringify(children[position+1]);
for (const title of ['Notice the Claim.','Find the Source.','Check the Match.']) assert.ok(json.includes(title));
assert.ok(!json.includes('\u2014'));
const page=fs.readFileSync(path.join(root,'illustrations/hallucination-check-claim-v1.jpg'));
const prep=fs.readFileSync(path.join(root,'lessons/hallucination-4-check-claim.jpg'));
assert.ok(page.equals(prep),'Page and prep boards must be byte-identical');
const prompt=fs.readFileSync(path.join(root,'Prompts/hallucination-video-prompt.txt'),'utf8');
assert.ok(prompt.trim().split(/\s+/).length<=500);
for (const file of prompt.matchAll(/`(hallucination-[^`]+\.jpg)`/g)) {
  assert.ok(fs.existsSync(path.join(root,'lessons',file[1])),file[1]);
}
assert.ok(fs.readFileSync(path.join(root,'lessons/hallucination.md'),'utf8').includes('### Check the Claim'));
console.log('PASS: lesson renders, board precedes close, export copy matches, no em dash, identical assets, prompt under 500 words.');
