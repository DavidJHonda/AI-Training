# Loudest Voices: live evaluation, September 30, 2026

**Owner follow-up:** David confirmed that “Worrier” is pronounced correctly and approved building the suggested visual improvements. The pronunciation flag below is resolved; preserve the narration. Build record: `../loudest-voices-build-2026-09-30-v8/REVIEW.md`.

## Recommendation

Preserve this narration. The core teaching is complete and the progression works: competing opinions, three experts with qualified positions, historical misses in both directions, human adoption, personal judgment. A reroll is not justified by the evidence inspected. The strongest opportunity is visual framing on the expert board, with smaller readability improvements to the supporting diagrams.

**Narration verdict: provisional KEEP on teaching coverage.** This is not a completed audiovisual certification. Review used the complete fresh transcript, selected ASR checks, five sequentially decoded contact sheets spanning the video, selected full-resolution frames, current lesson/board content, and the matching build record. I could not directly hear the audio or watch continuous audiovisual playback with the available tools. Pronunciation, audio joins, and motion quality therefore remain unverified. The prior review's claim that Hinton is called “warrior” is an ASR flag, not an established listening finding.

## Exact live file

- Public course: https://besmarterthanthetool.com/
- Public reference verified: `course-assets/loudest-voices/loudest-voices.mp4?v=20260924ship1`.
- Public bytes streamed and hashed: 23,088,951 bytes; SHA-256 `e671f6bceff6b2e31d1dee294c638c437e951d7cb99a708ffd981ae812f16391`.
- Local canonical file has the same hash and matches the v7 build record.
- 1280 × 720, 30 fps, 6,884 frames decoded sequentially, 3:49.467 runtime.
- All three current canonical board hashes match the assets recorded in that build. No stale board asset was identified.
- Authority: `WhatPeopleSaySection` in `index.html`; current boards; upload text in `lessons/loudest-voices.md`. Historical review used for provenance, not as a substitute for this inspection.

## Teaching review

Times below are approximate output times from fresh ASR, cross-checked against the source transcript and the edit's approximately 4.23-second cut offset after the opening edit. Machine transcription is not evidence of exact pronunciation.

| Essential point | Assessment | Evidence on the live output |
|---|---|---|
| Many opinions; whom should a student believe? | TAUGHT | 0:00–0:16, YouTube/TikTok, friends/family, noise, then AI builders. The quadrillion joke is omitted harmlessly. |
| Same field, same evidence, different bets | RICH | 0:19–0:24, stated directly. |
| Amodei: identity and relevant background | RICH | 0:29–0:39, GPT-2/GPT-3, Anthropic, Claude. “Helped build” is appropriately qualified. |
| Amodei: medical optimism | RICH | 0:39–0:50, preserves the 50–100 years into 5–10 years comparison. |
| Amodei: systems may lack maturity for that power | RICH | 0:50–1:03, includes social, political, and technological systems. |
| Hinton: identity and background | RICH, pronunciation unresolved | 1:03–1:14, Nobel Prize and leaving Google at 75 to warn about AI. |
| Hinton: given goals can produce other goals | RICH | 1:15–1:25, the full causal explanation is present, not merely “AI is dangerous.” |
| Hinton: early cancer detection benefit | RICH | 1:25–1:32. |
| LeCun: identity, Turing Award, disagreement with the approach | RICH | 1:32–1:40. |
| LeCun: LLM dead end and house-cat comparison | RICH | 1:41–1:50, both claims present. The second quotation is introduced as a paraphrase rather than being recited verbatim from its first word. |
| LeCun: acknowledge risks and human agency | RICH | 1:51–2:00, explicitly connects building AI to controlling its risks. |
| None has a simple one-sided view | RICH | 2:01–2:14, names the optimism/danger, worry/benefits, doubt/risks reversals. |
| Even the experts cannot settle the future | TAUGHT | 2:09–2:18, carried by narration without requiring viewers to read the board. |
| Historical bridge; predictions miss in both directions | TAUGHT | 2:18–2:29. |
| Stoll, 1995, online shopping versus malls; outcome | RICH | 2:35–2:44. |
| Ballmer, 2007, iPhone market share; outcome | RICH | 2:44–2:53. |
| Metcalfe, 1996, catastrophic internet collapse; outcome | RICH | 2:53–3:04. |
| Ford, 1940, flying cars; still not ordinary transport | RICH | 3:04–3:13. |
| People change the result | TAUGHT | 3:18–3:22, the board's conclusion is spoken. |
| Adoption/habits explain the uncertainty | RICH | 3:22–3:40, machine improvement contrasted with human adaptation; all three source sentences about habits are present. |
| Two closing lines | TAUGHT / MET in transcription | Approximately 3:41–3:46, “Where AI will be in ten years is a bet” and “Which voice you listen to is your call.” |

