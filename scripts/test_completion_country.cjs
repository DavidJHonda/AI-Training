const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.join(__dirname, '..');
const backend = fs.readFileSync(path.join(root, 'google-apps-script.gs'), 'utf8');
const frontend = fs.readFileSync(path.join(root, 'index.html'), 'utf8');

class Sheet {
  constructor(name, rows = []) { this.name = name; this.rows = rows.map(row => row.slice()); this.columns = Math.max(8, ...this.rows.map(row => row.length)); }
  appendRow(row) { this.rows.push(Array.from(row)); this.columns = Math.max(this.columns, row.length); }
  setFrozenRows() {}
  setName(name) { this.name = name; return this; }
  getLastRow() { return this.rows.length; }
  getLastColumn() { return Math.max(0, ...this.rows.map(row => row.length)); }
  getMaxColumns() { return this.columns; }
  insertColumnAfter(column) { this.rows.forEach(row => row.splice(column, 0, '')); this.columns++; }
  deleteColumns(column, count) { this.rows.forEach(row => row.splice(column - 1, count)); this.columns -= count; }
  copyTo(spreadsheet) { const copy = new Sheet(this.name + ' copy', this.rows); spreadsheet.sheets.push(copy); return copy; }
  getRange(row, column, height = 1, width = 1) {
    return {
      getValues: () => Array.from({length: height}, (_, i) => Array.from({length: width}, (_, j) => this.rows[row - 1 + i]?.[column - 1 + j] ?? '')),
      setValues: values => values.forEach((valuesRow, i) => valuesRow.forEach((value, j) => {
        this.rows[row - 1 + i] ||= [];
        this.rows[row - 1 + i][column - 1 + j] = value;
      })),
      createTextFinder: value => ({
        matchEntireCell() { return this; },
        findNext: () => {
          const offset = this.rows.slice(row - 1, row - 1 + height).findIndex(r => r[column - 1] === value);
          return offset < 0 ? null : {getRow: () => row + offset};
        }
      })
    };
  }
}

const oldHeaders = ['Completed At', 'Student ID', 'First Name', 'Last Name', 'City', 'State', 'Final Score', 'Completion ID', 'Course Version'];
const targetHeaders = ['Completed At', 'Student ID', 'First Name', 'Last Name', 'Country', 'Final Score', 'Completion ID', 'Course Version'];
function fixture(completionRows) {
  const enrollment = new Sheet('Enrollment', [['Timestamp', 'First Name', 'Student ID', 'Country']]);
  const completion = completionRows === null ? null : new Sheet('Course Completions', completionRows);
  const sheets = completion ? [enrollment, completion] : [enrollment];
  const emails = [];
  let locked = false;
  const spreadsheet = {
    sheets,
    getSheets() { return this.sheets; },
    getSheetByName(name) { return this.sheets.find(sheet => sheet.name === name) || null; },
    insertSheet(name) { const sheet = new Sheet(name); this.sheets.push(sheet); return sheet; }
  };
  const server = {
    console: {error() {}, log() {}},
    SpreadsheetApp: {getActiveSpreadsheet: () => spreadsheet, flush() { assert(locked); }},
    MailApp: {sendEmail: (...args) => { assert(locked); emails.push(args); }},
    ContentService: {MimeType: {TEXT: 'text'}, createTextOutput: text => ({setMimeType: () => text})},
    LockService: {getScriptLock: () => ({waitLock() { assert(!locked); locked = true; }, releaseLock() { locked = false; }})}
  };
  vm.createContext(server);
  vm.runInContext(backend, server);
  return {
    spreadsheet, emails,
    sheet: () => spreadsheet.getSheetByName('Course Completions'),
    post: data => server.doPost({postData: {contents: JSON.stringify(data)}}),
    migrate: () => server.migrateCompletionSheet()
  };
}

const base = {eventType:'course_completed',completionPayloadVersion:2,completionId:'student:v1',studentId:'student',firstName:'Alex',lastName:'Taylor',country:'United States',score:88,courseVersion:'v1'};

