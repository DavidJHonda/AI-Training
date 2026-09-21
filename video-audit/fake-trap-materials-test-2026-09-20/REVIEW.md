# Fake Trap materials test — 2026-09-20

Purpose: test whether restoring the 2026-09-11 recipe (voice block + beat spine in the
prompt, clean upload Markdown, text-only uploads of the face boards) produces a roll that
beats the current best candidate. Baseline is `Prompts/fake-trap-v3.mp4`, which David
judged shippable on 2026-09-20. Nothing here changes the live video or the v3 candidate.

**Result (2026-09-20 evening): the new kit wins.** Roll 2 (`Prompts/fake-trap-new-2.mp4`)
is the base; roll 1 supplies the four-motive passage. Details below the baseline.

## What changed in the materials

| | 2026-09-18 kit (rolls 1 and 2, the v3 donors) | 2026-09-20 test kit |
|---|---|---|
| Prompt | Generic speak-the-answers template; no VOICE block; no verbatim list; few named beats | VOICE block (9/11 wording plus lesson-specific banned words), 8 required-verbatim lines, beat spine naming every teaching point; 480 words |
| Markdown | Board sections with `Takeaway` lines, `Scene (your own drawing, no board)` markers, `Course image (post-production only)` labels | Board / Image file / Teaching content only; banner lines as plain sentences; 886 words |
| Face boards | Withheld entirely; Notebook taught Board 1 and Board 3 over invented scenes | Uploaded as text-only variants (`Prompts/fake-trap-*-faceless.jpg`); canonical boards replace them in post |
| Uploads | 4 files (md + 3 JPGs) | 6 files (md + 5 JPGs) |

Everything else is held constant: same lesson text, same boards, same close board, same
Notebook account. Watermark: the Gemini mark is present on both rolls (see Editing notes).

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

## Rolls

| Roll | File | Runtime | Frames |
|---|---|---|---|
| new-1 | `Prompts/fake-trap-new-1.mp4` | 4:06.33 | 7,390 @ 30 fps, 1280×720 |
| new-2 | `Prompts/fake-trap-new-2.mp4` | 5:04.43 | 9,133 @ 30 fps, 1280×720 |

Transcripts: `fake-trap-new-1/transcript.txt`, `fake-trap-new-2/transcript.txt` (segment
level, faster-whisper base.en). Contact sheets in each roll's `sheets/`.

## Per-roll block: fake-trap-new-2 (BASE)

