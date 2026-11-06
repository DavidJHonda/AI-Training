# Learn with AI — updated narration donors

November 6, 2026. **Select `Prompts/learn-reroll-2.mp4`, output-list sentence only, as the donor for original `Prompts/learn-with-ai-3.mp4`.** It supplies all missing output types. Keep the original base's exact takeaway instead of the donor's paraphrase. A 24.4-second audio preview demonstrates the proposed sequence and has been freshly transcribed; direct listening and voice/cadence approval remain outstanding.

This reviews scoped donor passages, not three complete lesson replacements. No full video was built, installed, committed, or published. The original evaluation remains historical: its missing-donor condition has now changed, but a fully verified REPAIR verdict requires auditioned joins under the narration-review rules.

## Evidence and limits

Read the full fresh timestamped transcripts of all three uploaded files against the prepared donor Markdown, its four required sentences, and the current lesson. Verified unchanged SHA-256 of the base, lesson Markdown, and canonical input/output board against the prep manifest. Captured hashes, sizes, runtime, frame count, and FPS in `sources.json`. Inspected all three contact sheets, sampled every four seconds with sequential decode. Measured quiet intervals in base and selected donor using ffmpeg silencedetect at -35 dB, minimum 80 ms. Created the audition preview and transcribed its encoded audio afresh.

**Not performed:** direct listening, end-to-end audiovisual playback, voice/cadence matching, full motion inspection, or finished-video QA. ASR numerical warnings did not prevent complete transcription. ASR is not proof of pronunciation or a clean audio seam. No uncertain ASR phrase is treated as a confirmed speech defect.

## Comparison

| Teaching point | learn-reroll-1 — 0:36.07 | learn-reroll-2 — 0:43.60 | learn-reroll-3 — 0:58.07 | Selection |
|---|---|---|---|---|
| Source-grounded class study | TAUGHT, 0:00–0:14: “primary study tool… entirely grounded… so you do not have to rely on outside information.” Stronger than source. | TAUGHT, 0:00–0:12: “primary study tool… securely grounded… sources your teacher actually provided.” “Securely” is an unnecessary addition. | TAUGHT with unsupported assurance, 0:00–0:21: “ensure the information you review is accurate to your specific course.” | Keep existing base; no donor intro needed. |
| Board introduction | TAUGHT meaning, 0:14.60–0:15.72: “Here's how the process works.” | TAUGHT meaning, 0:13.22–0:15.76: “This graphic shows exactly how Gemini Notebook works.” | TAUGHT meaning, 0:21.94–0:24.32: “This graphic illustrates the Gemini Notebook workflow.” | None matches the requested introductory sentence exactly; no need to import it for the minimal repair. |
| Upload types | THIN enumeration, 0:16.44–0:22.00: “notes, PDFs, slides, images, articles, and YouTube videos”; websites omitted. | TAUGHT, 0:16.80–0:24.92: “personal notes, PDFs, presentation slides, images, websites, articles, or YouTube videos.” All required types included. | THIN enumeration, 0:24.32–0:30.42: “class notes, PDFs, slide decks, websites, and YouTube videos”; images/articles omitted. | 2 is the best full-board alternate. Minimal repair retains the existing base list. |
| Complete study outputs | Provisionally TAUGHT, 0:22.54–0:28.62: “quizzes, flashcards, study guides, audio video overviews, and mind maps.” ASR does not resolve whether “and” is spoken between audio/video. | **TAUGHT**, 0:25.86–0:34.68: “From those inputs, you get back custom quizzes, flashcards, study guides, audio and video overviews, mind maps, and more.” Both overview types explicit. | **THIN**, 0:31.10–0:37.98: “practice quizzes, flashcards, study guides, audio overviews, and mind maps.” Video overviews missing. | **TAKE 2**, whole sentence under canonical course board. |
| Exact materials-to-tools takeaway | TAUGHT meaning, exact requirement MISSED, 0:28.62–0:32.64: “Turn class materials directly into study tools you need.” | TAUGHT meaning, exact requirement MISSED, 0:35.60–0:40.12: “You turn your existing class materials directly into the specific study tools you need.” | TAUGHT meaning, exact requirement MISSED, 0:48.50–0:54.36: “…turn your raw class materials into the exact study tools you need to prepare for your exams.” | Keep original base **2:35.00–2:37.50**, which has the exact line. |
| Added claims | Outside-information clause above; not selected. | No accuracy/test-result guarantee in selected output sentence. | “Ensure… accurate” plus 0:38.72–0:47.90 “highly accurate… tailored to your curriculum”; not selected. | 2 is cleanest for the needed passage. |