// A new installation starts directly in the compact layout.
let f = fixture(null);
assert.equal(f.post(base), 'completion-ok');
assert.deepEqual(f.sheet().rows[0], targetHeaders);
assert.deepEqual(f.sheet().rows[1].slice(1), ['student','Alex','Taylor','United States',88,'student:v1','v1']);
assert(f.emails[0][2].includes('Country: United States'));
const submittedAt = f.sheet().rows[1][0];
assert.equal(f.post(base), 'completion-ok');
assert.equal(f.sheet().rows.length, 2);
assert.equal(f.emails.length, 1);

// An existing but empty tab is initialized rather than rejected as malformed.
let empty = fixture([]);
assert.equal(empty.migrate(), 'Initialized the empty Course Completions sheet.');
assert.deepEqual(empty.sheet().rows[0], targetHeaders);

// A country refresh and certificate-name correction update the same row without
// changing completion date, score, ID, or version. A blank legacy retry cannot erase Country.
assert.equal(f.post({...base,country:'Canada'}), 'completion-ok');
assert.equal(f.sheet().rows[1][4], 'Canada');
assert.equal(f.emails.length, 1);
assert.equal(f.post({...base,firstName:'Alexa',country:'Canada',score:99,courseVersion:'v2'}), 'completion-ok');
assert.equal(f.sheet().rows.length, 2);
assert.equal(f.sheet().rows[1][0], submittedAt);
assert.deepEqual(f.sheet().rows[1].slice(1), ['student','Alexa','Taylor','Canada',88,'student:v1','v1']);
assert.equal(f.emails.length, 2);
assert.equal(f.post({...base,firstName:'Alexa',country:''}), 'completion-ok');
assert.equal(f.sheet().rows[1][4], 'Canada');

// Validation occurs before a row is appended.
for (const invalid of [{...base,completionId:'low',score:79},{...base,completionId:'bad-country',country:'Atlantis'},{...base,completionId:'no-last',lastName:''}]) {
  const before = JSON.stringify(f.sheet().rows);
  assert.equal(f.post(invalid), 'error');
  assert.equal(JSON.stringify(f.sheet().rows), before);
}

// Existing City/State rows remain readable during the deploy-before-migrate window.
const historicalDate = new Date('2026-08-01T12:00:00Z');
const historical = [historicalDate,'old-student','Old','Name','Dallas','Texas',84,'old:v1','v1'];
f = fixture([oldHeaders, historical]);
assert.equal(f.post(base), 'completion-ok');
assert.deepEqual(f.sheet().rows[0], ['Completed At','Student ID','First Name','Last Name','City','State','Country','Final Score','Completion ID','Course Version']);
assert.deepEqual(f.sheet().rows[1], [historicalDate,'old-student','Old','Name','Dallas','Texas','',84,'old:v1','v1']);
assert.equal(f.sheet().rows[2][6], 'United States');

// Migration creates a full backup, deletes only City/State, and preserves every
// completion date, certificate name, score, ID, version, and recorded Country.
const beforeMigration = f.sheet().rows.map(row => row.slice());
const message = f.migrate();
assert(message.startsWith('Course Completions cleaned up. Historical data is preserved in Course Completions backup '));
assert.equal(f.spreadsheet.sheets.length, 3);
const backup = f.spreadsheet.sheets[2];
assert.deepEqual(backup.rows, beforeMigration);
assert(backup.name.startsWith('Course Completions backup '));
assert.deepEqual(f.sheet().rows[0], targetHeaders);
assert.deepEqual(f.sheet().rows[1], [historicalDate,'old-student','Old','Name','',84,'old:v1','v1']);
assert.deepEqual(f.sheet().rows[2].slice(1), ['student','Alex','Taylor','United States',88,'student:v1','v1']);
const cleanRows = JSON.stringify(f.sheet().rows);
assert.equal(f.migrate(), 'Course Completions is already clean. No columns removed.');
assert.equal(f.spreadsheet.sheets.length, 3);
assert.equal(JSON.stringify(f.sheet().rows), cleanRows);

