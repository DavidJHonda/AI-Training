# In Your Hands v6 — revised for review

Candidate: `Prompts/in-your-hands-v6.mp4`. Built September 29, 2026. 1280 × 720, 30 fps, 5,508 frames, 3:03.60. SHA-256: `721e0738684fa09007104865ef0ca292dac2951a93766d04e7db8bcfbde2151c`.

## Requested changes

- Canonical lesson board now says **“Make something real with AI instead of waiting to see what happens.”** The lesson Markdown and the page's board alt text/cache key match. The video uses that same updated canonical JPG.
- The original board art and all other wording/layout were preserved by placing only the generated sentence region into the original board. Dimensions remain 1600 × 1340. Original and full generated edit retained in assets; assembly details in `assets/BOARD-EDIT.md`.
- Replaced the three cartoon/craft images with realistic generated people in ordinary clothing using an AI assistant to plan, test and finish a useful club-events app. This follows the owner's latest request for more realistic people and no jersey requirement. The subsequent owner-approved style update in Edit Spec 8d makes this naturalistic style the standard for newly created people scenes. These are custom generated assets, not externally sourced stock photographs.
- All five cutaway positions and restrained 2% pushes remain: testing at 1:18–1:24.20 and 2:09–2:14.60; making with AI at 1:41–1:43.80 and 2:37–2:42; own plan before AI at 2:23–2:30.
- Preserved Notebook opening, approved white-column camera framing, fixed 4 px highlights, canonical closing, source audio, pauses and runtime. The narration still says “make something real right now”; “with AI” is explicit in the board and the supporting imagery. No audio edits were requested or made.

## Verification

- Full sequential decode passed: 5508 frames.
- Audio packet payload is byte-identical to the source: `17d0f162b70b127c5f9de88b6ea360a17cf45313e3ce1c0f8c17a45ef729f685`.
- All 128 encoded preview checks passed (maximum mean pixel error 3.1329/255), as did 51 retained opening/close checks (maximum 2.6883/255).
- Inspected native encoded images of the revised highlighted row and all three new scenes. Text is complete, the AI assistant and usable output are visible, and the person/screen framing survives the push.
- Inspected before/cut/after frames for all ten new cutaway boundaries. No stale or intervening artwork found.
- Transition guard: 28/30 automatic passes. The same two camera-motion flags as v5, frames 1405 and 3145, were inspected in every-frame strips: intentional dive/pullback, no stale picture. Raw detector result remains retained.
- Updated board dimensions verified. Outside the patched region, mean pixel change is 0.6374/255 from JPEG encoding; original artwork and remaining text retained.

## Scope and limits

Owner approved local shipping with “ship it.” V6, the revised board and lesson copy, and the custom-graphics style policy are installed and committed locally. V5 and V6 review candidates are preserved. No push or deployment performed.

No real-time end-to-end listening/viewing pass was performed. Source audio is unchanged. The disclosed 42.7-second first board run and prior accepted narration variants remain as documented in v5; this is a narrow visual revision, not a new whole-file ship certification. Only the finished source video is available; retained scenes have one additional encode.

Build/QA scripts: `scripts/video/build_in_your_hands_v6.py`, `scripts/video/qa_in_your_hands_v6.py`. Asset prompts: `assets/PROMPTS.json`. Exact hashes/timing: `edit-manifest.json`. Checks: `qa.json`, `board-edit-check.json`, `transitions/` and the two boundary contact sheets.

## Local shipping — September 29, 2026

Commit: `8f82a6f03a9b56ee18c1c1956ba235bf708f225e`. Installed video SHA-256: `721e0738684fa09007104865ef0ca292dac2951a93766d04e7db8bcfbde2151c`. Page video cache key: `20260929ship1`; board key: `20260929ai1`. Committed video, board and Markdown bytes verified against installed files; committed page references verified. Full audio/video decode completed without errors, and audio payload matches the source. Existing 128-frame content checks and 51 retained-scene checks remain applicable to the identical approved candidate. The prior disclosed real-time viewing/listening limitation remains; no new listening pass is claimed. User approval authorizes this exact candidate; no unrelated visual or audio changes made.

**Shipped locally; queued for batch deployment.** Only five release files are in this commit. Unrelated working changes and broader shared-document revisions remain untouched.
