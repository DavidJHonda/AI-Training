# What Is AI? Current live specification review, September 28, 2026

The live video does not fully meet the current specs. Keep its lesson structure and investigate targeted repairs. The earlier definition/close problems have been fixed; the remaining problems are narrower. This is an evaluation, not a build or shipping certification.

Evidence limit: I read the current lesson and complete fresh transcript, inspected contact sheets across the full runtime plus selected full-resolution frames, and measured board spans and rings. I did not directly hear the audio or watch continuous playback end to end. Therefore narration and donor wording below are transcript evidence, not listening certification. A formal verified REPAIR verdict requires auditioning the proposed joins. No verified reroll requirement has been established.

## Exact version and sources

- Deployed page: `https://besmarterthanthetool.com/`, `LESSON_VIDEOS.llms`, cache key `20260926ship5`.
- Deployed MP4: `https://besmarterthanthetool.com/course-assets/what-is-ai/what-is-ai.mp4?v=20260926ship5`, HTTP 200, 17,575,182 bytes.
- Deployed stream SHA-256 equals the local canonical MP4: `d3dc0512652914a55725b53eb478eafec727e20c968773481e2621127511feff`.
- Sequential decode: 5,156 frames, 30 fps, 1280×720, 2:51.87. This is the shipped September 26 v8 narration repair, not the September 25 reviewed file.
- Authorities: `index.html` LLMsSection and referenced canonical boards; `scripts/video/EDIT-SPEC.md` (September 26), `NARRATION-REVIEW.md`, shared README; current lesson Markdown and video prompt for production requirements.
- Source hashes and deployment verification: `source-verification.json`. Workflow tracker status was not checked or changed.

## Findings, in priority order

1. **Incomplete compliance with the current narration recipe.** The opening omits asking a friend for help. The ten-topic example is compressed to “from ancient Egypt to the Berlin Wall,” leaving eight names unspoken. Three of eight required verbatim lines are paraphrased (table below). These are current recipe failures even though the main picks-versus-creates explanation remains clear.
2. **Both dense board walks crop inside the cards.** At approximately 1:05–1:51 and 2:04–2:36, excluding cutaways, the camera frames the text sections and discards nearly all of each active card's illustration. The active text is legible, but Edit Spec §§1b/4 require the complete active card, including illustration, title, and bottom section. The introductory rings also frame titles rather than whole cards. See `frames/0066.00.jpg` and `sheets/sheet-02.jpg`. This treatment was intentionally built and previously approved in v7; it is a discrepancy with the written current spec, not a new regression.
3. **Notebook artifacts remain at 0:26.10–0:43.20.** The first frame after the desk board resumes partway through a chip-to-four-panel transition, showing “AI: Software Emulating Intelligence,” pseudocode and “Algorithmic Logic & Neural Models.” The following panel adds off-recipe examples and the heading “Key AI Capabilities in Action.” At 0:33.53–0:37.60 the people/server drawing contains “ADULTS of CHATTING” and “WE'LL FINDING ABOUT CONNECTION?” At 0:37.60–0:43.20 the laptop's fourth item is garbled, with yellow marker washes. These are distracting text/production defects; the illustrated people themselves are allowed by the September 26 rule.
4. **Donor cutaways retain treatments barred by the current written spec.** At 1:13.47–1:17.00 and 1:34.97–1:44.17 the donor diagram restates the same two-category board using “synthesizes new content” and “New Synthetic Output,” rather than supplying a concrete drawn example (§8b). At 2:25.17–2:32.07 the Maya/Leo reading card has broad purple highlighting (§5 prohibits Notebook washes anywhere). These cutaways were expressly approved for v6/v7; report them as existing exceptions/deviations, not newly introduced defects. The Maya/Leo illustrations are allowed.
5. **Voice is wordier than the present recipe.** Examples include “Its primary job,” “two specific kinds you likely already interact with daily,” the spoken production reference “This board breaks down those two systems,” and “a completely original scene.” The last phrase overstates what the lesson's “a scene from your request” promises. Tightening these is secondary to coverage and mandatory wording. “Ideas for your homework” at about 0:31 preserves the general function but loses the history-project callback.

## Teaching coverage

Times below are approximate segment-level ASR times; picture cuts in the visual tables are frame-derived.

