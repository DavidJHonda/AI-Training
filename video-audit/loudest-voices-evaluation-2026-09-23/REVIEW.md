# Loudest Voices — live video evaluation against the current system (2026-09-23)

David: "evaluate the live versions of Loudest Voices and Pace of Change videos. I need to know if they
need a reroll to our current system." Scope: evaluation only. Nothing built, nothing shipped, no
materials changed. Bundle (transcript, scenes, holds, contact sheets) in `loudest-voices/`.

Live file: `course-assets/loudest-voices/loudest-voices.mp4` — v5, shipped 2026-09-18, 3:54.90,
sha256 d77eae1e…, cache key 20260918ship1, pill 4 min. Built as a best-of of rolls 1 and 2 (Amodei
beat from roll 2). **Both raw rolls are gone from `Prompts/`**, so the live audio is the only source:
no REPAIR path exists for anything below.

Materials state: `lessons/loudest-voices.md` is already in the 2026-09-20 structure (Board / Image
file / Teaching content, Closing Message). `Prompts/loudest-voices-video-prompt.txt` (382 words) is the
interim 9/18 form: NARRATION FIRST paragraph, no REQUIRED VERBATIM AUDIO list, no beat spine, no
banned-word list. Not in `Prompts/upload-sets.json`. No board carries a face, so no faceless variant
is needed.

