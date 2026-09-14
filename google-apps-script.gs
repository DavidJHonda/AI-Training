// Complete replacement for the Apps Script web app handler.
//
// The first spreadsheet tab remains the enrollment sheet. Add "Student ID" as
// the heading in column G. Course completions and reviews are stored in separate
// tabs that this script creates automatically.

var NOTIFICATION_EMAIL = "besmarterthanthetool@gmail.com";
var COMPLETIONS_SHEET_NAME = "Course Completions";
var REVIEWS_SHEET_NAME = "Reviews";

function doGet(e) {
  var diagnostic = { stage: "request", startedAt: Date.now() };
  try {
    var params = e && e.parameter ? e.parameter : {};
    if (params.action !== "public_reviews") throw new Error("Unknown action");
    return jsonResponse_(getPublicReviews_(params, diagnostic));
  } catch (error) {
    var code = "REVIEWS_" + diagnostic.stage.toUpperCase() + "_FAILED";
    console.error(JSON.stringify({ operation: "public_reviews", code: code,
      elapsedMs: Date.now() - diagnostic.startedAt,
      detail: String(error && error.stack ? error.stack : error) }));
    // A safe category helps diagnose live failures even when Cloud logs are unavailable.
    // Never send exception text, spreadsheet details, or student data to the browser.
    return jsonResponse_({ error: "Student reviews could not be loaded.", code: code });
  }
}

function getPublicReviews_(params, diagnostic) {
  diagnostic = diagnostic || {};
  diagnostic.stage = "request";
  var cursor = params.cursor ? JSON.parse(params.cursor) : null;
  if (cursor && (!Number.isSafeInteger(cursor.offset) || cursor.offset < 0 ||
      typeof cursor.revision !== "string")) throw new Error("Invalid cursor");
  var entries = [];
  var ratingTotal = 0;
  var ratingSum = 0;
  // Read one snapshot without queuing behind submissions, other readers, or
  // certificate emails. Writers serialize with each other and update each review
  // in one range operation, so rating, text, and permission are not split writes.
  // A public read must not create a sheet or change its sharing settings.
  diagnostic.stage = "read";
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(REVIEWS_SHEET_NAME);
  if (sheet) {
    diagnostic.stage = "layout";
    sheet = getReviewSheet_(); // Validate the compact or legacy headers before reading.
    diagnostic.stage = "read";
    var feedbackIndex = sheet.getRange(1, 7).getValues()[0][0] === "Improvement" ? 6 : 10;
    var count = sheet.getLastRow() - 1;
    var rows = count > 0 ? sheet.getRange(2, 1, count, feedbackIndex + 4).getValues() : [];
    diagnostic.stage = "format";
    rows.forEach(function(row, index) {
      // Each saved row is one submission; editing updates that row instead of adding a rating.
      // Aggregate all valid ratings, regardless of written text or publication permission.
      var rating = Number(row[5]);
      if (!Number.isInteger(rating) || rating < 1 || rating > 5) return;
      ratingTotal++;
      ratingSum += rating;
      var permission = clean_(row[feedbackIndex + 2]);
      var text = clean_(row[feedbackIndex + 1]);
      if (!text || (permission !== "anonymous" && permission !== "first_name")) return;
      var submitted = row[0] instanceof Date ? row[0] : new Date(row[0]);
      if (!row[0] || !isFinite(submitted.getTime())) return;
      // Explicit allowlist: never return review/student IDs, private feedback, or entire rows.
      entries.push({ order: index, review: {
        rating: rating,
        text: text,
        submittedAt: submitted.toISOString(),
        name: permission === "first_name" ? (clean_(row[feedbackIndex + 3]) || "Anonymous") : "Anonymous"
      } });
    });
  }
  diagnostic.stage = "format";
  entries.sort(function(a, b) {
    return Date.parse(b.review.submittedAt) - Date.parse(a.review.submittedAt) || b.order - a.order;
  });
  var reviews = entries.map(function(entry) { return entry.review; });
  var ratingSummary = { average: ratingTotal ? ratingSum / ratingTotal : null, total: ratingTotal };
  // Restart pagination if a review was added, edited, or made private between requests.
  // The cursor contains only an offset and a digest of public fields, never private IDs.
  var revision = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, JSON.stringify({ reviews: reviews, ratingSummary: ratingSummary }))
    .map(function(byte) { return ("0" + ((byte + 256) % 256).toString(16)).slice(-2); }).join("");
  var reset = !!cursor && cursor.revision !== revision;
  var offset = cursor && !reset ? cursor.offset : 0;
  var page = reviews.slice(offset, offset + 20);
  var nextOffset = offset + page.length;
  return {
    reviews: page,
    ratingSummary: ratingSummary,
    nextCursor: nextOffset < reviews.length ? JSON.stringify({ offset: nextOffset, revision: revision }) : null,
    reset: reset
  };
}

