# Data Centers — live evaluation, September 30, 2026

**Recommendation: retain this version; make a small visual clarification pass if revising it.** The transcript teaches the current lesson completely, with a clear progression from one answer's calculation to physical infrastructure, community effects, responses, and the limits of efficiency. No missing essential teaching or need for a new generation was identified. The boards already have supporting cutaways and readable framing.

**Review limitation:** This is a verified-public-file, complete-transcript and sampled-frame review. I did not hear the audio or watch continuous motion. A formal KEEP / REPAIR / REROLL narration verdict and audiovisual sign-off are withheld. In particular, the close graft still needs listening. Nothing was edited or deployed.

## Verified identity and evidence

- Public page: https://besmarterthanthetool.com/
- Public entry: `course-assets/data-centers/data-centers.mp4?v=20260924ship1`, displayed runtime `4 min`.
- Public stream returned HTTP 200, `video/mp4`, 34,526,116 bytes. Streamed directly to a checksum; no duplicate MP4 saved.
- Public stream, local canonical MP4, and v4 build manifest share SHA-256 `239d5a26ee58a5e28322eadc364a15af27f946324c4fe4563bb96d9a659c4130`.
- Public `TheHiddenCostSection` matches the local function exactly. Read current page, upload Markdown, canonical boards, current Narration Review and Edit Spec, and v3/v4 reviews.
- Sequentially decoded all 6,694 frames: 1280×720, 30 fps, 223.133 seconds (3:43.13).
- Inspected five newly extracted contact sheets at four-second intervals, selected full-resolution frames, current canonical boards, and the literal final frame. This is sampling, not continuous viewing.
- Complete retained transcript: `../data-centers-v3-2026-09-24/transcript-medium.txt`. The v4 record documents byte-identical decoded audio to v3. This association was reused; the transcript was not freshly generated or confirmed by listening.
- Exact board intervals below come from the matching v4 manifest and are saved in `manifest-board-spans.json`. The redundant ORB board-matching run was stopped before completion; no independent automated span result is claimed. Current sampled frames support the manifest's board/cutaway sequence.
- Tracker was not accessed; no workflow status inferred and no row drafted.

## Findings in priority order

1. **Clarify that the numerical graphics describe the worked example.** At approximately 0:12, the graphic says “Every single weight participates in generating each new token.” The narration properly starts “Let's assume,” but the graphic reads as a general rule. Retain the numerical demonstration and replace that caption with “In this example: one trillion weights used per token.” At approximately 3:04, the phone graphic says “Single Request ~2 Quadrillion Ops.” Change that to “Our 1,000-token example: ~2 quadrillion calculations.” The concern is loss of the lesson's assumptions when the example is restated, not that an illustrative number is inherently objectionable. Keep the existing reveals and phone-to-facility sequence. Final replacement spans must be located across every affected animation frame before a build.

2. **Optional: improve the facility picture around 1:10–1:14.** Its large cooling towers and pylons read as a power station beside server racks. That could blur the distinction between a data center and its electricity supply during “the scale varies by facility.” It does not explicitly claim that a data center generates its own power, so this is visual clarity rather than a demonstrated factual error. A more recognizable data-center exterior would support the line. Prefer a small treatment of this scene; preserve the surrounding city comparison and request/response graphic.

3. **Preserve the successful board treatment.** The neighbors board's active cards are complete and readable in inspected frames; the main title is partially cropped during the dive, but the active card is intact. Meeting the Demand reads comfortably at full view. Longest manifest board run is 20.0 seconds, with breaks already provided. No reason to add more cuts or automatic pauses.

4. **Do not turn older flags into automatic defects.** The GPU label at 0:48 actually reads `2×10^15 OPS/SEC`, not `2×10^14` as the old review says. It is an unspoken illustrative throughput label on an unspecified chip; this review does not establish it as false. Removing the unnecessary precision would be optional, not grounds for a reroll. Existing stroke widths predate the fixed 4 px rule and are explicitly grandfathered by the current Edit Spec. Apply today's width only if rebuilding those spans.

5. **Listen to the existing edits before declaring a full pass.** The retained record identifies cuts at 2:22.9 and 2:51.4 and a different-roll close at 3:33.8. The old review explicitly left listening undone. Transcript continuity and quiet splice measurements do not establish voice continuity or natural cadence.

## Teaching coverage, in lesson order

These are transcript assessments, not claims about words heard in this session.

| Essential point | Assessment | Evidence |
|---|---|---|
| A chat answer requires physical computation | TAUGHT | 0:00–0:09, question/send/answer and computers doing math |
| Assumed trillion weights, two calculations each, 1,000 tokens ≈750 words, two quadrillion, 15 zeros | RICH | 0:09–0:27, full numerical example; “piece of text” compresses “token,” whose count is stated immediately afterward |
| Compute definition and millions of simultaneous users | RICH | 0:28–0:41, explicitly explains why more data centers are needed |
| Warehouse, specialized GPUs, continuous operation | TAUGHT | 0:42–0:50 |
| Racks, human for scale, football fields/city comparison and facility variability | RICH | 0:50–1:14, concrete visual description and spoken qualification |
| Data center answers ChatGPT; someone pays; community bridge | TAUGHT | 1:14–1:27 |
| Electricity: 4.4% in 2023, Berkeley Lab 6.7–12% projection for 2028, household bills in some places | RICH | 1:33–1:49, numbers, attribution, dates, and local qualifier preserved |
| Water: hot chips, evaporation, about a million gallons on a hot day at a large facility, alternatives | RICH | 1:49–2:01, causal explanation and reuse/recycling stated |
| Noise: continuous fans, lost sleep, lawsuits in some towns | TAUGHT | 2:01–2:10 |
| Many construction jobs versus 100–200 permanent workers; supermarket comparison | RICH | 2:10–2:23, “may need” preserved |
| Three responses: power supply, water reuse, efficient chips | RICH | 2:23–2:45, each explained |
| Supply meets demand; efficiency reduces resources per task | TAUGHT | 2:45–2:51, distinction explicit |
| Efficiency does not guarantee falling total demand | RICH | 2:51–3:02, growth can outweigh savings |
| One request versus millions, other technologies have footprints | TAUGHT | 3:02–3:15 |
| Company dollars, grid watts, neighborhood water and quiet | RICH | 3:15–3:25 |
| Understanding rather than guilt | TAUGHT | 3:25–3:33 |
| Two exact closing lines | MET in transcript | 3:33.96 “Every AI chat costs something real.” / 3:36.72 “Now you know what's behind the magic.” |

