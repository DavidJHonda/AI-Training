# One More Thing v9 — new Board 1, and the branching-paths drawing restored (2026-09-23)

**Candidate:** `Prompts/one-more-thing-v9.mp4` — 8077 frames, 4:29.23, 1280x720, 30 fps.
**Built by:** `scripts/video/build_one_more_thing_v4.py`. (v8 deleted; it held a static board over the beat below.)
**Supersedes:** v7 (`video-audit/one-more-thing-build-2026-09-22/REVIEW.md`), deleted — it carries a board
that is no longer the lesson's board.
**Scope:** review candidate only. The live `course-assets/one-more-thing/one-more-thing.mp4` (v5) is unchanged.

David, 2026-09-23: "I modified the Same Probabilities, Different Choices box. We need to use that version
in the One More Thing video." The asset changed under the same filename, so this is a picture-only rebuild.

## What changed

On the board (`course-assets/one-more-thing/one-more-thing-draws.jpg`, same 1600x910):

- "Five Separate Tries" → **"Five Random Picks"**
- "Unchanged across all five tries" → "Unchanged across all five picks"
- a new three-line caption under the list: *"Spot was picked only once, even with the highest probability.
  Another five picks could turn out differently."*
- the five rows now end at y=625 instead of 671; the left panel is byte-for-byte the same layout
  (rows 286–691, Other row 642–691)

In the build, one line: the right-hand ring runs to 730 instead of 681, so it holds the whole column —
heading, the five picks and the caption. Everything else is identical to v7: the narration, both grafts,
all three pauses, the other seven rings, the close.

## v9: the graphic at 1:54–2:07

David, 2026-09-23: "At 1:54 we say 'and because each new word...' It goes to 2:07. We need graphics
here. What about using graphics from the How AI Answers video... We could use that, and keep the final
frame appearing."

He is right that the beat needed a picture, and the picture was already in the roll. Board 1 now ends at
Notebook's own cut at source 3152 (105.07) instead of running on to 3540, and roll 2's own drawing plays
underneath the whole beat — output 3413 to 3801, which is **1:53.8 to 2:06.7**, the span he named.

What it draws, in step with the line: **Max** → is / chases / sleeps with their percentages → Path A
lights up through chases → a ball → into the lake and spells out *"Path A: 'Max chases a ball into the
lake'"* → then Path B runs sleeps → on the sofa → until morning and spells out *"Path B: 'Max sleeps on
the sofa until morning'"*. Two whole sentences diverging from one different token. The pause then holds
the frame with both paths readable. Contact sheet: `contact-branching-drawing.jpg`.

**This was my error, not a missing asset.** Frames 1570–3152 are Notebook's recreation of our board and
are covered as always; 3152–3540 is a genuine drawing, and v1–v8 hid it only because I ended the board at
the NEXT cut rather than at the one where the recreation stops.

**The How AI Answers borrow was declined**, with David's agreement (`option-how-ai-answers-loop.jpg`).
Its mechanism half fits well — Current Context → AI Model → Next Token with the buffer filling
You/could/name/him/Spot, the same dog-name example — but: its heading reads "AUTOREGRESSIVE INFERENCE
LOOP" and this lesson's prompt bans "inference" from the narration outright; its `<EOS>` / "GENERATION
COMPLETE" beat would land under "a single unexpected choice immediately cascades", where a closed
sequence argues the opposite; it carries P( Token | Context ) notation the lesson never uses; and How AI
Answers is the lesson immediately before this one in Understand AI, so the drawing would appear twice in
a row.

## Verification

| Check | Result |
|---|---|
| Decoded frame count | 8077, matches the manifest exactly (4:29.23) |
| Audio vs v8 | **identical within ±60 LSB at every one of 12,923,904 samples** (−54 dBFS; AAC re-encode plus one extra 5 ms crossfade pair). The v8→v9 row split at source 3152 sits in clean silence — the gap runs 104.90–105.11 and speech starts at 105.12 |
| Picture vs v7 outside Board 1 | max mean per-pixel diff **0.11 before** the board and **0.41 after** — re-encode noise, no content change |
| New board artwork | Board 1 mean diff 3.62 vs the old board, as intended |
| `transition_guard.py`, 13 boundaries | pass, 0 failed |
| Engine corner mark | 2597 cloned, 535 inpainted, **0 declined** (388 more source frames now pass through cleaning) |
| Pauses | all four frozen |
| Protected files | all unchanged |
| Ring states | `states-1-draws.jpg` — the Five Random Picks ring encloses heading, picks and caption |

## Open: the narration now says "tries", the board says "picks"

David reworded the lesson page, `lessons/one-more-thing.md` and `Prompts/one-more-thing-video-prompt.txt`
from "tries" to "picks" in the same pass, and added the caption as **required verbatim line 2**. Neither
roll was rolled against that:

1. **Required line 2 is not spoken in either roll.** Roll 2's nearest is "Spot, our mathematical top
   choice, only wins once." (81.28), which carries the first half of the caption but not "Another five
   picks could turn out differently."
2. **The noun differs.** The board says *picks*; roll 2 says "five consecutive, completely separate
   **attempts**" (74.40) and the graft says "**Try** one is max… And **try** five returns to max." The
   mapping is still exact — the same five names in the same order — so nothing contradicts, but the
   picture and the words use different words for the same thing.
3. Required line 1 still reads "22 times out of 100 **tries**", which David kept, so "tries" is not
   banned outright.

Only a reroll on the updated prompt closes 1 and 2; this build cannot. The prompt and Markdown are already
updated, so the materials are ready whenever David wants one.

Also still open from v7: both graft joins want David's ear (84.96–93.64, 246.62–249.64), and the Notebook
bar chart at 0:25.2–0:43.6 whose dog names and percentages contradict Board 1.

## If it ships

Install as `course-assets/one-more-thing/one-more-thing.mp4`, bump the `inference` cache key in
`LESSON_VIDEOS` (currently `?v=20260918ship1`), and leave the pill at "4 min" — 4:29 still rounds to 4.
