# Big Upside: narration review of rolls 3 and 4 on the rewritten lesson (2026-09-24)

Scope: evaluation only. Authority: `index.html` BigUpsideSection as rewritten 2026-09-24 (visible prose
matches `lessons/big-upside.md`), `Prompts/big-upside-video-prompt.txt` (495 words), and the five current
boards. Bundles in this folder; medium.en re-transcribes of the spans quoted below.

| File | Runtime | Health board | Everyday board | Verdict |
|---|---|---|---|---|
| `Prompts/big-upside-3.mp4` | 3:38.8 | 2:00-2:30 (30 s) | 2:30-2:58 (28 s) | REPAIR (base if built) |
| `Prompts/big-upside-4.mp4` | 3:17.4 | 1:47-2:15 (28 s) | 2:15-2:38 (23 s) | REROLL |

For comparison, v3 gave the old two boards about 22 s and 18 s. Both new rolls give each card one sentence.
The prompt's "for each, explain the problem, AI's contribution, and the benefit" did not land in either.
v3 cannot be the base any more: the protein board, timeline narration and both example boards changed.

---

CANDIDATE: Prompts/big-upside-3.mp4 (3:39)
VERDICT: REPAIR
TEACHING POINTS:
  Giant calculator, fifty-year challenge — TAUGHT — 0:00-0:15 ("recently helped", "stumped them for 50 years")
  Proteins as tiny machines, oxygen, infections; finding shapes was slow and difficult — RICH — 0:15-0:31
  A New Scale for Science: shape line, 200,000 vs over 200 million shared free — RICH — 0:31-0:53
  Starting point for disease and medicines — RICH — 0:53-1:05 (adds "instead of spending years finding a single shape")
  "Who helped make that happen?" bridge — RICH — 1:05
  Timeline as a story — TAUGHT — 1:08-1:24. Chess and games, the brain, DeepMind, AlphaFold, free predictions, Nobel in Chemistry. The ages (13, 17) and Theme Park are dropped.
  Kid-who-loved-games line — RICH — 1:27
  Three million people, over 190 countries — RICH — 1:31
  Shared 2024 Nobel Prize in Chemistry — WRONG — 1:39 "That global reach is why in 2024, Hassabis stood on stage to share the Nobel Prize in Chemistry." The prize was not awarded for user numbers. "For protein structure prediction" is dropped.
  The quotation, attributed — RICH — 1:46-1:57
  Patterns in scans and fields; AI accelerating work that protects lives — THIN — 1:57 "We can see that potential in how AI helps people stay healthy." The farm-fields sentence and the pre-board "AI is already accelerating..." line are dropped.
  Finding Cancer — THIN — 2:01-2:10. "Extra set of eyes" is a good frame. "Over 100,000 women" is dropped; "found more signs of breast cancer" is weaker than "found more cancers than those without it". Both models hear "medical stands" for "scans".
  Urgent Scans — THIN — 2:10 "It also speeds up triage by flagging possible brain bleeds immediately." "Immediately" is added and "triage" is jargon; the doctor reviewing and deciding is dropped (2:21 "the technology isn't replacing human experts" partly covers it).
  New Antibiotics — THIN — 2:15 "a new antibiotic that killed drug-resistant bacteria". Abaucin is not named and the resistance problem is dropped. "In the lab" is kept, which keeps the lab-test limit.
  Health banner — RICH — 2:25
  Reading Aloud — TAUGHT — 2:33
  Flood Warnings — THIN — 2:39 "AI analyzes weather data to provide free flood warnings days in advance." Time to prepare and move to safety is dropped, and so are places without river gauges. "Analyzes weather data" is not in the lesson.
  Targeted Spraying — TAUGHT — 2:45 ("harsh chemicals"; spraying only where weeds are is dropped)
  Everyday banner — RICH — 2:55
  "Every one of those is true." — MISSING
  Question, ready answer — RICH — 2:58-3:09
  One more thing about Demis — RICH — 3:09-3:26
  Nobel line, closing two lines — RICH — 3:26-3:35
HARD REQUIREMENTS: 11 of 11 met. One note: "A protein's shape helps determine what it does." is heard as "a protein shape" by both models (0:32), behind "And as this graphic shows,".
ERRORS: 1:39 the Nobel Prize is attributed to AlphaFold's reach.
ADDITIONS: "Notice that the technology isn't replacing human experts." (2:21): accurate, and it does the prompt's no-automatic-decisions job. Keep.
SCREEN REFERENCES: "as this graphic shows" (0:31, mid-sentence), "Looking at the left side, we can see the historical baseline." (0:36), "This timeline tracks..." (1:08), "The bottom of the board sums it up perfectly." (1:24), "The common thread here is at the bottom." (2:53). The three whole sentences cut cleanly.
PICTURES: Nobel ceremony photograph with a person, 1:40-1:58, needs cover. Notebook renders every board; all replaced.
LISTENING: base.en throughout; medium.en on 0:30-0:40, 1:08-1:12, 1:38-1:50, 1:59-2:15, 2:52-2:59, 3:09-3:14. The name is heard correctly at 1:08 and 3:09. "Medical stands" needs David's ear.

