# Loudest Voices v12 — remove the redundant opening sentence

**Shipped locally on David’s approval; queued for batch deployment.** See [release record](SHIP.md). The review below records the pre-shipping checks.

David requested deleting “Even at the highest levels, the experts themselves do not share a unified vision.” The cut removes source v11 frames 708–863 (23.600–28.800 seconds), with both endpoints inside measured quiet gaps. It joins “Same field, same evidence, very different bets” to “First, the Optimist, Dario Amodei.”

Candidate: `Prompts/loudest-voices-v12.mp4`. Runtime **4:36.733**, 5.2 seconds shorter; 8,302 frames at 30 fps, 1280×720. Review only; not installed or committed. The already-shipped Embrace opener is unchanged.

Our board still enters at 19.900 seconds. It stays at full view through the cut and moves to Dario's identity at the shifted onset, 23.900 seconds. No new pauses or other narration changes. Five-millisecond fades are confined to the quiet join handles.

All 8,182 unaffected video packets match v11 exactly, with later timestamps shifted by 156 frames. Only the continuous native-board segment was re-encoded (120 frames). Audio comes from the retained pre-AAC v10 assembly, verified against v11 at correlation 0.999808, avoiding another generation of AAC compression. It is cut on exact samples and encoded once.

Verification passed: full decode and presentation timing; every replacement board frame; packet identity of all retained video; audio correlation 0.999829 to the intended edit; quiet join with negligible sample step; transition guard at the board entry, audio join, and resumed identity view. Inspected the contact sheet and every-frame strip through the new join. Fresh transcription of the first 34 seconds confirms the sentence is absent and both neighboring phrases remain. Listening was not performed; review the new join using **Sentence cut · 0:21** on the combined review page.

SHA-256: `31a18fc49cc76e576ea736d23160bc516f486e9160df6557c5f0a018ad4edc37`.

Build: `scripts/video/cut_loudest_sentence_v12.py`.
QA: `scripts/video/qa_loudest_sentence_v12.py`; `qa.json`; `transcripts/`; `transitions/`.

[Review both videos](../remove-doubter-2026-10-22/review.html).
