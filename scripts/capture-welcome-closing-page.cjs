// Compatibility entry point. Welcome now uses the same canonical generator as
// every other lesson instead of maintaining a separate page-only variant.
const { spawnSync } = require("node:child_process");
const path = require("node:path");
const result = spawnSync(process.execPath, [
  path.join(__dirname, "generate-closing-boards.cjs"),
  "--lesson", "welcome"
], { stdio: "inherit", env: process.env });
if (result.error) throw result.error;
process.exitCode = result.status == null ? 1 : result.status;
