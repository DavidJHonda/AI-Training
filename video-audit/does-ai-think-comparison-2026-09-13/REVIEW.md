# Does AI Think?: roll comparison (2026-09-13, NARRATION-REVIEW)

Rolls: Prompts/does-ai-think-1.mp4 (2:45) and does-ai-think-2.mp4 (3:58). Live page (doesaithink) exported and compared against
lessons/does-ai-think.md: page prose matches; the Markdown adds the boards' text as prose. Both rolls end on "It is a pattern
machine, not a thinker… weird moments make sense": Notebook narrating the STALE close-board copy that was in the kit until this
morning (regenerated 2026-09-13). That tail is not lesson content and is cut in any build.

```text
LESSON: does-ai-think
CANDIDATE: Prompts/does-ai-think-1.mp4 (2:45)
VERDICT: REROLL
TEACHING POINTS:
  Hook: types back like a person; explains, jokes, says sorry; someone in there; the big question — TAUGHT — 0:00–0:26
  Sounding human doesn't tell you whether it understands — TAUGHT — 0:26–0:46
  The Chinese Room: note "How are you?", rulebook, reply "I'm fine, thank you", looks fluent, doesn't know Chinese — TAUGHT — 0:46–1:06 (compressed; the three steps not walked; "locked in a room" dropped)
  A convincing answer doesn't prove understanding — TAUGHT — 1:06–1:13 (paraphrase)
  An LLM doesn't follow a literal rulebook; patterns learned during training — TAUGHT — 1:13–1:30
  Board 2, five comparisons both sides — THIN — 1:30–1:53: meaning and experience merged into one line; beauty "You feel art. AI recalls descriptions"; uncertainty "you understand uncertainty, while AI confidently hallucinates facts"
  Similar-looking answers, very different processes — TAUGHT — 1:53–2:06 (paraphrase)
  None of this means AI is dumb or useless; a human-sounding answer is not enough — TAUGHT — 2:06–2:24
HARD REQUIREMENTS:
  Three Chinese Room steps and "To anyone outside, it looks like fluent Chinese conversation" — MISSED (compressed; the line paraphrased)
  All five comparisons, both sides each — MISSED
  "Sounds human. Works differently." / "A convincing answer doesn't prove understanding." — MET — 2:36–2:42, verbatim, nothing after
ERRORS: none
SOURCE_QA: PASS
ADDITIONS: 2:24–2:36 the stale close board narrated ("As this graphic states, it is a pattern machine, not a thinker…"); cut
EDITING NOTES: not built on its own; its verbatim closing lines (2:36.0–2:41.5, silences 155.74–156.11 and 161.35–164.72) are the donor for roll 2's close
LISTENING: not listened
```

```text
LESSON: does-ai-think
CANDIDATE: Prompts/does-ai-think-2.mp4 (3:58)
VERDICT: REPAIR (with roll 1's closing lines grafted)
TEACHING POINTS:
  Hook; the big question — TAUGHT — 0:00–0:26
  Sounding human doesn't tell you whether it understands — TAUGHT — 0:26–0:37
  The Chinese Room: locked in a room, no Chinese, a giant rulebook; steps 1, 2, 3; "To anyone outside, this looks like a completely fluent conversation in Chinese"; still understands zero Chinese — TAUGHT — 0:54–1:42, full
  An LLM doesn't use a literal rulebook; patterns learned during training — TAUGHT — 1:42–1:56
  Producing an answer and understanding it aren't the same — TAUGHT — 1:56–2:08
  Board 2, five comparisons both sides: meaning, experience, word choice, beauty, uncertainty — TAUGHT — 2:08–3:10, all five (editorial: "static scraped data", "regurgitating", "lacks that internal monitor")
  Outputs look the same, the process is different — TAUGHT — 3:10–3:19 (stronger than the page: "shares nothing in common with human cognition")
  None of this means AI is dumb or useless; a human-sounding answer is not proof — TAUGHT — 3:19–3:38
HARD REQUIREMENTS:
  Three steps and the "To anyone outside" line — MET — 1:05–1:33
  Five comparisons both sides — MET — 2:15–3:10
  "Sounds human. Works differently." / "A convincing answer doesn't prove understanding." — MISSED — 3:38–3:45 "It sounds human, but it works entirely differently. A convincing answer never proves true understanding." then the stale close board narrated
ERRORS: none
SOURCE_QA: PASS
ADDITIONS: 0:44–0:54 "The goal here is to uncouple two ideas…" (inflated, cut); 3:29–3:34 "resist our natural instinct to anthropomorphize it" (jargon, cut); 3:45–3:55 stale close board (cut)
EDITING NOTES: build from roll 2; end its narration at 3:38.3 and graft roll 1's verbatim closing lines (audio only, same voice, 0.6 dB apart) under our close board; cuts at 0:44.3–0:54.1 and 3:29.1–3:33.5; Board 1 (Chinese Room) rendered by Notebook 0:56–1:44 with its callouts (replace with ours, compact, three step rings); Board 2 (faces; not uploaded) inserted over 2:08–3:19 in place of Notebook's own "Human cognition vs AI pattern processing" matrix, dense by legibility (five rows), dive per row; Notebook drawings elsewhere are good (typing hands, silhouette head, eye, poem cards, server and phone, empty room 0:40–0:48, symbols and prediction, OUTPUT / COMPREHENSION, data center, gears, bubble-x-bulb); no photographs; corner mark present; pauses at idea boundaries only: hook -> sounding human (0:26), into the Chinese Room (0:37 or 0:54 after the cut), into what an LLM does (1:42), into the comparison (2:08), into none of this means (3:19), before the close; longest board run ~70s (the comparison board) — interleave with Notebook's own per-row drawings? none exist (its matrix is one graphic), so leave it
LISTENING: not listened; no doubtful words
```

