# Embeddings — proposed narrow repair

**Recommendation: REPAIR the existing 4:38.33 video. No reroll proposed.** Preserve the original narration and illustrations except the two explicitly proposed cuts below; preserve current lesson boards and the owner's prior framing/omission decisions. This is a plan, not build or publication approval.

## Verified source and scope

Current page reference: `course-assets/embeddings/embeddings.mp4?v=20260922ship7`. Fresh local SHA-256 is `a47d96f332712cba24a26bf7483eaaaf184bbac72327cd2499c20ebf5825237e`, exactly matching the September 22 production manifest and the September 27 public/local byte verification. Fresh sequential decode: **8,350 frames, 30fps, 4:38.33**. All five current teaching JPG hashes match the production manifest. No fresh remote download was performed for this plan.

Read the current EmbeddingsSection in index.html, full lessons/embeddings.md, current video prompt, complete timestamped published-file transcript, current shared video specs, previous build/comparison records, and prior section review. Inspected the current board sheet and 39 freshly decoded frames across four overview sheets, plus the full-resolution embedding-table frame at 3:42. Earlier recorded ring measurements and transition results apply to this exact source hash; their limits are stated below.

The current prompt already incorporates the owner's approved omissions: badge numbers, coffee's six scores, and cat's complete numerical vector are shown without being read aloud. Preserve those decisions. Preserve full-view Student ID and Inside a Real Model boards. No surviving raw/donor Embeddings MP4 was found under Prompts or video-audit; the current published recording supplies both proposed cuts.

## Teaching assessment

| Current time | Teaching point | Assessment |
|---|---|---|
| 0:00–0:34 | A token ID identifies rather than describes; Student ID and fry gag | TAUGHT. The personal-traits list is compressed, but the distinction and gag survive. |
| 0:35–1:04 | Why IDs are insufficient; taste-test setup, six traits, 0–10 scale | TAUGHT. |
| 1:04–1:21 | Coke's six values and coffee's different profile | RICH; preserves the approved omission of coffee's full readout. |
| 1:22–1:46 | Fixed positions, recognition question answered immediately, vector → dimension → value | RICH; preserve these definitions and the question. |
| 1:47–1:56 | Repeats that characteristics become an ordered number row | Redundant; removable after the definitions. |
| 1:57–2:33 | Pepsi matches Coke on six dimensions; Citrus separates them; 10/1/0 | RICH; all three Citrus values spoken. |
| 2:34–3:23 | Embedding; every token; thousands of dimensions; learned positive/negative decimals; patterns of use and unlabeled dimensions | TAUGHT. The last two comparison rows are taught together; the earlier approved graft supplies the human-named versus AI-unlabeled contrast. |
| 3:28–4:09 | Cat ID 4719 selects its row; other token rows; d1–dn; learned number/parameter; whole-row embedding | RICH. Earlier value definition supplies the meaning of “value”; explicit parameter example retained. |
| 4:09–4:26 | Word fragments each get an embedding | Essential application worth retaining. The word “syllables” at ~4:22 is inaccurate terminology and needs repair. |
| 4:26.54–4:32.68 | Both closing lines | Present in order; delivery not auditioned. |

All eight required wording sequences appear in the full transcript, including the vector definition and closing lines. ASR punctuation cannot establish statement cadence or exact sentence boundaries. This is not an end-to-end listening verdict.

The word-piece issue is specific: modern subword tokenizers use learned text chunks, which need not coincide with spoken syllables. Primary reference: https://huggingface.co/docs/transformers/tokenizer_summary . No claim is made that all tokenization algorithms exclude syllable-based segmentation.

## Two proposed narration edits

1. **Approximately 1:46.7–1:56.4, redundant recap:** remove the complete sentence, “By placing these values in a structured grid, we have taken the abstract experience of drinking a beverage and turned it into an ordered row of numbers that accurately defines it.” Keep the preceding vector/dimension/value definitions and move directly into adding Pepsi. The spoken content is about ten seconds; final boundaries must sit in the surrounding quiet gaps, not merely at ASR word timestamps.
2. **Approximately 4:21.06–4:22.18, wrong noun:** remove only “individual syllables” from the existing sentence. The intended result is: **“Every one of those gets its own dedicated row of learned numbers in the table.”** Keep the preceding unbelievable → un / belie / vable example and its original animation. This uses the existing speaker and recording, with no donor or synthetic wording. It is a proposed intra-sentence edit, **not an auditioned repair**. The sibilant tail of “those,” the attack of “gets,” and sentence cadence must be checked during the approved build. If it cannot join naturally, return with a concrete alternative; do not silently delete the entire example or declare the incorrect wording repaired.

