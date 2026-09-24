# Big Upside: narration review of rolls 5 and 6 (2026-09-24, third materials revision)

Materials: `lessons/big-upside.md` with the six card sentences on their own lines, and the 475-word prompt
with 19 verbatim lines (see `video-audit/big-upside-review-2026-09-24b/REVIEW.md`). Bundles in this folder;
medium.en word timings for roll 6.

| File | Runtime | Verbatim lines | Example boards | Verdict |
|---|---|---|---|---|
| `Prompts/big-upside-5.mp4` | 2:49 | about 10 of 19 | 1:24-2:05, one clause per card | REROLL |
| `Prompts/big-upside-6.mp4` | 5:19 | 19 of 19 (several with notes) | 2:18-4:07, 1:49 total | **REPAIR, the base** |

The materials change worked in roll 6: every card now gets its name, the problem, the required sentence and,
for urgent scans, the doctor-decides line. Roll 5 ignored it.

---

CANDIDATE: Prompts/big-upside-5.mp4 (2:49)
VERDICT: REROLL
Missed verbatim lines: the Swedish-trial line (100,000 women dropped), the scan line, the doctor-decides line,
the abaucin line, and all three everyday-card lines (paraphrased to one clause each). The quotation is
spoken, prefixed "Hassabis stated".
ERRORS: 1:35 "identify abaucin, killing drug-resistant bacteria" drops "in lab tests", which the prompt
forbids. 0:47 "breakthrough" (banned) and 2:18 "breakthroughs". "Over 190 countries" is dropped. "Theme park"
at 17, but "designed", not "helped design".
Nothing in roll 5 beats roll 6.

---

CANDIDATE: Prompts/big-upside-6.mp4 (5:19)
VERDICT: REPAIR
TEACHING POINTS:
  Giant calculator; "But that calculator can do some amazing things."; fifty-year challenge — RICH — 0:00-0:16
  Proteins, their jobs, shape matters, shapes were hard to find — RICH — 0:16-0:30
  A New Scale for Science: 200,000 vs over 200 million shared free — RICH — 0:30-0:54
  Starting point for disease and medicines — RICH — 0:54-1:04
  Bridge, co-founder of DeepMind, chess and video games — RICH — 1:04-1:18 ("breakthrough" at 1:11; see cuts)
  Timeline as a story with the ages 13 and 17 and Theme Park — RICH — 1:20-1:36
  Kid-who-loved-games line — RICH — 1:36
  Three million people, over 190 countries — RICH — 1:40
  Shared 2024 Nobel Prize in Chemistry — RICH — 1:45
  The quotation, attributed — RICH — 1:50-1:59
  "For protein structure prediction" — TAUGHT, but inside a padding passage (1:59-2:18) proposed for cutting
  "AI finds patterns in everything from medical scans to farm fields ... AI is already accelerating work..." — MISSING
  Health board, all three cards: name, problem, verbatim line; "the process relies on human medical judgment at the end" — RICH — 2:18-3:07
  Health banner — MET, behind "As the banner at the bottom summarizes," — 3:07
  Everyday board, all three cards: name, problem, verbatim line — RICH — 3:18-3:59
  Everyday banner — MET, behind "As the board states," — 4:02
  "Every one of those is true." — MET WITH NOTE — 4:36, behind "Whatever examples you thought of from our list,"
  Question and ready answer — TAUGHT — 4:38 "the next time someone asks you that question, you have a definitive answer ready." The question itself was asked only inside the pause-the-video passage.
  One more thing about Demis, Nobel line, closing lines — RICH — 4:47-5:16
HARD REQUIREMENTS: 19 of 19 spoken. With notes: "A protein's shape helps determine what it does, but..." (0:23, run on);
  both banners and "Every one of those is true." carry spoken prefixes.
ERRORS:
  4:07-4:36 "Let's take a moment here. I want you to pause the video right now. If someone walked up and asked
  you, what good does AI do for society, how would you respond? Think of your answer before hitting play.
  You likely realize that these everyday tools are not infallible guarantees. Instead, they act as highly
  practical enhancements. They build a direct bridge between complex math and immediate human needs." This
  breaks the prompt's "never ask viewers to answer" and adds claims the lesson doesn't make.
ADDITIONS WORTH KEEPING: "Importantly, the process relies on human medical judgment at the end." (2:44);
  "These aren't abstract concepts for tomorrow." (3:59).
SCREEN REFERENCES (the ban did not hold): "We can see its impact on this board ... The contrast shows exactly
  what happened." (0:34-0:41); "Now look at the right side." (0:47); "This timeline charts his career." (1:18);
  "This board outlines how AI is helping people stay healthy." (2:18); "Starting on the left with finding
  cancer." (2:22); "Next is the urgent scans column." (2:34); "As the banner at the bottom summarizes," (3:07);
  "This board shows examples of helping people in everyday life." (3:18); "Look at the reading aloud
  section." (3:22); "In the middle column, we have flood warnings." (3:35); "On the far right is targeted
  spraying." (3:47); "As the board states," (4:02).
LISTENING: base.en throughout; medium.en word timings. Both models hear "Hassabis" correctly at 1:20 and 4:49
  and "Hasavas" at 1:07 and 1:45. "Abaucin" is heard as "abosin" / "a balsen" (3:00). Needs David's ear.

---

REPAIR PLAN: base roll 6
Cuts (whole sentences between measured pauses; frames set on the waveform at build):
  1. 0:34.2-0:41.5 "We can see its impact on this board, laying out a completely new scale for science. The contrast shows exactly what happened." (pauses 0.86 / 0.68 s)
  2. 0:47.4-0:48.6 "Now look at the right side." (pause before 0.74 s; the gap after it is short, so check on the waveform)
  3. 1:59.3-2:18.5 "Earning a Nobel Prize, specifically for protein structure prediction, demonstrates a clear lesson. It requires human curiosity ... tangible societal benefits. We see that same dynamic across other medical fields." (pauses 0.42 / 0.90 s). Loses the spoken "for protein structure prediction".
  4. 4:06.6-4:35.8 the pause-the-video passage through "Whatever examples you thought of from our list," (pauses 1.00 / 0.56 s), so "the upside is already reaching people." runs into "every one of those is true."
  5. 4:37.6-4:41.9 "So the next time someone asks you that question, you have a definitive answer ready." replaced by a GRAFT from roll 3 2:58.0-3:04.7: "So the next time someone asks you, what good does AI do for society? You have an answer ready." (roll 3's level to be matched on the waveform)
  Optional, David's call: 1:11-1:18 "His path to a scientific breakthrough actually started with two things you might recognize, chess and video games." (banned word; the timeline right after covers chess and games).
Screen pointers that name a card or board title ("Next is the urgent scans column.", "In the middle column, we have
  flood warnings.", and the rest): proposed KEEP, because each carries the card's name and the edit rings that
  card as it is spoken. Cutting them would leave the cards unnamed. "As the banner at the bottom summarizes," and
  "As the board states," have no clean pause before them and stay.
RESIDUAL IF BUILT: about 1:50 of example-board narration with card-by-card pointers; "AI finds patterns in everything
  from medical scans to farm fields" unspoken; "for protein structure prediction" unspoken; "every one of those is
  true" starts lowercase mid-phrase (listen); runtime about 4:25.
