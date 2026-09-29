# Fake Trap — live-video evaluation, September 29, 2026

**The live video teaches the lesson well, but it is not a clean pass against all current specifications.** The principal visual repairs are a 41.10-second comparison-board run, a 31.47-second checks-board run, and a Corroboration ring that remains through a summary of all three checks. Four of the current prompt's eight required verbatim lines are paraphrased. Their meaning is present; these are exact-wording failures, not four missing teaching points.

This is an evaluation only. No course file, lesson, prompt, canonical board, or site reference was changed. No build or publication was performed.

## Identity and evidence

- Public video: https://besmarterthanthetool.com/course-assets/fake-trap/fake-trap.mp4?v=20260921ship25
- Verified September 29 at 18:07 UTC by streaming and hashing the complete public MP4 and all five public JPG assets. All six match local files exactly. The public lesson section also matches local `index.html`.
- Video: `course-assets/fake-trap/fake-trap.mp4`; 34,219,610 bytes; SHA-256 `8fffe6bdf9de2fc9e8b6736a18b2235f5b54e6992ec8fd1873a3bdd7195ab24e`.
- 1280×720, 30 fps, 9,240 decoded frames, 5:08.00. This matches the September 21 v6 manifest exactly.
- Authorities: `index.html` / `SyntheticMediaSection`, `lessons/fake-trap.md`, `gemini-notebook/fake-trap/PROMPT.txt`, and the September 29 README, EDIT-SPEC, and NARRATION-REVIEW in `scripts/video/`.
- Seven new contact sheets cover the whole file at four-second intervals. Current board images and all twenty boundary strips were inspected. These are sampled-frame and every-frame boundary inspections, **not an end-to-end audiovisual playback**.
- Historical complete transcript: `video-audit/fake-trap-materials-test-2026-09-20/build-v4/verification/fake-trap-v4/transcript.txt`. The subsequent v5 and v6 changes were visual-only, with unchanged audio documented in their manifests/reviews. The fresh complete transcript from the exact installed file, `fake-trap/transcript.txt`, was read in full and reproduces the historical wording and all four literal mismatches.
- Public evidence: `public-verification.json`; live lesson text: `public-lesson-source.txt`; frame evidence: `sheets/`; cut evidence: `transitions/`.
- Video Tracker was not accessed or updated.

## Findings

### 1. Long board runs need a current-spec cutaway plan

| Board | Exact output interval | Unbroken run | Assessment |
|---|---|---:|---|
| The Same Clip. Two Eras. | 0:26.80–1:07.90 | 41.10 s | Clear §8b target. The narration walks both eras effectively, but the picture stays on the board throughout. Preserve the row-level explanation and add one relevant break. |
| Why Some Fakes Aren't Friendly | 1:34.33–1:55.90 | 21.57 s | Borderline against “about twenty seconds.” Four complete-card views change quickly. Retaining this as an explicit exception is preferable to inserting a token decorative cutaway. |
| Check the Source, Not the Pixels | 2:17.43–2:27.13 | 9.70 s | Appropriate short compact board. |
| Move the Test Off the Image | 2:38.07–3:09.53 | 31.47 s | Clear §8b target. Compact full-board framing is appropriate, but the long hold needs a relevant break. |
| Standard close | 4:58.87–5:08.00 | 9.13 s | Preserve the canonical close. |

These exact intervals come from the build manifests tied to this file's hash, checked against current boundary strips. The new board matcher provides an independent half-second sampling check; its edges are approximate.

There is no minute-long chain of consecutive boards: Notebook scenes separate them. The applicable current issue is the individual-board rule added September 23, after this release. This is a current-spec upgrade, not evidence that the September 21 edit violated a rule that did not yet exist.

### 2. The last checks highlight outlasts its spoken target

At about **3:00.7–3:09.5**, narration says “By applying these checks…” and explains moving the burden of proof to external evidence. The **Corroboration** ring remains visible in the 3:04 and 3:08 frames and up to the outgoing boundary.

Clear the ring when the narration returns to all three checks, or cut to a supporting evidence-trail scene for this summary. Do not ring the banner merely because it is available: its specific sentence is taught later at about 3:59.

### 3. Four exact lines do not meet the current prompt's literal requirement

