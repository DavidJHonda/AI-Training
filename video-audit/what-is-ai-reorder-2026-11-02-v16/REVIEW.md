# What Is AI? — reordered review cut v16

Scope: narrow revision requested 2026-11-02. Move Two Types of AI before Where AI Already Lives, use the current banner-free Types board, remove its redundant spoken summary, and put the separate course-focus sentence after the everyday examples. No new narration, new examples, added pause time, installation, commit, or publication.

Candidate: `Prompts/what-is-ai-v16.mp4`. Planned duration 2:43.300, 4,899 frames at 30 fps, 1280 × 720. Final encoded verification results are in `qa.json`.

## Source and edit map

Installed v14 SHA-256: `738113d2f4bcb6d805960fc0405e042dafcf90ea29809356e66e856ff83315af`. Its approved audio is used directly, with no donor rerecording. Unchanged opening/Types support footage comes from the retained v11 source, and Everyday footage from the retained Why Learn v10 source, as in v14's assembly. The closing picture comes from approved v14. These are finished sources, so this assembly adds one video encoding generation to reused picture. The Types inserts use the exact current canonical JPG; the installed source MP4 and all course files remain protected by hash.

| Output | v14 source | Edit |
|---|---|---|
| 0:00–0:42.800 | 0:00–0:42.800 | Opening and definition preserved |
| 0:42.800–1:29.300 | 1:45.500–2:32.000 | Move Types explanation and its supporting scenes forward |
| 1:29.300–2:32.000 | 0:42.800–1:45.500 | Move Everyday section, including its existing final one-second hold, afterward |
| 2:32.000–2:35.100 | 2:35.200–2:38.300 | Retain “This course focuses on generative AI.” under the unmarked current Types board |
| 2:35.100–2:43.300 | 2:38.300–2:46.500 | Preserve the approved closing picture and audio |

Remove v14 2:32.000–2:35.200: “AI can recommend, AI can create.” The cuts bracket the full sentence in measured silence. The source's example sentence finishes before the first cut, and “This course…” begins after the second cut. Total removed: 3.200 seconds.

New joins receive only 5 ms edge ramps within existing silence. No new pause duration, gain adjustment, or other audio cleanup. The previous one-second Everyday hold travels with that section. The contiguous focus-to-close audio remains untouched.

## Visual plan and review

| Board | Highlights | Camera / duration | Rationale |
|---|---|---|---|
| Two Types of AI, recommendation explanation | Whole recommendation card, then job and mechanism, at preserved spoken onsets; fixed 4 px outlines | Whole unmarked board opens at 0:47.933, then slight complete-card dive; 14.567 seconds before the existing six-second recommendation animation | Replaces the old banner-bearing asset without flattening the supporting animation |
| Two Types of AI, generative explanation | Job, prompt mechanism, examples at preserved spoken onsets; fixed 4 px outlines | Whole board return at 1:08.500, then complete-card dive; 20.800 seconds | Uses the current two-column board; all active-card art/text stays in frame |
| Where AI Already Lives | Existing five-card sequence and takeaway outline | Preserved source camera, supporting scenes, and final hold; whole topic 62.700 seconds | Reordering alone requires no visual redesign |
| Two Types of AI, course focus | Unmarked | Whole board, 3.100 seconds | Connects the concluding focus sentence to the generative column without restoring the deleted banner |
| Closing board | Unmarked | Preserve approved hold/push/settle, 8.200 seconds | Current canonical closing and both approved lines remain |

The v15 internal check found the slightly tighter framing cut into the Types title. v16 raises both complete-card windows by 32 source pixels to retain the title while still showing the full active card. The audio timeline is unchanged from v15. v15 is superseded for visual review; do not install it.

## Narration and limitations

The complete v15 transcript was read against the current lesson and reorder. It retains the definition, recommendation/generative distinction, prompt explanation, all six generative examples, five everyday applications, course focus, and closing lines, in the new order. The redundant summary is absent. Existing narration and supporting scenes outside the named edit remain unchanged, including “two main categories” in the original introduction; this is a narrow reorder rather than a rewrite of that sentence.

No direct audio audition or uninterrupted audiovisual watch was performed. Transcript, waveform, correlation, decoded-frame, and transition-strip checks do not certify perceived cadence or voice joins. Listening review points: **0:42.800**, **1:29.300**, **2:32.000**, and the preserved close at **2:35.100**. This is a review candidate, not a claim of whole-file shipping readiness. The external Video Tracker was not accessed or modified.

Reproduce with `scripts/video/build_what_is_ai_v16.py` and verify using `scripts/video/qa_what_is_ai_v16.py`. The manifest records exact end-exclusive source/output frame ranges and protected hashes. No course reference points to this candidate yet.

## Encoded verification completed

- 4,899 decoded frames at 30 fps with continuous timestamps.
- Every frame compared with its intended source or current board render; maximum mean absolute error 3.079/255.
- Encoded audio correlation to intended PCM: 0.999985. Final v16 decoded audio is sample-for-sample identical to the freshly transcribed v15 audio; the transcript provenance is recorded in `transcripts/what-is-ai-v16.json`.
- All 12 transition gates passed. The every-frame transition strips and encoded overview were inspected; no stale banner frame appears at the edited joins. Complete active cards, title, and section outlines remain inside frame.
- Source and protected course-file hashes are unchanged. No installation or publication.
- Measured gaps across the review joins (seconds): 41.961–42.888 (0.927), 88.632–89.368 (0.736), 150.663–152.486 (1.823), 154.491–155.368 (0.876). These are retained source pauses, not new inserted time.
- Direct listening and uninterrupted audiovisual audition remain unperformed, as disclosed above.