function jsonResponse_(value) {
  return ContentService.createTextOutput(JSON.stringify(value)).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    var data = parseRequest_(e);
    if (data.eventType === "course_completed") {
      recordCompletion_(data);
      return textResponse_("completion-ok");
    }
    if (data.eventType === "review") {
      recordReview_(data);
      return textResponse_("review-ok");
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

function recordReview_(data) {
  var reviewId = clean_(data.reviewId);
  var studentId = clean_(data.studentId);
  if (!reviewId || !studentId) throw new Error("Review ID and student ID are required");

  var usefulness = normalizeRating_(data.usefulnessRating);
  var testimonial = sheetSafe_(data.testimonial, 2500);
  // Publication permission applies only to the written review, never improvement feedback.
  var quotePermission = testimonial ? (clean_(data.quotePermission) || "none") : "none";
  if (["none", "anonymous", "first_name"].indexOf(quotePermission) === -1) {
    throw new Error("Invalid quote permission");
  }
  var quoteFirstName = quotePermission === "first_name" ? sheetSafe_(data.quoteFirstName, 80) : "";
  if (quotePermission === "first_name" && !quoteFirstName) {
    throw new Error("A first name is required for first-name quote permission");
  }

  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sheet = getReviewSheet_();
    // Support the old layout until G–J are deleted, then write feedback into G–J.
    var feedbackColumn = sheet.getRange(1, 7).getValues()[0][0] === "Improvement" ? 7 : 11;
    var now = new Date();
    var existingRow = findReviewRow_(sheet, reviewId);
    var reviewValues = [
      now,
      reviewId,
      studentId,
      clean_(data.courseVersion),
      usefulness
    ];
    var feedbackValues = [
      sheetSafe_(data.improvement, 2500),
      testimonial,
      quotePermission,
      quoteFirstName
    ];

    if (existingRow) {
      // Preserve Submitted At (A). Review ID continues to identify the same row.
      var retiredValues = feedbackColumn === 11 ? sheet.getRange(existingRow, 7, 1, 4).getValues()[0] : [];
      var updatedValues = reviewValues.concat(retiredValues, feedbackValues);
      // Keep rating, text, publication permission, and name in the same range write.
      sheet.getRange(existingRow, 2, 1, updatedValues.length).setValues([updatedValues]);
    } else {
      var retiredColumns = feedbackColumn === 11 ? ["", "", "", ""] : [];
      sheet.appendRow([now].concat(reviewValues, retiredColumns, feedbackValues));
    }
    SpreadsheetApp.flush();
  } finally {
    lock.releaseLock();
  }
}

function getReviewSheet_() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName(REVIEWS_SHEET_NAME);
  var headers = [
    "Submitted At",
    "Updated At",
    "Review ID",
    "Student ID",
    "Course Version",
    "Usefulness Rating",
    "Improvement",
    "Testimonial",
    "Quote Permission",
    "Quote First Name"
  ];
  if (!sheet) {
    sheet = spreadsheet.insertSheet(REVIEWS_SHEET_NAME);
    sheet.appendRow(headers);
    sheet.setFrozenRows(1);
  } else {
    // Validate before writing so partial deletions or reordered columns cannot misfile answers.
    var currentHeaders = sheet.getRange(1, 1, 1, Math.max(1, sheet.getLastColumn())).getValues()[0];
    var legacyHeaders = headers.slice(0, 6).concat(
      ["Confidence Before", "Confidence After", "Most Useful", "What Changed"], headers.slice(6));
    if (JSON.stringify(currentHeaders) !== JSON.stringify(headers) &&
        JSON.stringify(currentHeaders) !== JSON.stringify(legacyHeaders)) {
      throw new Error("Reviews headers do not match the supported layout. Delete the four retired columns together, leaving Submitted At through Usefulness Rating followed by Improvement, Testimonial, Quote Permission, and Quote First Name.");
    }
  }
  return sheet;
}

function findReviewRow_(sheet, reviewId) {
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return null;
  var match = sheet
    .getRange(2, 3, lastRow - 1, 1)
    .createTextFinder(reviewId)
    .matchEntireCell(true)
    .findNext();
  return match ? match.getRow() : null;
}

function normalizeRating_(value) {
  var rating = Number(value);
  if (!isFinite(rating) || rating < 1 || rating > 5 || Math.round(rating) !== rating) {
    throw new Error("Review ratings must be whole numbers from 1 to 5");
  }
  return rating;
}

function sheetSafe_(value, maxLength) {
  var text = clean_(value).slice(0, maxLength || 2500);
  return /^[=+\-@]/.test(text) ? "'" + text : text;
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
