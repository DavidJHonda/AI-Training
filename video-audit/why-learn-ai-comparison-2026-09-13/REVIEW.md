# Why Learn AI?: roll comparison (2026-09-13, NARRATION-REVIEW)

Rolls: Prompts/Why_Learn_AI_.mp4 (3:24, reviewed as why-learn-ai-1) and Prompts/Why_Learn_AI__The_Historical_Shift.mp4 (3:40,
reviewed as why-learn-ai-2). Live page (whydeeper) exported and compared against lessons/why-learn-ai.md: page prose matches;
the Markdown adds the boards' text as prose. No materials bug.

```text
LESSON: why-learn-ai
CANDIDATE: Prompts/Why_Learn_AI_.mp4 (3:24)
VERDICT: REROLL
TEACHING POINTS:
  Scribe in the 1450s; the machine in Mainz; two choices — TAUGHT — 0:00–0:21 ("Ignore the change or learn to run it"; "Mainz" heard as "minds", needs an ear)
  "Run it, or someone else will." — THIN — 0:23 "You can master the tool or step aside for someone who will"
  AI is everywhere: apps, search results, first-job tools; sci-fi to normal — TAUGHT — 0:27–0:40
  Five places AI already lives, each with where you've seen it — TAUGHT — 0:44–1:34
  You can start now — TAUGHT — 1:34–1:42
  Desktop publishing example; the tool didn't replace skill — TAUGHT — 1:42–2:02
  Three reasons you'll thrive with instructions — TAUGHT — 2:06–2:45 (inflated: "AI acts as an initiator for your ideas", "independent judgment you'll need as a professional")
  Steam engine, electricity, internet; AI across almost everything — TAUGHT — 2:45–3:04
  White House document named and quoted exactly — MISSING — 3:04–3:17: document not named ("White House National Strategy document"); quote stops after "all at once", "This is the potential that AI presents" not spoken
HARD REQUIREMENTS:
  "Run it, or someone else will." — MISSED (paraphrase)
  White House quote exactly — MISSED (second sentence missing)
  "AI is today's printing press." / "Learn to run it." — MET — 3:17–3:21, nothing after
ERRORS: none
SOURCE_QA: PASS
ADDITIONS: none worth keeping
EDITING NOTES: not built
LISTENING: not listened
```

```text
LESSON: why-learn-ai
CANDIDATE: Prompts/Why_Learn_AI__The_Historical_Shift.mp4 (3:40)
VERDICT: REPAIR
TEACHING POINTS:
  Scribe in the 1450s; the machine; two choices — TAUGHT — 0:00–0:19, verbatim ("Pretend it isn't happening, or learn to run it"; "in Mainz" dropped)
  "Run it, or someone else will." — TAUGHT — 0:20–0:24 "Run the machine, or someone else will take your place" (small.en confirmed; paraphrase, meaning intact)
  AI is everywhere; sci-fi to normal; tools your first job hands you — TAUGHT — 0:24–0:37 ("apps on your phone, the search results you read" compressed to "isn't a futuristic destination you go visit")
  Five places AI already lives with where you've seen it — TAUGHT — 0:40–1:04 (Netflix, Waze, Hey Google, photo tagging dropped from the examples; every category named with an example)
  AI was part of your day before chatbots — TAUGHT — 1:04–1:11
  You can start now — TAUGHT — 1:11–1:18
  Desktop publishing; posters, magazines, brochures; the tool didn't replace skill — TAUGHT — 1:18–1:47, full
  Three reasons you'll thrive with instructions — TAUGHT — 1:55–2:24, all three
  Start now, build skills you'll carry — TAUGHT — 2:24–2:31 (paraphrase of the banner)
  Steam engine, electricity, internet; AI across almost everything — TAUGHT — 2:31–2:59 (inflated: "rewrote how humanity accesses and shares information", "scale across almost everything simultaneously")
  White House document named and quoted exactly — TAUGHT — 2:59–3:23, "Winning the Race, America's AI Action Plan"; both sentences verbatim
HARD REQUIREMENTS:
  Two choices — MET — 0:15–0:19
  "Run it, or someone else will." — MET as a close paraphrase — 0:20
  Five places with examples — MET — 0:40–1:04
  Three reasons with instructions — MET — 1:55–2:24
  White House quote exactly — MET — 3:13–3:23
  "AI is today's printing press." / "Learn to run it." — MET — 3:31–3:37, nothing after
ERRORS: none
SOURCE_QA: PASS
ADDITIONS: 1:46–1:52 "You are perfectly positioned to take advantage of this shift by building foundational habits today" (harmless bridge into the thrive board; keep or cut); 3:23–3:32 "We are looking at a massive economic and cultural shift unfolding in real time. This brings us to one simple truth." (cut)
EDITING NOTES: cut 3:23.1–3:31.8; Board 1 (press, faces; not uploaded) inserted over Notebook's scribe/press drawings 0:00–0:24 at the scribe hook, or from "Run the machine…" only (owner taste; the drawn Gutenberg press at 0:20 is a good Notebook scene); Where AI Already Lives shown by Notebook 0:40–1:11 zoomed with its highlights (replace: five cards, compact, ring per card as spoken); Why You'll Thrive shown 1:56–2:31 with highlights (replace: three cards, compact); STOCK PHOTOGRAPHS at 1:32 (vintage computer desk), 2:40–2:47 (factory engine), 2:48–2:51 (old computer), 3:00–3:12 (the White House): objects and a building, no people, but check each first frame for a watermark before shipping; Notebook's drawings elsewhere (drafting tools 1:20, magazines 1:36, anvil-to-data-center 2:32, skyline 3:24) are good hand-off footage; corner mark present; standard close from the engine card's arrival (~3:31); pauses at idea boundaries only: hook -> AI is everywhere (0:24), into start now (1:11), into this has happened before (2:31), before the close; longest unbroken board run would be the thrive board (~35s), so no interleaving needed
LISTENING: 0:13–0:27 and 3:28–3:37 re-transcribed with small.en; "Mainz" is not spoken in this roll (no garble to check)
```