The five “Right or Wrong?” questions are page-based practice. Their generalization is taught by the video's four historical examples; the video's omission of those extra quiz cases is not treated as a missing essential explanation.

**Hard requirements:** the same-field line, one-sided-view line, people-change-the-result line, habits block, and two closing lines are present in transcription. The expert quotations preserve the essential claims and qualifiers. Exact spoken words/pronunciation still need listening where ASR is ambiguous.

**Errors:** no confirmed material teaching contradiction. Approximately 1:04 remains a pronunciation question. Base ASR also writes “warrior” during the summary around 2:06, whereas the older medium-model source transcription distinguished the two occurrences; that disagreement is why this report does not assert either pronunciation by ear.

A fresh medium-model check of the actual live audio at 1:01–1:10 also transcribes “Next is the warrior, Jeffrey Hinton” at approximately 1:03.54–1:05.52. Two recognition passes agree on the introduction, making it worth checking, but they still do not establish what a listener hears.

**Source QA:** no material conflict identified between current page, boards, upload content, and narration. This review does not independently authenticate all external quotations or historical sources.

**Additions:** the opening expectation that builders would agree helps set up the contrast. The additional machine/adaptation explanation reinforces the habits takeaway. Neither needs removal.

## Visual findings, ranked

1. **Expert-board framing, roughly 0:39–2:00.** At full view, the tall board is only about 680 pixels wide within the 1280-pixel video. Its body text is very small. During the quotations, the camera crops deeply into SAYS or BUT ADMITS, hiding the expert's name and role while leaving fragments of neighboring text visible. The quotes become readable, but attribution and orientation are lost. See `frame-052.jpg`, `frame-083.jpg`, and `frame-110.jpg`. A future rebuild should preview complete-card framing under the current spec; these very tall cards may not gain enough readability without a separately approved layout solution. Do not promise that merely reducing the zoom solves both problems.
2. **Older, heavy highlight rings.** The rings visibly become heavier in close views. This is an older build. Edit Spec section 5 explicitly exempts earlier shipped videos from rebuilding solely for the newer fixed 4-pixel rule. Normalize rings if the board is rebuilt; this is not, by itself, a reason to replace the live video.
3. **Supporting diagrams contain small, abstract labels.** The historical chart at 2:18–2:29 illustrates over- and underprediction usefully, but its labels are faint and small. At 3:22–3:37, “EXPONENTIAL / HIGH-FREQ,” “LINEAR / HABIT INERTIA,” and “STRUCTURAL FRICTION GAP” introduce jargon that the plainspoken narration does not need. Prefer a targeted label treatment such as “Machines improve fast,” “Habits change more slowly,” and “Adoption takes time,” preserving the useful visual comparison. The diagram's numbers/marks are illustrative, not a reason to reject it as fabricated data. Continuous motion has not been viewed, so any retiming judgment remains provisional.
4. **Long board runs, but still teaching.** The verified matching build places Board 1 at 0:23.73–1:09.33, 1:14.13–1:37.67, and 1:40.17–2:18.07. Board 2 runs 2:29.40–3:22.30, or 52.9 seconds. These are long, especially for teenagers, but the narrator continues through distinct content rather than filling time. The two extended expert-board holds were expressly requested by David in the v7 record. Preserve those choices; do not automatically insert stock breaks or cut narration to meet a duration target. No specific new donor illustration has been verified in this review.

