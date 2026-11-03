# When You Need More — repaired review candidate

Built 2026-11-03 following the owner’s “Build it please.”

Candidate: `Prompts/when-you-need-more-v7.mp4` — 2:48.967, 1280 × 720, 30 fps. Review candidate only; installed v4 remains unchanged. Intermediate v5 and v6 are retained, superseded by v7’s app-diagram repairs.

## Approved production plan

Roll 8 supplies the spine. Two complete roll-6 passages restore the human-thinking distinction, full thinking explanation, and Deep Research’s sourced report plus the complete physics example. Removed the physical-engine sentence and all obsolete banner narration. All six examples remain. Minor opening paraphrases were accepted as part of the approved repair recommendation; this is not a claim of verbatim opening compliance.

Current banner-free comparison boards appear in full view, with 4 px highlights following each whole-card description and its example separately. Source drawings remain where useful: conversation phone, task examples, optional switches, app/LLM, hourglass, clock, documents/network, web lookup. Targeted repairs simplify app labels and remove the fake model menu. The optional three-choice overview replaces the misleading controls. The native node animation is preserved, including its fade, without a rectangular compositing seam. The canonical close holds, pushes, and settles. No instructional pauses were added; only the standard closing tail.

## Narration content check

The complete encoded-audio transcript was compared with `index.html`’s ChoosingModelSection and `lessons/when-you-need-more.md`. This is transcript-based review, not direct listening or a shipping KEEP verdict.

| Teaching point | Result and output time |
| --- | --- |
| Ordinary chat; demanding plans/options/sources | TAUGHT, 0:00–0:14 |
| App/subscription qualification; three optional choices; no need to change every time | TAUGHT, 0:14–0:29 |
| LLM powers the app; model choice; capabilities; start with default | TAUGHT, 0:29–0:44 |
| Everyday model; funny movie tonight | RICH, 0:46–0:53 |
| More capable model; summer business costs, pricing, customer count | RICH, 0:53–1:02 |
| Choosing LLM versus time on task; AI does not think as humans do | TAUGHT, 1:02–1:18 |
| Less thinking; routine work; meeting notes into checklist | RICH, 1:22–1:34 |
| More thinking; steps, options, checking; analysis/coding/planning | RICH, 1:35–1:47 |
| Project: four people, one week, different schedules, two video editors | RICH, 1:47–1:56 |
| Research combines websites; regular chat can look things up; fuller investigation | TAUGHT, 1:56–2:12 |
| Regular chat; Dallas drive to Texas A&M College Station versus UT Austin | RICH, 2:12–2:21 |
| Deep Research compares websites and builds a report showing sources | RICH, 2:22–2:28 |
| Physics programs, undergraduate research, admissions, costs, sources | RICH, 2:28–2:41 |
| Both required closing lines | MET, 2:42–2:46 |

No essential teaching point is absent in the assembled transcript. The Career Explorer lab remains outside the narration. The base.en transcript renders the first sentence’s last words as “go out”; the medium.en source transcript reads “going.” The opening uses uncut roll-8 audio; this is an ASR discrepancy to confirm in the listening pass, not evidence that the cut removed a word.

## Verification and limits

See `encoded-qa.json`, `transitions/transition-guard.json`, `edit-manifest.json`, and `transcripts/`. The final QA sequentially decodes the complete candidate, checks all 14 edit boundaries, saves encoded-frame samples and transition strips, checks audio clipping and splice neighborhoods, and verifies protected hashes. v7 audio is compared sample-for-sample against the decoded v6 AAC already transcribed; transcript reuse requires equality, not an assumption.

Visual review covers the encoded sample sheets, the final app-scene repair, all transition strips, board-highlight states, and closing frames. This is sampled visual inspection, not an end-to-end audiovisual watch. No direct listening was available. Voice/cadence continuity at the donor joins and full playback still require an ear check before shipping. Signal checks alone do not establish that a join sounds natural.

Audio joins for listening: 1:01.73, 1:11.40, 1:55.87, 2:21.20, 2:41.30. The source-to-donor gain is +1 dB based on measured comparable-speech loudness. Cuts fall in quiet source gaps with short ramps; no phrase-level grafts were used.

Rebuild from pristine sources with `scripts/video/build_when_you_need_more_v7.py` under a new unused candidate name. Existing candidates are never overwritten. Source rolls, canonical boards, lesson Markdown, and installed video remain unchanged.

Final checks: PASS — 5,069 decoded frames; all 14 transition guards pass; no decoded clipping (peak −0.83 dBFS); final audio is sample-identical to the transcribed v6 audio; all protected hashes unchanged. Final transition strips and repaired app-scene samples reviewed. Candidate SHA-256: `ae5499e7373e2cbd5231c4cebbdd1b3df3a5814c1e540729b427ba9a0cb8eaf3`.

## Shipping update

Owner approved shipping. Installed and committed locally as `b4993f70fceb7cb65bb1af627e7b418c68322afa`; queued for batch deployment. See `SHIP.md`. Prior review-status statements above describe the pre-approval state.
