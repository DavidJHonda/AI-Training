# How an LLM Works — current-spec evaluation, September 28, 2026

**Owner decision after review:** retain the 1:33–1:42 Notebook training-loop sequence because it adds variety. This explicit exception supersedes the recommendation below to replace it. David agreed with the other comments and corrected the audio-glitch location to approximately **0:44.5**, within “To see where those patterns come from, we have to look at the training process,” not the shortening join at 0:46.615. The approved visual revision is tracked in `../how-an-llm-works-repair-2026-09-28-v14/`. Earlier findings below remain as the evaluation record, not instructions to remove the approved sequence.

Recommendation: retain the shortened narration and prepare a visual refresh. The core teaching is complete in the transcript; the current production treatment does not fully meet the updated spec. No video, lesson, upload materials, or website references were changed by this evaluation.

## Exact version and review limits

- Page authority: `index.html`, `AIHistorySection`, lines 3702–3754; page ID `aihistory`. Current video cache key: `20260925ship13`.
- Evaluated file: `course-assets/how-an-llm-works/how-an-llm-works.mp4`, 1280×720, 9,114 decoded frames, approximately **5:03.8**. SHA-256: `45b48a41a26a372887653f1b5d37418e5e7689ffc04e4f957acef568b315724f`.
- This is byte-identical to the September 25 shortened v2. It is NOT the 6:22.9 file described in the September 25 pre-shortening review.
- Read the complete shortened transcript, current page, upload Markdown, prompt, Narration Review, Edit Spec, and shared workflow. Examined all seven new contact sheets, the six current page assets, and selected full-resolution encoded frames. Sequentially decoded the whole file. This is a sampled visual and transcript evaluation, **not an end-to-end playback/listening certification**.
- Reused `../how-an-llm-works-shorten-2026-09-25/transcript-shortened.txt` only after verifying that its candidate's AAC payload and the current video's AAC payload have the same SHA-256: `cf5cc83ef08ba5623c0c8559c0f2737a36709361fb700f5f77a676e39a6fa4d5`.
- No audio was auditioned in this review. In particular, the owner's reported glitch at 0:46 remains unresolved. Transcript completeness and a low-RMS seam do not establish that it sounds right.
- Tracker status was not accessed or changed. “Current” here means the exact locally referenced course file; remote deployment was not checked.

## Findings in priority order

1. **Long board holds remain the main engagement weakness.** “Same Word. Different Odds.” stays on screen from **2:45.70 to 3:53.73 (68.03 seconds)**. “How Training Works” runs **0:46.60–1:32.97 (46.37 seconds)**; “What's an LLM?” **0:08.47–0:46.60 (38.13 seconds)**; “One Word at a Time” **4:05.00–4:43.27 (38.27 seconds)**. These exceed the September 23 default to break individual holds over about 20 seconds with relevant Notebook drawings. They are largely active explanation, not dead air: cutting essential explanations is not the remedy. The original probability run had an explicitly approved long-board exception; the new evaluation should disclose that exception rather than describe it as an unauthorized edit.
2. **A prohibited Notebook recreation survives at 1:32.97–1:41.97.** The READ / GUESS / CHECK / ADJUST flowchart is a restatement of the course training board, with Notebook's own yellow highlighting. It is not an eligible drawing break under rules 2 and 8b. Replace it with the canonical board during the repetition explanation, or a verified relevant drawing. Simply inserting the canonical board makes that training hold about 57 seconds when joined to the brief summary; disclose that tradeoff.
3. **The training introduction arrives on the previous board.** The narrator introduces training around 0:42.7 while “What's an LLM?” remains visible. “How Training Works” arrives at 0:46.6, with only about 0.83 seconds before its first existing ring. It does have unmarked opening frames; the earlier commentary impression that it opens already highlighted was incorrect. Move the board entrance to the retained training introduction, preserving audio. The probability board's second visit likewise has only about one second of full view before its dive. Delay that dive while allowing the first spoken item to highlight in full view; do not add silence.
4. **The 0:46 audio issue is still open.** The September 25 report says the owner heard a glitch at the first shortening join (0:46.615), that no cause was established, and that v2 shipped with that join unchanged. The current file is that same v2. Audition approximately 0:42–0:50 before deciding whether an audio repair is needed. Do not call this resolved on signal measurements alone.
5. **The new ring weight applies to the next build.** The September 26 standard is a fixed 4 pixels in a 720p delivery frame, regardless of zoom. Representative detected rings in the existing encoded video read roughly 6–7 solid pixels. Automated extrema include artwork false positives and should not be treated as real highlight widths. Update rings in rebuilt spans, but **the spec explicitly says earlier shipped videos are not rebuilt solely for this change**. The README and Edit Spec checklist still contain older “5 px” wording; the dated section 5 rule takes precedence.
6. **Some retained Notebook scenes are weak or unsuitable donors.** At 2:04.03–2:14.30, “Structural Sequence Mapping / Decompose Problem / Deduce Relations / Synthesize Solution” introduces unnecessary written jargon while narration gives accessible examples. This scene was previously approved, so it is a lower-priority replacement opportunity. At 2:14.30–2:20.70, “LLM Engine / Internal Weights” shows arbitrary decimals and an unrelated generated-answer example. Avoid reusing it as a new donor under the current restriction on invented figures. The words/fragments drawing and prediction-loop drawing are more useful existing material.