**What works visually:** the opening opinion-noise illustration; the clear active-card sequence on the predictions board; the visible bottom edges of both second-row highlight boxes; full-view expert synthesis with cards highlighted as named; and the canonical two-line close. The literal final decoded frame is the expected close, with no subsequent graphic. Sampled close frames show the expected push/settle progression; continuous motion is not certified.

## Proposed treatment if a revision is requested

Scope: targeted visual refinement; retain narration and duration unless the pronunciation check establishes a specific audio repair. No edit or publication is performed by this evaluation.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason / qualification |
|---|---|---|---|---|
| Even the Experts Don’t Know | Whole Amodei card → SAYS → BUT ADMITS; repeat for Hinton and LeCun; whole cards as named during synthesis | Unmarked full opening; preview complete active-card framing; return to full comparison for synthesis | Preserve current 0:23.73–2:18.07 structure, including breaks at 1:09.33–1:14.13 and 1:37.67–1:40.17 | Main improvement is keeping speaker context visible. Tall cards make a readability preview necessary. Preserve David's requested uninterrupted Amodei qualification and synthesis. |
| This Has Happened Before | Whole Stoll → Ballmer → Metcalfe → Ford cards; then complete takeaway banner | Preserve full opening and complete-card dives/pans | 2:29.40–3:22.30; no added cutaway proposed | The existing walk works. Normalize rings only if rebuilt; preserve complete second-row bounds. |
| Where AI will be in ten years is a bet. / Which voice you listen to is your call. | No rings | Preserve canonical close and standard motion | 3:36.70–3:49.47 | Current final image is correct. |

Supporting scenes provisionally retained: opinion bubbles and viewer drawing, 0:00–0:14; consensus setup, about 0:14–0:23.5; building drawing, 1:09.33–1:14.13; “Flawed Approach,” 1:37.67–1:40.17; historical predictions, 2:18.07–2:29.40; machine/adaptation comparison, 3:22.30–3:36.70. The last two are candidates for label cleanup, not wholesale replacement.

**Narration repairs:** none established. For the possible Hinton label issue, the old source record identifies `Prompts/loudest-voices-1.mp4` around 2:10.12–2:10.46 as a possible correct-word donor for source 1:08.44 (live about 1:04.21). This remains an unauditioned lead, not a verified repair plan. Do not splice it based on ASR alone.

**Selective pauses:** none proposed. Listening is required before proposing a timing change. The existing opening edit's approximately 0.55-second joined gap is documented in the earlier build but has not been re-certified by ear here.

## Verification limits

- Fresh base-model ASR invented “Thank you very much” at 3:47–3:50. The file ends at 3:49.467, and half-second RMS samples at 3:46, 3:47, 3:48, and 3:49 measure approximately −66.1 dBFS, the held room-tone floor. The source transcript also ends with the correct closing line. Do not treat this ASR tail as an actual spoken outro.
- No full continuous watch/listen, audio seam audition, or donor-join audition was possible. Contact sheets do not certify animation quality or absence of one-frame defects.
- No new transition-guard certification is claimed; the matching older build's result remains historical evidence.
- Supplementary whole-file ring measurement and remaining medium-model excerpt checks were stopped after the useful primary review evidence was collected. No numeric ring-width result or completed medium-model summary/close check is claimed.
- The Video Tracker was not accessed or updated; no workflow status is inferred from it.
- Canonical video, boards, lesson, and site were not edited. Generated review evidence remains in this audit folder.
