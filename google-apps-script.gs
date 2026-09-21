// Complete replacement for the Apps Script web app handler.
//
// The first spreadsheet tab remains the enrollment sheet. New sheets use:
// Timestamp | First Name | Student ID | Country.
// Existing enrollment layouts are read by header, including the old "Certificate?"
// heading for Student ID. After deploying this version, run migrateEnrollmentSheet
// once to back up the enrollment sheet and remove Last Name, Email, City and State.
// Reviews remain in their existing separate tab. Course Completions keeps the
// certificate first/last name and tracking fields. Run migrateCompletionSheet once
// to back up that tab and replace its City/State columns with Country.

var NOTIFICATION_EMAIL = "besmarterthanthetool@gmail.com";
var COMPLETIONS_SHEET_NAME = "Course Completions";
var REVIEWS_SHEET_NAME = "Reviews";

// Same country labels as country-select.js. Legacy enrollments may omit country.
var COURSE_COUNTRIES = [
  "United States",
  "Afghanistan",
  "Åland Islands",
  "Albania",
  "Algeria",
  "American Samoa",
  "Andorra",
  "Angola",
  "Anguilla",
  "Antarctica",
  "Antigua & Barbuda",
  "Argentina",
  "Armenia",
  "Aruba",
  "Australia",
  "Austria",
  "Azerbaijan",
  "Bahamas",
  "Bahrain",
  "Bangladesh",
  "Barbados",
  "Belarus",
  "Belgium",
  "Belize",
  "Benin",
  "Bermuda",
  "Bhutan",
  "Bolivia",
  "Bosnia & Herzegovina",
  "Botswana",
  "Bouvet Island",
  "Brazil",
  "British Indian Ocean Territory",
  "British Virgin Islands",
  "Brunei",
  "Bulgaria",
  "Burkina Faso",
  "Burundi",
  "Cambodia",
  "Cameroon",
  "Canada",
  "Cape Verde",
  "Caribbean Netherlands",
  "Cayman Islands",
  "Central African Republic",
  "Chad",
  "Chile",
  "China",
  "Christmas Island",
  "Cocos (Keeling) Islands",
  "Colombia",
  "Comoros",
  "Congo - Brazzaville",
  "Congo - Kinshasa",
  "Cook Islands",
  "Costa Rica",
  "Côte d’Ivoire",
  "Croatia",
  "Cuba",
  "Curaçao",
  "Cyprus",
  "Czechia",
  "Denmark",
  "Djibouti",
  "Dominica",
  "Dominican Republic",
  "Ecuador",
  "Egypt",
  "El Salvador",
  "Equatorial Guinea",
  "Eritrea",
  "Estonia",
  "Eswatini",
  "Ethiopia",
  "Falkland Islands",
  "Faroe Islands",
  "Fiji",
  "Finland",
  "France",
  "French Guiana",
  "French Polynesia",
  "French Southern Territories",
  "Gabon",
  "Gambia",
  "Georgia",
  "Germany",
  "Ghana",
  "Gibraltar",
  "Greece",
  "Greenland",
  "Grenada",
  "Guadeloupe",
  "Guam",
  "Guatemala",
  "Guernsey",
  "Guinea",
  "Guinea-Bissau",
  "Guyana",
  "Haiti",
  "Heard & McDonald Islands",
  "Honduras",
  "Hong Kong SAR China",
  "Hungary",
  "Iceland",
  "India",
  "Indonesia",
  "Iran",
  "Iraq",
  "Ireland",
  "Isle of Man",
  "Israel",
  "Italy",
  "Jamaica",
  "Japan",
  "Jersey",
  "Jordan",
  "Kazakhstan",
  "Kenya",
  "Kiribati",
  "Kuwait",
  "Kyrgyzstan",
  "Laos",
  "Latvia",
  "Lebanon",
  "Lesotho",
  "Liberia",
  "Libya",
  "Liechtenstein",
  "Lithuania",
  "Luxembourg",
  "Macao SAR China",
  "Madagascar",
  "Malawi",
  "Malaysia",
  "Maldives",
  "Mali",
  "Malta",
  "Marshall Islands",
  "Martinique",
  "Mauritania",
  "Mauritius",
  "Mayotte",
  "Mexico",
  "Micronesia",
  "Moldova",
  "Monaco",
  "Mongolia",
  "Montenegro",
  "Montserrat",
  "Morocco",
  "Mozambique",
  "Myanmar (Burma)",
  "Namibia",
  "Nauru",
  "Nepal",
  "Netherlands",
  "New Caledonia",
  "New Zealand",
  "Nicaragua",
  "Niger",
  "Nigeria",
  "Niue",
  "Norfolk Island",
  "North Korea",
  "North Macedonia",
  "Northern Mariana Islands",
  "Norway",
  "Oman",
  "Pakistan",
  "Palau",
  "Palestinian Territories",
  "Panama",
  "Papua New Guinea",
  "Paraguay",
  "Peru",
  "Philippines",
  "Pitcairn Islands",
  "Poland",
  "Portugal",
  "Puerto Rico",
  "Qatar",
  "Réunion",
  "Romania",
  "Russia",
  "Rwanda",
  "Samoa",
  "San Marino",
  "São Tomé & Príncipe",
  "Saudi Arabia",
  "Senegal",
  "Serbia",
  "Seychelles",
  "Sierra Leone",
  "Singapore",
  "Sint Maarten",
  "Slovakia",
  "Slovenia",
  "Solomon Islands",
  "Somalia",
  "South Africa",
  "South Georgia & South Sandwich Islands",
  "South Korea",
  "South Sudan",
  "Spain",
  "Sri Lanka",
  "St. Barthélemy",
  "St. Helena",
  "St. Kitts & Nevis",
  "St. Lucia",
  "St. Martin",
  "St. Pierre & Miquelon",
  "St. Vincent & Grenadines",
  "Sudan",
  "Suriname",
  "Svalbard & Jan Mayen",
  "Sweden",
  "Switzerland",
  "Syria",
  "Taiwan",
  "Tajikistan",
  "Tanzania",
  "Thailand",
  "Timor-Leste",
  "Togo",
  "Tokelau",
  "Tonga",
  "Trinidad & Tobago",
  "Tunisia",
  "Türkiye",
  "Turkmenistan",
  "Turks & Caicos Islands",
  "Tuvalu",
  "U.S. Outlying Islands",
  "U.S. Virgin Islands",
  "Uganda",
  "Ukraine",
  "United Arab Emirates",
  "United Kingdom",
  "Uruguay",
  "Uzbekistan",
  "Vanuatu",
  "Vatican City",
  "Venezuela",
  "Vietnam",
  "Wallis & Futuna",
  "Western Sahara",
  "Yemen",
  "Zambia",
  "Zimbabwe"
];