| Required wording | Current narration and approximate output time | Literal result |
|---|---|---|
| “Appearance can mislead. The source trail can be checked.” | Same words, 1:04–1:08 | MET |
| “The Fake Trap is believing it because it looks real.” | “The fake trap is believing **a piece of media** because it looks real,” 1:08–1:12 | MISSED; meaning taught |
| “Harmful fakes are made to get something back.” | “Harmful fakes are specifically engineered to extract something from you,” 1:30–1:34 | MISSED; meaning taught |
| “Treat its verdict as a clue, never a ruling.” | A detector can flag a pattern but cannot make the final decision; tools conflict, 2:03–2:17 | MISSED; meaning taught |
| “Check the source, not the pixels.” | Same words, 2:21 and 5:02 | MET |
| “Verify somewhere the sender does not control.” | “You must verify **information** somewhere the sender does not control,” 3:59–4:03 | MISSED; meaning taught |
| “You did nothing wrong by being targeted.” | Same words, 4:56–4:59 | MET |
| “Seeing or hearing isn’t proof anymore.” | Same words, 4:59–5:02 | MET |

The September 20 evaluation already noted the motives and detector paraphrases and recommended accepting their meaning. Its approved plan retained the base detector narration; the subsequent build review records the owner's positive assessment. That history matters: do not silently convert a previously accepted paraphrase into a claim that students are missing its concept.

Nevertheless, the current prompt says these lines must be exact. Under NARRATION-REVIEW's strict hard-requirement rubric, this file cannot earn a fresh unconditional KEEP. **Strict verdict: REROLL for literal compliance, provisional on listening**, because no complete, verified, available audio repair for all four lines has been established. This does not mean the lesson's substantive teaching needs replacement.

The historical roll-1 transcript supplies the exact definition at 0:56.80–1:00.30 and verification rule within 3:04.30–3:10.30. However, `Prompts/fake-trap-new-1.mp4` and `fake-trap-new-2.mp4` are absent at review time. The older detector donor is itself near-verbatim; it does not solve strict compliance. Historical transcripts alone are not usable audio donors, and no graft or join has been auditioned. A visual repair can preserve the previously accepted narration, but cannot claim to resolve these literal failures.

### 4. Ring width is an inherited exception, not a standalone rebuild reason

The September 21 synchronization used artwork-scaled outlines on the comparison and follow-source boards, while the other two boards retained the earlier fixed-width treatment. Current §5 requires fixed 4 px at 720p **and expressly says videos shipped under earlier rules are not rebuilt solely for this**. Preserve that exception when evaluating this release. Any newly rebuilt board span should use the current fixed 4 px rule.

The README and §10 still contain older “5 px” language; §5 explicitly supersedes it. Do not use that stale checklist phrase as the target for a new build.

## Teaching coverage, in lesson order

The following assesses the complete transcript's meaning. Exact-wording compliance remains separately failed above.

| Teaching point | Assessment | Evidence |
|---|---|---|
| Cheap convincing fakes; awareness is not a skill; the first ten seconds | RICH | 0:00–0:18 gives the problem and why knowledge alone is insufficient. |
| Principal cancels school next week | RICH | 0:20–0:26 supplies the scenario used throughout. |
| Before AI: face, voice, hallway, manner of speaking, “real” verdict | RICH | 0:31–0:46 walks the original test and verdict. |
| AI era: source trail, school website, “unverified” | RICH | 0:46–1:08 explains why the test changes and states the takeaway. |
| Both jaws: believing a fake and dismissing truth | RICH | 1:08–1:17 makes the second danger explicit. |
| Stanley Cup joke; deception changes the situation | RICH | 1:17–1:30 preserves the example and distinction. |
| Money, power, fame, cruelty and their reasons | TAUGHT | 1:30–1:56 explains each; power compresses the page's vote/protest/spend list to vote/spend without losing the influence concept. |
| Detectors: patterns, conflicting answers, no final authority | TAUGHT | 1:56–2:17 carries the limitation and independent-investigation response. |
| Move from pixels to source | RICH | 2:17–2:27 states and explains the change. |
| Outrage, fear, excitement, hope; stop before reacting/sharing/believing | RICH | 2:27–2:38 names all four emotions and the action cue. |
| Source, context, corroboration with questions | TAUGHT | 2:38–3:09 explains the three checks. Source says “a way to know” rather than separately repeating “a reason and a way”; motives were already explained. |
| Apply every check to the school clip | RICH | 3:09–3:44: find the original school announcement, check date/school, then a separate trusted school channel or front office. |
| Reposts are not independent confirmation; unverified is not a finding of fake | TAUGHT | 3:38–3:56 rejects circular reposts and says definitive proof of AI generation is unnecessary. The upload's explicit “That does not prove the clip is fake” would be clearer, but the current distinction is conveyed. |
| Verify beyond sender control; voicemail and viral-clip examples | RICH | 3:56–4:17 explains the rule and both actions. |
| Eyes remain useful, but not as a lie detector | RICH | 4:17–4:26 preserves the contrast. |
| Targeted personally: save safe details, adult that day | RICH | 4:26–4:41 covers username/link/date/messages and adult support. |
| Under-18 private-image rule; adult/platform; Take It Down/CyberTipline | RICH on transcript | 4:41–4:56 includes all prohibitions and both resources. ASR spelling is not evidence of mispronunciation; listening remains needed. |
| Not the target's fault; both closing lines | RICH | 4:56–5:04, with no additional spoken outro in the transcript. |

