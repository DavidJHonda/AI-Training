# Work With AI opener — current-spec evaluation, September 29, 2026

**Verdict: REROLL pending a verified narration repair.** Keep the useful camera example and board/drawing alternation. The course-linked version misses required spoken language and makes three guarantees the lesson does not support. Visual work alone cannot resolve that.

Scope: evaluation only. No video, lesson, prompt, or course reference changed. Evaluated the local file selected by `LESSON_VIDEOS.openerworkwith`, `course-assets/work-with-ai-opener/work-with-ai-opener.mp4?v=20260921ship14`: **2:37.900, 4,737 decoded frames, 1280×720, 30 fps**, SHA-256 `48c90ec931943f0a98464aafe74d5b99c3ff7967db9d4b0af16bde6f146ac4ed`. This matches the September 21 v8 release record. Public deployment and tracker status were not checked.

Applied the current working copies of `scripts/video/README.md`, `EDIT-SPEC.md` and `NARRATION-REVIEW.md`, including September 29's instruction to preserve useful animations. Section 5's fixed 4 px at 720p supersedes residual 5 px checklist language. Current page content is at `index.html`'s `OpenerWorkWithSection`, plus `CLOSE_BOARDS` and its four canonical JPGs.

## Priority findings

1. **0:00–0:18: restore the four opening lines.** The video says “Take a look at these four principles,” then paraphrases Aim / Check / Work with it / multiplies your thinking. It never speaks the four required lines as written. The abstract “Your logic provides the foundation, which AI scales up and amplifies” is a weaker entrance for a sixteen-year-old.
2. **1:51.38–1:55.40: remove the guarantee.** “By providing the right details, you force a better outcome from the model.” Required replacement: **“Giving AI the right details helps it give you a better answer.”**
3. **2:16.32–2:19.58: judgment is not a guarantee either.** “Your judgment ensures that the result is both accurate and useful.” The page asks the learner to question, verify, and decide whether the answer is good enough. A replacement generation should say that directly. A possible later edit is to remove this whole sentence, provided listening confirms the preceding judgment beat still connects naturally to the takeaway; this is not a verified cut proposal.
4. **2:20.46–2:25.60: restore the map takeaway.** “The final result depends entirely on how you apply the tool” overstates user control. Required wording: **“The result depends on how you use the tool.”**
5. **Around 1:52–1:56: the context graphic reinforces the wrong claim.** Its revealed output is labeled **“VERIFIED OUTCOME”** and **“Precision Density: 99.4%”** despite showing context entering a model, not any checking of its output. The issue is the implied verified precision, not simply the presence of illustrative numbers. First try a targeted label repair: “BETTER-FOCUSED DRAFT” and removal of the precision claim, preserving the useful input/detail arrows and reveal. If that cannot be done cleanly, propose a supporting drawing of a clearer draft still awaiting checking. See `frames/03405.jpg`. This recommendation is based on sequential sampled states and the complete narration transcript; motion with audio remains unreviewed.
6. **2:30.68: check the exact close by ear.** Fresh ASR again reports “AI doesn’t replace your thinking” instead of “It doesn’t replace your thinking.” Meaning is intact; exact wording is an unresolved listening check. It does not drive the verdict by itself.

**Repair history matters.** The September 26 reroll plan explicitly records that v9 and v10's external-voice inserts were rejected for voice mismatch. Do not revive them as approved repair sources. The retained transcripts for `Prompts/opener-work-1.mp4` and `opener-work-2.mp4` also paraphrase the opening and close; neither supplies a complete remedy to all failed requirements. No accepted, auditioned donor resolves this file today. The prepared Notebook reroll prompt already requests the correct opening, details sentence, qualified takeaway, both closing lines, one narrator, and avoidance of all three guarantees. A new roll can provide repair passages or become the new base after comparison; the useful existing video need not be discarded wholesale.

## Teaching coverage

Quotes and times are fresh ASR output, not independently heard speech.

