// Complete replacement for the Apps Script web app handler.
//
// The first spreadsheet tab remains the enrollment sheet. Add "Student ID" as
// the heading in column G. Course completions are stored in a separate tab that
// this script creates automatically.

var NOTIFICATION_EMAIL = "besmarterthanthetool@gmail.com";
var COMPLETIONS_SHEET_NAME = "Course Completions";

function doPost(e) {
  try {
    var data = parseRequest_(e);
    if (data.eventType === "course_completed") {
      recordCompletion_(data);
      return textResponse_("completion-ok");
    }

    recordEnrollment_(data);
    return textResponse_("ok");
  } catch (error) {
    console.error(error && error.stack ? error.stack : error);
    return textResponse_("error");
  }
}

function parseRequest_(e) {
  if (!e || !e.postData || !e.postData.contents) {
    throw new Error("Missing request body");
  }
  var data = JSON.parse(e.postData.contents);
  if (!data || typeof data !== "object") {
    throw new Error("Invalid request body");
  }
  return data;
}

function recordEnrollment_(data) {
  var firstName = clean_(data.firstName) || "Student";
  var lastName = clean_(data.lastName);
  var email = clean_(data.email);
  var city = clean_(data.city);
  var state = clean_(data.state);
  var studentId = clean_(data.studentId);
  var fullName = [firstName, lastName].filter(String).join(" ");
  var location = [city, state].filter(String).join(", ");

  SpreadsheetApp.getActiveSpreadsheet().getSheets()[0].appendRow([
    new Date(), firstName, lastName, email, city, state, studentId
  ]);

  var lines = [fullName];
  if (email) lines.push(email);
  if (location) lines.push(location);
  if (studentId) lines.push("Student ID: " + studentId);

  MailApp.sendEmail(
    NOTIFICATION_EMAIL,
    "New course signup: " + fullName,
    lines.join("\n")
  );
}

function recordCompletion_(data) {
  var completionId = clean_(data.completionId);
  var studentId = clean_(data.studentId);
  var firstName = clean_(data.firstName);
  var lastName = clean_(data.lastName);
  if (!completionId || !studentId || !firstName || !lastName) {
    throw new Error("Completion ID, student ID, first name, and last name are required");
  }

  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sheet = getCompletionSheet_();
    var city = clean_(data.city);
    var state = clean_(data.state);
    var location = [city, state].filter(String).join(", ");
    var score = normalizeScore_(data.score);
    if (score < 80) throw new Error("A passing completion score is required");
    var completedAt = new Date();
    var fullName = firstName + " " + lastName;
    var existingRow = findCompletionRow_(sheet, completionId);

    if (existingRow) {
      var existingName = sheet.getRange(existingRow, 3, 1, 2).getValues()[0];
      if (clean_(existingName[0]) === firstName && clean_(existingName[1]) === lastName) return;
      sheet.getRange(existingRow, 3, 1, 2).setValues([[firstName, lastName]]);
      MailApp.sendEmail(
        NOTIFICATION_EMAIL,
        "Course completion name updated: " + fullName,
        "The certificate name for an existing completion was updated.\n" +
          "Name: " + fullName + "\n" +
          "Student ID: " + studentId
      );
      return;
    }

    sheet.appendRow([
      completedAt,
      studentId,
      firstName,
      lastName,
      city,
      state,
      score,
      completionId,
      clean_(data.courseVersion)
    ]);

    var lines = [
      fullName + " completed Be Smarter Than the Tool.",
      "Final score: " + score + "%"
    ];
    if (location) lines.push("Location: " + location);
    lines.push("Student ID: " + studentId);
    lines.push("Completed: " + completedAt.toLocaleString());

    MailApp.sendEmail(
      NOTIFICATION_EMAIL,
      "Course completed: " + fullName,
      lines.join("\n")
    );
  } finally {
    lock.releaseLock();
  }
}

function getCompletionSheet_() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName(COMPLETIONS_SHEET_NAME);
  if (!sheet) {
    sheet = spreadsheet.insertSheet(COMPLETIONS_SHEET_NAME);
    sheet.appendRow([
      "Completed At",
      "Student ID",
      "First Name",
      "Last Name",
      "City",
      "State",
      "Final Score",
      "Completion ID",
      "Course Version"
    ]);
    sheet.setFrozenRows(1);
  } else {
    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    if (headers.indexOf("Last Name") === -1) {
      sheet.insertColumnAfter(3);
      sheet.getRange(1, 4).setValue("Last Name");
    }
  }
  return sheet;
}

function findCompletionRow_(sheet, completionId) {
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return null;
  var match = sheet
    .getRange(2, 8, lastRow - 1, 1)
    .createTextFinder(completionId)
    .matchEntireCell(true)
    .findNext();
  return match ? match.getRow() : null;
}

function normalizeScore_(value) {
  var score = Number(value);
  if (!isFinite(score)) throw new Error("A valid completion score is required");
  return Math.max(0, Math.min(100, Math.round(score)));
}

function clean_(value) {
  return value == null ? "" : String(value).trim();
}

function textResponse_(value) {
  return ContentService.createTextOutput(value)
    .setMimeType(ContentService.MimeType.TEXT);
}
