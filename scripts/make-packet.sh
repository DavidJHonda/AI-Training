#!/usr/bin/env bash
# Regenerate the downloadable Start Smarter packet. Welcome is intentionally omitted:
# it is course orientation, not quiz material. Each of the seven learning lessons is
# rendered as ONE continuous-height PDF page (exactly like the individual lesson
# downloads, so no box or paragraph is ever split by a page break), then the pages are
# merged in course order into packets/start-smarter.pdf. The per-lesson PDFs are a
# build intermediate only: the course no longer ships them (2026-09-12), so they are
# removed from tmp/lesson-pdfs/ once the packet is merged.
# Rerun whenever the Start Smarter lessons change. Usage: bash scripts/make-packet.sh
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p packets
PACKET="packets/start-smarter.pdf" bash scripts/make-lesson-pdfs.sh \
  whydeeper llms aihistory doesaithink control whybother studying
rm -f tmp/lesson-pdfs/*.pdf
echo "Removed the per-lesson PDF intermediates from tmp/lesson-pdfs/ (downloadable keepsake PDFs are preserved)." 
