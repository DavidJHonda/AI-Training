# Does AI Think? — v9 review candidate

Built 2026-09-29 from the approved best-of proposal. Candidate: `Prompts/does-ai-think-v9.mp4`, **3:36.20**, 1280×720, 30 fps, 6,486 frames. This is a review build; the published video, lesson copy, canonical JPGs and three raw candidates are unchanged.

Candidate SHA-256: `0f9f12e310a522ca97a867e0436ac04795173bee8e6e93491aef9321c4a7f8c9`.

## What changed

- Candidate 2 supplies the entire teaching body through 3:28.20. Its useful drawings and animations retain their motion and original timing.
- Candidate 3 supplies only its two exact closing sentences, source 3:04.00–3:09.40. The spoken “Slight pause for emphasis,” redundant closing introduction and engine outro from Candidate 2 are gone. Donor speech measured −21.21 LUFS versus −20.61 LUFS for the preceding base passage; the donor receives +0.6 dB gain. Five-millisecond ramps sit inside the silent handles.
- Both course-board recreations are replaced by the exact current canonical JPGs. The comparison photo panel is restored. The Chinese Room uses the approved camera-only walk; the comparison uses uniform complete-row framing, green 4 px outlines at spoken onsets, and a purple takeaway outline.
- Five supporting cutaways interrupt long board runs, with no extra pauses in the teaching body.
- The closing animation's footer “Internal Process Differs: Pattern Matching ≠ Understanding” is replaced by “Similar answers can come from different processes.” The surrounding animation is preserved. This removes the categorical implication identified in the evaluation's conditional visual review.
- All 3,336 retained/donor Notebook frames pass through corner-mark cleanup: 2,467 paper clones, 869 glyph inpaints, zero declined frames. Canonical boards and the generated photo have no added mark.
- The canonical close runs for eight seconds: 48-frame full hold, 150-frame push to 1.2×, 42-frame settled hold. After the 5.4-second donor audio span, 2.6 seconds of source-matched room tone carry the remaining motion and hold. The literal last frame is the settled canonical close.

## Board treatment and breaks

| Board | Treatment | Actual board windows | Longest uninterrupted run |
|---|---|---|---|
| The Chinese Room | Full unmarked opening; camera visits complete Step 1, Step 2, phrase chart, Step 3 and outside-observer callouts; returns to full view for takeaway | 1:00–1:06; 1:09.50–1:25.70; 1:32–1:50.17 (40.37 s total) | 18.17 s |
| When You Think. What AI Does. | Full unmarked opening; Meaning 2:16.33, Experience 2:24.03, Word choice 2:33.03, Beauty 2:42.53, Uncertainty 2:52.77; pullback starts 3:04.57 and takeaway outline starts 3:05.57 | 2:07.97–2:20.50; 2:23–2:38.70; 2:41.50–2:58; 3:01.50–3:09.90 (53.13 s total) | 16.50 s |
| Sounds human. Works differently. | Unmarked canonical close; standard hold/push/settle | 3:28.20–3:36.20 | 8 s |

| Supporting insert | Output | Source and purpose |
|---|---|---|
| Door and incoming note | 1:06–1:09.50 | Candidate 2, frames 1387–1492; incoming note |
| Person inside room | 1:25.70–1:32 | Candidate 2, frames 1589–1778; internal rule-following |
| Learned network/input | 2:20.50–2:23 | Candidate 2, 2:02–2:04.50; learned patterns under Meaning |
| Next-word prediction | 2:38.70–2:41.50 | Candidate 1, 0:27–0:28.60, slowed to 2.8 s; preserves the reveal and completed “horizon” example |
| Student checking an answer | 2:58–3:01.50 | New realistic photograph with a restrained 3% push; comparing laptop response with a reference book |

**Timing correction to evaluation:** Candidate 1's prediction animation is at 0:27, not the proposed 2:33–2:40. The latter contains the recreated comparison board. Sequential inspection established the usable source before rendering; the intended prediction insert and output timing are preserved.

The [generated photo](student-checking-source.png) was made with the built-in imagegen tool. Its exact final prompt and source location are saved in [image-generation.md](image-generation.md).

