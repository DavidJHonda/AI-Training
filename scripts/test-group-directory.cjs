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
  assert.equal(a.questions.length,5);
  assert(a.questions.every(q=>q.title));
  assert(html.includes('return a.id === "'+a.id+'"; }).questions'));
 }
}
const inlineLessons = [...html.matchAll(/id: "([a-z]+)-group-exercise"/g)].map(m=>m[1]);
for(const lesson of inlineLessons) assert(activities.some(a=>a.lesson===lesson),'Missing lesson '+lesson);
const standaloneFiles = [...html.matchAll(/href: "(group-exercises\/[^"?]+\.html)"/g)].map(m=>m[1]);
for(const href of standaloneFiles) assert(activities.some(a=>a.href===href),'Missing activity '+href);
assert(html.includes('var activities = window.COURSE_GROUP_ACTIVITIES;'));
console.log('PASS: shared directory covers '+activities.length+' activities/discussions; destinations exist and lesson questions share the same source.');

const navigation = html.slice(html.indexOf('const SECTION_GROUPS ='), html.indexOf('// Opener sections all share'));
const nav = vm.runInNewContext(navigation + '\n({groups: SECTION_GROUPS, required: REQUIRED_SECTIONS, optional: isOptionalLesson("forgroups")})');
assert(nav.optional);
assert.equal(nav.required.length,58);
assert(nav.groups.find(g=>g.label==='Finish Smarter').sections.includes('forgroups'));
console.log('PASS: For Groups is navigable under Finish Smarter and does not change the 58 required lessons.');
