# Training — live video evaluation and current-board retrofit plan (2026-09-16)

**Live file:** `course-assets/training/training.mp4` (4:34.97, 8249 frames, 30 fps, 1280x720, AAC mono 48 kHz), sha256 `fcd3a89276d10067e6b52ce238b62bee4a2eb64f7b10bc181a464e12b504eca1`. Served as `?v=20260909repair1`, pill "5 min".
**Scope of this record:** narration review of the live file under `NARRATION-REVIEW.md`, board audit against the current `course-assets/training/` JPGs, and ONE edit plan (Edit Spec 1b + 6) for David's approval. No candidate has been rendered; the live video, lesson, and boards are unchanged.
**Source limitation:** the raw rolls (`Prompts/training-1.mp4`, `training-2.mp4`) were removed in the 2026-09-15 cleanup and the 2026-09-09 review bundle with them. The live file is the only source, so any rebuild re-encodes its Notebook spans from a finished H.264 file (one extra generation), and no Notebook drawing exists for the phase narration beyond what the live file already shows.

## Narration review

```text
LESSON: training
CANDIDATE: course-assets/training/training.mp4 (4:34.97)
VERDICT: KEEP
TEACHING POINTS:
  Hook: AI explains chemistry / writes code; how did it learn? — TAUGHT — 0:00 "AI can explain complex chemistry concepts or write lines of software code… how exactly does a computer learn to do those things?" (essay example dropped; harmless)
  Basketball analogy: shoot, check, adjust — RICH — 0:09–0:18
  Training = guess, check, adjust, but adjusting the numbers inside the model — RICH — 0:18–0:35 "instead of adjusting physical force, AI training strictly involves tweaking a set of internal numbers. Those numerical adjustments help the model make a better guess next time."
  Before Training Starts: Set Up the System (design model, starting values, training will adjust them) — TAUGHT — 0:43 "design the model's structure and assign starting values to its internal numbers" (the "training will adjust those numbers" clause was already taught at 0:32)
  Before Training Starts: Gather the Data (books, websites, conversations, code, images, audio, video = curriculum) — TAUGHT — 0:48 "a massive curriculum of data, collecting books, websites, conversations, code, and images" (audio and video not spoken; the board shows them)
  Training Loop: PB&J example, guess "cloud" — RICH — 0:59
  Training Loop: check against "jelly" — RICH — 1:06
  Training Loop: adjust the numbers so jelly becomes more likely — RICH — 1:12
  Training Loop takeaway: repeat with more examples, patterns build — RICH — 1:20 "Repeating this loop millions of times builds reliable patterns."
  Three phases intro (page 2026-09-16: patterns, follow instructions, more useful answers; same basketball question) — TAUGHT — 1:25–1:37 "three distinct phases of training, each with a different job… the exact same prompt through each phase. How do I shoot a basketball?" (the jobs are on the new Three Phases board and each is taught in its own phase)
  Pretraining: 1,000 lifetimes; guess next word, check, adjust weights ("called weights") — RICH — 1:42–1:55
  Pretraining: answer example read — RICH — 2:00 (read verbatim)
  Pretraining: fluent text but doesn't reliably follow instructions — RICH — 2:06–2:20
  Instruction Tuning: questions paired with example answers; practices; weights adjusted toward the examples — TAUGHT — 2:26–2:37 "adjusting its weights to match the requested format" (lesson: "more like those examples"; same idea)
  Instruction Tuning: answer example read — RICH — 2:41 (verbatim)
  Instruction Tuning: follows the request but may be unclear, incomplete, or unhelpful — TAUGHT — 2:52 "dry or incomplete… might not be helpful"
  Preference Tuning: several answers, people pick the best (clear, useful, accurate), weights adjusted toward it — RICH — 3:07–3:25
  Preference Tuning: answer example — TAUGHT — 3:28–3:41 (first two sentences read, then characterised; full text on the board)
  Preference Tuning: can still give a wrong answer that sounds right — RICH — 3:41–3:54 ("can still hallucinate… confidently provide a wrong answer that simply sounds correct")
  When training ends: model ready; chat uses the trained weights; new info can be used but the conversation does not change the weights — RICH — 3:54–4:26
HARD REQUIREMENTS:
  "AI learns from examples and feedback." — MET — 4:26.48
  "Guess. Check. Adjust. Repeat." — MET — 4:29.94 (medium.en word transcript: "Guess, check, adjust, repeat."; the base.en bundle heard "Yes", which is a transcription error)
ERRORS: none. ("Repeating this loop millions of times" and "hallucinate" are accurate additions.)
SOURCE_QA: PASS
ADDITIONS: names the failure "hallucinate" (ties to the Avoid Traps section); "fixed, frozen weights" is a memorable phrasing of the closing paragraph.
REPAIR PLAN: none
EDITING NOTES:
  - Order: the video teaches Before Training Starts (0:37) BEFORE the Training Loop (0:56); the lesson has them the other way round. Accurate and arguably more logical; no change proposed.
  - The 2026-09-09 build inserted a one-second pause at every section boundary (old rule). They are in the live audio and stay under a visual-only retrofit. No new pauses proposed (Edit Spec 6): the transitions already breathe.
  - Visual defects and the current-board gaps are listed below; none affect this verdict.
LISTENING: two transcriptions (base.en segments, medium.en words) plus the 4:25–4:35 close re-checked; no human-equivalent audition in this environment. Audio is not being edited, so no joins need listening beyond the appended close tail.
```

