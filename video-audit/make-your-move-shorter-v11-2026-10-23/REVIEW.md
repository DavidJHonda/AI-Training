# Make Your Move — shorter video v11

October 23, 2026. **Review candidate complete: 3:01.03, down from 4:54.17 (1:53.13 removed).**

Candidate: `Prompts/make-your-move-v11.mp4`
SHA-256: `bd537212dbfb94d6cf96611c33d056f58aea78fb6ac65e370758843e9763929d`

The user's request authorized the narrower three-career lesson edit. This candidate retains teacher, electrician, and graphic designer; removes doctor, lawyer, entrepreneur, and the full skills recap; and retains all four actions, the reassurance, and both closing lines. The current three-career JPG replaces both obsolete career boards. Useful teaching illustrations, the action sequence, and the close remain.

**Status: ready for playback review, not installed, committed, or published.** Direct listening and continuous audiovisual playback have not been performed. The completed checks below do not replace them or establish shipping readiness. The local canonical video and its website reference remain unchanged.

## Narration review

**KEEP on complete candidate transcript evidence, with listening verification outstanding.** Read the actual encoded candidate's entire ASR transcript, alongside the current page and Markdown. All essential teaching is RICH or TAUGHT. The bridge uses an existing complete sentence pair about transferable skills, rather than the new page sentence verbatim. Its relationship is preserved: human responsibility gives students a reason to develop skills and act. The specific four-skill recap is intentionally removed.

| Teaching point | Verdict | Candidate evidence |
|---|---|---|
| Practice must lead to participation | RICH | 0:00–0:15, basketball team, drills, joining a league |
| Apply the AI understanding and skills already learned | RICH | 0:16–0:28, decide what to do with the skills |
| Jobs contain tasks affected differently | RICH | 0:28–0:45, professions versus distinct tasks |
| Teacher: AI assistance and human responsibilities | TAUGHT | 0:45–1:02, lesson drafts and practice; knowing students, motivation, adaptation, community |
| Electrician: AI assistance and human responsibilities | TAUGHT | 1:03–1:17, manuals/causes; safety, diagnosis, adapting on site |
| Graphic designer: AI assistance and human responsibilities | RICH | 1:17–1:32, drafts/variations; purpose, audience, taste, final direction |
| Bridge from career examples into transferable capability | TAUGHT | 1:33–1:40, responsibility and capabilities usable across careers |
| Act without deciding an entire future | RICH | 1:45–1:53, reassurance and room for exploration |
| Learn from people in the field | RICH | 1:54–2:06, normal week, changing industry, student misunderstandings |
| Build real depth | RICH | 2:07–2:20, class, reps, feedback, enough knowledge to catch AI errors |
| Make something real | TAUGHT | 2:21–2:32, project/event/business/problem and tangible proof |
| Step into responsibility | TAUGHT | 2:33–2:43, club, volunteering, leadership, delivering a result for others |
| First closing line | MET | 2:50–2:52, “you know how to be smarter than the tool” |
| Second closing line | MET | 2:53–2:56, “Keep learning. Keep building. Make your move.” |

The interactive Make One Move lab remains on the page for both reading and video routes; it is not duplicated as narration. Existing harmless compression remains: reviewing student work, planning electrical work, and research as one possible project are not separately spoken. Examples still teach both AI help and human responsibility. No new claims or voices were added. Existing narration uses “AI excels/can/generates” while the board uses “AI MAY HELP”; no capability guarantee has been added by this edit.

## Visual treatment and checks

See `EDIT-PLAN.md` for the board plan, exact retained words and source times. `edit-manifest.json` records hashes, frame ranges, all four audio joins, board targets, and supporting visual runs.

- New career board opens complete and unmarked at 0:42.50; first highlight starts at 0:45.27. Fixed full-board camera; whole-card and section outlines follow narration, using 4px output strokes and matching card colors.
- Its uninterrupted runs are 13.83, 10.43, and 11.30 seconds. Retained supporting illustrations show teacher judgment, electrical diagnosis, and design decisions.
- An existing team/leadership drawing covers the 7.83-second bridge. Its original restrained motion is slowed to fit; no new narration time is added.
- All four action scenes and the original closing motion are retained. The last decoded frame matches the source close within normal recompression error.
- Inspected full-size board states, both whole-video contact sheets (four-second sampling), and all nine every-frame transition strips. No old career or skills board flash found at the edits.
- Automated transition guard: **9 boundaries, 0 failures**. Full decode: **5,431 frames, 30fps, 1280×720**, regular timestamps, no near-black frames.
- Encoded audio at each join matches the planned audio with correlation above 0.99998. All source edit endpoints are below −51dBFS RMS. Quiet gaps at the four output joins are 0.53, 0.49, 0.38, and 0.91 seconds; no pauses were added.
- Integrated loudness: **−18.7 LUFS**; true peak: **−1.3dBFS**. No gain or speed changes to the narration.
- Representative retained pictures have mean absolute pixel differences below 1.23/255; final-frame difference is 0.006/255. These are recompression comparisons, not claims of identical encoded bytes.

## Remaining review

Listen through the full candidate for natural pacing and voice continuity. Four eight-second audio excerpts (`join-01350.wav`, `join-01871.wav`, `join-02776.wav`, `join-03011.wav`) provide context at the edited joins. ASR and low waveform energy do not establish how those joins sound. Continuous motion review beyond the sampled frames/transition strips is also outstanding.

The build starts from the surviving finished v10, whose hash is locked and which matches the installed local video; no raw generation was available. Unaffected pictures were passed to the encoder in their original planar YUV format, then the whole candidate received one new encode. No external Video Tracker status was read or changed.

## Reproduction

```sh
.video-venv/bin/python scripts/video/build_make_your_move_v11.py
.video-venv/bin/python scripts/video/qa_make_your_move_v11.py
HF_HUB_OFFLINE=1 .video-venv/bin/python scripts/video/transcribe_selected_videos.py Prompts/make-your-move-v11.mp4 --output-dir video-audit/make-your-move-shorter-v11-2026-10-23/transcript
```

The builder deliberately refuses to overwrite the candidate. Preserve or version an existing candidate before rebuilding.
