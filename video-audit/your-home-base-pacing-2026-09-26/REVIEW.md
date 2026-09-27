# Your Home Base v5 — board-hold pacing repair, 2026-09-26

**Review candidate:** `Prompts/your-home-base-v5.mp4` (sha256 `5072b96c…2dedd`, 3:53.20, 6,996 frames @ 30 fps).
**Live video unchanged:** `course-assets/your-home-base/your-home-base.mp4` (sha256 `c3a337dd…68e7b`, 3:58.93, 7,168 frames). The lesson page is unchanged too. Not shipped.

**Scope:** a narrow repair of the two long board holds named in `video-audit/work-with-ai-review-2026-09-26/your-home-base/REVIEW.md`, plus the one approved narration trim. There was no reroll and no new narration. The raw rolls no longer exist, so every picture and sound comes from the live file, snapshotted as `baseline-live-2026-09-21.mp4`. Reused Notebook frames and the audio go through one extra encode generation.

Build: `.video-venv/bin/python scripts/video/build_your_home_base_v5.py`. The edit manifest is `edit-manifest.json`.

## Change log

1. **The Big Three, Side by Side**: the 68.5 s hold is now four board legs with three cutaways. The cutaways use the video's own three-monitor drawing (source 1:01.2–1:08.5). It is a still with no labels except "Chat" and "email", no logos, and no corner mark. Each cutaway eases toward the monitor that matches the line being spoken and rings that monitor in the app's card accent:
   - 1:23.90–1:28.00, ChatGPT: "You ask questions, create things, and get help with your daily work." The green chat screen is ringed green.
   - 1:39.77–1:43.60, Claude: "…for working through complex ideas and difficult multi-step tasks." The orange analysis screen is ringed purple.
   - 1:57.80–2:02.93, Gemini: "…when your work connects to the Google tools you already use on a daily basis." The blue calendar-and-email screen is ringed blue.
   - Board rings follow the spoken onsets for each app: whole card, then What It Is, then [Company] Asks. The board goes unmarked for the overlap summary (from 2:10.0). Section rings sit 16 px inside the card. The board stays compact at full view with no push, as shipped. Each return to the board lands 0.4–0.7 s before the next section's ring.
2. **Narration trim** at output 3:16.70: removed "This infographic details a specific breakdown of how the big three were utilized behind the scenes." That is source 196.700–202.433, exactly 172 frames or 5.73 s. Both cut points sit in the noise floor, with a 10 ms crossfade. The join leaves about 0.52 s of the original room tone between "…for the exact same task." and "We use ChatGPT…", close to the 0.53 s and 0.56 s natural gaps that were there before. No silence was added.
3. **How We Used the Big Three**:
   - 3:04.00–3:09.27: "To see how this looks in practice, multiple AI apps actually helped build this very course." now plays over the video's opening drawing of a person at a laptop. This is its complete 5.27 s span, source 0:00–0:05.27.
   - The board arrives at 3:09.27, on "We dynamically assigned different apps to different jobs…". It gets one whole-card ring per app, as before.
   - 3:29.17–3:33.57: "…writing code with Claude Code and styling pages with Claude Design" plays over the video's page-curl drawing, an app interface peeling back to a blueprint. This is its complete 4.40 s span, source 1:08.53–1:12.93. The board returns 0.5 s before "Finally, Gemini".
4. **Ring stroke**: every new ring is exactly 4 px at 720p (6 px at 1080p). `ring_stroke.py` read 4.0 px on all 146 samples (green, purple, blue; board and drawing). The live file reads 6–7 px. Two fixes were needed:
   - OpenCV's `cv2.line` draws only odd widths, so the build uses its own supersampled outer-minus-inner stroke drawer.
   - Ring edges are snapped to even pixels, so 4:2:0 chroma blocks never straddle the stroke. The first render read 2–3 px on purple and blue because of this.
   - `ken_burns_path.py` itself is **not** modified. The drawer is swapped in only inside this build.
