# AI Is Different: three-roll narration review and edit plan, 2026-09-26

Sources: `Prompts/ai-is-different-1.mp4` (4:31), `-2.mp4` (4:22), `-3.mp4` (3:31), rolled from the 2026-09-26 kit
(`video-audit/ai-is-different-reroll-prep-2026-09-26/`). The transcripts (faster-whisper small.en, with doubtful
spans re-checked on medium.en) are in `transcripts/`, board spans in `spans-N/`, scene cuts in `scenes-N.txt`, and
contact sheets in `sheet-N/`. Voice check: median F0 is 172, 176, and 174 Hz, with matching quartiles, so the same
narrator voice appears in all three rolls. This is not a listening pass.

**Status: plan only. Nothing built. Awaiting David's approval (Edit Spec 1b).**

## Verdicts

| Roll | Verdict | Why |
|---|---|---|
| 1 | **REPAIR, BASE** | Every plan item is present in order: superpowers → foundation, Superman *before* the risks, both tool choices, training + guardrails with both failure modes, all three risks, both closing lines verbatim. Five narrow gaps, all with identified donors (below). |
| 2 | REROLL alone | No closing lines (it ends "…will always come with these inherent risks"), no Superman comparison, no PS5 titles, no app qualifier. It has the best legal-pad story and the fullest input/output sentence, which become donors. |
| 3 | REROLL alone | No app qualifier, and no PDFs, audio, or first-draft examples. Risks are compressed into one clause. It says "probabilistic" (a banned word) and adds "exciting" to closing line 1. Its "Spider-Man 2 every single time" line and its robot beat become donors. |

## Plan checklist against roll 1 (as rolled)

