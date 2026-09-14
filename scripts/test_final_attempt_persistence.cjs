const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const helpers = html.slice(
  html.indexOf('const FINAL_BANK ='),
  html.indexOf('function OpenerFoundationsSection')
);

function contextFor(storage) {
  const context = {
    localStorage: {
      getItem: key => storage.has(key) ? storage.get(key) : null,
      setItem: (key, value) => storage.set(key, String(value)),
      removeItem: key => storage.delete(key)
    },
    console
  };
  vm.createContext(context);
  vm.runInContext(helpers, context);
  return context;
}

const storage = new Map();
storage.set('final-exam', JSON.stringify({
  bestScore: 92, attempts: 2, certName: 'Alex Taylor',
  certFirstName: 'Alex', certLastName: 'Taylor',
  completionDate: '2026-08-20T15:30:00.000Z'
}));

let page = contextFor(storage);
vm.runInContext("saveFinalAttempt_(FINAL_BANK, {fx01: 1, fx12: 1}, '2026-09-14T18:00:00.000Z')", page);
let saved = JSON.parse(storage.get('final-exam-unfinished:v1'));
assert.equal(saved.version, 1);
assert.match(saved.bankSignature, /^bank-/);
assert.equal(saved.questionIds.length, 25);
assert.deepEqual(saved.answers, {fx01: 1, fx12: 1});

// A new page context sees the same valid attempt after refresh/navigation.
page = contextFor(storage);
let restored = vm.runInContext('loadFinalAttempt_()', page);
assert.equal(restored.questionIds.length, 25);
assert.equal(Object.keys(restored.answers).length, 2);
assert.equal(restored.startedAt, '2026-09-14T18:00:00.000Z');

// Invalid choices, changed question order, corrupt JSON, and old schema versions
// are discarded without touching the completed score/certificate record.
const completedBefore = storage.get('final-exam');
for (const bad of [
  {...saved, version: 0},
  {...saved, bankSignature: 'bank-outdated'},
  {...saved, questionIds: saved.questionIds.slice().reverse()},
  {...saved, answers: {fx01: 99}},
  {...saved, answers: {unknown: 0}}
]) {
  storage.set('final-exam-unfinished:v1', JSON.stringify(bad));
  assert.equal(vm.runInContext('loadFinalAttempt_()', page), null);
  assert.equal(storage.has('final-exam-unfinished:v1'), false);
  assert.equal(storage.get('final-exam'), completedBefore);
}
storage.set('final-exam-unfinished:v1', '{broken');
assert.equal(vm.runInContext('loadFinalAttempt_()', page), null);
assert.equal(storage.has('final-exam-unfinished:v1'), false);
assert.equal(storage.get('final-exam'), completedBefore);

// Clearing a submitted/abandoned attempt leaves earned results intact.
vm.runInContext("saveFinalAttempt_(FINAL_BANK, {fx25: 1})", page);
vm.runInContext('clearFinalAttempt_()', page);
assert.equal(storage.has('final-exam-unfinished:v1'), false);
assert.equal(storage.get('final-exam'), completedBefore);

