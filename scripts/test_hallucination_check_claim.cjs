const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const source = html.slice(html.indexOf('function HallucinationSection('), html.indexOf('function CriticalThinkingSection('));
const componentNames = ['LessonHeader','LessonReading','BodyP','PhoneReadingBoard','SixthPhoneReadingBoard',
  'HallucinationQuiz','GroupExercise','DiscussionQuestions','LessonRule','NextLessonGate'];
const context = {
  React: {createElement: (type,props,...children) => ({type,props:props||{},children:children.flat(Infinity)})},
  PHONE_READING_BOARDS: {hallucinationExample:{cards:[]}},
  window: {COURSE_GROUP_ACTIVITIES:[{id:'hallucination-discussion',questions:[]}]},
  closeBoard: id => ({type:'closeBoard',props:{id},children:[]}),
  BOX_CARD_TITLE:24, BOX_TEXT:20,
  ...Object.fromEntries(componentNames.map(name=>[name,name])),
};
vm.createContext(context);
vm.runInContext(source,context);
const tree=context.HallucinationSection({});
const children=tree.children.find(n=>n.type==='LessonReading').children;
const position=children.findIndex(n=>n.props?.kind==='hallucinationCheck');
assert.ok(position>0);
const board=children[position].props.image.props;
const title='Suspect a Hallucination?';
assert.ok(board.alt.startsWith(title));
assert.ok(fs.existsSync(path.join(root,board.src)));
const study=children[position-2];
assert.equal(study.type,'BodyP');
assert.equal(study.children.length,1);
assert.ok(study.children[0].includes('In one third-party study'));
const transition=children[position-1];
assert.equal(transition.type,'BodyP');
assert.ok(transition.children.join('').endsWith('The skill is noticing when something does not add up.'));
assert.equal(children[position+1].props.className,'md-source');
assert.equal(children[position+1].children[0].children[0],title);
assert.equal(children[position+2].type,'closeBoard');
const json=JSON.stringify(children[position+1]);
for (const title of ['Notice the Claim.','Find the Source.','Check the Match.']) assert.ok(json.includes(title));
assert.ok(!json.includes('\u2014'));
const registry=JSON.parse(fs.readFileSync(path.join(root,'gemini-notebook/upload-sets.json'),'utf8'));
const kit=registry.lessons.find(lesson=>lesson.slug==='hallucination');
if (kit) {
  const prompt=fs.readFileSync(path.join(root,kit.prompt),'utf8');
  assert.ok(prompt.trim().split(/\s+/).length<=500);
  for (const file of prompt.matchAll(/`(hallucination-[^`]+\.jpg)`/g)) {
    assert.ok(fs.existsSync(path.join(root,'course-assets/hallucination',file[1])),file[1]);
  }
} else {
  assert.ok(registry.needs_preparation.some(lesson=>lesson.slug==='hallucination'));
  assert.ok(!fs.existsSync(path.join(root,'gemini-notebook/hallucination/PROMPT.txt')));
}
const markdown=fs.readFileSync(path.join(root,'lessons/hallucination.md'),'utf8');
assert.ok(markdown.includes([study.children[0],transition.children[0],'### Board 3: '+title].join('\n\n')));
assert.ok(markdown.includes('!['+title+'](../'+board.src+')'));
console.log('PASS: the study paragraph precedes the board in the lesson and Markdown.');
