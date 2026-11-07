# Probability & Prediction — flow revision v11

Review candidate: [probability-and-prediction-v11.mp4](../../Prompts/probability-and-prediction-v11.mp4), **2:44.07**, 4,922 frames at 30 fps.

Implements the user's November 7 feedback on v10. Built directly from the hash-verified v9 source, avoiding another generation of compression through v10. Installed course video, website, lesson, and canonical boards remain unchanged.

## Changes

1. Restored the complete original opening, including the 0:07–0:15 Claude/interface transition, with its original picture and narration.
2. Restored the uninterrupted readout of **Spot 22%, Max 17%, Buddy 14%** and its original board/highlights. No phrase-ending splice remains after Spot.
3. Added a **6.57-second bridge at 2:01.07–2:07.63**, between the knowledge-change insight and the dog example. The timing moves from v10's 1:52 location because the opening is restored.

The bridge displays: **“AI uses conditional probability to answer your questions.”**

Its narration is a complete existing sentence moved from v9 2:53.20–2:59.77: **“Based on the words already written, the AI calculates the likelihood for the next word in the sequence.”** The exact displayed sentence is not newly spoken. This preserves the original narrator and adds the requested explicit conditional-probability connection visually. The moved sentence appears only once.

Other approved cuts remain: the coin-outcome enumeration, repeated 25% result, preliminary clue explanation, repeated 25%→50% recap, and the old general prediction/Paris/coin-callback sequence. The history, calculations, knowledge-change insight, prompt/context example, repeat loop, and complete close remain.

## Picture and audio treatment

The new transition is a simple full-frame text card using the existing Plus Jakarta Sans font, course purple, dark ink, and pale background. No highlights, camera moves, or extra silent holds are introduced. Canonical board framing and existing highlight timing are retained for the kept source spans.

The three short adjacent-picture repairs from v10 remain: coin board held through the removed recap tail, clue board brought forward to eliminate a diagram remnant, and dog board brought forward to eliminate a callback remnant. The opening repair is no longer needed because the complete original opening is restored.

Audio uses the same v9 narrator and levels. Five-millisecond ramps are confined to measured quiet shoulders at the six new joins. No synthesized voice or extra pause is added. Source v9 SHA-256: `ece825d7d83cd6249a6ce240fb2c2a1cc41a21283e9cfd407f14f20055eec1b3`.

## Evidence

- [Edit manifest, output ranges, and candidate SHA-256](edit-manifest.json)
- [Fresh transcript from encoded v11](qa/probability-and-prediction-v11.txt)
- [Encoded bridge frame](qa/encoded-bridge.png)
- [Encoded join samples](qa/encoded-joins.jpg)
- [Verification results](qa/verification.json)
- [Transition guard report](qa/transitions/transition-guard.md)

The complete encoded transcript was read. It confirms the restored opening and all three choices, the relocated AI sentence, both numerical calculations, knowledge-change insight, repeat loop, and closing message. The bridge's source PNG, encoded frame, and five-frame samples around all nine declared boundaries were visually inspected. Transition guard passed all nine boundaries. Full decode and every-frame mapping passed; encoded audio correlation with planned PCM was 0.999989. Protected file hashes remained unchanged.

Checks use full file decode, every-frame comparison against the planned source/card, encoded audio alignment against assembled PCM, quiet-shoulder measurements, and transition-guard checks. See verification for exact results. The build protects v9, v10, the installed probability video, the lesson Markdown, and all canonical lesson JPGs by hash.

**Not performed:** perceptual listening, continuous real-time audiovisual viewing, or mobile/player testing. Automated audio and ASR checks do not certify prosody, cadence, or pronunciation. This is a review candidate, not an unconditional shipping sign-off.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_probability_and_prediction_v11.py`

QA: `.video-venv/bin/python scripts/video/qa_probability_and_prediction_v11.py`

Transcribe: `.video-venv/bin/python scripts/video/transcribe_selected_videos.py Prompts/probability-and-prediction-v11.mp4 --output-dir video-audit/probability-and-prediction-flow-v11-2026-11-07/qa --model base.en`

The build refuses to overwrite an existing candidate; future rendered revisions require a new version.