const component = html.slice(html.indexOf('function TheFinalQuiz('), html.indexOf('function FinishLetter()'));
assert(component.includes('"Continue the Final"'));
assert(component.includes('"You’ve answered " + savedAnswerCount + " of " + FINAL_BANK.length + " questions."'));
assert(component.includes('"Start over"'));
assert(component.includes('"Try the Final on your own first. This is your chance to see what you know. If you miss something, review the explanation and lesson, then try again."'));
assert(component.includes('"You passed."'));
assert(component.includes('"You’ve earned your certificate. Put your name on it, then take a look at any questions you missed. You can take the Final again whenever you like. Your best score stays on record."'));
assert(component.includes('window.confirm("Start over and clear your unfinished Final answers?")'));
assert.match(component, /var finish = function\(\) \{[\s\S]*?clearFinalAttempt_\(\);[\s\S]*?setRecord/);
assert.match(component, /var pick = function\(qid, oi\) \{[\s\S]*?saveFinalAttempt_\(questions, next/);
assert.match(component, /var start = function\(\) \{[\s\S]*?saveFinalAttempt_\(freshQuestions, \{\}\)/);

// Stateful component check: start, answer, leave/recreate the component, resume,
// cancel and confirm reset, then submit the resumed attempt.
function finalClient(clientStorage, confirmResult = true) {
  const states = [];
  let cursor = 0;
  let navigatedTo = null;
  let scrolledTo = null;
  let focusedIn = null;
  const storageApi = {
    getItem: key => clientStorage.has(key) ? clientStorage.get(key) : null,
    setItem: (key, value) => clientStorage.set(key, String(value)),
    removeItem: key => clientStorage.delete(key)
  };
  const context = {
    React: {createElement: (type, props, ...children) => ({type, props: props || {}, children: children.flat(Infinity)})},
    useState(initial) {
      const i = cursor++;
      if (!(i in states)) states[i] = typeof initial === 'function' ? initial() : initial;
      return [states[i], value => { states[i] = typeof value === 'function' ? value(states[i]) : value; }];
    },
    useEffect() { cursor++; },
    useLocalStorage(key, initial) {
      const pair = context.useState(() => clientStorage.has(key) ? JSON.parse(clientStorage.get(key)) : initial);
      return [pair[0], value => {
        const next = typeof value === 'function' ? value(pair[0]) : value;
        pair[1](next);
        clientStorage.set(key, JSON.stringify(next));
      }];
    },
    localStorage: storageApi,
    sessionStorage: storageApi,
    window: {
      confirm: () => confirmResult,
      matchMedia: () => ({matches: true}),
      setTimeout: callback => callback()
    },
    document: {
      getElementById(id) {
        return {
          scrollIntoView() { scrolledTo = id; },
          focus() { focusedIn = id; },
          querySelector() { return {focus() { focusedIn = id; }}; }
        };
      }
    },
    getStudentProfile: () => ({studentId: 'student', firstName: 'Alex', country: 'Canada'}),
    saveStudentProfile() {}, reportCourseCompletion() {},
    SECTION_META: {},
    ActivityButton: 'ActivityButton', InnerCard: 'InnerCard'
  };
  vm.createContext(context);
  vm.runInContext(helpers, context);
  vm.runInContext(html.slice(html.indexOf('const FINAL_PASS_PCT ='), html.indexOf('function FinishLetter()')), context);
  const flatten = node => [node, ...(node && node.children ? node.children.flatMap(child => child && typeof child === 'object' ? flatten(child) : []) : [])];
  return {
    render() { cursor = 0; return flatten(context.TheFinalQuiz({onNavigate: id => { navigatedTo = id; }})); },
    print() { return context.CertificatePrintView(); },
    setConfirm(value) { confirmResult = value; },
    navigatedTo: () => navigatedTo,
    scrolledTo: () => scrolledTo,
    focusedIn: () => focusedIn
  };
}
const find = (ui, predicate) => {
  const match = ui.render().find(predicate);
  assert(match, 'Expected UI control was not rendered');
  return match;
};
const hasText = (node, text) => {
  const visit = value => typeof value === 'string' ? value === text : !!(value && value.children && value.children.some(visit));
  return visit(node);
};

const uiStorage = new Map([['final-exam', completedBefore]]);
let ui = finalClient(uiStorage);
find(ui, n => n.type === 'ActivityButton' && n.children.includes('Start the Final')).props.onClick();
const firstRadioGroup = find(ui, n => n.props && n.props.role === 'radiogroup');
assert.equal(firstRadioGroup.props['aria-labelledby'], 'final-question-label-fx01');
let firstFalse = find(ui, n => n.type === 'button' && hasText(n, 'False'));
assert.equal(firstFalse.props.role, 'radio');
assert.equal(firstFalse.props['aria-checked'], false);
assert.equal(firstFalse.props.tabIndex, -1);
firstFalse.props.onClick();
assert.equal(JSON.parse(uiStorage.get('final-exam-unfinished:v1')).answers.fx01, 1);
firstFalse = find(ui, n => n.type === 'button' && hasText(n, 'False'));
assert.equal(firstFalse.props['aria-checked'], true);
assert.equal(firstFalse.props.tabIndex, 0);
let preventedArrowDefault = false;
let focusedRadio = null;
firstFalse.props.onKeyDown({
  key: 'ArrowRight',
  preventDefault() { preventedArrowDefault = true; },
  currentTarget: {parentElement: {querySelectorAll: () => [
    {focus() { focusedRadio = 0; }},
    {focus() { focusedRadio = 1; }}
  ]}}
});
assert.equal(preventedArrowDefault, true);
assert.equal(focusedRadio, 0);
assert.equal(JSON.parse(uiStorage.get('final-exam-unfinished:v1')).answers.fx01, 0);
firstFalse.props.onClick(); // Restore the selection used by the persistence checks below.
assert.equal(JSON.parse(uiStorage.get('final-exam-unfinished:v1')).answers.fx01, 1);

ui = finalClient(uiStorage); // Leave the lesson/page and return.
assert(find(ui, n => n.children && n.children.includes('You’ve answered 1 of 25 questions.')));
find(ui, n => n.type === 'ActivityButton' && n.children.includes('Continue the Final')).props.onClick();
firstFalse = find(ui, n => n.type === 'button' && hasText(n, 'False'));
assert.equal(firstFalse.props.style.color, 'var(--tryAccent)');

ui = finalClient(uiStorage, false); // Cancel keeps the unfinished answers.
find(ui, n => n.type === 'button' && n.children.includes('Start over')).props.onClick();
assert.equal(JSON.parse(uiStorage.get('final-exam-unfinished:v1')).answers.fx01, 1);
ui.setConfirm(true);
find(ui, n => n.type === 'button' && n.children.includes('Start over')).props.onClick();
assert.deepEqual(JSON.parse(uiStorage.get('final-exam-unfinished:v1')).answers, {});
find(ui, n => n.type === 'ActivityButton' && n.children.includes('Submit the Final')).props.onClick();
assert(find(ui, n => n.children && n.children.includes('You have 25 unanswered questions.')));
assert.equal(uiStorage.has('final-exam-unfinished:v1'), true);
assert.equal(JSON.parse(uiStorage.get('final-exam')).attempts, 2);
find(ui, n => n.type === 'ActivityButton' && n.children.includes('Keep answering')).props.onClick();
assert.equal(ui.scrolledTo(), 'final-question-fx01');
assert.equal(ui.focusedIn(), 'final-question-fx01');
assert.equal(ui.render().some(n => n.children && n.children.includes('You have 25 unanswered questions.')), false);
find(ui, n => n.type === 'ActivityButton' && n.children.includes('Submit the Final')).props.onClick();
find(ui, n => n.type === 'button' && n.children.includes('Submit anyway')).props.onClick();
assert.equal(uiStorage.has('final-exam-unfinished:v1'), false);
assert.equal(uiStorage.has('final-exam-result:v1'), true);
const completedAfter = JSON.parse(uiStorage.get('final-exam'));
assert.equal(completedAfter.bestScore, 92);
assert.equal(completedAfter.attempts, 3);
assert.equal(completedAfter.certName, 'Alex Taylor');
assert.equal(completedAfter.certFirstName, 'Alex');
assert.equal(completedAfter.certLastName, 'Taylor');
assert.equal(completedAfter.completionDate, '2026-08-20T15:30:00.000Z');
let resultLinks = ui.render().filter(n => n.type === 'button' && String(n.props['aria-label'] || '').startsWith('Review lesson: '));
assert.equal(resultLinks.length, 25);
resultLinks[0].props.onClick();
assert.equal(ui.navigatedTo(), 'aihistory');

// Returning to the Final in the same tab restores the submitted result review.
ui = finalClient(uiStorage);
resultLinks = ui.render().filter(n => n.type === 'button' && String(n.props['aria-label'] || '').startsWith('Review lesson: '));
assert.equal(resultLinks.length, 25);
assert(ui.render().some(n => n.children && n.children.includes('0%')));

// A new attempt dismisses the prior detailed result while preserving its summary.
find(ui, n => n.type === 'ActivityButton' && n.children.includes('Take it again')).props.onClick();
assert.equal(uiStorage.has('final-exam-result:v1'), false);
assert.equal(JSON.parse(uiStorage.get('final-exam')).bestScore, 92);

// Wrong and unanswered items both count as missed. The filtered view keeps the
// original question numbers, and a perfect result defaults to all questions.
const correctAnswers = JSON.parse(vm.runInContext('JSON.stringify(Object.fromEntries(FINAL_BANK.map(q => [q.id, q.correct])))', page));

// A complete attempt still submits immediately; the confirmation is only for blanks.
const completeStorage = new Map();
completeStorage.set('final-exam-unfinished:v1', JSON.stringify({...saved, answers: correctAnswers}));
let completeUi = finalClient(completeStorage);
find(completeUi, n => n.type === 'ActivityButton' && n.children.includes('Continue the Final')).props.onClick();
find(completeUi, n => n.type === 'ActivityButton' && n.children.includes('Submit the Final')).props.onClick();
assert.equal(completeStorage.has('final-exam-unfinished:v1'), false);
assert.equal(JSON.parse(completeStorage.get('final-exam')).bestScore, 100);
assert.equal(completeUi.render().some(n => n.children && String(n.children.join('')).includes('unanswered question')), false);
assert.equal(completeUi.render().some(n => n.children && n.children.includes('Review missed questions')), false);

// A student who has not passed gets review and retry actions beside the score.
const failedStorage = new Map([['final-exam-result:v1', JSON.stringify({...saved, answers: {}})]]);
let failedUi = finalClient(failedStorage);
find(failedUi, n => n.type === 'ActivityButton' && n.children.includes('Review missed questions')).props.onClick();
assert.equal(failedUi.scrolledTo(), 'final-missed-review');
assert.equal(failedUi.focusedIn(), 'final-missed-review');
find(failedUi, n => n.type === 'button' && n.children.includes('Take it again')).props.onClick();
assert.equal(failedStorage.has('final-exam-result:v1'), false);
assert.equal(failedStorage.has('final-exam-unfinished:v1'), true);

// The first passing attempt fixes the completion date. Certificate name edits and
// later lower retakes preserve it. A legacy printable certificate gets one fixed date.
const firstPassAnswers = Object.fromEntries(Object.entries(correctAnswers).slice(0, 20));
const firstPassStorage = new Map();
firstPassStorage.set('final-exam-unfinished:v1', JSON.stringify({...saved, answers: firstPassAnswers}));
let passUi = finalClient(firstPassStorage);
find(passUi, n => n.type === 'ActivityButton' && n.children.includes('Continue the Final')).props.onClick();
find(passUi, n => n.type === 'ActivityButton' && n.children.includes('Submit the Final')).props.onClick();
assert(find(passUi, n => n.children && n.children.includes('You have 5 unanswered questions.')));
find(passUi, n => n.type === 'button' && n.children.includes('Submit anyway')).props.onClick();
let passingRecord = JSON.parse(firstPassStorage.get('final-exam'));
assert.equal(passingRecord.bestScore, 80);
assert(Number.isFinite(Date.parse(passingRecord.completionDate)));
const firstCompletionDate = passingRecord.completionDate;
const certificate = find(passUi, n => typeof n.type === 'function' && n.type.name === 'CertificateBlock');
certificate.props.onSaveName('Jamie', 'Student');
passingRecord = JSON.parse(firstPassStorage.get('final-exam'));
assert.equal(passingRecord.completionDate, firstCompletionDate);
find(passUi, n => n.type === 'ActivityButton' && n.children.includes('Take it again')).props.onClick();
find(passUi, n => n.type === 'ActivityButton' && n.children.includes('Submit the Final')).props.onClick();
find(passUi, n => n.type === 'button' && n.children.includes('Submit anyway')).props.onClick();
assert.equal(JSON.parse(firstPassStorage.get('final-exam')).completionDate, firstCompletionDate);

const legacyStorage = new Map([['final-exam', JSON.stringify({
  bestScore: 88, attempts: 1, certName: 'Legacy Student',
  certFirstName: 'Legacy', certLastName: 'Student'
})]]);
finalClient(legacyStorage).print();
const migratedLegacyDate = JSON.parse(legacyStorage.get('final-exam')).completionDate;
assert(Number.isFinite(Date.parse(migratedLegacyDate)));

const threeMissed = {...correctAnswers, fx23: correctAnswers.fx23 === 0 ? 1 : 0, fx24: correctAnswers.fx24 === 0 ? 1 : 0};
delete threeMissed.fx25;
uiStorage.set('final-exam-result:v1', JSON.stringify({...saved, answers: threeMissed}));
ui = finalClient(uiStorage);
let missedToggle = find(ui, n => n.type === 'button' && n.children.includes('Missed questions (3)'));
assert.equal(missedToggle.props['aria-pressed'], true);
assert.equal(ui.render().filter(n => n.type === 'button' && String(n.props['aria-label'] || '').startsWith('Review lesson: ')).length, 3);
assert(ui.render().some(n => n.type === 'div' && n.children.includes('23')));
assert(ui.render().some(n => n.type === 'div' && n.children.includes('24')));
assert(ui.render().some(n => n.type === 'div' && n.children.includes('25')));
find(ui, n => n.type === 'button' && n.children.includes('All questions (25)')).props.onClick();
assert.equal(ui.render().filter(n => n.type === 'button' && String(n.props['aria-label'] || '').startsWith('Review lesson: ')).length, 25);

uiStorage.set('final-exam-result:v1', JSON.stringify({...saved, answers: correctAnswers}));
ui = finalClient(uiStorage);
missedToggle = find(ui, n => n.type === 'button' && n.children.includes('Missed questions (0)'));
assert.equal(missedToggle.props.disabled, true);
assert.equal(find(ui, n => n.type === 'button' && n.children.includes('All questions (25)')).props['aria-pressed'], true);
assert.equal(ui.render().filter(n => n.type === 'button' && String(n.props['aria-label'] || '').startsWith('Review lesson: ')).length, 25);

console.log('PASS: Final drafts/results and certificate dates persist; filters, resets, retakes, name edits, and lesson links behave correctly');