| Plan item | Roll 1 | Rating |
|---|---|---|
| 1 Superpowers → foundation; Superman before weaknesses | 0:00 "It has superpowers…"; 3:22.9 "A human can hold kryptonite safely in a backpack, but for Superman, it can be fatal." (before risks at 3:42) | RICH |
| 2 Inputs/outputs + app line | 2:54 "messy notes, PDFs, or audio files … a summary or a clean first draft"; 3:03 "While the available inputs and outputs depend on the app, the flexibility remains." | TAUGHT (5 of 8 examples; pictures, table, image missing) |
| 3 Both tool choices | 3:08 "Normal software still wins for exact, consistent jobs like GPA math, but AI earns its place on the open-ended, messy jobs that defy rigid rules." | RICH |
| 4 Both safety approaches + limits | 3:59–4:19 training, "a safety layer to the apps, guardrails", "block harmless requests or miss dangerous ones" | RICH |
| 5a Passwords | 0:27–0:40 both outcomes | RICH |
| 5b Robot vs chef | 1:20–1:39 | RICH (slip: "Think **as** normal software as a robot") |
| 5c All three PS5 answers | Preset-list rule spoken; normal side "repeats the exact same answer" (Spider-Man 2 never named); AI side names NHL 26 + God of War | TAUGHT (Spider-Man 2 unnamed) |
| 5d Receipt + text message | 2:24–2:30 | RICH |
| 5e Legal pad | 2:31 "Think about drafting a lesson plan from chaotic legal pad notes… doesn't give you a usable lesson document" | THIN (hypothetical; it doesn't say *this lesson* was written that way or that AI made the draft) |
| 5f Three risks | Scams that scale, deepfakes, confident but wrong (+ "hallucinate") | RICH |
| 5g No "absolute certainty" | Not present | PASS |
| Closing lines | 4:22.5 / 4:25.4 verbatim | MET |

Other verbatim lines: MET for "Written rules…", "Learn patterns first…", "Rules repeat… / Patterns build…",
"Trained behavior is harder…", "During training…", and "They also add a safety layer…". Near misses: "AI is built on a
**completely** different foundation"; "You bring the mess, **and** AI helps make sense of it" (harmless); and the app line
spoken as a clause (meaning intact).

## Best-of plan

```text
BEST-OF PLAN: ai-is-different
BASE: ai-is-different-1.mp4 (only roll with every plan item, Superman-before-risks, verbatim close)
  Robot beat — r1 RICH-with-slip @1:20.6 "Think as normal software as a robot perfectly executing a rigid recipe…" | r3 RICH @1:09.6 "To visualize this, think of normal software as a robot following a recipe in a cookbook. Someone wrote every step, and the robot follows the rules to make the exact same dish every time." — TAKE r3 (scene graft with r3's own watercolor robot drawings)
  PS5 normal side — r1 TAUGHT @1:51.7 "Ask again, and it repeats the exact same answer." | r3 RICH @1:47.3 "It repeats Marvel's Spider-Man 2 every single time you ask." — TAKE r3 (under Rules vs. Patterns board)
  Legal pad — r1 THIN @2:31.2 (hypothetical) | r2 RICH @2:30.3 "This lesson started as a series of handwritten notes on a legal pad, with lines crossed out and ideas moved around. And AI was able to recognize the patterns in those messy notes and organize them into a clean first draft." — TAKE r2 (scene graft with r2's legal-pad drawing)
  Inputs/outputs — r1 TAUGHT (notes, PDFs, audio → summary, draft) | r2 TAUGHT @2:50.0 "AI is flexible, taking unstructured inputs, like a PDF or a photo, and transforming them into a summary, table, or image." — TAKE BOTH (r2 inserted after r1's sentence; together they name all 8)
GRAFTS: 4 (2 under boards, 2 whole-scene grafts carrying their own drawings)
```

## Proposed narration changes (roll 1 timeline)

| # | Change | Source words / times | Net |
|---|---|---|---|
| N1 | Replace robot sentence | cut r1 80.56–87.92; insert r3 69.60–80.12 | +3.2 s |
| N2 | Name Spider-Man 2 | cut r1 111.70–113.86; insert r3 107.28–110.34 | +0.9 s |
| N3 | Legal-pad story | cut r1 151.22–161.06; insert r2 150.26–162.88 | +2.8 s |
| N4 | Add photo/table/image | insert r2 169.96–177.50 after r1 "…clean first draft." (182.52) | +8.3 s |
| N5 | Cut "So remember the rule." | cut r1 197.22–198.92 ("rule" collides with the lesson's technical *Rules*) | −1.7 s |
| N6 *(optional)* | Excise "completely" from the foundation line | r1 9.46–9.84; single-word splice, audition, and drop if the join isn't clean | −0.4 s |

All joins fall in sentence gaps of 0.56–1.26 s. Known risk: N4 says "AI is flexible" and r1 then says "the flexibility
remains", which is mildly repetitive. Output ≈ 4:40 including the standard close.

## Board plan (Edit Spec 1b); treatments reuse the approved v8/v9 densities

| Board | Highlighting | Camera | On screen / breaks | Notes |
|---|---|---|---|---|
| Rules Look Like This | User enters password → IF → THEN → ELSE → banner, at spoken onsets | full board (compact) | ~18 s, no break | under 20 s |
| Two Ideas Behind Every Answer | Training 0:54.2 → Patterns 0:58.1 → Probability 1:06.5 → Prediction 1:12.5 → banner 1:16.9 | full board (compact) | ~13 s, **break** 1:03.3–1:06.3 to r2 "Learned Patterns → Constructing Response" drawing (r2 ~1:20) under "Once trained, it answers one word at a time", then ~14 s | the drawing's faint % bars are illustrative |
| Rules vs. Patterns | Question → Normal Software column (through N2) → NHL 26 → God of War → pull back for banner | dense: dive/pan as v9 | intro under r2 controller+phone drawing (~3 s); board ~12 s; **break** under "Ask AI software that exact same prompt… word by word using learned patterns" to r3 "AI Software / learned patterns" network (r3 ~0:09–0:15, ~6 s); board ~10 s | Spider-Man 2 first ask on the AI side stays unspoken (board shows it) |
| Structured vs. Unstructured Data | Normal Software col → AI Software col → app line → (after tool-choice drawing) banner | dense: dive/pan as v9 | board ~12 s; **break** under N4 region: r2 "Unstructured real-world data" (email/receipt/notes/audio, r2 ~2:22–2:30) then r3 "unstructured input → AI → summary/table/draft" (r3 ~2:38–2:41); back ~1 s before the app line (~5 s); r1's own tool-choice drawing (calculator/messy notes) unchanged; board ~3.5 s for "You bring the mess" | |
| AI's Kryptonite | Scams → Deepfakes → Confident but Wrong | full board (compact) | ~20.5 s, **no break proposed** | at the threshold; the three risks are one continuous sentence run with no clean seam. Banner was spoken just before the board (under r1's own rules-vs-patterns drawing), so it stays unringed |
| Close | standard close | standard motion | from "This graphic sums up the trade-off." (4:19.9) | Notebook's close replaced |

Other visual changes:
- **0:11.6–0:15.7 floppy disk: MUST GO.** It's photoreal and shows a Microsoft Excel logo. Replace it with r2's calculator drawing (r2 0:14.3–0:18.4) under "To see how different it is, consider how normal software is created."
- **Kryptonite hook (3:22.8–3:28.1):** swap r1's "protective case" drawing for r3's kryptonite-in-a-backpack drawing (r3 ~2:41–2:49), which shows what the narration says.
- Every other Notebook span in roll 1 stays: the opening foundation diagrams, "NOT HOW AI OPERATES", robot/chef (after N1), the GPA table, the receipt and text, the tool-choice drawing, and both guardrail-layer drawings.

## Selective pauses

| At | Reason | Existing | Proposed total | Adds |
|---|---|---|---|---|
| after "Patterns build a fresh one." (r1 2:10.4) | change of subject into structured data | 0.74 s | 1.2 s | +0.46 s |
| after "…AI helps make sense of it." (r1 3:22.2) | superpowers → Kryptonite turn | 0.68 s | 1.3 s | +0.62 s |

## Open items
- No listening pass yet. Every graft, N6, and the "Think as" slip (removed by N1) still need David's ears on the candidate.
- The longest unbroken board after the edit is Kryptonite at ~20.5 s.
