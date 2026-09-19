# Hallucination v8 review candidate

## Recommendation

**KEEP as the new review candidate.** The opening now alternates between the example board and four teaching-aligned visual passages from Hallucination-1 and Hallucination-2. The updated “Why Hallucinations Happen” board appears at 1:05.567 with the first title reduced to “Learns From / Training Text.”

Candidate: `Prompts/hallucination-v8.mp4`

- SHA-256: `fd1eb11fa7cfbba2cc75daa69108328f6a9c05dffabeb3dcf26026af28a0cc2b`
- Runtime: 4:00.667
- Video: 1280x720, 30 fps, 7,220 frames
- Status: review candidate only; not deployed

## Opening visual revision

The original example board previously occupied the full 0:00-1:05.567 opening. It now appears in two shorter passages totaling about 20.7 seconds. The new sequence is:

| Output span | Picture | Teaching purpose |
| --- | --- | --- |
| 0:00.000-0:12.767 | Hallucination-2 laptop and prompt | Introduces the student's question as the narration asks it. |
| 0:12.767-0:21.767 | Current “Nothing Sounds Wrong” board | Shows the fabricated answer and its precise claims. |
| 0:21.767-0:34.233 | Hallucination-1 Stanford and “Authority Without Evidence” visuals | Supports the narration about institutional weight, sample size, precise percentage, and apparent care. |
| 0:34.233-0:45.667 | Hallucination-1 response-anatomy visual | Separates real anchors, plausible details, and the fabricated claim while the narration explains that the study does not exist and an invented detail was attached to a real fact. |
| 0:45.667-0:53.867 | Hallucination-2 “HALLUCINATION” visual | Lands on the definition of an AI hallucination. |
| 0:53.867-1:05.567 | Current “Nothing Sounds Wrong” board | Returns to the worked example while the narration explains that one specific false detail can be embedded in otherwise realistic advice. |
| 1:05.567 onward | Updated “Why Hallucinations Happen” board | Begins the mechanism explanation with “Learns From / Training Text.” |

## Verification

- All 11 declared visual boundaries passed the stale-frame/island transition guard; the six new opening strips were also inspected frame by frame.
- A two-second opening pass confirms that each borrowed visual supports the narration at that moment and that the example board returns at the two points where its text is useful.
- The encoded 1:06 frame confirms the updated board title is legible on two lines.
- The complete automatic transcript contains 636 words and preserves all three approved narration repairs.
- Decoded v8 audio is byte-identical to decoded v7 audio: SHA-256 `248be259a56b555b46bd292bf08313bcff95f0499d6ca23ff9ba0272d3287c40`.
- The existing six narration joins retain their prior sample-continuity measurements and the decoded peak remains 0.699677.
- Protected inputs were hash-checked after rendering and are unchanged.
- `index.html` was not edited by this build.

## Remaining human check

This environment could inspect frames, transitions, transcript timing, and decoded audio samples, but it could not play the result perceptually. The visual revision does not change audio. If v7's audio was already human-approved, no new audio audition is required; otherwise the six narration-boundary checks listed in the v7 review remain pending.

Detailed overlay mappings, source hashes, board timing, and render metadata are in `edit-manifest.json`.


## Shipped

**SHIPPED 2026-09-19** on David's approval ("ship hallucination-v8"): v8 copied to `course-assets/hallucination/hallucination.mp4` (SHA-256 verified before and after the copy, `fd1eb11f…`), v5-v8 candidates removed, `index.html` video src given cache key `?v=20260919ship1` and the pill 3 min → 4 min, the updated Why board committed with its cache key bumped and the page card heading + Markdown step 1 changed to "Learns From Training Text" to match it, `course-assets/manifest.json` entries updated. See `shipping-receipt.json`.