| Essential point, in lesson order | Assessment | Evidence |
|---|---|---|
| Aim your request | TAUGHT meaning; exact line MISSING | 0:06, “You aim your requests.” |
| Check instead of copying | TAUGHT meaning; exact line MISSING | 0:06–0:08, “you verify the output.” |
| Work with AI rather than merely use it | TAUGHT meaning; exact opening line MISSING | 0:08.78–0:09.98, “treat it as a collaboration.” |
| AI multiplies thinking rather than replacing it | TAUGHT overall; exact opening line MISSING | Foundation/amplification at 0:13–0:18; explicit nonreplacement at the close. |
| Move from knowing the tool to practical use | TAUGHT | 0:18.92–0:25.10. Formal wording, but the bridge is spoken. |
| Same AI can produce different results | RICH | 0:26.22–0:33.76. |
| Identical cameras, same sandwich, rushed blurry versus carefully framed crisp photo; unchanged tool | RICH | 0:34.40–0:48.74. The comparison preserves the page's meaning. The absence of “photographer’s cover shot” is not an essential teaching failure; retain the stronger concrete sandwich explanation. |
| Apply that relationship to working with AI | TAUGHT | 0:49.48–0:57.60. “Mastering the mechanics” is unnecessarily formal; an optional language improvement beyond the concrete guarantee corrections. |
| Introduce a three-part section map | TAUGHT | 0:59.20–1:04.24. The organizational bridge is clear. |
| Know What It’s For: different from ordinary software, suitable work, pick and learn an app | TAUGHT | 1:05–1:27.04, all three elements covered. |
| Use It Well: better-answer moves and what the model reads | TAUGHT | 1:27.68–1:50.72. “Model perception” is less accessible than the page, but the explanation follows. |
| Details help rather than guarantee the outcome | WRONG qualification | 1:51.38–1:55.40, “force a better outcome.” |
| Think Before You Trust: question, verify, decide whether good enough | TAUGHT core; WRONG guarantee appended | 1:56.22–2:19.58. Questioning and deciding are explicit; verification was introduced at 0:06–0:08. The later assurance of accuracy needs removal or replacement. |
| Qualified map takeaway | WRONG qualification; exact line MISSING | 2:20.46–2:25.60, “depends entirely.” |
| Close line 1 | MET in transcript | 2:27.20–2:29.72, “Don’t just use AI. Work with it.” |
| Close line 2 | TAUGHT meaning; exact wording unresolved | 2:30.68–2:33.68, ASR “AI doesn’t…” rather than “It doesn’t…”. |

The arc is coherent: principles → practical use → same-tool example → section map → action. Preserve those connections. Formal vocabulary is a tone weakness, not a separate missing teaching point. No additional factual research is needed for these findings: they concern internal contradictions and unqualified guarantees, not external statistics.

**Source QA: PASS for the lesson's teaching.** Current Markdown covers the page's essential content and includes the approved details sentence. Its face-free Same Tool image is an upload stand-in; the final course asset contains the students. No source text change is needed for this evaluation. Accurate useful addition: the explicit same-sandwich comparison.

## Visual results and proposed board plan

**The visual rhythm works.** Fresh half-second matching reproduces the previous measured maximum: **19.5 s for one content board**, **21 s across adjacent content boards** at approximately 0:47–1:08. No additional drawing break is required under section 8b. Two low-confidence section-map matches at 0:22.5 and 0:39.5 are false positives: the inspected frames show the technical diagram and camera drawing, respectively. Do not include them in the board total.

Current opening and map are readable at full view. The map needs no dives. The Same Tool image has a deliberately approved comparison zoom; retain that useful unusual treatment rather than imposing a new camera move. Its photographed course imagery is covered by the canonical-page-asset exemption in section 8c.

This is a provisional plan for whichever narration is eventually selected, not a build. The displayed intervals are current-source timings; audio replacements will change them.