What is still current: all five teaching-board image hashes match those recorded in the earlier build manifest. Their wording and probability numbers agree with today's page. The closing card matches today's asset visually and remains the literal final frame. The sampled frames contain no Notebook stock photographs. The older ban on all people is no longer current: illustrated/cartoon/stylized people are allowed; this file does not need changes on that account.

## Narration assessment

**VERDICT: KEEP on essential teaching, provisional pending listening.** No essential explanation needs replacement on the evidence of the complete transcript. This is not a whole-file shipping pass. Production defects above are separate from the narration verdict.

| Current lesson point | Assessment | Current video evidence |
|---|---|---|
| Hook: AI learns before a user prompts it | TAUGHT | 0:00–0:08.3, learns the peanut-butter continuation from examples |
| App versus engine; full term Large Language Model / LLM | RICH | 0:13.7–0:22.1, “ChatGPT is the app. The LLM is the engine,” then full term |
| Large: extensive text and code | TAUGHT | 0:22.1–0:29.9 |
| Language: reads, writes, summarizes, translates, explains | RICH | 0:29.9–0:37.5, all five functions |
| Model: learned numerical patterns predict output | TAUGHT | 0:37.5–0:42.7 |
| Training happens first; learned patterns then build an answer | RICH | Hook plus 0:42.7–0:46.5 and explicit bridge at 2:14.4–2:20.9 |
| Training example includes the correct answer | RICH | 0:46.5–0:53.9, Read |
| Guess: peanut butter and ___ → cloud | RICH | 0:53.9–1:09.4, includes why prediction can be wrong |
| Check against jelly in the example | RICH | 1:09.4–1:17.8 |
| Adjust internal numbers to make jelly more likely | RICH | 1:17.8–1:33.1 |
| Repeat across examples; patterns build | RICH | 1:33.1–1:48.7, explicitly repeats the four-step cycle across billions of examples |
| Familiar jelly pattern | TAUGHT | 1:48.7–1:53.2 |
| Star, time, never pattern examples | TAUGHT | 1:53.2–2:01.1; all three completed phrases spoken |
| Patterns extend to explaining, problem-solving and misspellings | TAUGHT | 2:01.1–2:14.4. “Ask questions” is omitted as a separate example, but the broader understanding survives |
| Uses patterns to calculate the continuation; not a stored complete answer | RICH | 2:14.4–2:37.6 |
| Left prompt and jelly 41%, bread 27%, bananas 16%, honey 5% | RICH | 2:46.6–3:02.5, all values spoken |
| Probabilities are illustrative; remaining possibilities total 100%; highest is not compulsory | RICH, accurate additions | 3:02.5–3:16.5 |
| Changed prompt and sandwich 54%, smoothie 16%, toast 9%, jelly 2% | RICH | 3:16.5–3:37.8, all values spoken |
| Context changes the odds; jelly drops 41% → 2% | RICH | 3:37.8–3:53.6, reason and comparison explicit |
| Phone suggests a word; user taps; repeats; model automates loop | RICH | 3:53.6–4:08.0 |
| Growing sentence predicts jelly → for → lunch | RICH | 4:08.0–4:36.6, updated input explained |
| Every chosen word joins the next input | RICH | 4:36.6–4:43.2 |
| Repeated prediction builds a paragraph very quickly | TAUGHT | 4:43.2–4:54.1 |
| Two closing lines | RICH | 4:54.1–5:00.6, both lines verbatim, no narrated sign-off |

The shortened lesson still carries the causal arc: examples change internal numbers → learned patterns → context-sensitive probabilities → choose a continuation → use the updated input again. The token clarification at 2:37.6–2:46.6 usefully qualifies the lesson's whole-word simplification. There is no need to restore the ten deleted restatements merely because the spec changed.

Hard requirements: the full term, app/engine distinction, four training steps, all pattern examples, all probability values, jelly/for/lunch sequence, and exact two-line close are present. The four topic blocks remain in order. The deleted “training phase” recap is no longer in this version. The upload prompt's requested sentence “A full paragraph runs this loop many times, fast enough to look like thought” remains a meaning-preserving paraphrase, as in the previously accepted video: “To generate a full paragraph, the model runs this exact loop of predicting, adding, and updating many times over. It happens at speeds fast enough to look like active thought.” **That is not a word-for-word prompt pass.** If literal wording becomes a hard requirement for this accepted video, no verified exact donor has been found and KEEP would need reconsideration under that requirement.