None of the raw donors is a verbatim pass on all four demanded sentences. That is not a reason to keep generating when the existing base supplies the required exact takeaway and the selected donor supplies the missing teaching. A source may be useful for one complete beat without being a usable standalone lesson.

**Donor verdicts:** 1 = backup pending ambiguous audio wording; 2 = selected complete output beat, semantically adequate despite paraphrase; 3 = reject for this repair because it still omits video overviews. Full repair feasibility remains provisional until listening.

## Proposed smallest repair

Keep original base through the upload explanation. Replace **2:25.00–2:34.90** with roll 2 **0:25.80–0:35.15**. These are measured quiet edit boundaries, not just ASR segment endpoints. The donor's spoken sentence falls approximately 0:25.86–0:34.68 in ASR; retain lead/trail silence rather than slicing at those word estimates.

Return to base **2:34.90** for the exact takeaway. Preserve “Turn your class materials into the study tools you need.” Cut the previously flagged hallucination/test-relevance guarantee at quiet boundaries **2:37.90–2:48.75**, then resume the base four-moves introduction. All source files are hash-pinned in `sources.json` and the earlier prep manifest.

The source-to-source transition in words:

> You can provide your notes, PDFs, slide decks, images, websites, and even YouTube videos. [BASE]
>
> From those inputs, you get back custom quizzes, flashcards, study guides, audio and video overviews, mind maps, and more. [DONOR 2]
>
> Turn your class materials into the study tools you need. [BASE]
>
> This infographic lays out four specific operational moves required to use Gemini Notebook effectively. [BASE, guarantee removed]

The bridge “From those inputs” refers clearly to the preceding upload list. One whole-sentence donor graft, no word-level manufacturing, no repeated introduction, and no new factual claim. The separate proposed cut to the overpromising memory summary later in the base remains in the edit handoff; it is outside this preview.

## Audition preview

File: `output-splice-preview.wav`, 24.400 seconds, 48 kHz mono PCM. This is a listening sample, not a video candidate. `preview-manifest.json` records exact legs and output positions; `build_preview.py` reproduces it.

| Preview position | Source |
|---|---|
| 0:00–0:06.20 | Base 2:18.80–2:25.00: preceding upload list |
| 0:06.20–0:15.55 | Donor 2 0:25.80–0:35.15: complete output list |
| 0:15.55–0:18.55 | Base 2:34.90–2:37.90: exact takeaway |
| 0:18.55–0:24.40 | Base 2:48.75–2:54.60: next-section introduction |

Applied 8 ms edge fades inside measured quiet portions, channel/rate conversion only, no gain adjustment, no synthetic speech, and no added silence. Approximate combined quiet gaps from threshold detection: 0.80 seconds before donor, 0.57 before base takeaway, 0.68 before four-moves introduction. These are existing retained silence, not an approved new-pause prescription. Threshold detection cannot certify perceived pacing.

Fresh preview ASR reproduces all six output categories and the exact takeaway, and excludes the guarantee. Listen especially across preview ~0:06, ~0:15.5, and ~0:18.5 for voice match, volume, breath/cadence, clicks, or a conspicuous tone shift before adopting these seams.

## Visual handoff

Use **audio only** from donor 2. Its sampled generated board has cropped/malformed text, blank upload panels, and Notebook highlighting; none is needed in the finished video. Its supporting desk imagery is also unnecessary for this graft. Roll 1's anchor/notes sketch and roll 3's student/materials sketch are possible supplementary visuals, but not selected or motion-approved here. Do not reuse roll 3's “100%” study-aid image as a result promise.

| Board | Highlighting | Camera | On screen / breaks | Reason |
|---|---|---|---|---|
| How Gemini Notebook Works | Keep Upload through the base input list; switch to whole You Get card as donor introduces outputs; then takeaway banner on the original base line | Full canonical board, unmarked introduction, compact full view; one 4 px outline at 720p | Revised topic duration approximately 23.9 seconds from base introduction at 2:13.42 through takeaway before cutting the guarantee; retain planned ~4-second materials drawing during upload list if motion inspection supports it | This gives about 20 seconds board exposure split by the drawing; actual output timeline and visual cut frames remain to be finalized. No donor board recreation ships. |

Other board framing, useful illustrations, later cut, and standard close remain as proposed in the original evaluation and handoff. No new pause or generated illustration is added by this donor selection.

## Next step

Audition this concrete preview, then complete the production edit with donor 2 if the voice/joins work. No further narration generation is indicated by the current transcript evidence. Do not label the assembled lesson KEEP until the actual encoded candidate has been reviewed and the remaining production checks completed.
