# Context Window — the 2026-09-21 reroll (rolls 1 and 2)

`Prompts/context-window-1.mp4` (3:12.60, 55 cuts) and `-2.mp4` (4:20.17, 43 cuts), the first rolls from
the kit rebuilt on the 2026-09-20 recipe — VOICE block, seven required-verbatim lines, beat spine,
Boards 1 and 2 uploaded as faceless variants. The live video
(`course-assets/context-window/context-window.mp4`, 4:30.20, 231 cuts, shipped 2026-09-16 as v3) was
rolled from the old prompt without the VOICE block.

**Verdict: roll 2 is the base, with two identified repairs. It is the only one of the three that both
teaches the whole lesson and speaks in the lesson's own voice. Roll 1 is REROLL — at 3:12 it drops all
three Personalization/Saved Memory/Projects examples, never names the five sources separately, and
loses how each outside-the-window item gets in. The live video is complete but carries the formal
register the new kit was written to remove.**

## The seven required lines

| # | Line | roll 1 | roll 2 | live |
|---|---|---|---|---|
| 1 | "What car should I buy after I graduate from college?" | MET | MET | MET |
| 2 | "Same question. Different context. Different answer." | MET | MET | MET |
| 3 | "Different doesn't always mean wrong." | MET, but inside the Markdown's own compound sentence ("…not to trust the output, **but** different doesn't always mean wrong") | MET, its own sentence at 0:57 | MET, its own sentence |
| 4 | "With the right context, AI gives better answers." | MET at the close, after a "**Always remember,**" lead-in; the mid-lesson instance is missing | MET twice — 0:59 and at the close, the close after an "**Ultimately,**" lead-in | MET twice, the close clean |
| 5 | "You don't have to start from scratch every time you ask a question." | MET | MET, prefixed "By setting these up," | MET, prefixed "By utilizing these features," |
| 6 | "If it isn't in the context window, the model can't see it." | MET | MET | MET |
| 7 | "Control the context, control the quality." | MET | MET | MET |

All seven land in all three. Worth recording against the Document Trap finding: line 3 is the one
required line that sits buried mid-paragraph in this Markdown, and **it landed anyway in both rolls**.
So "buried in prose" is not on its own a reliable predictor of failure — the Document Trap failures may
owe more to three required lines being crowded into a single twenty-second beat. Treat the layout
change made there as a reasonable bet, not a proven fix.

## Coverage, beat by beat

| Teaching point | roll 1 | roll 2 | live |
|---|---|---|---|
| 2 + 2 calculator; AI doesn't work that way | RICH | RICH | TAUGHT, formal ("Identical inputs yield identical answers") |
| The car question and both responses word for word | RICH | RICH, but drops "**but**" from Luke's ("could work well, compare its price") | RICH |
| Luke and Nate typed the same prompt and still got different answers | RICH | THIN | RICH |
| **Why they differ: earlier in his chat, Nate said he loves pickup trucks** | **RICH** — "This happened because earlier in his chat, Nate said he loves pickup trucks. The AI recognized this past detail and used it to suggest the Ford Raptor." | **THIN** — "the AI remembered an earlier detail from his chat history"; the pickup-truck detail is never named as the reason | RICH |
| Some people distrust varying answers; tailoring is a strength | RICH | **MISSING** | RICH |
| Context window defined; working memory with a limit | RICH | RICH (adds "not a physical storage space on a hard drive") | RICH |
| **All five sources named separately** | **MISSING** — "personalization and memory pull saved details" merges two of them | RICH — prompt, earlier messages and answers, personalization, saved memory, projects | RICH |
| **Personalization with its complete example** | **MISSING** | RICH | RICH |
| **Saved Memory with its complete example** | **MISSING** | RICH, but the last word is garbled — see below | RICH |
| **Projects with its complete example** | **MISSING** | RICH | RICH |
| **All four outside-the-window items and how each gets in** | **MISSING** — compressed to one list, no "how it gets in" | RICH, all four with their route in | RICH |
| Forgetting problem, both fixes, and that a fresh chat does not reset the limit | RICH | RICH | RICH |
| Voice: plain words, the lesson's own sentences | TAUGHT, with drift ("tools automatically inject context", "strict boundaries exist around data") | RICH | **WEAK** — "five **technical** sources", "one of AI's **functional** strengths", "the model's **technical** context window limit" |
| Close, nothing after | MET, lead-in | MET, lead-in | MET, clean |