Decision: build from roll 2 with roll 1's closing lines grafted. A reroll is the alternative now that the close copy is fixed, but
roll 2's teaching is complete and the graft is a two-line, same-voice swap.

## Best-of plan (added 2026-09-14 under the beat-by-beat rule; retrospective check of the shipped v3)

```text
BEST-OF PLAN: does-ai-think
BASE: Prompts/does-ai-think-2.mp4 (shipped 2026-09-13 as v3: both boards walked in the lesson's words; close lines grafted from roll 1)
  Hook: types back like a person; explains, jokes, says sorry; someone in there; the big question — roll 1 TAUGHT @0:00–0:26 | roll 2 RICH @0:00–0:26 "it explains complex topics, it cracks jokes, and it even says sorry… hard not to feel like someone is actually in there… does it actually think, is it understanding the world the way you do?" — TAKE roll 2
  Sounding human doesn't tell you whether it understands — roll 1 TAUGHT @0:26–0:46 "sounding human is not the same thing as understanding like a human. Producing language that mimics a person does not prove the machine comprehends those words the way you do" | roll 2 TAUGHT @0:26–0:37 "sounding human is a separate skill. It doesn't actually tell us if the machine comprehends the words it's generating" — tie (roll 1 slightly closer to the page's wording; not a quality gap)
  Chinese Room setup and the three steps — roll 1 THIN @0:46–1:06 (one clause per step; "match the symbols to a rule book") | roll 2 RICH @0:54–1:33 (locked in a room, no Chinese, massive rulebook; Step 1 "How are you?", Step 2 "look up the whole phrase on their giant wall chart", Step 3 "I'm fine, thank you… slide it back under the door… looks like a completely fluent conversation") — TAKE roll 2 (under The Chinese Room)
  A convincing answer doesn't prove understanding (board takeaway) — roll 1 TAUGHT @1:06 "Delivering a convincing, accurate answer is entirely different from actually understanding what you just said" | roll 2 TAUGHT @1:33–1:42 "produced a perfect response, yet they still understand absolutely zero Chinese" — tie
  Producing vs understanding; no literal rulebook; patterns from training; fluent alone doesn't tell — roll 1 TAUGHT @1:13–1:30 "…patterns learned during its training to mathematically predict its response. It gives you fluent text, but that text alone is not proof of comprehension" | roll 2 TAUGHT @1:42–2:08 "doesn't use a literal physical rulebook… billions of complex patterns it learned during training… Mechanically generating a correct sequence of words is an entirely different process from actually understanding what those words mean" — tie
  Board 2: five comparisons, both sides each — roll 1 THIN @1:30–1:53 (meaning and experience merged; one clause per row; "AI confidently hallucinates facts") | roll 2 RICH @2:08–3:10 (all five rows, both sides, in order) — TAKE roll 2 (under When You Think / What AI Does)
  Similar-looking answers, very different processes (banner) — roll 1 TAUGHT @1:53–2:06 "the internal processes creating that text, human comprehension versus mathematical pattern matching, are completely disconnected" | roll 2 TAUGHT @3:10–3:18 "the underlying process generating those words shares nothing in common with human cognition" — tie (roll 1 names both processes, roll 2 overclaims "nothing in common"; wording, not a quality gap; David may prefer roll 1's line, it sits under the board's banner and would graft safely)
  Not dumb or useless; a human-sounding answer isn't enough — roll 1 TAUGHT @2:06–2:24 "generating an answer that sounds remarkably human is simply not enough evidence to prove it understands the world the way you do" | roll 2 TAUGHT @3:19–3:38 (shipped with the anthropomorphize sentence cut) "A human-sounding answer is simply not proof of human-like comprehension" — tie (roll 1 closer to the page; under Notebook's drawing in the shipped edit, so a graft would be the risky kind)
  Close lines — roll 1 verbatim @2:36–2:42 (already grafted) | roll 2 paraphrase — TAKE roll 1 (done)
GRAFTS: none beyond the shipped close; no RICH-vs-THIN gap favours roll 1. Optional wording swap only: the banner sentence (roll 1 1:53–2:06) under the comparison board.
```
