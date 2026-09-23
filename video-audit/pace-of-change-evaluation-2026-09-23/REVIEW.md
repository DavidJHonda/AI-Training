# Pace of Change — live video evaluation against the current system (2026-09-23)

David: "evaluate the live versions of Loudest Voices and Pace of Change videos. I need to know if they
need a reroll to our current system." Scope: evaluation only. Nothing built, nothing shipped, no
materials changed. Bundle (transcript, scenes, holds, contact sheets) in `pace-of-change/`.

Live file: `course-assets/pace-of-change/pace-of-change.mp4` — v2, shipped 2026-09-18, 4:11.93,
sha256 75f65a59…, cache key 20260918ship1, pill 4 min. Roll 2 base, AGI beat grafted from the earlier
course video, both closing lines grafted from roll 1. **Rolls 1 and 2 are gone from `Prompts/`**, so
the live audio is the only source: no REPAIR path exists.

Materials state: `lessons/pace-of-change.md` is already in the 2026-09-20 structure.
`Prompts/pace-of-change-video-prompt.txt` (399 words) is the interim 9/18 form (NARRATION FIRST, no
verbatim list, beat spine or banned-word list). Not in `Prompts/upload-sets.json`. No face boards.

```text
LESSON: pace-of-change
CANDIDATE: course-assets/pace-of-change/pace-of-change.mp4 (4:11.93, live v2)
VERDICT: KEEP (narration) — the reroll question is a pictures question; see Answer
TEACHING POINTS:
  Hook: argument louder; because the technology is advancing at blazing speeds — RICH — 0:00–0:09
  2023 vs 2026, Answering (both years) — RICH — 0:22–0:37
  Images (both years) — RICH — 0:37–0:52 (dog's name Spot dropped, harmless)
  Context Window (both years, million tokens = novel series) — RICH — 0:52–1:12
  Doing (both years; agents book, build, fix) — RICH — 1:12–1:27
  Race; new models every couple of months; today's "no" not necessarily permanent — TAUGHT — 1:27–1:40 ("today's no is not necessarily a permanent no")
  Three concepts, "you already understand the first one" — TAUGHT — 1:46 (the callback to the Training lesson is not spoken; minor)
  Better Training — RICH — 1:51
  More Compute — RICH — 1:59
  AI Helps Build AI — RICH — 2:11
  "Slow down and read that third one again. AI is already helping people build better AI." — TAUGHT — 2:23 ("AI is already actively helping people build better AI"; one added word)
  Four ideas; one happening in limited form, three not demonstrated — TAUGHT — 2:30–2:44; the up-front "one happening / three not demonstrated" sentence is not spoken, but each idea is tagged as it comes (limited form 2:46, not demonstrated 2:58, theoretical 3:24, hypothetical 3:20)
  Two groups (how AI might improve / how capable it might become), not four steps in order — THIN — 2:37 "whether AI could eventually improve itself" and 3:24 "these final two theoretical concepts represent the ultimate finish lines"; the "not four sequential steps" idea is never spoken and "ultimate finish lines" pulls the wrong way (see ERRORS)
  Automated AI Research (limited form; researchers set goals, direct, verify) — RICH — 2:44–2:58
  Self-Improving AI (not demonstrated; the loop) — RICH — 2:58–3:15
  Banner: "One is human-directed. The other would be a self-reinforcing loop." — TAUGHT (not verbatim) — 3:15 "One process is entirely human-directed. The other represents a hypothetical self-reinforcing loop."
  AGI: human-level across many kinds of work; no agreed finish line; no accepted definition or test — RICH — 3:29–3:48 (the 9/18 graft)
  ASI: exceeding the best humans across nearly every cognitive field — RICH — 3:48
  "Nobody knows whether AI will reach either milestone." — TAUGHT (not verbatim) — 3:57 "It is critical to understand that nobody knows whether AI will actually reach either of these milestones."
HARD REQUIREMENTS:
  "AI keeps getting faster and more powerful." — MET — 4:03 (exact, roll 1 graft)
  "Nobody is sure where it stops." — MET — 4:06 (exact)
  "today's 'no' is not necessarily permanent" — MET in substance — 1:36
  "AI is already helping people build better AI." — near miss — 2:26 adds "actively"
  "Nobody knows whether AI will reach either milestone." — near miss — 3:57 adds "actually … of these"
ERRORS:
  3:24 — "These final two theoretical concepts represent the ultimate finish lines for AI" — Notebook's phrase; the lesson calls them possible milestones with no agreed finish line. Not a reversal, but it muddles the framing it is meant to introduce.
  3:37 — "But look at the tag above it. No agreed finish line." — narrates board furniture (banned under current VOICE rules). It happens to be the earlier course video's audio, grafted 9/18.
SOURCE_QA: PASS (the Markdown's "not every release improves every task" qualifier is Markdown-only nuance the page does not carry; its absence from the narration is not an error)
ADDITIONS: none worth keeping.
REPAIR PLAN: none available — no rolls survive. The two errors are mid-beat and would need synthetic cuts.
EDITING NOTES (where the live file fails the current spec):
  Board holds (Edit Spec 8b, widened 2026-09-23 to ~20 s per board): ChatGPT: 2023 vs. 2026 about 0:10–1:27 (77 s, dense dive-and-pan, unbroken); Why So Fast? about 1:46–2:31 (45 s, unbroken); Could AI Improve Itself? about 2:37–3:26 straight into How Far Can AI Go? about 3:26–4:03 (85 s back to back, recorded 9/18 as an "intentional exception"). All four boards exceed the new limit; the total board time is about 3:30 of a 4:12 video.
  Notebook spans that would not ship under current rules: 0:00–0:09 "AI CAPABILITY ACCELERATION" chart (Relative Performance Index 0–450, 2016–2024: invented figures); 1:28–1:42 "AI RELEASE CADENCE & ITERATION RACE" timeline naming GPT-4, Claude 2, Gemini 1.0 etc. with quarter dates and a "TODAY'S 'NO' → TEMPORARY CEILING" box (invented detail, tiny text); 1:44–1:46 "WHY SO FAST?" drawn title (a chapter card); 2:32–2:37 "FOUR KEY TRAJECTORIES OF AI DEVELOPMENT" diagram (a Notebook restatement of the two future-idea boards in its own words, tiny text). These are the only non-board pictures in the file, so there is nothing in this roll to break the holds with.
  Compliant today: canonical boards, full-view opens, one row/card ring at a time at spoken onsets, corner mark cleaned, no photographs, canonical close as the literal final frame, the 0.33 s selective pause before the close. Rings are constant 5 px under the pre-9/21 rule (grandfathered).
LISTENING: transcript only. Not auditioned by ear: the AGI graft joins at 3:29 and 3:48, the "milestones" cut into the close at 4:03, and the two grafted closing lines (all listed as owner-listening items on 9/18).
```

