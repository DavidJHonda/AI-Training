# Context Window v4 → v5, 2026-09-26

**SHIPPED 2026-09-26 on David's "ship it".** `Prompts/context-window-v5.mp4` was copied to `course-assets/context-window/context-window.mp4` (SHA-256 verified identical: `6d3e3ff7…`, 26,564,928 bytes). `index.html` cache key is now `?v=20260926ship9`; the pill stays "4 min" (4:08.70). The manifest `video_assets` row is refreshed; it still held the 09-16 hash. David's ear-check of the audition clips was not recorded before shipping.


**v5 (current review copy): `Prompts/context-window-v5.mp4`**, SHA-256 `6d3e3ff7d2ad4c0019a460a44e250470a47b19ca2998f4eab0f8539300cb7c12`, 7,461 frames (4:08.70). Built after David's note on v4: "At 1:20, there's a flash of an old graphic." It was the 0.77 s hands-on-keyboard drawing (1:19.97–1:20.73). It is leftover footage from the 09-16 video and is also in the live video; I had wrongly listed it below as harmless. In v5, the context-window panel's settled frame ("CAPACITY FULL (100%)") holds over it until The Context Window board arrives at 1:20.73, inside the 80.26–81.10 s silence. The picture now makes one cut in 1:19–1:21. `transition_guard.py` passes at 1:06.3, 1:06.8 and 1:20.73. The narration is unchanged from v4: the only audio difference is a 5 ms room-tone crossfade inside that silence, plus re-encode noise about 42 dB below the speech. Everything below describes v4 and applies to v5 unchanged. Build script: `scripts/video/build_context_window_v5.py` (the v4 script plus this one row). v4 is kept.


**Candidate:** `Prompts/context-window-v4.mp4`. SHA-256 `ab21e7fb99530bfdbd59e35bf1f2a3e37eff5f0fa080ff9c45515b76fb259d22`. It decodes to 7,461 frames at 30 fps (4:08.70).
**Source:** the live `course-assets/context-window/context-window.mp4` (v3, 20260921ship6, SHA `6b3a4d39…`, 4:25.47). The live file, the lesson page, `lessons/context-window.md` and every board JPG are unchanged (their hashes were verified after the render). **Not shipped.**
**Build:** `scripts/video/build_context_window_v4.py`. The board legs, clips and wavs are in `build/`. `--render-existing` re-renders without rebuilding the legs.
**Scope:** the approved narrow repair. Three long board holds are broken up, three wording repairs come from existing narration, and the two 09-21 grafts are checked. No reroll and no new narration.

## Source limitation

Rolls `context-window-1` and `-2` and the archived live v3 no longer exist. **The live file is the only source.** So:
- Every cutaway is a drawing that already appears somewhere in this video. Each one is moved, re-timed or shown a second time. No unseen footage exists.
- Every kept Notebook frame is one encode generation further from Notebook. The boards and the close are re-rendered from the canonical JPGs, so they are not affected.
- The corner mark was already removed at the 09-21 build, so corner cleaning did not run.

## Change log

