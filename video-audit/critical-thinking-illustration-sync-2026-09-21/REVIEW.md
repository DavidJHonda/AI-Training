# Critical Thinking v13: SHIPPED 2026-09-21 (illustration sync with dives and rings, narrow visual repair)

**Scope.** David, 2026-09-21: "Critical Thinking shows the illustration from :57 to 1:16." The Same Claim. Different Thinking.
board is the lesson's middle illustration (`index.html` line 8599, `?v=20260921batch6`); the refresh replaced it in place — same
board, same 1600x1077 dimensions, same title, THE CLAIM strip, two comparison cards and takeaway banner. Only that span changes.
Narration, timing, FPS, frame count and the audio stream are untouched. Eleventh of the day's illustration syncs.

**The board's wording changed too, and it is safe.** Besides the new cast, the two pills now read FIRST REACTION and SECOND
REACTION where they read LUKE'S REACTION and NATE'S REACTION — matching the lesson copy the parallel session changed the same day.
The narration over this stretch never speaks either name; transcribed from the live audio: "The face value reaction was immediate.
Sounds great. I believe it. But a critical thinking reaction takes a different path. Wait. What's behind the claim?" So the new
wording contradicts nothing the student hears. (`lessons/critical-thinking.md` still carries the old "Luke's reaction" /
"Nate's reaction" lines for the generation source — someone should bring that file in line, outside this repair.)

**Span.** Output frames 1710–2315 (0:57.00–1:17.17), 605 frames. Verified by decoding: the OLD JPG rendered through the shipped
leg spec (stroke forced to the old constant 5) reproduces the live video at 3.06 mean per-pixel difference, sampled every 15
frames and at every beat and ring onset, nothing over 6.

**Dives and rings, the shipped ones, verbatim.** 82-frame establish, THE CLAIM ring at full view, dive to Face Value, 126-frame
hold, pan to Critical Thinking, 129-frame hold, 30-frame pull back, 162-frame full hold with the banner. All four rectangles and
all three dive windows land exactly as before on the refreshed art. Stroke follows the artwork-scaled rule: 5 px at the dives —
the shipped weight, so the two card rings are unchanged — and 4 px at full view, where THE CLAIM ring and the banner ring live.

**The audio is the delicate part, and it is bit-identical.** The live file is v12: v11's video with a deliberately re-encoded AAC
track (256 kbps, PNS and TNS disabled to remove a tonal artifact at 2:54). This build packet-copies that track; its payload
sha256 matches the baseline's exactly, so the fix survives untouched.

**Build.** `scripts/video/build_critical_thinking_reactions_sync.py`. Baseline: the shipped file itself, frozen here as
`baseline-live-2026-09-17.mp4` (sha256 fe9fed9a912b…, 5935 frames, gitignored). Canvas from
`editspec_build.Build.compose` at its default tall margin: 2068x1164 at offset (234, 43), matching the v11 manifest. One
`ken_burns_path.py` leg, one concat pass.

- Asset: `course-assets/critical-thinking/critical-thinking-two-reactions.jpg` (a85e157775995677…, 1600x1077). Previous:
  778a3222f47dc7b1…, the sha the shipped build recorded. The build asserts the new sha's prefix, so a further revision of the
  artwork fails loudly instead of shipping unreviewed.
- Candidate: `Prompts/critical-thinking-v13.mp4` (fc07ea211e70…), shipped to
  `course-assets/critical-thinking/critical-thinking.mp4` and removed.
- Cache key `20260917ship1` → `20260921ship19` on the `critical` entry. Pill unchanged and correct (3 min; 3:17.83).

**Note.** The refreshed JPG was still uncommitted in the working tree at build time (modified 18:24) — it belongs to the parallel
refresh session, which commits its own assets and lesson copy. This ship staged only the video, this script, this audit directory
and the one `LESSON_VIDEOS` line.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 5935 frames at 30 fps, matching the baseline exactly. Leg decoded its 605 frames.
2. Audio packet payload sha256 identical to the baseline; the v12 AAC track was never re-encoded.
3. `transition_guard.py` on eleven declared boundaries: both splices pass and their strips were inspected (the hand-drawn
   chocolate headline into the board at 1710, the board into the study-design drawings at 2315), one clean cut each way. Seven
   beat/ring boundaries flag one-frame islands; running the same guard on the **baseline** flags the same seven at the same
   frames, so it is the detector reacting to the shipped camera motion.
4. Frame diff against the baseline every 10th frame: inside the span mean 7.76 (the new cast and the new pill wording); outside
   it mean 0.31, max 0.98 — re-encode noise. Nothing outside 1710–2315 changed visually.
5. Per-frame motion profile inside the span correlates 0.9999 with the baseline's, maximum difference 1.20.
6. States inspected (`state-001710-board-open.jpg`, the three ring states, `state-002149-banner.jpg`,
   `state-002314-board-last.jpg`): correct component ringed in each, card text and both pills readable at the dives, banner
   readable at full view, nothing clipped.
7. Not re-auditioned by ear: the audio is bit-identical to the shipped file. The 2:54 whistle fix lives in that track and is
   therefore unchanged, but this build did not re-listen to it.
8. Not performed: a full end-to-end rewatch, and no check of the lesson's other two boards (the equation board and Five Habits),
   which this repair does not touch and the refresh did not change.