| Lesson point | Assessment | Evidence |
|---|---|---|
| History project without a topic; asking the desk | RICH | 0:00–0:12, same setup and question; joke paraphrased |
| Ask a friend, then ask AI | MISSING friend comparison / TAUGHT AI | 0:12 jumps directly to AI |
| Ten history ideas | TAUGHT as a brainstorming example; incomplete required enumeration | 0:14–0:22 names only Ancient Egypt and Berlin Wall |
| Core definition | TAUGHT | 0:22–0:26, current exact sentence |
| Understand, summarize, translate, suggest | TAUGHT | 0:26–0:33; fourth example generalized to homework |
| Does not imply human thought; not all ideas good | RICH | 0:33–0:46; explains both and suggests using only two ideas |
| Tool for formerly human tasks | TAUGHT | 0:46–0:54 |
| Different systems, different jobs | TAUGHT | 0:54–1:02; bridge into two kinds present |
| Recommendation: existing choices, ranking, best match | RICH | 1:05–1:17 |
| Netflix, Spotify, Maps examples | TAUGHT | 1:17–1:24; ASR's “your out” needs listening, not a finding of misspoken “route” |
| Generative: learned patterns create output | TAUGHT | 1:24–1:35 |
| Prompt means question or instructions | TAUGHT | 1:35–1:41 |
| Email, essay, image, website, song, video | TAUGHT | 1:45–1:50; all six included |
| Distinction and course focus | TAUGHT meaning / mandatory wording missed | 1:50–1:57 |
| Superhero scenario and existing movie | RICH | 1:57–2:16; catalog, interests, Captain America: Civil War |
| Create a scene; teammates disagree | RICH | 2:16–2:32; all three Maya/Leo dialogue lines transcribed |
| Generative result | TAUGHT meaning / mandatory wording missed | 2:32–2:35; adds “completely original” |
| Find something to watch versus create a story | TAUGHT | 2:35–2:41, exact current takeaway |
| Two-line close | TAUGHT | 2:42–2:48, exact current close |

The lesson arc works: familiar task → definition and limits → two jobs → same-theme comparison → course focus. There is no need to restructure that arc. Source QA: no material contradiction found between the current lesson, boards and Markdown. Extra prompt requirements such as reading all ten names are recorded as production requirements rather than pretending the abbreviated example fails to explain brainstorming.

## Current mandatory audio

| Required line | Status in fresh transcript |
|---|---|
| “Nothing. It’s a desk.” | MISSED, ~0:10: “Nothing happens. It's a desk.” |
| “AI is software built to do things that used to take a human brain.” | MET, ~0:22 |
| “AI can recommend. AI can create. This course focuses on generative AI.” | MISSED, ~1:50: “One system recommends, and the other creates. This course focuses solely on generative AI.” |
| “It picked a movie that already exists.” | MET, ~2:14 |
| “It generated a scene from your request.” | MISSED, ~2:32: “It generated a completely original scene from your request.” |
| “One helps you find something to watch. The other helps you create a story of your own.” | MET, ~2:36 |
| “Two kinds. One picks, one creates.” | MET, ~2:42 |
| “This course is about the one that creates.” | MET, ~2:46 |

ASR punctuation cannot establish spoken punctuation or cadence. The three failures above are actual word differences, not punctuation differences.

## What now meets the spec

- The desk board stays up through the definition, 0:12.33–0:26.10, with its full banner ring. The old invented-date timeline is gone.
- Canonical boards are recognizable and match current assets. Boards open whole and unmarked before the first ring.
- Course highlight strokes measure **4 px at 720p**: 135 detected course-ring samples. Twelve 2 px detections are Notebook diagram strokes at 0:28–0:34, not thin course rings. The obsolete 5 px line in the README checklist does not override Edit Spec §5.
- Pacing has improved substantially: no single canonical teaching-board hold exceeds about 18 seconds. The longest continuous sequence across adjacent teaching boards is **23.5 seconds**, 1:44.17–2:07.67. It is not the old 111.6-second board run.
- The catalog-grid cutaway at 2:07.67–2:10.07 supports the existing-catalog narration.
- The close is the actual final frame. The build record specifies the standard hold/push/settled hold; beginning, later and final close frames are consistent with that treatment. Exact motion was not remeasured frame by frame.
- No non-course photographic scene or visible engine corner mark was found in the inspected frames. This is sampled evidence, not a whole-file clearance. The desk board's photographic illustration is a canonical course asset, explicitly exempt under §8c.

## Board timing and proposed treatment

