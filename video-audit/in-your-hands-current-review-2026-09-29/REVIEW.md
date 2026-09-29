# What You Can Control / In Your Hands — current-spec evaluation

Reviewed September 29, 2026. Scope: evaluation only; no video, lesson, prompt, or deployment changed.

**Graphics-policy update:** The subsequent [Notebook graphics reassessment](GRAPHICS-REASSESSMENT.md) applies the revised September 29 rules and supersedes the fixed custom-cutaway plan below. Preserve useful Notebook motion; the prior six-cutaway schedule is provisional, not a production recommendation.

## Assessment

The video teaches the current lesson's essential ideas. The main production weakness is the long, uninterrupted board sequence: **81.5 seconds on What's in Your Hands?, then 51.4 seconds on Three Moves Worth Your Energy**, then the close. The approved column walk improves readability but does not supply the supporting illustrations requested by current Edit Spec 8b.

The spoken close does not match the required wording. This is a known variance in previously approved audio, not a new regression. Under a literal application of today's narration rules the verdict is **REROLL for the exact-wording requirement**, because no complete correct donor closing beat is identified. That formal verdict should not be mistaken for missing lesson teaching or a recommendation to discard useful narration. A visual refresh can preserve the accepted audio, but cannot be called full literal compliance with the current prompt.

This is a transcript-and-frame evaluation, **not an end-to-end audiovisual sign-off**. No fresh audio was heard in this session. Wording, cadence, splice cleanliness, and pause quality therefore remain subject to listening.

## Exact live identity

- Public page checked: https://besmarterthanthetool.com/
- Public `control` entry: `course-assets/in-your-hands/in-your-hands.mp4?v=20260925ship1`.
- Public MP4 streamed for SHA-256 verification; it exactly matches the local reviewed file and the September 25 shipped v4 manifest.
- SHA-256: `da5e5302dc17c0243d3071360e30122e581a19bc52409e20a473899a84fab842`.
- Sequentially decoded: **5,508 frames, 30 fps, 1280×720, 3:03.60**.
- Current lesson: `index.html`, `ControlSection`, and `CLOSE_BOARDS.control`. The upload Markdown agrees with the lesson. All three current canonical JPGs were inspected.
- Complete timestamped transcript read: `video-audit/in-your-hands-live-review-2026-09-25/in-your-hands/transcript.txt`. The shipped v4's audio is unchanged from that reviewed baseline according to its recorded packet comparison; current payload hash is saved in `identity.json` for comparison.

## Findings against today's production spec

| Finding | Evidence | Disposition |
|---|---|---|
| Long board holds | Board 1: 0:35.30–1:56.80, 81.50 s. Board 2: 1:56.80–2:48.20, 51.40 s. Teaching boards run continuously for 132.90 s; including close, 148.30 s. Fresh feature matching confirms the spans to its 0.5 s sampling precision. | Main refresh priority under 8b. The narration is still teaching throughout; this is visual variety, not dead narration. |
| Current board assets | Frames show the current artwork, wording, banners, and website credit. Board 1's current JPG hash also matches the shipped manifest. | Pass in inspected frames. |
| Board openings | Both boards arrive full-view and unmarked. Board 1 remains unmarked until ~0:46.83; board 2 until ~2:02.5. | Pass: exceeds the two-second opening requirement. |
| Column camera | At ~0:46.83 the camera dives to the left white column, pans right at ~1:06.47, and pulls back at ~1:44.83. Illustrations are cropped while zoomed. | **Approved exception**, not an unauthorized defect: David explicitly requested this white-section framing September 25. Preserve it unless a new plan changes it. |
| Ring stroke | Real board-ring samples measure roughly 6 px on left-column rings, 7 px on right-column rings, 4 px on the first banner, and 6 px on detected second-board rings. | Older stroke treatment, heavier than today's fixed 4 px at 720p. Section 5 explicitly exempts already-shipped videos from rebuilding solely for this. Update when those spans are next rebuilt. |
| Ring targeting | Inspected samples show whole-column introductions, then one row at a time; second board uses whole-card rings; banners receive full-width violet outlines. | Preserve sequence and accents. Fresh samples align with the transcript's named targets. Frame-exact audio onset certification was not performed. |
| Second-board readability | Full-resolution frame at 2:02.60 shows all three complete cards and readable text. | Compact; retain full view. Do not add zoom merely to disguise a long hold. |
| Supporting imagery | Opening city/phone crowd and the distorted-face phone drawing are illustrated, not photographic. No new cutaway follows 0:35.3. | Allowed by September 26 people rule. The older review's claim that these drawings are banned because they contain faces is obsolete. Their relevance still governs reuse. |
| Standard visual close | Current closing JPG appears at frame 5046 (2:48.20), remains to literal final frame 5507; sampled frames show initial hold, push, and settle. Existing manifest specifies 48-frame hold, 150-frame push to 1.2×, then 264-frame settle. | Canonical close and final-frame requirement pass visual inspection. Fresh pill-width measurements are in `close-motion.json`; no new outro follows. |
| Pauses/audio | Existing gaps are retained; no fresh listening performed. | No new pauses proposed. Do not infer a pause defect from board boundaries or add automatic one-second gaps. |