| Board | Highlighting | Camera | Current on-screen time / breaks | Proposed treatment |
|---|---|---|---|---|
| What Makes AI Use Good? | Four lines in spoken order, one tight gold `#f2cf5b` outline at a time | Compact, full view, unmarked arrival | 0:00–0:19.233, 19.233 s | Rebuild against restored lines. Existing outlines extend almost across the navy panel instead of hugging each line. Use tight bounds and 4 px on-screen stroke. No pause added to create an opening hold. |
| Same Tool. Different Results. | Unmarked | Preserve approved full opening → comparison detail → full return | 0:47–0:59.30, 12.30 s | Keep the canonical image and useful walk. The approved focus on the two photo outcomes is an illustration treatment, not a text-card dive. No new rings or cutaway needed. |
| Work With AI | Whole first row purple, second blue, third teal; full-width takeaway violet | Compact, complete board at each return; no dives | 0:59.30–1:07.567; 1:27.733–1:40.133; 1:56.30–2:08.833; 2:20.467–2:26.133. Existing animated wipe tails can extend matching beyond these edit boundaries. | Preserve row/drawing alternation. Whole-row rings are sufficient: these are short overview descriptions. Update to 4 px only on rebuilt spans and align to selected narration. |
| Don’t just use AI. Work with it. | Unmarked | Canonical close; 48-frame hold, 150-frame push to 1.2×, settled hold | 2:26.133–2:37.900, 11.767 s | Preserve current compliant visual if audio permits; retime hold only if the accepted close needs it. |

Fresh ring measurements are generally **6–7 px**; the 1.5 px detection at 1:53.5 is Notebook graphic emphasis, not a course ring. Section 5 explicitly grandfathers older shipped stroke widths. They are an update during a rebuild, not grounds for a standalone rebuild. The opening's broad line bounds should also be corrected when the required narration replacement is made.

Close verification: current canonical asset hash agrees with the release record; correct two lines, white-background treatment, literal final frame. Pill width measures 721 px during the opening hold and 865 px after the push, a **1.200×** ratio. The settled size persists to frame 4736. No close redesign is proposed.

### Supporting scenes

- **0:26.47–0:47:** retain the Same Tool title and drawn camera/sandwich comparison; these establish the contrast before the course illustration. Title-only duration can be shortened if the new narration supports it, but this is optional pacing polish.
- **1:07.57–1:27.73:** retain the software contrast, pattern illustration, and app-selection sequence provisionally; they support the three parts of Know What It’s For. Check their complete motion and small labels during the candidate pass, rather than replacing them just because they are Notebook graphics.
- **1:40.13–1:56.30:** retain the prompt-detail reveal with the targeted output-label repair described above. Context should improve an answer, not certify it.
- **2:08.83–2:20.47:** retain the evaluation/checking sequence provisionally. Its draft → checks → usable output progression supports the lesson. Correct the accompanying narration's guarantee; inspect the moving gold emphasis that overlaps “Domain Accuracy” for readability (`frames/04140.jpg`).
- **0:19.23–0:26.47:** the Temperature / Context Window / System Prompt controls introduce unexplained mechanics. The already prepared narration plan removes this bridge. Follow that plan with the new opening/transition, instead of inventing a new technical lesson or decorative replacement.

No new custom illustration is needed if the context labels can be repaired cleanly. No new pauses proposed. Natural gaps and approved earlier cuts remain the baseline; any later graft must be auditioned and measured before a concrete join plan is called verified.

## Checks and limits

Fresh checks: source hash; full sequential decode; complete fresh timestamped ASR; half-second board and ring measurements; visual contact sheets every two seconds across the file; selected full-resolution frames; close geometry; automated transition guard at eleven declared inherited visual boundaries. All eleven pass; the overview strips show no obvious stale-picture flash. This is not an every-frame manual certification of all boundaries.

**Not performed: end-to-end audiovisual playback, listening to cadence/voice/joins, full animation review in motion with narration, every-frame visual inspection, or fresh word-level alignment of all highlights.** This environment provided no audio-listening tool. Accordingly this is a transcript-and-frame spec evaluation, not shipping clearance. Do not treat ASR or signal measurements as auditioning. The current file already fails on the clearly missing opening and the guarantee wording regardless of the unresolved small close-word difference.

No tracker rows were drafted or posted. v10 was separately transcribed during source identification; its transcript is retained as evidence only, and its rejection remains governing. This task does not reopen it for acceptance.

Evidence: `verification.json`, `transcripts/work-with-ai-opener.txt`, `board-spans.txt`, `ring-stroke.txt`, `contact-1.jpg` through `contact-4.jpg`, `frames/`, `close-measurements.json`, and `guard/transition-guard.md`. Earlier decisions: `../work-with-ai-opener-notebook-reroll-2026-09-26/PLAN.md`, `../opener-work-illustration-sync-2026-09-21/REVIEW.md`, and `../opener-work-repair-2026-09-16/REVIEW.md`.