```text
LESSON: fake-trap
CANDIDATE: Prompts/fake-trap-new-2.mp4 (5:04)
VERDICT: REPAIR (one THIN essential beat; roll 1 supplies the complete donor)
TEACHING POINTS:
  Hook: AI can fake a voice, face, video, screenshot; knowing isn't a skill; ten seconds after a clip hits your feed — RICH — 0:00–0:18, lesson wording
  Scenario: principal clip, closed next week — RICH — 0:20 ("classes are cancelled for the entire next week")
  Before AI: face, voice, hallway; matched how the principal talks; verdict real — RICH — 0:30–0:45 "you reached a verdict. The video is real."
  AI era: ignore pixels, check the trail, source that would know, nothing on the website; verdict unverified — RICH — 0:45–1:04
  Banner: "Appearance can mislead. The source trail can be checked." — RICH — 1:04 verbatim
  The Fake Trap definition — TAUGHT — 1:08 "believing a piece of media because it looks real" (three words added)
  Second jaw — RICH — 1:12 "dismissing the actual truth because it could be a fake"
  Stanley Cup joke; trap begins when someone is meant to believe it — RICH — 1:17–1:30
  Four motives with reasons — THIN — 1:38–1:53: Money complete; Power drops "protest, and spend"; Fame drops "It does not have to be true to travel"; Cruelty drops "especially at school"
  Banner: "Harmful fakes are made to get something back." — TAUGHT — 1:30 "specifically engineered to extract something from you" (paraphrase; register drift)
  Detector dead end: patterns, conflicting results, don't let it decide — TAUGHT — 1:53–2:14; "clue, never a ruling" not spoken; adds "confirm the truth through your own independent investigation"
  Test moves off the image; Board 3 line — RICH — 2:14–2:24 "Check the source, not the pixels. Shift your focus away from appearance and toward independent evidence."
  Emotion cue: outrage, fear, excitement, hope; stop; three checks before you react, share, or believe — RICH — 2:24–2:35, all four named
  Three checks with their questions — RICH — 2:35–2:57, each question spoken
  Checks applied to the clip; repost not confirmation; unverified — RICH — 3:06–3:46
  "That does not prove the clip is fake" — TAUGHT — 3:46 "You don't need to definitively prove the clip as an AI generation; leaving it unverified protects you from the trap"
  One rule; voicemail; clip — RICH — 3:53–4:10
  "Until the trail checks out, unverified is your answer" — RICH — 4:10 verbatim; "for something important, look for independent confirmation too" not spoken (minor sub-clause)
  Eyes still work / lie detector — RICH — 4:14–4:23
  If the fake is about you: save details when safe; adult that day, parent/counselor/someone at school — RICH — 4:23–4:38
  Under-18 image rule; tell an adult; report through the platform; Take It Down and CyberTipline — RICH — 4:38–4:53
  "You did nothing wrong by being targeted." — RICH — 4:53 verbatim
HARD REQUIREMENTS:
  "Appearance can mislead. The source trail can be checked." — MET — 1:04
  "The Fake Trap is believing it because it looks real." — MET (near) — 1:08 "believing a piece of media because it looks real"
  "Harmful fakes are made to get something back." — MISSED — paraphrased at 1:30
  "Treat its verdict as a clue, never a ruling." — MISSED — meaning taught at 2:00 ("cannot make a final decision for you"), line not spoken
  "Check the source, not the pixels." — MET — 2:18 and 4:58
  "Verify somewhere the sender does not control." — MET — 3:53
  "You did nothing wrong by being targeted." — MET — 4:53
  Closing lines verbatim, in order, nothing spoken after — MET — 4:56 / 4:58; engine outro card at 5:04 is visual only
  No web address on screen — MET — none seen on the contact sheets
  No advice to save a copy of an under-18 image — MET
ERRORS: none
SOURCE_QA: PASS
ADDITIONS: "you stop trying to spot fakes with your eyes; you transfer the burden of proof onto verifiable external evidence" (2:57–3:06) is accurate but formal; harmless
REPAIR PLAN: replace 1:30.0–1:53.0 (motive lead-in + thin list) with roll 1's 1:22.8–1:44.3 (lead-in + all four motives in lesson wording), under the reasons board; see BEST-OF PLAN
EDITING NOTES: Gemini Notebook corner mark on every frame; close board shown at 2:16–2:24 in place of Board 3 (canonical Board 3 goes there); faceless Board 1 held 0:26–1:16 with Notebook's own highlights (50 s run); drawn people with faces at 1:24 and 4:36 are Notebook drawings, not stock; engine outro after the close
LISTENING: transcript read in full; audio not auditioned; word-level timing for the graft to be measured at build
```

## Per-roll block: fake-trap-new-1 (DONOR)

```text
LESSON: fake-trap
CANDIDATE: Prompts/fake-trap-new-1.mp4 (4:06)
VERDICT: REPAIR (loses to roll 2; close line altered and words spoken after it)
TEACHING POINTS:
  Hook — TAUGHT — 0:00–0:12 (drops the voice/face/video/screenshot list)
  Scenario — RICH — 0:12
  Before AI; verdict real — RICH — 0:20–0:38 "you reached a verdict. It was real."
  AI era; verdict unverified — THIN — 0:38–0:52 "you find nothing"; the word "unverified" is not spoken here
  Banner: "Appearance can mislead…" — RICH — 0:52 verbatim
  Definition — RICH — 0:56 verbatim
  Second jaw — TAUGHT — 1:00 "dismiss the truth simply because you suspect it might be AI generated"
  Stanley Cup — RICH — 1:09–1:22
  Four motives with reasons — RICH — 1:22–1:44 "Money. Outrage generates clicks and clicks pay. Power. Changing beliefs influences how people vote and spend. Fame. Viral clips bring followers without needing to be true. Cruelty. Some fakes exist solely to humiliate an individual, particularly at school." (Power drops "protest")
  Banner: "Harmful fakes are made to get something back." — THIN — 1:22 "usually driven by four motives"
  Detector dead end — TAUGHT — 1:53–2:07 "starting point, never a final ruling"; the follow-on "then check source, context, corroboration" not spoken
  Emotion cue — RICH — 2:07–2:23, all four, "before you react, share, or believe"
  Test moves off the image — TAUGHT — 2:23
  Three checks with questions — TAUGHT — 2:28–2:45, shortened questions folded into the application
  Application; repost not confirmation — RICH — 2:28–2:58 ("Beware of the illusion of confirmation")
  "Does not prove fake" — TAUGHT — 2:58 "even if you can't definitively prove it's fake"
  One rule; voicemail; clip — RICH — 3:04–3:22
  "Until the trail checks out…" — MISSING
  Eyes still work — RICH — 3:22
  Safety: save details; adult that day — TAUGHT — 3:29–3:41 (no adult examples)
  Under-18 rule; resources — THIN — 3:41–3:52 "If you see a private image of someone under 18" (drops "fake"); Take It Down only, CyberTipline not named
  "You did nothing wrong by being targeted." — RICH — 3:52 verbatim
HARD REQUIREMENTS:
  Closing lines verbatim, nothing after — MISSED — 3:55 "Check this source, not the pixels." then 4:01 "Fade to black." spoken
  "Harmful fakes are made to get something back." — MISSED
  "Treat its verdict as a clue, never a ruling." — MISSED
ERRORS: 3:55 "Check this source" — lesson says "Check the source"
SOURCE_QA: PASS
ADDITIONS: 1:44–1:53 "shift from a passive viewer to a skeptic who recognizes that someone stands to gain from your reaction" — accurate, optional graft
REPAIR PLAN: not needed; used as donor only
EDITING NOTES: corner mark on every frame; engine outro at 4:04; never use this roll's close
LISTENING: transcript read in full; audio not auditioned
```

