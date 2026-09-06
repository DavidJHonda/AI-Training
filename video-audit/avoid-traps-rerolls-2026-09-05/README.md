# Avoid Traps — six new video evaluations

Evaluated September 5, 2026. No videos, lesson content, prompts, or production assets changed.

| Video | Source runtime | Recommendation | Main consideration |
|---|---:|---|---|
| [Hallucination](hallucination-review.md) | 3:21 | Repair | Strong examples; remove absolute claims and the invented “intuition trigger” framing. |
| [Training Bias](training-bias-review.md) | 4:34 | Repair | Complete teaching; remove the unsupported diagnosis of Claude’s cutoff. |
| [Document Trap](document-trap-review.md) | 4:20 | Repair, with a qualification | Strong explanation and practical moves; distinguish long-document retrieval from all uploads. |
| [Mind Trap](mind-trap-review.md) | 4:19 | Repair, with a heavier editorial pass | Core message survives; restore the concrete college comparison visually and remove contradictory/abstract claims. |
| [Flattery Trap](flattery-trap-review.md) | 4:44 | Reroll recommended | First four practical moves are rushed, alongside several promises that prompting can eliminate the problem. |
| [Engagement Trap](engagement-trap-review.md) | 4:43 | Repair | Good lesson; tighten repeated explanations and replace misleading incidental teaching graphics. |

## Review basis and limits

Read the current lesson text and current lesson board references in `index.html`; reviewed full timestamped narration transcripts, all 35 sampled contact sheets, scene/hold diagnostics, and the illustrated boards that may need to be inserted. Selected technical and historical claims were cross-checked against primary sources linked in the individual reviews.

These are teaching/content evaluations, not final audiovisual QC certifications. Narration was assessed from speech-recognition transcripts; exact wording at proposed cut boundaries must be confirmed during editing. Contact sheets sample frames and cannot prove that no one-frame flashes exist. No claim is made that breaths, clicks, pronunciation, or every transition have passed a listening/frame-by-frame check.

All timestamps refer to the untouched uploads in `Prompts`, not any future patched timeline. Ranges identify passages to review, not frame-accurate edit instructions. Source naming is `Hallucination.mp4` and `engagement-trap.mp4` (the latter resolves the request’s “engagment-trap”).

Notebook highlighting is expected raw material and does not count against these videos or justify a reroll. Board replacement and the standard closing treatment are routine post-production work, separate from the numbered teaching concerns.

## Instructions for the later repair pass

- Preserve useful generated footage between current lesson boards; do not automatically cover an entire long narration passage with a single illustration.
- Insert exact current lesson boards, including illustrated versions where the narration supports their teaching. Use full-card/full-bubble/full-banner boundaries, locked accent colors, and cameras derived from the same measured bounds.
- Choose visual boundaries separately from narration boundaries. Replacement coverage must include the complete unwanted shot, including its transition frames.
- Record every splice on the final output timeline; run `transition_guard.py` and inspect its every-frame boundary strips. Then review audio around every cut for complete words, natural breaths, and continuity.
- End on the current standard close. None of these raw uploads is approved to ship unchanged.
