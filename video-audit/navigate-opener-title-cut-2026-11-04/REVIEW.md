# Navigate the Future opener — spoken title removal

Candidate: `Prompts/navigate-the-future-opener-v11.mp4`.

User-authorized narrow edit: cut “Embrace the Future” from the roadmap introduction. The resulting sentence is “This roadmap shows what we’ll explore in this section.” The current roadmap visual from v10 remains.

Removed v10 timeline frames [3189,3234), 106.300–107.800 seconds: exactly 45 frames / 1.500 seconds. Both picture and audio lose the same interval, preserving synchronization. Original measured silence handles are 106.195–106.458 and 107.631–108.209 seconds. The resulting encoded gap before “One” measures 0.514146 seconds. Five-millisecond fades sit entirely inside the quiet handles. No level changes or synthesized speech.

The candidate is assembled from v8 plus the existing lossless current-roadmap leg, then encoded once. v10 is the comparison reference, avoiding another video generation of loss from using its compressed picture as the build source. Source and candidate hashes and the shifted highlight/cutaway/close positions are recorded in `edit-manifest.json`.

The changed introduction was transcribed from the actual encoded output. It retains “section,” then “one, the argument,” and contains no old title. `after.wav` is a seven-second contextual listening clip beginning at output 103 seconds. Direct listening was not performed; the splice at 106.3 seconds remains available for the owner's listening review. No whole-video listening review is claimed.

Build: `.video-venv/bin/python scripts/video/build_navigate_opener_v11.py`
Verification: `.video-venv/bin/python video-audit/navigate-opener-title-cut-2026-11-04/verify.py`

Shipped locally on the user’s “ship it” approval. Commit `396003160d24137cc5e85f04869f5b9b9c38fe66` installs v11 and changes only its video, cache key, and manifest entry. Asset verification with `--migration-hashes` passed. Installed bytes match the reviewed candidate. Queued for batch deployment; no push or deployment performed. Unrelated concurrent working-tree changes were left untouched.

Verification passed: 4,325 decoded frames at 30 fps, 144.167 seconds. All retained frames were compared against v10 using the exact 45-frame timeline shift (maximum frame mean pixel difference 0.556/255). Encoded audio correlates 0.999797 with the expected cut PCM. All five transition guards passed; strips and the highlight-state contact sheet were visually inspected. The title-cut picture remains on the full roadmap with no flash or stale frame. The retained first-row highlight follows “One” after the cut.

After the local commit, removed regenerable map leg/canvas, WAV preview clips, and edited PCM scratch only from this task’s two audit folders. Candidates, manifests, transcripts, and review images are retained. Regenerate the map leg with the v10 build preparation before rerunning v11.
