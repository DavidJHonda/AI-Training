# Where’s the Line video evaluation

The installed 3:21.97 video preserves the lesson’s teaching arc and covers all essential teaching points. Retain its core explanation and useful supporting scenes. Prioritize breaking up the long board runs, correcting the company-response graphic, and checking the absolute wording about AI obedience. This is a provisional editorial assessment, not an audio or shipping signoff.

## Scope and evidence

- Reviewed September 30, 2026 against `index.html`, `lessons/wheres-the-line.md`, the current generation prompt, canonical boards, and current video workflow.
- File: `course-assets/wheres-the-line/wheres-the-line.mp4`; page entry uses `?v=20260923ship2`.
- SHA-256: `848ac733051b1a1ad1856fbb60099b54e2978ce7651027d5f7e7575cad47ff51`. Exact match to the retained September 23 v2 build manifest. All three canonical JPG hashes also match that manifest.
- Fresh full-file automatic transcript: `wheres-the-line/transcript.txt`. Five contact sheets in `visuals/` cover the complete runtime at four-second intervals. Source boards inspected directly.
- A fresh sequential frame-analysis pass completed, reporting 30 fps and 3:21.97. Independent board matching (`board-spans.txt`, 0.5-second sampling) measured 33.5 seconds for the first board and 47.5 seconds for the second, consistent with the exact manifest spans and the hold before the close.
- LISTENING: No direct auditory audition. Motion was sampled as frames, not watched continuously with sound. No claims about voice continuity, clicks, pronunciation, natural pauses, or animation smoothness are certified here. A final KEEP / REPAIR / REROLL narration verdict is withheld pending these checks and resolution of the wording concern below.
- The current file and lesson were not changed. Local installation was verified; public deployment and the external Video Tracker were not verified.

## Teaching coverage

Ratings below describe transcript coverage; uncertain ASR is explicitly separated from confirmed wording defects.

| Teaching point | Coverage | Current video evidence |
|---|---|---|
| Human responsibility and choosing tasks with affected people in mind | TAUGHT | 0:00–0:13, “we the people are responsible” and “identifying everyone affected.” The explicit prompts/answers contrast is compressed without losing the central distinction. |
| Ethics means considering what to do and effects on others | RICH | 0:13–0:21, retains both halves of the definition. |
| DraftKings, casino games, sports bets, and shared casino incentive | TAUGHT | 0:30–0:41, including “The company earns money when customers lose.” |
| Some people struggle to control gambling; consequences | RICH | 0:41–0:53, connects difficulty controlling gambling to finances, health, and relationships. |
| Digital activity records and patterns AI can identify | RICH | 0:53–1:05, frequency, bet size, and losses. |
| Promotion thought experiment and example email | RICH | 1:05–1:21, predicting further losses after offers; exact email example appears in ASR. Clearly introduced as a thought experiment. |
| Protection thought experiment | TAUGHT | 1:21–1:32, early recognition and help instead of promotions. |
| Ethical question | TAUGHT | 1:32–1:37, when DraftKings should stop encouraging potentially harmful play. |
| Reporting attribution | TAUGHT | 1:37–1:41, New York Times investigation. |
| Promotion system and deployment outcome | TAUGHT, pronunciation check pending | 1:41–1:58, user habits, greater losses after incentives, deployed and continued development. ASR renders a likely “predict” as “permit” at 1:43–1:48; do not call this a spoken error without listening. |
| Protection system and nondeployment | RICH | 1:58–2:11, employees developed a separate predictive system; company chose not to use it. |
| Company response and limits of evidence | RICH | 2:11–2:22, disputed targeting, existing monitoring, insufficient evidence for the proposed system. |
| Successful task execution can still harm people | TAUGHT intent; wording concern | 2:22–2:27, “AI will do exactly what it is asked to do” overstates the source lesson. See below. |
| Transition from case to action | TAUGHT | 2:27–2:31, “Making responsible choices requires four specific moves.” |
| Consider everyone affected | RICH | 2:31–2:42, harm, exclusion, and pressure beyond beneficiaries. |
| Be clear with people | TAUGHT | 2:42–2:50, explain operation and effects on choices. |
| Build in protection | RICH | 2:50–2:59, test for harm, boundaries, and challenges to mistakes. |
| Own the outcome | RICH | 2:59–3:09, monitor, change, or stop the system. |
| Responsible decision takeaway | TAUGHT | 3:09–3:14, “A responsible decision considers the people who live with it.” |
| Both closing lines | TAUGHT | 3:14–3:18, “We the people make the call” and “What should AI do? That’s our responsibility.” |

All seven required verbatim lines are represented in the fresh ASR, subject to auditory confirmation. The on-page scenarios are intentionally omitted by the generation prompt; that is not a missing teaching beat.

SOURCE_QA: No discrepancy identified between the page’s intended teaching and the local source record. Independent verification of the full NYT investigation remains incomplete: both the article and a search-discovered NYT-hosted copy failed to open. Do not treat search snippets as a complete fact-check. No source-text correction is proposed.

## Prioritized findings

