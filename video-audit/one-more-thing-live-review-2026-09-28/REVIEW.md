# One More Thing — current-spec review, 2026-09-28

**Recommendation: KEEP the narration, with targeted visual repairs. No reroll recommended on the teaching evidence.** This is a content and sampled-frame assessment; direct end-to-end listening/viewing remains outstanding, so it is not a full shipping certification.

## Verified version and scope

Fresh public-page lookup selects `course-assets/one-more-thing/one-more-thing.mp4?v=20260923ship3`. Streamed public bytes match the local file: SHA-256 `bd076d8d401a95a87e82ad3e317766f61c4bce3985120e4e313971425ad3eea8`, 26,260,787 bytes. Runtime 3:43.90, 6,717 frames, 30 fps, 1280×720; the 4 min duration pill is appropriate. See `published-verification.json`.

Read the current page's One More Thing component, `lessons/one-more-thing.md`, current prompt, shared workflow, Narration Review and Edit Spec. All three teaching JPGs hash-match the retained build's assets (`asset-check.json`); the closing picture matches the current closing copy. Read the full fresh ASR transcript and inspected all five four-second contact sheets, the board sheet, and full-resolution details. The old build report's “live unchanged” language is historical; public-byte verification establishes that its built version is now live.

No lesson, video, prompt, tracker, or published asset was changed.

## Narration

```text
LESSON: one-more-thing
CANDIDATE: course-assets/one-more-thing/one-more-thing.mp4 (3:43.90)
VERDICT: KEEP — content recommendation, subject to listening verification
TEACHING POINTS:
  Three opening questions — TAUGHT — 0:00–0:10 sets up different answers, temperature, and calculation scale.
  Dog-name example; highest probability does not guarantee selection — TAUGHT — 0:13–0:34, Spot at 22%.
  Meaning of 22% — RICH — 0:34–0:43, about 22 times out of 100, on average, if odds stay the same.
  Same probabilities, five independent picks — RICH — 0:54–1:22, all six probabilities, unchanged odds, Max/Spot/Buddy/Rex/Max, one possible sequence, Spot once, another five can differ.
  Highest chance is not a guarantee — TAUGHT — 1:22–1:26.
  Variety and a changed token affecting what follows — TAUGHT — 1:26–1:45; branching picture supports the second relationship.
  Temperature reshapes probabilities before each pick; handled behind the scenes — TAUGHT — 1:45–1:55.
  Low versus high temperature — TAUGHT — 1:55–2:10; Spot rises to 36%, then falls to 16%; effects on less likely choices explained.
  Temperature does not change learning — TAUGHT — 2:10–2:16.
  Training creates weights, which stay fixed during use — TAUGHT — 2:22–2:33.
  Imagined trillion-weight model and two calculations per weight — TAUGHT — 2:33–2:46.
  Calculation scale — RICH — 2:46–3:12; one token about 2 trillion, 100 generated tokens about 200 trillion, 1,000 about 2 quadrillion.
  Estimates for an imagined model, not real measurements — TAUGHT — 3:12–3:18.
  Even a short answer takes trillions of calculations — TAUGHT — 3:24–3:30.
  Closing lines — TAUGHT in fresh ASR — 3:30–3:40, including “Math.”
HARD REQUIREMENTS:
  All ten required passages are present in the fresh transcript, ignoring ASR capitalization/punctuation and introductory “Ultimately.” Final close also matches the original build transcript.
ERRORS: no wrong worked-example number found. Fresh base.en writes “Rax” where earlier transcripts and the board say Rex; treat this as an ASR/pronunciation check, not a proven narration error.
SOURCE_QA: no source change proposed. Both source and narration clearly frame the calculation model as hypothetical.
ADDITIONS: formal filler (“outputs are inherently capable of variation,” “sheer density of effort”) could be plainer; these do not create a missing teaching point.
REPAIR PLAN: none for narration; no cut or graft is needed on the reviewed content evidence.
EDITING NOTES: opening example consistency and board pacing; details below.
LISTENING: direct listening not performed. Check original graft joins at 0:54.27 and 1:15.43, Rex pronunciation, pauses, and the full close before any fresh ship certification.
```

The current prompt asks for every temperature-table number. The shipped narration teaches the meaningful contrast through Spot's 22% → 36% / 16% and explains the broader effect, rather than reciting all cells. This is sufficient teaching under the current verdict rubric; adding a table recitation would not improve the lesson. The 1,000-token example inherits the preceding generated-token context, though explicitly saying “tokens written by AI” would be clearer in a future version.

The Sept. 27 ASR omitted “Math” from the close. Today's fresh transcript includes it, as does the original build transcript. There is no evidence here for declaring that word missing; direct audition still controls pronunciation and cadence.

## Lesson arc

The opening promises three answers and the video delivers them in order: **why a top choice need not win → how temperature changes those odds → how much calculation each choice requires.** It keeps the dog-name example across the first two topics, then explicitly bridges at 2:16 to “the ... calculations driving these probabilities.” This is a clear connection, not an unexplained jump to a new board. The hypothetical arithmetic supports the closing “Not a mind. Math.” No new overview or process diagram is needed.

There is some repetition before the first board: the 22% explanation is followed by a general statement about variation, then the five-pick example. The example adds substance, so this is an optional tightening opportunity rather than material excess requiring an audio repair.

## Findings against production specs