// A failed backup leaves the live sheet exactly as it was.
f = fixture([oldHeaders, historical]);
f.sheet().copyTo = () => { throw new Error('Backup unavailable'); };
const beforeFailure = JSON.stringify(f.sheet().rows);
assert.throws(() => f.migrate(), /Backup unavailable/);
assert.equal(JSON.stringify(f.sheet().rows), beforeFailure);

// Malformed headers fail safely before any write.
f = fixture([oldHeaders.map(header => header === 'Completion ID' ? 'Certificate ID' : header), historical]);
const beforeInvalidLayout = JSON.stringify(f.sheet().rows);
assert.equal(f.post(base), 'error');
assert.equal(JSON.stringify(f.sheet().rows), beforeInvalidLayout);
assert.throws(() => f.migrate(), /supported layout/);

// The previous no-last-name schema still receives a Last Name and Country safely.
const veryOldHeaders = ['Completed At','Student ID','First Name','City','State','Final Score','Completion ID','Course Version'];
const veryOld = [historicalDate,'old-student','Old','Dallas','Texas',84,'old:v1','v1'];
f = fixture([veryOldHeaders,veryOld]);
assert.equal(f.post(base),'completion-ok');
assert.deepEqual(f.sheet().rows[0], ['Completed At','Student ID','First Name','Last Name','City','State','Country','Final Score','Completion ID','Course Version']);
assert.deepEqual(f.sheet().rows[1], [historicalDate,'old-student','Old','','Dallas','Texas','',84,'old:v1','v1']);

// If an old retry is already in flight, a newer v2 payload must retain and send
// Country rather than being cleared by the first response.
(async () => {
  const completionClient = frontend.slice(
    frontend.indexOf('const SIGNUP_ENDPOINT'),
    frontend.indexOf('function getOrCreateReviewId')
  );
  const storage = new Map();
  const requests = [];
  const client = {
    localStorage: {
      getItem: key => storage.has(key) ? storage.get(key) : null,
      setItem: (key, value) => storage.set(key, String(value)),
      removeItem: key => storage.delete(key)
    },
    crypto: {randomUUID: () => 'generated-id'},
    fetch: (_url, options) => new Promise(resolve => {
      requests.push({payload: JSON.parse(options.body), resolve});
    }),
    console
  };
  vm.createContext(client);
  vm.runInContext(completionClient, client);
  storage.set('llm-student-profile', JSON.stringify({
    studentId: 'student', firstName: 'Alex', lastName: 'Taylor', country: 'Canada'
  }));
  storage.set('llm-completion-pending', JSON.stringify({
    eventType: 'course_completed', completionId: 'student:bstt-course-v1',
    reportKey: 'legacy-report-key', studentId: 'student', firstName: 'Alex',
    lastName: 'Taylor', score: 88
  }));
  client.retryPendingCompletionReport();
  assert.equal(requests.length, 1);
  client.reportCourseCompletion(88, 'Alex', 'Taylor');
  const queued = JSON.parse(storage.get('llm-completion-pending'));
  assert.equal(queued.completionPayloadVersion, 2);
  assert.equal(queued.country, 'Canada');
  requests[0].resolve({text: async () => 'completion-ok'});
  await new Promise(resolve => setImmediate(resolve));
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(requests.length, 2);
  assert.equal(requests[1].payload.reportKey, queued.reportKey);
  assert.equal(requests[1].payload.country, 'Canada');
  requests[1].resolve({text: async () => 'completion-ok'});
  await new Promise(resolve => setImmediate(resolve));
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(storage.has('llm-completion-pending'), false);
  assert.equal(storage.get('llm-completion-reported'), queued.reportKey);

  console.log('PASS: completion Country, compact/legacy layouts, backup migration, names, IDs, scores, retries and validation');
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
