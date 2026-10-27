# Avoid Traps and Embrace the Future: shorter openers

Status: lesson changes complete; two revised video review candidates built and technically verified. Canonical MP4s unchanged. No commit, installation, or deployment.

## Approved scope

David accepted the five earlier blue-board cuts (“The videos are good”), then approved shortening Avoid Traps and Embrace the Future. For Avoid Traps, remove the paragraph after “This section teaches you to read the water.” For Embrace, remove the Magellan detour and repeated uncertainty commentary. Keep the analogies and essential teaching.

## Result

| Video | Previous approved cut | Revised candidate | Additional saving |
|---|---:|---:|---:|
| avoid-traps-opener | 202.300s | 178.333s | 23.967s |
| embrace-the-future-opener | 187.200s | 145.667s | 41.533s |

Candidates: `Prompts/avoid-traps-opener-v11.mp4` and `Prompts/embrace-the-future-opener-v8.mp4`.

Both are rebuilt from the hash-pinned pre-blue-board source versions (Avoid v9, Embrace v6), with all approved cuts in one encode. This avoids re-encoding the already-rendered v10/v7 intermediates. Full paths and hashes are in `edit-manifest.json`.

## Cuts and flow

Avoid Traps removes approved-v10 87.500–111.467: the extra ocean-malfunction comparison, the models-as-designed expansion, and the repeated train-your-eye conclusion. “The most dangerous areas often look the most helpful and inviting” now leads directly into the section map. All three map categories, the complete main rip-current analogy, and close remain. The written paragraph beginning “And you have a head start” is removed from index.html and Opener-Avoid.md.

Embrace removes approved-v7 71.733–82.600 (repeated hopes/fears explanation), 94.200–112.533 (Magellan), and 132.267–144.600 (repeated unpredictable-trajectory/preparation conclusion). The route is now: map analogy → unexpected discoveries → take both views seriously → AI is here to stay, with its qualifier → section map. Magellan is removed from the page, Markdown, prompt, and active kit guidance. The two expanded uncertainty passages already had no counterpart in the lesson text.

The previous replacement of the repeated blue board with the canonical map illustration remains. At each new Embrace splice, seven opening frames of the outgoing scene are replaced by the first clean destination frame; audio stays at the measured silent cut. This removes orphan serpent, Magellan-response X, and trajectory frames. No new artwork, voice, pauses, board design, or highlight treatment.

## Verification

- Avoid: 5,350 decoded frames. Embrace: 4,370 decoded frames. Both 30 fps, matching the plan.
- Zero blue-board frames found by the full-video detector. All six declared boundaries pass transition_guard.py; opening/splice contact sheets visually inspected.
- Source-to-plan audio correlations above 0.9997, original mono/stereo layouts preserved. All cut handles below -52 dBFS; 5 ms fades only in quiet handles. No added silence.
- Fresh full candidate transcripts confirm the retained sentences bridge correctly and the cut explanations are absent. The two closing messages remain.
- Final-frame comparison confirms preserved closes (mean pixel error under 2.6/255 after encoding). Source hashes remain unchanged.
- Both written pages checked in the browser. Inline JavaScript parses; git diff --check passes; Embrace upload sync check passes.

## Listening and shipping limits

No direct listening or continuous end-to-end playback performed. Please audition Avoid at 1:24–1:33 (splice 87.500 s), and Embrace at 1:09–1:29 (splices 71.733 and 83.333 s) and 1:40–1:48 (splice 103.067 s). Transcripts and correlations do not certify audible cadence.

The user approved the previous candidates, not these new joins. These are narrow review cuts, not whole-video ship certifications. Existing formal wording and other unrelated production findings remain outside scope. Canonical course MP4s, cache keys, and public deployment remain unchanged pending the repository’s separate shipping step.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_opener_shortening.py` (refuses to overwrite review candidates). QA reuses `qa_opener_blue_board_cuts.qa` with OUT set to this directory; transcripts use `transcribe_selected_videos.py`.

## Local shipping — 2026-10-27

All five final approved openers shipped locally in `8cb7cbdfeaaf0ec98e2d2453c264d9ac735ee098`; queued for batch deployment. Avoid Traps v11 and Embrace the Future v8 supersede earlier review candidates. See `video-audit/opener-shortening-2026-10-27/SHIP.md` and `shipping.json` for exact installed hashes and verification.
