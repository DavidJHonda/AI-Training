# Does AI Think? — current live evaluation, September 29, 2026

**Recommendation: REROLL narration, then rebuild the visuals.** The video covers the lesson's structure well, but fails the required comparison takeaway and substitutes stronger claims than the current lesson supports. Cosmetic editing alone cannot resolve those issues. No existing alternate audio was found to provide a verified repair.

**Review limitation:** this is a complete transcript comparison and sampled-frame production assessment, not a completed audiovisual sign-off. I read a fresh full-file transcript, inspected contact sheets across the full duration and selected full-resolution frames, and measured the encoded file. I did not hear the audio or watch continuous playback end to end; cadence, pronunciation, audio seams, and transient visual defects remain unverified. The findings below are sufficient to withhold a pass, but do not certify every other part of the file.

## Identity and scope

- Read-only evaluation; no lesson, prompt, canonical asset, or live video changed.
- The deployed page points to `course-assets/does-ai-think/does-ai-think.mp4?v=20260925ship12`.
- Streamed the published MP4 through SHA-256 without saving a duplicate: its checksum equals the local file and the September 25 row-walk manifest: `fe8d537e47bc8aa7ee9ec319fa227986dd0d46b907910c390a4047bf7474b77a`.
- 1280 × 720, 30 fps, 6,600 decoded frames, 3:40.00.
- Authorities: current `index.html` lesson and referenced JPGs; `lessons/does-ai-think.md`; current generation prompt; `scripts/video/NARRATION-REVIEW.md`; `scripts/video/EDIT-SPEC.md` updated September 29.
- The prior September 25 review predates the latest camera repair. This review freshly verified the current file rather than reusing that review's full-view comparison-board finding.
- Video Tracker not accessed or changed; no tracker status inferred.

## Narration

LESSON: does-ai-think  
CANDIDATE: current live file, 3:40  
VERDICT: **REROLL**, based on transcript evidence; listening remains outstanding.

| Essential point, in lesson order | Assessment | Evidence from the fresh transcript |
|---|---|---|
| Human-like answers: explanations, jokes, apologies | RICH | 0:00–0:09, all three behaviors explained |
| Why it feels as if someone is inside | TAUGHT | 0:09–0:16, natural responses create that impression |
| Ask whether AI thinks or understands like you | TAUGHT | 0:19–0:26, both questions asked |
| Fluency is insufficient evidence of understanding | TAUGHT | 0:27–0:39, sentence completion and poem explanation followed by “doesn't actually tell us if the machine comprehends” |
| Chinese Room setup: no Chinese, symbol-matching rulebook | RICH | 0:39–0:57, the room, person, language gap, and rulebook |
| Step 1: incoming Chinese note asks “How are you?” | RICH | 0:57–1:04, question spoken |
| Step 2: person cannot read it, looks up the whole phrase | RICH | 1:04–1:13, whole-phrase lookup on the wall chart |
| Step 3: matching reply, “I'm fine, thank you,” returned | RICH | 1:13–1:21, reply and return both spoken |
| Outside impression versus inside understanding | RICH | 1:21–1:36, fluent appearance contrasted with knowing zero Chinese |
| Convincing answer does not prove understanding | TAUGHT | Supported by the example; exact line spoken at 3:33–3:38 |
| LLM is not a literal rulebook; learned patterns predict responses | RICH | 1:39–1:50, explicit distinction and learned-pattern explanation |
| Producing an answer and understanding it are not necessarily the same | TAUGHT, with overstatement | 1:53–2:02 changes the cautious distinction to “an entirely different process” |
| Five-comparison orientation | TAUGHT | 2:02–2:10 introduces the human/AI comparison |
| Meaning: lived meaning versus learned patterns and prompt | TAUGHT | 2:10–2:20 covers both sides, albeit more technically |
| Experience: lived experience versus patterns learned from varied data | TAUGHT, with inaccurate narrowing | 2:20–2:30 covers both sides but says “works entirely with static scraped data” instead of the board's learned-pattern wording |
| Word choice: expression versus repeated next-word prediction | RICH | 2:30–2:39, intentional expression and predict/output/repeat |
| Beauty: personal response versus learned descriptions | TAUGHT | 2:39–2:51, both sides; “just regurgitating” is unnecessary and dismissive |
| Uncertainty: noticing doubt versus sounding certain when wrong | TAUGHT, with overstatement | 2:51–3:05, practical contrast present; “lacks that internal monitor” is stronger than the source |
| Similar-looking answers can come from very different processes | WRONG as stated | 3:05–3:15 replaces the limited comparison with “shares nothing in common with human cognition” |
| AI remains useful and can do impressive work | TAUGHT | 3:15–3:25; unnecessary consciousness assertion added |
| Return to fluency not proving human-like comprehension | TAUGHT | 3:25–3:31 |
| Both closing lines | TAUGHT | 3:31–3:38, correct words in order; transcript punctuation is not an audio check |

