# Does AI Think? v13 narrow repair

Built October 26, 2026. The pre-board Chinese Room setup is shorter, and Step 2 stays on the current board while the narrator describes the wall chart. The three-row comparison board and its highlighting/camera sequence are preserved.

Candidate: [does-ai-think-v13.mp4](/Users/davidobrien/Developer/AI-Training/Prompts/does-ai-think-v13.mp4). Duration **2:55.73**, 5,272 frames at 30 fps, 1280 × 720 H.264/AAC. This is 16.1 seconds shorter than v12.

SHA-256: `df83cf608a0585578c9b77c65644dc89556df39c6e916848acd7f6e18ae0ab4f`.

## Authorized changes

1. The setup now ends with “Imagine a person locked in a room who does not know a single word of Chinese,” then proceeds to “This diagram shows exactly how the Chinese Room works step by step.” Removed raw version 4 at 0:47.600–1:03.700, corresponding to v12 at 0:47.500–1:03.600. The three removed sentences described the incoming paper, rulebook lookup, and outgoing answer; the board walkthrough still teaches each of these once, including the full “How are you?” / “I’m fine, thank you!” exchange.
2. Removed the rulebook cutaway that occupied v12 1:17.400–1:21.000. The board remains on screen. At v13 1:00.600–1:01.600 the camera pulls back from Step 2 to reveal the actual wall chart, retaining the Step 2 outline through 1:05.900. It then moves to Step 3. No new pause was added.

The Chinese Room board begins complete and unmarked at 0:47.500. Its initial full view lasts 4.23 seconds. The complete-card highlights retain their fixed 4-pixel screen-space stroke. The current board image, wording, and fonts were not edited. The user's removal of the conflicting cutaway produces a 25.9-second uninterrupted board run, using the existing camera walk rather than substitute filler.

The current comparison board appears at 1:46.800–2:29.000. Its camera beats and highlight specifications are identical to v12, shifted 16.1 seconds earlier. The three approved donor passages and all other retained narration remain unchanged. The outgoing-note drawing at 1:13.400–1:16.400, prompt-input drawing at 2:01.800–2:04.800, uncertainty drawing at 2:18.800–2:21.800, and standard close remain in the edit.

## Verification

- Rebuilt pictures from pristine raw versions 4, 5, and 6 and canonical boards, using the existing v12 treatments. Audio uses the pristine assembled v12 PCM with the approved cut and 5 ms room-tone treatment at the new join; samples outside that join are exactly equal to v12's master after accounting for the cut.
- All protected source, v12 candidate, lesson, board, prep, index, and installed-video hashes remained unchanged. Source identities, donor spans, gains, output timings, and visual runs are in `edit-manifest.json`. The new removal and camera timing are in `narrow-edit-plan.json`.
- Complete sequential decode confirmed 5,272 frames and uniform timestamps. All 155 sampled encoded frames matched the intended renderer; minimum PSNR 34.08 dB. Encoded audio matched the assembled master at 44.98 dB SNR, with peak −1.41 dBFS and no clipping.
- The new join at 0:47.500 lies in measured quiet audio; the encoded quiet interval is 0.55 seconds. The sample step at the boundary is one PCM unit. Its seven-second listening excerpt is `join-3-encoded.wav`.
- Fresh transcription of the complete encoded video was read end to end. It confirms the shortened setup, complete board walkthrough, wall-chart wording, all three comparisons, useful-work conclusion, and closing lines. The removed overview sentences are absent.
- Inspected the two encoded contact sheets covering 0:40–1:32, full-resolution wall-chart and Step 3 frames, each comparison row, and the final frame. The wall chart is visible during the lookup sentence; the rulebook cutaway is absent. Preflight geometry checked 2,023 active highlight frames for containment within the camera.
- Transition guard checked 31 boundaries. Its nine flags are continuous intended camera moves at frames 1552, 1747, 1818, 1848, 1977, 2411, 2441, 4314, and 4344. Inspected all nine flagged every-frame strips plus the new cut at frame 1425; no stale visual island appears in those strips. The original automated FAIL result is retained in `transitions/transition-guard.md` alongside this disposition. The remaining unchanged transition strips were generated but not manually re-reviewed in this narrow pass.

Build command: `.video-venv/bin/python scripts/video/build_does_ai_think_v13.py`. QA command: `.video-venv/bin/python scripts/video/qa_does_ai_think_v13.py`. Additional evidence: `preservation-check.json`, `qa.json`, `encoded-transcript.txt`, `encoded-transcript.json`, `encoded-frames/`, `encoded-sheets/`, and `transitions/`.

## Review status

The requested repair is built and passes the transcript, inspected visual, timing, and preservation checks described above. **Direct listening and continuous audiovisual playback were not performed.** These checks cannot certify breath/cadence or inherited donor voice continuity. The new join to audition is **0:47.500**; inherited joins are now at 0:32.900, 0:38.100, 1:38.433, 2:05.933, 2:15.167, 2:29.000, and 2:39.967. Contextual encoded excerpts are saved as `join-1-encoded.wav` through `join-8-encoded.wav`.

Ready for review, not certified KEEP or installed. The course video and lesson reference remain unchanged. No commit, push, or publication was performed.
