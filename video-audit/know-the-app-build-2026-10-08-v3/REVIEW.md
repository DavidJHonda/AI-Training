# Know the App — v3 — shipped locally

Built 2026-10-08 from roll 6 using the October 1 edit plan. Shipped locally on 2026-10-08 after owner approval. Queued for batch deployment. Local release commit: 4c56e1e81c57a9b815d9a2b49b330a0c807c92fa. Installed at course-assets/your-choices/your-choices.mp4, cache key 20261008ship3.

- Runtime: 4:23.63, 7,909 frames at 30 fps, 1280×720.
- Roll 6 audio is copied unchanged; compressed audio stream hashes match.
- Current canonical Which Model?, How Much Thinking?, and How Much Research? boards, with narration-timed highlights using the established nominal 4 px renderer.
- Drawn camera, engine and project-planning examples from rolls 4 and 5. New college-physics comparison illustration replaces the property-like maps at 3:47–3:55.
- Useful source animation retained. Repaired settled answer labels to say Proposed answer / Review before using, removing claims that the answer has been verified.
- Banner highlights begin at 1:23.82, 2:39.52 and 4:02.54 and remain through each takeaway.
- Canonical closing: 48-frame hold, 150-frame push, 26-frame settle.
- Canonical boards and protected source files remain unchanged.

## Validation

Decoded all 7,909 output frames. Automated transition guard passed all 27 declared boundaries. Reviewed full-size previews of all three banner states, encoded frames immediately before and at each new highlight, and the new college illustration at its beginning, middle and end. The earlier v2 full-video visual review remains the baseline for unchanged sections. Audio identity: SHA256=83b2ea2a3724ecbb2fde7d28b80c77c7c72ef98ff9f24f4722a7f36e3304e342.

Candidate SHA-256: `42612126a609f966c3581726c76d65b615f93e135beee722183a57e487ec7f5b`.

Editor continuous audiovisual listening was not completed; this limitation was disclosed before the owner reviewed the video, requested revisions, and approved shipping. Roll 6’s narration KEEP review and byte-identical audio are retained. No completed editor listening pass is claimed.

v2 is superseded by v3: three banner highlights and the college-comparison illustration. The generated image is stored in assets/college-physics-comparison.png. Build script: `scripts/video/build_know_the_app_v3.py`. Exact timeline and asset hashes: `edit-manifest.json`. QA: `qa.json` and `transitions/`.