**Hard requirements:** the three-step example, both sides of all five comparisons, rulebook limitation, usefulness, and two closing lines are present. The prompt explicitly says “Speak every takeaway line as written” and explicitly requires “Similar-looking answers can come from very different processes.” That sentence is absent. The Chinese Room's takeaway is spoken verbatim at the close, so it is not absent from the video. The outside-observer sentence is a faithful near-paraphrase, not an essential teaching failure by itself.

**Material issues:**

1. **3:07.8–3:14.8:** “shares nothing in common with human cognition” overreaches the lesson's “can come from very different processes.” The problem is substantive, not merely a missed quotation. The lesson argues that a fluent answer is insufficient evidence; this replacement asserts a categorical conclusion.
2. **2:24.6–2:30.2:** “works entirely with static scraped data” loses the distinction between training data and learned patterns, and narrows the source beyond its wording. Restore the board's sentence about patterns learned from text, images, audio, and other data.
3. **3:18.1 onward:** “Even without human consciousness” adds an unnecessary assertion the lesson does not make. Similarly, avoid turning “can sound certain even when wrong” into a categorical claim about an absent internal monitor.

**SOURCE_QA: PASS for page/upload alignment.** No missing essential page teaching was found in the Markdown. This is not an independent scientific literature review. The page's careful claims are the appropriate teaching target. The historical unused `SIDES` array above the rendered lesson is not the displayed comparison; the current JPG and its alt text govern.

**ADDITIONS:** the clear inside/outside contrast at 1:25–1:36 strengthens the thought experiment. Preserve it in a new generation. The added jargon—“matrix,” “visceral,” “regurgitating,” “human cognition”—weakens the plain teacher-to-student voice.

**REPAIR PLAN: no verified audio repair.** No alternate Does AI Think roll remains in `Prompts/`. The audit directory retains `does-ai-think-illustration-sync-2026-09-21/baseline-live-2026-09-16.mp4`, but a fresh packet-payload hash confirms that its audio is identical to the current video (`audio-identity.json`), so it supplies no missing words. Earlier records identify the original rolls as deleted. The live file never speaks the missing takeaway. Cutting the consciousness clause alone would not solve the other defects. Do not call hypothetical donor audio a feasible repair.

**Reroll target:** retain the hook, complete Chinese Room example, explicit limitation of the analogy, five comparisons, usefulness, and exact close. Use the Markdown's cautious, plain wording; speak both board takeaways; avoid the absolute claims identified above. The existing prompt already asks for the missing line, so this was a generation failure, not missing source material. No new generation was requested or started during this evaluation.

## Production assessment

