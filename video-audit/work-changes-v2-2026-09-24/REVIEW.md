# Work Changes v2 — build record, 2026-09-24

Candidate: `Prompts/work-changes-v2.mp4` (5:14.8, 9443 frames). Review only; live video unchanged.
Build: `.video-venv/bin/python scripts/video/build_work_changes_v2.py` (manifest: `build/edit-manifest.json`).
Approval: David, 2026-09-24, "yes, build it" on the roll 4 repair plan in
`video-audit/work-changes-review-2026-09-24/REVIEW.md`, waiving three near-verbatim lines.

## Narration changes (base: Prompts/work-changes-4.mp4)

| Change | Source | Words |
|---|---|---|
| Graft 1 (−0.4 dB) | roll 2 4.00–12.65 over r4 4.00–14.35 | "Familiar job titles like entrepreneur, teacher, lawyer, or designer will still exist, but the daily reality of those roles is already changing." |
| Cut | r4 225.00–226.40 | "Look at the bottom banner." |
| Graft 2 (−5.3 dB) | roll 1 200.45–207.20 over r4 252.45–258.50 | "In one study, consultants finished certain tasks 25% faster, achieving 40% higher quality." |
| Graft 3 (−0.5 dB) | roll 2 250.30–253.55 over r4 283.00–287.10 | "AI can make you productive before it makes you knowledgeable." |
| Cut | r4 310.10–319.80 | "Because AI is permanently changing … falls entirely on you. Look at this final message." |
| Tail | after r4 323.70 | "Thank you." and the end card |

Waived (no roll speaks them verbatim): "It's what you already know." (spoken "The answer is what you already know."),
the focus line, the learn/school line. No pauses added.

## Pictures

Boards (canonical JPGs): Four AI Strengths (dense, card dives), Your First Assignment (compact, full view), Two Ways
(compact, banner ring), What Changes (compact). On-screen runs: Strengths 23.7 + 7.5 s; Assignment 19.3 / 10.0 / 15.0 /
14.9 s; **Two Ways 33.8 s unbroken; What Changes 24.7 s unbroken** (no people-free drawing fits either).

Covered from other rolls (all people-free, no invented figures): drawn graduate; drawn teacher/lawyer/designer (removed
with graft 1); Notebook's own board render before Board 1; chapter card "02 The Human Element"; drawn office workers
and hand editing; invented "85% of timeline" chart; drawn professional/robot faces; drawn man in empty room; drawn
people over entry-level work; invented "Productivity Outpaces Knowledge" chart; drawn person with tablet; drawn
student reading and campus crowd. The full list with frames is in the manifest timeline.

Kept from roll 4 with figures: Two Pillars diagram (small portrait icon, 0:13–0:21) and the hand signing an "Approved
By A. Johnson" report (3:54–3:58).

## Verification (on the encoded file)

- medium.en transcript of v1 matches the plan; all three grafts and both cuts read correctly. Whisper's "you" at 5:14.7
  is a hallucination over the silent close hold (word-level pass shows silence).
- `transition_guard.py`: 34 boundaries, 0 failures (strips in `transitions/`).
- Audio joins: max sample step ≤ 301 at every join (speech 99.9th percentile 7607), no clicks; noise floors on both
  sides are ~−70 dBFS or lower, no cliff.
- Corner mark: 0 declined frames. Protected sources unchanged.
- Fixed during verification: the entry-level donor held a mid-crossfade frame; its end moved to roll 2 frame 7122.

## Not yet done

- **Listening by ear.** The three graft seams (0:04, 0:12.7, 4:09–4:16, 4:40–4:44) and the two cuts (3:43, 5:07)
  were measured, not heard. Graft 2 is roll 1's voice at −5.3 dB; its cadence against roll 4 needs David's ear.
- Your First Assignment is a tall board: its list text is small at full view. Column zoom gains only ~1.2×, so it was
  left at full view; preview and decide.
- Not shipped; `course-assets/work-changes/work-changes.mp4` is untouched.

## v2 changes (David's notes on v1, 2026-09-24)

- **Flash at 0:13 fixed.** v1 showed 0.6 s of roll 4's coffee-and-tablet drawing between the roll 2 graft and the Two
  Pillars diagram. v2 starts the Two Pillars scene at its first frame (roll 4 frame 450), holding its last frame
  before Notebook's board render.
- **Your First Assignment highlighted by section, as in the live video.** Dense, with a camera dive per section:
  the assignment 1:34, Before AI header 1:43, first pass (under the drawing, visible on return) 1:57, then you
  2:03, the result 2:07, With AI header 2:13, AI does the first pass 2:28, you start here 2:33, the result 2:42.
  Breaks moved so every section is seen while spoken: result/rework drawing now 2:08–2:11, AI automation drawing
  2:18–2:23 (under "The AI completes that entire first pass in minutes").
- **Audio dropouts fixed (also present in v1).** The builder fades every row in and out of room tone over 5 ms;
  where a picture swap splits one continuous sentence, that left a 10 ms dip inside speech (ten in v1, the deepest at 0:47.6, 2:23.4
  and 4:52.6). v2 restores the untouched source samples at all 25 audio-continuous
  boundaries (deviation from source now 0). Grafts and cuts keep their crossfades.
- Verified: 34 boundaries pass `transition_guard.py`; 0 corner-mark frames declined; protected files unchanged.