The ring detector also labels parts of the opening drawing and purple artwork as hollow shapes (including apparent 10 px detections). Those are **false positives**, excluded from the assessment above. Contact sheets cover every four seconds; selected native-resolution frames include board entrances, settled states, and the final frame. This sampling does not certify every frame or every audio seam.

Current Edit Spec section 5's dated 4 px instruction supersedes stale 5 px wording still present in the shared checklist and section 10. No spec files were edited for this evaluation.

## Narration evaluation

**VERDICT: REROLL under literal current wording requirements; essential teaching is complete.** No complete verified donor repair was located in the available lesson video sources. Previously approved audio remains the starting point for a visual-only refresh; this evaluation does not revoke the historical shipping decision.

| Essential teaching point, in lesson order | Assessment | Transcript evidence |
|---|---|---|
| AI taking jobs: prediction becoming news | RICH | 0:00–0:11: headline introduced and its change explained. |
| Stakes beyond jobs: power, planet, online trust | TAUGHT | 0:13–0:26: all three consequences spoken. The base transcript's “fast planetary resources” was “vast” in the previous medium-model check; not newly auditioned. |
| Uncertain future, even for experts; little individual control | TAUGHT | 0:26–0:36.7: “nobody actually knows,” builders guessing, trajectory outside your control. |
| Ask what is and is not in your hands | RICH | 0:36.7–0:44.4: explicit question followed by the two columns. |
| Cannot control future jobs | TAUGHT | 0:50.2–0:53.4. |
| Cannot control speed of AI change | TAUGHT | 0:53.4–0:56.0. |
| Cannot control volume of machine output | TAUGHT | 0:56.0–0:59.8. |
| Cannot control others' AI use | TAUGHT | 0:59.8–1:03.2. |
| Cannot control next headline | TAUGHT | 1:03.2–1:06.5. |
| Can build depth in a subject you care about | TAUGHT | 1:10.9–1:15.2. |
| Stay curious and keep what works | RICH | 1:15.2–1:25.3: testing tools and keeping consistently useful methods explains the choice. |
| Practice original ideas | RICH | 1:25.3–1:32.0: explicit contrast with outsourcing thinking. |
| Choose AI use and collaboration with people | TAUGHT | 1:32.0–1:38.2: both personal use and collaboration spoken. |
| Make something real instead of waiting | TAUGHT | 1:38.2–1:44.8. |
| Choices matter despite uncertain outcomes | TAUGHT | 1:44.8–1:49.2. |
| Stay informed; spend energy on controllable choices | TAUGHT | 1:49.2–1:55.5. |
| Bridge from agency to practical action | TAUGHT | 1:56.8–2:02.5: right column becomes a “to-do list,” leading to three moves. |
| Go Deep: one tool, strengths, errors, limits, depth over dabbling | RICH | 2:02.5–2:15.6: all components explained. |
| Think First: own view before prompting; AI sharpens thinking | TAUGHT | 2:15.6–2:31.0: order and smarter-versus-answers distinction spoken. |
| Skip the Hype: doomscrolling versus developing a real skill | RICH | 2:31.0–2:43.0: the hour is presented as a concrete choice. |
| Effort where it affects outcomes | TAUGHT | 2:43.0–2:47.1; “guarantees” is an unnecessary stronger wrapper than the lesson uses. |
| Closing agency takeaway | TAUGHT in meaning | 2:51.7–2:58.9: both ideas present; exact wording fails below. |

**Hard requirements and wording:**

