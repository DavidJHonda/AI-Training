# Questions Matter — v5 revision review

## Status

- Candidate: `Prompts/questions-matter-v5.mp4`
- Status: **SHIPPED 2026-09-16** on David's approval ("ship questions-matter-v5"): copied to `course-assets/questions-matter/questions-matter.mp4` (sha256 7ec1f3a73430bebb…), cache key 20260916ship1, duration pill 3 min → 4 min (3:43); candidates v3–v5 removed from Prompts/.
- Verdict: **KEEP** for picture and narration content.
- Direct listening was not available in this environment. The revised pass does not alter spoken wording; the exact-export transcript is identical to v3, but a human listening pass remains the final delivery check.

## Requested revisions completed

1. The Library, Search, and AI rings on the first board now enclose each complete card, including its `TIME TO ANSWER` panel.
2. During “Half a day, then an hour, now seconds,” the three lower time panels highlight separately in spoken order:
   - 00:51.06 — Half a Saturday
   - 00:52.08 — An hour or two
   - 00:52.86 — Seconds
3. The legacy donut sequence around 01:51 was removed. The scientific-method graphic now cuts directly to the approved hand-lettered criteria title.
4. The legacy framework graphic around 01:58 was removed. The criteria title holds cleanly until the canonical Four Qualities board appears.

The removed source-picture spans are frames 3080–3100 and 3288–3323 of `questions-matter-2.mp4`. Narration across both spans is retained.

## Verification

- Output: 1280×720, 30 fps, 48 kHz mono AAC.
- Planned, metadata, and decoded frame counts: 6,688.
- Duration: 222.933 seconds.
- SHA-256: `7ec1f3a73430bebb5deb9a39b1881cced3b611361a85ceda9f8d0e880b1bf643`.
- Transition guard: 17/17 declared boundaries passed.
- The two changed transition strips were inspected frame by frame; neither removed graphic remains.
- The three time-highlight states were inspected from exact output frames and appear independently in the correct sequence.
- Five whole-video contact sheets were inspected; the remainder of the approved visual progression is intact.
- Exact-export transcript: 617 words and text-identical to the previously approved v3 transcript.
- Corner cleanup: 2,679 cloned frames, 98 inpainted frames, 0 declined frames.
- Both source videos, the live lesson video, lesson Markdown, and all four canonical boards were hash-checked and remain unchanged.

Supporting artifacts: `edit-manifest.json`, `transcript/`, `transition-guard/`, `final-sheets/`, exact-frame checks, board state sheets, and the reproducible builder `scripts/video/build_questions_matter_v5.py`.
