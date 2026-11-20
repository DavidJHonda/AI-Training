# Work Changes video preparation

Updated November 20, 2026. Review required passages for meaning, not exact wording,
per David’s direction. The prep bundle reflects the revised lesson.

The three uploads were evaluated in
`video-audit/work-changes-three-rolls-2026-11-20/REVIEW.md`. David selected version 3,
then approved targeted visual changes, built as v9 and revised as v10.

**Installed release:** `Prompts/work-changes-v10.mp4` (4:12.90), copied to
`course-assets/work-changes/work-changes.mp4` with cache key `20261120ship1`.
At David's request, it removes two redundant sentences, zooms into the assignment
banner, and adds photographic training-ground and school scenes matching the
checking illustration. David authorized shipping and pushing all changes after
the listening limitation was disclosed. The two new audio joins have not been
certified by perceptual listening; full continuous playback is not claimed.
Build, checks, and installation record:
`video-audit/work-changes-v10-2026-11-20/REVIEW.md`.

## Source and upload workflow

`index.html` and `lessons/work-changes.md` hold the current lesson and lab.
`lessons/work-changes-video.md` is the generated narration source. It preserves
the teaching sequence and board copy, excludes the lab, and ends with the closing
lines. The only prose substitution is the approved spoken time-savings passage
below; the following knowledge takeaway is retained. Preferred audio passages are
standalone. The What Changes heading ends the assignment board hold before the
following prose.

Refresh the derived source, compatibility board, and upload bundle after source edits:

```sh
.video-venv/bin/python scripts/video/prepare_work_changes.py
.video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson work-changes
.video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson work-changes --check
```

Upload the four files in `upload/` only. Paste `PROMPT.txt` into the customization
box. Do not upload this note, the README, the prompt, or the full page/lab source.
Save the raw video as `Prompts/work-changes-reroll.mp4`, using the next unused
suffix if it already exists. Preserve earlier raw rolls and the finished video.

## Approved spoken time-savings passage

Before AI, you read and organized the reviews yourself. With AI, you get help
organizing the feedback and drafting a summary. You spot-check the results,
investigate the problems, and decide what to recommend. Less time on routine work
can mean more time for judgment and decisions.

Follow with: “The more you know, the better you’ll be at that work.”

## Board handoff

| Upload | Final edit asset | Treatment |
| --- | --- | --- |
| `work-changes-assignment-faceless.jpg` | `course-assets/work-changes/work-changes-assignment-short.jpg` | Same 1600x1506 layout and copy; replace the version with empty photo panels with the canonical board. |
| `work-changes-automation-and-augmentation.jpg` | Same filename in `course-assets/work-changes/` | Current title: Two Ways AI Changes Work. Byte-identical upload. |
| `work-changes-close.jpg` | Same filename in `course-assets/work-changes/` | Exact current closing lines. Byte-identical upload. |

The preparation renderer omits only the assignment photo panels. It does not crop
or rewrite the teaching. The final edit keeps the current labels Routine Work and
Judgment & Decisions, their purpose lines, Before AI / With AI comparisons, equal
section spacing, no connector arrow, and the same-assignment banner.

Retired strengths, productivity, and old assignment boards are excluded from the
active bundle. Keep historical production scripts and raw videos as records, not
as the new narration plan.

## Narration review checklist

- Career opening uses possibilities, not a promise that named jobs will survive.
- Both stages include Before AI and With AI, including spot-checking and presenting
  your recommendation. The same-assignment banner is spoken.
- The time-savings passage uses no week-to-minutes claim or invented benchmark.
- Automate and augment both use examples from the assignment; the ownership point
  remains clear.
- The lost training opportunity is explained through learning about customers.
- The productivity-before-knowledge risk leads to the concrete response: read a
  sample, note observations before AI’s summary, then compare.
- What can you do today leads to learning and school. Both closing ideas are taught,
  in order, with no lab instructions or narration afterward.

The full beat spine is in `scripts/video/kits/NAVIGATE-THE-FUTURE-VIDEO-KITS.md`.
Evaluate the new roll under `scripts/video/NARRATION-REVIEW.md` before planning
cuts, camera moves, highlights, or a new build under `scripts/video/EDIT-SPEC.md`.
