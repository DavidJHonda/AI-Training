#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -n "${COURSE_ASSET_PYTHON:-}" ]]; then
  interpreter="$COURSE_ASSET_PYTHON"
elif [[ -x "$repo_root/.video-venv/bin/python3" ]]; then
  interpreter="$repo_root/.video-venv/bin/python3"
else
  interpreter=python3
fi
exec "$interpreter" "$repo_root/scripts/video/course_credit.py" "$@"
