# Tokens v9 — approved for shipping

Approved repair of the existing video, with three narrated split examples. David subsequently authorized publication: “ship the video.” Candidate: `Prompts/tokens-v9.mp4`, 1280×720, 30fps, 8,157 frames, **4:31.90**. Source: the exact local published file `course-assets/tokens/tokens.mp4?v=20260922ship6`, 9,158 frames, 5:05.27. Total reduction: **33.37s**.

Candidate SHA-256: `d1b7a9e0a5dabb90ec3bbb241518fc5727bab84be6f2bbd3327170b6812a1f16`.
Source SHA-256: `48f170a1ed6794de08903ca578570dab9186d80ac605896bc9718c7e9433aa1f`.

## What changed

- **3:26.60–3:59.57:** the examples board now runs **32.97s**, formerly 66.33s. Retains all five rows in the canonical board; opens full and unmarked for three seconds. Narrates basketball, spaces/symbols, and the URL count, with uniform complete-row zooms. Omits the repeated unbelievable walkthrough, ChatGPT walkthrough, URL fragment recital, and redundant recap. Spoken example numbers 2, 4, and 5 still match the board. The later return-to-words explanation and closing narration remain intact.
- **About 2:05–2:15:** corrects the vocabulary chart subtitle to **GPT-4o / o200k_base**, tracking its existing entrance/exit. Preserves the chart, counts, count-up animation, other model examples, and narration.
- **All five teaching boards:** fixed **4px at 720p** outlines, drawn after camera transforms. Uses exact current canonical JPGs. Previous framing and ring targets/timing retained on the first four boards. The examples board follows the three retained walkthroughs.
- Original illustrations, animations, standard close, and existing pauses retained. No new voice, narration graft, extra pause, or gain change. Three 5ms anti-click ramps only.

## Narration edits and review points

| Removed source interval | Removed material | Join in candidate |
|---|---|---|
| 3:29.50–3:36.17 | Unbelievable walkthrough | 3:29.50: introductory sentence → basketball |
| 3:40.87–3:49.13 | Names bridge and ChatGPT walkthrough | 3:34.20: basketball → spaces/symbols |
| 4:14.30–4:32.73 | URL fragments and repeated tokenizer recap | 3:59.37: eight-token count → return to words |

Cut boundaries were placed in measured quiet gaps, accounting for word tails that extend beyond ASR timestamps. Read the complete new ASR transcript in `audio-check/edited.txt`; the retained statements and their order are intact. This is a transcript/signal finding, not listening certification.

## Continuous board durations

These include every zoom, pan, hold, and existing pause; camera moves do not reset the clock.

| Board | Candidate interval | Continuous duration |
|---|---|---:|
| You Use Words. AI Uses Numbers. | 0:10.30–0:32.50 | 22.20s |
| Building Blocks for Language | 1:04.90–1:55.10 | 50.20s |
| What Happens When You Hit Send | 2:23.97–3:01.67 | 37.70s |
| Humans See a Cat. AI Starts With a Token ID. | 3:01.67–3:26.60 | 24.93s |
| How AI Splits Text Into Tokens | 3:26.60–3:59.57 | 32.97s |
| Standard close | 4:21.13–4:31.90 | 10.77s |

Longest teaching board is now Building Blocks, 50.20s. The Send → Cat → Examples chain is **95.60s**, formerly 128.97s. Retained long spans continue teaching their corresponding board; no unrelated cutaway was introduced.

## Finished-file checks

- Sequentially decoded all **8,157 frames**; verified resolution, 30fps, duration.
- Compared **all 3,117 original-graphic/close frames** against the source or the narrowly corrected chart. Compared **446 board frames** covering states, one-second samples, and every frame around edited boundaries. Maximum mean absolute pixel error 3.188/255, consistent with the final encode.
- Inspected five encoded contact sheets covering all prepared board states, chart fades, new joins, and closing card. Complete active rows and rings remain inside the delivery frame.
- Measured 37 encoded highlight samples across all five boards against their actual geometry/background. Median effective coverage is 4.11–4.22px by board; anti-aliasing and codec spread explain the small excess over the specified 4px. No zoom-related thickening.
- Checked **19 boundary strips**, every frame for 12 frames each side. Automatic guard passed 18 and flagged one continuous pan (f6426, high deltas at f6437–6438). Manually inspected all strips: the flagged pair is smooth progression on the same canonical board, not an intermediate scene or stale frame. Raw detector result remains unchanged; manual adjudication is recorded separately in `manual-review.json`.
- Retained source PCM is **exactly equal outside the three 5ms ramps** after the approved cuts. Final AAC decode correlates 0.999976 with the edited PCM; signal-to-noise ratio 43.09dB. No encoding truncation detected.
- Source video, Tokens lesson Markdown, and canonical JPG hashes are unchanged. Course/page, prep materials, and published video were not changed by this build.

## Limits and remaining checks

- End-to-end real-time watching/listening, audible join naturalness, warmth/prosody, and pronunciation were **not performed**. In particular, audition new joins at 3:29.50, 3:34.20, and 3:59.37. Older pronunciation checks around 1:22–1:25 and 2:41–2:48 remain unverified; the former URL-fragment recital is removed.
- No mobile playback/readability check. No exhaustive automatic ring detector run; encoded geometry-based samples were measured instead.
- No new local recomputation of token IDs (tiktoken unavailable) or independent verification of Gemini/Claude vocabulary statistics. Those existing illustrations/claims remain as scoped. GPT-4o's tokenizer mapping was checked against OpenAI's official tiktoken source during planning.
- Original raw generations are unavailable locally; this repair uses the existing published MP4 and canonical board JPGs. Preserved graphics therefore receive one additional video encode.
- No new public download comparison, tracker access/update, publication, or deployment. This is a review candidate, not whole-file ship certification.

## Shipping authorization

David approved shipping this exact candidate after the review disclosed the unperformed listening checks. Installed at `course-assets/tokens/tokens.mp4` with cache key `20260927ship1`; manifest hash and byte count updated. Retained verification applies to the identical file. Prior listening and other limitations above remain disclosed, not converted to passes. Deployment will not be awaited.

Shipping validation: canonical file, staged website reference, and staged manifest hash/bytes match the approved candidate. Staged whitespace check passes. The broad asset verifier reports the same pre-existing In Your Hands retired-file and Training-prefixed Where’s the Line reference warnings as HEAD; no new asset warning was introduced. Details: `shipping-verification.json`.
