# Vector Space v18 board and flash repair

Review candidate: `Prompts/vector-space-v18.mp4`. Runtime remains 4:16.63 (7,699 frames, 30 fps, 1280 × 720).

The drink board from 1:25.40 now uses the current lesson diagram: a smaller soft-drink group, closer Coke and Pepsi markers, Coke’s two-line label centered beside its marker, and Pepsi’s label closer beneath its marker. Hot coffee and Mystery B keep their geometry. All eight reveal cues and 15-frame reveal blends are preserved.

The reported flash was exactly two old graph frames at 5721–5722 (3:10.70–3:10.77). The final drink board now covers them. The next source animation resumes at its original frame 5723; no audio or time was removed.

## Verification

- All 7,699 output frames decode. All 45 declared transitions pass the automatic short-flash guard.
- Actual encoded board states and the every-frame repaired exit strip were visually inspected.
- Original v17 AAC was copied without re-encoding. Extracted AAC hashes match exactly: `c9647f0aa6f7115abbb1241da978abdad27730bbfc5defaf8c6c7e58cba28360`.
- Unchanged-section frame comparisons match exactly at sampled opening, city, later scale, context, and closing frames. The continuing animation immediately after the repair differs only by minor compression noise.
- The renderer used original raw sources and retained previous capture assets for other sections. Protected source, v17, and installed-video hashes remain unchanged.
- Direct listening and real-time motion review were not performed. This is a narrow visual repair with identical audio, not a new whole-video listening certification.

The candidate was subsequently approved and installed locally; see release record below.

Evidence: [manifest](edit-manifest.json), [verification](verification.json), [transition guard](transitions/transition-guard.json), [encoded stages](inspection/encoded-board-states.jpg), [repaired exit](inspection/after-transition.jpg). Open [review page](review.html) for jump points to the updated board and transition.

## Local release

Shipped locally; queued for batch deployment. David approved v18 with “ship it.” Installed the approved MP4 and updated the cache key. The same commit includes the approved current drink-diagram changes so the lesson and video match.

Commit: `ea76d9155d11ab1ef56d643e9eaf38717565d998`. Installed SHA-256: `cd895007b43e295a86f7aaea199014cec17e17bd332bf6ceaac08506e87ac805`. The local `/course` page references v18 and the locally served video matches the approved candidate exactly. No push or deployment. Unrelated edits remain unstaged. Reclaimed 0.13 GB of regenerable scratch for this build only.