Roll 1 is not a base: four of the lesson's biggest beats are simply absent, and at 3:12 against a 5-minute
pill there is no way to read that as trimming. It is a useful donor for exactly one beat.

## Roll 2's two repairs

**1. The Saved Memory example ends in a garbled word (2:19.3–2:23.2).** "The app saves that detail and
uses it later when you ask about buying a…" — the final word decodes as "BIPL" on `base.en` and
"biopole" on `small.en`. The Markdown's word is "vehicle". Two models failing differently on the same
word is the same signature as the Document Trap six-foul problem, and it lands on the payoff of the
pickup-truck callback. **David's ear decides**; the clip is roll 2 at 2:14–2:24.

   Donor: the live video says the sentence cleanly at **2:37.91–2:41.68** — "The app saves that detail
   and uses it when you ask about buying a vehicle." It is a whole beat between silences (0.21 s / 0.65 s),
   3.77 s against roll 2's 3.91 s, so it swaps in at nearly the same length. The live is 1.8 dB quieter
   (-17.7 against -15.9 LUFS), so it needs +1.8 dB.

**2. The "Why did this happen?" beat is generic.** Roll 2 explains the difference as "an earlier detail
from his chat history" and never names the pickup trucks — the one thing that makes the example land.

   Donor: roll 1 at **0:52.99–1:01.78**, "This happened because earlier in his chat, Nate said he loves
   pickup trucks. The AI recognized this past detail and used it to suggest the Ford Raptor." Whole beat
   between silences (0.35 s / 0.52 s), 8.79 s. It goes into roll 2's 1:02.35–1:02.79 pause, after "With
   the right context, AI gives better answers." — which is where the Markdown puts it. Roll 2's own weak
   sentence at **0:48.62–0:53.67** then comes out; it is cleanly bounded on both sides.

   Narrator pitch sits in a 168–208 Hz band across all three sources, consistent with one Notebook voice,
   but each seam is an ear judgement.

With both repairs the candidate lands near 4:24.

## Smaller notes

- Roll 2 says "This illustration shows the five specific sources…" and calls the context window a
  "working memory tray" — screen references to cut or cover.
- Roll 2 drops "but" from Luke's quoted response. The prompt says read both responses word for word.
  One word, inside a quotation; worth a note rather than a repair.
- Roll 2 skips "Some people see different answers to the same question as a reason not to trust AI… That's
  one of AI's strengths." Roll 1 and the live both have it. Not grafted in the plan above because roll 2
  already delivers the conclusion ("Different doesn't always mean wrong."); flagged for David's call.
- Visuals: roll 2 is drawn panels and diagrams throughout, no people, no photographs, and it renders both
  canonical boards for the edit to replace. It adds a "NOT Local Disk Storage" panel matching its spoken
  "not a physical storage space", which is consistent with the prompt's ban on calling the window a
  physical space.
- The live video's 231 cuts are worth knowing if it stays: that is by far the choppiest file in the library.

## v2 build (`build-v2/`, script `scripts/video/build_context_window_v2.py`) — CURRENT

David's notes on v1, 2026-09-21, all applied. Audio is byte-identical to v1; only the picture changed.

- **0:57-1:20 no longer sits on a finished board.** The Same Question board now leaves at 0:57, right
  after its banner line, and the live v3's own footage of those beats carries the stretch: its
  working-memory panel showing Nate's earlier "I love pickup trucks", then the AI Generation panel
  resolving to the Ford Raptor, under the grafted why-beat; then the desk drawing and the Context Window
  capacity panel under "It's called the context window… working memory… a strict capacity limit". The
  panel builds its capacity bar exactly as that line is spoken.
  The graft's picture had to be prepared by hand (`prepare_live_leg`): `Build.graft` takes picture and
  audio from the same file, and here the audio is roll 1's while the picture needs to be the live v3's.
