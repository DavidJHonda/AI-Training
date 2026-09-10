# Understand AI opener: versions 3 and 4

Recommendation: **repair version 3**. Both contain the major introductory content and both exact closing lines. Version 3 is the stronger narration source: more direct, less repetitive, and avoids version 4's specific probability error. No new roll is needed to secure missing teaching.

This is raw-source selection, not shipping approval. No videos, lesson text, or generation materials were changed. Current lesson, both complete transcripts, all eight contact sheets, scenes and holds were reviewed. Targeted full-resolution frames and sequentially decoded final frames supplement the sampled record. Speech judgments use full ASR transcripts; the critical version 4 probability wording was checked with a second, larger ASR model. This is not a complete listening/seam QA pass.

## Sources and lesson authority

- `Prompts/understand-opener-3.mp4`: 4,825 decoded frames, 30 fps, **2:40.83**.
- `Prompts/understand-opener-4.mp4`: 5,642 decoded frames, 30 fps, **3:08.07**.
- Hashes and sizes: `sources.json`.
- Lesson: `lessons/Opener-Understand.md`, compared with `index.html` OpenerFoundationsSection.
- Canonical illustration: `illustrations/opener-understand-under-hood-v3.jpg`.
- Canonical roadmap: `illustrations/opener-understand-section-map.jpg` (Notebook upload counterpart `lessons/opener-understand-2-map.jpg`).
- Close: “The machine won’t feel like magic anymore.” / “Take it a piece at a time.”

Source QA passes at introductory scope. Lines 17–31 establish the practical benefit and reassurance; lines 41–49 expressly distinguish learning order from per-message processing. Lines 43–47 introduce later lessons without claiming to teach their mechanics. No lesson rewrite is needed for this intake.

## Narration coverage

| Teaching | Version 3 | Version 4 |
|---|---|---|
| AI is its own kind of thing | 0:00–0:12, direct opening | 0:00–0:14, more abstract |
| Expert / six-year-old contrast | 0:12–0:30 | 0:14–0:36; adds trust commentary |
| Car analogy and practical benefit | 0:40–1:08 | 0:43–1:18; more technical phrasing |
| No memorization; words become answer | 1:08–1:23 | 1:18–1:45; repeats the goal |
| Roadmap is learning order | 1:23–1:35, explicit | 1:45–1:55, explicit, then contradicted |
| Training | 1:35–1:42 | 1:55–2:01 |
| Probability | 1:42–1:51 | 2:01–2:08, followed by faulty elaboration |
| Tokens and numbers | 1:51–2:02 | 2:15–2:23 |
| Context changes meaning/numbers | 2:02–2:11 | 2:23–2:31 |
| Answer construction, variation, math | 2:11–2:22 | 2:31–2:40 |
| Each topic builds on previous | 2:22–2:27 | 2:49–2:53, incorrectly calls it a process |
| Both exact closing lines | 2:34–2:38 | 3:01–3:05 |

## Version 3: recommended repair

The narration stays at opener depth. “How words become numbers” receives an explanation rather than just a title, as do the other four topics. It does not need added technical material.

Suggested narration cuts, approximate source times (not edit-ready splice boundaries):

1. **0:30–0:34.5:** remove “The only way to make sense of that contradiction is to look inside the machine.” The following sentence supplies the useful point without “the only way.”
2. **2:26.7–2:33.8:** remove the repeated summary beginning “By the end of these five steps…” The preceding sentence already closes the roadmap clearly as course topics, and this cut avoids reintroducing the ambiguous word “steps.”
3. Keep the car analogy and practical benefit. “Ensuring you remain smarter” at 1:02–1:08 is stronger than the approved “helps,” but is motivational framing rather than a new technical mechanism. Do not manufacture awkward single-word repairs just to polish it.

Visual plan:

- Preserve useful Notebook illustrations throughout the opening and transitions. The first 8.5 seconds alternate nearby server-corridor framings; `adjacent/opening-frames.jpg` verifies actual frame changes. Smooth this using one of its own clean frames and a restrained camera move if distracting. The automatic 225-cut count is not 225 editorial scenes.
- 0:20–0:25.6: the laptop has mirrored “ERROR” lettering, confirmed in adjacent frames. A small graphic repair or replacement illustration can clean it up; no new course board is needed.
- Start the car example with the original driving visual (0:39.33–0:45.43), then use the approved Under the Hood illustration for the relevant explanation. Do not replace the entire opener with static boards.
- 1:23–2:26.6: replace the engine-treated roadmap with the current asset and course outlines. Its pan resolves much of the apparent clipping, but crops the first/last rows at different times and does not follow the required full-section treatment. Native arrows and filled takeaway highlighting are disposable post-production material, not reasons to reject this roll.
- Insert measured one-second pauses at major idea boundaries, not after every sentence.
- 2:33.73 onward: insert the exact standard course close under the existing correct narration and remove the engine end card starting at 2:37.83.

