# Where AI Lives · version 9 review copy

This edit uses the November 19 version 3 narration as its base. The version numbers below refer to the three raw uploads. The complete source hashes, source intervals and output frame numbers are in [the edit manifest](edit-manifest.json).

| Output time | Audio source and edit |
|---|---|
| 0:00–2:53 | Version 3 follows the spreadsheet into the cloud, walks through the math example and explains why millions of simultaneous questions lead to data centers. Version 2 supplies the drawing of a GPU performing calculations in parallel. |
| 2:53–3:00 | Version 2 qualifies the comparison with “The biggest AI data centers.” Version 1 supplies the football-fields illustration. |
| 3:00–3:09 | Version 3 directs attention to the person on the left. The complete server-hall photograph stays on screen. |
| 3:09–3:18 | Version 1 identifies the cabinets as racks and explains that each rack contains individual servers stacked one above another. |
| 3:18–3:46 | Version 3 moves from the hall to the neighborhood and electricity bills. The shot of houses on the same street as the facility comes from version 2. |
| 3:46–4:01 | Version 2 explains the cooling requirement for a large facility on a warm day, followed by the fresh water needed to replace evaporation. Its narration says “continually need”; the approved board says “may need.” |
| 4:01–4:42 | Version 3 covers fan noise, lost sleep, jobs and company responses. A brief shot of a resident at the window accompanies the noise passage. |
| 4:42–4:56 | The line about efficient chips leads to the two closing perspectives. The phone and fan precede the canonical closing board. |

The three donor passages received +0.3 dB (facility size), +0.4 dB (racks) and +0.7 dB (water). Cuts are in measured gaps between sentences. [Listening excerpts](narration-joins.m4a) collect continuous passages from the encoded review copy around the inserts and closing cut.

## Encoded checks

A fresh [transcript of the exported audio](encoded-transcript/where-ai-lives-v9.txt) confirms the six donor boundaries preserve the complete sentences in their intended order. The facility comparison leads into the person in the aisle. The person introduces the racks, then the narration returns to the building. The electricity discussion leads into cooling and fresh water, then resumes with noise. The speculative footprint sentence is absent.

The six transitions between speakers have 0.52–0.73 seconds of quiet between phrases. The closing cut has 0.76 seconds. All cuts fall below −67 dBFS at the splice. The measured peak of the exported audio is −0.97 dBFS. The return from the rack insert at 3:18 has the largest shift in measured speaking pitch. The first excerpt includes both sides of this change. The waveform, loudness, pitch estimates and transcription check the technical and verbal flow. The subjective match between the three voices has not been directly auditioned. See the [encoded measurements](encoded-qa.json).

The export decoded through all 8,894 frames. The automated [transition report](transitions/transition-guard.md) flagged three continuous camera moves between cards. I checked all 48 encoded frames across each of those moves against the expected view of the canonical board. Each follows the planned pan with no intervening shot. [Board-move checks](board-move-verification.json) · [Encoded board moves](encoded-board-moves.jpg) · [Selected frames](encoded-states.jpg)
