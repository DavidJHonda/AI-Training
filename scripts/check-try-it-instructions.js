#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const sourcePath = path.join(root, "index.html");
const source = fs.readFileSync(sourcePath, "utf8");

function matchingBrace(start) {
  let depth = 0;
  let quote = null;
  let escaped = false;
  let lineComment = false;
  let blockComment = false;

  for (let i = start; i < source.length; i += 1) {
    const ch = source[i];
    const next = source[i + 1];

    if (lineComment) {
      if (ch === "\n") lineComment = false;
      continue;
    }
    if (blockComment) {
      if (ch === "*" && next === "/") {
        blockComment = false;
        i += 1;
      }
      continue;
    }
    if (quote) {
      if (escaped) escaped = false;
      else if (ch === "\\") escaped = true;
      else if (ch === quote) quote = null;
      continue;
    }
    if (ch === "/" && next === "/") {
      lineComment = true;
      i += 1;
      continue;
    }
    if (ch === "/" && next === "*") {
      blockComment = true;
      i += 1;
      continue;
    }
    if (ch === "\"" || ch === "'" || ch === "`") {
      quote = ch;
      continue;
    }
    if (ch === "{") depth += 1;
    if (ch === "}") {
      depth -= 1;
      if (depth === 0) return i;
    }
  }
  return -1;
}

function functionNameAt(index) {
  const before = source.slice(0, index);
  const matches = [...before.matchAll(/function\s+([A-Za-z0-9_]+)\s*\(/g)];
  return matches.length ? matches[matches.length - 1][1] : "unknown";
}

function lineAt(index) {
  return source.slice(0, index).split("\n").length;
}

function callsFor(component) {
  const pattern = new RegExp("(?:React\\.createElement|E)\\(" + component + ",\\s*\\{", "g");
  const calls = [];
  let match;
  while ((match = pattern.exec(source))) {
    const objectStart = source.indexOf("{", match.index);
    const objectEnd = matchingBrace(objectStart);
    if (objectEnd < 0) {
      calls.push({ component, index: match.index, props: "", parseError: true });
      continue;
    }
    calls.push({ component, index: match.index, props: source.slice(objectStart, objectEnd + 1) });
    pattern.lastIndex = objectEnd + 1;
  }
  return calls;
}

const interactiveCalls = callsFor("InteractiveBox").filter((call) => {
  return !/\bvariant\s*:\s*["']lab["']/.test(call.props);
});
const choiceQuizCalls = callsFor("ChoiceQuiz");
const tryCalls = interactiveCalls.concat(choiceQuizCalls);
const missing = tryCalls.filter((call) => call.parseError || !/\binstructions\s*:/.test(call.props));

if (missing.length) {
  console.error("TRY IT instruction check failed:");
  missing.forEach((call) => {
    console.error(`  ${call.component} in ${functionNameAt(call.index)} at index.html:${lineAt(call.index)} has no instructions prop.`);
  });
  process.exit(1);
}

console.log(`TRY IT instruction check passed: ${tryCalls.length} activity call sites include instructions.`);