## Board audit (why a retrofit is needed)

Page state at review time: `index.html` and `lessons/training.md` are uncommitted in the working tree (David's session): the Training lesson now has six boards including the new `training-three-phases.jpg`, and the Markdown carries it as Board 3, so upload materials and page agree.

Frame-vs-asset diff of each board's opening frame against the current JPG laid out the 2026-09-09 way (`board-diffs.jpg`): mean difference 7.6–8.1 with 0.1–0.3 % of pixels differing, and the heat maps show the ONLY content difference is the **website credit footer** (`besmarterthanthetool.com`) now baked into every canonical JPG. Board text, layout, and illustrations are otherwise identical, so the 2026-09-09 ring rectangles still fit the current assets exactly (`rects-sheet.jpg`).

What the live file does not meet under the 2026-09-15 spec:

| Item | Live file | Current spec |
|---|---|---|
| Board pixels | pre-credit boards on a pink-white (251,245,246) stage, scaled to 1220x680 | exact current JPG (with credit) on the house stage from the board's own corner colour (Edit Spec 2, retrofit playbook 3) |
| Closing board | 2026-09-09 close on a lavender background (`8020-close-a` in `frames-sheet.jpg`) | current canonical white `training-close.jpg` via `make_close_board --lesson training` (Edit Spec 7) |
| Gemini Notebook corner mark | present on every Notebook span: 0:00–0:37, 1:26–1:39 (weak, credit-like), 3:55–4:27 (`mark_strength` ≥ 15) | never ships; cleaned per kept frame (Edit Spec 8) |
| "Three Phases of Training" overview (1:25.73–1:39.53) | an invented course-style graphic built on 2026-09-09 | resolved 2026-09-16: David added the page board `training-three-phases.jpg`; the video uses it |
| Notebook garbled-title morph at 3:59.8–4:00.4 (source 7194–7211) | gibberish title text + grey overlay for 18 frames (`strip-7055-7230.jpg`) | cover with a still from the roll (Edit Spec 8c pattern) |
| Rings | outline, ~5 px, correct accents | same; re-drawn by `ken_burns_path.py` after the crop |
| Photographs | none (all Notebook spans are drawings) | ok |
| Longest unbroken board run | 1:39.53 → 3:55.30 (135.8 s, the three phase boards back to back) | Edit Spec 8b would interleave Notebook drawings, but the roll is gone and the live file has no drawings for that narration — cannot be applied; reported |

## Proposed edit plan (one approval)

**Scope:** visual-only retrofit (Edit Spec 1, retrofit playbook). Audio carried untouched for all 8249 source frames; the one audio change is 78 frames (2.6 s) of matched room tone appended after the file's end so the canonical close settles for 4.0 s after the closing audio (framework default). Output 8327 frames / 4:37.57. If David prefers bit-identical audio, drop the tail: the close then settles 1.4 s.

Build script: `scripts/video/build_training_v3.py` → `Prompts/training-v3.mp4`, audit dir `video-audit/training-repair-2026-09-16/`.

### Board table (Edit Spec 1b)

Source cuts from `scenes.py` (sequential decode). Onsets from the medium.en word transcript. All boards are **compact** (every card's text reads at full view on the 1280x720 frame), so each stays at full frame with the framework's capped 4 % push; rings pop card to card at spoken onsets; no dives.

| Board | Source span | Full view before first ring | Highlighting sequence | Camera | Reason or exception |
|---|---|---|---|---|---|
| Before Training Starts | 1112–1694 (0:37.07–0:56.47) | 6.6 s ("Before training can begin… This graphic outlines the two preliminary steps.") | whole card **Set Up the System** (editorial purple) at 0:43.62 "First, they design…" → whole card **Gather the Data** (blue) at 0:48.18 "Then, they gather…" | full board | same treatment as the live file |
| The Training Loop | 1694–2572 (0:56.47–1:25.73) | 3.1 s ("Once set up, the training loop begins.") | example line (neutral purple) at 0:59.54 "Using the phrase peanut butter and jelly" → **1 Guess** column (purple) at 1:02.34 "given the prompt…" → **2 Check** (blue) at 1:06.92 → **3 Adjust** (teal) at 1:12.46 "Because it's wrong…" → gold takeaway banner (neutral) at 1:20.72 "Repeating this loop…" | full board (tall board, 4 % stage above/below) | column rings trace illustration + number + text as one component, as approved 2026-09-09 |
| Three Phases of Training | 2572–2986 (1:25.73–1:39.53) | 6.3 s ("That fundamental loop is applied across three distinct phases of training, each with a different job.") | "THE SAME QUESTION / How do I shoot a basketball?" strip (neutral purple) at 1:32.06 "To see how they work, we'll run the exact same prompt…"; the three phase cards stay unmarked (not named individually here; each gets its own board next) | full board | **new page board** `training-three-phases.jpg` (1600x620, sha256 57b44c5e…, added by David 2026-09-16) replaces the 2026-09-09 video-only graphic |
| 1 · Pretraining | 2986–4264 (1:39.53–2:22.13) | 3.3 s ("This image illustrates phase one, pre-training.") | **Learn from Vast Amounts of Data** at 1:42.82 "The model ingests…" → **What an Answer Might Look Like** at 1:55.10 "If we ask our basketball question…" → **What Still Needs Work** at 2:09.86 "but there is a core limitation, as noted in the bottom section" (all editorial purple) | full board | |
| 2 · Instruction Tuning | 4264–5507 (2:22.13–3:03.57) | 4.8 s | **Learn to Follow Instructions** at 2:26.96 "Now, humans provide…" → **What an Answer Might Look Like** at 2:38.00 "Now, when we ask…" → **What Still Needs Work** at 2:52.66 "However, while the model…" (all blue) | full board | |
| 3 · Preference Tuning | 5507–7059 (3:03.57–3:55.30) | 4.2 s | **Learn from Feedback** at 3:07.80 "In this stage…" → **What an Answer Might Look Like** at 3:25.96 "Look at the final answer…" → **What Still Needs Work** at 3:42.36 "But there is still a vulnerability." (all green) | full board | |
| Close | 8009–end (4:26.97 →) | — | canonical `training-close.jpg` (white), 48-frame hold, 150-frame push to 1.2x, settled hold | standard | replaces the lavender 2026-09-09 close |

### Notebook spans (kept, corner mark cleaned)

- 0–1112 (0:00–0:37.07): chemistry/code whiteboard, question-mark chip, basketball player, shot arc, neural net, Notebook's own "AI Training Loop" and weight-tweak drawings. Kept as is.
- 7059–7194 (3:55.30–3:59.80): Notebook's "Three Training Phases" drawing including its fade-in. Kept.
- 7194–7212 (3:59.80–4:00.40): the garbled-title morph — **covered by holding source frame 7193** (last clean drawing frame) until the packaged-model scene is fully drawn at 7212. Hard cut instead of Notebook's morph.
- 7212–8009 (4:00.40–4:26.97): "Packaged Model Deployment", chat-window sketch, "AI Inference Phase" frozen-weights drawing. Kept.
- Photographs replaced: none. Notebook spans used out of place: only the 18-frame hold above.

### Narration changes and pauses

None proposed. Existing measured gaps at section boundaries (from the 2026-09-09 pauses): 0:55.8→0:56.1 (0.3 s), 1:24.2→1:25.7 (1.5 s), 2:20.7→2:21.8 (1.1 s), 3:02.3→3:03.6 (1.3 s), 3:54.1→3:55.3 (1.2 s), 4:25.6→4:26.5 (0.9 s). They already give breathing room; nothing is added or removed.

## Verification plan for the candidate (after approval)

Decoded frame count = 8327; audio PCM of the first 8249 frames compared with the live track; `transition_guard.py` on every declared boundary (1112, 1694, 2572, 2986, 4264, 5507, 7059, 7194, 7212, 8009, 8249) with strip inspection; state sheets for every ring state at full resolution; corner-mark declined-frame list reviewed; close is the literal final frame.

## Dry run (2026-09-16, `--prepare-only`)

Timeline, legs, close, and manifest prepared: 8327 frames / 4:37.57. Ring-state frames inspected at full resolution (`state-before-0223.jpg`, `state-loop-0118.jpg`, `state-pre-0125.jpg`, and the `states-*.jpg` sheets): current JPGs with the website credit on the house stage, whole-card 5 px rings, complete cards inside every ring, full-view opens confirmed. No candidate MP4 rendered; awaiting David's approval of the plan above. 2026-09-16 15:40: overview leg switched to the new page board; dry run repeated.

## Candidate (built 2026-09-16 on David's "Build it")

**Candidate:** `Prompts/training-v4.mp4` — 4:37.57, 8327 frames, 30 fps, 1280x720, AAC mono 48 kHz.
sha256 `99b092aa0f9bb3574f35be93965204deb04fe9e91e9969b95cfc5a69cfa9d930`.
**Build:** `scripts/video/build_training_v3.py` (render) + an audio remux, recorded under `audio_remux` in `edit-manifest.json`. The framework's render (`training-v3.mp4`) crossfades 5 ms of room tone at every timeline-row edge; with rows split at the board cuts, one of those edges (7212, 4:00.40) fell inside the word "packaged" and measured a 14 dB-scale dip against the live track. v4 copies v3's video stream bit-for-bit and replaces the audio with the live track itself (all 8249 source frames, no per-row fades) plus the 78-frame matched room-tone tail, encoded once to AAC. v3 was removed; it was never handed over.
**QA:** `scripts/video/qa_training_v3.py`, `transition_guard.py`, `frames.py --sheet`, `pauses.sh`.

### Verification (all on the v4 file)

- Decoded frame count 8327 = plan. Close starts at frame 8009 (4:26.97), 48-frame hold, 150-frame push to 1.2x, 120 settled frames; the canonical white close is the literal final frame.
- Audio identity: first 8249 frames vs the live track, correlation 0.99999, difference RMS 21.7 against a signal RMS of 4559, peak difference 1948 (codec noise on the loudest peaks; no window above 3000, none at the row edges). Appended tail 2.60 s at RMS 7.3 (matched room tone); `silencedetect` reports the final silence 4:32.62 → 4:37.57.
- Transition guard: PASS 11/11 declared boundaries (1112, 1694, 2572, 2986, 4264, 5507, 7059, 7194, 7212, 8009, 8249). Strips inspected for 2986, 7212, 8009: the first frame after each boundary is already the destination; the 7194–7211 hold resolves onto the fully drawn packaged-model scene at 7212.
- Corner mark: 1363 frames paper-cloned, 699 inpainted, 0 declined. Bottom-right crops sampled at 100, 300, 700, 900, 1050, 7100, 7300, 7500, 7700, 7900, 8000: no residue.
- Ring states inspected at full resolution (`state-*.jpg`, `states-*.jpg`): current JPGs with the credit footer on the house stage, whole-card 5 px rings, complete cards inside every ring, full-view opens 3.1–6.6 s, all six boards compact.
- Six contact sheets (`sheets/`) walked from 0:00 to the settled close: Notebook drawings, six boards, close, no photographs, no Notebook rendering of a course board.
- Protected files hash-identical through the build: live video, `index.html`, `lessons/training.md`, the six boards, `training-close.jpg`.

### Listening still owed (David)

Audio is the live track, so the only new join is the close tail:
1. **4:32–4:37.6** — the end of "Repeat." into the appended room tone; confirm no level step.
2. Optional spot-check of the boards' onsets against the rings: 0:43, 1:02, 1:32, 1:42, 2:27, 3:08.

### Status

Ready for David's eye-test and ship decision. Not published; `course-assets/training/training.mp4` and `index.html` untouched. On ship: replace the live file, bump the cache key (`?v=20260916ship1`), keep the pill at "5 min" (4:37).

**SHIPPED 2026-09-16** on David's "ship it": `Prompts/training-v4.mp4` copied to `course-assets/training/training.mp4` (sha256 99b092aa…, 46,953,261 bytes), cache key `?v=20260916ship1`, pill stays "5 min" (4:37.57). Candidate removed from Prompts/. `course-assets/manifest.json` `video_assets` entry updated in the working tree (hash + bytes) but left uncommitted with David's pending manifest work. `scripts/verify-course-assets.py` reports Training clean; its other "changed finished video bytes" lines belong to earlier ships from other sessions.
