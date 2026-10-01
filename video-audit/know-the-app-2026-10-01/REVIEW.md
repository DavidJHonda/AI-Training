# Know the App: three raw-roll evaluation

Grounding: `index.html` `ChoosingModelSection`, `lessons/your-choices.md`, `gemini-notebook/know-the-app/PROMPT.txt`, and the three current board JPGs. Complete timestamped ASR transcripts are in `transcripts/`. Raw-roll visuals were sampled in contact sheets and full-resolution frames; no whole-file listening pass was performed. The tracker and public site were not checked.

## Decision

**REROLL.** Roll 3 is the strongest teaching spine, but none meets the prompt's verbatim audio requirements or reads all three boards' complete examples. Rolls 1 and 2 do not supply the missing full beats as usable donors. A visual edit cannot fill missing narration. Preserve all three raw files.

The installed `course-assets/your-choices/your-choices.mp4` was also checked as a fourth donor. Its transcript teaches the previous four-choice lesson with a music-app opening, different boards, and a different closing line. It can supply only general ideas about defaults, model strength, and source-based research; it cannot supply the new phone-camera analogy, English-exam example, two-editor project constraint, or the complete physics-college request. Its installed narration also says choosing settings “ensures you get the right result” (0:35–0:40), which should not be carried into the new lesson. See `video-audit/your-choices-evaluation-2026-09-30/REVIEW.md` for the installed-file audit.

| Roll | Length | Teaching verdict | Main evidence |
|---|---:|---|---|
| `Prompts/know-the-app-1.mp4` | 3:00 | REROLL | Best camera opening (0:00–0:22) and a clear model/Thinking distinction. The model takeaway changes to “Select the larger model” (1:17), contrary to starting with the default. Group-project constraints and college comparison are compressed. No required verbatim opening or close. |
| `Prompts/know-the-app-2.mp4` | 2:47 | REROLL | Says the correct default-model takeaway (0:49–0:54), but omits the group-project example, both full college examples, and much of the camera analogy. Adds “raw horsepower” and an unsupported guarantee that more time lets AI “check its own work.” Opening visual is blank at 0:00. Closing is prefaced by an extra sentence. |
| `Prompts/know-the-app-3.mp4` | 4:12 | REROLL | Most complete paraphrase of the camera, model, Thinking, and Research arc. Still omits the English exam's summer-book and first-exam context, the group project's two editors, the college names and research opportunities, and verbatim required lines. Adds technical diction and invented “dials”/interface diagrams. |

## Teaching point comparison

| Current lesson beat | Roll 1 | Roll 2 | Roll 3 | Best available |
|---|---|---|---|---|
| Phone-camera flash/zoom and ordinary default | RICH 0:00–0:25 | THIN 0:00–0:06 | TAUGHT 0:00–0:27 | 1 |
| Conditional access, three choices, leave defaults alone | THIN 0:25–0:42: “you often have three advanced options” | THIN 0:08–0:18: “you have three choices” | THIN 0:28–0:42: “you have three primary dials” | 3 for continuity; none has required conditional wording |
| LLM as engine; model changes which LLM; capabilities differ | TAUGHT 0:43–0:59 | TAUGHT 0:19–0:37 | TAUGHT 0:43–0:59 | 3 |
| Model board: both descriptions, complete movie/business prompts, default-first takeaway | THIN 1:00–1:19: business details given, then “Select the larger model” | THIN 0:38–0:54: examples reduced to “suggesting a movie” and “planning a business” | TAUGHT 1:02–1:37: examples close, but adds “break even” | 3 |
| Model choice versus time spent | TAUGHT 1:19–1:27 | TAUGHT 1:08–1:16 | TAUGHT 1:37–1:44 | 2 or 3 |
| English-exam planning analogy and AI caveat | THIN 1:28–1:44: loses first exam/summer book; adds internal verification claim | THIN 1:01–1:22: loses first exam/summer book | THIN 1:44–2:05: loses first exam/summer book and says “mechanically” | 2 |
| Thinking board: both descriptions, checklist, four people/one week/different schedules/two editors, takeaway | THIN 1:45–2:03: omits week and two editors | THIN 1:25–1:41: omits group-project example | THIN 2:08–2:45: omits only two editors and does not explicitly state checking the answer | 3 |
| Cheeseburger versus first-house information needs; regular chat can search | TAUGHT 2:08–2:31 | TAUGHT 1:49–2:09 | TAUGHT 2:49–3:27, but “basic knowledge retrieval” is needlessly technical | 1 |
| Research board: both descriptions, full Dallas and physics-college prompts, sources takeaway | THIN 2:32–2:49: omits A&M driving time, research opportunities, admissions nuance and sources request | THIN 2:12–2:27: both examples reduced to generic labels | THIN 3:21–3:56: omits Texas A&M and UT Austin names, research opportunities, and full example wording | 3 |
| Two-line close in statement cadence and nothing after | THIN 2:50–2:57: first line paraphrased | THIN 2:28–2:43: prefaced by extra rule; first line embedded | THIN 4:02–4:09: first line prefaced and paraphrased | none |

