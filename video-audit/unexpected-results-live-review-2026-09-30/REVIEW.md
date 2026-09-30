# Unexpected Results — live evaluation, September 30, 2026

**Recommendation: retain this version and make two small label corrections.** The narration covers the current lesson, the rat story explains the mechanism rather than merely naming it, and the four examples have useful visual breaks. Nothing found in the transcript warrants a reroll or a narration cut.

**Scope and limitation:** verified public file, complete transcript, sequential frame samples across the whole video, and selected full-resolution frames. This is not an end-to-end listening or continuous-motion sign-off. Formal KEEP / REPAIR / REROLL narration verdict is withheld pending those checks. No video, lesson, board, tracker, or deployment changes were made.

## Verified live file

- [Public video](https://besmarterthanthetool.com/course-assets/unexpected-results/unexpected-results.mp4?v=20260924ship1), linked by the public page as `unexpected`, displayed runtime `4 min`.
- HTTP 200, `video/mp4`, 30,922,098 bytes. Runtime 239.067 seconds (3:59.07), 1280×720, 30 fps, 7,172 frames in the matched build record.
- Public bytes, local canonical video, and v2 manifest `render_sha256` all match: `1aadfdf5f509be580e4ceb70789a52da017474a1c9cda00b2be6dc0b12a5730a`.
- Public `UnexpectedResultsSection` matches the current local section exactly. Read the current page, upload Markdown, both canonical JPGs, Narration Review, and Edit Spec.
- Shipping commit: `c8d429f4`, September 24 v2. The earlier v2 review still says “review only”; it predates shipping and is not the current release status.
- Transcript evidence: fresh `unexpected-results/transcript.txt`, read in full and matching the retained v2 transcript's narration and timestamps. The older transcript is tied to this exact file by the matching build hash as well. Timestamps below are transcript/manifest times, not auditioned edit boundaries. Fresh ASR is not listening verification.
- Fresh visual evidence: `frames/sheet-00.jpg` through `sheet-04.jpg`, sampled every four seconds; `detail-*.png` includes full-resolution findings and the literal final frame. Public identity is saved in `identity.json` and the HTTP/hash records.
- Fresh `grade_bundle.py` completed: 3:59.07 sequential decode, 133 detected cuts, 64 transcript segments. Fresh and retained transcript text/timestamps are identical after their file-name headings. Automated cuts include camera motion and are not all editorial splices.

## Findings and proposed narrow repair

1. **0:32.40–0:40.17 — correct the ledger heading.** At 0:36 the ledger visibly reads “GOVERNMENT LEDGER – Q4 RESULTS” and **“12/04/2023”**, during a story explicitly set in 1902. The old manifest misread the date as 12/09/2023; the fresh full-resolution frame is the evidence. Keep the rising bars and green check, which communicate apparent success. Change the header to “Rat tails collected” and remove the date, or use “Hanoi, 1902.” There is no need to invent a precise historical day or replace the whole scene. Evidence: `detail-036.000.png`.

2. **Approximately 0:47–0:53.20 — qualify the survival label.** The useful reproduction diagram says “Full lifespan / Survives tail loss intact.” That is more absolute than the lesson and narration's “can live a relatively full rat life.” Change just this box to **“Can survive / Can keep breeding.”** Preserve the parent-to-offspring sequence and “New Tails Born!”; those explain why keeping the rats alive sustains the bounty supply. This is a wording correction, not a claim that the diagram's reproduction mechanism is wrong. Evidence: `detail-052.000.png`. Confirm the box's exact first visible frame before editing.

These are visual repairs; preserve audio, duration, scene order, and useful animation. Neither defect requires new narration. No additional pauses proposed without listening evidence.

Optional polish only: the late forecast diagram uses “AI Outcome State Space” and “Outside Modeled Distribution” around 3:23–3:33. Simpler labels could help sixteen-year-olds, but the narration already explains the idea clearly. The crossed-out forecast document near 0:07–0:14 also has small synthetic text; treat it as an illustrated prop, not a source students must read. Neither justifies replacing the scene wholesale.

## Teaching coverage in lesson order

Ratings describe transcript coverage, not an audio-quality pass.

| Essential point | Assessment | Evidence |
|---|---|---|
| Confident AI predictions can miss major results | TAUGHT | 0:00–0:14, both camps and unpredicted outcomes |
| Hanoi, 1902; new sewers and too many rats | TAUGHT | 0:14–0:23, setting and problem |
| Payment for tails appears successful | RICH | 0:23–0:40, bounty, thousands of tails, apparent success measured by tail count |
| Tailless rats reveal what went wrong | RICH | 0:40–1:01, survival, babies, clipping tails and releasing rats |
| Dead rat pays once / live rat pays forever | TAUGHT | 1:01–1:05; reproduction explained immediately beforehand, so the maxim has a mechanism |
| Rat farms and worse outcome | TAUGHT | 1:05–1:16, farms, program stopped, more rats |
| Successful payment system versus failed real goal | RICH | 1:16–1:28, explicitly contrasts paying for tails with reducing rats |
| Bridge from rats to other plans | TAUGHT | 1:28–1:35, same pattern and four examples |
| Text messaging | RICH | 1:35–1:56, short-message service, voice-oriented phones, users adopting texting |
| GPS | RICH | 1:56–2:11, military purpose, civilian applications, Google Maps |
| Cane toads | TAUGHT | 2:11–2:20, beetle-control goal, poor pest control, poisoned wildlife and spread |
| Katy Freeway | TAUGHT | 2:20–2:32, $2.8 billion, 2014, 51% longer than three years earlier, explicitly one rush-hour trip |
| Two better / two worse; outcomes differ from plans | TAUGHT | 2:32–2:40, both sides of uncertainty |
| Why easier roads attract more driving | RICH addition | 2:40–2:58, newly worthwhile trips fill space; included in upload Markdown |
| Houston qualification | TAUGHT addition | 2:58–3:03, not the whole explanation, other changes over those years |
| Why adding lanes is not a guaranteed cure | TAUGHT | 3:03–3:14, people's response to the changed system |
| Apply history to AI; biggest result may be unimagined | TAUGHT | 3:14–3:32, explicit return to AI, good or bad |
| Curiosity rather than fear | TAUGHT | 3:32–3:38 |
| Recognize uncertainty, observe behavior, build durable skills | TAUGHT | 3:38–3:49, all three actions spoken |
| Both exact closing lines | MET in transcript | 3:49–3:54, “Some of the biggest results are the ones nobody predicted.” then “That's the best reason to stay curious.” |

The arc works without the pictures: surprising rat outcome → incentive mechanism → beneficial and harmful surprises → people's response to a change → humility and curiosity about AI. The road explanation earns its extra time because it explains rather than merely repeats the freeway statistic. The page's invitation to guess what happened is compressed into a direct explanation; no essential understanding is lost.

ASR renders “worriers” as “warriors,” “Katy” as “Katie,” and the hunters line as “The renters.” These are transcription uncertainties, not established spoken defects. The retained build notes specifically record David accepting the pronunciation of “worriers.” Do not reopen that as a known error based on ASR alone. Listen to the hunters line at approximately 0:25 if doing a future audio pass.

## Source QA and additions

The historical mechanism is supported by historian Michael Vann's account of his archival research: tail payments, tailless rats, rat farms, and trafficking. His interview does not supply a measured before/after citywide rat census; the lesson's “more rats” remains a qualitative account, not a checked numerical population result. [Vann interview](https://journals.gmu.edu/index.php/whc/article/download/3804/2200?inline=1).

The SMS explanation usefully distinguishes intended short messaging from unexpected mass adoption; texting itself was designed, not an accidental invention. The standards body's account supports that distinction. Keep the richer spoken explanation. [ETSI, July 2021, page 17](https://www.etsi.org/images/files/Magazine/ETSI_Enjoy_MAG_2021_N03_July.pdf).

Cane-toad purpose, failure and poisoning/spread are supported by the Australian government. [DCCEEW](https://www.dcceew.gov.au/environment/invasive-species/feral-animals-australia/cane-toads). Civil GPS applications and the policy change enabling much more accurate civilian use are documented by [GPS.gov](https://www.gps.gov/gps-modernization).

The 51% claim matches the current lesson. Transportation for America's report attributes that specific comparison to Houston Tomorrow's analysis of downtown-to-Pin Oak travel in 2011 and 2014. The original Houston Tomorrow page was unavailable during this check; the statistic was corroborated through that report, not independently recalculated. [The Congestion Con, Katy case study](https://t4america.org/wp-content/uploads/2020/03/Congestion-Report-2020-FINAL.pdf). Preserve “one rush-hour trip,” both years, and the later qualification about other causes. The final chart state is correctly indexed at 100 and 151; its temporary 95 during the reveal is not evidence of a wrong final statistic.

The examples establish outcomes beyond the original plan. They do not prove that literally nobody foresaw any adverse effect. Keep that distinction in future factual expansions; no broader source rewrite or narration repair is proposed from this bounded review.

## Board and camera plan

The proposed repair touches only the two supporting-scene labels above. Board treatment is recorded here for completeness and should be preserved. Timings are the matched build's actual timeline, confirmed by current samples.

| Board | Highlighting sequence | Camera | On screen / breaks | Recommendation |
|---|---|---|---|---|
| The Biggest Results Were Never the Plan | Whole Text Messaging card (purple), GPS (blue), Cane Toads (teal), Wider Highways (amber); both top cards at “two better,” both bottom cards at “two worse,” title at takeaway | Full unmarked opening 1:30.90–1:35.10; dense board, zoom to complete active card; wide for comparison | Topic block 1:30.90–2:39.60. Breaks: SMS 1:42.87–1:52.97; map 2:00.97–2:05.47; cane-toad map 2:14.07–2:18.67; 51% chart 2:22.67–2:31.37. About 40.8 seconds of actual board exposure; longest uninterrupted run 11.97 seconds. | Preserve. Full-view text is too small for sustained reading; complete-card zooms are justified. Multiple rings are justified by the explicit two-versus-two comparison. |
| Some of the biggest results are the ones nobody predicted. / That's the best reason to stay curious. | Unmarked canonical close | Preserve existing hold, push and settle | 3:48.83–3:59.07, literal final frame correct | Final frame inspected. Exact continuous motion and listening are not signed off here. |

The older delivered rings thicken during the camera dive. Section 5 of the current Edit Spec expressly grandfathers earlier shipped stroke treatment. Do not rebuild this otherwise useful board solely for that reason. If the board is rebuilt later, use fixed 4 px delivery strokes.

Fresh `board-spans.py` measurement agrees with the approximately 12-second maximum and finds 41.5 seconds of board exposure at half-second sampling resolution. Use the matched manifest's 40.8 seconds for exact timeline accounting. The detector falsely identifies the SMS diagram at 1:50–1:52.5 as the close (only 37 feature inliers); the current frames clearly show SMS there, so that interval is excluded from the close assessment.

## Supporting visuals to retain

Retention recommendations are based on sampled sequences and transcript, not continuous motion viewing.

- 0:00–0:30: contrasting heads, marked-up predictions, sewer and bounty sequence establish the question and story.
- 0:30–0:53: tails/coins scale, ledger, tailless rats and offspring explain apparent success and the hidden mechanism; correct only the two labels identified above.
- 0:53–1:30.90: capture/clip/pay/release sequence, dead/live comparison, rat farm, tail mountain and crowded street, payment loop, and payment→behavior→goal diagram complete the causal explanation. “Infinite Bounties” is figurative in the context of breeding already explained; it is not a claim that severed tails regenerate.
- 1:42.87–1:52.97: SMS diagram supports the shift from voice dominance to texting.
- 2:00.97–2:05.47: map/zoom imagery makes civilian navigation concrete.
- 2:14.07–2:18.67: cane-toad map supports spread.
- 2:22.67–2:31.37: indexed travel-time chart makes the 51% comparison legible.
- 2:39.60–3:13.77: road scenes explain additional driving. The 2:58.53–3:04.10 held frame is about 5.6 seconds under the important qualification; it is not an unexplained long course-board hold.
- 3:13.77–3:48.83: heads/gears, outcome fan, feedback loop, magnifier and behavior branches return to AI and active observation.

No Notebook stock photograph or corner mark was apparent in the sampled frames. This does not certify every frame. The matching historical manifest reports zero declined corner-cleanup frames; its historical transition check had one inspected camera-move flag, not an established stale-frame defect.

## Remaining verification and repair feasibility

- No material narration change proposed; no donor audition claimed.
- Listen across the existing SMS/GPS grafts near 1:35.1, 1:56.4, 2:01.0 and 2:10.8, and the road graft near 2:54.8 and 2:58.1, if conducting a full sign-off. ASR does not establish voice continuity or clean seams.
- Raw `Prompts/unexpected-results-1.mp4`, `-2.mp4` and the old v2 candidate are absent locally. The exact finished file is available. Any new repair must disclose using that encoded file unless pristine sources are restored; do not rerun the old builder against a mutable canonical-video donor path.
- Before a label repair: identify complete label visibility/reveal spans, preview the correction, preserve underlying movement, and validate the resulting encoded spans and boundaries. No new audio edit, pause, lesson change or reroll is needed for the proposed scope.
- Continuous full-file viewing/listening and a fresh splice/animation sign-off remain unperformed. Video Tracker was not accessed; no tracker status inferred or row drafted.
- The optional exhaustive ring-width scan was stopped before completion; no numerical width pass is claimed. Full-resolution frames show the older zoom-dependent treatment, and the current spec grandfathers it, so a fresh numerical stroke measurement is not needed to decide the proposed label-only scope.
