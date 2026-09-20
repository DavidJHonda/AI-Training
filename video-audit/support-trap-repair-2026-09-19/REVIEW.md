# Support Trap v2 review handoff

## Recommendation

Review `Prompts/support-trap-v2.mp4` as the replacement candidate. It fixes the
remaining euphemism by using the complete Support-Trap-3 narration passage while
preserving the live video's spine, the stronger roll-1 explanatory schematic,
all existing course-board treatment, and the standard close. Nothing has been
published or changed in the live lesson.

## Narration result

Transcript-content verdict: **KEEP**, subject to David's required listening check
for delivery and voice continuity.

The repaired output says:

> 2:30.26–2:48.34 — “After Sophie died by suicide, her mother described the chats
> as a black box. The AI offered empathetic words, but those private conversations
> held crucial details that made it harder for the people around her to understand
> how serious her distress was, and to intervene.”

This directly reconnects the content warning to Sophie's death and teaches why the
chats were a “black box.” The live emergency guidance resumes at 2:48.98 with
“This panel outlines exactly what to do if someone may be in immediate danger.”
The 988 and 911 guidance and the standard closing lines remain intact.

## Edit map

| Use | File | Source span | Output span | Treatment |
|---|---|---:|---:|---|
| Spine | `course-assets/support-trap/support-trap.mp4` | all except f4505–4724 (2:30.167–2:37.500) | before 2:30.167 and after 2:48.967 | Preserved |
| Explanatory picture | `Prompts/support-trap-1.mp4` | f5182–5673 (2:52.733–3:09.133) | f4505–5068 (2:30.167–2:48.967) | Complete schematic slowed to 87.234%; engine mark removed |
| Corrected narration only | `Prompts/Support-Trap-3.mp4` | f0–563 (0:00.000–0:18.800) | f4505–5068 (2:30.167–2:48.967) | Audio only, 0 dB gain; Support-Trap-3 video not used |

No extra pause was inserted. The donor provides 0.224 seconds of leading room tone
and 0.391 seconds after the final word. At the second join, that combines with the
live source's existing room tone for a natural 0.647-second sentence transition.

## Board and camera treatment

The recommended plan is the candidate's existing treatment; no new board work is
proposed.

| Board/scene | Existing treatment preserved in v2 | Proposed change |
|---|---|---|
| Supportive Words versus Support | Full comparison, sister and chatbot emphasis, takeaway | None |
| Use AI to Get Ready for People | Full view, What Can Be Real, What Is Missing, takeaway | None |
| Black-box explanation | Roll-1 schematic: black box, closed AI interface, trapped details, physical support network | Narration replaced; visual slowed slightly to carry it |
| If Someone May Be in Immediate Danger | Full board, then Leave the Chat, Do It Now, Tell Anyway, takeaway | None |
| Standard close | Existing final composition and motion | None |

## Verification completed

- Output: 6,656 decoded frames, 30 fps, 1280×720, 3:41.867.
- Full audio and video decode completed without error.
- Full output was re-transcribed; the corrected passage is complete and the live
  re-entry has no leaked or clipped donor words.
- `transition_guard.py` passed both output boundaries at f4505 and f5069. Every-frame
  strips were inspected: each boundary is a single clean visual cut with no stale
  or intermediate frames.
- Both joins land inside measured silence: approximately 2:29.551–2:30.390 and
  2:48.576–2:49.222 on the output timeline.
- Five-millisecond waveform checks found no click-sized discontinuity. Boundary
  sample jumps were 0.000810 and 0.000027; both are within local waveform changes.
- Outside the graft, decoded-audio correlation with the pristine live source is
  0.999995 before and 0.999977 after (expected AAC re-encode variance).
- Contact sheets and both boundary strips were inspected. Support-Trap-3 contributes
  no picture frames; no engine corner mark remains in the graft.
- Protected source hashes matched after the build.

## Listening still required

This environment could not play audio to the reviewer. David should listen to the
full candidate, with special attention to the two joins and the voice/cadence change.
Convenience clips are in `qa/join-1-live-to-roll3.wav`,
`qa/join-2-roll3-to-live.wav`, and `qa/graft-context.wav`. Do not ship until that
listening check passes.

## Files and status

- Candidate SHA-256: `e1511c4bc19f01f9cff072b1d6a1e1892f02d5b8fbb02f126d72cb83005af753`
- Live SHA-256: `48ad17d38fbeee9e0eb9cf521c86922d85d67c234ce61d5385885afc322289ec`
- Visual donor SHA-256: `e37c32e3acc1eaffb5ebdfa2a001e2f3ce0b26fdc06b12f97a88f8358fceec40`
- Audio donor SHA-256: `4eec0eaa9e068109e1cb5b8ed6e9433e8b39b031ba2518ab6427c877e795681f`
- Live video, `index.html`, lesson Markdown, tracker, and deployment are unchanged.
