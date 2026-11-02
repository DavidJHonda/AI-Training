# AI is Different v16 — built November 2, 2026

**Candidate:** [ai-is-different-v16.mp4](../../Prompts/ai-is-different-v16.mp4) — **4:29.167**, 1280×720, 30 fps, 8,075 decoded frames.

**Status:** built for review under David's “Build it please” authorization. The approved [best-of plan](../ai-is-different-rolls-7-9-2026-11-02/REVIEW.md) is implemented. No installation, commit, or publication was performed. The live video, lesson, and all source boards remain unchanged.

## What changed

Roll 8 carries the lesson. Roll 9 supplies the complete three-song table read and the exact two closing sentences. All four boards are the current course assets, including the illustrated cooking board and captionless playlist board with Traditional Software/AI headings. Whole-card/section rings follow the narration. The closing board holds 48 frames, pushes to 1.2× over 150 frames, then settles for 19 frames; it is the literal final frame.

The digital/handwritten comparison and note close-ups come from roll 7. Its chef drawing and the live video's robot/recipe/cupcake sequence break up the cooking board. The live picture donor is the immutable v15 candidate, verified byte-identical to the installed video at evaluation. Roll 8's useful training and mistake animations remain. Roll 9's lock-and-magnifier drawing replaces the phone graphic with malformed labels.

No extra teaching pauses were added. Visual-only cuts preserve contiguous base PCM exactly. Only the three actual narration joins have 5ms fades to measured source room tone. Roll 9 receives −0.09 dB gain to match the measured integrated levels (roll 8 −20.33 LUFS, roll 9 −20.24 LUFS).

## Narration and listening status

**All essential teaching is present in the encoded-file transcript; all nine mandatory lines match.** This is a content verification, not a completed listening verdict. The complete rendered transcript was read against the current lesson and the prior comparison. The table now includes “As It Was by Harry Styles,” and the final words are exactly “Different jobs need different tools. Choose the tool that fits the work.”

| Teaching | Encoded candidate assessment |
|---|---|
| Expectations; patterns and unstructured data as the two differences | TAUGHT, 0:00–0:29; predictability consequence taught in the downside |
| Spotify exact match; programmer instructions; calculator/spreadsheet | RICH/TAUGHT, 0:30–0:55 |
| Password condition, green/red outcomes, same-result takeaway | RICH, 0:56–1:28 |
| Training learns patterns to answer you; people still write the code | RICH/TAUGHT, 1:28–1:39; both exact lines retained |
| Robot recipe/repetition; chef ingredients, methods, substitutions, no recipe | RICH, 1:40–2:26 |
| Structured fields versus unstructured input; “usually” and “can help” | RICH, 2:27–2:55 |
| Same playlist; explicit software/AI sides; all songs, artists, order | RICH, 2:55–3:23; roll-9 table donor completes the worked example |
| Start-here/last-song arrows and excluded Shake It Off | RICH, 3:24–3:45 |
| Training explains handwriting, language, arrows and cross-outs | RICH, 3:46–3:58; exact required explanation |
| Harder prediction/inspection; missed cross-out; polished mistakes | RICH, 3:58–4:21 |
| Match tool to work; exact two-line close | TAUGHT, 4:22.32–4:25.66 |

The smaller ASR model again rendered “know to skip” as “notice skip.” A separate medium.en check on the unchanged source phrase transcribes “How does the AI know to skip a song that is clearly written right there on the page?” This supports retaining the sentence; it does not constitute listening.

**Listening not performed:** voice continuity, cadence, pronunciation, breath tails, and subjective pacing remain for playback review. Continuous motion with sound was not watched end to end. No full shipping KEEP verdict is claimed.

### Narration joins to audition

| Edit | Exact source frames and output placement | Encoded quiet gap containing join |
|---|---|---|
| Table entry | Base 8 ends at f5722 (190.733s); roll 9 f5349–5600 replaces base f5722–5951. Donor plays at 3:10.733–3:19.100. | 190.474–190.903s; join RMS −77.75 dBFS |
| Return after table | Base 8 resumes f5951 at output f5973 (199.100s), before “On the right…” | 199.034–199.673s; join RMS −75.72 dBFS |
| Exact close | Base 8 ends f7836; roll 9 f7341–7558 begins at output f7858 (261.933s). | 261.377–262.245s; join RMS −77.57 dBFS |

