# Your Choices — current installed video evaluation

Date: 2026-09-30. Scope: evaluation only; no video, lesson, or release changes.

Candidate: `course-assets/your-choices/your-choices.mp4`, selected from the `choosemodel` entry in `index.html` (cache key `20260926ship1`). Duration 2:42.10; 1280×720; 30 fps; 4,863 sequentially decoded frames. SHA-256: `af2477837d7f525f9be897e721a021478355f3cd647e82265b229c0bcd974411`.

Grounding: current `ChoosingModelSection` in `index.html`, the two canonical board JPGs and closing JPG, `lessons/your-choices.md`, and the current generation prompt. The interactive lab remains a separate page activity; this evaluation covers the video overview specified by its generation materials. The tracker and public deployment were not checked.

## Assessment

The music-app hook and individual explanations of app, model, reasoning, and research work well. The main weakness is the opening: it turns a lesson about understanding available choices into a claim about configuring four controls to ensure a correct result. It omits the reassurance that a student need not see all those controls. The elaborate settings diagram reinforces that problem.

**Recommendation: targeted repair, with audio feasibility still provisional.** The installed narration does not meet KEEP. Both existing source recordings contain the missing reassurance, and roll 1 contains the exact app-and-subscription sentence. There is enough identified wording to investigate a repair before requesting a reroll. Under the narration-review rules this is not yet a verified REPAIR verdict: the proposed joins have not been auditioned.

## Teaching coverage

Times below are approximate segment timestamps from a fresh transcription of the exact installed file, not precise edit boundaries.

| Essential point, in lesson order | Assessment | Evidence |
|---|---|---|
| Music-app analogy | RICH | 0:00–0:09: Spotify, Apple Music, pick an app and start listening. |
| AI starts with choosing an app | TAUGHT | 0:09–0:13: “Using AI starts the same way, you pick an app.” Naming ChatGPT/Gemini is omitted, but the concept is clear. |
| Availability depends on both app and subscription | THIN | 0:13–0:18 says only “depending on your subscription.” Later “some apps” partly qualifies model choice but does not supply the complete framing. |
| Name the four choices | TAUGHT | 0:18–0:25 names app, model, reasoning, and deeper research. |
| Not every choice must be made every time | TAUGHT | 0:25–0:28: “You won't make all four choices every time.” |
| Default is a good starting point | TAUGHT | 0:28–0:35: “The default settings are a solid starting point for most jobs.” |
| Harder/important work: know which thing to change | WRONG | 0:35–0:40 substitutes “ensures you get the right result” for “lets you change the right thing.” Choosing settings is presented as a guarantee. |
| App is first; other controls may not appear | THIN | Choices are ordered correctly, but “up to four” does not clearly explain that controls themselves may be absent. |
| No need to see every choice; understand each when it appears | MISSING | Neither sentence nor an equivalent explanation occurs in the full transcript. |
| App as home base | TAUGHT | 0:46–0:50. |
| Choose an available app fitting tools and work | RICH | 0:50–0:56 explains availability and workflow fit. |
| Use a second app when its strengths fit better | RICH | 0:56–1:03 explains the exception to staying with the home base. |
| Model choice happens inside an app; families of models | TAUGHT | 1:03–1:16. “Subset of options” adds unnecessary abstraction. |
| Everyday model versus more capable model for difficult work | RICH | 1:16–1:33 includes the split and a reason to match capability to the task. |
| Reasoning labels: Effort, Thinking, Reasoning | TAUGHT | 1:40–1:47, all three spoken. |
| More reasoning for math, code, planning, multistep work | RICH | 1:47–1:54 names all four applications. |
| Default reasoning for routine work | TAUGHT | 1:54–2:02; the added “bypasses those deep logical steps” claim is not supported by the lesson and should be omitted from a new narration. |
| Research may be called Deep Research | TAUGHT | 2:02–2:08. |
| Search, compare sources, return a cited report | RICH | 2:08–2:16 supplies all three parts. |
| Broad/current questions needing many sources | TAUGHT | 2:16–2:23; “strictly require synthesized information” is more formal than the lesson needs. |
| Closing takeaway and action | TAUGHT | 2:30–2:38: both canonical closing lines, in order, with no subsequent speech in the transcript. |

