> **Lesson updated after this review (2026-09-16):** The overview board now matches How an LLM Works: **Learn First** (Training / Patterns) and **Answer One Word at a Time** (Probability / Prediction), without numbered steps. The page, Markdown, and video prompt are aligned. This review describes the prior lesson version; re-evaluate the candidate narration and recheck overview highlight coordinates against the new JPG before the next build or shipping decision. No video was changed by this lesson update.

# AI Is Different — v7 review handoff

## Recommendation

**Ready for David's review; not approved to ship yet.** The repaired cut now carries the lesson's essential teaching accurately and completely according to the lesson text and timestamped transcript. The remaining gate is an audible, end-to-end playback by a human listener, with special attention to the three donor-audio joins listed below.

The live lesson video, lesson Markdown, source rolls, close donor, and canonical board images were not changed. Nothing was deployed.

## Candidate

- File: `Prompts/ai-is-different-v7.mp4`
- Duration: 5:22.47
- Format: 1280x720, 30 fps
- Decoded frames: 9,674 of 9,674 expected
- SHA-256: `c58f808613e44d99acddb1abee1e07f34f3142b222ed5ef7efe24233feaf9395`
- Status recorded by QA: `Review only; live video unchanged`

`ai-is-different-v6.mp4` is the retained superseded attempt. Its transition check found a three-frame source-visual flash before the spreadsheet. v7 moves that visual cut to the exact source boundary and passes the same check.

## Narration repair

The cut uses roll 1 as the base and makes three teaching-driven replacements:

1. **Structured versus unstructured data**
   - Output: 3:11.40–3:23.27
   - Donor: `Prompts/ai-is-different-2.mp4`, 1:47.80–1:59.67
   - Replaces the ambiguous “pattern mattering” wording with the concrete messy-handwritten-receipt explanation and the relationship-between-words-and-numbers explanation.

2. **Kryptonite examples**
   - Output pause: 4:14.23–4:14.53
   - Output donor speech: 4:14.53–4:52.53
   - Donor: `Prompts/ai-is-different-2.mp4`, 2:42.40–3:20.40
   - Supplies the full scams, deepfakes, and confident-but-wrong examples, followed by the trained-behavior explanation.
   - The only editorial pause added is this 0.30-second matched-room-tone breath. It measures about -39.0 dBFS internally; it is not digital silence.

3. **Exact lesson close**
   - Output: 5:13.07–5:18.47
   - Donor: `Prompts/close-ai-is-different.mp4`, 0:38.20–0:43.60
   - Restores: “AI's foundation gives it new superpowers. Those superpowers come with kryptonite.”
   - A four-second settled close hold follows.

The weaker claim that AI is a necessary tool was removed. The repaired transcript retains the important distinction that normal software wins for exact, repeatable tasks such as password checks and GPA calculations.

### Audible review required

This environment cannot listen to or play audio perceptually. ASR, waveform, decoded-sample, timing, and correlation checks passed, but they cannot certify voice timbre, cadence, room-tone match, or whether a join sounds natural. Listen to the whole candidate, with extra attention at:

- 3:11.40 and 3:23.27 — roll 1 / roll 2 / roll 1 joins
- 4:14.23–4:14.53 and 4:52.53 — selective breath and Kryptonite donor joins
- 5:13.07 and 5:18.47 — exact-close donor joins

The encoded audio correlates with the planned edit at `0.9999129`. The source AAC contains existing full-scale samples, so sample-count checks are not a substitute for listening.

## Visual and production review

- Canonical lesson boards are used for rules, learning, rules-versus-patterns, structured data, and Kryptonite.
- Board moves begin with a readable full view, use complete-card zooms and targeted rings, and return to context.
- Notebook drawings remain as visual interleaves: code/IF-THEN-ELSE, cookbook and chef, PS5 controller, spreadsheet, legal pad, tool-choice diagrams, phone, and guardrails.
- The structured-data section breaks up the dense boards with the spreadsheet and legal-pad drawings.
- Course imagery remains illustration-led. No new stock photography was introduced.
- The Notebook corner mark was cleaned where required: 3,426 cloned frames, 880 inpainted frames, zero declined frames.
- Full-resolution checks of readable Notebook frames found no inappropriate or profane generated text. Some decorative code is intentionally pseudo-code and not lesson content.
- The full 4-second-interval timeline, all board state sheets, every declared boundary pair, and selected full-resolution Notebook frames were visually inspected.

## Verification

- Full decode: PASS, 9,674/9,674 frames
- Transition guard: PASS, 22/22 declared boundaries
- Manual boundary-pair inspection: PASS
- Protected input and lesson files unchanged: PASS
- Transcript teaching coverage against `index.html` and `lessons/ai-is-different.md`: PASS
- Final visual remains on the intended close frame: PASS
- End-to-end audible playback: **NOT PERFORMED — human review required**

Supporting artifacts:

- `edit-manifest.json` — frame-accurate timeline and board-state manifest
- `verification.json` — decode, audio, pause, hash, and protected-file checks
- `guard/transition-guard.md` — all boundary results and per-boundary strips
- `boundary-pairs.jpg` — before/after frame comparison sheet
- `bundle/ai-is-different-v7/transcript.txt` — complete timestamped ASR transcript
- `final-sheet-0.jpg` through `final-sheet-6.jpg` — whole-video visual timeline
- `states-*.jpg` — board-state review sheets
- `notebook-fullres/` — selected full-resolution Notebook checks

## Build and QA entry points

- Build: `scripts/video/build_ai_is_different_v6.py` (currently emits v7; filename retained because v6 was its first versioned output)
- QA: `scripts/video/qa_ai_is_different_v7.py`

Do not replace `course-assets/ai-is-different/ai-is-different.mp4` or deploy until the audible review is complete and the candidate receives a final Keep verdict.