- Direct opening, both columns with all five items, all three named moves with instructions, and no sign-off after the close: met in the transcript.
- Closing line 1: required “You can’t control where AI goes next.” Recorded wording: “and you cannot control where **the technology** goes next” at 2:51.7–2:54.7. Not verbatim.
- Closing line 2: required “You can build the skill and judgment to decide what you do next.” Recorded wording begins “but” and adds “the” before judgment at 2:54.7–2:58.9. Meaning intact, but also not literally exact. The earlier report called this near-verbatim; it is not an exact-wording pass.
- Body takeaways also paraphrase requested copy: “Deep expertise beats superficial dabbling” (2:12.4), “mechanical difference … genuinely getting smarter … merely retrieving answers” (2:25.2–2:31.0), and the joined/paraphrased choices and energy lines at 1:44.8–1:55.5. Teaching passes; strict “speak every takeaway as written” does not.
- The extra “cultural conversation … deafening” sentence at 2:48.1–2:51.7 makes the ending wordier. It is optional cleanup, not missing teaching.

**Errors:** no essential teaching contradiction found. “Guarantees” at 2:43 is too absolute relative to the source; avoid it in replacement narration. Formal wording (“framework,” “workflow,” “interrogate,” “mechanical difference”) weakens the intended plain voice but does not erase the explanation.

**Source QA:** PASS for lesson/Markdown/current boards agreement. **Additions worth retaining:** the explanation of testing and keeping useful tools; the contrast with outsourcing all thinking. **Repair plan:** no verified complete donor closing beat. Do not claim that a word splice or changed graphic repairs the spoken requirement. **Listening:** none heard in this session; complete archived transcript read, exact live file identified, prior unchanged-audio provenance checked.

## Proposed visual refresh plan — no build performed

Preserve narration, duration, existing pauses, canonical JPGs, useful opening drawings, and the specifically approved white-column framing. Replace long uninterrupted board holds with drawings tied to the spoken idea. The original two raw lesson rolls are not present in the checked source locations; this plan therefore proposes four custom illustration concepts under new section 8d. These are proposals, not existing assets or verified donors.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| What’s in Your Hands? | Full unmarked introduction; whole left column, then five blue row outlines; whole right column, then five green row outlines; violet banner. Restore the relevant outline after each break. Fixed 4 px on any rebuilt span. | Preserve approved left/right white-column walk and pullback. Return from a drawing to a settled camera before the next named item. | Span 0:35.30–1:56.80. Proposed drawing breaks 0:54.8–0:58.8 (machine output), 1:18.0–1:24.2 (trying and evaluating tools), 1:41.0–1:43.8 (making an original project after its row outline has registered). Board visible ~68.5 s total; longest proposed uninterrupted run ~19.5 s. | Preserve David's September 25 framing exception. Concepts explain scale, testing, and action rather than decorating the board. |
| Three Moves Worth Your Energy | Unmarked intro; whole Go Deep, Think First, Skip the Hype cards at spoken onsets; violet banner. No sentence-by-sentence rings. Fixed 4 px on rebuilt spans. | Compact, full view; no dives. | Span 1:56.80–2:48.20. Proposed breaks 2:09.0–2:14.6 (reuse tool-testing drawing), 2:23.0–2:30.0 (original notes being refined), 2:37.0–2:42.0 (phone set aside for practice). Board visible ~33.8 s; longest proposed run ~12.2 s. | First show each named card and let its outline register; cutaways carry the explanatory continuation. |
| You can’t control where AI goes next. / You can build the skill and judgment to decide what you do next. | Unmarked. | Preserve standard hold/push/settle. | 2:48.20–3:03.60, 15.40 s. | Visual close already uses the current canonical image. Spoken wording is a separate issue. |

Custom concepts: (1) a machine producing many pages, without fabricated quantities; (2) a student trying a tool and checking useful versus flawed results; (3) a student's own notes/project, with a related refinement view for Think First; (4) a phone set aside beside practical work. Match the video's drawn style, minimal text. Reusing concepts should use an appropriate view, not repeat an unrelated loop. The opening distorted-face phone is allowed but poorly matched to constructive skill-building; do not recycle it merely to satisfy a timer.

These editorial times are grounded in transcript beats and must be checked in a visual preview and by listening before assembly. No pause extensions or narration cuts are proposed for the visual-only route. If full literal narration compliance is required, obtain the complete correct closing beat and required takeaways first, then re-time the plan against that audio. No repair joins have been auditioned or certified.

## Evidence and limits

Fresh evidence: `identity.json`, `board-spans.txt/json`, `ring-stroke.txt/json`, `close-motion.json`, `sheets/`, and selected native-resolution `frames/`. Existing evidence: September 25 column-walk manifest/review and September 16 assembly manifest. No new `transition_guard` ship certification was attempted; no edited candidate exists. Video Tracker workflow status was not consulted or changed.

The evaluation is complete within those stated inspection limits. A final ship decision still requires end-to-end viewing/listening and audio seam review; transcript agreement and hashes do not substitute for hearing the file.
