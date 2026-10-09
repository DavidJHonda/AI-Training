# What’s an LLM? — production candidate

Built October 9, 2026. Candidate: `Prompts/whats-an-llm-v3.mp4`, 2:36.40, 1280×720, 30 fps, 4,692 frames. This is production candidate v3, based on uploaded roll **2**. It supersedes the preliminary production v2; it is not uploaded roll 3.

[Open review player](http://127.0.0.1:8880/tmp/whats-an-llm/review-v3.html).

## Changes

Roll 2 supplies the main narration, including the context comparison and the explanation that multiple words can fit. Two complete passages restore its omissions:

| Output interval | Source | Passage |
|---|---|---|
| 0:23.93–0:30.07 | Roll 3, 0:31.63–0:37.77 | “Language describes what it does. Reads, writes, summarizes, translates, and explains.” |
| 1:09.53–1:11.77 | Roll 1, 1:29.37–1:31.60 | “Better late than, leads to, never.” |

Donors receive −0.2 dB and −0.4 dB level adjustments respectively. Cuts sit in measured silence, with 5 ms edge fades inside that silence. No synthetic narration or additional pauses were introduced. The optional “mental library” cut was unnecessary and that sentence remains.

Canonical definition, patterns, next-word loop, and closing boards replace the generated versions. Boards begin with the whole composition and use fixed 4 px outlines at 720p. Supporting animations explain the app/model relationship, training before use, broader patterns, context changes, phone suggestions, growing input, and alternative continuations without numerical probability diagrams. The opening devices, human/model jelly reveal, and drawn phone remain from roll 2. A percentage sublabel was removed from the retained jelly reveal without replacing its animation. The close holds 48 frames, pushes for 150 frames to 1.2×, then settles for 91 frames.

## Verification

- All 4,692 frames decoded. All 17 transition checks passed; encoded boundary samples and the final frame were visually inspected. The corrected jelly reveal has no remaining percentage label in the inspected settled frames.
- Final assembled audio was transcribed during v2 verification. V3 has the identical compressed audio stream, SHA-256 `dca7adbc405391894d9f5b7d093b7e3d89448c544dc765df3a71a864632208d2`; the [assembled transcript](../whats-an-llm-build-2026-10-09-v2/transcript.txt) therefore applies to this candidate. Both donor passages, the context comparison, the updated-input loop, the variability explanation, and both closing sentences are present.
- Decoded AAC versus assembled PCM correlation: 0.999982. This is a technical integrity check, not a listening assessment.
- Literal final-frame mean pixel error against the intended canonical close: 2.958/255, within the check’s threshold of 3.
- Longest continuous board run: 20.97 seconds. The patterns board is split by the retained reveal; the next-word loop runs 18.67 seconds.
- Source videos, canonical course boards, and the installed course video retain their pre-build hashes. Exact source hashes, cuts, visual intervals, board states, and candidate hash are recorded in [edit-manifest.json](edit-manifest.json). Detailed results are in [qa.json](qa.json).

Direct audio perception was unavailable. No end-to-end listening pass or final KEEP/ship certification is claimed. Use the review player’s **0:22** and **1:07** shortcuts to check narrator consistency, prosody, and the donor entry/exit joins. The browser loaded the full 156.4-second candidate successfully. The seek-enabled localhost server reports the full duration as seekable; keyboard activation of the Language shortcut starts playback at 22 seconds. Playback was left paused for review.

This build is a local review candidate. It has not replaced the course video or been published.

Candidate SHA-256: `24f152bc45f7c18a6ec52c7d13c611b9d578112532e0a953d46662a55cfd0489`.