## Comparison: v3 baseline against the new rolls

| Teaching point | v3 | new-2 (raw) | new-1 (raw) |
|---|---|---|---|
| Hook and "knowing isn't a skill" | TAUGHT | RICH | TAUGHT |
| Before AI: verdict "real" spoken | TAUGHT (unspoken) | RICH | RICH |
| AI era: verdict "unverified" | RICH | RICH | THIN |
| Banner: appearance can mislead / trail can be checked | THIN | RICH (verbatim) | RICH (verbatim) |
| Trap definition verbatim | TAUGHT (paraphrase) | TAUGHT (near) | RICH |
| Second jaw | TAUGHT | RICH | TAUGHT |
| Stanley Cup joke | RICH | RICH | RICH |
| Four motives, lesson wording | TAUGHT (register drift) | THIN | RICH |
| Banner: made to get something back | TAUGHT | TAUGHT | THIN |
| Detector dead end | RICH | TAUGHT | TAUGHT |
| Four emotions named | TAUGHT (3 of 4) | RICH | RICH |
| Three check questions spoken | THIN | RICH | TAUGHT |
| Checks applied to the clip | RICH | RICH | RICH |
| "Does not prove the clip is fake" | MISSING | TAUGHT | TAUGHT |
| One rule + both examples | RICH | RICH | RICH |
| "Until the trail checks out" | THIN | RICH | MISSING |
| Eyes-still-work line | RICH (moved) | RICH | RICH |
| Safety guidance + both resources | RICH | RICH | THIN |
| "You did nothing wrong" | RICH | RICH | RICH |
| Close verbatim, nothing after | MET (with a lead-in sentence) | MET | MISSED |
| Voice sources in the candidate | 3 (live 9/07, roll 2, roll 1) | 1 | 1 |
| THIN / MISSING count (essential beats) | 3 / 1 | 1 / 0 | 4 / 1 |
| Runtime | 4:26 | 5:04 | 4:06 |

