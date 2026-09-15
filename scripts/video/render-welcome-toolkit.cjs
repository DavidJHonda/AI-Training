#!/usr/bin/env node
// The finished board is now the source of truth; individual artwork was retired.
// Keep this command as a lossless export helper for existing workflows.
const fs = require('node:fs');
const path = require('node:path');
const root = process.env.COURSE_RENDER_ROOT || path.resolve(__dirname, '../..');
const source = path.join(root, 'course-assets/welcome/welcome-3-course-toolkit.png');
const output = path.resolve(process.argv[2] || source);
if (!fs.existsSync(source)) throw new Error('The finished Welcome toolkit board is missing: ' + source);
if (output !== path.resolve(source)) {
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.copyFileSync(source, output);
}
console.log('Finished toolkit board: ' + output);