**SOURCE_QA:** no material source contradiction identified in this comparison. **ADDITIONS:** the full school-closure application expands the visible page usefully and is explicitly present in the upload Markdown. No substantive narration cut is recommended for runtime. Some phrases (“engineered to extract,” “burden of proof onto verifiable external evidence”) are more formal than the prompt's requested voice, but remain understandable; this is polish, not missing teaching.

## Notebook scenes to preserve

The inspected sequences support the lesson. Full synchronized motion/audio evaluation remains outstanding, so these are retention recommendations, not a new motion certification.

- 0:00–0:26.8: media types, awareness versus skill, first-ten-seconds cue, principal phone sketch.
- 1:07.9–1:34.3: two jaws, shared Stanley Cup joke, intent/motives. The “100% VERIFIED” record illustrates rejecting established truth; it is not presented as an empirical detection rate.
- 1:55.9–2:17.4: detector scan, an ambiguous illustrative percentage, conflicting tool results, independent checks. Under current §8, do not remove the illustrative percentage solely for lacking a statistical citation.
- 2:27.1–2:38.1: emotions spreading and the stop/check response.
- 3:09.5–3:56: the source/context/corroboration school application, circular reposts, and unverified status. The illustrative old date and different school make context checking concrete.
- 3:56–4:26: sender control, known-number callback, original source, and the eyes/lie-detector distinction.
- 4:26–4:58.9: victim support, safe metadata, trusted adult, all three private-image prohibitions, reporting help, and reassurance.

Drawn people are allowed under §8c. Their presence is not a reason to replace these scenes with photographs. No Notebook stock-photo or engine-mark problem was apparent in the inspected samples; sparse sampling does not prove frame-by-frame absence. The historical build recorded five photo replacements and mark cleanup on every retained Notebook frame.

## Proposed visual-only plan

This is a review proposal, not an executed or newly approved build. Preserve narration, duration, and pauses. If a new compliant narration roll is chosen instead, retime the board plan to that audio.

| Board | Highlighting sequence | Camera | On screen / proposed breaks | Reason or exception |
|---|---|---|---|---|
| The Same Clip. Two Eras. | Retain owner-approved section sequence: question, evidence/checked, matched, verdict; AI-era question, source trail, skipped, checked, verdict; final banner. New rings 4 px. | Full unmarked opening; dense complete-card views; full-board takeaway. | Existing 0:26.8–1:07.9. Candidate break 0:43.9–0:48.4 using the existing principal-phone sketch from about 0:20.4–0:24.9. This leaves approximately 17.1 s and 19.5 s board runs. | Makes the “looks real / old test fails” transition concrete. Preview exact motion and boundary frames before committing this retiming. |
| Why Some Fakes Aren't Friendly | Money → Power → Fame → Cruelty whole-card rings; retain the previously approved unringed banner. | Full opening, then complete-card views. | Keep 1:34.33–1:55.90, 21.57 s, as an explicit “about twenty seconds” exception. | Four quick distinct views already track four concise explanations. No useful additional break identified; do not add filler. |
| Check the Source, Not the Pixels | Full unmarked opening; banner at its spoken explanation. | Compact full view. | Keep 2:17.43–2:27.13, 9.70 s. | No long-hold defect. |
| Move the Test Off the Image | Source → Context → Corroboration whole-card rings; clear Corroboration at the all-checks summary around 3:00.7. | Compact full view throughout board portions. | Existing 2:38.07–3:09.53. Candidate break 2:47–2:52.8 using the existing worked-example date/full-announcement scene around 3:22–3:27.8; return roughly one second before Corroboration. Approximate remaining runs: 8.9 s and 16.7 s. | Shows what “context” means while keeping the overview readable. Inspect motion with narration before selecting exact source frames; avoid duplicating a later reveal awkwardly. If that retiming weakens the later application, propose a minimal custom full-announcement/date illustration instead. |
| Seeing or hearing isn’t proof anymore. / Check the source, not the pixels. | No added ring. | Canonical 48-frame hold, 150-frame push to 1.2×, settled hold. | Preserve 4:58.87–5:08.00. | Standard close. |

