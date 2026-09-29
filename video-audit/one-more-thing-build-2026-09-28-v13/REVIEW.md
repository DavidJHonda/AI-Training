# One More Thing v13 — review candidate

Built from the three fresh September 28 rolls, with roll 1 as the narration base and roll 2 supplying the dependency sentence and full math explanation. Owner approved the wording exceptions and build. **Review only; not published.**

Candidate: `Prompts/one-more-thing-v13.mp4` — 3:27.90, 6,237 frames, 1280×720 at 30 fps.

## What changed

- Opening follows the three questions: possible continuations, temperature comparison, calculations. It no longer spends the opening on two views of a dog. The dog-name question and blank answer drawing enter with the worked example.
- Roll 1's two chart/table announcements are cut. Its categorical claim that one different choice *will* send the answer in a completely different direction is replaced with roll 2's complete sentence, “Each token the AI chooses shapes what comes next.” A cleaned branching drawing shows possible continuations.
- Roll 2's fuller math explanation replaces the compressed ending: one token, 100 generated tokens, 1,000 generated tokens, explicit multiplication, and the imagined-model qualification.
- Current canonical boards replace all generated board recreations and invented percentages. Compact full views, fixed 4 px outlines, and restrained pushes. The five selections get separate row rings at spoken pick numbers, checked with word-level ASR.
- The current close reads “Math and probability, one token at a time.” / “Every time you hit send.” Standard 48-frame hold, 150-frame push to 1.2×, 66-frame settled hold. No Notebook outro follows it.
- No midlesson pauses added. Natural gaps retained; only 5 ms edge ramps at actual audio splices. Roll 2 is raised 1.48 dB to match local active speech. The four-second tail uses quiet source audio.

Approved wording exceptions: retain “Every choice starts with calculations” without the additional “Now count what an answer takes”; retain “these weights” instead of “those weights.” No generated or synthesized speech.

## Board timing and retained drawings

| Board | Candidate time | Treatment |
|---|---|---|
| Same Probabilities, Different Choices | 0:21.50–0:37.10; 0:45.13–1:09.57 | Probability column; five pick rows; conclusion caption; banner. A 100-trial drawing breaks the explanation at 0:37.10–0:45.13. Longest run 24.43 s. |
| How Temperature Changes the Odds | 0:04.23–0:08.17 preview; 1:21.40–1:31.63 introduction; 1:35.93–2:15.50 comparison | Starting/low/high columns, Spot values, top-row comparison, banner. Behind-the-scenes drawing breaks introduction from detailed comparison. **39.57 s continuous comparison retained**: donor charts have inaccurate distributions; narration uses the side-by-side comparison throughout. |
| The Math Adds Up Fast | 2:32.70–3:07.57; 3:13.87–3:19.10 | Complete one-token, 100-token and 1,000-token cards; banner. Hypothetical-model drawing breaks at 3:07.57–3:13.87. Initial run 34.87 s includes the setup and all three calculations. |
| Current closing message | 3:19.10–3:27.90 | Unmarked canonical close; standard motion. |

Notebook drawings retained/re-timed: roll 3's branching choices at 0:00–0:04.23 and 1:18.20–1:21.40; roll 2's fixed-weight diagram at 0:08.17–0:12.17 and 2:15.50–2:30.47; roll 2's dog question at 0:12.17–0:16 and blank answer at 0:16–0:21.50; roll 2's 100-trial drawing at 0:37.10–0:45.13; roll 1's repetitive/varied name collage at 1:09.57–1:18.20; roll 2's behind-the-scenes drawings at 1:31.63–1:35.93; exact previous-live hypothetical-model still at 2:30.47–2:32.70 and 3:07.57–3:13.87. Jargon removed from branch/weights/scale donors; no new teaching figures added. Engine corner marks cleaned.

Source hashes, exact source frames, visual and audio timelines, gain, current board paths, and all splice frames are recorded in `edit-manifest.json`. The previous-live still is extracted into this audit folder and tied to the source hash; it does not silently follow a mutable live filename.

## Verification status

Prepared visual states inspected, including all board/highlight states and donor transformations. Encoded-file verification completed: all 6,237 frames decoded at 30 fps; all 19 declared boundaries passed transition_guard with zero short stray-scene flags. Inspected the complete four-second encoded contact sheets, all boundary-neighbor sheets, prepared highlight states, and the closing frame. Fresh encoded-file transcript read in full; both donor passages, the arithmetic, qualifications, and closing message are retained. Encoded audio peak is −0.45 dBFS with zero full-scale samples. All protected-file hashes are unchanged. Records: `qa.json`, `transitions/`, `transcript.txt`, and encoded contact sheets. These checks are not continuous audiovisual playback.

Ring audit: every implemented outline is rasterized at 4 output pixels. The encoded color-threshold detector reports 2–4 solid-color pixels as the moving rings cross chroma-subsampling boundaries. Investigated its thinnest case at 0:25: the raw straight side has exactly four accent pixels; the encoded side retains four dark pixels with two desaturated edge pixels. Reviewed the enlarged encoded crop; no zoom-scaled stroke or clipping. See `rings/` and `ring-raw-vs-encoded.png`.

**Listening not performed.** ASR and waveform measurements do not certify voice continuity, pronunciation, cadence, or click-free joins. Do not mark this candidate KEEP/ready to ship until that review is complete. Useful listening points:

- 0:37.10: chart-announcement removal.
- 1:18.20 and 1:21.40: short dependency donor in/out.
- 1:35.93: table-announcement removal.
- 2:34.93: full math donor starts.
- 3:19.10: return to roll 1 for the close.

Context WAVs for every join are saved as `join-<frame>.wav`. Also audition “dog,” “ChatGPT,” and the low-temperature Spot sentence, which had inconsistent automatic transcriptions in source review.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_one_more_thing_v13.py` (refuses to overwrite an existing candidate).

Verification: `.video-venv/bin/python video-audit/one-more-thing-build-2026-09-28-v13/verify.py`.

Live MP4, raw rolls, current lesson Markdown, prompt, and canonical JPGs are hash-protected. No site reference, tracker entry, or publication is changed by this build.
