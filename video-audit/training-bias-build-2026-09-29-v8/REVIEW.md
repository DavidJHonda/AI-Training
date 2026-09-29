# Training Bias v8 — visual pacing candidate

Built from the approved September 29 review after David said, “Build it please.” **Review candidate only; not shipped or published.**

## Scope and result

Visual-only repair. Narration, existing pauses, total runtime, and the four-turn chat walkthrough are preserved. The final retrieval animation and standard close remain at their existing times.

Candidate: `Prompts/training-bias-v8.mp4` — 4:21.00, 1280×720, 30 fps, 7,830 frames.

The original roll no longer exists in `Prompts/`. The base is the verified finished v7, SHA-256 `0423a1b5f34337d130fbb1ff9392fa45ffab98d09426b47da68c8b99bc9917cd`, frozen for this active build at `/private/tmp/training-bias-v7-0423a1b5f343.mp4`. Video receives one new encode; compressed AAC is copied directly. The script asserts the source hash before building. No intermediate compressed candidate is used as a source.

## Changes on the output timeline

| Output | Treatment | Teaching purpose |
|---|---|---|
| 1:06.00–1:10.00 | Re-time the existing data/worldview drawing from source 0:49.40–0:54.80. | Show a narrow training sample shaping the default. Return to the board 1.23 s before Blind Spots is named. |
| 1:23.00–1:27.60 | Re-time the existing cow warning drawing from source 0:19.00–0:21.87. | Concrete callback after the Wrong Patterns card is introduced. |
| 1:52.27–1:57.70 | Hold the settled end of the existing default-versus-reality diagram. | Keep the broader-picture idea under the questions' introduction. Then establish the complete unmarked board for 3 s before the first prompt card. |
| 2:23.00–2:28.60 | Re-time source 1:48.00–1:52.23, where varied examples appear beside the uniform default. | Illustrate the rest of the picture during the takeaway. All three prompts have already been spoken with their cards visible; the banner gets about 3.5 s first. |
| 3:21.27–3:27.67 | New supporting diagram: question → outside sources → active context. | Give the retrieval introduction its own visual before the canonical RAG board appears. |
| 3:49.00–3:59.27 | New animated context/weights diagram. Trained weights remain fixed; retrieved information enters the active context on the corresponding spoken clause. | Replace the stale Generate highlight with the distinction currently being taught. |

The new graphics are code-native explanatory diagrams rendered by `build_training_bias_v8.py`, using the course navy, purple, blue, and teal palette. They contain no new numerical claims and no generated stock imagery. The existing animation at 3:59.27–4:11.67 is preserved, including its source-reliability warning.

## Boards, highlights, and pacing

Current canonical JPGs are used directly, with their original aspect ratios and compact full views. The three affected card boards are rendered at the current fixed 4 px outline width, using the original measured card edges and spoken highlight onsets. A 4× supersampled outline keeps its width independent of the artwork scale. The chat board is outside the repair and retains its existing treatment.

| Board | Visible spans | Highlights / camera |
|---|---|---|
| Wrong Pattern. Wrong Answer. | 0:21.90–0:33.73, unchanged | Preserve the approved whole-board opening and illustration camera walk. |
| How Skewed Data Distorts the Picture | 0:55.67–1:06.00; 1:10.00–1:23.00 | Full view; Defaults at 1:02.03, Blind Spots at 1:11.23, Wrong Patterns at 1:18.20. Longest uninterrupted appearance: 13.00 s. |
| Three Questions That Reveal Bias | 1:57.70–2:23.00 | Full view; card rings at 2:00.70, 2:05.03, 2:12.43; banner at 2:19.47. 25.30 s continuously, retaining the three complete prompts and a short takeaway. |
| Stale Information in Real Life | 2:38.47–3:02.33, unchanged | Preserve all four speech-bubble rings and full-board framing. 23.87 s; deliberate uninterrupted conversation. |
| How RAG Works | 3:27.67–3:49.00 | Full view; Retrieve at 3:30.63, Add to Context at 3:36.97, Generate at 3:44.93. 21.33 s. Generate ends when narration turns to context versus weights. |
| Closing message | 4:11.67–4:21.00, unchanged | Preserve canonical close, push, and final hold. |

Longest uninterrupted canonical board: **25.30 s**, down from **38.00 s**. No blanket twenty-second cutoff was used at the expense of a complete spoken walkthrough. No pauses, narration cuts, or audio grafts were added.

## Build and verification

- Build: `.video-venv/bin/python scripts/video/build_training_bias_v8.py`
- QA: `.video-venv/bin/python scripts/video/qa_training_bias_v8.py`
- Scope, half-open frame ranges, source/asset hashes, and declared boundaries: `edit-manifest.json`.
- Actual encode checks: `qa.json`; transition checks and every-frame boundary strips: `guard/`; encoded states: `encoded/`.

Finished-file verification completed:

- All **7,830 frames** decoded at 30 fps; duration **261.00 s**. Video packet timestamps are uniformly spaced at 1/30 s, with no missing final frame.
- Compressed AAC payload SHA-256 matches the source exactly: `d15112e5f0752f53852aa426e85c5e865b9a64d66527b245bad1fa655f60970a`. Audio packet timestamps and durations are also identical.
- **23/23 declared transitions passed** `transition_guard.py`. All every-frame boundary strips were visually inspected; no stale board flashes or leaked intermediate scenes were found. Restored Notebook scenes retain their original brief fade-in from the paper background.
- Encoded frames inspected for each changed ring state, board opening, cutaway, diagram reveal, restored animation, and the literal final closing frame. Text remains readable and complete; ring geometry follows each whole card or banner.
- Targeted encoded-ring samples have a median 3 px saturated core plus antialiased edges, consistent across the ten new outline states; the renderer uses a fixed 4 px supersampled stroke. See `ring-check.json`. No full-file color-threshold scan is claimed.
- Unchanged regions were compared with the stable source once per second: mean absolute channel difference **2.51/255**, maximum sampled frame mean **2.89/255**, reflecting the documented video round trip. Color-space metadata matches the source. This is visual preservation, not bit-identical video.
- Installed video, six canonical JPGs, and upload lesson hashes are unchanged. No website entry, commit, tracker row, or deployment was changed by this build.
- Candidate SHA-256: `612715b2ae1719028f0cafa9df01d52701205d4c8cc54a29c28c92799cf1ca88`.

 This is a narrow visual candidate: the prior listening limitations still apply. No new full end-to-end listening pass or continuous whole-video watch is claimed. RAG pronunciation and the wording around 3:15 remain listening checks from the evaluation, not established narration defects. This candidate is not labeled ready to ship.
