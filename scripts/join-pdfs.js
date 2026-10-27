// Preserve Chrome's embedded fonts and searchable text. PDFKit converted body
// text to outlines during merging, leaving only headings extractable.
// Usage: node scripts/join-pdfs.js [--min-text-chars N] out.pdf in1.pdf ...
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const localPython = path.join(__dirname, "../.video-venv/bin/python3");
const python = process.env.PDF_PYTHON || (fs.existsSync(localPython) ? localPython : "python3");
execFileSync(python, [path.join(__dirname, "join-pdfs.py"), ...process.argv.slice(2)], { stdio: "inherit" });