function doGet(e) {
  var diagnostic = { stage: "request", startedAt: Date.now() };
  try {
    var params = e && e.parameter ? e.parameter : {};
    if (params.action === "feedback_status") return textResponse_("feedback-ready");
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
    if (data.eventType === "lesson_feedback") {
      sendLessonFeedback_(data);
      return textResponse_("feedback-ok");
    }
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

// Feedback uses email only. Small fixed-recipient limits preserve the shared mail quota.
function sendLessonFeedback_(data) {
  var id = typeof data.reportId === "string" ? data.reportId : "";
  var client = typeof data.clientId === "string" ? data.clientId : "";
  var lessonId = typeof data.lessonId === "string" ? data.lessonId : "";
  var title = typeof data.lessonTitle === "string" ? data.lessonTitle.trim() : "";
  var message = typeof data.message === "string" ? data.message.trim() : "";
  if (!/^[a-zA-Z0-9-]{16,80}$/.test(id) || !/^[a-zA-Z0-9-]{16,80}$/.test(client) ||
      !/^[a-z0-9_-]{1,80}$/.test(lessonId) || !title || title.length > 100 || /[\r\n\x00-\x1f]/.test(title) ||
      !message || message.length > 2500 || data.website) throw new Error("Invalid lesson feedback");
  var hash = Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, JSON.stringify([lessonId, title, message])));
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var properties = PropertiesService.getScriptProperties();
    var now = Date.now(), prefix = "lesson-feedback-sent:";
    // Bounded receipts protect retries after a lost response; no message text is stored.
    var receipt = properties.getProperty(prefix + id);
    if (receipt) {
      var previous = JSON.parse(receipt);
      if (previous.hash !== hash) throw new Error("Feedback request changed");
      return;
    }
    var day = new Date(now).toISOString().slice(0,10);
    var budget = JSON.parse(properties.getProperty("lesson-feedback-budget") || "{}");
    if (budget.day !== day) budget = { day: day, count: 0 };
    var cache = CacheService.getScriptCache();
    var rateKey = "lesson-feedback-client:" + client;
    var rate = JSON.parse(cache.get(rateKey) || "{}");
    if (!rate.until || rate.until <= now) rate = { until: now + 3600000, count: 0 };
    if (budget.count >= 50 || rate.count >= 5 || MailApp.getRemainingDailyQuota() <= 10) throw new Error("Feedback sending limit reached");
    MailApp.sendEmail(NOTIFICATION_EMAIL, "Course feedback: " + title,
      "Lesson: " + title + "\nLesson ID: " + lessonId + "\nReport ID: " + id + "\n\n" + message);
    properties.setProperty(prefix + id, JSON.stringify({ at: now, hash: hash }));
    budget.count++; properties.setProperty("lesson-feedback-budget", JSON.stringify(budget));
    rate.count++; cache.put(rateKey, JSON.stringify(rate), Math.max(1, Math.ceil((rate.until - now) / 1000)));
    var all = properties.getProperties();
    Object.keys(all).forEach(function(key) {
      if (key.indexOf(prefix) === 0 && JSON.parse(all[key]).at < now - 86400000) properties.deleteProperty(key);
    });
  } finally { lock.releaseLock(); }
}

