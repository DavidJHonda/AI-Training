# Fake Trap v4 — build review (2026-09-20)

Status: review candidate only. The live video, both raw rolls, `index.html`, the lesson
Markdown, and the board JPGs are unchanged (protected hashes verified after render).

- Candidate: `Prompts/fake-trap-v4.mp4`
- SHA-256: `09e625fe2124e2aaf86bac9f8009d0f0960b6474623a963dfb26a89116c79c6f`
- Runtime: 9,240 frames at 30 fps (5:08.00), 1280×720
- Build script: `scripts/video/build_fake_trap_v4.py`; manifest: `edit-manifest.json`
- Scope: full production pass on `Prompts/fake-trap-new-2.mp4` (the 2026-09-20 materials-test
  roll 2) under the approved best-of plan in `../REVIEW.md`. Owner decisions 2026-09-20: no
  skeptic-sentence graft, no ring on the reasons banner, no second visit to the checks board.
- A first render of this candidate had a blank hold at 4:08 inside a borrowed roll-1 drawing
  (the drawing fades out at its 3:15.9). That render was never handed over; it was deleted and
  the borrow trimmed to the drawing's stable span. This file is the only v4.

## Narration

Roll 2 is the spine, single voice, from its first word to its verbatim close. One graft:

| Beat | Removed from roll 2 (source frames) | Inserted from roll 1 (source frames) | Output span |
|---|---|---|---|
| Four motives | 2931–3390 (1:37.70–1:53.00: "First, money…" through "…humiliate someone.") | 2589–3135 (1:26.30–1:44.50: "Money. Outrage generates clicks and clicks pay. Power. … Cruelty. … particularly at school.") | 1:37.70–1:55.90 |

- Donor gain 0 dB: speech RMS roll 1 −16.18 dBFS, roll 2 −16.20 dBFS (donor span −15.46 vs
  roll 2 neighbourhood −15.58).
- Both audio seams sit inside measured quiet: cut out of roll 2 at 97.70 s (quiet 97.43–97.97,
  before the breath for "First"); donor starts 0.26 s before "Money" and ends 0.52 s after
  "school."; roll 2 resumes at 113.00 s (quiet 112.46–113.10, "If" onset 113.12).
- Encoded seams: sample jump 0.00061 and 0.00000 full scale; noise floor within 0.7 dB across
  each seam.
- The engine outro after "pixels." is removed; the close audio ends at roll 2's 301.10 s.
- Rendered transcript (`verification/fake-trap-v4/transcript.txt`) read in full: every teaching
  point from the roll-2 review is present, the grafted list reads as one continuous beat, the
  two closing lines are the last words, nothing spoken after.

No teaching pause was added. Natural gaps at the four proposed pause points, measured in the
encoded file: 0.72 s (banner → definition, 1:08), 0.61 s (graft seam → detector, 1:55.9),
0.36 s (Board 3 → emotions, 2:27), 0.55 s (eyes → safety, 4:16.9). The 0.36 s gap at 2:27 is
roll 2's own pacing and was left alone; flag it if it feels rushed on listening.

## Boards (all canonical page assets, rings drawn post-crop at 5 px)

| Board | Output span | Density | Treatment |
|---|---|---|---|
| The Same Clip. Two Eras. | 0:26.80–1:07.90 | dense | Full view 4.1 s; dive + amber ring on Before AI at "Before artificial intelligence" (0:30.9); dive + blue ring on The AI Era at "In the AI era" (0:45.7); back to full view with the banner ringed at "Appearance can mislead" (1:04.8). Replaces the faceless upload variant. |
| Why Some Fakes Aren't Friendly | 1:34.33–1:55.90 | dense | Full view 3.6 s under roll 2's introduction; dive + ring on Money / Power / Fame / Cruelty at roll 1's onsets (1:37.9 / 1:41.5 / 1:45.9 / 1:50.2). Banner unringed. |
| Check the Source, Not the Pixels | 2:14.53–2:24.23 | compact, no push | Full view; banner ringed at "Shift your focus…" (2:20.1). Replaces the close board Notebook showed here. |
| Move the Test Off the Image | 2:35.17–3:06.63 | compact, no push | Full view 2.6 s; card rings Source / Context / Corroboration at their names (2:37.7 / 2:43.4 / 2:51.1). |
| Standard close | 4:58.87–5:08.00 | — | 48-frame hold, 150-frame push to 1.2×, 76-frame settle; literal final frame. |

