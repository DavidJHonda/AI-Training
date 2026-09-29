# Context Window — live evaluation, 2026-09-29

**Owner disposition:** the 1:07–1:10 desk scene was explicitly accepted as-is. The owner approved only the forgetting-animation label change; see `../context-window-label-repair-2026-09-29/REVIEW.md` for the v6 review candidate. The other optional suggestions were not applied.

**Recommendation: keep the teaching; targeted visual cleanup.** Narration coverage earns **KEEP against the current lesson**, provisionally on transcription. This is not a complete audiovisual sign-off: no listening or continuous real-time playback was performed. No video, lesson, board, or website reference was changed.

## Exact file and method

- Public file: https://besmarterthanthetool.com/course-assets/context-window/context-window.mp4?v=20260926ship9
- Local file: `course-assets/context-window/context-window.mp4`.
- Both SHA-256 hashes: `6d3e3ff7d2ad4c0019a460a44e250470a47b19ca2998f4eab0f8539300cb7c12`; 26,564,928 bytes. Public page reference and streamed public-file hash verified today; see `public-verification.json`.
- 4:08.70; 7,461 decoded frames; 30 fps; 1280×720. This is the shipped v5, not an older review candidate.
- Read current `PromptSection`, both supporting board components, upload Markdown, prior review, and current video review rules. Read the complete newly generated timestamped transcript. Inspected six contact sheets spanning the file and full-resolution frames at selected teaching, board, and closing moments. Ran fresh board-span and ring-stroke measurements.
- Speech timestamps below are approximate ASR segment times. They are review locations, not sample-accurate edit boundaries. Tracker was not accessed or updated.

## Teaching assessment

| Essential point | Assessment | Evidence in this file |
|---|---|---|
| Calculator versus AI | RICH | 0:00–0:11, 2 + 2 → 4, same input and answer, followed by AI contrast. |
| Identical car question | RICH | 0:11–0:19, asks what car to buy after college. |
| Luke's answer | RICH | 0:19–0:34, no strong preference, versatile Jeep Cherokee, price/reliability/insurance/fuel caveats. |
| Nate's answer | RICH | 0:34–0:49, pickup preference, Ford Raptor, interests and affordability caveats. |
| Different context explains the split | RICH | 0:49–1:06, comparison refrain, “Different doesn't always mean wrong,” and earlier pickup preference causing the recommendation. |
| Context window definition and limited working memory | TAUGHT | 1:06–1:20, what the model can see for the answer; working memory and capacity. |
| Current prompt and earlier messages/answers | TAUGHT | 1:20–1:34, names both chat sources and explains their relationship to the tray. |
| Personalization, saved memory, projects feed the answer | TAUGHT | 1:34–1:56, overview followed by the practical head-start transition. |
| Personalization and coding example | RICH | 1:56–2:11, interests, answer preferences, plain language and explanations of new coding terms. |
| Saved memory and pickup example | RICH | 2:11–2:26, app brings useful notes into future context; vehicle example carried through. |
| Projects and summer-job example | RICH | 2:26–2:46, instructions/files/chats, résumé, applications, interview help, avoiding repeated setup. |
| What does not enter automatically | TAUGHT | 2:46–2:54 explicitly sets up the qualification before the four categories. |
| Older chats | TAUGHT | 2:54–3:03, app must bring relevant information into this conversation. |
| Web pages | TAUGHT | 3:03–3:11, share the information or have the app retrieve it. ASR reads the previous repair as “share it.” |
| Local files | TAUGHT | 3:11–3:20, upload or grant access; local existence alone is insufficient. |
| Other apps/tabs | TAUGHT | 3:20–3:32, open on screen is not in the conversation; share/connect; outside-window refrain. |
| Forgetting and response | TAUGHT | 3:32–3:57, older conversation can be shortened/omitted, remind AI, start a fresh chat for a different task. |
| Closing message | MET | 3:57–4:04, both “With the right context, AI gives better answers” and “Control the context, control the quality.” |

The arc is coherent without relying on the pictures: surprising difference → reason → sources → controls → boundaries → forgetting → action. The car answers and the three practical examples preserve the lesson's substance. The distrust paragraph is compressed adequately. The LAB is below the common watch/read endpoint and remains a separate page activity; omitting its click-by-click instructions is not a missing video teaching point.