| Area | Finding | Recommendation |
|---|---|---|
| Canonical course boards | All three current assets match the build; whole-board framing and substantive section/card outlines are appropriate. | Preserve. |
| Opening example, 0:16.83–0:42.90 | Generated probability sequence uses “The dog's name was…” instead of “You could name him…”. Its table redraws the course probabilities. The 100-trial illustration later in the span does explain the narration correctly, including “on average.” | Replace the alternate-context table portion; preserve the useful 100-trial illustration. Locate its precise internal animation boundary before a build. Do not replace the entire span indiscriminately. |
| Generated tree, 0:42.90–0:50.27 | “PROBABILISTIC TOKEN SAMPLING” starts from “The dog was,” branches through Spot/Max/Buddy/Rex, then adds “barking loudly” and other continuations. This changes the example and creates awkward paths such as “The dog was Max ... running fast.” | Replace with a relevant dog/name sketch; the current “You could name him…” drawing at 0:50.27–0:53.93 is an available candidate. Preview any retiming to avoid a repetitive hold. |
| Same Probabilities board | 0:53.93–1:31.70 = 37.77s uninterrupted. | Review for a purposeful break after the five picks, preserving the comparison. |
| Temperature board | 1:45.30–2:16.53 = 31.23s uninterrupted. | This is a justified comparison-heavy hold if no relevant temperature drawing improves it. Do not hide the columns merely to hit 20 seconds. |
| Math board | 2:45.93–3:30.50 = 44.57s uninterrupted; the longest teaching-board run. | Best pacing repair: cut away during the hypothetical-model qualification around 3:12–3:18, then return for the conclusion. |
| Branching illustration, 1:31.70–1:45.30 including pause | Useful demonstration that a changed choice changes the continuation. Extra percentages and jargon remain, but this specific donor drawing was explicitly approved in the build history. | Preserve the authorized treatment; disclose the extra numbers rather than silently invalidating prior approval. |
| Weights illustration, 2:16.53–2:45.93 | Supports fixed weights and the hypothetical arithmetic. Contains “FLOPs” and a small “Parameters” label beyond the plain lesson vocabulary. | Optional simplification in a visual repair; the numerical example itself matches the lesson. This is not a narration failure. |
| Ring width | Sept. 27 measurements on this identical file show about 6px on Board 1, 4px on Board 2, and 6–7px on Board 3. | Current target is fixed 4px at 720p, drawn after transforms. Apply to changed boards in a repair; older shipped widths are explicitly grandfathered and alone do not justify rebuilding. |
| Closing picture | Current wording, white stage, hold/push/settled close visible; literal final frame is the standard close. | Preserve. |
| Photographs, placeholder text, corner mark | None found in inspected samples. | Sampled finding only; not a claim of exhaustive per-frame clearance. |

Current longest board chain is 44.57s for teaching boards alone, or 57.97s including the adjacent 13.40s closing card. The spec's single-board threshold of about 20s triggers editorial review, not automatic cutting or invented filler.

## Proposed visual plan — not built

Scope: targeted visual repair, preserving narration and existing pauses. No new generation or audio editing is required by this recommendation. Current local raw rolls are absent; candidates below are available in the hash-verified live file, not assumed missing donors.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| Same Probabilities, Different Choices | Probability column → five-pick column → takeaway | Full view; no dives | Current 37.77s. Consider the existing name sketch under “Another five picks could turn out differently,” about 1:19.6–1:22.2, returning for the takeaway. | Leaves an initial ~25.6s comparison run; accept that overage rather than interrupt the actual five picks. Timing and drawing reuse provisional. |
| How Temperature Changes the Odds | Whole low column → Spot 36% → whole high column → Spot 16% → banner | Full view to retain comparison | Preserve 31.23s unless a relevant donor is recovered. | Purposeful comparison exception; no filler dog sketch proposed just to shorten the hold. |
| The Math Adds Up Fast | Whole one-token card → whole short-answer card → whole conversation card → banner | Full view | Insert the existing HYPOTHETICAL MODEL SCALE picture during the qualification around 3:12–3:18; return for conclusion. | Matching image is visible around 2:28–2:31. A representative frame at 2:30 was inspected. Final source range/retiming needs a preview. Leaves roughly 26s and 13s board runs. |
| Not a mind. Math, at a scale nobody can picture. / Every time you hit send. | Unmarked | Standard close | Retain 3:30.50–3:43.90 | Current asset and existing motion. |

Also replace the two opening inconsistencies above while retaining the 100-trial illustration. Bringing the canonical board in for the earlier probability beat must be balanced with drawings; do not create a longer uninterrupted board run as the repair. No pauses proposed without a listening pass. No changes executed.

## Verification and limits

Fresh sequential decode and ASR completed for the exact public-matching file. Fresh `transition_guard.py` passed all 13 declared manifest boundaries, zero failures. Automated guard checks visual islands, not audio joins; its frame strips were not all manually inspected. All five fresh contact sheets were inspected plus eight captured detail frames (six inspected at full resolution); current board images were inspected via the retained board sheet and matched by hash. Board durations are supported by the hash-matched manifest and fresh scene cuts.

Not completed: real-time end-to-end listening/viewing, audible graft/pauses/noise-floor checks, mobile readability or streaming behavior, exhaustive frame-by-frame mark/photograph checks. Ring measurements are retained measurements on the identical file, not fresh measurements. This review does not certify those checks or authorize a build or publication.