Expected total is roughly **4:27**, subject to final quiet-gap selection. No new pauses, automatic gap padding, speech cleanup, gain changes, or unrelated trims proposed. Preserve all other source audio, existing grafts, and existing pauses.

## Board and camera plan

All durations below count continuous exposure across zooms, pans, changed highlights, narration grafts, and holds. Same-board production segments have been merged. Target durations remain approximate until the narration cut is verified.

| Exact board title | Current span / continuous time | Planned highlights and camera | Proposed duration / break |
|---|---|---|---|
| An ID Identifies You. It Doesn’t Describe You. | 0:18.37–0:34.63 / 16.27s | Keep complete static board and existing banner cue. No badge walk. | 16.27s; existing drawings before/after. |
| Meaning Becomes an Ordered Row of Numbers | 1:04.33–1:56.87 / 52.53s | Keep full table. Coke row → coffee row → banner → Coke's three recognition values → vector row → dimension headings → one value. Preserve the visible numbers during the question. | About 42s after cutting the redundant final recap. No drawing substituted under the worked question. |
| One New Dimension Separates Similar Meanings | 1:56.87–2:27.57 / 30.70s | Keep full table. Pepsi → matching six → Citrus heading → Pepsi 10, Coke 1, coffee 0 → takeaway. | 30.70s; existing 6.23s drawing follows. |
| From Taste Ratings to AI Embeddings | 2:33.80–3:22.73 / 48.93s | Keep full opening and existing complete-comparison-row zooms/pans, both sides together. Preserve all five comparison points and pullback. | 48.93s; retain as a teaching exception, followed by existing 5.20s drawing. |
| Inside a Real Model | 3:27.93–4:08.97 / 41.03s | Keep the owner-requested full view. Token → ID → token rows → ID/token columns → dimension headings → 0.45 parameter → entire embedding row. | 41.03s; existing word-piece animation follows. |
| Standard closing message | 4:26.27–4:38.33 / 12.07s | Keep literal current close and existing hold/push/settle. | 12.07s, moves earlier with the cuts. |

**Highlight repair:** existing true ring samples read approximately 4–6px; normalize renderer-created outlines to a fixed **4px at 720p**, after camera transforms. Preserve canonical artwork, including its own embedded callout circle and highlighted cat row. Older ring widths are grandfathered, so they are not grounds for a reroll by themselves.

**Longest single board:** currently 52.53s; proposed approximately 48.93s (the comparison board). **Longest adjacent-board chain:** currently 83.23s (the two drink tables); proposed approximately 73s. These remain explicit pacing exceptions. The retained spans teach corresponding values/comparisons; cutting away to a generic diagram would hide useful information. No new matched drawing donor has been established. If further shortening is wanted, it is a separate teaching edit to discuss, not an excuse for filler.

Existing drawing spans to preserve: 0:00–0:18.37; 0:34.63–1:04.33; 2:27.57–2:33.80; 3:22.73–3:27.93; 4:08.97–4:26.27 (the last shortens only for the phrase repair). Their output timestamps after the first cut will move earlier.

## Clarification of the earlier section review

Do not delete the entire word-fragment passage: it applies the lesson to pieces as well as whole-word tokens and is expressly requested by the current prompt. Try the much smaller wording repair first.

Do not replace useful numerical demonstrations merely because their values are illustrative. Keep the original diagrams at approximately 2:28, 3:23, and 4:13 and the canonical embedding table. The table does not identify a named model or establish that its decimal values were measured from one. A possible “Illustrative values” caption is optional source clarification, not part of this recommended repair; no lesson/board change is proposed here.

Do not reuse the opening ID sketch over the thousands-of-dimensions comparison or hide the Coke question's numerical table just to reset a duration count. Preserve the explanatory pictures already in place.

## Transitions and checks still needed

The same-hash source has a retained **18-boundary automatic transition-guard pass**. This plan did not repeat that scan or manually inspect every seam strip. Fresh source decoding and selected transition/scene frames establish the current file and displayed boards, not real-time motion or audio quality.

After approval: verify the exact new narration cuts against waveform/ASR and listening; retime the affected pictures/rings; compare retained graphics and audio; sequentially decode the candidate; inspect every new splice and all changed ring states; confirm actual durations and unchanged canonical assets. The intra-sentence repair remains provisional until that check.

Not performed: real-time end-to-end watching/listening; voice warmth/prosody/pronunciation; audible splice/noise-floor checks; mobile playback/readability; fresh exhaustive ring measurements; independent token-ID recalculation or provenance verification of illustrative table values; new public download; tracker access/update. No raw donor rolls are available locally. Nothing built, edited in the course, or published.
