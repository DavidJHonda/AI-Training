# Your Home Base — current-spec evaluation, 2026-09-29

**Recommendation: retain the narration and existing edit; make two targeted visual-label corrections. No reroll or broad visual rebuild is justified by this review.** Narration is a **provisional KEEP based on the complete transcript**. This is an editorial and measured production evaluation, not a completed end-to-end audiovisual certification: audio audition and real-time playback were unavailable.

## Scope and sources

Evaluation only. No video, course asset, lesson, prompt, tracker, or release reference was changed. The review uses the September 29 versions of `scripts/video/README.md`, `EDIT-SPEC.md`, and `NARRATION-REVIEW.md`.

- Current local course reference: `index.html:1113`, lesson ID `modelselection`, `course-assets/your-home-base/your-home-base.mp4?v=20260926ship7`, displayed runtime 4 min.
- Actual file: **3:53.200**, **6,996 decoded frames**, **1280×720**, **30 fps**.
- SHA-256: `5e73454b5b7f468be774a46e25cf6377ed0fad030dc45a28d964f9825b1de018`. Exact match to the shipped v6 manifest.
- Content authority: `ModelSelectionSection` in `index.html` (beginning near line 7806), current board JPGs, and `CLOSE_BOARDS.modelselection` at line 1188. Upload source: `lessons/which-app.md`.
- Complete transcript: `../your-home-base-pacing-2026-09-26/transcript-v5.txt`. The v6 build changes only the Big Three camera treatment from v5; its audio/timeline is unchanged. This transcript was inherited, not freshly generated or verified by ear.
- Prior treatment and source lineage: September 16 v3, September 21 illustration sync, September 26 v5/v6 manifests and reviews. The original raw rolls are no longer available under `Prompts/`; a future repair must disclose use of the hash-pinned finished video and its extra visual encode generation.
- Public deployment and Video Tracker status were not checked. This review establishes the local file and local page reference only.

## Findings

### 1. Clarify the training graphic's common input label, approximately 0:50–1:01.17

The graphic says **“Shared Training Data (Web Patterns & Language)”** above a common line feeding all three systems. The lesson says all three learn patterns during training, with different company choices; it does not establish one shared dataset. The common-feed drawing can imply more sameness than the narration teaches.

**Proposed narrow correction:** change only that label to **“All Learn Patterns During Training”**, retaining the arrows, three systems, reveals, and surrounding illustration. This is a clarity correction to a potentially misleading relationship, not a reason to replace the entire graphic. Exact first visible label frame should be established before building; 1:01.17 is its outgoing scene cut. Evidence: `frames/extra-059.jpg`.

### 2. Correct apps-versus-models terminology, 2:21.40–2:35.03

The animated choice/age graphic is headed **“THE BIG THREE AI MODELS”**, but its named items are the apps ChatGPT, Claude, and Gemini. This lesson is explicitly about choosing an app and distinguishes the app from the models underneath it.

**Proposed narrow correction:** change the heading to **“THE BIG THREE AI APPS”** across this scene. Keep the moving “Top Benchmark” badge and the Claude age/access reveal. Half-second sequence inspection shows the badge moving ChatGPT → Claude → Gemini alongside “what is best today might change by next week.” It is an effective illustration of changing leadership, not a static claim that ChatGPT is the current benchmark leader. No numerical disclaimer or replacement still is needed. Evidence: `comparison-sequence-1.jpg` through `comparison-sequence-3.jpg`.

### Production treatment that should remain

- **Current assets:** Big Three and How We Used hashes exactly match the v6 inputs. Home Base matches the September 21 asset hash preserved by v6. All four current JPGs were inspected, and current-asset matching found them in the video. The final frame carries the current canonical closing design and wording.
- **Board pacing:** longest uninterrupted board appearance and longest consecutive board run are **19.900 s**, at 3:09.267–3:29.167. The final How We Used → close run is **19.633 s**. No additional cutaways are needed to satisfy rule 8b. Half-second matching rounds the 19.9 s appearance to 20.0 s; it is not a new overlong hold.
- **Rings:** fresh measurement finds **146 samples, all 4.0 px**, including board dives and monitor cutaways. This meets current Edit Spec section 5. Old references to 5 px elsewhere in the README/checklist are superseded by that explicit September 26 rule.
- **Framing:** Big Three begins fully visible and unmarked for about 3.27 s, then uses the owner-requested complete-card zoom and pan. A settled 720p frame shows the entire active card, including illustration and bottom question. Adjacent cards may be cropped. How We Used opens full and unmarked and remains at full view with whole-card rings.
- **Home Base illustration:** retains the previously approved full-view → ChatGPT-workstation detail → pullback. This is an existing illustration camera treatment, not a new proposal to crop a text card. Preserve it rather than applying a new redesign during a label repair.
- **Close:** starts at 3:42.300; 327 frames/10.9 s. Every close frame was decoded and pill geometry measured: width 720 px initially, 864 px finally, exactly **1.2×**. The opening bounds remain unchanged through the initial 48 frames; final bounds are reached by frame 197 and remain through the literal final frame. This corroborates the prescribed 48-frame hold / 150-frame push / settled hold.
- **Transitions:** fresh guard passes **16 checked boundaries**, including all 13 v6 assembly seams, both preserved Home Base board boundaries, and the picture surrounding the 3:16.70 audio splice. The every-frame strips were inspected in four overview sheets; no stale-frame insert was seen. This is a picture check, not an audio-join pass or an exhaustive check of every historical audio graft.
- **Source imagery:** no Notebook stock photograph, legible profanity, or engine corner mark was found in the inspected samples. The photographic Home Base scene is the current canonical course asset and is allowed. Existing drawn students, burger diagrams, and interfaces remain permitted under today's spec; the preference for realism applies to new custom graphics.

