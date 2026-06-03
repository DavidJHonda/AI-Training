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

# baseline 3: 2 counter pills + 1 section-overview "NN / 10" badge (shared renderOverview)
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
chk "em-dashes in copy" 4 \
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