Longest unbroken board run: 41.1 s (Board 1). State sheets: `states-*.jpg`; every settled ring
frame inspected at full resolution (right card, complete card inside the ring, nothing clipped).

## Notebook spans replaced (Edit Spec 2 and 8c)

| Roll-2 span | What it was | Cover | Frames used |
|---|---|---|---|
| 1:07.90–1:17.20 | Roll 2 held its render of the faceless board under the definition and second jaw | Roll 1's "1st Jaw / 2nd Jaw" drawing | roll 1 1860–2104, last frame held 35 frames |
| 1:19.37–1:23.20 | Photo-real Stanley Cup on a notebook page with a real hand | Roll 1's three-friends-with-the-Cup drawing | roll 1 2104–2258, held 0 |
| 3:41.60–3:46.73 | Photo-real folder on a desk | Roll 1's question-mark-and-magnifier drawing | roll 1 5227–5361, held 20 frames |
| 4:00.53–4:05.50 | Photo-real phone contacts on a notebook | Roll 1's "urgent request ✗ pre-saved database" cards | roll 1 5760–5875, last frame held 34 frames |
| 4:45.27–4:53.90 | Photo-real shield on a notebook | Roll 1's Trusted Adult / Platform Report / Take It Down cards | roll 1 6900–7005, last frame held 154 frames |

Every borrow onset was frame-checked past its fade-in. Everything else is roll 2's own drawing.
Drawn people with faces (bench at 1:24, counselor at 4:40) are Notebook drawings, not photos.

Corner mark: the Gemini mark was on every frame of both rolls (the watermark toggle was on).
The render cleaned it on every kept Notebook frame: 4,802 cloned, 1,049 inpainted, 0 declined.
Board legs and the close never carry it.

## Verification

- Decoded 9,240 frames, matches the plan; 308.01 s of audio.
- `transition_guard.py`: 18 of 19 declared boundaries pass. The one flag, at output frame 2931,
  is the reasons board's own camera dive to the Money card (continuous motion over frames
  2915–2939, deltas 9–24 per frame, no stale island); the strip was inspected frame by frame.
  All 19 strips inspected: the first frame after every boundary is already the destination.
- Contact sheets (`verification/fake-trap-v4/sheets/`, every 4 s) reviewed end to end: no
  photograph, no Notebook rendering of a course board, no web address, no engine outro; the
  close board is the final picture.
- Protected files unchanged: roll 1, roll 2, live video, five board JPGs, lesson Markdown.

## Listening checks for David (not auditioned here)

1. 1:37.7 — roll 2's "…four goals behind harmful fakes." into roll 1's "Money." (voice and
   energy continuity across rolls).
2. 1:55.9 — roll 1's "…particularly at school." into roll 2's "If you suspect a clip is malicious."
3. 2:27 — the 0.36 s gap between "…toward independent evidence." and "Fakes travel quickly."
4. 4:58.9 — "You did nothing wrong by being targeted." into the close lines (same roll, no cut,
   just the board arriving).

## Not done

- No headphone audition of the seams or of pacing; transcript and waveform checks only.
- Ship checklist otherwise complete for a full pass. Not shipped: needs David's listening check
  and approval. On approval: replace `course-assets/fake-trap/fake-trap.mp4`, bump the cache
  key in `LESSON_VIDEOS`, pill stays "4 min" (5:08 rounds to 5; owner's call on the pill).
