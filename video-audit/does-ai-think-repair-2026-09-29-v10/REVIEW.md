# Does AI Think? v10 — stay in the Chinese Room

Owner-requested narrow visual repair to v9. The different room drawing at **1:25.70–1:32.00** is removed. The video stays on the canonical Chinese Room's complete Step 3 callout while the narrator describes choosing and returning the reply, then follows the existing camera move to the outside-observer callout at 1:33.

Candidate: `Prompts/does-ai-think-v10.mp4`. Duration remains **3:36.20**, 6,486 frames at 30 fps, 1280×720. v9 remains available as the parent review candidate.

The changed picture span is exactly frames **2571–2759**, inclusive. No narration, pause, highlight or other shot is intentionally changed. Picture is rebuilt from the same pristine raw sources and canonical canvases used for v9; audio is copied from v9's encoded AAC stream.

The Chinese Room now stays on screen continuously from 1:09.50 to 1:50.17 (40.67 seconds). This is the owner's requested exception to the usual long-board cutaway treatment. The earlier door/note cutaway at 1:06 is outside the requested repair and remains.

At the visual-repair stage, the installed course video, canonical JPGs, lesson text, raw rolls and v9 were preserved. Subsequent local shipping is recorded below.

The prior review limitations remain: full listening/continuous playback is not certified, including the unresolved “thread/threat” pronunciation at 0:39 and the existing closing voice graft at 3:28.20. This visual repair adds no audio seam.

Rebuild command:

```sh
.video-venv/bin/python scripts/video/build_does_ai_think_v10.py
```

The builder refuses to overwrite an existing candidate. Evidence is stored in `edit-manifest.json`, `encoded/`, `repair-sheet.jpg` and `transitions/`.

## Finished-file verification

- All 6,486 frames decode at 1280×720 and 30 fps. Duration and final canonical close are unchanged.
- AAC packet SHA-256 is identical to v9: `64db12dc74a299b61dd7446796796a54451c08afd75fb03c18dec1b1d8effd99`.
- Both removed-cutaway boundaries pass the automated transition guard; their every-frame strips show the same Step 3 panel without a cut.
- The extra check on the existing 1:33 camera move triggers the detector on consecutive moving frames. Visual strip inspection confirms a smooth pan within the same canonical illustration, with no intervening graphic. This is a resolved camera-motion false positive; the original automatic FAIL report is retained.
- Compared all 189 repaired frames and 36 subsequent pan frames with the canonical renderer: minimum PSNR 37.64 dB. Inspected repair sheet and all three boundary strips.
- Parent, live video, raw rolls, lesson and canonical assets retain their recorded hashes.
- Candidate SHA-256: `098b77a5b70fbc9ba6bce99e6b2b2f345343792a34688c1a2d6245a29df3771f`.

## Shipped locally — 2026-09-29

Owner authorized shipping with “ship it” after review of v10 and disclosure of the prior listening limitations. Installed approved v10 at `course-assets/does-ai-think/does-ai-think.mp4` and updated only this lesson's cache key in `index.html` to `20260929ship-doesaithink-v10`. The displayed runtime remains “4 min” for 3:36.20.

- Local commit: `23f517343a61a0d95b82c2885433f5b16ca6e4f6` — `Ship approved Does AI Think v10 locally`.
- Installed and committed video SHA-256: `098b77a5b70fbc9ba6bce99e6b2b2f345343792a34688c1a2d6245a29df3771f`. Both verified byte-for-byte against the approved candidate.
- Commit scope verified: canonical video and one `LESSON_VIDEOS` entry only. Unrelated working changes and local audit/build records were not staged.
- Local reference verified; no push, deployment or public-site verification performed. **Queued for batch deployment.**
- Owner release approval is recorded; assistant listening/continuous-playback verification remains unperformed and is not represented as a pass.
- After the commit, removed ten regenerable WAV/canvas scratch files (about 0.10 GB) from this build only. Kept raw rolls, v9/v10 candidates, generated source photo, manifests, review evidence and code.
