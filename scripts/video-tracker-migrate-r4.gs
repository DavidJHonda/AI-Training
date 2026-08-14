/**
 * migrateToR4 — one-shot gate-column migration for the
 * "AI-Training — Video Tracker" sheet.
 *
 * Rubric r4 keeps every r3 numeric score unchanged and adds four
 * review outcomes:
 *   - Source QA
 *   - Accuracy Gate
 *   - Substitute Gate
 *   - Board Walk Gate
 *
 * Run ONCE after migrateToR3. The function is idempotent and preserves every
 * existing column, row, score, grade, status, and reason.
 *
 * To run:
 *   1. Open the Video Tracker Apps Script project.
 *   2. Paste this function alongside doPost()/doGet(); remove neither.
 *   3. Select migrateToR4 and press Run.
 *   4. Confirm the execution log ends with "Done".
 *
 * Existing reviews remain tagged r2/r3 and receive blank gate cells. Set
 * Rubric="r4" and fill the gates only when a video is actually watched under
 * r4; never convert prior reviews on paper.
 */
function migrateToR4() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var values = sheet.getDataRange().getValues();

  // Find the real header row rather than assuming row 1.
  var headerIdx = -1;
  for (var r = 0; r < values.length; r++) {
    var cells = values[r].map(function (c) { return String(c).trim(); });
    if (cells.indexOf('Lesson') !== -1 && cells.indexOf('Grade') !== -1) {
      headerIdx = r;
      break;
    }
  }
  if (headerIdx === -1) {
    Logger.log('ABORT: no header row (needs both Lesson and Grade). Nothing changed.');
    return;
  }

  var headerRow = headerIdx + 1;
  var headers = values[headerIdx].map(function (c) { return String(c).trim(); });
  Logger.log('BEFORE: ' + JSON.stringify(headers));

  // r4 reuses the r3 score columns; refuse to create gates on an older schema.
  var pacingCol = headers.indexOf('Pacing & attention (20)') + 1;
  var rubricCol = headers.indexOf('Rubric') + 1;
  if (!pacingCol || !rubricCol) {
    Logger.log('ABORT: r3 columns missing. Run migrateToR3 first. Nothing changed.');
    return;
  }

  var gateHeaders = ['Source QA', 'Accuracy Gate', 'Substitute Gate', 'Board Walk Gate'];
  var missing = gateHeaders.filter(function (h) { return headers.indexOf(h) === -1; });
  if (!missing.length) {
    Logger.log('Already migrated to current r4 gates. Nothing changed.');
    return;
  }

  // Make future manual entry unambiguous without changing existing rows. Add
  // only missing gates so this also upgrades sheets that already ran the
  // original three-gate r4 migration.
  var firstDataRow = headerRow + 1;
  var dataRows = Math.max(sheet.getMaxRows() - headerRow, 1);
  var validation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['PASS', 'FAIL'], true)
    .setAllowInvalid(false)
    .build();

  gateHeaders.forEach(function (gate, i) {
    if (headers.indexOf(gate) !== -1) return;
    var insertAfter = pacingCol;
    if (i > 0) {
      var predecessor = headers.indexOf(gateHeaders[i - 1]);
      if (predecessor !== -1) insertAfter = predecessor + 1;
    }
    sheet.insertColumnsAfter(insertAfter, 1);
    var newCol = insertAfter + 1;
    sheet.getRange(headerRow, newCol).setValue(gate);
    sheet.getRange(firstDataRow, newCol, dataRows, 1).setDataValidation(validation);
    headers.splice(insertAfter, 0, gate);
  });

  var after = sheet.getRange(headerRow, 1, 1, sheet.getLastColumn()).getValues()[0];
  Logger.log('AFTER: ' + JSON.stringify(after));
  Logger.log('Done. Added missing blank r4 gate columns; no existing data changed.');
}