Decision: build from roll 2 (Why_Learn_AI__The_Historical_Shift.mp4). Roll 1 drops half the White House quote and paraphrases the "run it" line.

## Best-of plan (added 2026-09-14 under the beat-by-beat rule; retrospective check of the shipped v3)

```text
BEST-OF PLAN: why-learn-ai
BASE: Prompts/why-learn-ai-2.mp4 (Historical Shift roll, shipped 2026-09-13 as v3)
  Scribe story; two choices; run it or someone else will — roll 1 TAUGHT @0:00–0:27 "Ignore the change or learn to run it… master the tool or step aside for someone who will" | roll 2 RICH @0:00–0:24 "Pretend it isn't happening, or learn to run it… Run the machine, or someone else will take your place" — TAKE roll 2
  AI is everywhere: apps, search results, first job; sci-fi to normal; better tomorrow — roll 1 TAUGHT @0:27–0:40 "already running inside the apps on your phone, the search results you read, and the tools you'll be handed on your first day of work" | roll 2 TAUGHT @0:24–0:37 "already running inside the tools your first job will hand you on day one" (apps and search dropped) — roll 1 fuller by a clause; both drop "it will do better tomorrow"; sits under Notebook's Gutenberg diagram in the shipped edit (risky kind) — not grafted
  Where AI Already Lives: five rows, each with its job and its examples — roll 1 RICH @0:40–1:34 (each row named and explained with every example: "Spotify, Netflix, or TikTok predict what you might like next… Google Maps or Waze use AI to analyze traffic patterns and calculate your arrival time… unlock your phone by looking at it, or an app tags your friends in a photo… Siri, Alexa, and Google use AI to turn the sound you make into written words… ChatGPT, Claude, and Gemini use AI to hold conversations"; banner "AI was already part of your daily routine long before these conversational chatbots arrived") | roll 2 TAUGHT @0:37–1:04 (one sentence per row, examples halved: Spotify or TikTok, Google Maps, phone unlock, Siri and Alexa) — TAKE roll 1 (under Where AI Already Lives; the dense leg's five dives and the banner would follow roll 1's onsets; roll 1 0:40.2–1:34.6 replaces roll 2 0:36.8–1:10.9)
  You can start now — roll 1 TAUGHT @1:34–1:42 | roll 2 TAUGHT @1:10–1:18 — tie (both drop "learn what AI does well, notice where it struggles… every project gives you experience")
  Desktop publishing story — roll 1 TAUGHT @1:42–2:02 (no posters / magazines / brochures) | roll 2 RICH @1:18–1:47 "create professional posters, magazines and brochures… The software did not replace design skill. It simply shortened the distance between wanting to do the work and actually getting it done" — TAKE roll 2
  Why You'll Thrive: three reasons — roll 1 RICH @2:02–2:45 | roll 2 RICH @1:52–2:31 — tie
  This has happened before: steam, electricity, internet; AI across almost everything — roll 1 TAUGHT @2:45–3:04 | roll 2 RICH @2:31–2:59 — TAKE roll 2
  White House quote — roll 1 THIN (half the quote) | roll 2 RICH @2:59–3:23 (full, with "This is the potential that AI presents") — TAKE roll 2
  Close lines — both verbatim — roll 2
GRAFTS: 1 recommended, under Where AI Already Lives (roll 1 0:40.2–1:34.6 for roll 2 0:36.8–1:10.9; +20 s). Not yet built; the live v3 stands until David says go.
```
