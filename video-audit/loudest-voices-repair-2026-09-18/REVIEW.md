# Loudest Voices — best-of repair review

## Recommendation

**KEEP the repaired candidate for owner review; do not publish yet.** The planned repair is complete and the candidate preserves the lesson's essential teaching. Visual QA, transcript QA, frame accounting, and transition checks pass. This Codex session cannot ingest audio for perceptual listening, so an owner ear-check of the two narration joins remains required before publication.

## Scope

- Candidate: `Prompts/loudest-voices-v3.mp4`
- Base roll: `Prompts/loudest-voices-1.mp4`
- Donor roll: `Prompts/loudest-voices-2.mp4`
- Duration: 3:54.90 at 30 fps
- Planned and decoded frames: 7,047
- Output SHA-256: `5d27132b13819c427ab24bd710bc7cddd24b2d469fccdd5822a174537d5b444b`
- Review candidate only. The existing lesson, upload Markdown, source videos, course boards, and live course video were not changed.
- No deployment or publication was performed.

## Narration repair

Roll 1 remains the base. Its Dario Amodei section was replaced with the fuller Roll 2 version.

- Replaced from Roll 1: 0:35.37–1:00.90 (safe quiet-frame boundaries; spoken material approximately 0:35.82–1:00.52).
- Donor from Roll 2: 0:45.83–1:13.40 (safe quiet-frame boundaries; spoken material approximately 0:46.18–1:12.78).
- Candidate placement: 0:35.37–1:02.93.
- Donor gain: +1.1 dB to match the neighboring Roll 1 speech level.
- Join treatment: 5 ms matched-room-tone crossfades at both ends.
- Added teaching pauses: none.

The completed timestamped transcript contains the full teaching sequence:

1. Three experts working from the same evidence make different bets.
2. Dario Amodei's optimistic claim and his warning about humanity's maturity.
3. Geoffrey Hinton's risk warning and his cancer-detection upside.
4. Yann LeCun's LLM skepticism and his acknowledgement of controllable risk.
5. The synthesis: the Optimist sees danger, the Worrier sees benefits, and the Doubter acknowledges risks.
6. Four historical misses: Clifford Stoll/online shopping, Steve Ballmer/iPhone, Robert Metcalfe/internet collapse, and Henry Ford/flying cars.
7. The distinction that technological capability alone does not determine adoption; human habits change the result.
8. The conclusion: where AI will be in ten years is a bet, and which voice to listen to is the student's call.

The automatic transcript phonetically misspells some proper names (for example, "Amote" and "Lechin"). Those are ASR renderings, not on-screen text changes. Because perceptual audio input was unavailable, exact pronunciation remains part of the owner ear-check.

## Visual and production review

- The expert board opens in full, then uses restrained complete-card moves and 5 px rings for each expert, claim, and counterpoint. The tall card layout remains uncropped.
- The historical-predictions board opens in full, moves to each complete example card, then returns to the full takeaway banner.
- Safe Notebook drawings interrupt the longest board passage: the AI-system/human silhouette for Hinton and the "A DEAD END" drawing for LeCun.
- The longest unbroken course-board run is approximately 42.2 seconds.
- All source photographs in the repaired spans are covered: Hinton, LeCun, the shopping mall, Steve Ballmer, iPhone imagery, the old computer, and Henry Ford.
- The canonical close is used and settles for four seconds after narration.
- Corner-mark cleanup completed with 1,116 cloned frames and 482 inpainted frames; no frames were declined.
- Full 4-second visual contact sheets were inspected from start to finish. No blank frames, unexpected photographs, broken crops, stale frames, or close-card errors were found. This was a sampled full-timeline inspection, not continuous real-time playback.

## Verification

- `transition_guard.py`: **PASS**, 11/11 declared boundaries, 0 failures.
- Manual every-frame transition strips: inspected for all 11 boundaries; no short visual islands or stale transition frames found.
- Full candidate transcription: complete through the final sentence; no missing teaching point found.
- Silence detection: both narration joins land in measured quiet. The splice-start gap is 0.40 s and the splice-end gap is 0.68 s; no accidental long pause was introduced.
- Audio stream: AAC-LC, 48 kHz mono. Whole-program mean is -17.8 dBFS. Peaks reach 0 dBFS in both supplied rolls as well as the candidate; the candidate does not introduce a new program-wide peak ceiling.
- Protected-file hashes: unchanged for both source rolls, all three course boards, and `lessons/loudest-voices.md`.

## Remaining owner check

Listen to the candidate around 0:32–0:39 and 0:59–1:07 to confirm the Roll 1/Roll 2 voice match and cadence at both joins. Then listen through the close at 3:42–3:55. Publication remains unapproved until that perceptual check is complete.
