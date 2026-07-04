#!/usr/bin/env bash
# design-check.sh - pre-ship consistency check for index.html
# Run from repo root before shipping a new lesson:  bash design-check.sh
F="index.html"
fail=0

chk() {  # label  expected  actual
  local label="$1" exp="$2" act="$3"
  if [ "$act" = "$exp" ]; then
    printf "  OK   %-42s %s\n" "$label" "$act"
  else
    printf "  FLAG %-42s %s (expected %s)\n" "$label" "$act" "$exp"
    fail=1
  fi
}

echo "Design consistency check on $F"
echo "----------------------------------------------------"

# baseline 3: 1 counter pill (the ActivityCounter component def — still used by
#   LAB boxes; TRY ITs carry no counters per David 2026-07-03, so the Put It In
#   Order hand-rolled pill was removed) + 1 evidence pill + 1 autoregressive
#   word-chip (added 2026-06-06; the "It -> is -> going -> to -> rain" generation
#   strip in AIIsMath "Tying the math together" box). All deliberate, not counters.
#   The section-overview "NN / N" badge in renderOverview was removed 2026-06-06.
chk "hand-built counter pills" 3 \
  "$(grep -oF 'borderRadius: 999, padding: "6px 14px"' "$F" | wc -l | tr -d ' ')"
chk "Source Serif reintroduced" 0 \
  "$(grep -oE 'Source.Serif' "$F" | wc -l | tr -d ' ')"
chk "raw fontFamily off-allowlist" 0 \
  "$(grep -oE 'fontFamily: "[^"]*"' "$F" | grep -vE 'var\(--(sans|serif|mono)\)' | grep -vF '"inherit"' | grep -vF '"Segoe UI, sans-serif"' | wc -l | tr -d ' ')"
chk "raw mint hairline (non-token)" 1 \
  "$(grep -oF 'rgba(63, 107, 63, 0.18)' "$F" | wc -l | tr -d ' ')"
chk "raw mint surface #eef4eb" 1 \
  "$(grep -oF '"#eef4eb"' "$F" | wc -l | tr -d ' ')"
chk "literal --shadowSoft value" 1 \
  "$(grep -oF '0 4px 12px rgba(14, 10, 31, 0.05)' "$F" | wc -l | tr -d ' ')"
chk "literal --shadowElevated value" 1 \
  "$(grep -oF '0 8px 22px rgba(14, 10, 31, 0.05)' "$F" | wc -l | tr -d ' ')"
# Near-miss lavender: outer bands use var(--primaryFaint), not this lookalike hex
# (normalized 2026-06-10: opener overview band + 2 Embeddings taste profiles).
chk "near-token lavender #f3f1fa" 0 \
  "$(grep -oF '#f3f1fa' "$F" | wc -l | tr -d ' ')"
# Page background as an outer band fill: lesson-level boxes use var(--primaryFaint)
# borderless; var(--bg)+rule-border stays an INTERIOR treatment only
# (normalized 2026-06-10: HowWeGotHere timeline, Training phases x3, WorkChanges value box).
chk "page-bg used as outer band" 0 \
  "$(grep -oF 'background: "var(--bg)", border: "1px solid var(--rule)", borderRadius: 12, padding: 24' "$F" | wc -l | tr -d ' ')"
# 3 = validate() JS comments (not copy). The "words — analogy" context-window-size
# line left with the CONTEXT_WINDOW_FACTS cut (parked for Inference, 2026-07-02).
# (The 3 "not magic / not a person / not a truth machine" myth em-dashes were
#  converted to colons 2026-06-19; InferenceJourneyDiagram was rewritten em-dash-free
#  2026-06-18.)
# The verbatim White House quote in whydeeper carries one more, written as the
# backslash-u2014 JS escape, so this raw-byte count doesn't see it (quotes from sources
# keep their original punctuation; our own copy still avoids em-dashes).
chk "em-dashes in copy" 3 \
  "$(grep -oF '—' "$F" | wc -l | tr -d ' ')"

echo "----------------------------------------------------"
if [ "$fail" = 0 ]; then
  echo "PASS - no new drift against baselines."
else
  echo "FLAG - a count is above baseline. A FLAG is not always a bug:"
  echo "  - new counter pill   -> use ActivityCounter instead of hand-building"
  echo "  - new raw font       -> use var(--sans) / var(--serif) / var(--mono)"
  echo "  - new shadow literal -> use var(--shadowSoft) / var(--shadowElevated)"
  echo "  - new mint divider   -> use var(--tryRule); new mint surface -> var(--tryBand)"
  echo "  - new em-dash        -> rewrite the copy without it (course style avoids them)"
  echo "  - deliberate diagram/assessment exception -> bump the expected number"
  echo "    on that check line so future runs stay meaningful."
fi