Hard requirements from the current prompt: complete app-and-subscription sentence MISSED; “You won’t make all four choices every time” MET; see-every-choice pair MISSED; both closing lines MET in transcription. These labels do not certify pronunciation or cadence.

Source QA: the overview prose, upload Markdown, and canonical boards agree on the central teaching. No material contradiction was found within those sources. This was not an external fact-check of current product controls or the separate lab’s account-specific claims.

Additions: the explanation of matching model capability to task difficulty is useful. The configuration jargon, guarantee of a correct result, and categorical account of what the default reasoning setting bypasses should not be carried into a new generation.

## Visual and editorial findings

1. **0:11.63–0:40.60 — correct the opening diagram.** Its staged states show “Tier Locked,” “Requires Subscription,” “Auto (Locked),” and “Off (Locked),” then “Complex & High-Impact Work: Full 4-Parameter Tuning.” The final configuration becomes “Custom Agent / Frontier Tier / Deep Logic + Code / Deep Synthesis.” These are invented categories and restrictions absent from the lesson. More seriously, the visual suggests escalating all four settings rather than changing the appropriate available choice. Preserve the four-choice reveal concept if it can be relabeled and retimed coherently; otherwise replace this specific scene with a simple supporting diagram. Its 29-second span is not automatically dead time: the diagram changes during the narration.
2. **1:10.93–1:15.57 — revise the model-picker labels.** “Standard 1.5,” “Advanced Ultra,” and “Compact Flash” look like product names. Use generic everyday/more-capable labels in a future production pass, preserving the useful idea of alternatives inside one app.
3. **2:23.63–end — refresh the close in a full production pass.** The takeaway appears while the four-choice recap is still being spoken. The encoded close also has a pale colored canvas rather than the current prescribed white background. Use the exact canonical JPG and standard hold/push/settle treatment, beginning with its matching narration. The literal final frame does contain the correct closing words.

The current boards are readable at 1280×720 and the sampled whole-card rings guide the discussion sensibly. The longest uninterrupted teaching-board span is about 18.4 seconds, while the model explanation is continuing; it is not a reason to cut useful teaching. Old ring thickness alone does not require rebuilding a previously shipped file; a new build uses the current fixed 4-pixel rule.

## Proposed production plan

Timing is provisional until the narration source is selected. Existing spans below show the intended visual structure, not approved cut points. No build has been performed.

| Board | Highlight sequence | Camera | Current screen time / proposed breaks | Reason |
|---|---|---|---|---|
| Choose the Tool | Unmarked opening; whole Which App? card at its spoken onset; replace with whole Which Model? card at its onset | Full board; compact, no card dives | Currently 0:43.07–1:33.97, about 40.3 seconds visible after cutaways. Retain app-tool illustration at 0:49.63–0:55.60 and a corrected model-choice scene at 1:10.93–1:15.57. | Each card teaches one connected choice; section rings would fragment short explanations. Introduce the board with its actual spoken setup. |
| Choose How It Works | Unmarked opening; whole Reasoning card, then whole Research card | Full board; compact, no card dives | Currently 1:33.97–2:23.63, about 31.9 seconds visible. Retain reasoning/routine break at 1:47.63–1:58.30 and source-to-report graphic at 2:08.37–2:15.50. | Contrasts when to spend more effort with when to keep defaults, then shows what research does. |
| The choices behind the answer shape it. | Unmarked | Canonical white canvas; 48-frame hold, 150-frame push to 1.2×, settled hold | Current closing scene starts 2:23.63, preceding its narration around 2:30. Align a rebuilt close to the actual closing words. | Preserve exact wording and stop on the lesson takeaway. |