---

CANDIDATE: Prompts/big-upside-4.mp4 (3:17)
VERDICT: REROLL
TEACHING POINTS (differences from roll 3):
  Hook — THIN — 0:00-0:31. "Solving a puzzle of that magnitude required a completely new scale of calculation. That demand led directly to an AI breakthrough, known as AlphaFold." Invented causation, and "breakthrough" twice (0:26, 0:31), a banned word.
  Predictions are not experimental confirmations — 0:49, from the prompt's guardrail, not the lesson; accurate.
  Timeline — RICH — 1:09-1:26 (13 and 17 kept; Theme Park dropped)
  Three million people, over 190 countries — MISSING
  Shared Nobel — THIN — 1:22 "That work earned him the 2024 Nobel Prize." "Shared" and Chemistry are dropped.
  1:39-1:47 "The true impact ... solving real-world problems for billions of people." — padding
  Finding Cancer — THIN — 1:50 (100,000 women dropped)
  Urgent Scans — TAUGHT — 1:53 "so doctors can review them faster"
  New Antibiotics — WRONG — 1:58 "identify abaucin, a compound that kills drug-resistant bacteria". "In lab tests" and "a type of" are dropped, so it reads as a working treatment, which the prompt forbids.
  Everyday cards — THIN — 2:18-2:34, one clause each. Both models hear "target spring" for "targeted spraying".
  Everyday banner — MET WITH NOTE — 2:34, run straight into "so the next time someone asks".
  "Every one of those is true." — MISSING
HARD REQUIREMENTS: 11 of 11 spoken; banner 7 run on.
REPAIR PLAN: none worth it. It misses the reach numbers, overstates abaucin, and its examples are shorter than roll 3's.
PICTURES: not surveyed in detail. A doctor drawing appears at 2:08.

---

BEST-OF PLAN (if building now): base roll 3
  Nobel causation — roll 3 WRONG @1:39 | roll 4 THIN @1:22 — CUT roll 3 1:39.3-1:57.1 ("That global reach is why ... billions of people.") and GRAFT roll 4 1:29.6-1:39.4 ("When he won the award, Hassabis explained his motivation clearly. I've dedicated my career ... billions of people."). The canonical timeline shows "2024 Nobel Prize, In Chemistry" on screen. "Shared" is not spoken.
  Screen pointers — CUT roll 3 0:36.3-0:39.8, 1:24.3-1:26.9, 2:53.4-2:55.5 (whole sentences).
  The examples — no donor. Roll 4's version of every card is the same length or shorter.
RESIDUAL IF BUILT: the six cards still get one sentence each; 100,000 women, abaucin by name, the doctor deciding, prepare and move to safety, and places without river gauges are unspoken; "Every one of those is true." missing.

## Why the examples came out thin, and the fix

The six card texts sit in the Markdown as paragraphs, and the prompt asks for them only in the beat spine.
Both rolls did what Notebook does with a beat-spine request: one summary clause per card. What has worked in
every lesson since Document Trap is making the sentences verbatim requirements and splitting each onto its
own line in the Markdown.

Proposed materials change (same words, no new facts):
1. `lessons/big-upside.md`: put each card sentence on its own line under Boards 3 and 4 (the page text is unchanged).
2. Prompt: add these to REQUIRED VERBATIM AUDIO:
   - "In a Swedish trial with over 100,000 women, doctors using AI found more cancers than those without it."
   - "AI can flag a scan that shows a possible bleed so doctors can review it sooner."
   - "The doctor evaluates the scan and decides what care is needed."
   - "Researchers used AI to identify abaucin, which killed a type of drug-resistant bacteria in lab tests."
   - "AI tools on a phone can read the text aloud and describe photos, helping with everyday tasks."
   - "AI helps provide free warnings days ahead, including places without equipment that measures river levels."
   - "AI-guided equipment uses cameras to tell weeds from crops and sprays where weeds are found."
   To stay under 500 words, trim the protein paragraph (the "Do not reintroduce ..." list can shrink to one line
   now that the Markdown no longer carries that material) and the timeline paragraph's explanation.
3. Also add "Every one of those is true." to the verbatim list; both rolls dropped it.
