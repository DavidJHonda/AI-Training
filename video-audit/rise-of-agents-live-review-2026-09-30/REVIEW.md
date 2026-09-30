# Rise of Agents live video evaluation

The published 3:07.8 video needs a factual correction before it can receive a clean pass. Its central explanation is worth preserving, but the Gemini file-deletion story was withdrawn by the original reporter. The PocketOS animation also depicts a deletion command that conflicts with the infrastructure provider's account.

This is an evaluation and proposed repair scope, not a build or release. The lesson, boards, video, and tracker were not changed.

## Verified version and review limits

- Public page retrieved September 30, 2026: `https://besmarterthanthetool.com/`. Its `LESSON_VIDEOS.agents` reference is `course-assets/rise-of-agents/rise-of-agents.mp4?v=20260924ship1`.
- The public video stream and local canonical MP4 have the same SHA-256: `d27f50d630ccae490c6d6c9511d6694d638e65dc073e8dd4ff9a4887ebfe8dcd`.
- Fresh sequential decode: 5,634 frames, 30 fps, 187.8 seconds. See `verification.json` and `public-video-headers.txt`.
- Read the current lesson in `index.html`, upload Markdown, current prompt, and complete v4 medium.en timestamped transcript. The transcript belongs to the matching shipped v4 file. Freshly inspected all four contact sheets covering the file at four-second intervals, selected full-resolution frames, and the literal final frame.
- **No direct listening or continuous audiovisual viewing was possible in this tool session.** Motion smoothness, pronunciation, cadence, and audio joins are unverified. Still-frame sampling is not an end-to-end watch. This is a content and sampled-visual evaluation, not shipping certification.
- Tracker status was not read or changed. Public file identity is independently verified; workflow status is not inferred from it.

## Required factual corrections

### Gemini files were found

At **2:27.40–2:37.94**, the narration says Gemini wiped out a user's project files, then quotes its apology. The canonical Rogue Agents board says **Project Files Wiped**; it is visible in both **2:01.10–2:09.50** and **2:22.77–2:38.63**. Removing only the spoken example would leave the false claim on screen.