**Source QA:** no material contradiction with the current page found. The upload Markdown additionally states that a fresh chat does not increase/reset the model limit. That sentence is absent from the current page and video; its absence is not a current-page coverage failure. The working-memory definition is a beginner simplification. Technically the token budget also includes output and, for applicable models, reasoning; see [official OpenAI documentation](https://developers.openai.com/api/docs/guides/conversation-state#managing-the-context-window). This does not require expanding this introductory video into an API lesson.

**Precision to consider at a future narration edit:** 1:42–1:56 uses “totality” and “we know exactly where the AI looks.” These are more absolute than the page's “five places” framing. Prefer describing these as the context sources the lesson teaches. This is an optional narrowing of the framing, not an identified missing essential explanation. No audio cut or graft is proposed in this visual review.

**Addition:** 1:17–1:20 distinguishes the working-memory metaphor from physical hard-drive storage; useful at this level.

## Visual findings and priorities

1. **Clean the desk drawing, approximately 1:06.3–1:10.4.** The notebook visibly contains production-style phrases including “fineliner notes” and malformed text; book labels are also garbled. See `details/68.00.jpg`. The drawing supplies little explanation of the context-window definition. First choice is a localized cleanup of the notebook/book text preserving the existing composition; if impractical, replace this brief insert with a relevant context illustration. Do not retain it solely because the preceding half-second flash was fixed in v5.
2. **Simplify the labels in the forgetting animation, approximately 3:38–3:57.** Its useful sequence shows older information leaving, a reminder restoring relevant context, and a fresh-chat clear-out. Preserve that sequence. But the first expelled item is specifically “System Instructions: Setup”; other labels include “Database Schema” and “Update Endpoints.” These unnecessary implementation labels invite an unsupported general inference about which instructions disappear. Relabel the example as ordinary student conversation details, including the moving and settled copies, rather than treating this as a verified account of ChatGPT's internal truncation policy. This is an editorial inference from the displayed sequence, not a claim that the cited API guide documents ChatGPT's exact handling of system instructions. See `details/219.00.jpg`, `223.00.jpg`, and `232.00.jpg`.
3. **Optional next-build refinement: Head Start whole-card introductions.** The current ring goes directly to each definition, then its example. Current Edit Spec 1b prefers a brief whole-card outline when introducing a card before section emphasis. Keep its complete-card framing and legible definition/example treatment; this is a standards refinement, not a reason to rebuild all boards now.

The capacity animation's illustrative “100%” at about 1:19 is a depiction of a full example, not a measured product statistic. It is not a defect merely because the example has five labeled source blocks. Likewise, repeated pickup imagery is an appropriate callback because the lesson deliberately reuses the example for saved memory.

## Proposed board/camera plan

This is an evaluation proposal, not an approved build. Preserve existing board timing for a narrow cleanup. Approximate detected spans have 0.5-second resolution.

| Board | Highlight sequence | Camera | On screen / breaks | Recommendation |
|---|---|---|---|---|
| Same Question. Different Answers. | Question → Luke → Nate → takeaway | Full board with restrained movement; no chat-card dive | 0:11–0:33.5; two-phone drawing; 0:39–0:52 | Preserve. Both answers are fully explained. |
| The Context Window | Five sources grouped as narrated; existing image walk remains unringed | Whole image first, then left and right source groups | 1:21–1:42.5 | Preserve the overview/detail distinction; no extra break needed. |
| Give AI a Head Start | Personalization definition/example → Saved Memory definition and illustrated example → Projects definition/example → takeaway | Whole board first, complete active card retained in closer views | 1:52.5–2:17; context/pickup cutaways; 2:27–2:47 | Preserve; optional whole-card intro rings on next board rebuild. |
| Outside the Window | Older Chats → Web Pages → Files → Other Apps/Tabs → takeaway | Whole board first, complete-card zoom and transitions, return wide | 2:51–3:15; files illustration; 3:19.5–3:33 | Preserve. |
| Closing message | Unmarked canonical close | Existing hold/push/settled ending | 3:57.5–4:08.7 | Preserve. Literal final decoded frame inspected. |

Longest uninterrupted board run: **24.5 seconds**, Head Start, 1:52.5–2:17. It continues teaching the displayed material. The five-sources board lasts 21.5 seconds and is actively walked. These are not automatic failures based on duration. The detector's “Same Question” at 1:48.5–1:52.5 is a false positive: inspected images show the input/output diagram.

Stable actual course-ring runs measure **4.0 pixels**. Raw detector outliers include drawn gold highlights, artwork, and transitions; the mixed histogram is not evidence that the course rings change width. Sampled boards match current page layouts and wording. Detailed fresh seam-by-seam transition certification was not performed.

## Supporting scenes to retain

| Approximate span | Teaching purpose / treatment |
|---|---|
| 0:00–0:11 | Calculator establishes repeatable output. Retain. |
| 0:33.4–0:38.9 | Two phones support same prompt/different response. Retain; its stillness is not a content defect. |
| 0:51.6–1:06.3 | Pickup preference → car answer explains causation. Retain. |
| 1:10.4–1:20.7 | Source blocks entering limited working memory. Retain illustrative capacity sequence. |
| 1:42.5–1:52.4 | Inputs/context/output connects the overview to giving the model useful information. Retain. |
| 2:17–2:27 | Context blocks and pickup callback illustrate saved memory. Retain. |
| 2:46.6–2:51; 3:14.8–3:19.3 | Outside tiles support information boundaries and file access. Retain; reused shot is modest optional polish. |
| 3:33–3:38 | Long-chat paper trail introduces forgetting. Retain. |
| 3:38–3:57 | Preserve the sequence but simplify labels as above. |

These retention recommendations come from extracted frame sequences and transcript alignment. Smoothness and real-time engagement have not been auditioned.

## Listening and remaining verification

No audio was heard during this pass. A transcript cannot certify pronunciation, cadence, graft continuity, noise-floor steps, or natural pauses. Before calling a repaired version fully verified, listen end to end, especially 0:48, 0:57–1:06, 2:21–2:27, 3:07–3:11, 3:38, and 3:55–3:59. These locations include prior edits and are review targets, not newly proven audio defects.

No new pauses, narration grafts, reroll, or deployment are recommended by this evaluation. No ship authorization is implied. Evidence files include `context-window/transcript.txt`, `board-spans.txt`, `ring-stroke.txt`, `sheets/`, and `details/`.