function recordEnrollment_(data) {
  var country = clean_(data.country);
  if (country && COURSE_COUNTRIES.indexOf(country) === -1) throw new Error("Invalid country selection");
  // The new form requires a country. Older pages and queued signups can still
  // send the legacy payload, preserving returning-student and retry behavior.
  if (data.registrationVersion === 2 && (!clean_(data.firstName) || !country)) {
    throw new Error("First name and country are required");
  }
  var firstName = clean_(data.firstName) || "Student";
  var studentId = clean_(data.studentId);

  // Serialize header creation and row writes. Email delivery stays outside the lock.
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var enrollment = getEnrollmentSheet_();
    var values = new Array(enrollment.width).fill("");
    values[0] = new Date();
    values[1] = firstName;
    values[enrollment.studentIdColumn - 1] = studentId;
    values[enrollment.countryColumn - 1] = country;
    enrollment.sheet.appendRow(values);
    SpreadsheetApp.flush();
  } finally {
    lock.releaseLock();
  }

  var lines = [firstName];
  if (country) lines.push("Country: " + country);
  if (studentId) lines.push("Student ID: " + studentId);

  MailApp.sendEmail(
    NOTIFICATION_EMAIL,
    "New course signup: " + firstName,
    lines.join("\n")
  );
}

function enrollmentLayout_(sheet) {
  var width = sheet.getLastColumn();
  var headers = sheet.getRange(1, 1, 1, Math.max(1, width)).getValues()[0];
  var normalized = headers.map(function(header) { return clean_(header).toLowerCase(); });
  if (["timestamp", "registered at", "date"].indexOf(normalized[0]) === -1 || normalized[1] !== "first name") {
    throw new Error("The first enrollment columns must be Timestamp and First Name");
  }
  var studentIndexes = [], countryIndexes = [], retiredColumns = [];
  normalized.forEach(function(header, index) {
    if (header === "student id" || header === "certificate?") studentIndexes.push(index);
    if (header === "country") countryIndexes.push(index);
    if (["last name", "email", "city", "state"].indexOf(header) !== -1) retiredColumns.push(index + 1);
  });
  // Older setup instructions sometimes left G1 blank, but G already held IDs.
  var legacyBlankId = !studentIndexes.length && normalized.slice(2, 6).join("|") === "last name|email|city|state" && !normalized[6];
  if (legacyBlankId) studentIndexes.push(6);
  if (studentIndexes.length !== 1 || studentIndexes[0] < 2 || countryIndexes.length > 1 || (countryIndexes.length && countryIndexes[0] < 2)) {
    throw new Error("Enrollment requires one Student ID column and at most one separate Country column");
  }
  return { sheet: sheet, headers: headers, width: Math.max(width, studentIndexes[0] + 1),
    studentIdColumn: studentIndexes[0] + 1, countryColumn: countryIndexes.length ? countryIndexes[0] + 1 : null,
    retiredColumns: retiredColumns };
}

function getEnrollmentSheet_() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (!sheet.getLastRow()) sheet.appendRow(["Timestamp", "First Name", "Student ID", "Country"]);
  var layout = enrollmentLayout_(sheet);
  if (clean_(layout.headers[layout.studentIdColumn - 1]) !== "Student ID") {
    sheet.getRange(1, layout.studentIdColumn).setValues([["Student ID"]]);
  }
  if (!layout.countryColumn) {
    layout.countryColumn = ++layout.width;
    while (layout.width > sheet.getMaxColumns()) sheet.insertColumnAfter(sheet.getMaxColumns());
    sheet.getRange(1, layout.countryColumn).setValues([["Country"]]);
  }
  return layout;
}

