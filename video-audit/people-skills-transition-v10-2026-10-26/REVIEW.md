# People Skills v10 — explicit AI-future transition

User-requested narrow repair to v9 at the motivation board entrance. Built candidate: `Prompts/people-skills-v10.mp4`, 2:21.633, 4,249 frames at 30 fps. SHA-256: `69e9a92be3725fe33b16bd1f5fec6882c268e0351996990072550b8c60a9949c`.

The sequence now says:

> What happened with Maya matters beyond this group project.
> People skills matter even more in the AI future.
> First, you’ll stand out.

The middle sentence comes from the installed video at 1:35.000–1:38.033, replacing roll 5's generic graphic introduction at 0:50.200–0:54.433. Both replacement boundaries fall in measured silence. The live donor is raised 0.54 dB to match the surrounding measured narration level. Its output span is 0:51.567–0:54.600, with speech transcribed at approximately 0:51.84–0:54.10.

The People Skills Will Matter More board appears in full view at 0:51.567, unmarked during the new sentence. Its first card highlights at 0:54.967, aligned to “First,” then follows the existing three-card sequence and live cutaways. All other v9 teaching and visual treatment is retained. The overall timeline is 36 frames (1.2 seconds) shorter.

Verification completed:

- Fresh medium.en transcription of the encoded transition confirms the complete AI-future sentence and the return to “First, you’ll stand out,” followed by the polished-work explanation.
- Decoded all 4,249 frames; verified constant 30 fps cadence.
- Unaffected picture samples match corresponding v9 frames at a minimum 66.26 dB PSNR.
- Unaffected master speech is sample-identical to v9. The shortened segment's final 5 ms room-tone crossfade has a loop-phase variation of at most 29 PCM units; other audio outside the repair is identical.
- Encoded audio matches the new master at 45.98 dB SNR, peak −1.98 dBFS.
- All three scoped transition boundaries pass the automatic guard. Inspected their every-frame strips: clean board entry, stable board across the return to roll 5, and correctly placed first-card highlight.
- Protected source files, installed video, lesson assets, and v9 candidate retain their original hashes.

This is a review candidate, not installed or published. Direct listening and continuous playback have not been performed; voice continuity at the new donor joins still needs an ear check. `transition-review.wav` contains output 0:47–1:03 for that review. Existing full-playback limitations from v9 remain.

Build: `scripts/video/build_people_skills_v10.py`. Checks: `scripts/video/qa_people_skills_v10.py`. Source boundaries, gain and provenance: `edit-manifest.json`. Encoded wording: `encoded-transition-transcript.json`. Technical results: `qa.json`.

## Local shipment — 2026-10-26

David reviewed v10 and explicitly approved: “Looks good. Ship v10.” Installed the approved bytes at `course-assets/people-skills/people-skills.mp4`, updated the cache key to `20261026ship10`, retained the rounded `2 min` display, and updated the asset manifest hash and size. Verified working and staged metadata against the installed SHA-256.

Local commit: `503395bda55b02609ca9123d4c77dbb35a7d474a` — `Ship People Skills v10 with explicit AI-future transition`. Only the video, its manifest entry, and its lesson video reference are in this release. Unrelated working changes were preserved. **Shipped locally; queued for batch deployment.** No push or deployment was performed.

Shipment follows the user’s review acceptance; the previously disclosed limitation of no independent assistant listening/full playback is unchanged. The old installed source is preserved byte-identically as `Prompts/people-skills-v8.mp4`; future rebuilds of the historical assembly must use that file for its original live graphics and donor audio.

Removed regenerable render scratch only from this lesson’s v9, v10, and reroll audit folders. Candidates, raw rolls, reports, transcripts, manifests, and review images remain.
