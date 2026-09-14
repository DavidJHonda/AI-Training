const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.join(__dirname, '..');
const backend = fs.readFileSync(path.join(root, 'google-apps-script.gs'), 'utf8');
const countries = {};
vm.runInNewContext(fs.readFileSync(path.join(root, 'country-select.js'), 'utf8'), countries);
const names = Array.from(countries.COURSE_COUNTRIES);
assert.equal(names.length, 249);
assert.equal(names[0], 'United States');
assert.equal(new Set(names).size, names.length);
assert.deepEqual(names.slice(1), names.slice(1).sort((a, b) => a.localeCompare(b, 'en')));

class Sheet {
  constructor(rows = []) { this.rows = rows.map(row => row.slice()); this.columns = Math.max(7, ...this.rows.map(row => row.length)); }
  appendRow(row) { this.rows.push(Array.from(row)); this.columns = Math.max(this.columns, row.length); }
  getLastRow() { return this.rows.length; }
  getLastColumn() { return Math.max(0, ...this.rows.map(row => row.length)); }
  getMaxColumns() { return this.columns; }
  insertColumnAfter(column) { assert.equal(column, this.columns); this.columns++; }
  deleteColumns(column, count) { this.rows.forEach(row => row.splice(column - 1, count)); this.columns -= count; }
  copyTo(spreadsheet) { const copy = new Sheet(this.rows); spreadsheet.sheets.push(copy); return copy; }
  setName(name) { this.name = name; return this; }
  getRange(row, column, height = 1, width = 1) {
    return {
      getValues: () => Array.from({length: height}, (_, i) => Array.from({length: width}, (_, j) => this.rows[row - 1 + i]?.[column - 1 + j] ?? '')),
      setValues: values => values.forEach((valuesRow, i) => valuesRow.forEach((value, j) => {
        this.rows[row - 1 + i] ||= [];
        this.rows[row - 1 + i][column - 1 + j] = value;
      }))
    };
  }
}
const headers = ['Date', 'First Name', 'Last Name', 'Email', 'City', 'State', 'Student ID'];
const historical = ['2025-01-01', 'Old', 'Student', '', 'Dallas', 'Texas', 'old-id'];
function fixture(rows) {
  const sheet = new Sheet(rows), emails = [];
  const spreadsheet = {sheets: [sheet], getSheets() { return this.sheets; }};
  let locked = false;
  const server = {
    console: {error() {}, log() {}},
    SpreadsheetApp: {getActiveSpreadsheet: () => spreadsheet, flush() { assert(locked); }},
    MailApp: {sendEmail: (...args) => { assert(!locked); emails.push(args); }},
    ContentService: {MimeType: {TEXT: 'text'}, createTextOutput: text => ({setMimeType: () => text})},
    LockService: {getScriptLock: () => ({waitLock() { assert(!locked); locked = true; }, releaseLock() { locked = false; }})}
  };
  vm.createContext(server);
  vm.runInContext(backend, server);
  assert.deepEqual(Array.from(server.COURSE_COUNTRIES), names);
  return {sheet, emails, spreadsheet, migrate: () => server.migrateEnrollmentSheet(), post: data => server.doPost({postData: {contents: JSON.stringify(data)}})};
}
const base = {eventType: 'enrollment', registrationVersion: 2, firstName: 'Nick', studentId: 'new-id', country: 'United States'};
let f = fixture([headers, historical]);
assert.equal(f.post(base), 'ok');
assert.deepEqual(f.sheet.rows[0], headers.concat('Country'));
assert.deepEqual(f.sheet.rows[1], historical);
assert.deepEqual(f.sheet.rows[2].slice(1), ['Nick', '', '', '', '', 'new-id', 'United States']);
assert(f.emails[0][2].includes('United States'));
assert.equal(f.post({...base, country: 'Canada', studentId: 'other'}), 'ok');
assert.equal(f.sheet.rows[0].filter(x => x === 'Country').length, 1);
for (const data of [{...base, country: ''}, {...base, country: 'Atlantis'}, {...base, country: '=1+1'}, {...base, firstName: '  '}]) {
  const before = JSON.stringify(f.sheet.rows);
  assert.equal(f.post(data), 'error');
  assert.equal(JSON.stringify(f.sheet.rows), before);
}
// Old queued signups remain accepted; obsolete fields are no longer collected.
assert.equal(f.post({firstName: 'Legacy', city: 'Austin', state: 'Texas', studentId: 'legacy'}), 'ok');
assert.deepEqual(f.sheet.rows.at(-1).slice(4), ['', '', 'legacy', '']);
// Existing additional columns are kept, with Country appended after them.
f = fixture([headers.concat('Notes'), historical.concat('Keep this note')]);
assert.equal(f.post(base), 'ok');
assert.equal(f.sheet.rows[0][7], 'Notes');
assert.equal(f.sheet.rows[0][8], 'Country');
assert.equal(f.sheet.rows[1][7], 'Keep this note');
assert.deepEqual(f.sheet.rows[2].slice(7), ['', 'United States']);
// Reuse an existing dedicated Country column, even with later custom columns.
f = fixture([headers.concat('Country', 'Notes'), historical.concat('Canada', 'Keep')]);
assert.equal(f.post(base), 'ok');
assert.equal(f.sheet.rows[0].length, 9);
assert.deepEqual(f.sheet.rows[1].slice(7), ['Canada', 'Keep']);
assert.equal(f.sheet.rows[2][7], 'United States');
// Reject destructive/manual header changes before any writes.
for (const badHeaders of [headers.map(h => h === 'First Name' ? 'Country' : h), headers.concat('Country', 'Country'), headers.map(h => h === 'Student ID' ? 'Notes' : h)]) {
  f = fixture([badHeaders, historical]);
  const before = JSON.stringify(f.sheet.rows);
  assert.equal(f.post(base), 'error');
  assert.equal(JSON.stringify(f.sheet.rows), before);
}
f = fixture([]);
assert.equal(f.post(base), 'ok');
assert.deepEqual(f.sheet.rows[0], ['Timestamp', 'First Name', 'Student ID', 'Country']);
assert.deepEqual(f.sheet.rows[1].slice(1), ['Nick', 'new-id', 'United States']);