## Retained supporting scenes

Candidate 2's opening chat, explanation/joke/apology sequence, student at laptop, question chip, human/model comparison and sentence/poem/conversation animation remain through 0:40.70. Its output/comprehension drawing remains at 0:40.70–0:46.23 as a distinction between output and understanding, under the narration's explicit caution. The door/plaque/room setup remains at 0:46.23–1:00.

The rulebook → learned network → input → predicted output sequence at 1:50.17–2:07.97 is preserved, including its illustrative probabilities. The files/gears and analytical-organization animation at 3:09.90–about 3:22 remain, followed by the human/model process comparison with the corrected footer. These are independent teaching illustrations rather than course-board recreations.

## Verification and limits

See `qa.json`, `transition-run.txt`, `transitions/`, `ring-check/`, `encoded-review/`, and the encoded contact/corner sheets for checks on the finished MP4. Source/asset hashes and the exact source-to-output mapping are in `edit-manifest.json`.

Completed on the final encoding:

- Decoded all 6,486 frames at 30 fps and confirmed 1280×720 throughout, no black frames, and the canonical last frame.
- Inspected all five whole-video contact sheets, board/cutaway state previews, four corner sheets and every-frame strips around all 16 declared edits. No leaked board recreations, engine marks or stale intermediate shots were seen in those samples. The blank-paper start at 1:50.17 is the original retained animation's reveal, not a flash of an old board.
- Transition guard: 16 boundaries, zero failures. Render/encoded preview comparisons: minimum 36.38 dB PSNR, including JPG preview compression.
- Comparison outlines: all 40 detected green course-ring samples measured 4 px. Three wider gold detections at 0:17–0:18 are parts of the student drawing, not course outlines. The purple banner measures 4 px when its anti-aliased edge is included (80 RGB-distance threshold); its fully saturated core is 3 px. Geometry uses the shared fixed-4-px renderer throughout.
- Base speech alignment: minimum one-second waveform correlation 0.999866 with Candidate 2; donor closing correlation 0.999981 with the assembled master. These establish alignment and retention, not listening quality.
- Final encoded graft gap, measured at −35 dB: **3:27.843–3:28.314 (0.471 s)**. No additional gap was inserted before the close. Final speech falls below that threshold at 3:33.318; the video finishes at 3:36.200 (AAC decoder tail extends to 3:36.213).
- Full encoded transcript confirms both closing sentences, with no spoken pause instruction or engine outro. Base-model segment times drift around the graft; source word timing and measured waveform boundaries govern the edit.
- All protected raw sources, live video, lesson text and canonical JPGs retained their original hashes.

**Listening and continuous playback are not completed.** No available tool in this session provided audio perception; transcript, waveform and level checks are not substitutes. Before a shipping verdict, listen end to end, especially:

- **0:39:** “without dropping the thread/threat.” Both source ASR passes reported “threat”; this could be pronunciation or transcription. The optional clause is retained because an error has not been confirmed. Context clip: `pronunciation-review-39s.wav`.
- **3:28.20:** the only voice graft. Check voice identity, cadence, level and consonant boundaries. Context from the final encoding: `encoded-closing-review.wav`, starting at output 3:21.50.

The previously identified voice weaknesses “regurgitating” and “You inherently notice” are retained under the approved minimum narration repair. No new full KEEP/ready-to-ship verdict is asserted from automated evidence.

## Reproduction

```sh
.video-venv/bin/python scripts/video/build_does_ai_think_v9.py --prepare-only
.video-venv/bin/python scripts/video/build_does_ai_think_v9.py
.video-venv/bin/python scripts/video/qa_does_ai_think_v9.py
.video-venv/bin/python scripts/video/grade_bundle.py video-audit/does-ai-think-build-2026-09-29-v9/encoded-review Prompts/does-ai-think-v9.mp4
.video-venv/bin/python scripts/video/ring_stroke.py Prompts/does-ai-think-v9.mp4 video-audit/does-ai-think-build-2026-09-29-v9/ring-check --step 1
```

The builder refuses to overwrite an existing review candidate. Preserve the generated photo and version output paths for any revision. No installation, commit, push or deployment was performed.
