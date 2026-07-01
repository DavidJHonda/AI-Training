You are auditing index.html, a single-file React AI-literacy course, for engineering
and QA issues only — NOT content or teaching. Design token/font/shadow drift is already
covered by design-check.sh; don't re-report those. Triage, ranked, capped.

File: [paste index.html or the relevant range]

Check for:
- Broken/duplicate lesson IDs; NextLessonGate targets that point at the wrong or a
  removed lesson; SECTION_GROUPS vs SECTION_META/SECTION_COMPONENTS mismatches.
- Gates that never unlock or unlock too early; localStorage/reset/"visited" edge cases.
- Dead or duplicate components, unused variables, copy-paste leftovers, broken references.
- Activities that don't follow the intended TRY IT / SEE IT pattern; inline styles that
  should be tokens (beyond what design-check counts).
- Componentization: repeated card/inline-style patterns worth standardizing.

Output this and NOTHING else, grouped:
- 🔴 Bugs (breaks behavior): [file:line] problem → fix — MAX 8
- 🟡 Drift / dead code: [file:line] problem → fix — MAX 8
- 🟢 Maintainability / componentization: one-line opportunities — MAX 6
- If a category is clean, write "clean" and move on. Ranked by impact within each group.
