# Questions Matter v7 → v8 — opening pacing repair + breath cut (v8 SHIPPED 2026-09-26, cache key 20260926ship8)

**Scope.** Narrow visual repair of the opening board run (David, 2026-09-26, approved plan: keep narration and second half, break
up 0:08–1:26.5). Audio untouched. Live video and lesson page unchanged.

- Candidate: `Prompts/questions-matter-v7.mp4` (sha256 `0083fd044ce0…`), 6688 frames, 30 fps, 3:42.93.
- Baseline: live `course-assets/questions-matter/questions-matter.mp4` (`45a69035d7fc…`, 20260921ship17), still unchanged.
- Donor: the video live before 2026-09-16, recovered from git `13e9d847:videos/questions-matter.mp4` and saved as
  `donor-live-2026-09-04.mp4` (gitignored). It's a different Notebook roll, and the only other Questions Matter footage left: the
  two 09-16 rolls are deleted. The donor has no engine corner mark on the frames used.
- Build: `scripts/video/build_questions_matter_v7.py`; manifest `edit-manifest.json`.

## Change log

| Output | Was | Now | Narration under it |
|---|---|---|---|
| 0:07.83–0:12.87 | Answers board, full view | **Donor A**: abacus → book → computer, each with a question mark (donor f2452–2603; drawn for "while the tools we use to find answers change") | "For decades, technology has steadily reduced the friction of getting answers," |
| 0:12.87–0:45.67 | same board | Answers board, full view; Library ring 0:19.5, Search 0:32.1, AI 0:44.3 (same onsets as before) | "and the less time…" through "Now we have AI." |
| 0:45.67–0:50.40 | same board | **Donor C**: brain and robot face (donor f2–144; drawn for "the human prompt… the machine's output") | "You open an app, type a prompt, and the answer appears on your screen in seconds." |
| 0:50.40–1:03.53 | same board | Answers board returns with the AI ring, then Half a Saturday / An hour or two / Seconds rings, then banner (same onsets as before) | "Half a day, then an hour, now seconds." … "changes where our value lives." |
| 1:03.53–1:13.73 | Value board | Value board, Pre-AI ring, then With AI ring at 1:11.6 | "Before AI…" through "the answer is instant." |
| 1:13.73–1:17.57 | same board | **Donor B**: brain → question mark (donor f151–266; drawn for "the question you ask") | "The hard part is deciding which questions to ask, and judging whether" |
| 1:17.57–1:26.10 | same board | Value board returns with the With AI ring, then banner at 1:23.1 | "the output actually solves your problem." … "Questions didn't." |

- Both boards keep their approved treatment: compact, still full view, no zoom (all three research columns stay in view), same
  rectangles, colours and ring onsets. Only the board appearances are re-rendered, with the house ring setting.
- 0:00–0:07.83 and 1:26.10 to the end come from the live file frame for frame (re-encoded once). That covers Socrates, the scientific method, all four quality cards with
  their pairs and drawings, and both closing lines on the standard close.
- Every picture cut except one falls in a speech gap (12.72–13.10, 45.36–45.94, 50.36–51.06, 73.34–73.86). The cut back to the
  value board at 1:17.57 lands on a word boundary mid-sentence ("whether | the output"), because Donor B runs only 3.8 s.
- **Rejected donor:** the old roll's monitor drawing (donor 8.9–19.5 s, "the generation is instantaneous"). It fits the AI beat, but
  the text it writes on screen becomes legible nonsense within about a second, a leak from its style prompt: "Instantly
  generated wobbly felt-tip ink scribbles to transportation…"
- Not used: every board frame in the old roll (outdated boards), and the Socrates, Einstein, pill and ship's-wheel drawings
  (off-topic for this span).

## Board-hold measurements (exact frames; board_spans.py at 0.5 s agrees within 0.5 s)

| | Before (live) | After (v7) |
|---|---|---|
| How Answers Got Easier and Faster | 1 appearance: 55.7 s (0:07.83–1:03.53) | 32.8 s (0:12.87–0:45.67); 13.1 s (0:50.40–1:03.53) |
| It Changes Where Value Lives | 22.6 s (1:03.53–1:26.10) | 10.2 s (1:03.53–1:13.73); 8.5 s (1:17.57–1:26.10) |
| **Longest continuous board run** (adjacent boards counted together) | **78.3 s** (0:07.83–1:26.10) | **32.8 s** (0:12.87–0:45.67) |
| Other continuous runs in the opening | — | 23.3 s (0:50.40–1:13.73, Answers board then Value board); 8.5 s |
| Second half (unchanged) | 14.0, 7.0, 12.5, 8.5 s, each broken by drawings | same |