Source QA: no material discrepancy found between the current lesson and spoken teaching. The transcript's “peanut butter end” is an ASR uncertainty, not a verified spoken error. Listening is needed before attributing those words to the narrator. No new narration cut, graft, speed change, or pause is proposed.

## Proposed board and camera plan

This is a reviewable proposal, not an executed build. Times refer to the current video and are approximate for spoken onsets. Preserve the current audio timeline except for a separately diagnosed repair to the reported 0:46 glitch. Use the exact current JPGs and fixed 4-pixel delivery rings in rebuilt spans.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| What's an LLM? | Unmarked arrival; banner at ~0:13.7; complete Large, Language, Model cards at their spoken onsets | Compact, full view | Keep 0:08.47–~0:42.7, about 34 seconds; change to training board at its introduction | No suitable unused drawing for these three definitions was located. Explicit long-hold exception pending donor availability |
| How Training Works | Unmarked introduction; Read → Guess → Check → Adjust; then banner/loop during repetition | Compact, full view; no sentence-level zooms | ~0:42.7–1:43.9 if canonical board replaces the prohibited flowchart, about 61 seconds | Removing the counterfeit board fixes fidelity but worsens the uninterrupted hold. A relevant training drawing is needed to improve engagement; none verified locally |
| How AI Learns Patterns | Whole familiar-pattern card, then whole examples card | Compact, full view | 1:43.90–2:04.03, about 20 seconds; retain the following approved drawing provisionally | Borderline duration, actual examples are being explained; no gratuitous extra cut needed. Improve the jargon drawing when a suitable donor exists |
| Same Word. Different Odds. | First visit unmarked. Detail visit: complete left card → prompt/table sections as explained; same sequence right; banner under context takeaway; simultaneous jelly-row rings for explicit 41% vs 2% comparison | Dense: whole-board entry; delay dive until full view has had at least two seconds; complete active card always visible; smooth pan and full pullback | First visit 2:20.70–2:33.50 (12.8 s); second 2:45.70–3:53.73 (68.0 s) | Preserve approved long-run exception until a relevant probability drawing is available. Do not cover the numeric explanation with arbitrary filler or break it by dropping spoken values |
| One Word at a Time | Whole jelly card → whole for card → whole lunch card; banner under next-input rule | Compact, full view | Current 4:05.00–4:43.27 (38.3 s). Preserve three-card walk; optional use of the existing loop drawing under ~4:36.6–4:43.2 reduces board run to ~31.6 s | Drawing would reinforce “chosen word becomes input,” but does not solve the entire >20 s hold. Preserve the spoken banner explanation; choose this tradeoff explicitly rather than cutting away mid-example |
| Training builds the patterns. (close) | Unmarked | Preserve standard hold → 1.2× push → settled hold | 4:54.20–5:03.80, 9.6 seconds, literal final frame | Current copy and treatment remain appropriate |

No new pauses proposed. The board entrance and dive timing can be corrected without stretching narration. Silence should not be added merely to provide animation time.

## Donor availability and evidence

Current Notebook spans: 0:00–0:08.47 peanut-butter jars; 1:32.97–1:41.97 training flowchart (ineligible board recreation); 2:04.03–2:14.30 structural-sequence diagram; 2:14.30–2:20.70 app/engine with arbitrary weight numbers; 2:33.50–2:37.73 incremental pieces; 2:37.73–2:45.70 words/fragments; 3:53.73–4:05.00 prediction loop; 4:43.27–4:54.20 prediction loop. No new donor insert was made.

The project search found the pre-shortening backup in `archive/how-an-llm-works/`, but no original `how-an-llm-works`, `how-the-model-learns`, or `how-the-model-answers` raw MP4 rolls in `Prompts/`, `gemini-notebook/`, or `archive/`. The backup is an already edited file; its removed material includes the unwanted numerical network and phase/percentage graphics. Recovering an original roll or generating a drawing donor may improve the visual options, but is not a reason to discard the complete narration. A rebuild from only the surviving finished video would incur another video encode; copy its AAC unless the approved scope includes an audio repair.

Local evidence: `source-identity.json`, `mapped-timeline.json`, `current-assets.jpg`, `sheets/`, selected `frame-*.jpg`, `board-spans.txt`, and `ring-stroke.txt`. The completed board scan independently confirms the 68-second probability hold. Its brief probability-board hits near 1:39, 2:09, and 2:15 are false matches to Notebook diagrams, not actual board appearances; do not use its uncorrected total as board exposure. Timings in the mapped timeline are derived from the original build and shortening manifests at nominal 30 fps, checked against sampled encoded frames. OpenCV reports average FPS 30.00329, so automated timestamps can differ by a few hundredths of a second. Any future edit must finalize boundaries against decoded frames and audio gaps.

Remaining verification before a new ship verdict: end-to-end listening/playback; audition the 0:46 join; exact boundary strips for changed entrances and cutaways; final highlight/camera checks; logo cleanup inspection in retained drawings; and verification of any actual audio repair. No claim of shipping readiness is made here.