No narration graft is represented as ready. No new pause is proposed: neither a heading nor a highlight change justifies inserting silence. Before any build, resolve whether to retain the previously accepted paraphrases or pursue literal prompt compliance, then finalize the supporting-scene timings through playback.

## Verification and limits

- Public MP4, all boards, and lesson section verified against local files.
- Fresh transition guard decoded 9,240 frames and tested 20 declared boundaries: 19 automatic passes and one flag at f2931 (1:37.70). Manual strip review shows continuous camera movement into Money, not a one-frame foreign image; this reproduces the historical false positive. The machine result remains FAIL in the raw report rather than being silently relabeled.
- All twenty strips were reviewed in montage; no stale-image island was identified at those boundaries.
- Full lesson and complete timestamped historical transcript read; fresh encoded-file transcript also read in full; close measurements recorded below.
- **Not performed:** auditory review of the complete file, pronunciation/cadence checks, real-time review of all animation, or a full-frame watermark/license audit. In particular, listen at the motives graft around 1:37.7 and 1:55.9, the transition at 2:27, resource names around 4:52, and the close entry at 4:59.
- These limitations prevent a fresh whole-file shipping certification. Historical approval and byte identity do not substitute for checks claimed to have been performed today.

## Fresh verification addendum

- The fresh ASR pass produced 81 complete timestamped segments. It agrees with the historical transcript on the teaching and all four verbatim mismatches. The ASR artifacts “reported” / “NC mecs” are flagged for listening, not called narration errors.
- An additional sequential decode independently counted 9,240 frames at 30 fps. Close measurements at f8966/f9013/f9014 show a 720 px pill; f9163/f9164/f9239 show 864 px, confirming the initial hold, 1.2× push endpoint, and settled final image at the planned boundaries. The literal final frame was inspected (`close-9239.jpg`); it is the canonical close. This is a sampled geometry check, not a claim to have watched the entire push in real time.
- Fresh ORB board matching independently measures comparison 41.0 s, reasons 21.5 s, follow-source 10.0 s, and checks 31.5 s (half-second samples), agreeing with the exact manifest/boundary intervals above. Its low-confidence `close` hit at 4:50–4:52 is a false positive: inspected frames show the Trusted Adult / Platform Report / Take It Down scene, not an early close. The real close starts at f8966.
- Fresh ring scanning (`ring-stroke.txt`) finds comparison and follow-source outlines at 4 px in detected samples. Reasons-board detections reach about 6–7.5 px; Source and Corroboration on the checks board measure about 7 px. These are measured colored-outline widths, which may include adjacent native card borders; they should not be equated automatically with a renderer's nominal stroke setting. The 16 px secondary violet detection on Source and gold detections at 4:33 are not evidence of additional intended course highlights. The pre-September-26 exception still applies; use fixed 4 px and inspect overlap with card edges in any rebuilt span.

## Owner follow-up and operative decision

After this evaluation, David asked whether the recommendation was reroll or repair. The recommendation was clarified as **repair**: keep the existing narration and useful animation, add the two cutaways, and clear the lingering Corroboration highlight. The prompt paraphrases preserve meaning and had already been accepted; a full reroll was not recommended solely for those differences. David then explicitly requested building that repaired version. This is the operative scope for `video-audit/fake-trap-repair-2026-09-29-v8/REVIEW.md`; the strict-rubric discussion above must not be mistaken for an instruction to reroll or alter the approved audio.
