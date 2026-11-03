# Pace of Change v12 — review candidate

Built November 3, 2026 under the owner's “Agree. Build it” approval of the three-roll evaluation and best-of plan. **Candidate: `Prompts/pace-of-change-v12.mp4`, 3:42.233, 1280×720, 30 fps, 6,667 frames.** Full production pass from pristine rolls, with one final H.264/AAC encode. Installed and committed locally on November 3 after the owner’s “ship it” approval. Queued for batch deployment; not pushed or deployed.

SHA-256: `b95735d476d8bd6747c2cf6af1cfab91bf04bd1a6caad101f1aee86530cfed8e`.

## Assembly

Roll 1 supplies the narration spine. Roll 2 supplies two complete passages; roll 3 supplies supporting drawings only. Exact source identities, hashes, source/output frame mappings, gains, board assets, and picture placements are in `edit-manifest.json`. Original evaluation: `../pace-of-change-comparison-2026-11-03/REVIEW.md`.

| Donor passage | Roll 2 source | Candidate position | Gain |
|---|---|---|---|
| Complete image comparison | 0:45.400–1:00.100 | 0:25.767–0:40.467 | −0.331 dB |
| Releases are designed to improve capability, speed, and cost | 1:51.500–2:01.533 | 1:32.833–1:42.867 | −0.349 dB |

The five approved deletions remove the projection introduction, obsolete/exponential claims, excess limitation rhetoric, the misleading present-day autonomous loop, and the redundant closing lead-in. The release replacement also removes the “complete shift” aside. Boundaries follow the approved quiet handles, rounded to 30 fps. No narration was generated, and no pauses were inserted. Five-millisecond fades apply only at actual narration joins; picture cuts do not touch the audio.

The full small.en transcript retains all four required lines, both data volume and quality, the human-directed coding explanation, RSI/AGI/ASI definitions, the absence of an agreed AGI definition/test, and the explicit uncertainty qualifier. This is transcript verification, not listening. See `transcript.txt` and `candidate-asr.json`.

## Boards and supporting pictures

All three teaching boards are the current canonical assets, held in full view. Four-pixel outlines follow the comparison rows and the complete driver/future cards. Each board first appears unmarked for more than five seconds. The future headings use the approved full terms and initials on two lines. No retired banners or old four-idea layout appear.

| Board | Candidate topic interval | Treatment / interruptions |
|---|---|---|
| ChatGPT: 2023 vs. 2026 | 0:04.600–1:17.567 | Answering, images, context, doing; computer, user, and code cutaways. Longest continuous exposure: 24.067 s. |
| Why So Fast? | 1:48.067–2:43.600 | Training, compute, AI helps build AI; server aisle and human programmer cutaways. Longest continuous exposure: 23.700 s. |
| Three Future Ideas | 2:43.600–3:27.533 | RSI, AGI, ASI; loop and human-work cutaways; clear outline for the qualifier. Longest continuous exposure: 17.500 s. |
| Closing message | 3:34.733–3:42.233 | Canonical close: 48-frame hold, 150-frame push to 1.2×, 27-frame settled hold. Literal final frame is the course close. |

Supporting scenes retain drawn conversation, competition/race imagery, frequent releases, capability/speed/cost dials, crossed-out “IMPOSSIBLE,” computing infrastructure, human coding, a recursive loop under explicitly hypothetical narration, and a question mark/server rocket under the uncertainty qualification. The dials are an illustrative animation without attribution to a particular benchmark. Unsupported error-rate/human-baseline charts, projection graphics, and the branded endcard are excluded. No Notebook stock photography is used.

Version 11 was an internal first assembly. Frame inspection found four short donor-scene leaks. Version 12 holds the last valid donor picture for 2, 4, 6, and 5 frames at those ends, removing the leaks without changing narration or timing. Its preencode audio is byte-identical to v11. Source motion was examined through sequential frames and strips; continuous audiovisual playback remains unperformed.

## Verification and remaining review

- Full FFmpeg decode: no errors. Sequential frame count and dimensions match the plan.
- Transition guard: **38 boundaries passed**, covering every authored splice and isolated native cut. All every-frame ±12-frame strips were inspected in eight montages; the four corrected tails now cut directly to the intended destination.
- All ten settled outline states inspected at delivery resolution; 121 encoded canonical-board comparisons passed. Final v12 future-board states and final frame rechecked.
- Audio is sample-identical to the selected source assembly outside the documented gains and five-millisecond join handles. Encoded audio SNR versus the edited PCM is 45.43 dB. These measurements do not certify natural cadence or voice matching.
- Corner cleanup processed all 2,154 retained Notebook frames, with no declined frames. Canonical assets, all three uploaded rolls, and the installed video passed protected-file hash checks.
- No added pauses. The final spoken word ends around 3:40.6; the existing quiet tail supports the closing motion and settled hold.

**Direct listening, subjective donor-voice/cadence review, and continuous audiovisual playback are still required before treating this as shipping-ready.** Listen especially to the donor passages at 0:25.767–0:40.467 and 1:32.833–1:42.867. Other narration joins are 0:09.333, 1:17.567, 1:48.067, 2:43.600, and 3:34.733. Individual `join-*.wav` previews were generated with context around all nine joins; regenerable audio scratch was removed after local shipping. The original rolls and build scripts retain the information needed to recreate them.

## Local shipping record — November 3, 2026

The owner explicitly approved shipping after the outstanding listening/playback checks were disclosed. Installed the exact approved v12 bytes at `course-assets/pace-of-change/pace-of-change.mp4`, updated cache key to `20261103ship12`, retained the rounded 4 min label, and updated every affected asset record. Local commit: `6f0c7510d2b79410cc3393c5a207a92dcf7b930f`. Installed SHA-256: `b95735d476d8bd6747c2cf6af1cfab91bf04bd1a6caad101f1aee86530cfed8e`; 30,892,796 bytes.

Asset integrity, staged-page syntax/reference checks, and upload sync passed. The commit contains only the approved Pace of Change release and its lesson/board/preparation dependencies; unrelated working changes remain unstaged. Source assets retained for the board renderer are recorded as retained sources, not deleted assets. Migration hashes were preserved.

Removed 45 regenerable scratch files (about 0.17 GB) from this lesson’s November 3 build/comparison folders. Raw uploads, review candidates, scripts, transcripts, frame sheets, transition strips, manifests, and review records remain. No push or deployment was performed. **Shipped locally; queued for batch deployment.** Agent listening and continuous playback remain unperformed; owner approval is not recorded as proof that those checks occurred.
