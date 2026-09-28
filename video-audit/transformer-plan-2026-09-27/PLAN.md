# Latest approved revision — September 28

David requested complete-card zooms and pans on the opening and resolving-meaning boards, the full “The cat drank the milk because it was fresh” sentence in the opening, and individual spoken-word highlights on How Earlier AI Read Text. This supersedes the earlier full-view-only recommendation below. The approved v11 rereads and sentence-to-clue highlights carry forward. No conceptual lesson rewrite, graphic removal, or publication is authorized.

Candidate v12 is being built in `video-audit/transformer-repair-2026-09-28-v12`, from the unchanged published source. Its review report is the current implementation record. The historical proposal below describes the earlier planning stage and should not be read as current build status.

---

# Transformer — revised repair proposal

Updated after David's review of the explanation and agreement to reread the examples. This replaces the earlier reroll/source-correction proposal. Keep the current introductory explanation; no causal-attention or prediction lesson is proposed. No course, board, prompt, or video changes have been made.

## Scope and status

Recommend a narrow repair of the return to the examples at current **2:25.48–2:46.14**. David agreed that each full sentence should be read again before explaining its clue. The proposed audio reuse is identified below, but natural joins are not yet verified. This is a repair feasibility plan, not a claim that a completed repair has earned KEEP. No reroll is justified by the previously raised scope concern.

Current source: `course-assets/transformer/transformer.mp4?v=20260922ship6`, 3:46.267, 6,788 frames at 30 fps. SHA-256 `d55f0000452087fb4b7993b2e79e06759ef263e147362cbd744a3c44883d9eb6`. Current source and all seven board/close JPGs match the retained build-v10 manifest. See `source-checks.json`.

## Narration repair

Read each sentence, then retain the corresponding current explanation:

1. “Please turn on the light.” → “Turn on” tells the AI LIGHT means brightness.
2. “The suitcase is light enough to carry.” → “Carry” indicates LIGHT means not heavy.
3. “The cat drank the milk because it was thirsty.” → “Thirsty” describes the cat, so IT refers to the cat.
4. “The cat drank the milk because it was fresh.” → “Fresh” describes the milk, pointing the pronoun to the milk.

The first presentation introduces the ambiguity. This return teaches the clues that resolve it. Do not add a prediction explanation or change the current conceptual scope.

Potential narration sources, all from the current published MP4:

| Intended insertion | Existing source words | ASR reference interval | Destination before existing explanation |
| --- | --- | --- | --- |
| LIGHT / brightness sentence | “please turn on the light” | 0:30.24–0:31.26 | Approximately 2:25.48–2:28.98; handle “In our examples” as a bridge rather than leaving it stranded |
| LIGHT / not-heavy sentence | “the suitcase is light enough to carry” | 0:34.24–0:36.06 | Approximately 2:29.94; keep or remove “In the second” according to natural phrasing |
| IT / thirsty sentence | “the cat drank the milk because it was thirsty” | 0:41.32–0:43.58 | After “It's the same for pronouns” (2:33.62–2:34.44), before the 2:35.46 explanation |
| IT / fresh sentence | “the cat drank the milk” plus “because it was fresh” | Prefix approximately 0:41.32–0:42.58; ending approximately 0:47.42–0:48.42 | Before the 2:38.74 explanation |

**Important limitation:** the opening does not speak the fourth sentence in full. It says, “If we change the sentence to, because it was fresh…”. The desired full reread therefore needs an internal join between the repeated prefix and this ending, or another verified source. The ASR assigns “because” a zero-length timestamp, so those edges especially require waveform/phonetic checking. No raw alternate Transformer recordings survive under Prompts or video-audit. Do not promise a natural assembled sentence before testing and listening review.

All listed source times are word-location guides, not approved sample-accurate cuts. Preserve word attacks/tails and existing voice/levels. Do not add automatic one-second pauses; retain only the breathing room needed for the rereads. No other narration edits are recommended.

## Additional repair suggestions

- Synchronize the board with each reread: highlight the complete sentence while it is spoken, then its clue section during the explanation. Use the sentence boxes already on the current canonical board; do not invent or reflow artwork.
- Use fixed 4 px outlines at 720p, drawn after camera transforms, throughout rebuilt board legs. Keep the same colors and the existing embedded IT border; do not double-outline it.
- Retain approved full-view framing, illustrations, and drawing breaks. No new zoom is proposed. Previous tall-card zoom attempts clipped content.
- Expect the resolving-meaning board to grow from 21.47 s to roughly 30–35 s, pending audio assembly. This is purposeful worked-example time. Keep the sentence and its clue visible together; do not insert filler or remove the new readings to meet a duration threshold. Report the actual final continuous duration, including all motion and pauses.

## Board plan

Current times are reference timings. Later video spans shift by the final added audio duration.

| Exact board title | Current continuous exposure | Proposed highlights and camera | Break / duration decision |
| --- | --- | --- | --- |
| Two Problems Context Must Solve | 0:23.567–0:39.033, 15.467 s; 0:42.867–0:53.667, 10.800 s | Preserve full view, whole-card introduction then spoken sentence sections and banner; 4 px outlines | Preserve the intervening cat/IT/glass drawing |
| How Earlier AI Read Text | 1:01.600–1:21.967, 20.367 s | Preserve full view, word-sequence ring and banner; leave embedded IT border alone | Keep complete explanation as a minor duration exception |
| How a Transformer Reads a Sentence | 1:32.100–1:42.600, 10.500 s | Preserve full view, sentence and CAT/IT highlighting; 4 px | Keep existing illustration breaks |
| How Context Changes the Numbers | 1:51.900–2:13.500, 21.600 s | Full view; Attention card → Transformation card → banner; 4 px | Keep paired explanation intact |
| How the Transformer Resolves Meaning | 2:25.467–2:46.933, 21.467 s currently; roughly 30–35 s proposed | Full-board opening; each sentence box during reread → corresponding clue section during explanation; final banner. Full view, one ring at a time, 4 px | Deliberate longer worked example; preserve the active-data drawing before and LIGHT/brightness drawing after |
| How a Transformer Keeps Words in Order | 3:12.700–3:36.267, 23.567 s | Full view; comparison strip → Without Position Information → Position Stamps Preserve Order → banner; 4 px | Keep current complete example; no narration change |
| Attention is all you need. / AI uses relationships between words to help interpret your message. | 3:36.267–3:46.267, 10 s | Preserve current canonical close and motion | Keep |

The current longest teaching-board run is 23.567 s; counting its adjacent close gives a 33.567 s chain. The repaired resolving-meaning board will likely become the longest single teaching-board run. Measure its final duration rather than treating new rings, pans, or zooms as breaks.

## Verification and limits

The retained September 27 full sequential decode and automated transition guard passed all 17 declared boundaries on the current source hash. This planning review inspected the full timestamped transcript, lesson/page/prompt, board/scene contact sheets, and selected fresh full-resolution frames. Current sampled generated highlights vary approximately 4–7 px; widths alone are not a reason to reroll. The boards match current assets.

The candidate must be checked for exact source/cut mapping, full word preservation, encoded audio integrity, new transition boundaries, ring geometry, and continuous board durations. Natural cadence and the internal join in the fourth reread require perceptual listening. End-to-end listening, existing audio-graft naturalness, mobile readability, and public-player behavior have not been checked. No new donor audition, build, source edit, tracker write, or publication has occurred.