- **Give AI a Head Start is now dense.** The camera dives to each column and pans across the three; the
  rings follow the sections inside a column - the feature, then its EXAMPLE block - instead of outlining
  the whole column. It pulls back to the full board for the banner.
- **Outside the Window is now dense too**, diving to each card as it is named, panning across both rows,
  and pulling back for the banner.
- Candidate: `Prompts/context-window-v2.mp4`; SHA-256
  `9e620ea08c04fe80d46a9ce8fc2e993afa99669ad32ba2db53f3b4ef958bfa09`; 7,964 frames at 30 fps (4:25.47).
  Corner mark 2,142 cloned, 133 inpainted, 0 declined. `transition_guard.py` 13/13 pass. Protected files
  unchanged.
- One more thing to know: the live footage at 1:19-1:23 is a drawing of hands on a keyboard. The kit says
  "Between boards use simple drawn scenes with no people"; this is hands only, and it is the live v3's
  own frame, not a new generation. Flagged rather than covered.

## v1 build (`build-v1/`, script `scripts/video/build_context_window_v1.py`; superseded by v2)

Built on David's instruction, 2026-09-21.

- Candidate: `Prompts/context-window-v1.mp4`; SHA-256
  `819f0ec79d8dc688c74058e2fdd2c4abb39bafff8e9a4773d13ad2b3ff9f598c`; 7,964 frames at 30 fps (4:25.47).
- Narration: roll 2 start to finish with both repairs. Roll 1's 0:52.80-1:01.97 carries the why-beat in
  at 1:02.57 and roll 2's weak version (0:48.40-0:53.83) comes out, so the finished line reads
  "…With the right context, AI gives better answers. **This happened because earlier in his chat, Nate
  said he loves pickup trucks. The AI recognized this past detail and used it to suggest the Ford
  Raptor.** What do you call everything the model can see…" - the Markdown's own order. The live v3's
  2:37.73-2:41.93 replaces roll 2's garbled sentence, +1.8 dB to match, and the finished audio reads
  "…uses it when you ask about **buying a vehicle**. Finally, projects act as…". Both grafts are audio
  only: the picture stays on the held board. Verified on the rendered file with `small.en`.
- Boards: canonical Same Question. Different Answers. 0:11.00-1:17.00 (question strip at 0:16.6, Luke's
  card at 0:19.9, Nate's card at 0:33.6, banner at 0:54.0); The Context Window 1:17.00-1:38.50 as an
  illustration camera walk, no rings, because it is a photographic render with a person at the left
  edge; Give AI a Head Start 1:45.13-2:42.93, arriving on its own introduction and held past its own
  banner line, with a column ring per feature; Outside the Window 2:45.67-3:29.33, likewise held to its
  banner, one ring per card; standard close from 4:10.37 as the literal final frame.
- Two geometry errors caught in the state sheets before the render: the five-sources walk had no room
  for its pull-back before the board's own cut, and both lower rings on Outside the Window cut through
  their own body text because that card's box was measured at a line gap and came out 124 px short.
- Corner mark cleaned on every kept frame: 1,842 cloned, 0 inpainted, 0 declined. `transition_guard.py`
  13/13 pass. All thirteen row boundaries measured: -50 to -66 dBFS in the 60 ms after the splice, worst
  peak sample difference 0.0046. Protected files unchanged.

## Listening checks for David

1. 0:57-1:07 - the why-beat graft. Roll 1's voice against roll 2's, and both seams.
2. 2:18-2:24 - the vehicle graft, and whether the repaired word now lands.
3. The whole file end to end; I read the rendered transcript and measured every boundary but did not
   audition the audio.

## Not repaired

- "Ultimately," still leads the first closing line. It is one breath group with the line itself, so it
  cannot be cut cleanly, and this prompt bans words *after* the close rather than before it.
- Roll 2 drops "but" from Luke's quoted response, and skips "Some people see different answers… That's
  one of AI's strengths." Both flagged in the review above; neither was grafted.
- A drawn person appears 3:29-3:35, against "Between boards use simple drawn scenes with no people."
  It is a drawing, not a photograph, and covering it would need a donor.
