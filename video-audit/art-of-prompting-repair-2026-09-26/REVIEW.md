# The Art of Prompting — v4 narration cleanup, 2026-09-26

**Scope:** a narrow narration repair, approved in David's 2026-09-26 brief. It makes two complete-sentence cuts and nothing else. The candidate is for review only; the live video and lesson page are unchanged.

- Candidate: `Prompts/art-of-prompting-v4.mp4`. It runs 3:51.20 (6,936 frames, 30 fps, 1280x720, AAC 48 kHz mono). sha256 `548792ba…081d06e`.
- Source: the live `course-assets/art-of-prompting/art-of-prompting.mp4` (20260916ship1). It runs 4:00.30 (7,209 frames). sha256 `c0b9ecb5…a7f347ab`, unchanged after the build. It is the only source: the 09-16 raw rolls and donor were deleted on 2026-09-15. The picture therefore went through one extra encode generation (x264 CRF 18).
- Build: `.video-venv/bin/python scripts/video/build_art_of_prompting_v4.py`
- Frame map for the 09-16 build: `video-audit/art-of-prompting-repair-2026-09-16/edit-manifest.json`

## Change log

| # | Removed words | Live audio removed | Output join | Picture |
|---|---|---|---|---|
| 1 | "To successfully package that question for AI, however, we use a specific framework of instructions," | frames 1478–1646 (49.267–54.867 s, 5.600 s). Both edges sit in −66 to −70 dB silence; the speech runs from 49.32 to about 54.55 s. | 0:49.27 | The good-question board now ends in its Open-Ended dive and cuts to Notebook's four-moves intro at 0:49.33. Live frames 1472–1647 (the pull-back and full-view hold, which sat only under the cut sentence) were dropped. The static dive frame 1471 is held for 8 extra frames so everything after it stays in sync. |
| 2 | "You don't need to apply this entire framework every single time." | frames 6027–6131 (200.900–204.400 s, 3.500 s). The join runs from the approved room-tone pause into the true silence before "A quick…". | 3:15.30 | Picture removed over the same frames. The Move 4 drawing cuts straight to Notebook's finished "Simple Query" drawing. Its fade-in and typing animation, which played under the cut sentence, are gone. |

Each audio join has a 10 ms equal-power crossfade inside the silence. Nothing else changed: no rings, boards, or close were re-rendered, and every kept frame is the live frame.

## Verification performed

- **Frame count:** decoded 6,936 frames, matching the plan (7,209 − 176 − 105 + 8). Every output frame matches its mapped live frame (max mean-abs diff 2.76 at 160x90, which is encode noise).
- **Sync:** the audio matches the live file at the expected offset in every one-second window outside the joins. The worst correlation is 0.998, with 0 ms lag before cut 1, between the cuts, and after cut 2.
- **Joins:** `transition_guard.py` passed both boundaries (1480 and 5859). I inspected the strips by eye: each shows one clean cut, with no stale frames and the destination scene on the first frame.
- **Words at the joins:** I re-transcribed both with faster-whisper small.en. It reads "…leaving room for an unexpected answer. Packaging your question for AI comes down to four specific moves." and "…Let's work on the thesis first. A quick factual question requires zero packaging." There are no clipped words.
- **Pauses (RMS, word end to word onset):**
  - Join 1: 0.66 s. The originals were 0.52 s before the cut sentence and about 0.50 s after it.
  - Join 2: 1.08 s. The approved 1-second pause after the thesis example is kept, with 0.05 s added.
  - No pauses were added.

## Board holds (frame-accurate, from the 09-16 manifest, cross-checked with `board_spans.py`)

| Board appearance | Before | After |
|---|---|---|
| Every Strong Prompt Starts With a Good Question | 0:26.57–0:54.93, **28.37 s** | 0:26.57–0:49.33, **22.77 s** |
| Four Moves (Move 1) | 1:04.93–1:21.20, 16.27 s | 0:59.33–1:15.60, 16.27 s |
| Four Moves (Move 2) | 1:31.77–1:49.67, 17.90 s | 1:26.17–1:44.07, 17.90 s |
| Four Moves Continued (intro) | 2:09.93–2:17.30, 7.37 s | 2:04.33–2:11.70, 7.37 s |
| Four Moves Continued (Move 4) | 2:48.57–2:59.73, 11.17 s | 2:42.97–2:54.13, 11.17 s |
| Closing board | 3:44.67–4:00.30, 15.63 s | 3:35.57–3:51.20, 15.63 s |

No two board appearances are adjacent: Notebook scenes separate every pair. The longest uninterrupted board run is therefore the same as the longest single appearance: 28.37 s before and 22.77 s after.

