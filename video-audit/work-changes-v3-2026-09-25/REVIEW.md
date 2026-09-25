# Work Changes v3 — build record, 2026-09-25

Candidate: `Prompts/work-changes-v3.mp4` (5:28.3, 9848 frames). Review only; live video unchanged.
Build: `.video-venv/bin/python scripts/video/build_work_changes_v3.py` (manifest: `build/edit-manifest.json`).
Everything not listed here is v2 unchanged (see `video-audit/work-changes-v2-2026-09-24/REVIEW.md`).

## Change (David, 2026-09-25)

Lesson Board 4 was rewritten as "How Work Is Changing" (new canonical JPG, 1600x814; no study statistic). David chose
roll 5's narration for it. v3 replaces roll 4 241.0–265.0 (the old board's intro and explanation, including v2's
roll 1 study graft) with roll 5 176.2–214.4, +1.0 dB (roll 5 −20.1 LUFS vs roll 4 −19.4 / −18.7 either side):

> When you put automation and augmentation together, three overarching changes appear across almost every career
> path. First, you take on more kinds of work. With AI's help, you can confidently handle tasks outside your
> traditional specialty, such as design, marketing, or customer support. Second, you become more productive. AI helps
> you complete routine tasks faster, allowing you to accomplish a higher overall output in the exact same timeframe.
> Third, your schedule becomes more meaningful. With routine tasks out of the way, you have the time to solve complex
> problems, develop ideas, and make decisions that require your direct judgment.

Roll 5's following addition ("When you are handling more parts of a project ... a comprehensive owner of the
outcome.", 214.8–227.7) is not in the lesson and was left out.

Pictures (output times): board 3:58.3–4:10.1 (More Kinds of Work ring 4:05.4); roll 1 office floors 4:10.1–4:14.0
under "such as design, marketing, or customer support"; board 4:14.0–4:29.6 (More Productive 4:15.8, More Meaningful
4:25.3); roll 1 glasses and pen 4:29.6–4:36.1 under "solve complex problems, develop ideas, and make decisions".
Roll 5 drew only its own board render here. Longest unbroken board run is now Two Ways (~34 s).

## Verification (encoded file)

- Word-level transcript of 3:52–4:42 reads exactly as above, then "This leads to a complicated situation."
- Splices in (3:57.9, 0.66 s gap after "shoulders") and out (4:36.1, ~0.6 s gap before "This leads") have no clicks
  (max step ≤ 45) and quiet floors (roll 5's silence is a few dB quieter, around −84 dBFS).
- The three row boundaries inside the roll 5 passage are restored to continuous audio (≤ 1 LSB from source).
- `transition_guard.py`: 35 boundaries, 0 failures. Corner mark: 0 declined. Protected files unchanged.

## Not yet done

- Listening by ear, especially the roll 4 → roll 5 → roll 4 voice changes at 3:58 and 4:36, plus v2's joins.
- Not shipped.
