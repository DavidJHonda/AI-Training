# Fake Trap materials test — 2026-09-20

Purpose: test whether restoring the 2026-09-11 recipe (voice block + beat spine in the
prompt, clean upload Markdown, text-only uploads of the face boards) produces a roll that
beats the current best candidate. Baseline is `Prompts/fake-trap-v3.mp4`, which David
judged shippable on 2026-09-20. Nothing here changes the live video or the v3 candidate.

## What changed in the materials

| | 2026-09-18 kit (rolls 1 and 2, the v3 donors) | 2026-09-20 test kit |
|---|---|---|
| Prompt | Generic speak-the-answers template; no VOICE block; no verbatim list; few named beats | VOICE block (9/11 wording plus lesson-specific banned words), 8 required-verbatim lines, beat spine naming every teaching point; 480 words |
| Markdown | Board sections with `Takeaway` lines, `Scene (your own drawing, no board)` markers, `Course image (post-production only)` labels | Board / Image file / Teaching content only; banner lines as plain sentences; 886 words |
| Face boards | Withheld entirely; Notebook taught Board 1 and Board 3 over invented scenes | Uploaded as text-only variants (`Prompts/fake-trap-*-faceless.jpg`); canonical boards replace them in post |
| Uploads | 4 files (md + 3 JPGs) | 6 files (md + 5 JPGs) |

Everything else is held constant: same lesson text, same boards, same close board, same
Notebook account and watermark setting.

## Baseline: fake-trap-v3 (per-roll block)

v3 is itself a best-of build: live 2026-09-07 audio for 0:00–1:14, roll 2 as the spine,
roll 1 for the four-motive passage, plus cuts. So the baseline is the best the 9/18 kit
produced after three build rounds, not a raw roll. The new roll is judged raw first; a
fair second comparison is "new roll after one build round" against v3.

```text
LESSON: fake-trap
CANDIDATE: Prompts/fake-trap-v3.mp4 (4:26)
VERDICT: KEEP (owner call 2026-09-20; THIN beats below are the comparison targets)
TEACHING POINTS:
  Hook: you already know fakes exist; knowing isn't a skill; the ten seconds after a clip hits your feed — TAUGHT — 0:00 "how you react in the first 10 seconds… very few people have a practiced routine" (drops "cheaply and convincingly, only getting better" and "AI has changed the playing field")
  Scenario: principal clip, school closed next week — RICH — 0:13
  Before AI: study face, voice, hallway; verdict real — TAUGHT — 0:19–0:30 method described; the verdict "real" is never spoken
  AI era: ignore pixels, check the trail, nothing on the school website; verdict unverified — RICH — 0:32–0:42
  Banner: "Appearance can mislead. The source trail can be checked." — THIN — implied by 0:30–0:42, never spoken
  The Fake Trap definition — TAUGHT — 0:43 "accept media as true because the visuals and audio match your expectations of reality" (paraphrase of "believing it because it looks real")
  Second jaw — TAUGHT — 0:51 "dismiss a proven fact as AI simply because the information is surprising or inconvenient" (lesson: "because it could be a fake")
  Stanley Cup joke; trap begins when someone is meant to believe it — RICH — 0:59–1:22
  Four motives with reasons — TAUGHT — 1:22–2:02 all four present; register drifts ("translates directly to financial profit", "deliberate tactic", "targeted individual… school environments")
  Banner: "Harmful fakes are made to get something back." — TAUGHT — 1:26 "manufactured to get something in return"
  Detector dead end: patterns, different answers, clue never ruling — RICH — 2:03–2:28
  Emotion cue: outrage, fear, excitement, hope; stop and run three checks — TAUGHT — 2:28–2:37 names three of four (excitement dropped); "before you react, share, or believe" not spoken
  Test moves off the image onto the source — TAUGHT — 2:37 "Move the test away from the image and look at the surrounding evidence trail"
  Three checks with their questions — THIN — 2:41 names them; the board questions ("Do they have a reason and a way to know?", "What important details are missing?") are not spoken
  Three checks applied to the clip; repost not confirmation; unverified — RICH — 2:48–3:09
  "That does not prove the clip is fake" — MISSING — not spoken anywhere
  One rule; voicemail; clip — RICH — 3:09–3:27 rule verbatim, both examples
  "For something important, look for independent confirmation too"; "Until the trail checks out, unverified is your answer" — THIN — only "remains unverified" at 3:04
  Eyes still work / lie detector — RICH — 4:06–4:14 (moved after the safety section; lesson order has it before)
  If the fake is about you: save details when safe, adult that day — RICH — 3:28–3:40
  Under-18 image rule; report through platform; Take It Down and CyberTipline — RICH — 3:40–4:03
  "You did nothing wrong by being targeted." — RICH — 4:03 verbatim
HARD REQUIREMENTS:
  "Treat its verdict as a clue, never a ruling." — MET — 2:22 "Treat a detector's verdict as a clue, but never a ruling"
  "Verify somewhere the sender does not control." — MET — 3:13
  Closing lines verbatim, in order, nothing after — MET — 4:18 / 4:21 (preceded by "So, always remember the ultimate rule.")
  No web address on screen — MET — replaced in the v1 build
  No advice to save a copy of an under-18 image — MET
ERRORS: none
SOURCE_QA: PASS
ADDITIONS: "very few people have a practiced routine for handling it" (0:08) is a fair gloss on "knowing fakes exist isn't a skill"; "step out of that app" (3:21) is a useful addition to the clip example
REPAIR PLAN: none required for the owner's KEEP; the MISSING qualifier and the two THIN beats are what the new roll must beat
EDITING NOTES: v3 carries three voice sources (live 9/07 opening, roll 2, roll 1 motives); the 1:14 and 1:46 joins are the listening risks already flagged in the v1/v2 reviews
LISTENING: transcript read in full; audio not re-auditioned for this baseline
```

