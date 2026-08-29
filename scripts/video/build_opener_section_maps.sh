#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
exec "$repo_root/.video-venv/bin/python" "$repo_root/scripts/video/render_opener_section_maps.py"
