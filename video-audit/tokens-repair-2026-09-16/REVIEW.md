# Tokens v8: SHIPPED 2026-09-16 (board refresh, visual-only retrofit of v7)

**Candidate:** `Prompts/tokens-v8.mp4` (3:37.60, 6528 frames, 30 fps). **Scope** (David: "take the live version and use the current boards and
closing message"): narrow visual repair of the shipped v7 (`course-assets/tokens/tokens.mp4`, sha256 f7db1df1b0cf2634…). The five course
boards are re-rendered from the current course-assets JPGs (`tokens-using-ai-feels-like.jpg` 6fda78dfb2…, `tokens-building-blocks.jpg`
4dbe7a44dd…, `tokens-how-tokenization-works.jpg` fb5d4c9d70…, `tokens-cat-token-id.jpg` 41bdd2bee5…, `tokens-how-ai-splits-text.jpg`
eaaed22d19…; the site URL line is the difference from the renders v7 carried), and the close is the canonical closing JPG (`tokens-close.jpg`,
01dd3cb70d…, 1332x597, bottom rows clean). **Source limitation, disclosed:** the roll behind v7 no longer exists, so the build takes the
finished v7 as its picture source and muxes v7's audio stream back in untouched. Outside the changed spans the picture is one more encoding
generation of v7 (mean per-pixel difference under 3, visually identical). **Shipped 2026-09-16** as `course-assets/tokens/tokens.mp4` (cache key 20260916ship1, pill 4 min); the v8 candidate removed from Prompts/. **Build:** `scripts/video/build_tokens_v8_retrofit.py`.
**Manifest:** `edit-manifest.json` here.

## What was reproduced

v7's camera schedule (`build_tokens_v7.py`, 2026-09-10) verbatim on the new files, which share the old files' dimensions: the same edit
timeline for mapping output frames to the roll's seconds, the same events, full views for the chat, Send, and cat boards, the Building Blocks
and How AI Splits Text dives with 24-frame moves, and the same rings at the same frames. Spans on the output timeline: chat 0–363, Building
Blocks 1638–2388, What Happens When You Hit Send 3655–4186, cat 4186–4576, How AI Splits Text 5025–5737, close from 6304. v7's two video-only
illustrations (words-to-math, whole-and-part) and every Notebook span are v7's picture.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 6528 = plan = v7; duration 3:37.60 = v7; audio stream MD5 identical to v7 (e6b28fbd6d729e872295f4a6a64d3fd0).
2. `transition_guard.py` passed all 9 declared boundaries (363, 1638, 2388, 3655, 4186, 4576, 5025, 5737, 6304); `boundary-pairs.jpg` inspected.
3. No pause or audio edits.
4. Ring states inspected (`states/*.jpg`) and a side-by-side of ten frames against the live file at ring and dive states: every ring and every
   camera position matches; the URL line is the only board difference. Frame diff, every 10th frame: only the close span exceeds re-encode noise.
5. Board treatment as v7.
6. Not auditioned by ear: nothing new to hear.
7. Nothing left undone in scope.

**At ship:** move to `course-assets/tokens/tokens.mp4`, new cache key on the `tokens` entry (currently `20260910repair1`), duration pill unchanged (4 min).
