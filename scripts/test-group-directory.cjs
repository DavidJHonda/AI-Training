const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.join(__dirname, '..');
const context = {window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'group-activities-data.js'),'utf8'),context);
const activities = context.window.COURSE_GROUP_ACTIVITIES;
const html = fs.readFileSync(path.join(root,'index.html'),'utf8');
assert.equal(new Set(activities.map(a=>a.id)).size,activities.length);
for (const a of activities) {
 assert(a.lessonTitle && a.section && a.note);
 assert(['Activity','Discussion'].includes(a.type));
 assert(fs.existsSync(path.join(root,a.href.split('?')[0])),a.href);
 if(a.type==='Discussion') {
  // Preserve the approved question counts for shorter discussion sets.
  const approvedCounts = {'evaluating-discussion': 2, 'whydeeper': 4, 'aivscode': 4, 'aihistory-discussion': 3, 'doesaithink-discussion': 4, 'whybother': 4, 'whatitdoesbest': 4, 'modelselection-discussion': 3, 'prompt-discussion': 4, 'aitips-discussion': 4, 'aiismath-discussion': 4, 'training-discussion': 3, 'embeddings-discussion': 2, 'attention-discussion': 2, 'prediction-discussion': 2, 'documenttrap-discussion': 3, 'trainingbias-discussion': 4, 'mindtrap-discussion': 4, 'flattery-discussion': 4, 'whatpeoplesay-discussion': 4, 'paceofchange-discussion': 4, 'bigdownside-discussion': 4, 'bigupside-discussion': 4, 'workchanges-discussion': 4, 'computecost-discussion': 4, 'unexpected-discussion': 4, 'critical-discussion': 4, 'integrity-discussion': 4, 'wherestheline-discussion': 4, 'peopleskills-discussion': 4};
  assert.equal(a.questions.length,approvedCounts[a.id] ?? 5);
  assert(a.questions.every(q=>q.title));
  assert(html.includes('return a.id === "'+a.id+'"; }).questions'));
 }
}
const evaluationLesson = html.slice(html.indexOf('function EvaluatingSection('), html.indexOf('function CreativeThinkingCareerLab('));
assert(evaluationLesson.indexOf('E(DigDeeperTryIt, null)') < evaluationLesson.indexOf('id: "evaluating-discussion"'));
assert(evaluationLesson.indexOf('id: "evaluating-discussion"') < evaluationLesson.indexOf('E(NextLessonGate'));
const inlineLessons = [...html.matchAll(/id: "([a-z]+)-group-exercise"/g)].map(m=>m[1]);
for(const lesson of inlineLessons) assert(activities.some(a=>a.lesson===lesson),'Missing lesson '+lesson);
const standaloneFiles = [...html.matchAll(/href: "(group-exercises\/[^"?]+\.html)"/g)].map(m=>m[1]);
for(const href of standaloneFiles) assert(activities.some(a=>a.href===href),'Missing activity '+href);
assert(html.includes('var activities = window.COURSE_GROUP_ACTIVITIES;'));
console.log('PASS: shared directory covers '+activities.length+' activities/discussions; destinations exist and lesson questions share the same source.');

const navigation = html.slice(html.indexOf('const SECTION_GROUPS ='), html.indexOf('// Opener sections all share'));
const nav = vm.runInNewContext(navigation + '\n({groups: SECTION_GROUPS, required: REQUIRED_SECTIONS, optional: isOptionalLesson("forgroups")})');
assert(nav.optional);
assert.equal(nav.required.length,54);
assert(nav.groups.find(g=>g.label==='Finish Smarter').sections.includes('forgroups'));
console.log('PASS: For Groups is navigable under Finish Smarter and does not change the 54 required lessons.');
