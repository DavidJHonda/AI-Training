# Hallucination v18 — narration clarity and board timing

Review candidate: [hallucination-v18.mp4](../../Prompts/hallucination-v18.mp4). 8,459 frames, 30 fps, 1280×720; video duration 4:41.967. Rebuilt from pristine roll 3 with the approved roll-2 narration passage and supporting visuals. No site installation, publication, or commit.

## Narration repair

Replaced roll 3 at 3:04.267–3:16.600 with roll 2 at 2:56.200–3:11.533. The output replacement occupies 3:04.267–3:19.600. It is a complete Find the Source / Check the Match passage:

> Second, find the source. Look for the original document. A provided citation link alone isn't proof. You have to find the actual text. Third, check the match. This means confirming that the source both exists and actually supports what the AI said.

This removes “Ask if the source…” and pairs the explanation with a visual of opening and reading the source yourself. The prior Notice the Claim sentence and following summary remain. Both Stanford and pizza worked examples remain, including the explicit distinction between finding a source and determining whether it supports the claim.

The complete passage adds 3 seconds; no pauses were added. The donor has a −0.454 dB level adjustment. Both joins land in quiet gaps, with a 5 ms smoothing bridge. Outside those bridges, the assembled PCM exactly matches the declared source samples and donor gain. The encoded audio matches the edited PCM at zero offset with 45.74 dB signal-to-error ratio.

**Listening remains unperformed.** The wording passed independent small.en transcription of the donor and the final encoded passage. This establishes intelligible words and retained context, not a subjective voice-match or seam audition. [Context audio](encoded-repair-context.wav) covers output 2:58–3:28.50, including both joins and the complete following summary. End-to-end real-time audiovisual playback was also not performed.

## Board timing and supporting visuals

| Board | Output appearances | Longest uninterrupted appearance |
|---|---|---:|
| Nothing Sounds Wrong | 0:00–0:27.80 | 27.80 s |
| Why Hallucinations Happen | 1:14.767–1:33.50; 1:37.40–1:50 | 18.73 s |
| Real Text. Wrong Meaning. | 2:22.467–2:33.833 | 11.37 s |
| Check the Claim | 2:43.80–2:46.80; 2:56–3:15.60 | 19.60 s |

The opening exchange is the intentional exception to the roughly twenty-second board rule: it remains visible through the complete reading and spoken reveal. Previously it stayed for 49.43 seconds. The Why and Check boards previously stayed for 42.97 and 42.17 seconds respectively. Canonical artwork and fixed 4 px outlines are retained. Check highlights now follow the donor's spoken second and third steps; its return is unmarked until First begins.

| Output span | Supporting visual and teaching purpose |
|---|---|
| 0:27.80–0:44.40 | New explanatory browser/magnifier animation examines the university, sample size, improvement, and volume recommendation as credibility cues in the fabricated answer. The actual university is distinguished from claimed details. |
| 0:44.40–0:49.433 | Roll-1 zero-results drawing, source 0:55–1:00.033, supports the missing original paper. |
| 1:33.50–1:37.40 | New illustrative next-token sequence shows a word selected and appended, without invented probability figures. |
| 1:50–1:57.733 | New claim-versus-original-study graphic shows why fluent language is not evidence, using the already-established invented example. |
| 2:46.80–2:56 | Roll-1 laptop-search drawing, source 2:12–2:17.033, supports looking beyond the answer. Picture is slowed; narration is unchanged. No adjacent source diagram or pizza scene leaks into this span. |
| 3:15.60–3:28.967 | New process animation opens an original source, reads a highlighted passage in context, then compares it to the AI's claim. Generic document lines avoid fabricating an article or evidence. |

Custom explanatory graphics are implemented in `scripts/video/hallucination_v18_graphics.py`; editable source and rendered preview states are retained. Donor corner marks are cleaned. Earlier factual-label repairs, useful Notebook illustrations, both worked animations, the pizza board, and the canonical closing treatment remain. The close begins at 4:31.367 and retains the 48-frame hold, 150-frame push, and 120-frame tail.

## Encoded-output verification

- Full FFmpeg decode passed with no errors; all 8,459 frames were decoded at the expected resolution and frame rate.
- 104 encoded preview samples matched their intended renders. Maximum raw RGB MAE: 3.050/255; every bias-adjusted detail MAE below 2.5/255.
- 206 unchanged-scene samples matched v17 at their mapped source frames; maximum MAE: 0.436/255.
- All 24 transition guards passed with no short stale-frame islands. Every boundary strip, whole-video contact sheets, and full-resolution encoded samples of the changed graphics were inspected.
- Quiet join windows measured approximately −68 dBFS; maximum adjacent sample changes were 10 and 8 on the 16-bit scale. No clipped words were found in encoded-passage transcription.
- Source rolls, v17, canonical board assets, lesson Markdown, and the live video matched their protected pre-build hashes.

Evidence: `edit-manifest.json`, `qa.json`, `encoded-repair-asr.json`, `mapped-transcript.json`, `encoded-preview/`, `encoded-contact-*.jpg`, and `transitions/`. The mapped transcript is source-derived, not manually corrected. Motion was assessed through decoded states and transition sequences, not a continuous real-time viewing.

Build: `.video-venv/bin/python scripts/video/build_hallucination_v18.py --preview`, then the same command without `--preview` (requires an unused candidate path). QA: `.video-venv/bin/python scripts/video/qa_hallucination_v18.py`.

Candidate SHA-256: `1fb0c5381207d5bc04bb5eec7f30e0cae6a5b68045f59fa06e9e478281cfbfa1`.
