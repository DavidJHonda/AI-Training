# Big Downside v7 — built for review

User instruction: “Build it,” following the three-roll evaluation. Scope: full production review candidate using Roll 3 as the base, with feasible source-audio repairs. Building does not imply shipping approval.

Candidate: `Prompts/big-downside-v7.mp4`. Encoded and decoded: **4:10.47**, 7,514 frames, 1280×720, 30 fps.

## What changed

- Restored the phone-excitement/AI-concern opening and the qualified “Because greater capability can create greater risk” from the earlier finished v6. Picture uses the new Roll 1 opening.
- Removed Roll 3’s statement that all protection is external. Roll 2 supplies “They rely on multiple layers of protection to keep the system acting safely.” Its board walk restores refusal, permissions, and human approval and removes the “physically” restriction.
- Added Roll 1’s patched-vulnerability/new-methods/cat-and-mouse explanation.
- Added Roll 1’s unauthorized-communication sentence before Roll 3 explains outside access and the Hugging Face intrusion.
- Replaced all four Notebook course-board reproductions with the current canonical JPGs and timed 4 px outlines; restored the illustrated jailbreak board.
- Preserved the ordinary-capabilities-to-harm sequence, network/Spot drawings, benign-intent examples, safety-lag chart, and red-team scenes. Added Roll 2’s short boundary-route drawing as a break during the communication graft.
- Replaced the source close and branded tail with the canonical closing asset, 48-frame hold, 150-frame push to 1.2×, and settled hold. Both original closing sentences remain.
- Applied existing corner-mark cleanup to kept Notebook frames. No new teaching pauses or generated voice were added.

## Audio changes and listening locations

Cut points use small.en word timing and quiet waveform boundaries. Donor gain uses active-speech RMS relative to Roll 3; this is a level estimate, not a perceptual voice-match certification. Adjacent pieces of uninterrupted source audio have no fades; only disjoint audio edits have 5 ms room-tone fades. All donor source files and hashes are protected in the manifest.

| Output | Source audio | Gain | Content |
|---|---|---|---|
| 0:00.00–0:11.60 | big-downside-v6.mp4, 0:00.00–0:11.60 | -3.45 dB | Opening restored: phone excitement, AI question, capability can create risk |
| 0:47.03–0:50.97 | big-downside-2.mp4, 1:08.20–1:12.13 | -0.45 dB | Graft: They rely on multiple layers of protection to keep the system acting safely |
| 0:50.97–1:08.03 | big-downside-2.mp4, 1:12.13–1:29.20 | -0.45 dB | Graft: safety training, screening, permissions and human approval |
| 1:41.93–1:49.53 | big-downside-1.mp4, 1:54.40–2:02.00 | -0.33 dB | Graft: patched vulnerability, new methods, ongoing cat-and-mouse |
| 2:57.13–3:01.47 | big-downside-1.mp4, 3:23.30–3:27.63 | +1.00 dB | Graft: unauthorized communication outward; supporting boundary-route drawing |

Listen in context at **0:11.60, 0:47.03, 1:08.03, 1:41.93, 1:49.53, 2:57.13, and 3:01.47**. The opening uses an earlier finished render and therefore has an additional prior encoding generation.

## Board treatment

| Board | Output spans | Highlight treatment |
|---|---|---|
| Layers of Protection | 0:50.97–1:11.77 | Safety Training → Screen for Harm → Limit What AI Can Do → takeaway |
| Why Jailbreaks Keep Appearing | 1:33.63–1:49.53 | Defenders’ sign → attacker’s sign → cat-and-mouse banner |
| The Voice-Clone Scam | 2:08.73–2:24.03 | Voice Clip → Voice Cloned → Fake Call → Call Back |
| A Test Became a Real Cyberattack | 2:47.73–2:57.13; 3:01.47–3:12.97; 3:16.97–3:20.73 | Assignment → Boundary Crossed → Harm; return for cheating banner |
| Closing Message | 3:57.40–4:10.47 | Unmarked canonical asset; standard close motion |

All boards stay at full view, with complete card or sign outlines. The longest unbroken course-board span is **20.80 seconds**, Layers of Protection. The voice board opens unmarked for approximately 1.47 seconds before its first item’s spoken onset; this uses the Edit Spec exception for an introduction shorter than two seconds, with no artificial pause. The cyberattack board is broken by the 4.33-second boundary-route drawing and the 4-second audit-record drawing.

## Remaining issues and honest status

**Review candidate, not certified ready to ship.** These build repairs improve the strongest roll; they do not change the earlier review into a KEEP.

- The narration still does not explicitly explain screening harmful outgoing answers.
- Callback still says “the real number” rather than explicitly “the number you already have.”
- Concrete permission examples such as sending money/deleting files remain visible but unspoken.
- Four required wording entries remain paraphrased: “Three ideas help explain why”; the two-sentence layers refrain; the record-alteration sentence; and “As AI becomes more capable, the protections have to keep up.” The opening now restores its required wording, and the two final lines remain correct.
- The capability chart is retained as an illustrative comparison. Its dated/numbered axes remain subject to the visual-review qualification in the comparison report.
- Direct listening and real-time end-to-end playback are unavailable to this agent. No claim is made that voice continuity, delivery, clicks, animation timing, or all visual details have been perceptually certified. Review the listed joins before shipping.

## Verification record

Build: `.video-venv/bin/python scripts/video/build_big_downside_v7.py`
QA: `.video-venv/bin/python scripts/video/qa_big_downside_v7.py`

The manifest contains source identities, gain values, all picture boundaries, audio seams, canonical board paths and ring onsets, the close treatment, and protected-file hashes. `qa.json` records decoded frame count, encoded-audio correlation and board-image comparisons; `transitions/transition-guard.json` records every declared seam. Transcription of the assembled audio is retained under `transcripts/`; it does not replace listening.

- Full decode confirms 7,514 frames, 30 fps, 1280×720. Encoded AAC correlation with the assembled PCM is **0.999985**; the 384-sample length difference is within the encoder-padding allowance. This confirms alignment, not perceptual voice matching.
- All 31 sampled encoded board states match their render references within the declared image-difference tolerance. The overview, board states, final closing frame, and boundary strips were visually inspected.
- The transition detector returned two flags and exit status 1. Both were reviewed from their decoded frame strips: at frame **5032**, the preceding server/shield animation has a regular motion step at frame 5031 (delta 8.0, compared with 7.7–7.9 on nearby motion steps), then cuts directly to the canonical board; at frame **5789**, the destination audit-log drawing gradually fades in. Neither inspected strip shows an intervening stale graphic. These are manual adjudications of detector false positives; the original automated failure record is retained unchanged.
- The ring scan completed. Authored outlines use the shared renderer's 4 px setting. The encoded color-threshold measurements are chiefly 4 px, with some teal and purple edges measuring 5 px; retain this rasterization qualification rather than claiming every encoded edge measures exactly 4 px. The 10–15 px amber/gold detections occur in retained source illustrations, outside the replacement course-board outlines.
- Source rolls, earlier donor, lesson Markdown, live Big Downside video, and canonical JPG hashes are unchanged. `index.html` changed concurrently in another task, solely to update The Next Token video cache key. The saved diff and Big Downside-specific signature confirm this lesson's section and asset references are unchanged.

Candidate SHA-256: `86f1f804ff1e857f4284160940b2f3286fff17e293394d2dd89bb72ef7146c7b`.

No Git commit, installation, push, or deployment is part of this build.