The source lesson and upload Markdown agree on the instructional content. No Source QA correction is needed.

## Preparation revision after this review

`lessons/your-choices.md` now expresses board cards as natural spoken sentences while retaining their printed content and all six full example requests. `gemini-notebook/know-the-app/PROMPT.txt` is 494 words: it retains the eight required verbatim passages, quotes the four long requests that repeatedly collapsed, names the English-exam and research details, and rejects the technical diction and invented controls seen in the new rolls. The registry points to `Prompts/know-the-app-4.mp4`. The upload bundle was resynced and passed `sync_gemini_notebook.py --lesson know-the-app --check`. This is preparation for a new roll; no video was generated or shipped.

## Hard requirements and errors

The generation prompt requires eight verbatim passages. Across the three ASR transcripts, roll 2 appears to have the exact model-versus-Thinking distinction (1:09–1:16) and the “AI isn’t thinking the way you do...” sentence (1:16–1:22). All three have the final “Use them when the work demands more.” line. None has the exact opening qualification, the exact Research qualification, or the standalone “Model. Thinking. Research.” line. These are material failures even where a paraphrase is broadly accurate. ASR was used for this comparison; any prospective donor would still need audio audition.

Roll 1's “Select the larger model” (1:17) reverses the board's default-first guidance. Roll 2 states “you have three choices” (0:08) without the lesson's “may,” implying availability. Roll 3 does the same with “you have three primary dials” (0:31) and “you now control” (4:01). Roll 3's “break even” (1:24–1:28) is an unnecessary addition to the business example. Roll 1's “verify its logic” (1:38–1:43) and roll 2's “check its own work” (1:44–1:49) suggest more reliability than the lesson promises.

## Visual observations and provisional edit plan

The raw boards show Notebook's yellow word highlighting, and roll 3 zooms so far into the boards that text and parts of adjacent cards are cropped (for example, model at 1:24 and Research at 3:36–3:48). Roll 3 also contains extra technical interface graphics (0:36 and 0:48) and a chart-summary sentence before the closing card (3:57–4:01). Roll 1's drawn phone and camera scenes (0:00–0:22) support the lesson and are worth retaining as a donor if a future edit uses mixed rolls. The sampled views do not establish an end-to-end visual or audio ship check.

| Board | Provisional highlighting | Camera | Timing / visual treatment |
|---|---|---|---|
| Which Model? | Full, unmarked opening; then one whole-card ring for Everyday Model and More Capable Model as each is spoken; unmarked takeaway | Full board throughout if text reads at 720p; otherwise complete-card zoom without cropping either card | Replace Notebook board at its visual cut with exact `course-assets/your-choices/your-choices-choose-tool.jpg`; start before the first description and remain through the takeaway. |
| How Much Thinking? | Same sequence for Less Thinking, then More Thinking | Full board if legible; otherwise complete-card zoom | Use exact `your-choices-thinking.jpg`; keep the complete checklist and four-person example visible while spoken. |
| How Much Research? | Same sequence for Regular Chat, then Deep Research | Full board if legible; otherwise complete-card zoom | Use exact `your-choices-research.jpg`; preserve both full college examples and return to full view for the takeaway. |

This table is provisional until a new narration roll establishes board onset and duration. The prompt's unhighlighted-board instruction governs generation; the course edit spec's rings and exact asset replacement govern a later production edit. No production build or shipping is authorized by this evaluation.

## Reroll direction

Keep the roll-3 breadth and the roll-1 camera scene. Ask for plain conversational wording rather than “dials,” “mechanically,” “processing time,” or invented controls. The new audio must read every board description, full example, and takeaway, with the exact eight passages already specified in `gemini-notebook/know-the-app/PROMPT.txt`. Emphasize the missing group constraint (only two people can edit video) and the full Texas A&M/UT Austin comparison, including undergraduate research opportunities and source display. The close should speak exactly the two lines with no preface or added recap. Generated board zoom/highlights can be replaced during editing; complete spoken teaching cannot.