// Run from the Apps Script editor only AFTER deploying the new web app version.
// It is not called by doGet/doPost. A full backup is created before removing columns.
function migrateEnrollmentSheet() {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = spreadsheet.getSheets()[0];
    if (!sheet.getLastRow()) {
      getEnrollmentSheet_();
      return "Created the four-column enrollment sheet.";
    }
    var layout = enrollmentLayout_(sheet); // Validate before making any changes.
    var backupName = "";
    if (layout.retiredColumns.length) {
      backupName = "Enrollment backup " + new Date().getTime();
      sheet.copyTo(spreadsheet).setName(backupName);
    }
    getEnrollmentSheet_(); // Normalize the ID heading and add Country if missing.
    layout.retiredColumns.sort(function(a, b) { return b - a; }).forEach(function(column) {
      sheet.deleteColumns(column, 1);
    });
    sheet.getRange(1, 1).setValues([["Timestamp"]]);
    SpreadsheetApp.flush();
    var message = backupName ? "Enrollment cleaned up. Historical data is preserved in " + backupName + "." : "Enrollment is already clean. No columns removed.";
    console.log(message);
    return message;
  } finally {
    lock.releaseLock();
  }
}

function recordCompletion_(data) {
  var completionId = clean_(data.completionId);
  var studentId = clean_(data.studentId);
  var firstName = clean_(data.firstName);
  var lastName = clean_(data.lastName);
  if (!completionId || !studentId || !firstName || !lastName) {
    throw new Error("Completion ID, student ID, first name, and last name are required");
  }
  var country = clean_(data.country);
  if (country && COURSE_COUNTRIES.indexOf(country) === -1) throw new Error("Invalid country selection");

  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var layout = getCompletionSheet_();
    var sheet = layout.sheet;
    var score = normalizeScore_(data.score);
    if (score < 80) throw new Error("A passing completion score is required");
    var completedAt = new Date();
    var fullName = firstName + " " + lastName;
    var existingRow = findCompletionRow_(layout, completionId);

    if (existingRow) {
      var existingName = sheet.getRange(existingRow, 3, 1, 2).getValues()[0];
      var existingCountry = clean_(sheet.getRange(existingRow, layout.countryColumn).getValues()[0][0]);
      var nameChanged = clean_(existingName[0]) !== firstName || clean_(existingName[1]) !== lastName;
      var countryChanged = !!country && existingCountry !== country;
      if (!nameChanged && !countryChanged) return;
      if (nameChanged) sheet.getRange(existingRow, 3, 1, 2).setValues([[firstName, lastName]]);
      // A blank legacy payload must never erase an existing country.
      if (countryChanged) sheet.getRange(existingRow, layout.countryColumn).setValues([[country]]);
      SpreadsheetApp.flush();
      if (nameChanged) {
        MailApp.sendEmail(
          NOTIFICATION_EMAIL,
          "Course completion name updated: " + fullName,
          "The certificate name for an existing completion was updated.\n" +
            "Name: " + fullName + "\n" +
            "Student ID: " + studentId
        );
      }
      return;
    }

    var values = new Array(layout.width).fill("");
    values[0] = completedAt;
    values[1] = studentId;
    values[2] = firstName;
    values[3] = lastName;
    values[layout.countryColumn - 1] = country;
    values[layout.scoreColumn - 1] = score;
    values[layout.completionIdColumn - 1] = completionId;
    values[layout.courseVersionColumn - 1] = clean_(data.courseVersion);
    sheet.appendRow(values);
    SpreadsheetApp.flush();

    var lines = [
      fullName + " completed Be Smarter Than the Tool.",
      "Final score: " + score + "%"
    ];
    if (country) lines.push("Country: " + country);
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

function completionLayout_(sheet) {
  var width = sheet.getLastColumn();
  var headers = sheet.getRange(1, 1, 1, Math.max(1, width)).getValues()[0].map(clean_);
  var target = ["Completed At", "Student ID", "First Name", "Last Name", "Country", "Final Score", "Completion ID", "Course Version"];
  var legacy = ["Completed At", "Student ID", "First Name", "Last Name", "City", "State", "Final Score", "Completion ID", "Course Version"];
  var transitional = ["Completed At", "Student ID", "First Name", "Last Name", "City", "State", "Country", "Final Score", "Completion ID", "Course Version"];
  var oldWithoutLastName = ["Completed At", "Student ID", "First Name", "City", "State", "Final Score", "Completion ID", "Course Version"];
  var signature = JSON.stringify(headers);
  var kind = signature === JSON.stringify(target) ? "target" :
    signature === JSON.stringify(legacy) ? "legacy" :
    signature === JSON.stringify(transitional) ? "transitional" :
    signature === JSON.stringify(oldWithoutLastName) ? "without-last-name" : "";
  if (!kind) {
    throw new Error("Course Completions headers do not match a supported layout. Restore the sheet from backup before retrying.");
  }
  return {
    sheet: sheet, kind: kind, headers: headers, width: width,
    countryColumn: kind === "target" ? 5 : (kind === "transitional" ? 7 : null),
    scoreColumn: kind === "target" ? 6 : (kind === "transitional" ? 8 : (kind === "without-last-name" ? 6 : 7)),
    completionIdColumn: kind === "target" ? 7 : (kind === "transitional" ? 9 : (kind === "without-last-name" ? 7 : 8)),
    courseVersionColumn: kind === "target" ? 8 : (kind === "transitional" ? 10 : (kind === "without-last-name" ? 8 : 9))
  };
}

function getCompletionSheet_() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName(COMPLETIONS_SHEET_NAME);
  if (!sheet) {
    sheet = spreadsheet.insertSheet(COMPLETIONS_SHEET_NAME);
    sheet.appendRow(["Completed At", "Student ID", "First Name", "Last Name", "Country", "Final Score", "Completion ID", "Course Version"]);
    sheet.setFrozenRows(1);
    return completionLayout_(sheet);
  }
  if (!sheet.getLastRow()) {
    sheet.appendRow(["Completed At", "Student ID", "First Name", "Last Name", "Country", "Final Score", "Completion ID", "Course Version"]);
    sheet.setFrozenRows(1);
    return completionLayout_(sheet);
  }
  var layout = completionLayout_(sheet);
  if (layout.kind === "without-last-name") {
    sheet.insertColumnAfter(3);
    sheet.getRange(1, 4).setValues([["Last Name"]]);
    layout = completionLayout_(sheet);
  }
  // During the deploy-before-migrate window, keep City/State untouched and add a
  // dedicated Country column before Final Score. The migration later removes only City/State.
  if (layout.kind === "legacy") {
    sheet.insertColumnAfter(6);
    sheet.getRange(1, 7).setValues([["Country"]]);
    layout = completionLayout_(sheet);
  }
  return layout;
}

