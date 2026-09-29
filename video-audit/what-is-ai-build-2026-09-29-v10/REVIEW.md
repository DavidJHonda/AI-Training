# What Is AI? — version 10 review candidate

Built September 29, 2026 from raw version 5. **Required visual corrections completed; ready for owner playback review. Not published.**

Candidate: [what-is-ai-v10.mp4](../../Prompts/what-is-ai-v10.mp4). Runtime **3:02.57**, 1280×720, 30 fps, **5,477 decoded frames**. Source and output timelines are identical.

## Authorized scope

User: “Let's do those changes that weren't optional. And build the video.” The version-5 review supplies the previously proposed board treatment. This build applies the necessary graphic corrections and canonical course-board finishing while retaining optional Notebook graphics and all source narration. No sentence trims, grafts, added pauses, new illustrative scenes, or publication. The exact assembly is recorded in [edit-manifest.json](edit-manifest.json) and [PLAN.md](PLAN.md).

## Corrections and retained material

| Output time | Treatment |
|---|---|
| 0:34–0:44 | Reuse the original history-topic list without ratings, framed as a readable list-only cutaway during the ten-topic narration. This breaks the long desk-board hold. |
| 0:58–1:04.27 | Keep the history diagram; remove all Solid/Flawed judgments and the three red verdict tints. Original appearance animation remains. |
| 1:04.27–1:09.80 | Same keyboard/hands/coffee illustration with marginal annotations removed. Built-in imagegen edit; restrained 2.5% video push. |
| 1:38.50–1:42.50 | Cover the originality caption, including its fade-in and crossfade tail. Keep the forming-star and prompt animations. |
| 1:48.33–1:56.00 | Replace the one-model heading with “Examples of Generative AI,” preserving the animated six output types. |
| 2:15.37–2:25.80 | Preserve the animated movie catalog, scan, selection, and profile. Track its horizontal movement; remove all match percentages and the action-preference percentage. Keep “TOP MATCH.” |
| Throughout formal board spans | Exact current lesson JPGs, full unmarked introductions, complete active-card camera framing, 4-pixel outlines after camera cropping. |
| 2:51.27–3:02.57 | Exact canonical close, 48-frame hold, 150-frame push to 1.2×, 141-frame settled hold. Course close is the literal final frame; engine outro covered. |

Kept as requested: AI Processing Pipeline; Prompt + Learned Patterns; Curation; Invention. Optional spoken production asides also remain. Original pipeline jargon, source transitions, and other unchanged Notebook styling were not redesigned.

The longest uninterrupted course-board run is **19.37 seconds**, including consecutive summary/introduction boards. The longest individual teaching-board segment is 15.13 seconds. All Notebook-return frames receive corner-mark cleanup: 2100 paper clones, 317 glyph inpaints, zero declined frames. Canonical course imagery is used under the course-asset exception; no new stock photograph was introduced.

## Verification on the actual encoded candidate

- Complete sequential decode: 5,477 frames at 30 fps, 1280×720, source duration preserved.
- Compressed audio payload **and decoded PCM are identical** to raw version 5. No audio joins or processing.
- 159 prepared visual states compared with the encoded file; maximum mean absolute difference 3.316/255, consistent with delivery encoding.
- All 22 declared transition boundaries pass [transition guard](guard/transition-guard.md); the every-frame boundary strips were visually inspected. Full-runtime four-second contact sheets and more frequent movie-catalog samples inspected.
- Board openings, complete-card framing, corrected captions, cleaned keyboard, and final closing frame inspected. All 15 native highlight states measure 4 pixels; [ring record](ring-native-verification.json). The earlier color-threshold encoded audit detects 2–4 solid-color pixels after chroma compression; this does not change the fixed 4-pixel rasterized geometry.
- The moving catalog tracker is constrained to the measured 0–145 pixel slide; [tracking verification](tracking-verification.json). This fixes the brief scan-line ambiguity found in the superseded v9 intermediate.
- Source roll, canonical assets, and live video hashes unchanged.

**Listening limitation:** no direct end-to-end audio audition was performed. Exact audio preservation is verified, but the source's delivery/pronunciation still needs owner playback review before shipping. The prior complete two-pass transcript review found version 5 teaching-complete. This candidate is not represented as having passed the listening requirement for publication. Tracker status was not changed.

## Retained build materials

- [Clean keyboard illustration](assets/keyboard-clean.png) and [exact built-in imagegen edit prompt](assets/imagegen-prompt.txt). Imagegen skill: `/Users/davidobrien/.codex/skills/.system/imagegen/SKILL.md`.
- [History-list cutaway](assets/history-list-cutaway.png), derived from the existing video drawing before ratings.
- Build: `.video-venv/bin/python scripts/video/build_what_is_ai_v10.py`; shared assembly in `build_what_is_ai_v9.py`.
- QA: `.video-venv/bin/python scripts/video/qa_what_is_ai_v10.py`; [QA results](qa.json).
- Raw source: `Prompts/what-is-ai-5.mp4`, SHA-256 `085a13929d3df5715efb428edf49e7159c4710ddd419785cd92161c55bf4dd1e`.
- Candidate SHA-256: `ce4e4670d14aa3489ce3d6a732287014c6743f05f1d0de4f5880ec3611bcdc00`.

Live course video and website were not changed. Version 9 remains a superseded intermediate; review version 10.
