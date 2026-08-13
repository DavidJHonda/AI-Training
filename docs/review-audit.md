You are auditing index.html, a single-file React AI-literacy course, for engineering
and QA issues only — NOT content or teaching. Design token/font/shadow drift is already
covered by design-check.sh; don't re-report those. Triage, ranked, capped.

File: [paste index.html or the relevant range]

Check for:
- Broken/duplicate lesson IDs; NextLessonGate targets that point at the wrong or a
  removed lesson. Every ID routed by SECTION_GROUPS must resolve in both SECTION_META
  and SECTION_COMPONENTS; extra unrouted entries are drift, not a routing bug.
- Missing or broken Previous/Next behavior; code or copy that still assumes advancement
  is gated. NextLessonGate is intentionally always available and currently ignores
  ready/lockedMessage. Also check localStorage/reset/"visited" edge cases.
- Dead or duplicate components, unused variables, copy-paste leftovers, broken references.
- TRY IT or LAB activities whose state, feedback, completion, or labels are broken;
  static demonstrations incorrectly implemented as activities; inline styles that should
  be tokens (beyond what design-check counts).
- Componentization: repeated card/inline-style patterns worth standardizing.

Output this and NOTHING else, grouped:
- 🔴 Bugs (breaks behavior): [file:line] problem → fix — MAX 8
- 🟡 Drift / dead code: [file:line] problem → fix — MAX 8
- 🟢 Maintainability / componentization: one-line opportunities — MAX 6
- If a category is clean, write "clean" and move on. Ranked by impact within each group.