## Comparison table (fill the right column from the new roll's transcript)

| Teaching point | v3 | New roll (raw) |
|---|---|---|
| Hook and "knowing isn't a skill" | TAUGHT | |
| Before AI: verdict "real" spoken | TAUGHT (verdict unspoken) | |
| AI era: verdict "unverified" | RICH | |
| Banner: appearance can mislead / trail can be checked | THIN | |
| Trap definition verbatim | TAUGHT (paraphrase) | |
| Second jaw | TAUGHT | |
| Stanley Cup joke | RICH | |
| Four motives, lesson wording | TAUGHT (register drift) | |
| Detector dead end | RICH | |
| Four emotions named | TAUGHT (3 of 4) | |
| Three check questions spoken | THIN | |
| Checks applied to the clip | RICH | |
| "Does not prove the clip is fake" | MISSING | |
| One rule + both examples | RICH | |
| "Independent confirmation too" / "until the trail checks out" | THIN | |
| Eyes-still-work line | RICH (moved) | |
| Safety guidance + resources | RICH | |
| "You did nothing wrong" | RICH | |
| Close verbatim, nothing after | MET | |
| Register: formal substitutions the lesson never uses | 8 in the transcript (translates directly, deliberate tactic, manipulating, manufactured, deployed, targeted individual, school environments, formal checks) | |
| Runtime | 4:26 | |

Decision rule: the new kit wins if the raw roll has no MISSING essential beat, fewer THIN
beats than v3, and the close verbatim. If it also reads in the lesson's register, roll the
rest of the Avoid Traps set on this recipe. If it loses on coverage but wins on register,
graft its beats under boards over the v3 spine. If it loses on both, the July "engine
variance on the day" explanation stands and the recipe change is not the lever.

## How to run

1. Follow `Prompts/fake-trap-upload-files.txt` (six uploads, prompt in the customization box,
   visible watermarking off). Save the roll as `Prompts/fake-trap-reroll.mp4` or the next
   free number. Two rolls on the same day if possible.
2. Transcribe with `grade_bundle.py` into this folder as `<roll>/transcript.txt`.
3. Fill the right column above, then write the BEST-OF PLAN block per
   `scripts/video/NARRATION-REVIEW.md`.