Expected result: roughly 2½ minutes after cuts and pauses. Final duration depends on clean speech boundaries. Build from the pristine source with a new review filename; perform normal audio, frame-boundary, and final-close verification before shipping.

## Version 4: usable fallback, weaker choice

At **2:08–2:15** it says the first two steps establish the knowledge and probabilities AI relies on before receiving the input. This confuses training with the next-token probabilities computed from the current input/context. Hugging Face's [text-generation documentation](https://huggingface.co/docs/transformers/llm_tutorial) describes prediction conditioned on the prompt and generated text. This added sentence is removable; the accurate probability introduction at 2:01–2:08 survives. It does not require regenerating all narration.

Additional issues:

- 0:27–0:43 adds abstract trust/“mechanics” commentary. 1:18–1:45 repeats reassurance and goal. This is less welcoming than the source and delays the roadmap.
- 2:31–2:36 repeats “how AI builds an answer” consecutively.
- 2:40–2:53 turns the roadmap back into a data-to-response process, despite its correct earlier disclaimer. Cut this elaboration if using version 4.
- 0:35–1:10 introduces token/attention diagrams and a “5-Stage Processing Roadmap”; 1:18–1:39 invents further operational-flow diagrams. These are unnecessary for this opener and partly misrepresent the roadmap as architecture.
- 2:53.37–3:00.57 shows the prompt passing through “Training,” then tokens/probability/context/synthesis. This is a substantive visual error, not just style. Replace if harvesting the narration.
- Engine-generated map emphasis and close need the normal replacements. No score penalty for native highlight styling in a raw roll.

There is no essential narration in version 4 that version 3 lacks, so a mixed-voice composite is not justified. The clean illustrations of confusion (0:27.03–0:35.43) and confident use (1:09.83–1:17.60) are possible visual donors; nothing requires them.

## Independent dimension scores

No combined totals; narration selection takes precedence over visual polish.

| Dimension | Version 3 | Version 4 |
|---|---|---|
| Teaching coverage /20 | 20: all required beats above; missing a topic explanation would cost credit | 20: all beats present despite added erroneous commentary; omissions would cost credit |
| Lesson material /15 | 14: “only way” at 0:30 and inflated car diagnosis language at 0:45 depart from the gentler practical benefit | 11: 2:08 and 2:40 additions distort the learning map; interface/mechanics detour at 0:35–1:10 |
| Teaches vs recites /15 | 14: analogy explains the benefit; roadmap stays appropriately introductory, though 1:42–2:11 is formally phrased | 12: accurate individual map explanations are undermined by the faulty connection at 2:08–2:15 |
| Board content /10 | 10: both boards' teaching is spoken; missing the analogy benefit or any roadmap explanation would cost credit | 9: board items taught, but “each piece of this process” at 2:49 changes the takeaway's referent |
| Cleanliness /20 | 18: persistent reversed ERROR at 0:20–0:25.6; map edge cropping at 1:30/2:00 (later pan resolves omitted rows) | 17: cramped overflowing diagram header at 1:06; map edge crops at 2:28; small invented technical labels at 0:40/2:59. Builds/dissolves not penalized |
| Pacing /20 | 18: redundant wrap-up 2:27–2:34 and restatement 0:30–0:40 | 15: repeated reassurance/goal 1:18–1:45 and duplicate wrap-up 2:40–3:01; not a runtime penalty |

## Gates and limitations

| Gate | Version 3 | Version 4 |
|---|---|---|
| Source QA | PASS | PASS |
| Accuracy | PASS at opener scope; remove overstatement as above | FAIL raw: 2:08–2:15 and operational diagrams |
| Substitute | PASS narration | FAIL raw: contradictory explanation despite full coverage |
| Spine | PASS; both exact closing lines | PASS; both exact closing lines |
| Restraint | PASS in inspected evidence | PASS in inspected evidence |
| Stock/watermarks | FAIL ship: Gemini corner mark and end card; no Getty seen | FAIL ship: Gemini corner mark and end card; no Getty seen |
| Ending | FAIL: literal final frame is engine end card | FAIL: same |
| Sync | Topic alignment generally passes; map crops need repair | FAIL: operational diagrams conflict with spoken roadmap distinction |
| Board walk | FAIL ship: current assets and proper outlines required | FAIL ship: same |
| No Notebook highlight | Expected raw material; not intake deduction | Expected raw material; not intake deduction |
| Standard close | FAIL ship: not inserted yet | FAIL ship: not inserted yet |
| Edit integrity | Not certified: raw roll, no repair seams created or reviewed | Not certified: same |

All eight contact sheets and the final frames were reviewed. No long hold was deducted merely for being static: the roadmap stays on screen while it is being taught. The 4-second sheets do not establish a full-frame shipping certification. Version 3 opening rapid reframings and version 4's dissolving diagrams were checked with adjacent frames rather than treated as unexplained corruption.
