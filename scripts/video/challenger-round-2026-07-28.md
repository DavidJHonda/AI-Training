# Challenger round — 2026-07-28

Six new rolls in `Prompts/`, all against sitting videos. Graded under r3 in the same
sitting as their incumbents (this morning's full re-grade), so the deltas are sound.
Per-video numbers in `challenger-round-2026-07-28.csv`.

**5 SWAP, 1 REJECT.** Worth noting against the 7/25 round, which went 0-for-8.

| lesson | new | old | Δ | verdict |
|---|---|---|---|---|
| ai-is-math | 87 | 83 | +4 | SWAP |
| training-bias | 84 | 80 | +4 | **REJECTED by David 7/28** |
| which-app | 86 | 83 | +3 | **SHIPPED 7/28** |
| fake-trap | 89 | 87 | +2 | **SHIPPED 7/28** |
| flattery-trap | 89 | 87 | +2 | SWAP |
| questions-matter | 81 | 86 | −5 | REJECT |

Nothing has been moved. Challenger re-runs get a recommendation, not an automatic
install — the standing auto-intake covers new lessons, not replacements of live ones.

## Why this batch beat the last one

David's framing was right and it shows in the transcripts: these came from the older,
stricter prompts, and the **rules that were retired on 7/27 were never what was wrong.**
What actually improved is the thing the rubric cares about — **deck-referential
narration collapsed**. ai-is-math went from 5 instances to ~1; flattery-trap 4 to 2.
That is the catalogue's weakest r3 dimension (teaches-vs-recites, 79% of max) and it
moved without a single rule aimed at it.

All six rolls are **watermark-clean** (detector max 0.21–0.43 against a 0.45 threshold).
That is decisive for training-bias, whose incumbent carries the mark on 112 of 146
sampled frames and whose 80 is almost entirely that.

## Per-video notes

**fake-trap 89 → SWAP.** Fixes the incumbent's one real gap. The lesson has two jaws
and the live video only ever covers one; this roll states the second at 1:13–1:26:
*"The second half of the trap is just as dangerous, dismissing the truth as AI just
because you don't like what you're seeing."* Garbles to check by ear: "feet" for feed
(0:22), "Cloud" for clout (1:54), and the close is "Ask the source, not the pixels"
where the lesson says "Check".

**flattery-trap 89 → SWAP.** Quotes the weak Gatsby paragraph verbatim instead of
paraphrasing it, and names "viral gold". Handles the gag product with more restraint
("a product we will politely refer to as"). One garble at 4:23: *"Never take an AI's
initial praise, spread a final word"* — should be "as the final word".

**ai-is-math 87 → SWAP.** Names Pascal, Fermat and Bayes where the incumbent said only
"two French mathematicians". Cleanliness is its weak spot, not the incumbent's: the
weather monitor at 1:18–1:23 letters style words into the art ("Weather tracking
whiteboard paper", "Exparative hoafithment onckling isterm") and the Bayes portrait at
1:23–1:28 is surrounded by nonsense equations. Both are incidental b-roll, so they cost
little under the rubric, but the weather one is the style-leak class. Garbles: "Blaze
Pascal", "Thomas Bays", "Tooting these models" (tuning), stray "methodical" at 1:45.

**which-app 86 → SWAP.** Names In-N-Out and McDonald's — the lesson's actual analogy,
which the incumbent described without naming. Runs 4:26 against the incumbent's padded
5:19, which was its single biggest deduct. It does lose something: the incumbent spells
out each app's *catch* (ChatGPT's looser guardrails, Claude's refusals, Gemini's
ecosystem dependency); this roll only implies them. "breath" for breadth, twice.

**training-bias 84 → SWAP, then patch.** Take it for the clean frames, but it is the
weakest teaching of the five: at 2:50 it is 50s shorter than the incumbent and
compresses the four mechanisms into a rapid list. **It also says the researchers built
"a model to identify towels" at 1:01** — that is the cow study, the lesson's central
example. Fix that word before this ships; `excise_audio.py` or a re-roll of the line.
Also "inheriting hours" (ours) at 2:45.

**questions-matter 81 → REJECT.** Three separate regressions. Eight deck-referential
walks ("This graphic breaks down", "On the left, we see", "In the middle, we see", "And
on the right is", "This diagram shows", "This interface checklist breaks down", "as
highlighted in green at the bottom", "As this final text banner summarizes") against an
incumbent that had almost none. 4:45 against the incumbent's tight 3:24. And it puts the
lesson's **TRY IT activity on screen with its answer states showing** — the
NOT QUITE / CORRECT feedback panels at 2:57 (17s), 3:24 and 3:40 — which spoils the
activity for anyone who watches before doing it.

## Harvest from the reject

The incumbent is at 86 and the graft budget should be spent carefully. Two beats in the
challenger are genuinely additive; the rest is not worth an edit.

| span | type | what, and why it's worth taking |
|---|---|---|
| 2:29–2:38 | AUDIO | The scientific method as a third example of question-first thinking, sitting between Socrates and Einstein: *"It doesn't begin by assuming a conclusion. It begins by defining a specific measurable question worth testing."* The incumbent jumps Socrates → Einstein with nothing between. Lands in the incumbent's own 1:09–1:30 inquiry passage. |
| 4:17–4:35 | AUDIO | The honesty caveat the incumbent lacks entirely: a strong question does not guarantee truth, *"AI systems still hallucinate and make mistakes"* — what it buys you is an output that is focused and **easier to verify**. This is the lesson's register and it closes a real gap. |

Both are audio-only and land inside narration the incumbent already has, so they need a
word-level splice, not a scene graft. The library interior at 0:37–0:44 is handsome but
the incumbent's card-catalog sequence already covers that beat — not worth the seam.

Nothing else nominated: the four-qualities section is where the challenger is weakest,
and its board work is the reason it was rejected.

---

## Decisions (updated 2026-07-28)

- **which-app — SHIPPED.** Installed after two repairs: the ending freeze (it was
  ending on b-roll mid-sentence) and a Ken Burns graft of the lesson's own
  illustration over 2:42-2:54. Sheet row set to FINAL & DONE. Commit 6492f65.
- **training-bias — REJECTED** (David's call). The "towels" mis-say was patched to
  "cows" first, so the file in `Prompts/` is the corrected version and stays as a
  graft donor.
- **fake-trap — SHIPPED.** Two owner-directed edits first: deleted 0:06.6-0:14.2 ("We know the
  technology exists...still falling for these clips every day"), and froze the close board through
  the end, which was being replaced by unrelated images at 4:02. Runtime 4:15 -> 4:07. Sheet row
  FINAL, grade 89. **Transcription correction:** the "Ask the source" and "hits your feet" garbles
  flagged in the notes above were whisper errors, not defects - the audio says "Check the source"
  and "hits your feed". "Cloud" for clout at 1:54 still wants an ear check.
- flattery-trap — still standing as a swap recommendation, unshipped.
- questions-matter — rejected on the merits; two harvest spans nominated above.

### ⚠️ Open consequence of the training-bias reject

The challenger was watermark-clean; the incumbent is not. `videos/training-bias.mp4`
still has the NotebookLM corner mark burned into **112 of 146 sampled frames**
(detector max 0.995, present from frame 0). It is the only video in the catalogue of
37 still carrying it — the 7/27 removal pass covered 31 videos and missed this one.

The tracker is wrong about this. The sheet's Reason cell for `training-bias` ends
with *"No Getty or watermark found."*, written during the 7/27 re-grade. That claim
is false and will mislead the next grader.

Fix is the standard one already proven on 31 videos:
`scripts/video/watermark_remove.py --auto`. Not run — rejecting the challenger was a
decision about the challenger, and editing a live video is a separate call.
