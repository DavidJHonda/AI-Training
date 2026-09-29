# Vector Space v10 — evaluation improvements

[Full candidate](/Users/davidobrien/Developer/AI-Training/Prompts/vector-space-v10.mp4) · [New graphic preview](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-29-v10/preview-bridge.mp4) · [Narration-join preview](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-29-v10/preview-narration-join.mp4) · [Context-board preview](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-29-v10/preview-context.mp4)

**Built for review, not shipped.** The user approved the evaluation improvements: “Built it please, with your improvements.” Candidate: **3:29.27**, 6,278 frames at 30 fps, 1280 × 720. SHA-256: `5a735042f7c25a5ccaad2747058ef3c9653eec3d457e85201f9b29eba077e296`.

## Changes

1. **Two coordinates → seven ratings, 1:37.37–1:46.23.** A new code-rendered graphic compares Dallas's latitude/longitude with Coke's seven ratings. It uses the lesson's existing values and labels. The position captions and vector takeaway appear during the spoken bridge. A separator keeps this a comparison, avoiding an arrow that could imply converting Dallas into Coke. This replaces the final 8.87 seconds of the table hold. Table exposure drops from 33.07 to 24.20 seconds. The longest consecutive board run drops from 73.07 to **40.00 seconds**. The 24.20-second table remains a deliberate pacing exception while the narrator walks its rows.
2. **Complete donor sentence at 2:26.57–2:34.63.** V9's “AI uses this exact mechanism to understand text” is replaced with Roll 1's complete sentence: “AI systems take this exact mathematical concept and scale it up to thousands of dimensions to measure the distance between complex concepts.” Source: `Prompts/vector-space-1.mp4`, 2:57.03–3:05.10, frames [5311,5553). Replaced v9 interval: 2:26.57–2:30.50, frames [4397,4515). The existing learned-during-training explanation follows. This uses available recorded narration rather than claiming the exact suggested sentence was available. It preserves the dimensionality point, though “thousands of dimensions” is consequently repeated in the next sentence. The replacement is 4.13 seconds longer. The existing meaning-neighborhood drawing is retimed continuously under the longer beat; no new board is inserted there.
3. **Larger complete context board, now 2:53.33–3:14.87.** Camera width changes from 2208 to 2112, a **4.55% enlargement**. The entire canonical board, title, path, labels, and takeaway remain visible. The framing is fixed throughout; the board arrives unmarked and keeps its original spoken highlight timing. This is a modest readability improvement, not a claim that small labels now read comfortably on phones. All four highlight states still measure 4 px on their straight sides.

## Preservation and assembly

Rebuilt the approved composite audio from the three original rolls, using the recorded source intervals and gains. The new whole-sentence donor is level-matched at −0.8325 dB. Cut boundaries were selected in measured low-level gaps, not at picture cuts; 20 ms edge RMS around the new joins is approximately 2.8–4.4 on the 16-bit scale, with 4 ms endpoint ramps. No artificial pause was added. Exact frame/sample mapping is in `edit-manifest.json`.

Pictures are rendered from the canonical JPGs, original code-rendered schematics, and the retained lossless drawing excerpts from the v9 build. No generation of the finished MP4 was used as a visual repair source. Retained excerpts carry hashes; the historical calculated-gap excerpt is protected separately because its original public-video path now contains a newer release.

Existing city and mystery-drink examples, the fixed map-to-map framing at 2:05, and the standard close remain. All source rolls, v9, installed live MP4, lesson Markdown, and canonical JPGs passed protected-hash checks. No index update, commit, push, deployment, or tracker edit was made.

## Board plan as built

| Board | Highlights / camera | Output span |
|---|---|---|
| Three Cities, Two Coordinates Each | Dallas → Mountain View → New York; full view | 0:31.67–0:54.67, 23.00 s |
| Use the Map to Find the Closest City | New coordinate/city pairs → takeaway; full view | 0:54.67–1:09.67, 15.00 s |
| Three Drinks, Seven Dimensions Each | Whole row → Coke/Pepsi → coffee → takeaway; full view, then new explanatory graphic | 1:13.17–1:37.37, 24.20 s |
| A Map of Drink Similarities | Soft drinks → coffee; unchanged fixed full view | 1:46.23–2:04.97, 18.73 s |
| Use the Map to Find the Closest Drink | Matching rows → Citrus 9/10 → Citrus 9/1 → takeaway; unchanged fixed full view | 2:04.97–2:26.23, 21.27 s |
| How Context Changes IT’s Position | Starting values → update path → updated values → takeaway; larger complete full view | 2:53.33–3:14.87, 21.53 s |
| Canonical two-line close | Unmarked; 48-frame hold, 150-frame push to 1.2×, 42-frame settle | 3:21.27–3:29.27, 8.00 s |

The longest board is 24.20 seconds. The longest uninterrupted board chain is 40.00 seconds. City, mystery, and context holds retain their existing mild >20-second exceptions. Their narration continues explaining the visible content.

## Verification

- Complete sequential decode: exactly 6,278 frames, correct dimensions/fps, no nearly black frames.
- Transition guard: **22 boundaries passed**. Manually inspected every-frame strips at the new graphic's entrance/exit, both new audio joins, and the enlarged context board's entrance/exit. Other boundary strips were generated and automatically checked but not all freshly inspected by eye.
- Fresh whole-video four-second contact sheets inspected, plus native-resolution changed frames and the literal final frame. The canonical close and both lines remain intact.
- Native context-ring measurements: 4 px on all four sides in each of the four active states; see `context-ring-widths.json`.
- Encoded audio has no sample clipping; peak 27,960 (~−1.38 dBFS), AAC/reference SNR 44.59 dB. AAC contains 640 trailing padding samples beyond the planned PCM timeline, not an extra content beat.
- Full-file ASR status is recorded below after completion. Transcript checks establish wording, not audible splice quality.

**Direct listening and continuous real-time playback were not performed.** The two new joins at 2:26.57 and 2:34.63 need listening for voice continuity and cadence; the contextual preview covers both. This candidate is not presented as fully listening-certified or ready to ship. Existing perceptual-listening limitations from v9 also remain.

Build: `.video-venv/bin/python scripts/video/build_vector_space_v10.py`. QA: `.video-venv/bin/python scripts/video/qa_vector_space_v10.py`. Evidence: `edit-manifest.json`, `qa.json`, `guard/`, `encoded/`, `contact-*.jpg`, `context-ring-widths.json`, and the contextual MP4 previews. Build refuses to overwrite an existing candidate.

## Final transcript check

Fresh full-file ASR completed and was read end to end. It confirms the complete new donor sentence at 2:26.96–2:33.82, the training explanation at 2:34.86–2:37.86, all retained city coordinates and mystery-drink differences, the complete CAT/IT example, and both closing lines. The ASR-estimated gaps surrounding the donor speech are about 0.98 s before and 1.04 s after; no clipped or duplicated wording appears in the transcript. These timings do not replace direct listening.

Narration coverage remains KEEP within the approved simplified lesson scope, provisional on listening. The new sentence describes scaling a mathematical concept, while the existing training sentence retains how the embeddings are learned. Its repeated dimensionality wording is a disclosed tradeoff of using a complete available donor sentence. All teaching-point assessments in the September 29 live evaluation remain applicable, with downstream timestamps shifted by 4.13 seconds after the graft.