This is a reviewable direction for a repair, not a rendered candidate. Timings must be recalculated if narration grafts change duration. Existing approved motion is retained in intent, but its framing needs correction to meet the complete-card rule.

| Board | Highlighting sequence | Camera | Current screen spans / proposed breaks |
|---|---|---|---|
| Ask the Desk. Ask AI. | Unmarked opening; question/list as spoken if expanded; full definition banner | Full view; no conversation dive | 0:12.33–0:26.10 (13.77 s). Retain current hold for unchanged audio. An expanded list needs a newly timed plan and a suitable drawing if the hold exceeds ~20 s. |
| Two Ways You Already Use AI | Whole Recommendation card, then job / how / examples; whole Generative card, then corresponding sections; full banner | Whole board first, then equal complete-card views, pull back for takeaway | 1:02.37–1:13.47, 1:17.00–1:34.97, 1:44.17–1:57.87. Preserve break locations where feasible, but replace the restated-board donor diagram with an appropriate drawing. A new acceptable donor is not yet verified. |
| One Picks. One Creates. | Scenario; whole Recommendation card, job / result / picked line; whole Generative card, job / dialogue / generated line; full banner | Whole board first, complete-card dive and pan, pull back for takeaway | 1:57.87–2:07.67, 2:10.07–2:25.17, 2:32.07–2:42.07. Keep catalog cutaway. Replace or clean Maya/Leo marker treatment without dropping the worked example. |
| Two kinds. One picks, one creates. | Unmarked | Preserve standard close | 2:42.07–2:51.87; retain through literal final frame |

The two tall comparison boards may yield only modest text enlargement when the entire card remains visible. Preview the complete-card framing before committing to its legibility. Do not silently preserve text-only crops as compliant.

The automated board detector falsely matches the Notebook four-panel to the close at 0:32–0:34 and donor category cards to One Picks at 1:13.5 and around 1:35–1:40. Those hits are excluded above. Returning from the first donor at 1:17 is likewise corrected against actual picture cuts, rather than taking the detector's 1:15 at face value.

## Existing audio worth auditioning before a reroll

These are candidate whole-beat donors identified in existing timestamped transcripts. Boundaries need word-level checking, silence measurement and in-context listening. They are not verified graft instructions.

| Target | Potential source and source words |
|---|---|
| Opening joke and friend, live ~0:10–0:14 | `Prompts/what-is-ai-1.mp4` ~0:10.28–0:19.56: “Nothing. It's a desk. You could ask a friend and they can help you brainstorm. Ask AI and it can give you a list in seconds.” Exclude the earlier spoken “Pause.” |
| Full ten-item list, live ~0:14–0:22 | `Prompts/what-is-ai-2.mp4` ~0:32.92–0:46.74: Ancient Egypt, printing press, Silk Road, moon landing, Roman Empire, Industrial Revolution, civil rights movement, history of voting, invention of flight, Berlin Wall. Roll 1's list omits Industrial Revolution and cannot satisfy this requirement. |
| Optional exact history-project callback, live ~0:26–0:33 | Roll 1 ~0:40.48–0:47.64: complete four-example sentence ending “suggest ideas for a history project.” |
| Mandatory categories banner, live ~1:50–1:57 | Roll 1 ~1:41.68–1:47.00, or roll 2 ~2:12.70–2:19.78: “AI can recommend. AI can create. This course focuses on generative AI.” |
| Generated-result line, live ~2:32–2:35 | Roll 1 ~2:33.44–2:36.44, or roll 2 ~2:59.30–3:02.30: “It generated a scene from your request.” |

No additional pauses proposed from transcript evidence alone. Natural pacing and all audio joins require listening. A fresh generation would only be justified if the existing donors cannot be joined coherently or the broader voice needs replacing after audition.

## Verification and remaining limits

Completed: deployed URL and content hash, fresh base.en transcript of the exact live MP4, sequential frame decode, full-runtime 4-second contact sheets, selected native-resolution frames, canonical comparison-board inspection, board-span measurement and ring-width measurement. Read both existing donor transcripts and prior build records.

Not completed: direct listening, continuous end-to-end playback review, independent word-level retranscription, donor join auditions, fresh transition guard over every inherited splice, exact close-motion remeasurement, or workflow tracker lookup. Consequently this report establishes specific current-spec failures and a repair direction, not a formal shipping pass or a fully verified narration-repair plan.

No lesson, prompt, canonical asset, live MP4, or deployment changed. Only this audit directory was created.