`board_spans.py` sampling notes:
- It reports 22.5 s for the first board, sampled every 0.5 s.
- It also reports a 2.0 s "good-question" hit at 2:01.5 (34 inliers, just above the threshold). This is a false match on a Notebook paper drawing, not a board. The live file has a similar false hit at 0:15.

## Not performed / open

- **No listening.** I cannot play audio. Every audio claim above comes from waveform, correlation, and ASR evidence. David should listen to:
  - **0:48.5–0:50.5**, the main risk. In the original recording "Packaging…" followed "instructions," with only a comma, so its opening intonation may sound like a continuation rather than a new sentence. The transcript and waveform cannot rule this out.
  - **3:14.0–3:16.5**, which runs from the room-tone pause into real silence. Levels match (about −62 to −73 dB); check for any audible change in the noise floor.
- **No end-to-end viewing pass.** Only the join strips and the frame mapping were checked.
- **Ring widths:** these are the 09-16 legacy widths, carried over unchanged (about 6–7 px solid at 720p, per the 09-26 section review). Nothing was re-rendered, so the fixed 4 px rule for 720p did not come into play.
- **Out of scope, noted only:**
  - The page alt text for Specific.
  - A pre-existing Notebook drawing around 2:01–2:04 (live 2:07–2:10) with garbled hand-lettered notes ("twist conscept now to referently this use!").
- **Not changed:** the live file, `index.html` (which already has uncommitted edits from another session; this task did not touch it), `manifest.json`, and the tracker. Nothing was committed.

---

# v5: closer framing on two boards (David's note on v4, 2026-09-26)

> "Board at :59. Zoom in closer. We don't need to show the illustration over the text. Do the same for the board at 2:05"

- Candidate: `Prompts/art-of-prompting-v5.mp4`. It runs 3:51.20 (6,936 frames). Audio, cuts, and timing are identical to v4.
- Build: `.video-venv/bin/python scripts/video/build_art_of_prompting_v5.py`. This is the same single pass from the live file as v4, with two board legs re-rendered from the canonical JPGs.

| Board (v5 time) | Before (v4) | v5 |
|---|---|---|
| Four Moves for Better Prompts, Move 1 (0:59.33–1:15.60) | Full view 2.9 s, then a "dive" to the whole tall card at 1.07×, with the illustration in frame | Full view 2.9 s (unchanged), then a dive to the text panels of both cards at **1.52×**, framed to start where the illustrations end. Ring timing is unchanged. The whole-card ring became a ring around Move 1's text, drawn on the same inner lines as its Include and Weak rings so it clears the top of the frame. |
| Four Moves for Better Prompts, Continued, intro (2:04.33–2:11.70) | Full view the whole 7.4 s | Full view 2.0 s, then a dive to both cards' text panels at **1.47×**. No rings, because the narration introduces the board as a whole. |

