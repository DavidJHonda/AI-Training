# Hallucination — three-way review and v9 build (2026-09-21)

Candidates: `Prompts/hallucination-1.mp4` (4:50), `Prompts/hallucination-2.mp4` (3:29), and the
live v8 (`course-assets/hallucination/hallucination.mp4`, 3:57, shipped 2026-09-19 as a best-of
over the 2026-09-08 spine). Both rolls came from the 2026-09-18 kit (no VOICE block; speak-the-
answers template with the pizza case reserved). Transcripts and sheets in the per-roll folders.

**Verdict: roll 1 is the base, no grafts. Built as v9, then v10 (full-height card rings, David's note), then v11 (`Prompts/hallucination-v11.mp4`, 4:40): the Why Hallucinations Happen board itself was changed on David's request so its step arrows match Check the Claim's (thin muted line, same head), the page's copy was updated with a new cache key, and the video carries the new board. v11 is byte-identical to v10 outside the why-board span.**

## Per-roll block: hallucination-1 (BASE)

```text
LESSON: hallucination
CANDIDATE: Prompts/hallucination-1.mp4 (4:50)
VERDICT: REPAIR (two audio cuts; fabricated screenshots to cover)
TEACHING POINTS:
  Chat exchange: question and the AI answer with study, 1,200 students, 18%, 60 decibels — RICH — 0:06–0:28
  Reveal: Stanford real, sample plausible, volume careful; no paper, no source — RICH — 0:28–0:39
  Definition — TAUGHT — 0:41 "a factual claim the system invents out of thin air. That sounds completely true, but isn't" (lesson: "AI makes up that sounds true but isn't")
  One invented detail attached to real facts; harder to spot — RICH — 0:48–0:57
  AI knows what a finding sounds like — RICH — 0:57–1:11
  Four reasons, in order, linked back — RICH — 1:21–2:08 (Probable ≠ True taught as "high statistical probability… does not mean… factual truth")
  Not every error is a hallucination — RICH — 2:08
  Pizza: search, glue, Reddit joke, real text, missed meaning — RICH — 2:16–2:44
  Invented vs misinterpreted distinction — RICH — 2:44–2:55
  Don't doubt every sentence; notice when something doesn't add up — RICH — 2:55–3:11
  Three steps named — RICH — 3:12–3:21
  Stanford application incl. "failing to find a source does not prove it false; unverified; do not repeat" — RICH — 3:21–4:03
  Pizza application incl. "finding the text is only part; it must support the claim" — RICH — 4:03–4:29
HARD REQUIREMENTS:
  Closing lines verbatim, in order — MET — 4:29.5 (preceded by "As this banner states," and followed by a sentence: both cut in v9)
  Study stated as nonexistent; Reddit as a joke; numbers never endorsed — MET
ERRORS: none
SOURCE_QA: PASS
ADDITIONS: "three-step framework", "logical friction", "mechanical failure": register drift, harmless
REPAIR PLAN: drop "As this banner states," (269.54–270.7, inside quiet 269.22–269.58 / 270.82–271.04); drop everything after "source." (277.54; quiet from 277.71)
EDITING NOTES: fabricated Reddit screenshots with a username (2:32–2:44, 4:16–4:29) and an invented on-screen statistic (3:08–3:12) must not ship; Notebook rendered Boards 1, 2, 4 and the close; corner mark on every frame
LISTENING: transcript read in full; audio not auditioned
```

## Per-roll block: hallucination-2

```text
CANDIDATE: Prompts/hallucination-2.mp4 (3:29)
VERDICT: REROLL (loses to roll 1)
  Definition — RICH — 0:32 verbatim
  Four reasons — TAUGHT — 1:10–1:52 (point 4 folded into a summary)
  Pizza case — WRONG — 1:52 "There is a second type of hallucination, where the AI… misreads a genuine source" (the lesson: not every AI error is a hallucination; this one is not)
  Applications — THIN — 2:52–3:22, steps named, "unverified, not proven false" nuance missing
  Close — MET — 3:22.7 / 3:26.0, nothing after
ERRORS: 1:52 calls the misread source a hallucination
```

## Per-roll block: live v8

```text
CANDIDATE: course-assets/hallucination/hallucination.mp4 (3:57)
VERDICT: superseded by roll 1
  Definition — TAUGHT (paraphrase) — 0:45
  Four reasons — TAUGHT — 1:05–1:45; adds "The AI is not trying to deceive you" (the prompt asks for no blanket claims about deceiving)
  Pizza + distinction — RICH — 1:48–2:35
  Three steps — THIN — never named as steps; taught as a walk-through 2:35–3:40
  Close — MISSED — 3:50 the two lines run together with no pause ("…AI answer when something doesn't add up")
```

## Comparison

| Point | roll 1 | roll 2 | live v8 |
|---|---|---|---|
| Definition | TAUGHT | RICH | TAUGHT |
| Four reasons | RICH | TAUGHT | TAUGHT |
| Pizza case classified correctly | RICH | WRONG | RICH |
| Steps named | RICH | RICH | THIN |
| Both applications with the unverified nuance | RICH | THIN | TAUGHT |
| Close verbatim, clean | MET after two cuts | MET | MISSED |
| Runtime | 4:50 → 4:40 | 3:29 | 3:57 |

Roll 2's verbatim definition was considered as a graft under Board 1 and not taken: roll 1's
definition is TAUGHT, and the seam would sit under Notebook's own drawing, not a board.

## v11 build (`build-v11/`, script `scripts/video/build_hallucination_v11.py`; v9/v10 superseded)

- SHA-256 `7522c552696b4201d7525dcaf58c823167fb1148f74d1fb52d543c78a0a26c35`; only the why-board frames differ from v10 (new arrows), 2 seams re-guarded, pass.

## v10 build (superseded)

- SHA-256 `4584c563233bfa7dcf7bb318f4da8173b69fb1eccda97ee84308463787be9bba`; the v9 figures below otherwise hold (same frames, audio, covers, corner-mark counts).

- SHA-256 `e6e648180ea559d59b19f203b19b803cbe2e61189354af085af42404f3b37254`, 8,412 frames (4:40.40).
- Narration: roll 1 with the two cuts above; single voice; no grafts; no added pauses (natural gaps
  0.42–0.70 s at every board boundary). Rendered transcript checked end to end: the closing lines
  are the last words.
- Boards: canonical Nothing Sounds Wrong (compact; AI bubble ring at "It cites", banner at "But the
  study does not actually exist"); Why Hallucinations Happen (dense; complete-card dives at each
  point's onset); Check the Claim (compact; step rings at the names, then again at each Stanford
  application beat); post-only Real Text. Wrong Meaning. as two illustration walks (2:28–2:56 over
  the Reddit explanation, 4:03–4:29 over the pizza application), which also cover Notebook's
  fabricated Reddit cards; the invented lost-items statistic (3:04–3:12) covered by a hold of the
  preceding TRUTH/FALSEHOOD drawing; standard close as the final frame. Longest board run 47 s.
- Corner mark cleaned on every kept frame (2,686 cloned, 136 inpainted, 0 declined).
- `transition_guard.py` 11/11 pass; strips inspected. Contact sheets reviewed end to end; no
  photograph, no username, no web address, no engine outro. Protected files unchanged.

## Listening checks for David

1. 4:29.5 — the audio cut removing "As this banner states," (seam sample jump 0.0005; both sides in room tone).
2. 4:37 — the close now ends on "source." with the post-close sentence gone.
3. 2:28 and 4:03 — the pizza board arrives mid-sentence both times (audio continuous; visual check).

## Ship notes

On approval: replace the live file, cache key `20260921ship2`, pill stays 4 min (4:40 rounds to 5;
owner's call). Both raw rolls stay until the ship; then roll 2 goes.
