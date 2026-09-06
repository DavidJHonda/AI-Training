# Hallucination — evaluation

Source: `Prompts/Hallucination.mp4` · 3:21 · September 5, 2026

**Recommendation: repair.** The video teaches the lesson’s central distinction and has enough narration to use our current boards. I would not reroll it for the issues below.

## What works

The Spotify example at 0:00–0:26 makes invented precision memorable: a real institution, plausible numbers, and a nonexistent study. The four reasons at 1:00–1:22 explain why fluent answers can be wrong. The pizza story at 1:35–2:26 correctly teaches the useful distinction between fabricating a claim and misinterpreting a real source. The final two sentences at 3:10–3:18 match the lesson’s takeaway.

## Owner decisions — recorded September 5, 2026

The approved repair has now been rendered as `Prompts/hallucination-patched.mp4` (3:01.53). This is a review candidate; the source and live video are unchanged.

- **Approved new cut, approximately 0:36–0:40:** remove “weaving a lie into an otherwise plausible framework.” Keep the preceding invented-metrics/real-institutions explanation, then transition to the hallucination definition. “Lie” implies intentional deception.
- **Approved:** cut the 0:45–0:51 “weaponizing” sentence.
- **Approved:** cut 1:06–1:08 “It doesn’t retrieve facts.”
- **Approved narrower cut:** owner approved the revised recommendation with “great. build it please.” Remove only “These fabrications are a core feature of the architecture” at approximately 1:22–1:26. Keep the mechanism explanation at approximately 1:26–1:35.
- **Approved:** remove the “most effective digital literacy skill” / “intuition trigger” sentence at approximately 2:43–2:48 (owner refers to 2:42–2:48). Preserve a grammatical transition into the following practical explanation.
- **Keep 2:57–3:10 narration.** Owner likes it. Replace the “VERIFY ALL CLAIMS” graphic; do not execute the original optional narration cut.
- **All visual repairs below approved**, including current boards, illustrated pizza board, replacement of the invented Reddit screenshot and productivity-study graphic, and the standard close.

## Original suggestions — superseded where owner decisions above differ

1. **0:45–0:51 — Cut “weaponizing” the confident tone.** It makes the system sound like it is deliberately manipulating the student. The convincing-tone point has already landed; the following question explicitly says the software has no personal agenda.
2. **1:06–1:08 — Cut “It doesn’t retrieve facts.”** That blanket statement conflicts with retrieval-enabled AI and with the real-source example later in this video. The token-generation explanation remains intact without it. Retrieval and generation can coexist; the [original RAG paper](https://arxiv.org/abs/2005.11401) explicitly combines the two.
3. **1:22–1:35 — Cut the added architecture summary.** “Fabrications are a core feature” and “exactly what it was built to do” overstate the point. We already have the better formulation immediately before it: probable does not mean true.
4. **2:43–2:48 — Remove the “most effective digital literacy skill” / “intuition trigger” sentence.** Keep the practical instruction that follows about noticing when a claim does not add up. We should not give an invented label or imply intuition is the best test of truth. At editing, check whether the following “It’s paying attention…” can begin naturally; do not leave an orphaned phrase.
5. **2:57–3:10 — Optional cut.** “Inherent unreliability” and the passive-consumer/active-investigator summary add a heavier message than needed. The exact close is clearer. The accompanying “VERIFY ALL CLAIMS” graphic also conflicts with the preceding instruction not to check every syllable; replace that graphic even if we retain the narration.

## Board and visual plan

- **0:09–0:26:** current `hallucination-example-v2.jpg`, with the full AI bubble and full takeaway banner highlighted in spoken order.
- **1:00–1:22:** current `hallucination-why-v2.jpg`. All four teaching points are present; normal board treatment is sufficient.
- **Approximately 2:01–2:19:** insert `hallucination-real-text-v2.jpg`. The narration already explains real joke → wrong interpretation, so the Nate and Luke board can be inserted without a new upload version. Preserve some of the generated pizza setup before it.
- Replace the invented “PizzaTroll” screenshot at about **2:01–2:10** rather than presenting it as the actual historical post. Likewise, do not present the generated 75%-productivity chat at **2:38–2:46** as a sourced statistic; a source-check visual without an invented study would fit.
- **3:10–end:** current lesson close; remove the Notebook end card.

Google’s own account supports the pizza example as misuse of sarcastic forum content. This is worth keeping, not cutting for technical pedantry. [Google’s explanation](https://blog.google/products-and-platforms/products/search/ai-overviews-update-may-2024/)

No lesson-source change was made. Exact source/output timings and measured highlight bounds are recorded in `Hallucination/patch/manifest.json`.

## Render verification

### Subsequent approved Flow-board integration

The owner approved the new three-step EE-FLOW and requested it in the lesson and video. The latest `Prompts/hallucination-patched.mp4` now uses `illustrations/hallucination-check-claim-v1.jpg` in both former temporary-card spans. New audit artifacts are in `Hallucination/patch-flow/`; the older `patch/` folder documents the initial version below.

- Added the exact approved board immediately before `closeBoard("hallucination")`, including hidden Markdown export text. No em dashes were added. The lesson's other content was preserved, verified by removing only the inserted block and matching the pre-edit SHA-256.
- Added the byte-identical prep asset `lessons/hallucination-4-check-claim.jpg`, moved the closing prep board to `hallucination-5-close.jpg`, and updated the Markdown, upload prompt, and board manifest. The prompt is 430 whitespace-delimited words.
- Replaced temporary-card highlights with full-width, complete step areas in purple, blue, and teal. Inspected all three states and every-frame strips for the four changed board boundaries. All 15 automated transition checks pass.
- Duration remains 5,446 frames / 181.53 seconds. Decoded audio is identical to the previously reviewed candidate: SHA-256 `a806bb55378c01bb4631838b65ed83d972fcef45e7ad0d24a53ba2433a014886`.
- `node scripts/test_hallucination_check_claim.cjs` passes: component rendering, placement before the close, complete export copy, matching asset bytes, valid prompt filenames, and prompt under 500 words.
- The live video has not been replaced. This remains the updated review candidate.

### Initial patch checks

- Final candidate decodes to 5,446 frames at 30 fps (181.53 seconds).
- All 15 declared output-timeline edit boundaries passed the transient-graphic detector. Every-frame strips were also visually inspected; no discarded-board islands were found.
- Every settled highlight state and the literal final frame were inspected. Full AI bubble, full takeaway banners, and complete four-reason columns are enclosed without intersecting text.
- All five audio joins land in measured quiet regions (20 ms seam levels approximately −52 to −66 dBFS). A word-timestamp transcription of the exported seam reel confirms the retained neighboring words and the intended cuts. This is waveform/ASR verification, not a claim of a human listening pass.
- The “It’s paying attention…” continuation remains intact after the guardrails sentence; no words were synthesized.
- Generated source-check cards replace the invented productivity-study graphic and “VERIFY ALL CLAIMS.” The illustration with Nate and Luke replaces the fabricated Reddit screenshot.
- Source MD5 was checked before and after rendering. Live video, `index.html`, and lesson assets were not modified.

Build: `scripts/video/build_hallucination_review.py`. QA: `scripts/video/qa_hallucination_review.py`. Review artifacts: `Hallucination/patch/qa/` and `Hallucination/patch/transitions/`.