5. **Unchanged, frame for frame**: everything before 1:12.93, the Notebook scenes at 2:21 and 2:47, the **Pick a Home Base** leg (12.2 s), and the navy-and-yellow close leg with both closing lines (10.9 s, copied from the live file).

## Board-hold measurements

These are frame-exact from the build timeline. `board_spans.py` at 0.5 s sampling agrees to within 0.5 s (`measure-after/board-spans.txt`). A "run" means consecutive board frames with no Notebook drawing between them, and the clock keeps counting across adjacent boards.

| | Before (live) | After (v5) |
|---|---|---|
| Big Three appearances | 1:12.93–2:21.40 **68.5 s** | 11.0 / 11.8 / 14.2 / 18.5 s |
| Pick a Home Base | 2:35.03–2:47.23 12.2 s | 12.2 s (unchanged) |
| How We Used appearances | 3:04.63–3:48.03 **43.4 s** | 3:09.27–3:29.17 19.9 s; 3:33.57–3:42.30 8.7 s |
| Close | 3:48.03–3:58.93 10.9 s | 3:42.30–3:53.20 10.9 s |
| Run: How We Used → close | **54.3 s** (3:04.63–3:58.93) | 19.6 s (3:33.57–3:53.20) |
| **Longest single board** | 68.5 s | **19.9 s** |
| **Longest continuous run** | 68.5 s | **19.9 s** |

## Checks performed

- Decoded frame count is 6,996, which equals the plan (7,168 − 172). The audio and video are both 3:53.20. Every leg decoded to its planned length.
- `transition_guard.py` passed all 13 boundaries. I inspected every strip (`strips-a.jpg`, `strips-b.jpg`): the first frame after each cut is already the destination, with no stale frames.
- Settled frames at every ring state are in `state-sheet.jpg` and `states/`. They show the right card or section, the complete component inside the ring, nothing clipped, and a full-view open on each board leg.
- Re-transcribed the whole candidate (`transcript-v5.txt`, faster-whisper small.en). All narration is present. The join reads "…for the exact same task. / We used ChatGPT for ideas and improvements" with no leaked syllable. All preserved lines are intact: burger analogy, three app explanations, ChatGPT as home base, the 18+ note, disagreement/agreement, all three use cases, and both closing lines.
- `silencedetect` at the join found natural low-level room tone, not digital zero. Integrated loudness is −16.1 LUFS live and −16.0 LUFS for v5.
- The corner mark is absent from all reused Notebook frames. The live file had already been cleaned.

## Not performed (please check)

- **No listening by ear.** I cannot play audio. Transcripts and RMS measurements do not certify sound. Please audition:
  - **3:16.70**, the narration cut ("…exact same task." → "We use ChatGPT…"): cadence, breath, noise floor.
  - A quick pass over the whole file. The audio was decoded and re-encoded once (AAC 200 kb/s mono). The live file was packet-copied from earlier builds.
- **No real-time playback.** I checked the picture with frame extracts, strips, and contact sheets, not by watching at speed. The eased push on the monitor cutaways should be judged in motion.

## Judgment calls to review

- **Rings on a Notebook drawing.** You asked for the corresponding app to be highlighted, so each monitor cutaway carries a ring in the card accent. Claude's monitor is drawn orange but is ringed in Claude's purple, to match the board.
- **Repetition.** The three-monitor drawing appears four times in total: once as drawn at 1:01, then in the three short cutaways. The laptop and page-curl drawings each appear twice. Nothing else in the file fits these beats.
- **The page-curl drawing for Claude is a metaphor.** It was drawn for "underneath the interface". It fits "building and design" but is not a literal picture of coding. If it doesn't work for you, the fallback is to drop it: How We Used would then run for 33.0 s unbroken plus the close.
- **No job-specific drawings** exist in the file for the ChatGPT and Gemini use cases, so those stay on the board. That is within the ~20 s guideline.

## Out-of-scope notes

- `index.html` has uncommitted changes from another session. None of them touch Your Home Base, and I did not change them.
- Render intermediates (`leg-*.mkv`, the baseline copy) are kept for a possible rebuild. Reclaim them with `clean_video_audit.py` after the video ships.