Register: v3's motive passage was the worst offender ("translates directly to financial
profit", "deliberate tactic"). Both new rolls speak the lesson's required lines verbatim,
and the remaining formal substitutions sit in connective sentences ("engineered to
extract", "burden of proof onto verifiable external evidence", "illusion of confirmation")
rather than in the teaching lines. Modest improvement, not a transformation.

Decision rule from the setup: the new kit wins if the raw roll has no MISSING essential
beat, fewer THIN beats than v3, and the close verbatim. new-2 raw: 0 MISSING, 1 THIN,
close verbatim. **The kit wins.** Recommendation: roll the remaining Avoid Traps lessons
on this recipe (voice block + verbatim list + beat spine; clean Markdown; faceless
variants of face boards).

Two lesson lines were not spoken verbatim in either roll: "Harmful fakes are made to get
something back." and "Treat its verdict as a clue, never a ruling." Both are taught in
meaning. The old fake-trap-2 roll (in v3 at 2:22) has the detector line near-verbatim, but
it is a different generation's voice under a Notebook drawing, so it is not proposed as a
graft. Owner's call whether either line is a ship blocker; the reviewer's view is no.

## BEST-OF PLAN: fake-trap

```text
BEST-OF PLAN: fake-trap
BASE: Prompts/fake-trap-new-2.mp4 (complete coverage, every banner but one verbatim, clean close, single voice)
  Four motives — roll 2 THIN @1:38–1:53 "Second, power. Change what people believe to change how they vote. Third, fame. Viral clips mean followers." | roll 1 RICH @1:22.8–1:44.3 "Money. Outrage generates clicks and clicks pay. Power. Changing beliefs influences how people vote and spend. Fame. Viral clips bring followers without needing to be true. Cruelty. Some fakes exist solely to humiliate an individual, particularly at school." — TAKE roll 1 (under the reasons board; replaces roll 2's 1:30.0–1:53.0 including its lead-in)
  Skeptic addition — roll 2 absent | roll 1 @1:44.3–1:53.3 "When you understand why these fakes are made, you can shift from a passive viewer to a skeptic…" — OPTIONAL (would ride the same graft; owner's call)
  Detector line "clue, never a ruling" — roll 2 TAUGHT @2:00 | roll 1 TAUGHT @2:03 "starting point, never a final ruling" — not grafted: neither is verbatim, roll 2 stays
  Everything else — roll 2 RICH or TAUGHT and equal or better than roll 1 — keep roll 2
GRAFTS: 1 (2 if the skeptic sentence is taken), all under the reasons board
```

## Proposed edit plan for approval (Edit Spec section 1b)

Base timeline is roll 2; times are roll 2 source times before the graft shifts them.

| Board / scene | Source span | Proposed treatment |
|---|---|---|
| Board 1, The Same Clip. Two Eras. (canonical, faces) | 0:26–1:08 | Replace the faceless variant with the canonical board. Full view at "This chart compares" (0:26); whole-card ring on Before AI at 0:30, on The AI Era at 0:45; banner ring at 1:04. 42 s run, under the 60 s guideline. Keep Notebook's phone drawing (0:20) before it and the 1:08 definition drawing after. |
| Board 2, Why Some Fakes Aren't Friendly | graft: roll 1 1:22.8–1:44.3 replacing roll 2 1:30.0–1:53.0 | Full view at the lead-in; card rings on Money / Power / Fame / Cruelty at roll 1's spoken onsets (word timing measured at build). Banner is not spoken verbatim by roll 1; ring it at the lead-in or leave it unringed. Owner's choice. |
| Board 3, Check the Source, Not the Pixels (canonical, faces) | 2:14–2:24 | Notebook showed the close board here; the canonical Board 3 replaces it. Full view; banner ring at "toward independent evidence" (2:21). |
| Board 4, Move the Test Off the Image | 2:35–3:06 | Full view at "This panel shows"; card rings Source 2:35, Context 2:42, Corroboration 2:49. Return to Notebook's own application drawings 3:06–3:46 (the tabbed SOURCE / CONTEXT / CORROBORATION scenes are good and break the board run). |
| Board 4 banner | 3:53 | Optional second visit: hold the checks board with the banner ringed under "Verify somewhere the sender does not control." Otherwise keep Notebook's "verification principle" drawing. Owner's choice. |
| Standard close | 4:56–5:01 | Trim the engine outro (5:01 on); standard close board with the prescribed hold and push. |

Corner mark: run the Gemini mark removal pass over every kept Notebook frame (Edit Spec
section 8); the setting was evidently on for this generation. Check the toggle before the
next rolls.

Selective pauses (proposals only; measure existing gaps at build): 1:08 banner to
definition; 1:53 motives to detector (the graft seam); 2:24 Board 3 to the emotion cue;
4:23 eyes line to the safety section. No automatic one-second minimum.

## How to run the next lesson on this recipe

1. Rebuild the lesson's Markdown to the clean Board / Image file / Teaching content form
   with banner lines as plain sentences. Visible page text only.
2. Prompt: the Fake Trap prompt is the template. Swap the verbatim list and the beat spine;
   keep the VOICE block. Under 500 words.
3. Face boards: cut the photo panels and upload the text-only variant from `Prompts/`.
4. Two rolls the same day; compare beat by beat before any build.