1. **Long uninterrupted boards reduce visual variety.** “How DraftKings Uses AI” occupies 1:36.60–2:10.50, 33.9 seconds. “Making the Responsible Choice” occupies 2:25.67–3:12.77, 47.1 seconds, with the preceding visual also held through the short close transition. These exact spans come from the hash-matched manifest and are consistent with fresh frame samples. Narration continues teaching throughout: this is not dead air and does not justify cutting explanations. The four-card camera moves improve legibility, but they do not provide the supporting-scene breaks requested by Edit Spec 8b.
2. **Company-response graphic can imply a different claim.** At 2:14.10–2:21.70, the “Audit” graphic checks “Current Safety Protocols” and crosses out “New Algorithm Testing.” The narration reports insufficient evidence and nondeployment, not a simple refusal to test. The check also risks looking like independent certification of current safeguards. Prefer a targeted label correction: explicitly attribute it to the company, say “Existing monitoring,” and “Predictive system not adopted.” Preserve the short scene if those labels can be repaired cleanly.
3. **AI obedience wording needs checking and correction.** At 2:21.72–2:27.16, ASR says, “AI will do exactly what it is asked to do, even if the end result is harming people.” The page’s conditional statement is more accurate: “AI can do what it’s asked while still harming people.” Keep the ethical distinction without implying guaranteed compliance. No verified existing audio donor has been identified for this replacement; the old raw-roll paths in the manifest are absent from `Prompts/`. A written replacement is not yet an executable audio repair. Audition this passage before choosing a repair source or a new generation.
4. **Optional economy at the introduction to the case.** 0:21.44–0:30.28 takes almost nine seconds to announce a real-world business model before naming DraftKings. A shorter bridge could get to the example faster. This is optional, not missing or wrong teaching, and no cut is proposed without listening to the joins.

The opening diagrams also use technical labels such as “Impact Propagation” and “Behavioral Extraction.” The simpler narration carries the meaning, so these are secondary readability concerns rather than a reason to replace all supporting graphics. The hypothetical promotion graphic’s “Vulnerability Exploited” wording at roughly 1:15–1:21 is stronger than the narration; if revisited, use a neutral outcome description while keeping the useful offer-flow explanation.

## Proposed production plan

Evaluation only. Timing below is an initial visual plan; inspect full-resolution frames and motion, and finalize narration onsets before building. No added silence is proposed.

| Board | Highlighting sequence | Camera | On screen and proposed breaks | Purpose |
|---|---|---|---|---|
| How DraftKings Uses AI | Targeted Promotions whole card → its What They Did section → Customer Protection whole card → its What They Did section | Preserve complete unmarked opening and full-board treatment; preview full-resolution body-text readability before considering a complete-card dive | Currently 1:36.60–2:10.50. Proposed roughly 1:47–1:50 supporting offer scene, returning before the deployment outcome; roughly 2:03–2:06 early-support scene, returning before nondeployment. About 28 seconds total board exposure, in shorter runs. | Keep the two different outcomes clear while interrupting the long static view. Reuse the installed offer/help illustrations only after checking their labels and motion; avoid introducing a new factual claim. |
| Making the Responsible Choice | Consider Everyone Affected → Be Clear With People → Build In Protection → Own The Outcome; one whole-card outline for each | Preserve full-view introduction, complete-card dives, and summary pullback | Currently 2:25.67–3:12.77. Proposed 2:37–2:41 supporting scene showing affected people; 2:55–2:58 scene showing a test and a way to challenge a result. Return settled before each next move. About 40 seconds total board exposure; longest proposed run approximately 15 seconds. | Make the four actions concrete. Existing gambling/keyboard drawings do not clearly teach both actions; propose purpose-built supporting images rather than irrelevant filler. |
| We the People Make the Call | Unmarked | Preserve canonical close and existing hold/push/settle design | Starts 3:13.27; retains the two spoken lines and final hold through 3:21.97 | Strong concise ending; no proposed copy change. |

Use the current fixed 4 px delivery-frame ring width in a future build. Fresh measurements in `ring-stroke.txt` found roughly 4–5 px on the first board and 8.5–9 px in the second board’s zoomed views. The installed video predates the fixed-width rule; the spec explicitly says old ring width alone is not a reason to rebuild.

## Supporting scenes to retain

- 0:00–0:07.73: parchment provides a direct visual connection to “we the people.”
- 0:07.73–0:21.17: task/affected-population diagrams show why choice and consequences belong together. Simplify labels only if the scene is otherwise being repaired.
- About 0:21–0:53: phone/chips, revenue comparison, and consequences establish the case and its stakes. The $100 comparison is illustrative, not a claimed measured statistic; no removal is needed solely because it uses numbers.
- About 0:53–1:05: event stream and pattern graphic connect behavior to prediction; sampled reveal states are coherent, but motion still needs viewing.
- 1:02.70–1:14.90: roulette and betting-phone cutaways provide visual variety.
- About 1:15–1:31: the two thought-experiment flows help students compare possible goals; preserve that comparison and review the stronger outcome label noted above.
- About 1:31–1:36.60: “Where Is the Line?” reinforces the central question.
- 2:21.70–2:25.67: keyboard graphic bridges from the case to responsibility, subject to the narration wording check.

No photograph or engine-corner-mark defect was apparent in the sampled frames. This does not certify every frame. No new pauses, audio cuts, builds, source changes, commits, shipping, or publishing were performed.