Short context excerpts: [table joins, output 3:05–3:25](table-join-review.mp4) and [closing join, output 4:15–end](closing-join-review.mp4). All cuts use measured quiet gaps, preserve entire sentences, and retain the preceding/following references. The source-to-output map is in [edit-manifest.json](edit-manifest.json).

## Supporting visuals and board timing

| Output time | Picture source | Teaching purpose |
|---|---|---|
| 1:04.300–1:08.833 | Roll 8 f1190 onward | Entering/checking a password |
| 1:50.800–1:58.533 | v15 f3840–4072 | Recipe-following robot and repeated cupcakes |
| 2:09.000–2:16.000 | Roll 7 f3694–3904 | Ingredients and cooking methods |
| 2:55.367–2:59.600 | Roll 7 f7093–7220 | Digital organization versus handwritten information |
| 3:19.100–3:27.633 | Roll 7 f5176–5432 | Handwriting, title, arrow, crossed-out song |
| 3:45.567–3:58.400 | Roll 8 f6745–7130 | Training patterns and interpreting notes |
| 3:58.400–4:03.833 | Roll 9 f6647–6726, then final-frame hold | Inspection/predictability; replaces distracting phone labels |
| 4:13.100–4:21.933 | Roll 8 f7571–7836 | Cross-out/order mistake reveal |

The longest continuous board hold is **19.567s**. Rules board holds are 8.067s and 19.567s; cooking holds 11.033s, 10.467s, and 11.300s; playlist holds 19.500s and 17.933s. Each board first appears complete and unmarked for at least two seconds. Return visits resume the relevant highlight. The input/condition portion of the rules walk is partly covered by the approved lock drawing; the branch and takeaway rings remain on the board.

## Verification completed

- Entire MP4 decodes: 8,075 video frames, matching the planned duration and edited audio sample count.
- All **19 declared boundaries pass** `transition_guard.py`; all 25-frame boundary strips were visually inspected, along with outgoing/destination summaries. No stale intermediate board or donor frame was identified.
- Complete encoded transcript inspected; **9/9 required sentences matched**, with punctuation and hyphenation normalized. See [required-lines-check.json](required-lines-check.json).
- Audio peak **−1.58 dBFS**, no clipped samples. The three narration joins lie in detected quiet gaps. No new lesson pauses; original section transitions preserved. See [encoded-audio-qa.json](encoded-audio-qa.json).
- Canonical board openings, every visible settled ring state, and final closing frame inspected at delivery resolution. Rings use the shared fixed **4px** rasterizer. The strict RGB detector reports thinner solid-color cores on some compressed blue/purple edges; pixel profiles confirm four-pixel coverage in those examined sections. Unrelated detected shapes in Notebook drawings are excluded from the course-ring assessment.
- Full-video contact sheets, denser robot/training/mistake sequences, and all transition strips inspected. These are frame-sequence checks, not continuous audiovisual playback.
- Corner cleanup: 3,426 cloned frames, 1,264 glyph-inpainted frames, **zero declined frames**. Already-cleaned v15 footage was left alone.
- Protected source and asset SHA-256 hashes unchanged; unchanged base PCM outside the audio-seam fades compared exactly.

**Candidate SHA-256:** `2581711f20abd117913fd6fa44a3136e3631f3d131bc5bfa3c6c96cf5f570ae2`

Build: `.video-venv/bin/python scripts/video/build_ai_is_different_v16.py` (refuses to overwrite an existing candidate).

QA: `.video-venv/bin/python scripts/video/qa_ai_is_different_v16.py`, then `--transcribe`; `ring_stroke.py` at one-second intervals; FFmpeg decode/silence/peak checks. Details and evidence remain in this directory. Remaining release checks are listening and continuous audiovisual playback; local shipping still requires authorization.
