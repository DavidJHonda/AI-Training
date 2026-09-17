# Your Home Base v3: SHIPPED 2026-09-16

**Shipped file:** `course-assets/your-home-base/your-home-base.mp4` (3:58.93, 7168 frames, 30 fps; sha256 `8ce89dfb5807cb2e360918ea03267f77229797c74b4a95b2a31cd7d4b79c4a1e`).  
**Scope:** revise the v2 review candidate and publish the approved v3 file.  
**Build:** `scripts/video/build_your_home_base_v2.py`.  
**Manifest:** `edit-manifest.json` in this directory.

**Ship record:** David authorized publication on 2026-09-16. The approved candidate was moved to the canonical unsuffixed path, and `index.html` now references it with cache key `20260916ship1`. The displayed estimate remains `4 min`. The superseded live file is preserved here as `live-before-ship-2026-09-16.mp4` (sha256 `bb4e3ebc798f6c390faa96d3f97aefcd473a405499a1735b8aeba63b8cfd9dd8`). The shipped file decoded successfully from its canonical path and its hash matches the approved candidate.

## Requested changes

- Big Three board progression:
  - 1:12.93–1:16.48: complete board, unmarked.
  - 1:16.48–1:19.84: complete ChatGPT card.
  - 1:19.84–1:32.00: ChatGPT “What It Is,” heading and paragraph.
  - 1:32.00–1:35.52: “OpenAI Asks,” heading and question.
  - 1:35.52–1:37.92: complete Claude card.
  - 1:37.92–1:49.12: Claude “What It Is,” heading and paragraph.
  - 1:49.12–1:52.60: “Anthropic Asks,” heading and question.
  - 1:52.60–1:54.52: complete Gemini card.
  - 1:54.52–2:06.40: Gemini “What It Is,” heading and paragraph.
  - 2:06.40–2:10.00: “Google Asks,” heading and question.
  - 2:10.00–2:21.52: complete board, unmarked, for comparison and conclusion.
- Inserted exactly 30 frames / one second of matched room tone at 3:03.60–3:04.60, immediately before “To see how this looks in practice...”
- Removed the short tail transient previously heard at approximately 3:47 by ending the roll 2 course-example donor four frames earlier, after “Gemini Notebook” has resolved and before the isolated spike.

## Verification

- Full audio/video decode passed; 7168 decoded frames match the edit plan.
- Transition guard passed all 15 declared boundaries. Key strips for the split Gemini board leg, return to unmarked board, pause, course-board entrance, and course-to-close transition were inspected.
- Board state sheets and final timestamped contact sheets confirm the requested full-card and section-level outline sequence.
- The transcript shows the requested exact one-second gap: the prior sentence ends at 3:03.60 and the next begins at 3:04.60.
- Waveform inspection around the repaired course-to-close join confirms the former high-amplitude transient is absent; the new donor tail resolves into low-level room tone before the close.
- Source videos, lesson Markdown, and board assets remain unchanged. The canonical lesson MP4 was intentionally replaced under David's shipping authorization.
- Limitation: this environment cannot provide a human-equivalent ear audition. Audio was fully decoded, transcribed, and inspected at the repaired waveform boundary; final human playback remains advisable before publishing.

## Verdict

**SHIPPED.** The requested finishing changes are present at the canonical lesson path and pass the production checks listed above.