## Answer

**Narration: KEEP.** Every point is RICH or TAUGHT, the two closing lines are exact, and the two
blemishes (the "ultimate finish lines" phrase and "look at the tag above it") are wording, not
teaching. On narration alone this video does not need a reroll.

**Pictures: this is the profile David named on 2026-09-23 as the weakness in shipped videos.** Four
boards held 45–85 s each, about 3:30 of board time in 4:12, and every Notebook span in the roll is
either an invented chart, a chapter card or a restatement of a course board, so Edit Spec 8b has no
material to work with. The only way to get drawings under this lesson is a new roll.

Recommendation: **reroll for pictures, keep the live narration as the base.** Roll on the rebuilt
kit; compare beat by beat under Narration Review. If the new narration wins, build from it. If the
live narration still wins (likely, given the above), use the new roll's drawings under the live
audio to break the four holds (8b: "drawings from OTHER ROLLS of the same lesson"). Either way the
prompt gets its verbatim list ("AI is already helping people build better AI.", "Nobody knows whether
AI will reach either milestone.", the two banners, the two closing lines), the beat spine (say the
two groups and "four ideas to understand, not four steps"), a banned-word list (finish line, trajectory,
theoretical, stakeholders, leverage, framework), a registry entry and a sync. Markdown unchanged.