| Finding | Evidence and current-standard implication |
|---|---|
| Misleading generated graphics | Full-resolution frames at 0:28.5 and 0:36.5 show invented `P = 99.8%`, 0.88/0.03/0.09 probabilities, and “Internal Comprehension: ABSENT.” The last contradicts the lesson's caution. Replace these scenes; a neutral drawing can support fluency without pretending to measure comprehension. |
| Chinese Room stays on screen about 49.6 s | Exact existing insert: 0:46.30–1:35.87. Fresh feature matching splits this at a deep dive, but the 1:24 frame is still the same board. No real cutaway occurs. |
| Comparison stays on screen 72.6 s | 2:02.30–3:14.90, the longest uninterrupted board run. Current file DOES zoom and pan through the rows, resolving the old readability complaint. It still needs relevant illustration breaks under Edit Spec 8b. |
| Canonical assets and opening views | Both current JPGs are visually present and feature-matched. Each opens complete and unmarked: approximately 11 s for the Chinese Room and 7.6 s for the comparison. |
| Chinese Room camera-only emphasis | Existing owner-approved treatment: complete callout views, chart detail, person, and pullback. No rings. Preserve this deliberate exception unless the new production plan changes it; do not count the absence of rings as a newly discovered defect. |
| Comparison highlight/camera sequence | Meaning, Experience, Word choice, Beauty, Uncertainty, then banner. Complete paired rows remain visible in inspected settled frames. Dense treatment is appropriate; do not revert to the obsolete compact/full-view-only proposal. |
| Older ring weight | Fresh detector reads approximately 7 solid pixels on settled green row rings, rather than the old manifest's stated 5. Gold detections outside board spans are illustration false positives. Current target is fixed 4 px at 720p. **Explicitly grandfathered for previously shipped videos**; update on the next rebuild, not a standalone failure requiring a rebuild. |
| Supporting pictures | Laptop/hands, head silhouette, eye, phone/server, empty room, gears, server aisle, and speech/lightbulb drawings provide useful variety outside boards. No Notebook photograph or corner mark was apparent in reviewed samples. Course-board photo panels are exempt from the Notebook photograph ban. This is not an exhaustive every-frame clearance. |
| Thin visual bridge | Around 1:36 the board cuts to blank paper before the symbols/prediction graphic develops. Worth replacing with a relevant drawing on a new build; not a narration verdict issue. |
| Close | Canonical close appears from 3:30.4, enlarges and settles; literal final frame 6599 is the correct close, with no black tail. Exact motion-frame compliance was not remeasured. |
| Boundaries | Fresh transition guard passes the five board/close seams at frames 1389, 2876, 3669, 5847, 6312. Overview strips inspected; no stale island apparent. This covers these seams, not all animation or audio transitions. |

## Proposed production plan after narration selection

Timing-dependent choices are provisional because a reroll is recommended. These are proposals, not approved edits or generated artwork. Keep narration natural; do not add silence to make room for camera moves.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| The Chinese Room | Preserve the approved unmarked illustration walk: incoming note → lookup → chart → returned reply → outside impression → person → full view | Full-view introduction; complete callout zooms and chart detail; full view for takeaway | Current 49.6 s. For the next roll, aim for board stretches around 15–20 s, with brief drawn cutaways to the incoming note and returned reply after their callouts have been taught. Exact seconds follow the selected narration. | Preserve the coherent example. Custom drawings should depict the action, not reproduce the board as a new teaching chart. |
| When You Think. What AI Does. | Full view unmarked; one paired-row outline for Meaning, Experience, Word choice, Beauty, Uncertainty; full banner ring on exact takeaway | Retain uniform complete-row zoom/pan and final pullback. Fixed 4 px rings on the rebuilt video | Current 72.6 s. Target uninterrupted board runs around 15–20 s. Provisional cutaways: lived meaning/context, words appearing one at a time, and checking a confident wrong answer. Return before the next row's spoken onset. | Three purpose-built drawings can support the specific ideas; no surviving alternate-roll imagery was identified. Final spans and artwork need review against the selected audio. |
| Sounds human. Works differently. | Unmarked | Standard 48-frame hold, 150-frame push to 1.2×, settled hold at 30 fps | Current 9.6 s; next duration follows the exact two closing lines | Use current canonical close as final frame. |

Also replace the invented-statistics/comprehension graphics near 0:27–0:39 with a simple drawn conversation or the existing phone/server scene where it fits. Reassess the symbols/prediction bridge for readability and relevance. Custom illustration support is now allowed under Edit Spec 8d; lack of a surviving raw drawing does not force us to keep misleading graphics or long holds.

**Selective pauses:** none proposed from transcript evidence alone. Existing transcript gaps do not establish natural audio pacing. Listen to the selected narration before proposing any measured gap changes; no automatic pause insertion.

**Verification still required before any future pass:** actual end-to-end watching/listening, uncertain-word audition, precise new timing and ring-onset checks, every-frame seam inspection at new edits, audio continuity, and final encoded illustration review. No shipping approval is implied by this evaluation.

Evidence: `identity.json`, fresh `does-ai-think/transcript.txt`, `board-spans.txt`, `ring-stroke.txt`, `sheets/`, `detail/`, and `transitions/` in this directory. The saved deployed HTML records the current live reference.
