# Probability & Prediction — spoken bridge v12

Candidate: [probability-and-prediction-v12.mp4](../../Prompts/probability-and-prediction-v12.mp4), **2:41.40**, 4,842 frames at 30 fps.

[Transition in context — 20.3 seconds](qa/transition-context.mp4)

The user's two new uploads were inspected for the requested pickup. **math-line-1** contains the exact complete sentence, and its extracted clip independently transcribes as:

> AI uses conditional probability to answer your questions.

The full transcript of math-line-2 does not contain that exact sentence. Selection is based on the wording and measured audio handles/levels, not a claimed perceptual audition of the voices.

## Edit

- Donor: `Prompts/math-line-1.mp4`, SHA-256 `70c52323512282929897a9b2d07f40eaa4e94754a77a80ba42c065719fe1dbe3`.
- Extracted donor interval: **0:29.700–0:33.600**, source frames **891–1008**, end exclusive. The handles preserve the complete attack and ending sibilant, not merely the ASR word timestamps.
- Output bridge: **2:01.067–2:04.967**, frames **3632–3749**. The dog example follows immediately.
- Replaces v11's title card and the relocated “Based on the words already written…” explanation. Neither remains in v12.
- Picture: the current canonical **What Comes Next?** board, full view and unmarked during the pickup; existing narration and highlighting resume for the dog example. No donor visuals are used.
- Preserves the restored opening and full Spot/22%, Max/17%, Buddy/14% readout, other approved cuts, history, both calculations, knowledge-change insight, repeat animation, and complete closing sequence.

The donor receives **+1.7 dB** gain, leaving it within **0.915 dB** of the adjacent speech's measured active RMS. The full RMS target of +2.615 dB would clip 12 samples; the smaller gain preserves peak headroom without limiting or changing the base narration. Five-millisecond ramps are confined to quiet shoulders. No extra pause or synthesized voice is inserted.

The full video is assembled directly from finished v9 plus the donor in one H.264 encode (CRF 16), not transcoded from v11. v9 is the available finished source, not a pristine-source reconstruction. Prior candidates, both uploaded donors, the installed probability video, the lesson, and all canonical boards are protected by hashes. No website or installed-course change is made.

## Evidence and verification

- [Donor 1 transcript](donors/math-line-1.txt), [donor 2 transcript](donors/math-line-2.txt)
- [Isolated pickup transcript](donors/isolated-check/transition-line-selected.txt)
- [Selection and level measurements](donor-selection.json)
- [Edit manifest and candidate hash](edit-manifest.json)
- [Encoded candidate transcript](qa/probability-and-prediction-v12.txt)
- [Verification results](qa/verification.json)
- [Encoded join samples](qa/encoded-joins.jpg)
- [Transition guard](qa/transitions/transition-guard.md)

Checks cover full decode, every encoded frame against the planned source/board, audio alignment against assembled PCM, quiet join measurements, and transition detection. Full decode and all-frame mapping passed. All nine transition-guard boundaries passed; five-frame samples at every declared boundary were visually inspected. Encoded audio correlation was 0.999988. Protected hashes remained unchanged. The normalized full v12 transcript matches v11 exactly except for replacing the old explanation with the requested sentence; see [narration comparison](qa/narration-change-check.json). Exact results are recorded in verification.json.

**Listening limitation:** no perceptual listening or continuous real-time audiovisual viewing was performed. Transcript and signal checks establish the words, timing, and levels but do not certify voice match, cadence, or audible seams. The context clip is provided for listening review. This is a review candidate, not an unconditional shipping sign-off.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_probability_and_prediction_v12.py`

QA: `.video-venv/bin/python scripts/video/qa_probability_and_prediction_v12.py`

Transcribe: `.video-venv/bin/python scripts/video/transcribe_selected_videos.py Prompts/probability-and-prediction-v12.mp4 --output-dir video-audit/probability-and-prediction-spoken-bridge-v12-2026-11-07/qa --model base.en`

The build refuses to overwrite an existing candidate. Subsequent renders require a new version.
