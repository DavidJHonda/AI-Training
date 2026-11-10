# How AI Answers — preserving useful animation

Version 2 remains the preferred base. Revise the visual plan to preserve the moving explanation of generation, with targeted corrections. Boards serve the recap, comparison, and probability reading; animation shows the handoffs and changes.

**Build follow-up:** the user approved building this plan. The resulting review candidate is `Prompts/how-ai-answers-v19.mp4`; see [the build record](../how-ai-answers-motion-v19-2026-11-10/REVIEW.md) for implemented treatments, exact timing, verification, and listening limitations. The proposal below is retained as the pre-build record.

## Evidence and limits

Follow-up inspection used sequentially decoded frames at one-second intervals for 0:53–1:09, 1:48–2:09, and 2:51–3:11, plus two-second opening samples. Contact sheets are in `motion/`. Frames were aligned with the existing word-timestamp transcript. This establishes visible states, progression, and approximate timing; it is not uninterrupted playback or perceptual listening. Smoothness and audio joins still require playback. All times below refer to the unedited source.

No video, narration, lesson, or prep asset was changed. This is the revised editing proposal, not a finished edit.

## Specific decisions

### Opening: retain the illustration and word-token reveal; repair the placeholder

At 0:00–0:04, the dog and question-mark drawing provides a friendly opening. Around 0:06–0:10, the prompt appears and points to a box labeled FIRST TOKEN containing a question mark. That mark is presumably an unknown-answer placeholder, but this lesson also uses the literal question-mark token. The ambiguity matters here.

Keep the scene progression. Replace the right-hand box content with an empty answer slot and label it “First answer token.” Remove the small “Combined contextual meaning integrated” caption. Keep the dog question readable. At approximately 0:13–0:16, preserve the reveal of its separate word/punctuation tiles; simplify the heading to “Tokens” and remove the T1–T8 sublabels. No extra title board or narration is needed.

### Layers and first prediction: distinguish two separate scenes

The closer inspection reveals two independent animations where the initial overview was too coarse:

- **0:55–1:03:** a layer diagram using “Explain quantum physics simply ?”. Its final vector assigns individual dimensions labels such as “Intent: Explain,” “Topic: Quantum,” and “Full Request Summary,” then says it encodes the entire request. It also labels specific layers as embeddings, attention, and synthesis. The motion communicates updating, but the extra example and literal semantic labels add conceptual problems. Let this scene go with the proposed redundant narration cut. Do not replace it with another still or extend the preceding board to fill the removed time.
- **1:04–1:09:** a different, simpler animation shows the updated vector moving toward next-token choices. It uses “Tell me a story” and Once/There/In/A with 72/16/8/4. **Keep this visual action, adapted to the dog example.** Show the full dog question, emphasize its final question mark, and carry its vector representation toward a panel labeled “Possible next tokens.” Reveal You/A/Great as the transition into the existing probability scene; show the approved percentages in that following scene. This bridge has only about 4.5 seconds of narration, so use one handoff, no extra layer sequence or numerical explanation.

The second scene needs a short animated reconstruction because changing four input tiles to eight and replacing the output panel is more than a clean text patch. Preserve its explanatory movement rather than substituting a still board. The values and labels in the raw animation are not approved lesson data.

### Growing reply: retain and retime the animation

The sequence around 1:48–2:09 is the strongest animation to preserve. You is followed by could, name, and him; emphasis transfers to the latest token, and a vector box follows beneath it. This makes the changing last token visible.

Keep the retained narration at 1:53.40–2:08.14 and use the existing animation with these repairs:

- Replace “AUTOREGRESSIVE GENERATION LOOP” with “Building the answer.” Remove “INFERENCE: 1 TOKEN AHEAD.”
- Keep the original dog question visible above the growing reply. Label the token row “AI’s Answer,” not the full context sequence; context includes the question too.
- Label the moving box “Updated vector.” Keep its changing-number treatment as a schematic, without adding semantic labels for individual dimensions.
- Retime the additions to their spoken words. ASR places “could” at 1:59.72, “name” at 2:02.04, and “him” at 2:03.32. Sampled frames already show could at 1:58 and name at 2:01, while him is still appearing at 2:04. These are provisional timing anchors pending listening.
- Finish with the question and full reply-so-far visible together as “Each added token becomes part of the context” is spoken. Remove the “accumulated context” label that only quotes the reply.

The subsequent extra-name chart and generic loop can disappear with the proposed 2:08.82–2:22.14 narration cut. They are separate scenes; removing them does not require discarding this useful token animation.

### Period and stopping: preserve the two-stage action

At 2:53–2:57, the word tiles gain a period. At 2:59–3:01, a separate EOS tile appears and the sequence stops. Preserve that distinction and movement.

Mask/remove the lower probability panel throughout this sequence. It adds unrequested 84% punctuation and 92% EOS distributions. Simplify the upper labels, remove t= indices, and label the stopping signal “End-of-answer token” while it is being explained. Visually separate that signal from the text of the answer. After completion, leave only “You could name him Spot.”; remove the signal, extra status banners, lower panel, and stray red bar before the close. This retains the explanation without leaving an end badge on the completed answer.

The original period arrives by about 2:55 and EOS by 3:00. Final timings should follow the actual spoken period/stop phrases, not these one-second samples.

### Boards and close: keep their precise teaching role

Use current canonical assets for Before the Answer Begins and Same Token, Different Context. Preserve the previous proposal’s brief full views and narration-led card emphasis. Use the current demonstration for both probability distributions and selections, highlighting each choice as spoken. These scenes support reading and comparing exact values.

The resulting rhythm is: illustrated opening → recap/comparison → moving vector handoff → first choices/selection → growing-word animation → name choices/selection → animated period/stop → close. The animated handoff breaks the early board run; the growing reply breaks the probability scenes. No extra decorative footage or narration is needed.

The source close is visible at 3:03–3:08; Gemini Notebook branding begins around 3:09. Use the canonical close with both required spoken sentences and remove the branded tail. Exact trim and end hold remain subject to playback.

## Before rendering and delivery

The three narration cuts from REVIEW.md remain proposed. Implement the specific visual repairs above without changing the lesson or probabilities. Then inspect the rendered transitions, confirm each token appears with its narration, audition all cuts, and review the complete audiovisual result. The present frame inspection cannot certify those checks.