// Reproduce the screenshot's misleading G heading; keep UUIDs intact.
const screenshotHeaders = ['Timestamp', 'First Name', 'Last Name', 'Email', 'City', 'State', 'Certificate?'];
f = fixture([screenshotHeaders, historical]);
assert.equal(f.post(base), 'ok');
assert.equal(f.sheet.rows[0][6], 'Student ID');
assert.equal(f.sheet.rows[2][7], 'United States');
assert.deepEqual(f.sheet.rows[1], historical);

// One-time migration backs up the exact old layout, then removes only retired columns.
f = fixture([screenshotHeaders, historical]);
f.migrate();
assert.equal(f.spreadsheet.sheets.length, 2);
const backup = f.spreadsheet.sheets[1];
assert.deepEqual(backup.rows, [screenshotHeaders, historical]);
assert(backup.name.startsWith('Enrollment backup '));
assert.deepEqual(f.sheet.rows[0], ['Timestamp', 'First Name', 'Student ID', 'Country']);
assert.deepEqual(f.sheet.rows[1], [historical[0], historical[1], historical[6]]);
assert.equal(f.post(base), 'ok');
assert.deepEqual(f.sheet.rows[2].slice(1), ['Nick', 'new-id', 'United States']);
const cleanRows = JSON.stringify(f.sheet.rows);
f.migrate();
assert.equal(f.spreadsheet.sheets.length, 2); // Safe to run twice.
assert.equal(JSON.stringify(f.sheet.rows), cleanRows);
// A preexisting Country and unrelated custom column survive cleanup.
f = fixture([headers.concat('Country', 'Notes'), historical.concat('Canada', 'Keep')]);
f.migrate();
assert.deepEqual(f.sheet.rows[0], ['Timestamp', 'First Name', 'Student ID', 'Country', 'Notes']);
assert.deepEqual(f.sheet.rows[1], [historical[0], historical[1], historical[6], 'Canada', 'Keep']);
assert.equal(f.post(base), 'ok');
assert.deepEqual(f.sheet.rows[2].slice(1), ['Nick', 'new-id', 'United States', '']);
// Never remove historical data if the backup cannot be created.
f = fixture([screenshotHeaders, historical]);
f.sheet.copyTo = () => { throw new Error('Backup unavailable'); };
assert.throws(() => f.migrate(), /Backup unavailable/);
assert.deepEqual(f.sheet.rows, [screenshotHeaders, historical]);

// Local profile updates from certificate naming preserve country and older city/state.
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
for (const script of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)) if (script[1].trim()) new vm.Script(script[1]);
const storage = new Map();
const profileContext = {
  STUDENT_PROFILE_KEY: 'profile',
  localStorage: {getItem: key => storage.get(key) || null, setItem: (key, value) => storage.set(key, value)}
};
vm.createContext(profileContext);
vm.runInContext(html.slice(html.indexOf('function saveStudentProfile('), html.indexOf('function getStudentProfile(')), profileContext);
profileContext.saveStudentProfile({studentId: 'id', firstName: 'Nick', city: 'Dallas', state: 'Texas', country: 'United States'});
profileContext.saveStudentProfile({studentId: 'id', firstName: 'Full', lastName: 'Name'});
assert.deepEqual(JSON.parse(storage.get('profile')), {studentId:'id',firstName:'Full',lastName:'Name',city:'Dallas',state:'Texas',country:'United States'});
console.log('PASS: country list, validation, column migration, historical rows, legacy enrollment and profile preservation');