The original reporter, `anuraag2601`, wrote on July 28, 2025: **“I did find these files in the C:\ root upon a deeper search.”** He apologized for the deletion alarm and explained that the AI responses and subsequent analysis had misled him. This directly changes the lesson's claim. The comment was retrieved through GitHub's public API and is retained in `gemini-issue-comments.json`. [Original reporter's correction](https://github.com/google-gemini/gemini-cli/issues/4586#issuecomment-3125818690).

**SOURCE_QA: FAIL.** The video accurately repeats a mistake in the lesson. Correct `index.html`'s Gemini alt text and hidden teaching prose, `lessons/rise-of-agents.md`, the canonical Rogue Agents JPG, and dependent generation materials before building a corrected video. Those are proposed dependencies, not edits made during this evaluation.

Two valid editorial directions:

1. **Smallest repair:** remove the Gemini example from the lesson and board, and cut the corresponding video sentence and apology. PocketOS already teaches that tool access can turn an AI mistake into real damage.
2. **Retain with new narration:** explain that Gemini misplaced the files and falsely reported their destruction; the user later found them. This supplies a useful second lesson: even an agent's explanation of its own actions needs verification. No corrected audio donor is identified among the reviewed rolls, so this option requires a new spoken beat.

Do not reuse the apology as evidence that deletion actually occurred.

### PocketOS animation invents the mechanism

The supporting diagram runs **2:09.50–2:22.77**. At **2:16**, it shows `403 PERMISSION DENIED`; at **2:20**, it shows `$ rm -rf /data /backups`, `TOTAL PURGE`, and `DESTROYED (0 B)`.

[Railway's own account](https://blog.railway.com/p/your-ai-wants-to-nuke-your-database) identifies an authenticated GraphQL `volumeDelete` request made with a locally stored API token. The shell command in the video is a different mechanism, and the precise `403` and zero-byte labels are not established by that source. Because the diagram is explicitly titled PocketOS Incident, these read as historical facts rather than a hypothetical illustration.

**Required visual correction:** retain the useful agent → access → database consequence sequence if its labels can be corrected throughout. Replace the command with plain language such as **Deletion request**, and use **Permission problem**, **Broad-access key**, and **Database and backups deleted** where needed. If the labels cannot be cleanly repaired, replace this span with a simple accurate supporting diagram. Avoid technical command text that adds no value for the student.

Railway also reports recovering the data. The current narration does not explicitly claim permanent loss, so this does not invalidate the deletion event; an optional recovery sentence would make the account more complete. Avoid imagery or wording implying that all possible recovery copies were permanently destroyed.

## Teaching coverage

Ratings below describe what the transcript teaches; they do not imply that its soundtrack was auditioned. A point can match the lesson and still fail external factual verification.

| Lesson point | Assessment | Evidence in this version |
|---|---|---|
| Introduce agents through a familiar analogy | TAUGHT | 0:00–0:31.14, Stanley Cup destination, navigation, steering, braking, self-driving |
| GPS advises; the person acts and catches mistakes | RICH in example, mapping THIN | 0:08.62–0:21.54, turn directions, hands on wheel, stopping at a bad route; GPS is not explicitly equated with ChatGPT |
| Self-driving acts; errors may go unnoticed until later | THIN | 0:22.12–0:37.82 teaches steering, braking, rerouting, and supervision; delayed discovery is MISSING |
| Chatbot answers; agent acts | TAUGHT; exact wording MISSED | 0:31.88–0:34.36 adds “but” to the required line |
| Agents are everywhere because they do the work | TAUGHT | 0:38.46–0:45.68, clear bridge into the example |
| Basketball highlight scenario | TAUGHT, compressed | 0:46.10–0:50.08 preserves 30 points, Friday, TikTok; friend's phone and 50 clips are not spoken |
| Human does the editing; chatbot contributes a caption | TAUGHT | 0:50.56–0:57.44; selection and posting-time details compressed; one-answer-and-stop distinction taught again at 1:21.96 |
| Agent carries the job through; human owns goal and final review | RICH | 0:58.14–1:11.74, task sequence and ownership stated explicitly; choosing a posting time is not spoken |
| Same kind of LLM, not a new kind of AI | RICH | 1:12.28–1:19.18 |
| After the prompt, chatbot stops; agent plans and uses tools | TAUGHT | 1:19.76–1:31.90, then Check is supplied by the loop explanation |
| Goal, Plan, Act, Check | TAUGHT | 1:32.40–1:41.44; Goal's human owner is made explicit at 1:49–1:51.72 |
| Check returns to planning when unfinished | RICH | 1:41.94–1:46.40, “loops back, adjusting the plan” |
| Human sets goal and judges result | TAUGHT | 1:47.02–1:51.72, required banner spoken |
| Review and improve the agent's work under your name | RICH | 1:07.84–1:11.74 plus 1:52.44–1:57.84; these together carry the responsibility point |
| Agents are good but imperfect | TAUGHT | 1:58.46–2:00.46 |
| Continued action plus vague goals or excess access can cause damage | RICH | 2:01.12–2:08.86 |
| PocketOS case, date, access, database, backups, nine seconds, quotation | RICH against lesson | 2:09.52–2:26.82; visual mechanism needs correction as above |
| Gemini project files wiped, apology | WRONG fact; matches lesson | 2:27.40–2:37.94; original reporter later found the files |
| Review before send, spend, submit, delete, post | RICH | 2:43.64–2:49.24, full list and human checkpoint |
| Advanced tools; start by getting good at ChatGPT | TAUGHT | 2:49.88–2:57.52 |
| Both closing lines, nothing spoken afterward | MET in transcript | 2:58.22–3:03.40; canonical close is the literal final frame at 3:07.77 |

Seven of the eight prompt-required passages match the transcript's words, allowing ordinary spoken punctuation. The first passage has the extra “but.” The earlier v3/v4 records explicitly identify this wording and the missing delayed-error warning as tradeoffs in the owner's chosen opening. They are not newly discovered faults or grounds to silently replace that opening. If revising it now, preserve the approved analogy scenes and restore the missing caution as a separate beat.

**Narration verdict:** the actual file cannot earn KEEP because the Gemini claim is factually wrong. A **REPAIR is the recommended direction**, conditional on correcting the source lesson and removing or replacing that example. It is not yet a verified repair under Narration Review: the proposed new join has not been auditioned, and no corrected Gemini donor is identified. A full reroll is not justified by the visual issues alone.

The lesson arc otherwise works: analogy → concrete work → underlying mechanism → responsibility → consequences → practical rule. The own-goal/final-review line and subsequent TikTok responsibility line reinforce different parts of the point rather than merely repeating a slogan.

## Proposed edit scope

First resolve the Gemini source correction. Recommended minimal direction: retain PocketOS as the sole destructive incident, remove the inaccurate Gemini case, and correct the PocketOS animation. Preserve the existing introduction and other narration unless the owner chooses the optional restoration below.

The proposed removal is **2:27.40–2:37.94**, from “In 2025, a Google Gemini agent…” through “…completely and catastrophically.” The resulting spoken join would be **“…I violated every principle I was given.” → “You can never expect an agent to safely navigate poorly defined constraints on its own.”** The current transcript has approximately 0.58 seconds between the PocketOS quotation and the Gemini sentence, and 0.36 seconds between the Gemini quotation and the next sentence. These are transcript intervals, not measured acoustic silence. Select exact cut frames within waveform-confirmed gaps and audition the joined sentences before calling this feasible. No target pause or added silence is approved or proposed yet.

Optional opening restoration: `Prompts/rise-of-agents-2.mp4`, **0:16.06–0:18.02**, says “You may not catch mistakes until later.” It could follow the self-driving explanation, before the chatbot/agent summary. This is an identified textual donor, not an auditioned graft. It would alter the previously approved opening and is separate from the required factual corrections.

### Board highlighting and camera proposal

Times below are the existing output timeline, derived from the v4 manifest and checked against sampled frames. Corrected output timings depend on the selected narration change.

| Board | Highlighting sequence | Camera | On screen and breaks | Reason or exception |
|---|---|---|---|---|
| A Chatbot Answers. An Agent Acts. | Preserve title emphasis with the spoken contrast | Full board | 0:31.67–0:38.20, 6.53 s; driving drawings precede it | Keep approved intro. If the caution donor is added, timing and matching imagery need a separate preview |
| Ask a Chatbot versus Hire an Agent | Scenario → You Do → AI Does → The Agent Does → What Changes → You Still Own | Full view then complete active-card framing | 0:45.97–0:53.20, 7.23 s; phone-of-clips break 0:53.20–0:55.50; board 0:55.50–1:12.20, 16.70 s | Preserve section highlights; full-resolution sample keeps the complete active card readable |
| What an Agent Does | Goal → Plan → Act → Check → return arrow → banner | Compact, full view | 1:29.03–1:52.30, 23.27 s | Longest board run. Narration actively walks all steps; slightly beyond the approximate 20-second preference. No useful new cutaway identified, so do not insert decorative filler |
| Rogue Agents | After source correction, PocketOS case → quotation; omit Gemini targets for removal option | Preview revised canonical board at full view, choose density after inspecting corrected asset | Existing 2:01.10–2:09.50, 8.40 s; corrected diagram 2:09.50–2:22.77, 13.27 s; return 2:22.77–2:38.63, 15.87 s, shortened by Gemini removal | Board must be corrected in both appearances, including the setup before Gemini is spoken |
| Agents do the work. The name on it is yours. | No rings | Preserve standard close | 2:58.17–3:07.80, 9.63 s including final hold | Literal final frame verified; both closing lines present |

Preserve these supporting scenes, subject to continuous playback QA during a build: driving/navigation drawings **0:00–0:31.67**; completed-tasks dashboard **0:38.20–0:45.97**; phone clips **0:53.20–0:55.50**; shared LLM and contrasting processes **1:12.20–1:29.03**; human oversight **1:52.30–2:01.10**; unclear-goal warning **2:38.63–2:43.30**; review-and-approve **2:43.30–2:47.90**; eye key and simple-chat/complex-dashboard **2:47.90–2:58.17**. Each illustrates a distinct spoken idea. The “Autonomous” label is more technical than the course voice prefers, but does not by itself justify discarding the explanatory animation.

Ring widths in sampled frames are heavier than the current 4 px delivery standard. Edit Spec explicitly grandfathers videos shipped under the older rule; this is not a standalone reason to rebuild. Apply fixed 4 px to changed board spans in the next build.

## Remaining verification

The automated `board_spans.py` and `ring_stroke.py` passes were stopped before completion. No fresh numerical ring-width measurement or automated board-match result is claimed. Board durations above come from the existing edit manifest, checked against fresh stills; the separate full sequential decode completed successfully.

No new transition guard was run because no candidate was built. The prior record reports 19 passing visual boundaries; that is historical evidence only. All audio joins remain unverified here, particularly **0:38.20, 0:44.03, 0:45.97, 1:32.20, 1:46.77, 1:51.97, and 2:43.30**, plus any new Gemini removal or replacement join.

The frame inspection supports the findings above; it does not certify every animation frame, ring state, or audible splice. Required next work is the source correction and a targeted, auditioned repair, followed by review of the actual encoded candidate. No release action is part of this evaluation.