```text
LESSON: loudest-voices
CANDIDATE: course-assets/loudest-voices/loudest-voices.mp4 (3:54.90, live v5)
VERDICT: REROLL
TEACHING POINTS:
  Hook: opinions everywhere, who do you believe — TAUGHT — 0:00–0:15 ("almost as many opinions about AI as there are calculations in a neural network"; page says LLM; the two-quadrillion joke not spoken, harmless)
  Ask the people who make AI; same field, same evidence, very different bets — TAUGHT — 0:19–0:35 (paraphrased, not the page's three-beat line)
  Amodei, Optimist: background — TAUGHT — 0:35 "built GPT-2 and GPT-3 at OpenAI and then founded Anthropic"
  Amodei SAYS quote — TAUGHT (paraphrase, indirect) — 0:43 "compress a century of human progress into a single decade" (board: 50-100 years into 5-10 years)
  Amodei BUT ADMITS quote — TAUGHT (paraphrase) — 0:49–1:02; drops "technological"
  Hinton, Worrier: background — TAUGHT — 1:02–1:15
  Hinton SAYS quote — THIN — 1:15 "we are actually making new kinds of beings. We give them goals, and they derive other goals we do not necessarily know." (compressed to the point of awkwardness; the quote's "we don't necessarily know what other goals they'll derive" is the teaching)
  Hinton BUT ADMITS (cancer) — TAUGHT — 1:23
  LeCun, Doubter: background — TAUGHT — 1:31
  LeCun SAYS (dead end; house cat) — TAUGHT — 1:41
  LeCun BUT ADMITS (we build it, agency, control the risks) — TAUGHT (paraphrase) — 1:49
  Synthesis: Optimist sees danger / Worrier sees benefits / Doubter acknowledges risks — RICH — 1:58
  "That's the tell: the people who know AI best still don't know where it's going" — TAUGHT — 2:04 "cannot say for certain where it is going"
  Every big technology arrives with confident predictions; miss in both directions — TAUGHT — 2:11
  Stoll 1995 online shopping — TAUGHT — 2:20
  Ballmer 2007 iPhone — TAUGHT — 2:34 (+ outside addition: keyboards / multi-touch / handheld computers)
  Metcalfe 1996 collapse — TAUGHT — 2:50
  Ford 1940 flying cars — TAUGHT — 3:04 (but see ERRORS: "as the bottom right panel notes")
  Banner: "The future is hard to predict because people change the result." — THIN — 3:19 spoken as "they overlooked the fact that people ultimately determined the result"; the banner sentence is never spoken
  Why wrong: habits line — TAUGHT (not verbatim) — 3:31 "A technology only truly becomes the future when people change their daily habits around it. Machines improve at an exponential pace. Human habits change at human speed."
HARD REQUIREMENTS:
  "None of them has a simple, one-sided view." — MISSED — not spoken anywhere (the 9/18 prompt required it)
  "Where AI will be in ten years is a bet." — MET — 3:46 (spoken once, at the close; the page also says it after the synthesis)
  "Which voice you listen to is your call." — MET — 3:50
  "A technology becomes the future only when people change their habits around it. Machines improve fast. Habits change at human speed." — MISSED as verbatim — paraphrased ("daily habits", "exponential pace")
ERRORS:
  3:14 — "as the bottom right panel notes" — narrates board furniture; banned under the current VOICE rules and it is mid-sentence, so it cannot be cut cleanly.
  3:37 — "Machines improve at an exponential pace" — Notebook's characterization, not the lesson's ("Machines improve fast").
  3:42 — "Because of that human variable, the final result isn't written yet." — added line, not on the page (harmless).
SOURCE_QA: PASS
ADDITIONS: the iPhone keyboard/multi-touch detail (2:40) and "survived its early growing pains" (2:56) are accurate but outside the lesson; none worth adding to the page.
REPAIR PLAN: none available — rolls 1 and 2 were deleted after the 9/18 ship; the live file has no donor for the missed line or the paraphrased banner.
EDITING NOTES (why the pictures also fail the current spec):
  Board holds (Edit Spec 8b, widened 2026-09-23 to ~20 s per board): Even the Experts Don't Know runs about 0:26–1:12 (46 s) and 1:15–2:11 (56 s) with one 3 s Notebook drawing between; This Has Happened Before runs about 2:11–3:30 (79 s) unbroken. Three of the four longest runs in the video are over twice the new limit.
  Invented on-screen figures (two Notebook spans): 0:12–0:19 "Neural Network Calculations, Operations: 10^15 FLOPs"; 3:32–3:44 "TECH OUTPACES HUMAN HABITS" chart with a "Pace of Change (Index)" axis and a "46x" label. Both are Notebook statistics the lesson never states.
  Drawn people in Notebook scenes: 0:00–0:08 three commuters on phones; 0:20–0:26 three people at a conference table (stand-ins for the experts). The current prompt rule is drawn scenes with no people.
  No donor drawings exist in this roll to break the board holds under 8b (the only Notebook spans are the two invented charts, the two people scenes, the opinion cards at 0:08, and the 1:12 city silhouette).
  Compliant today: canonical boards, full-view opens, dense dives per SAYS/BUT ADMITS card, corner mark cleaned, all source photographs covered, canonical close as the literal final frame. Rings are constant 5 px under the pre-9/21 rule (grandfathered, not a reroll reason).
LISTENING: transcript only (faster-whisper base.en). Not auditioned by ear: the pronunciations the ASR renders as "Amote", "found it anthropic" and "Jan Lechin" (flagged as unheard in the 9/18 review too), and the two roll-1/roll-2 joins at 0:35 and 1:02.
```

## Answer

**REROLL.** The narration teaches every essential point, but under the current system it misses a
required line ("None of them has a simple, one-sided view"), never speaks the board's banner, paraphrases
the habits takeaway, and narrates board furniture mid-sentence. With both rolls gone, none of that is
repairable. The pictures fail the 2026-09-23 hold rule three times over and carry two invented charts,
and the roll has no drawings to break the holds with. A reroll on the new recipe fixes both at once.

Before rolling: restructure the prompt to the four blocks (verbatim list: the three-beat "Same field.
Same evidence. Very different bets.", "None of them has a simple, one-sided view.", "Where AI will be in
ten years is a bet.", the banner, the three habits sentences, the two closing lines), add the beat
spine and a banned-word list (exponential, neural network, stakeholders, leverage, framework), register
the lesson in `upload-sets.json`, and run the sync. The Markdown needs no change. A new roll is compared
beat by beat against this live file; the live's canonical-board legs remain reusable if the new roll's
narration wins and its drawings are used under the boards.