function findCompletionRow_(layout, completionId) {
  var sheet = layout.sheet;
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return null;
  var match = sheet
    .getRange(2, layout.completionIdColumn, lastRow - 1, 1)
    .createTextFinder(completionId)
    .matchEntireCell(true)
    .findNext();
  return match ? match.getRow() : null;
}

// Run once from the Apps Script editor after deploying this version. The function
// creates a full backup before deleting City and State, then leaves the active tab
// in the compact layout used for all future completion records.
function migrateCompletionSheet() {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = spreadsheet.getSheetByName(COMPLETIONS_SHEET_NAME);
    if (!sheet) {
      getCompletionSheet_();
      return "Created the compact Course Completions sheet.";
    }
    if (!sheet.getLastRow()) {
      getCompletionSheet_();
      return "Initialized the empty Course Completions sheet.";
    }
    var before = completionLayout_(sheet); // Validate before backup or deletion.
    if (before.kind === "target") return "Course Completions is already clean. No columns removed.";
    var backupName = "Course Completions backup " + new Date().getTime();
    sheet.copyTo(spreadsheet).setName(backupName); // Stop here if backup creation fails.
    var layout = getCompletionSheet_(); // Add Last Name/Country if an older layout needs them.
    if (layout.kind !== "transitional") throw new Error("Course Completions could not be prepared for migration");
    // Delete right-to-left so the original City and State positions remain stable.
    sheet.deleteColumns(6, 1);
    sheet.deleteColumns(5, 1);
    SpreadsheetApp.flush();
    var finalLayout = completionLayout_(sheet);
    if (finalLayout.kind !== "target") throw new Error("Course Completions migration did not produce the expected layout");
    var message = "Course Completions cleaned up. Historical data is preserved in " + backupName + ".";
    console.log(message);
    return message;
  } finally {
    lock.releaseLock();
  }
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