| # | Output time | Change |
|---|---|---|
| 1 | 0:33.4–0:38.9 | Cutaway from Same Question to the video's own two-phones drawing (from 0:08.3). It shows the same scribbled prompt on both phones with two different outputs, under "But when Nate types the exact same prompt into the same app, ChatGPT responds". The drawing is static, as it is in the opening. Nate's ring now starts at his quote (0:39.1). |
| 2 | 0:51.6–0:58.7 | Same Question now leaves after its banner line. The pickup-truck panel ("Earlier Chat: Nate: 'I love pickup trucks.'") arrives under "Different doesn't always mean wrong". Its note builds, holds, and then plays in its original sync from 0:58.7. |
| 3 | 1:06.3–1:06.8 | The 0.5 s Jeep/Raptor phones flash is covered by the desk drawing's first frame. That drawing has prompt-leak labels ("WOBBLY FORD RAPTOR", "ALCOHOL-MARKER ALCOHOL WASH") and a Ford grille logo. |
| 4 | 1:48.9–1:52.4 | The input diagram (inputs → context window → model output) holds on its settled frame under "Because we know exactly where the AI looks for information". Give AI a Head Start arrives on "you can intentionally load these areas", 4.1 s before Personalization. |
| 5 | 2:17.0–2:20.9 | Cutaway to the context-window panel (five sources fly into the window; first shown at 1:10.5), under "and brings those notes into the context window for future chats". |
| 6 | 2:20.9–2:27.0 | Cutaway to the pickup-truck panel, re-timed for the Saved Memory example. The note appears on "you love pickup trucks", the new prompt on "saves that detail", and the Ford Raptor on "buying a vehicle". The board returns 0.5 s before "Finally, projects". |
| 7 | 2:46.6–2:51.0 | The "what's outside" tiles drawing (Older Chats, Live Web, Local Files outside the context window) holds 1.6 s longer under the intro. Outside the Window arrives 3.3 s before Older Chats. |
| 8 | 3:14.8–3:19.3 | That tiles drawing returns under "A local file isn't enough. You must upload it…". The Local Files tile lands on "You must upload it". |
| 9 | 3:07–3:11 | Narration: "you must share **the link** or the app" became "you must share **it** or the app". "share it" is the same narrator's, from 3:27.76 ("actively share it or connect the app"). It is spliced at sample precision: a 6 ms crossfade inside the /sh/ sound, then a 5 ms join in the quiet after the /t/. The donor is −1 dB. |
| 10 | 3:38.5 | Narration: "The primary reason is space." removed (live 3:38.83–3:41.00). The section now reads: "…something you told it earlier? Because the context window has a hard limit, older parts…". |
| 11 | 3:57.1 | Narration: removed "so the new task begins with a completely clean context window. Keep in mind, a fresh chat does not increase or reset the underlying context window limit of the model. It simply clears out the old data to make maximum room for the new." (live 3:59.55–4:13.87). The section now ends on the page's own "start a fresh chat." Under that line, the mechanics panel's messages clear out of the window, and its "Fixed Limit / Max Context Limit" frame stays. I skipped 16 static frames so the clearing finishes before the close. |
| 12 | 0:57.1–1:06.3 | Level: roll 1's why-beat graft raised +3.0 dB. It measured −18.2 LUFS between −15.6 and −14.5 and now measures −15.3. |
| 13 | 2:22.9–2:27.1 | Level: the "vehicle" graft lowered −1.8 dB. It measured −14.2 between −16.7 and −16.0 and now measures −16.0. The 09-21 build's +1.8 dB was calibrated on whole files and was wrong locally. |
| 14 | all boards | Rings re-rendered at an exact 4 px at 720p (6 px at 1080p) at every zoom. `ring_stroke.py` measures 4.0 px on every ring run. `ken_burns_path.py` is unchanged: the build swaps in the exact-width drawer from Your Home Base v5. |

Everything else is kept: the calculator, both full car answers, the pickup explanation, "Different doesn't always mean wrong", the context-window definition, the five-sources walk, all three Head Start features with their examples, all four Outside categories with their qualifications, the forgetting problem and "remind AI", both closing lines, and the standard navy-and-yellow close. The compressed distrust paragraph is unchanged.

**Transcript check (medium.en, candidate against live):** the only word differences are the three intended ones. Both small.en and medium.en read the splice as "which means you must share it or the app must actively retrieve it."

## Board holds, before and after

These come from `board_spans.py` (ORB match every 0.5 s) on both files. The candidate's figures are in `qa/board-spans.txt`.

| Board | Live v3 | v4 candidate |
|---|---|---|
| Same Question. Different Answers. | 0:11.0–0:57.5 = **46.5 s** | 0:11.0–0:33.5 = **22.5 s**, a 5.5 s drawing, then 0:39.0–0:52.0 = **13.0 s** |
| The Context Window (not in scope) | 1:21.0–1:42.5 = 21.5 s | unchanged, 21.5 s |
| Give AI a Head Start | 1:49.0–2:47.0 = **58.0 s** | 1:52.5–2:17.0 = **24.5 s**, 10.0 s of drawings (two), then 2:27.0–2:47.0 = **20.0 s** |
| Outside the Window | 2:49.5–3:33.0 = **43.5 s** | 2:51.0–3:15.0 = **24.0 s**, a 4.5 s drawing, then 3:19.5–3:33.0 = **13.5 s** |
| Close | 4:14.5–4:25.5 | 3:57.5–4:08.7 |

**Uninterrupted board sequences.** In the live file, Head Start and Outside are split only by a 2.5 s drawing, so boards effectively fill **1:49–3:33 (104 s)** with a 2.5 s break. In v4 the longest continuous board run is **24.5 s**. Across the same stretch the breaks now total 10.0 s, 4.4 s and 4.5 s. Board time dropped from 148 s to 117.5 s; teaching time on the three boards is unchanged.

The detector's 1:48–1:49 "Same Question" hit (33 inliers) is a false match: the frame is the input diagram.

**Cutaways that give less relief than their length suggests:**
- The two-phones cutaway (5.5 s) is a still. It changes the picture but has no motion, which is also how it appears in the opening.
- The input-diagram extension (3.5 s) is a held settled frame, so the diagram sits still for about 5 s in total.
- The tiles drawing is 2.7 s of motion plus holds: 4.4 s under the intro (1.6 s held) and 4.5 s under Files (1.8 s held). It is the same drawing both times, 25 s apart.
- ~~The 0.8 s hands-on-keyboard drawing at 1:20~~: removed in v5 (David: it read as a flash of an old graphic).

