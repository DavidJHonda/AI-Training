/**
 * migrateToR5 — idempotent gate-column migration for the
 * "AI-Training — Video Tracker" sheet.
 *
 * r5 preserves the r3 numeric scores and consolidates every current ship gate.
 * Existing columns, rows, scores, grades, statuses, and reasons are preserved.
 * Existing reviews remain tagged with their original rubric version and receive
 * blank cells for any newly added gate.
 */
function migrateToR5() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var values = sheet.getDataRange().getValues();

  var headerIdx = -1;
  for (var r = 0; r < values.length; r++) {
    var cells = values[r].map(function (cell) { return String(cell).trim(); });
    if (cells.indexOf('Lesson') !== -1 && cells.indexOf('Grade') !== -1) {
      headerIdx = r;
      break;
    }
  }
  if (headerIdx === -1) {
    Logger.log('ABORT: no header row with Lesson and Grade. Nothing changed.');
    return;
  }

  var headerRow = headerIdx + 1;
  var headers = values[headerIdx].map(function (cell) { return String(cell).trim(); });
  var pacingCol = headers.indexOf('Pacing & attention (20)') + 1;
  var rubricCol = headers.indexOf('Rubric') + 1;
  if (!pacingCol || !rubricCol) {
    Logger.log('ABORT: r3 numeric columns are missing. Run the r3 migration first.');
    return;
  }

  var gateHeaders = [
    'Source QA',
    'Accuracy Gate',
    'Substitute Gate',
    'Spine Gate',
    'Restraint Gate',
    'Stock Gate',
    'Ending Gate',
    'Sync Gate',
    'Board Walk Gate',
    'No Notebook Highlight Gate',
    'Standard Close Gate',
    'Edit Integrity Gate'
  ];
  var nullable = {
    'Board Walk Gate': true,
    'No Notebook Highlight Gate': true,
    'Standard Close Gate': true
  };
  var firstDataRow = headerRow + 1;
  var dataRows = Math.max(sheet.getMaxRows() - headerRow, 1);

  gateHeaders.forEach(function (gate, index) {
    if (headers.indexOf(gate) !== -1) return;

    var insertAfter = pacingCol;
    if (index > 0) {
      var predecessor = headers.indexOf(gateHeaders[index - 1]);
      if (predecessor !== -1) insertAfter = predecessor + 1;
    }
    sheet.insertColumnsAfter(insertAfter, 1);
    var newCol = insertAfter + 1;
    sheet.getRange(headerRow, newCol).setValue(gate);
    var allowed = nullable[gate] ? ['PASS', 'FAIL', 'N/A'] : ['PASS', 'FAIL'];
    var validation = SpreadsheetApp.newDataValidation()
      .requireValueInList(allowed, true)
      .setAllowInvalid(false)
      .build();
    sheet.getRange(firstDataRow, newCol, dataRows, 1).setDataValidation(validation);
    headers.splice(insertAfter, 0, gate);
  });

  var after = sheet.getRange(headerRow, 1, 1, sheet.getLastColumn()).getValues()[0];
  Logger.log('AFTER: ' + JSON.stringify(after));
  Logger.log('Done. Added missing blank r5 gate columns; no existing data changed.');
}
