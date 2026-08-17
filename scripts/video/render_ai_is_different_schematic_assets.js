#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const repoRoot = path.resolve(__dirname, '../..');
const assetsDir = path.join(repoRoot, 'board-review-first-four/assets/ai-is-different');
const sourceDir = path.join(assetsDir, 'schematic');

const assets = [
  ['scams-that-scale.svg', 'scams-that-scale.png'],
  ['deepfake-real-person.svg', 'deepfake-real-person.png'],
  ['confident-but-wrong.svg', 'confident-but-wrong.png'],
];

async function main() {
  for (const [sourceName, outputName] of assets) {
    const source = path.join(sourceDir, sourceName);
    const output = path.join(assetsDir, outputName);
    if (!fs.existsSync(source)) {
      throw new Error(`Missing schematic source: ${source}`);
    }
    await sharp(source, { density: 144 })
      .resize(512, 360, { fit: 'contain' })
      .png()
      .toFile(output);
    process.stdout.write(`Built ${output}\n`);
  }
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exit(1);
});
