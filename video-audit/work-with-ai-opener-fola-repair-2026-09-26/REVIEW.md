# Work With AI Opener v9 — three Fola repairs

Review candidate built September 26, 2026. **Unpublished; listening approval outstanding.**

Candidate: [work-with-ai-opener-v9.mp4](/Users/davidobrien/Developer/AI-Training/Prompts/work-with-ai-opener-v9.mp4) — **2:26.27**, 4,388 frames, 1280×720 at 30 fps. Previous live duration: 2:37.90. The reduction is 11.63 seconds, from replacing longer passages rather than accelerating the narration.

## Approved scope and result

David approved the three replacement passages, generated the Fola clips, placed them in the chosen direct lesson directory, and confirmed they were ready for the review build. No additional production approval was needed. This is a narrow repair; the live MP4 and lesson reference are unchanged.

| Replacement | Original audio | Candidate passage | Visual treatment |
|---|---|---|---|
| Opening and transition | 0:00–0:26.00 | 0:00–0:17.87 | Canonical full opening board; gold rings at each spoken line. Release the final ring for the transition. Remove the old technical-diagram bridge. |
| Giving AI context | 1:51.50–1:56.10 | 1:43.37–1:47.33 | Preserve the relevant context/precision drawing, retimed to the 3.96-second take. |
| Map takeaway | 2:20.40–2:26.13 | 2:11.63–2:14.50 | Canonical full section map; banner ring at the new spoken onset. |

All unaffected passages retain their original audio content, frame sequence and timing relative to their own segment. The sandwich comparison, later board/drawing alternation and complete original close are retained. Newly rendered rings use the fixed 4 px at 720p / 6 px at 1080p standard. Existing rings elsewhere were preserved under the narrow scope.

The longest content-board appearance is now the 17.87-second opening. The original same-tool → section-map sequence still totals approximately 21 seconds across two boards. No new teaching pauses were added; donor and retained-source gaps remain, with less than one frame of room tone added to align each donor duration to video frames.

## Sources and processing

- Baseline: `/Users/davidobrien/Developer/AI-Training/course-assets/work-with-ai-opener/work-with-ai-opener.mp4`; SHA-256 `48c90ec931943f0a98464aafe74d5b99c3ff7967db9d4b0af16bde6f146ac4ed`. The pristine Notebook roll no longer survives. This candidate uses the finished live source with one final H.264 encode.
- Original Fola WAVs remain untouched in `/Users/davidobrien/Developer/AI-Training/Prompts/narration-repairs/work-with-ai-opener`. The user chose this directory without a dated subdirectory; that instruction governs retention.
- Voice: Fola, supplied by David. Requested style: default, no description. Actual model/version and a separate generation-settings export were not supplied; they were not inferred.
- Full takes used: 17.84, 3.96 and 2.84 seconds. No words were cut from the supplied recordings and no audio speed change was made.
- Converted from 24 kHz mono to 48 kHz mono. Gain matched to surrounding active speech, with a −1 dB limiter ceiling; processed speech levels are within 0.75 dB of the chosen local references. A very quiet source room-tone bed and 5 ms fades smooth the joins. These measurements do not establish a perceptual voice match.
- Exact scripts and provenance are retained alongside originals in `approved-script-2026-09-26.txt` and `repair-provenance-2026-09-26.json`.

## Boundary handling

Source frame 794 is the first clean Same Tool title frame. The new opening returns to original audio at frame 780, inside silence; that title frame covers the preceding 14 obsolete technical-diagram frames. This avoids a flash of the removed diagram without clipping the next sentence.

The context repair uses source audio gap boundaries 3345 and 3483; its existing picture continues naturally into the original map transition at source frame 3489. The takeaway starts at source frame 4212, two frames before the previous visual cut, so no tiny fragment of the outgoing drawing remains. It ends exactly at the unchanged closing-board onset, source frame 4384.

## Verification on the encoded candidate

- Decoded **4,388 frames**, exactly matching the plan.
- All **five declared splice boundaries pass transition_guard**. Every-frame strips around all five were inspected, along with immediate before/after full frames. No leaked technical-diagram frame or brief extra picture was found.
- All four new opening highlight states, their release, the new banner ring, full-view openings and literal final closing frame were visually checked. Text and ring bounds fit the frame.
- The complete candidate was transcribed again. All three approved scripts appear word-for-word after normalizing punctuation. The next original sentence, “Here is the reality most people miss,” is intact. No “force a better outcome” or “depends entirely” remains in the replaced passages.
- Unchanged source audio is PCM-identical before encoding outside the 5 ms seam fades. Encoded audio correlation to the planned assembly exceeds 0.9999 for every segment; there is no detected timeline shift.
- Forty-one sampled untouched video frames differ from the baseline by 2.36/255 mean pixel intensity on average (maximum 2.78), consistent with the one final encode.
- Source MP4, original WAVs, canonical JPGs and index.html hashes remain unchanged.
- AAC decoding includes 768 padding samples (16 ms) beyond the planned PCM endpoint. This is encoder padding, not inserted narration or an additional video frame.

## Listening still required

I could not audition the audio. The remaining check is voice continuity, perceived loudness, natural cadence and both sides of each join. Listen to:

1. **0:00–0:21** — the new opening, then return to the existing voice around **0:17.87**.
2. **1:40–1:50** — into Fola at **1:43.37**, back out at **1:47.33**.
3. **2:08–2:19** — into the takeaway at **2:11.63**, then the original close after **2:14.50**.

This is ready for David’s review, not declared ready to publish. The inherited formal wording elsewhere and “AI doesn’t…” at the close remain as discussed; the camera comparison was intentionally retained. No broader narration rewrite, end-to-end listening sign-off or tracker update was performed.

## Reproduction and evidence

Build command: `.video-venv/bin/python scripts/video/build_opener_work_fola_review.py`. The script rejects an existing candidate, checks source hashes and records the timeline. Version a subsequent revision instead of overwriting a file David may have open.

[Edit manifest](/Users/davidobrien/Developer/AI-Training/video-audit/work-with-ai-opener-fola-repair-2026-09-26/edit-manifest.json) · [QA results](/Users/davidobrien/Developer/AI-Training/video-audit/work-with-ai-opener-fola-repair-2026-09-26/qa.json) · [Candidate transcript](/Users/davidobrien/Developer/AI-Training/video-audit/work-with-ai-opener-fola-repair-2026-09-26/candidate-transcript.txt) · [Visual check sheet](/Users/davidobrien/Developer/AI-Training/video-audit/work-with-ai-opener-fola-repair-2026-09-26/qa-overview.jpg) · [Transition results](/Users/davidobrien/Developer/AI-Training/video-audit/work-with-ai-opener-fola-repair-2026-09-26/transitions/transition-guard.json)
