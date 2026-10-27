# Five opener blue-board cuts

Status: five rendered and technically verified review candidates. Not installed, committed, or deployed.

Scope authorized by David: remove the five middle-section opening blue boards, retain the analogies, and fold essential points into the narration. The later Embrace board reprise is also removed. No new generated voice or illustration.

## Candidates

| Opener | Original | Candidate | Saved | File |
|---|---:|---:|---:|---|
| work-with-ai-opener | 136.533s | 117.567s | 18.967s | `/Users/davidobrien/Developer/AI-Training/Prompts/work-with-ai-opener-v12.mp4` |
| understand-ai-opener | 146.033s | 139.567s | 6.467s | `/Users/davidobrien/Developer/AI-Training/Prompts/understand-ai-opener-v15.mp4` |
| avoid-traps-opener | 215.267s | 202.300s | 12.967s | `/Users/davidobrien/Developer/AI-Training/Prompts/avoid-traps-opener-v10.mp4` |
| embrace-the-future-opener | 197.300s | 187.200s | 10.100s | `/Users/davidobrien/Developer/AI-Training/Prompts/embrace-the-future-opener-v7.mp4` |
| build-your-skills-opener | 164.267s | 153.467s | 10.800s | `/Users/davidobrien/Developer/AI-Training/Prompts/build-your-skills-opener-v6.mp4` |

Total saved: 59.300 seconds.

## Edit decisions

### work-with-ai-opener

Opening board commentary, from “Take a look at these four principles” through “which AI scales up and amplifies.”

Aiming/details and verification remain in the section map; thinking/multiplication remains in the close.

Source/output frame spans, exact source hashes, image hash, and boundaries are in the per-video `edit-manifest.json`.

### understand-ai-opener

Opening declaration presentation and “It is entirely its own kind of thing, operating by a completely different set of rules.”

Move “It’s not magic, it’s not a person, and it’s definitely not normal software” after the expert/mistake question; hold the existing comparison drawing.

Source/output frame spans, exact source hashes, image hash, and boundaries are in the per-video `edit-manifest.json`.

### avoid-traps-opener

Opening declaration through “every trap looks completely fine from the inside.”

Confident false facts, human susceptibility to agreeableness, convincing fakes, and hidden failure are explained in the retained narration and map.

Source/output frame spans, exact source hashes, image hash, and boundaries are in the per-video `edit-manifest.json`.

### embrace-the-future-opener

Initial four speculative quotes and “Who’s right? Nobody knows.”

Optimist, worrier, and uncertainty remain at source 35.4–50 s. Replace the board reprise at 35.4–43.033 s with the canonical map illustration, full view, unmarked, stationary.

Source/output frame spans, exact source hashes, image hash, and boundaries are in the per-video `edit-manifest.json`.

### build-your-skills-opener

“Look at this board” / what makes you valuable preamble and “Together, these mean you’ll always be smarter than the tool.”

Move “Your choices and the questions you ask, your judgment, and the permanent skills you bring” after the enduring-human-skills sentence, over the existing student writing scene.

Source/output frame spans, exact source hashes, image hash, and boundaries are in the per-video `edit-manifest.json`.

## Verification

- All five outputs decoded to exactly the planned frame count at 30 fps. A full-frame scan found zero remaining blue-board frames in every output.
- All six declared internal boundaries passed `transition_guard.py`. Opening and splice sheets inspected visually, including both ends of the Embrace replacement.
- All original analogies, section maps, and final closes retained. Final-frame comparison mean absolute pixel error is 2.1–2.6/255 after re-encoding.
- Original mono/stereo layouts retained at 48 kHz. Encoded audio correlates above 0.9997 with the planned source assembly. All new cut handles measure below -59 dBFS; only 5 ms fades inside silence. No inserted silence or speech normalization.
- Fresh complete candidate transcripts confirm complete opening sentences and both moved lines. They support wording checks, not a listening pass.
- Sources were the current approved finished MP4s. Hash-identical versioned originals in Prompts are pinned for reproducibility; the canonical installed files remain unchanged. Each retained source is re-encoded once.
- `git diff --check` passed.

## Listening review and limits

No direct listening or continuous end-to-end playback was performed. Audition Understand AI at 0:16–0:29 (moved distinction; seams at 18.300 and 24.033) and Build Your Skills at 0:51–1:06 (moved choices/judgment sentence; seams at 56.900 and 62.733). Check all five first sentences. Embrace illustration replacement occupies 25.300–32.933.

This is a narrow repair, not a new whole-course production or teaching certification. Existing formal phrasing remains. The earlier Build Your Skills review flags an unspoken map title and paraphrased exact-line requirements; this edit does not resolve those unrelated findings. Existing Embrace worrier pronunciation remains unauditioned. No public site or Video Tracker status was checked or changed.

The repository workflow separates build approval from local shipping. These candidates await owner review and shipping authorization before replacing the canonical files.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_opener_blue_board_cuts.py` (refuses to overwrite existing candidates).

QA: `.video-venv/bin/python scripts/video/qa_opener_blue_board_cuts.py`.

Owner response: “The videos are good.” The five blue-board cuts were accepted; Avoid Traps and Embrace the Future were then selected for further shortening. Their latest candidates and review are in `video-audit/opener-shortening-2026-10-27/`. No shipping instruction was issued.

## Local shipping — 2026-10-27

All five final approved openers shipped locally in `8cb7cbdfeaaf0ec98e2d2453c264d9ac735ee098`; queued for batch deployment. Avoid Traps v11 and Embrace the Future v8 supersede earlier review candidates. See `video-audit/opener-shortening-2026-10-27/SHIP.md` and `shipping.json` for exact installed hashes and verification.