**Not resolved:** two stretches are still over the ~20 s guideline.
1. **32.8 s** on the Answers board through the Library and Search eras (0:19.5–0:43.6). There's no library drawing and no
   internet-search drawing in any surviving footage for this lesson. Breaking this up needs either those two drawings or a reroll.
2. **23.3 s** across the time-to-answer rings, the banner, the value-board intro and the Pre-AI card. No surviving drawing fits
   "Before AI, the sheer work of locating a good answer was valuable." The live roll's own drawings are already in use or
   off-topic.

## Checks

1. Decoded 6688 frames at 30 fps, matching the plan. Each of the four legs decoded its exact span.
2. Audio packet payload identical to the live file (`-c copy -f data` sha256), so the narration, pauses and levels haven't changed.
3. `transition_guard.py`: 18/18 declared boundaries passed (8 splices, 10 ring onsets). All 8 splice strips inspected frame by frame:
   one clean cut each, no stale frames, no board render leaked from the donor.
4. Ring states inspected at full resolution (`state-*.jpg`): right card each time, complete card inside the ring, nothing clipped.
5. **Stroke:** drawn with `ken_burns_path.ring_px(720) = 4`, the same setting as the 20260926ship2 What Is AI reference.
   `ring_stroke.py` reads 4.0 px (5.0 on teal, a threshold effect). A raw pixel profile across each edge shows about 5 solid
   px plus anti-aliased edges, the OpenCV odd-width limitation flagged 2026-09-26. So the literal 4 px at 720p isn't met by this
   build or any other until `draw_ring` changes. The unchanged second half still carries the older 6–7 px rings (out of scope).
6. Contact sheet of 0:00–1:36 (`opening-sheet-0-96s.jpg`): order and content as planned.

**Not performed:** I can't listen or play video in this environment. I haven't heard the candidate end to end or watched it in
real-time playback. No join needs an audio audition because the audio is packet-identical, but David should watch the six picture
cuts (0:07.8, 0:12.9, 0:45.7, 0:50.4, 1:13.7, 1:17.6) at speed for pacing feel. The donor clips are a second-generation encode
of an older finished video. They looked clean in sampled frames but haven't been checked at playback speed.

**Housekeeping:** the `leg-*.mkv` intermediates are kept for a possible rebuild. After a ship decision, run `clean_video_audit.py`.

---

# v8 — extra breath at 0:08 deleted (David, 2026-09-26: "At :08, please delete the extra breath.")

- Candidate: `Prompts/questions-matter-v8.mp4`, 6674 frames, 30 fps, 3:42.47. Build: `scripts/video/build_questions_matter_v8.py`.
  Records in `v8/` (manifest, transitions, audition clip). v7 stays as it was, for comparison.
- **What was cut:** 7.833–8.300 s on the live/v7 timeline (frames 235–249, 0.467 s). That's a click at 7.86 followed by an inhale decaying
  to 8.30. It sits exactly at the 09-16 graft join, where roll 1's audio begins, which is why it doubled the pause.
- **How:** picture and sound were cut together. The audio was decoded from the live file and the span removed with a 5 ms
  equal-power crossfade; both edges sit at −63/−62 dBFS, the existing room-tone floor. AAC was encoded once at 192 kb/s,
  48 kHz mono. The picture drops the first 14 frames of Donor A (the abacus), so the cut lands on the existing opener → abacus
  picture cut.
- **Pause:** "…you have to know what to ask." → "For decades" went from 1.36 s to 0.89 s. The −53 → −62 dB floor step at 7.82 s was
  already in the live file; the cut didn't create it.
- **Checks:** 6674 decoded frames, matching the plan. Cross-correlation against the live audio shows 0-sample lag both before
  and after the cut. Transition guard 18/18, and every boundary sits exactly 14 frames earlier. The 0:07.8 strip was inspected:
  one clean cut. Board-hold durations are unchanged from v7 (Answers 32.8 s first appearance; longest continuous run 32.8 s,
  now 0:12.40–0:45.20).
- **Not performed:** I haven't listened to this join. Audition clip: `v8/audition-0004-0012-breath-cut.mp4` (output 0:04–0:12;
  the join is at 0:03.8 in the clip).

## Shipped 2026-09-26 (David: "ship it")

v8 copied to `course-assets/questions-matter/questions-matter.mp4` (sha256 `2c4fe76bbeb8…`, 23,698,941 bytes), and the `questionsvaluable` cache key
changed from `20260921ship17` to `20260926ship8`. Pill unchanged (4 min; 3:42.47). The `manifest.json` video_assets row is updated; it had still
carried the 09-16 hash. The v7/v8 candidates were removed from `Prompts/` and the leg intermediates deleted. The donor snapshot is kept
(gitignored; also recoverable from git 13e9d847). David hadn't heard the 0:08 join or the six picture cuts before the ship.