## Narration review

**VERDICT: provisional KEEP (transcript-based; listening pending).** No essential teaching gap or clear spoken factual contradiction to the supplied lesson was identified. No narration edit, new donor, reroll, or added pause is proposed.

| Teaching point, in lesson order | Assessment | Current-timeline transcript evidence |
|---|---|---|
| Which app; three names and companies; shared capabilities | TAUGHT | 0:00–0:21: ChatGPT/OpenAI, Claude/Anthropic, Gemini/Google; chat, write code, answer questions; why choose? Writing prose is not separately enumerated here but broad creation/work capability follows. |
| Burger analogy: similar ingredients, different experience | RICH | 0:21.68–0:46.12: In-N-Out/McDonald's, tiny fresh menu versus speed, scale, consistency. |
| Models learn patterns; company training/app choices shape behavior, strengths, uncertainty | RICH | 0:46.82–1:12.46: complete bridge from analogy to model/app choices and philosophies. |
| ChatGPT: Anything Box, general purpose, tasks and accessible capability | RICH | 1:16.42–1:34.58: questions, creation, daily work; “how do we put capable AI in everyone's hands?” |
| Claude: Thinking Partner, difficult tasks, safety/behavior and trust | RICH | 1:35.76–1:51.68: complex ideas and multi-step tasks; safety and predictable behavior; full trust question. |
| Gemini: built into Google, existing tools and integration | RICH | 1:52.32–2:09.48: existing Google tools and full integration question. |
| Strengths overlap; most tasks do not require agonizing; no permanent best | TAUGHT | 2:09.98–2:26.96: overlap, any tool for most jobs, best may change next week. Availability qualifier is carried by the following age note and assigned course app. |
| Claude 18+ and why it is included | TAUGHT | 2:27.76–2:34.62: restriction and knowing options before access. This is comparison with supplied course content, not an external policy fact-check. |
| ChatGPT is the course home base; depth beats dabbling | RICH | 2:35.14–2:44.50: settings, features, quirks, one app thoroughly. |
| Try same question in second app; missed detail/alternative route | RICH | 2:45.10–2:53.86: same question, missed detail, different approach. |
| Disagreement means investigate; agreement does not prove correctness | RICH | 2:54.40–3:03.26: both halves explicitly spoken. |
| Course example: different tools, both separate and overlapping jobs | TAUGHT | 3:04.40–3:16.32: several apps built course; different jobs and same task. |
| ChatGPT course uses | TAUGHT, one ASR uncertainty | 3:16.32–3:26.02: ideas, brainstorming activities/labs, lesson review, code, video editing. ASR writes “triads” at 3:20.20–3:22.46 where the course calls them “TRY ITs.” Do not silently certify the pronunciation or treat ASR alone as proof of an error; audition this phrase. |
| Claude course uses | TAUGHT | 3:26.94–3:33.46: code with Claude Code; pages with Claude Design. |
| Gemini course uses | TAUGHT | 3:34.18–3:41.80: current information; videos with Gemini Notebook. |
| Pick a home base and learn deeply | TAUGHT, verbatim in transcript | 3:42.64–3:44.76: “Pick a home base. Learn it deeply.” |
| Skills transfer; app is practice venue | TAUGHT, verbatim in transcript | 3:44.76–3:48.44: “The skills transfer. The app is just where you practice them.” |

**Hard requirements:** all three company guiding questions and both closing lines appear in full in the transcript. There is no extra sign-off. The page's interactive “It's in the Name” quiz remains a separate activity, not a missing narrated lesson explanation.

**Arc:** app-choice problem → burger analogy → different philosophies → specific apps → sensible choice/access → depth and cross-checking → actual course examples → transferable skills. Connections are spoken; no redundant restart needs removal. The already-trimmed “This infographic details…” sentence should stay removed.

**Additions:** multi-step tasks and daily-work examples elaborate existing points without changing their meaning. Some phrasing (“dynamically assigned,” “designated”) is more formal than the page, but does not require a narration edit.

