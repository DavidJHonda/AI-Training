#!/usr/bin/env bash
# Regenerate the downloadable Start Smarter packet. Each lesson is rendered as ONE
# continuous-height PDF page (exactly like the individual lesson downloads, so no
# box or paragraph is ever split by a page break), then the pages are merged in
# course order into packets/start-smarter.pdf. Also refreshes those lessons'
# individual PDFs in lessons/ as a side effect, keeping the two downloads in sync.
# Rerun whenever the Start Smarter lessons change. Usage: bash scripts/make-packet.sh
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p packets
PACKET="packets/start-smarter.pdf" bash scripts/make-lesson-pdfs.sh group:start-smarter
