# Probability & Prediction — approved shortening, November 7, 2026

Built **v10, 2:24.77**, removing **61.37 seconds** from v9 (3:26.13).
Review candidate only; the installed course video, lesson, boards, and website were not changed by this task.

- Candidate: [probability-and-prediction-v10.mp4](../../Prompts/probability-and-prediction-v10.mp4)
- Candidate SHA-256: `d53d91738f4815d88a893b121f8f01c5a10154375b3d317e809d1ebde4627c72`
- Source: `Prompts/probability-and-prediction-v9.mp4`
- Source SHA-256: `ece825d7d83cd6249a6ce240fb2c2a1cc41a21283e9cfd407f14f20055eec1b3`
- [Frame-accurate manifest](edit-manifest.json)
- [Encoded transcript](qa/probability-and-prediction-v10.txt)
- [Verification](qa/verification.json)
- [Encoded overview](qa/encoded-overview.jpg) and [join samples](qa/encoded-joins.jpg)

## Approved scope and implementation

The user approved the six proposed redundancy cuts, then approved removing the spoken coin-outcome list and reducing the names/probabilities readout to Spot alone. Adjacent cuts were combined into one edit. The optional history cut was not taken. No replacement voice or additional narration was created.

All ranges below use the original v9 timeline; ends are exclusive. Word timestamps were only starting points. Cut boundaries were refined against the actual PCM signal, preserving word tails that continue past ASR timestamps.

| Original range | Removed | New join |
|---|---|---|
| 6.933–15.233 | Claude/context opening repetition | 0:06.933 |
| 71.667–77.533 | Reading HH, HT, TH, TT aloud | 1:03.367 |
| 86.233–94.233 | Repeated one-in-four result | 1:12.067 |
| 109.533–117.867 | Preliminary explanation that the clue changes possibilities | 1:27.367 |
| 143.267–163.133 | Repeated 25%→50% result and general AI prediction overview | 1:52.767 |
| 173.200–179.767 | Repeated next-word calculation explanation | 2:02.833 |
| 182.867–187.300 | Max/17% and Buddy/14% readout | 2:05.933 |

Retained wording: “It might find a 22% chance for Spot.” The encoded ASR confirms the full phrase. Its perceptual cadence as a sentence ending still needs listening review.

Picture/audio are shortened together. Four brief picture holds/advances (0.17–0.67 seconds) replace remnants of removed scenes using adjacent approved source frames. They remove the Claude tail, coin recap tail, clue-diagram tail, and coin callback tail. No additional pause is inserted. Five-millisecond audio ramps are confined to quiet shoulders; there is no voice-level change.

## Boards and preserved scenes

Existing compact full-view treatment is preserved, with highlights following the retained source narration. No board redesign, zoom change, or global highlight pass was undertaken.

| Board | Output span | Treatment |
|---|---|---|
| Standard Probability | 0:36.23–0:52.83 | Existing unmarked arrival and formula outline |
| Counting the Possibilities | 0:52.83–1:12.73 | Scenario, outcome group, HH, calculation/takeaway; list removed while all outcomes remain visible |
| A Clue Changes the Odds | 1:27.37–1:52.77 | Unmarked arrival, ruled-out pair, remaining pair, HH, calculation; retain knowledge-change insight |
| What Comes Next? | 1:52.77–2:06.43 | Existing question/prefix/candidate outlines; all choices and the illustrative-values footnote remain visible |
| Closing message | 2:16.77–2:24.77 | Complete existing close and final frame preserved |

Longest continuous canonical-board run: approximately **36.5 seconds** (formula plus initial coin board). Clue board: **25.4 seconds**, with the numerical walkthrough retained as approved.

Supporting source scenes retained: ChatGPT opening (0:00–0:07.13), probability/history/modern-math sequence (0:07.13–0:36.23), conditional-probability introduction and first-coin peek (1:12.73–1:27.37), appended-word/repeat animation (2:06.43–2:16.77). Existing company imagery and supporting graphics retain their prior approved treatment. This is a narrow shortening, not a new whole-video visual certification.

## Verification and limits

- Fully decoded the encoded MP4: **4,343 frames, 1280×720, 30 fps**.
- Compared every encoded frame with its planned source frame, including picture overrides. Maximum mean pixel error: **3.224/255**, consistent with reencoding.
- Transition guard: **11 boundaries, zero flagged stale-frame islands**. Inspected the encoded overview and five-frame samples around all declared boundaries; the full generated strips remain available.
- Generated and read a fresh transcript from the encoded candidate. Both calculations, knowledge-change explanation, Spot/22%, context accumulation, and both closing lines remain. The agreed lists/repetition are absent.
- Encoded audio correlates **0.999982** with planned PCM; codec tail padding is 64 samples. Join shoulders are quiet (all measured 10ms RMS values below −56 dBFS), with no large sample discontinuity.
- Verified source, installed lesson video, lesson Markdown, and canonical board hashes were unchanged.
- Source limitation: one additional H.264 encode from the finished v9 video, using CRF 16; this is not a pristine-source reconstruction.
- **Not performed:** perceptual listening, continuous real-time audiovisual viewing, pronunciation/prosody evaluation, or mobile/player testing. ASR and acoustic checks do not certify these. No unconditional ship-ready verdict is claimed.

The mathematical progression and AI example remain supported by the transcript. Enumerating all four outcomes and speaking Max/Buddy were explicitly waived by the approved plan. The illustrative-values/remaining-47% qualification remains visible rather than spoken, carrying forward the accepted source treatment.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_probability_and_prediction_v10.py`

QA: `.video-venv/bin/python scripts/video/qa_probability_and_prediction_v10.py`

Transcription: `.video-venv/bin/python scripts/video/transcribe_selected_videos.py Prompts/probability-and-prediction-v10.mp4 --output-dir video-audit/probability-and-prediction-shortening-v10-2026-11-07/qa --model base.en`

The build refuses to overwrite an existing candidate. A changed render requires a new version.