**Source QA:** supplied page and upload Markdown agree on essential teaching and closing copy. No materials update identified. No external product/age-policy verification performed.

**Listening:** none performed in this review. Besides “TRY ITs,” audition the 3:16.70 narration splice. Historical donor joins near 1:52.20, 1:57.80, 2:03.10, 2:09.80, 3:04.63, and 3:42.30 remain relevant to a complete listening pass; the earlier editor also documented incomplete listening.

## Proposed narrow visual-only plan — no build performed

Patch the two labels above, keeping each scene's existing motion and reveal timing. No new graphics, changed audio, cuts, pauses, or runtime. Preserve the rest of the video and all board treatment below. This is a reviewable proposal, not an executed or newly approved build.

| Board | Highlighting | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| The Big Three, Side by Side | ChatGPT, Claude, Gemini: whole card → What It Is → company question. Unmarked overlap summary. Fixed 4 px outlines. | Full view first; approved uniform 1.19× complete-card dive/pans; full view for summary. | 1:12.933–2:21.400 topic block. Drawing breaks 1:23.900–1:28.000, 1:39.767–1:43.600, 1:57.800–2:02.933. Actual board pieces 10.967 / 11.767 / 14.200 / 18.467 s. | Keep entire treatment. Tall cards limit zoom; do not crop their interiors. Return views are settled. |
| Pick a Home Base. Learn It Deeply. | Unmarked. | Full introduction, existing workstation detail, pullback. | 2:35.033–2:47.233, 12.200 s. | Preserve previously approved illustration treatment. |
| How We Used the Big Three | One whole-card outline per app in spoken order; no item-by-item rings. | Compact, full view. | 3:09.267–3:29.167 (19.900 s), then 3:33.567–3:42.300 (8.733 s). Page-curl drawing between. | Brief supporting examples each teach one app's contribution. Existing break meets pacing guidance. |
| Pick a home base. Learn it deeply. | Unmarked canonical close. | 48-frame hold, 150-frame push to 1.2×, settled hold. | 3:42.300–3:53.200, 10.900 s; literal final frame. | Preserve. |

Supporting scenes to retain and their purpose (times are approximate except known hard cuts):

- **0:00–0:05.267:** student/laptop opening; introduces choosing a tool. Reused at **3:04.000–3:09.267** for course creation.
- **0:05.267–0:16.567:** app/company overview and common capabilities. An introductory comparison, not a recreation of the detailed course board.
- **0:16.567–0:21.700:** “THE IMPACT” transition; brief visual punctuation, optional aesthetic preference only.
- **0:21.700–about 0:46.8:** progressive burger comparison, showing philosophy → experience. Retain drawn people and assembly illustration.
- **About 0:46.8–1:01.167:** training/design relationship graphic. Keep animation; patch only the common-input wording.
- **1:01.167–1:08.533:** three-monitor illustration; different interfaces/uses. Its three short highlighted reuse spans are listed in the board plan. Their repetition is already approved and not a new spec violation.
- **1:08.533–1:12.933:** interface peeling back to underlying structure. Reused at **3:29.167–3:33.567** for building/design. It is a metaphor rather than a literal coding demonstration, but not misleading enough to justify replacement.
- **2:21.400–2:35.033:** moving leader badge, common capabilities, age/access. Patch “models” to “apps”; preserve the reveals.
- **2:47.233–3:04.000:** same-prompt/two-responses sequence, disagreement then agreement, ending on “CONSENSUS DOES NOT EQUAL TRUTH.” Retain. “Secondary Verifier” is shorthand weakened appropriately by the explicit warning; no claim that a second app guarantees truth should be inferred from an isolated earlier frame.

No selective pauses are proposed. Keep the existing approved breathing room before the course example and the existing narration trim. Without listening, there is no basis to add or remove time.

## Verification and limits

Fresh work: read current lesson, boards and complete inherited transcript; verified file and asset hashes; full video sequential decode plus successful full audio/video ffmpeg decode; five contact sheets at four-second intervals; selected 720p frames; half-second comparison/reveal sequence; half-second board and ring measurements; every-frame close bounds; 16-boundary guard and strip-overview inspection.

**Not done:** end-to-end audiovisual playback, listening to any words/joins/cadence, continuous animation review with sound, fresh ASR, fresh exact word-onset alignment, or exhaustive every-frame mark/stock inspection. Frame sequences support the visual recommendations but do not establish a complete in-motion teaching pass. These limits prevent an unconditional current-spec shipping pass.

Evidence: `verification.json`, `decode-check.txt`, `board-spans.txt/json`, `ring-stroke.txt/json`, `close-motion.json`, `current-boards.jpg`, `sheets/`, `frames/`, `comparison-sequence-*.jpg`, `guard/`, and `guard-overview-*.jpg`.
