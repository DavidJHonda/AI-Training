# Why Learn AI? — shortened v11

Review candidate: `Prompts/why-learn-ai-v11.mp4`. **2:47.233**, 5,017 frames at 30 fps, 1280 × 720. Shipped locally on owner approval; see SHIP.md. Queued for batch deployment.

The current page removed AI Is Everywhere, now in What is AI?. The existing video can accommodate that change with one continuous cut. The current page remains authoritative; no lesson or board text was changed for this edit.

## Exact cut

Source: verified finished `Prompts/why-learn-ai-v10.mp4`, byte-identical to the installed Why Learn AI? video before this build. SHA-256: `f7cab5a37d9c1f8ae141f1f2bcfadb441dd4341dedad782eb1684b63e9c6bd79`.

Remove source frames **[1197, 3255)**, or **0:39.900–1:48.500**. This removes 2,058 frames, **1:08.600**:

- The complete AI Is Everywhere narration, everyday examples, associated graphics and board, and its takeaway.
- The following context-dependent bridge: “Because you already interact with these systems, you can easily shift from being a passive consumer to an active user.”

Keep frames [0,1197) and [3255,7075). The new join is at output frame 1197 / 0:39.900:

> Run it, or someone else will.
>
> You can start now. Learn what AI does well, notice where it struggles, and practice using it for something you care about.

The outgoing cut is at the exact press-board scene boundary and within silence. The incoming cut is inside the measured 1:48.216–1:48.757 silence before “You can start now.” The active-user illustration remains briefly to support that line, followed by its original transition into the learning-loop graphic. No new pause is inserted, and no voiced material is cut at either edge. Five-millisecond ramps are confined to quiet join edges.

## Preserved lesson progression

1. Scribe/printing-press analogy and AI Is the Press board.
2. You Can Start Now: strengths, limits, meaningful practice and cumulative experience.
3. Desktop publishing: new tools make it possible to create while developing skill; the tool did not replace skill.
4. Why You’ll Thrive in the AI Future: starting at school, faster experimentation, good habits, and the takeaway.
5. This Has Happened Before: steam, electricity, internet, AI's potential, and the current lesson's attributed quotation.
6. Exact current closing: “AI is today’s printing press. Learn to run it.”

The transcript paraphrases the current lesson rather than reading it word for word. The retained school-skills board develops the lesson's point that students can start now. The removed passage is the relocated teaching; the historical section is retained in full.

## Visual plan and execution

| Board | Treatment |
|---|---|
| AI Is the Press | Retain the entire existing board walk and final highlighted banner. Cut before the first AI Is Everywhere graphic. |
| Where AI Already Lives | Remove its entire span and related examples. This board is now in What is AI?. |
| Why You’ll Thrive in the AI Future | Retain existing full-view opening, framing, highlights and supporting feedback illustration. |
| AI is today’s printing press. | Retain the existing canonical close and its motion through the final frame. |

All canonical board hashes match the source build's recorded assets. No board was regenerated. All retained source frames are passed through in order; the only additional visual loss is one encode from the verified finished source. The earlier approved supporting illustrations and historical animation remain.

## Verification

Checks passed: 5,017 decoded frames, continuous 30 fps timestamps, every-frame source comparison (maximum frame MAE 4.125/255), audio correlation 0.999989, and the single new transition gate at the 12-frame visual-island threshold. The 61-frame transition strip was visually inspected. The source and all protected file hashes are unchanged. The encoded gap between the preceding and following speech is about 1.369 seconds; no additional pause was inserted. Browser metadata confirms the intended 167.233-second file, 1280 × 720, with no media error.

The complete fresh transcript was read: it retains “You can start now,” the desktop-publishing explanation, all three reasons to thrive, the historical examples and quotation, and both exact closing lines. The relocated everyday-AI passage and dependent bridge are absent. The transcript spells Mainz as “mines”; this is unchanged source audio, not a new edit.

The actual candidate is checked by `scripts/video/qa_why_learn_ai_v11.py`, with results in `qa.json`. The builder is `scripts/video/cut_why_learn_ai_v11.py`; `edit-manifest.json` records source/candidate hashes, retained frames and protected files. The fresh transcript is in `transcripts/`; join strips and detection results are in `transitions/`.

Direct listening and continuous real-time motion review were not performed. The owner should review the join around 0:40. Technical checks are not represented as a listening pass. This is a review candidate, not a shipping authorization.