**Arc:** The relationships are spoken, including the important distinction between supplying more power and reducing resources per task. There is no material repetition requiring a cut. No narration grafts, deletions, extra pauses, or reroll proposed. The two display clarifications above preserve the existing narration.

## Source QA

No material contradiction between the transcript and current lesson was found. The calculation follows the stated approximation: 10^12 × 2 × 1,000 = 2×10^15. Keep its assumptions visible.

The electricity percentages match the dated [Berkeley Lab 2024 report](https://eta-publications.lbl.gov/publications/2024-lbnl-data-center-energy-usage-report). A [newer projection](https://datacenters.lbl.gov/index.php/modeling-forecasting) is available, but that does not make an explicitly dated 2028 projection incorrect. Updating the forecast would be a separate lesson/materials decision, not a video-only correction.

The [Virginia JLARC study](https://jlarc.virginia.gov/landing-2024-data-centers-in-virginia.asp) supports the construction-versus-operations distinction, variable cooling demands, and local noise concerns. Its cited example has roughly 50 workers for a 250,000-square-foot facility; it does not verify this lesson's particular 100–200 range. That range is qualified as a possibility, not a universal typical count. The precise million-gallon hot-day example, supermarket comparison, lawsuits, and already-realized household bill effect were not independently established in this limited source check. Do not present this as a comprehensive factual audit.

## Board and camera recommendation

This is a preservation plan for the existing edit, not authorization for a build. Times are on the current output timeline.

| Board | Highlight sequence | Camera | On screen / breaks | Recommendation |
|---|---|---|---|---|
| Inside a Data Center | Unmarked | Full photograph | 0:50.30–1:03.37; 13.07 s | Preserve; the person and racks communicate scale |
| What a Data Center Means for Its Neighbors | Full unmarked opening; Electricity purple at ~1:33.18, Water blue ~1:49.76, Noise teal ~2:01.68, Permanent Jobs amber ~2:10.68 | Full opening, then complete active-card dives/pans | 1:27.23–1:45.60; 1:48.77–2:05.90; 2:09.67–2:22.90. Runs 18.37, 17.13, 13.23 s | Preserve cable cutaway 1:45.60–1:48.77 and meeting-room cutaway 2:05.90–2:09.67 |
| Meeting the Demand | Full unmarked opening; More Power purple ~2:28.30, Better Cooling blue ~2:33.48, More Efficient Chips teal ~2:39.90, purple takeaway ~2:45.98 | Compact, full view | 2:22.90–2:42.90 and 2:44.97–2:51.40; runs 20.0 and 6.43 s | Preserve pylon/chip break 2:42.90–2:44.97 |
| Every AI chat costs something real. / Now you know what's behind the magic. | No added ring | Canonical close; existing hold/push/settle | 3:33.80–3:43.13 | Final frame checked; continuous motion and graft listening remain unverified |

## Supporting scenes to retain

Recommendations are based on sampled stills plus the transcript; motion/reveal timing has not been signed off.

- 0:00–0:50: phone, arithmetic build, compute, world demand, construction and GPU. Preserve the worked-example graphics with the caption clarification.
- 1:03–1:27: city comparison, request/response, and facility versus neighborhood. Only the brief power-station-looking scene is an optional replacement.
- 1:45.60–1:48.77: cable drawing under household bills; 2:05.90–2:09.67: community meeting room under neighborhood complaints; 2:42.90–2:44.97: pylon/chip under efficiency. These breaks have teaching purposes.
- 2:51.40–3:02.23: indicator and server aisle support the efficiency/demand distinction. No invented chart needs restoring.
- 3:02.23–3:15.90: single request, facility scale, streaming and cars. Clarify the request caption while keeping the sequence.
- 3:15.90–3:25.83: chat/servers then facility/homes supports who bears each cost.
- 3:25.83–3:33.80: Send and check-mark phone support the no-guilt/understanding conclusion.

## Remaining checks and scope

Only this evaluation and evidence artifacts were created. Course, lesson, MP4, tracker, Git release state, and deployment were not changed. The raw `Prompts/data-centers-1.mp4` through `-4.mp4` and old candidates are absent locally; a repair would need recovered pristine sources or disclosed use of the encoded finished file.

Remaining for full sign-off: end-to-end audiovisual viewing, material-word confirmation, the three edit joins above, full animation states and scene boundaries, and close motion. No new pause plan is justified without listening evidence. If the caption pass is requested, establish exact affected frames and preserve audio, duration, and unaffected visuals.