**Still over 20 s, with no donor:**
- Same Question 22.5 s: the question plus Luke's full answer. No drawing of Luke's answer survives.
- Head Start 24.5 s: the intro, Personalization and its example, and the Saved Memory definition. The only drawing for "learning to code" is the desk drawing, which has gibberish notebook text ("fineliner notes / wobbly annse & notes"), so I did not reuse it.
- Outside 24.0 s: Older Chats and Web Pages. No drawing exists for either.
- Head Start 20.0 s: Projects and its example. No drawing exists.

**Drawings shown twice (please judge whether it reads as recycled):**
- The pickup-truck panel: the why-beat, then the Saved Memory example, 84 s apart. The lesson uses the same example twice, so this is a callback.
- The context-window panel: the definition, then Saved Memory, 67 s apart.
- The two-phones drawing: the opening, then the car comparison, 25 s apart.
- The tiles drawing: the intro, then Files, 25 s apart.

## Wording repairs: exact outcome

1. **"One reason is space": not achievable.** Neither "One" nor any other hedge exists before "reason" in the surviving audio. I removed the sentence instead. That drops the overclaim, but the line never says "one reason". "Because the context window has a hard limit…" now answers the question directly.
2. **New chat: partial.** Both overbroad phrases are gone, and the section ends on the page's own "start a fresh chat." No existing words say "removes this conversation's accumulated messages", so the narration never states it. The picture shows it: the messages clear from the window while the limit frame stays. This also removes the "does not increase or reset the limit" sentence. The current page no longer has it, but `lessons/context-window.md` still does. Tell me if you want it back (live 4:03.8–4:09.7, one clean cut either side).
3. **Web pages: done**, with "share it" in place of "share the link". Risk: the donor "share" carries a pitch accent. Its pitch starts at about 320 Hz, against about 223 Hz for the original "share". In context that reads as contrast ("SHARE it or the app retrieves it"), but it may sound emphatic.

## Graft and join checks (machine measurements; nothing was heard)

| Join | Output | Finding |
|---|---|---|
| 09-21 roll-2 cut ("budget. / Same question") | 0:48.4 | 0.41 s gap, floor steady. Pitch is in range (185 → 172 Hz medians). |
| Why-beat graft in | 0:57.1 | It was 2.6 LU quiet; now level-matched. Pitch 224 (before) against 175 Hz is within the narrator's usual range (150–234 Hz). Spectral brightness matches. |
| Why-beat graft out | 1:06.3 | Level-matched. 0.59 s gap. |
| Vehicle graft | 2:22.9–2:27.1 | It was 2.5 LU loud; now matched. The sentence ends with rising pitch ("vehicle" at about 219 Hz), which is the live v3 take's own delivery. |
| Web splice | 3:08.85, 3:09.39 | Both ASR models read it as intended. Pitch-accent risk noted above. |
| "primary reason" cut | 3:38.5 | About 0.5 s pause after the question (the live had 0.52 s). The noise floor steps about 5 dB quieter across the cut, at about −50 dB. |
| "fresh chat" cut | 3:57.1 | 0.61 s to "Ultimately" (the live had 0.57 s). "chat" is fully released. Its pitch falls to about 167 Hz rather than a firm sentence-final low; medium.en punctuates it as a full stop. Floor steps about 5 dB quieter. |

Pre-existing issues, left alone:
- Near-digital-silence in pauses at 1:00.9–1:01.3 (inside roll 1's graft) and 1:58.3–1:58.8 (Head Start).
- The narrator says "You mentioned" where the page has "You mention".

## QA completed

- The decoded frame count matches the plan: 7,461.
- `transition_guard.py` passed all 22 declared seams, and I looked at every strip (`qa/transitions/`).
- Board state sheets were inspected. Rings sit on the card bodies, and each board opens full view.
- Ring stroke is 4.0 px on every ring run.
- Cutaway frames were spot-checked at full resolution. No photographs, logos or prompt-leak text were added.
- Transcript diff and LUFS were measured at every graft.

## Not performed, for you

- **No listening by ear, and no real-time playback.** I cannot hear, so every audio judgement above is a measurement: level, pitch, spectrum, ASR, silence. Audition clips (live against v4) are in `audition/`:
  - `1-why-graft` (0:52–1:08)
  - `2-vehicle-graft` (2:19–2:29)
  - `3-web-pages` (3:02–3:14): the pitch-accent question
  - `4-primary-reason` (3:32–3:43)
  - `5-fresh-chat` (3:46–end): whether "start a fresh chat." lands as an ending
  - `6-roll2-cut-0m48`
- Watch the whole candidate once, especially whether the four second showings read as recycled.
- Pre-existing issues outside scope: the desk drawing's gibberish text (1:06.8–1:10.4), the five-sources board (21.5 s, untouched), and the "You mentioned" wording.

After shipping, `clean_video_audit.py` can reclaim the 2.1 GB `build/` folder.