**Exception to Edit Spec §1b/§4 (on David's instruction):** the camera leaves the card illustrations out of frame. No text is cropped: both cards' full text is on screen in each held frame.

**Rings on the new legs:** these use the house `draw_ring` at `ring_px(720)`. `ring_stroke.py` reads **4.0 px** for every sample from 1:02.5 to 1:15.5, matching the What Is AI? 20260926ship2 reference. I tried an exact analytic 4 px stroke first, but it read 2–3 px, thinner than the approved reference, so I dropped it. All other boards keep their 09-16 rings at 6–7 px, so the video now mixes stroke widths across boards.

**Checks:**
- `transition_guard.py` passed all 6 boundaries (1480, 1780, 2268, 3730, 3951, 5859), and I inspected the strips.
- Only frames inside the two legs differ from v4 (the max diff elsewhere is 0.03).
- I checked the settled frames at full resolution. No sliver of an illustration shows, and no ring is clipped.

**Not changed:** the Move 2 board (1:26) and the Move 4 board (2:43) keep the old 1.07× whole-card dive. The live video and page are also unchanged.

---

# v6: the same zoom on Move 2 and Move 4 (David's note on v5, 2026-09-26)

> "at 1:29, zoom in to the right side of the board like you did for the left side. at 2:44, do the right side of the board the same zoom in as you did on the left side."

- Candidate: `Prompts/art-of-prompting-v6.mp4`. It runs 3:51.20 (6,936 frames). The audio stream is byte-identical to v5 (packet MD5 `b6a1b407…`).
- Build: `.video-venv/bin/python scripts/video/build_art_of_prompting_v6.py`. It uses the v5 script with two more legs.
- I regenerated `edited.wav`, which had vanished from the audit folder, using v4's exact cut math. I did not rebuild v4.

| Board (v6 time) | v5 | v6 |
|---|---|---|
| Four Moves, Move 2 (1:26.17–1:44.07) | 1.07× whole-card dive | Full view 2.0 s, then the Move 1 text-panel window (1.52×). The ring around the Move 2 text starts at 1:26.87 in full view (the 09-16 onset). Include and Weak follow at their 09-16 frames. |
| Four Moves Continued, Move 4 (2:42.97–2:54.13) | 1.07× whole-card dive | Full view 2.0 s, then the intro's text-panel window (1.47×). The ring around the Move 4 text starts at 2:43.57 in full view, followed by Include at its 09-16 frame. |

**Checks:**
- `transition_guard.py` passed all 10 boundaries.
- Only frames inside the two new legs differ from v5 (the max diff elsewhere is 0.19).
- `ring_stroke.py` reads 4.0 px on every new blue and amber ring sample. One amber sample reads up to 4.5–5 during the dive.
- All four Four Moves boards now share the closer framing and the fixed-4 px stroke. The good-question board keeps its 09-16 rings at 6–7 px.

---

# Shipped: v6, 2026-09-26 (David: "ship it")

- Installed `Prompts/art-of-prompting-v6.mp4` as `course-assets/art-of-prompting/art-of-prompting.mp4`, byte-identical. sha256 `ecf5ffc0…ff71f777e`, 21,340,096 bytes.
- Cache key: `index.html` `LESSON_VIDEOS.prompting` changed from `?v=20260916ship1` to `?v=20260926ship10`. The pill stays at "4 min" (3:51).
- `course-assets/manifest.json` video_assets row updated with the new sha256 and bytes.
- **Still unperformed at ship:** listening. Nobody on the editing side has heard the two joins (0:48.5–0:50.5 and 3:14.0–3:16.5), and there was no end-to-end watch-through. David authorized the ship knowing this.

---

# v7: good-question rings at 4 px, shipped 2026-09-26 (David: "do it")

- **Source:** built from the 20260916ship1 file (restored from git `56eec4cf^`), the same source as v4–v6, so it takes no extra encode generation. Build: `.video-venv/bin/python scripts/video/build_art_of_prompting_v7.py`.
- **Change:** the good-question leg was re-rendered with `ken_burns_path` from the canonical JPG. It uses the 09-16 camera beats and ring rects and times, cut at v4's frame 675 with the same 8-frame hold, and rings at `ring_px(720)` = 4. Nothing else changed.
- **Checks:**
  - The audio stream is byte-identical to v6 (packet MD5 `b6a1b407…`).
  - Frames outside the leg match v6 (max mean diff 0.18).
  - Inside the leg, the framing matches v6 and only the ring pixels change (at most 1.45% of the frame).
  - `ring_stroke.py` reads the good-question rings at 4.0–5.0 px (they were 6.0–7.5). Every ring in the video now comes from the same renderer and stroke setting.
  - `transition_guard.py` passed all 11 boundaries.
- **Shipped:** v7 installed byte-identical. sha256 `0e7437ee…9af934b`, 21,363,702 bytes. Cache key `20260926ship11`, manifest row updated.
- **Still not done:** listening to the two audio joins, which are unchanged since v4.

## v8 (2026-09-27): new Four Qualities board

David: "We've updated the board on the page. Use the new board in the video. It's a short board, so no need for zooming and panning. Just highlight each internal box as spoken."

- Candidate: `Prompts/art-of-prompting-v8.mp4` (6936 frames, 231.20 s, same as live). Build: `scripts/video/build_art_of_prompting_v8.py` (v7 chain from the 20260916ship1 source; only the good-question leg changes).
- Board: `art-of-prompting-good-question.jpg` sha 28a2780e… (1600x656, uncommitted page change). Compact: full view for the whole leg (0:26.6-0:49.3), no push/dive/pan.
- Rings at the 09-16 spoken onsets (leg frames): banner "foundation" 73 (#6e51ff), Open-Minded 143, Specific 278, On Target 416, Open-Ended 551 to the leg's end. Rects are the new JPG's measured card/banner edges.
- Checks: audio stream bit-identical to live (PCM hash); frames outside 797-1479 match live to encoder noise (max mean diff 0.42); ring_stroke 4.0 px on violet/purple/blue/amber, teal 5.0 (same as live v7's teal, house draw_ring); transition_guard PASS at 797 and 1480, strips inspected.
- SHIPPED 2026-09-27 on David's "ship it": cache key 20260927ship3, manifest row updated.
