# Your Choices v4 — built for review

User authorization: “Build please” (2026-09-30), approving the repair proposed in `video-audit/your-choices-evaluation-2026-09-30/REVIEW.md`.

Candidate: `Prompts/your-choices-v4.mp4` — **2:43.77 (2:44)**, 1280×720, 30 fps, 4,913 frames, H.264/AAC.
SHA-256: `77e76ad3d88a85594742312f980e77d326f42694b2e2ca167d0519305455c66c`.

Status: built and technically checked; **not installed or shipped**. Listening and normal-speed audiovisual approval remain outstanding. The original course MP4 and its course reference were not changed.

## Changes

- Replaced the opening with whole-sentence narration from rolls 1 and 2. It now states both app and subscription availability, explains that controls may not appear, and includes “You do not need to see every choice. You need to understand what each one does when it appears.” The claim that settings ensure the right result is gone.
- Preserved the installed music-app drawing, useful dials/routine/advanced-work drawings, app toolbar, and research-source diagram. The AI-app illustration and defaults/advanced-work sequence also use roll 2’s native motion.
- Replaced the misleading configuration graphic with a simple app-to-three-choices diagram. Its model, reasoning, and research branches appear at their spoken names. The availability and reassurance portion and final recap reuse that diagram with matching wording.
- Replaced invented model names with a conceptual app window showing everyday and more-capable models. It carries no invented product names or subscription locks.
- Rebuilt both teaching boards from current canonical JPGs, at full readable view, with whole-card 4-pixel rings and no card dives. Existing supporting cutaways remain inside their matching topic blocks.
- Removed only “which bypasses those deep logical steps for a faster response.” The instruction to keep defaults for routine work remains complete.
- Replaced the premature closing visual with a four-choice recap, then the exact canonical closing JPG on white. Closing visual begins at 2:31.57, with a 48-frame hold, 150-frame push to 1.2×, and settled hold through the literal final frame.
- No pauses added. Donor narration raised by 2.77 dB to match measured active speech in the installed source. Four joins use quiet frame-aligned boundaries and a 10 ms total local smoothing window; timing is unchanged by smoothing.

## Audio assembly and listening targets

| Output | Source | Exact source span | Purpose |
|---|---|---|---|
| 0:00–0:11.40 | `Prompts/your-choices-2.mp4` | frames 0–341, 0:00–0:11.40 | Music analogy and choosing an app |
| 0:11.40–0:20.40 | `Prompts/your-choices-1.mp4` | frames 452–721, 0:15.0667–0:24.0667 | Exact app/subscription/model/reasoning/research sentence |
| 0:20.40–0:46.5667 | `Prompts/your-choices-2.mp4` | frames 580–1364, 0:19.3333–0:45.50 | Defaults, harder work, conditional controls, reassurance |
| 0:46.5667–2:04.1667 | Installed source | frames 1217–3544, 0:40.5667–1:58.1667 | App/model/reasoning teaching |
| 2:04.1667–2:43.7667 | Installed source | frames 3675–4862, 2:02.50–2:42.10 | Research, recap, exact close |

Audition **0:11.40, 0:20.40, 0:46.57, and 2:04.17** for voice continuity, cadence, and intact word endings. Context clips are `join-1.wav` through `join-4.wav` in this folder. Their final encoded 20 ms gap RMS values are approximately −68, −69, −67, and −72 dBFS. These measurements do not establish how a join sounds.

## Verification

- Full sequential decode: 4,913 frames, matching the planned duration exactly.
- Transition guard: **18/18 pass**. Every-frame boundary strips inspected in the three `all-strips-*.jpg` sheets; exact before/after frames inspected in `boundary-summary-*.jpg`. No stale intermediate graphic remains at those boundaries.
- The first internal candidate (v3) contained four frames of a prior roll-2 diagram at 0:20.40. V4 starts directly on the destination dials picture while retaining every audio sample. V3 is superseded; review v4.
- V4 AAC packets are byte-identical to the fully transcribed v3 audio. `transcript.json` records this provenance. The complete transcript was checked: the missing availability/reassurance material is present, all four choices remain explained, the overclaim and bypass clause are absent, and both closing lines are complete and in order.
- Full-resolution board/close states and runtime contact sheets inspected. Complete cards remain visible; closing copy matches the page asset. The closing settled frame and final frame differ by only 0.140 mean pixel levels, consistent with encoding variation.
- Final decoded audio peak is 0.9904; no full-scale sample clipping detected. Donor active speech level matches the installed source by measurement.
- Source hashes verified unchanged. Hashes, exact source/output frames, audio joins, visual boundaries, and cleanup counts are in `edit-manifest.json`.

Content coverage now supports keeping the narration. **A final KEEP/shipping verdict still requires listening and normal-speed end-to-end audiovisual review.** No claim is made that transcripts, waveform measurements, contact sheets, or transition checks substitute for those checks. No additional content defect was identified in the final transcript.

## Reproduction and source limits

Build: `.video-venv/bin/python scripts/video/build_your_choices_v3.py --version 4` (refuses to overwrite an existing candidate).
QA: `.video-venv/bin/python scripts/video/qa_your_choices_v4.py`.

The code-rendered supporting diagrams, canonical close canvas, and review images are retained in this folder. The diagram source is in the build script; canonical JPG assets were not modified. No AI image generation was used.

The installed composite supplies retained cutaways and the existing central narration because its exact full-length assembly has no pristine raw equivalent. It is decoded directly into one new output encode; v4 was rebuilt from those same inputs, not re-encoded from v3. Raw rolls are preserved. No course deployment or tracker update was performed.