Supporting visuals provisionally worth retaining: music-app drawing at 0:00–0:06.07 (concrete opening analogy); four dials at 0:40.60–0:43.07 (orientation); app toolbar at 0:49.63–0:55.60 (tool/workflow fit); advanced-work reasoning graphic at 1:47.63–1:54.50 and routine checklist at 1:54.50–1:58.30 (contrast); sources feeding a cited report at 2:08.37–2:15.50 (research process). Preservation of their motion remains subject to a normal-speed audiovisual review.

Narration proposal: restore the source lesson’s complete opening, including app/subscription availability, controls that may not appear, and the see-every-choice reassurance. Replace the guarantee with roll 2’s accurate “allows you to change the right parameter.” Keep the four substantive explanations and exact closing lines. Also propose removing only the added clause “which bypasses those deep logical steps for a faster response” at approximately 1:58–2:02 of the installed file, retaining the preceding instruction to keep defaults for routine work. Exact silence boundaries need to be measured before an edit. No audio graft is approved or certified by this evaluation. Do not prescribe new pauses from a transcript; no pause additions proposed.

## Existing-audio repair investigation

The full transcripts of `Prompts/your-choices-1.mp4` (3:30.43) and `Prompts/your-choices-2.mp4` were read to look for donor wording. This is a focused donor search, not a complete visual or listening evaluation of those recordings.

| Failed beat in installed video | Roll 1 evidence | Roll 2 evidence | Proposed selection |
|---|---|---|---|
| Both app and subscription determine availability | 0:15–0:24: “But depending on the app and your subscription, you may also be able to choose the model, how much reasoning it uses, and whether it performs deeper research.” | 0:11.56–0:19.24 mentions app but omits subscription. | Roll 1, complete sentence. |
| Understanding choices helps you change the appropriate thing, without guaranteeing an answer | 0:34–0:40 still overstates certainty: “gives you the exact capability you need to solve the problem.” | 0:24.84–0:32.32: “But when the work is difficult or the results are critical, knowing these choices allows you to change the right parameter.” | Roll 2, complete two-clause sentence. |
| Controls may not appear; understand them when they do | 0:40–0:55 includes the reassurance but says availability depends “entirely” on the platform. | 0:32.32–0:45.76: “Your first choice is always the app. The remaining three choices are conditional and may only appear depending on your setup. You do not need to see every choice. You need to understand what each one does when it appears.” | Roll 2, whole explanatory passage. |

Concrete opening assembly to audition, replacing approximately 0:00–0:40.60 of the installed file:

1. Roll 2, approximately 0:00–0:11.56: music-app hook through “Pick a foundational app like ChatGPT or Gemini.”
2. Roll 1, approximately 0:15–0:24: complete app/subscription/model/reasoning/research sentence quoted above.
3. Roll 2, approximately 0:19.24–0:45.76: “You won’t make all four choices every time,” default guidance, harder-work guidance, conditional availability, and both reassurance sentences.
4. Resume installed video around 0:40.60: “Let’s look at the first two configuration choices…” and continue its stronger, complete board explanations.

This is about 47 seconds of opening narration in place of about 41 seconds. It uses whole sentences, preserves the narrative progression, avoids roll 1’s guarantee, and preserves the installed version’s default-reasoning instruction (which roll 2 omits). Voice continuity, exact word boundaries, and cadence are unverified. Use corrected supporting opening visuals; do not lay the opening under a board it has not yet introduced. A failed audition may change the donor choice or require a reroll. No assembled audio preview was produced.

## Verification limits

Completed: fresh full-file ASR transcript; current page and all three canonical assets inspected; sequential full video decode; 4-second contact sheets across the runtime; selected full-resolution frames including the literal final frame; hash and course-reference verification. The hash matches the September 26 installed candidate, so the later cutaways did not supply a new narration.

Not completed: human-equivalent listening, normal-speed end-to-end audiovisual playback, audio seam audition, or frame-by-frame animation review. Contact sheets are not proof that motion or joins work. The findings above concern demonstrable transcript coverage and visible content; this is not a shipping certification.
