# Where AI Works Best — repaired review candidate v5

## Recommendation

**KEEP for owner playback review. Do not ship without approval.**

Candidate: `Prompts/where-ai-works-best-v5.mp4`

- SHA-256: `d78374c18c64548f639a6d7258bd98b877a3ce6a4b17ba05637b466fe4a18592`
- 1280×720, 30 fps, 7,861 decoded frames, 4:22.03
- Base: `Prompts/where-ai-works-best-1.mp4`
- Donor: `Prompts/where-ai-works-best-2.mp4` for the exact final line only
- Build: `scripts/video/build_where_ai_works_best_v3.py`
- Manifest: `edit-manifest.json`

## Owner-directed changes from v4

- Removed the spoken takeaway-banner beat from all four individual strength boards.
- Removed all four takeaway-banner highlight rings. The sentence remains unhighlighted as part of each static board asset.
- Cut the six-format list after “more examples of human output than a person could process in a lifetime.”
- Resumed at “Because it has seen so many variations…”
- Replaced the outgoing formats-card picture at that join with the already-formed **Pattern Recognition: Standard Structural Templates** graphic. The formats card and its dissolve never appear.

The five removed source spans are frame-exact in the manifest. Together they shorten v4 by 456 frames, or 15.20 seconds.

## Narration findings

Verdict on the exact v5 candidate: **KEEP**.

Small.en transcription of the finished file confirms that none of these deleted banner lines remains:

- “Your material. A more useful form.”
- “More possibilities. You choose the direction.”
- “A lot to read. A clearer place to focus.”
- “Work through the pieces. Make your own call.”

It also confirms the requested later join:

- 3:37.58–3:42.96 — “During training, it read more examples of human output than a person could process in a lifetime.”
- 3:43.36 onward — “Because it has seen so many variations, it recognizes the standard layout…”

The 0.40-second interval between “lifetime” and “Because” is natural source silence, not an added one-second pause. The exact final line, “Can try is not built for,” remains at 4:16.14–4:17.86.

## Visual and production notes

- Strength boards retain rings only for **why it fits**, **what it does**, and the complete **examples** section. Each examples ring remains until the board cuts to the next section; no banner ring is generated.
- At the “Because…” join, every inspected post-cut frame belongs to the pattern-recognition graphic. There is no frame from the removed formats card or its fade-out.
- The standard close remains the literal final frame, followed by 4.09 seconds of settled room tone.
- Engine-corner treatment: 1,212 cloned frames, 450 inpainted frames, zero declined frames.

## Verification and limits

- Full decode completed: 7,861/7,861 planned frames.
- All 12 declared visual boundaries passed `transition_guard.py`; every new deletion seam was manually inspected in its every-frame strip.
- Full-runtime four-second contact sheets were inspected. They show the expected teaching sequence and no formats-card flash.
- Full-file small.en transcription completed with 743 words and confirms all requested deletions and the “Because…” restart.
- Silence detection confirms short natural gaps at the deletion seams and no automatic one-second pauses.
- Protected raw rolls, live lesson video, lesson Markdown, and current board assets all match their pre-build hashes.
- I could not hear the final v5 continuously in this environment. Wording and seam timing were verified from the exact rendered audio using transcription and silence analysis, but owner listening remains the subjective cadence/click check.
- The candidate is review-stage only. The canonical lesson video, `index.html`, lesson Markdown, and deployment were not changed by this build.

