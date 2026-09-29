# Your Home Base v8 — review candidate

Built September 29, 2026. Candidate is ready for owner review; not shipped.

Candidate: `Prompts/your-home-base-v8.mp4` — 1280×720, 30 fps, 6,852 frames, 228.4 seconds (3:48.4).

SHA-256: `28dbb9fbdf3be6cbf2a6fb57a1efb0ccf5b29b4757b66a74714896a41233905f`.

## Requested changes

1. Removed “Underneath the interface, each one is built around a different core philosophy.” This repeats the earlier explanation of company choices. Source frames [2044, 2188), 1:08.133–1:12.933, removed 4.8 seconds. The new join is “…and how it behaves. / This board breaks down the big three side by side.” Cut points are in the surrounding quiet gaps, with a 10 ms crossfade. No pause was added.
2. Tightened the Big Three camera to the inner cards’ text. The title and complete body text remain visible; top illustrations are excluded at the owner's explicit request. Full-board introduction lasts 3.267 seconds; the first dive starts at output 1:11.4. Equal zoom is used for all three apps, with 0.8-second eased moves and a summary pullback.
3. Added zoom and pan to How We Used. The full board appears at output 3:04.467, then the camera dives to ChatGPT at 3:12.167, pans to Claude at 3:21.8, and to Gemini at 3:29.3. Existing page-curl cutaway remains between 3:24.367 and 3:28.767. Each app has one text-panel highlight; no numbered-item highlights.

Both v7 label corrections are retained. Output was built directly from the pinned v6 source with those patches reapplied, avoiding another generation through v7. Canonical board JPGs were used without asset edits. The full manifest and exact camera coordinates are in `edit-manifest.json`; rationale and shot plan are in `PLAN.md`.

## Timing and retained visuals

All content after the cut advances 4.8 seconds. Big Three board runs are 1:08.133–1:19.1, 1:23.2–1:34.967, 1:38.8–1:53.0, and 1:58.133–2:16.6. The existing illustrated monitor cutaways between these runs remain. The home-base illustration and its camera treatment remain at 2:30.233–2:42.433. The longest uninterrupted board run is still 19.9 seconds (How We Used, 3:04.467–3:24.367). The proper 1.2× close remains at 3:37.5–3:48.4.

The opening page-curl shot accompanying the deleted sentence is removed with that sentence; the later page-curl use is preserved. Other source visuals and animations retain their timing relative to narration.

## Verification

- Full candidate decode passes; 6,852 frames and 228.4-second runtime match the edit plan.
- Source video and canonical boards remain hash-identical. Source SHA-256: `5e73454b5b7f468be774a46e25cf6377ed0fad030dc45a28d964f9825b1de018`.
- Audio checks at six positions throughout the candidate find zero sample lag against the edited reference. Reference SNR is 48.70 dB after AAC encoding.
- New join has a measured 0.469-second gap below −40 dB. Transcription of the actual encoded excerpt confirms the intended neighboring sentences and no remaining words from the removed sentence.
- All 37 detected highlight samples measure 4 pixels at 720p.
- Transition guard passes all 14 declared boundaries. Boundary strips were visually inspected, along with five encoded contact sheets, all 12 distinct settled board-highlight states at full resolution, and the close. Active-card text remains complete and readable; no stale frames were found at inspected boundaries.

Evidence: `verification.json`, `ring-stroke.json`, `guard/transition-guard.md`, `encoded/`, `encoded-sheet-*.jpg`, and `cut-context-encoded-transcript.txt`.

## Remaining review limits

This is a technical and sampled visual review, not a full real-time watch or listening pass. Audition the new join near 1:08 before shipping. Inherited audio questions from the prior review remain: the older splice now near 3:11.9 and the pronunciation of “TRY ITs” now near 3:15.4. ASR and waveform measurements do not substitute for listening.

Canonical course video and lesson index were not changed by this build. No commit, publish, or deployment was performed.
