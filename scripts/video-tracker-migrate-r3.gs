/**
 * migrateToR3 — one-shot schema migration for the "AI-Training — Video Tracker" sheet.
 *
 * Restructures the header row from rubric r2 to r3 (videos/video-rubric.csv, adopted
 * 2026-07-25). Run ONCE. It is idempotent: a second run detects the r3 headers and
 * exits without touching anything.
 *
 * NOT auto-deployed. To run:
 *   1. Open the Video Tracker Apps Script project (script.google.com).
 *   2. Paste this function alongside the existing doPost()/doGet() (remove neither).
 *   3. Select migrateToR3 in the function dropdown and press Run.
 *   4. Read the execution log. It prints the header row before and after, the number
 *      of rows stamped, and any stray blank-Lesson rows it found.
 *   NO redeploy needed — Run works from the editor. Deployment only affects the
 *   /exec web-app endpoints, which this does not change.
 *
 * WHAT IT DOES
 *   - Trims every header cell. Three r2 headers carry a leading space (" Boards (15)",
 *     " Animation (15)", " Pacing (10)") which has silently swallowed doPost writes.
 *     Trimming fixes that class of bug permanently.
 *   - Inserts the r3 scoring columns immediately after Grade, all empty.
 *   - Renames the five r2 dimension columns with an "r2 " prefix. NOTHING IS DELETED:
 *     every r2 score stays readable, it just moves right and is labelled as the old
 *     scale. r2 and r3 grades are not comparable, so both must stay legible.
 *   - Adds a Rubric column and stamps every existing lesson row "r2". Rows re-scored
 *     under r3 get flipped to "r3" by the normal intake write.
 *
 * WHAT IT DELIBERATELY DOES NOT DO
 *   - Delete any column, row, or value.
 *   - Touch the Grade column. Grade stays the live grade; the Rubric column is what
 *     tells you which scale produced it.
 *   - Install formulas. Teaching (60) is a plain cell, not =SUM(...), because the
 *     intake writes values via doPost and a written value would destroy a formula.
 */
function migrateToR3() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var lastCol = sheet.getLastColumn();
  var values = sheet.getDataRange().getValues();

  // Find the header row the same way doGet does: it has both 'Lesson' and 'Grade'.
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
  var headerRow = headerIdx + 1;                       // 1-indexed for Range calls
  var headers = values[headerIdx].map(function (c) { return String(c).trim(); });
  Logger.log('BEFORE: ' + JSON.stringify(headers));

  // Idempotence guard.
  if (headers.indexOf('Coverage (20)') !== -1) {
    Logger.log('Already migrated to r3 (Coverage (20) present). Nothing changed.');
    return;
  }

  // Step 1: write back the trimmed headers, killing the leading-space bug.
  sheet.getRange(headerRow, 1, 1, lastCol).setValues([headers]);

  // Step 2: prefix the r2 dimension columns so their data survives, clearly labelled.
  var renames = {
    'Teaching (45)':    'r2 Teaching (45)',
    'Boards (15)':      'r2 Boards (15)',
    'Animation (15)':   'r2 Animation (15)',
    'Cleanliness (15)': 'r2 Cleanliness (15)',
    'Pacing (10)':      'r2 Pacing (10)'
  };
  var renamed = [];
  for (var oldName in renames) {
    var at = headers.indexOf(oldName);
    if (at !== -1) {
      sheet.getRange(headerRow, at + 1).setValue(renames[oldName]);
      renamed.push(oldName + ' -> ' + renames[oldName]);
    }
  }
  Logger.log('Renamed ' + renamed.length + ' r2 columns: ' + JSON.stringify(renamed));

  // Step 3: insert the r3 block immediately after Grade.
  var gradeCol = headers.indexOf('Grade') + 1;         // 1-indexed
  var r3Headers = [
    'Rubric',                    // r2 | r3 — which scale produced this row's Grade
    'Teaching (60)',             // sum of the four sub-scores below
    'Coverage (20)',
    "Lesson's material (15)",
    'Teaches vs recites (15)',
    'Board content (10)',
    'Cleanliness (20)',
    'Pacing & attention (20)'
  ];
  sheet.insertColumnsAfter(gradeCol, r3Headers.length);
  sheet.getRange(headerRow, gradeCol + 1, 1, r3Headers.length).setValues([r3Headers]);
  Logger.log('Inserted ' + r3Headers.length + ' r3 columns after Grade (col ' + gradeCol + ').');

  // Step 4: stamp every existing lesson row as r2. Blank-Lesson rows are skipped and
  // reported, not touched — the sheet has carried a stray typo row since 7/13.
  var lessonCol = headers.indexOf('Lesson') + 1;
  var rubricCol = gradeCol + 1;
  var lastRow = sheet.getLastRow();
  var stamped = 0;
  var strays = [];
  for (var row = headerRow + 1; row <= lastRow; row++) {
    var lesson = String(sheet.getRange(row, lessonCol).getValue()).trim();
    if (!lesson) {
      strays.push(row);
      continue;
    }
    sheet.getRange(row, rubricCol).setValue('r2');
    stamped++;
  }
  Logger.log('Stamped Rubric="r2" on ' + stamped + ' lesson rows.');
  if (strays.length) {
    Logger.log('Stray blank-Lesson rows (NOT touched, delete by hand if unwanted): ' +
               JSON.stringify(strays));
  }

  var after = sheet.getRange(headerRow, 1, 1, sheet.getLastColumn()).getValues()[0];
  Logger.log('AFTER: ' + JSON.stringify(after));
  Logger.log('Done. No column, row, or score was deleted.');
}
