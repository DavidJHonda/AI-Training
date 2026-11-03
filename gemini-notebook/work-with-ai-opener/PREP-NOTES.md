# Work With AI opener — voice comparison, November 2, 2026

## Result and decision

David reported generating both prompt versions and hearing no change from the voice in recent videos with either version. This is the owner's listening result; the assistant has not independently auditioned the new rolls. A Google-side change is the leading explanation, not a confirmed provider update.

Decision: keep the simpler earlier conversational-voice instruction in `PROMPT.txt` and stop tuning voice instructions for this experiment. `PROMPT-WARM.txt` is retained only as the tested comparison record. No further voice-test reroll is requested. This decision applies to this opener; other lesson prompts have not been changed.

## Completed experiment preparation

David requested both a warmer-delivery reroll and a second roll using the earlier course voice instruction. Both prompts use the same current lesson Markdown, exact required lines, teaching sequence, and boards, including Evaluate and Improve. Only their VOICE blocks differ. Keep one narrator throughout each new roll.

| Variant | Paste into customization | Words | Save raw roll as |
|---|---|---|---|
| Earlier course instruction (active default) | `PROMPT.txt` | 422 | `Prompts/work-with-ai-opener-original-voice-test-2026-11-02.mp4` |
| Warm delivery (completed test; reference only) | `PROMPT-WARM.txt` | 496 | `Prompts/work-with-ai-opener-warmth-test-2026-11-02.mp4` |

Use the next unused numbered filename if either output name is occupied. Upload exactly the same four files from `upload/` for either roll: `Opener-Work.md`, the Same Tool face-free stand-in, the current section map, and the close board. Paste the selected prompt; do not upload prompts or these notes.

The earlier instruction is reproduced exactly:

> Use a conversational voice for a high-school student meeting this lesson on its own.

Provenance: `Prompts/fake-trap-video-prompt.txt` at `40fd4b1e^`, before the September 20 rewrite. This restores the earlier course voice instruction, not an entire historical Work With AI prompt. The opener itself already used “a teacher talking to one student” by September 14 (`eb03c784`); the earlier September 20–21 date described the broader rollout, not this opener's first use. Current content and visual instructions remain in place.

The warm variant asks for patient, relaxed delivery, gentle emphasis, and natural pitch and pacing. It asks for friendliness through delivery rather than added wording and avoids clipped, stern, or announcer-like delivery.

## Comparison references

- Baseline: installed v13, `course-assets/work-with-ai-opener/work-with-ai-opener.mp4`, also retained as `Prompts/work-with-ai-opener-v13.mp4`. Shipping receipt: `video-audit/work-with-ai-opener-roadmap-v13-2026-11-02/shipping-receipt.json`; SHA-256 `cbdf8cf869beed4c5fb7400e3ab3599ba00edab7c799deb7b7a278e024e8318e`.
- Compare matching passages from the opening, camera analogy, and close with the main voice; compare Evaluate and Improve with the second voice around 1:18–1:28. Judge warmth, naturalness, clarity, pace, and exact required wording separately. The existing two voices are references, not a request for two narrators.
- Both variants were generated and compared by David, with the result recorded above. No new roll has been installed by this task; the comparison does not establish the cause of the perceived voice change.

## Historical preparation — September 29, 2026

The notes below describe earlier preparation. The current prompt, registry, and instructions above govern this reroll.

> Superseded opening requirements (2026-10-27): remove the refrain board and its opening slogan recital. The current Markdown starts “You’ve met the tool and seen what it can do.” The camera analogy now folds in giving AI a clear goal and checking its answer. Keep the map and closing lines. Current PROMPT.txt and the upload registry govern; the historical nine-line validation and opening repetition below no longer apply. Existing MP4 awaits revision.

Ready for one complete Notebook video generation. This refresh applies the current-spec evaluation in `video-audit/work-with-ai-opener-current-spec-review-2026-09-29/REVIEW.md`. The page and finished video are unchanged.

## Lesson arc

Aim, check, and collaborate → move from knowing AI to using it → identical cameras and the same sandwich show how a person's approach changes the result → preview the three parts of Work With AI → retain responsibility for the answer → repeat the two-line close.

The section map is an overview, not three miniature technical lessons. Its complete descriptions provide the bridge into the later lessons. The camera comparison explicitly keeps the tool and subject constant while changing how the photograph is taken. The map moves from selecting/learning the tool to asking well to checking the returned answer.

## Narration preparation

- Preserve the current lesson wording and the existing approved details sentence.
- Require the four opening lines, practical-use transition, details sentence, verification sentence, map takeaway, and both closing lines verbatim. The two closing lines intentionally repeat the opening.
- The verification sentence is now a separate Markdown paragraph so it cannot disappear inside the map description.
- Preserve the concrete same-phone/sandwich comparison. A photographer's cover shot remains in the source prose; exact wording of that example is not a separate hard requirement.
- Do not promise that context forces an answer, all results depend on the user, or human judgment ensures accuracy.
- Use one narrator. Rejected v9/v10 external-voice repairs are not sources for this generation.

## Board handling

Upload five files: `Opener-Work.md` plus refrain, Same Tool face-free stand-in, section map, and close JPGs. The Same Tool stand-in preserves the canonical 1600×1150 dimensions, title and takeaway while removing the panel containing visible faces. Its comparison is fully spoken in the Markdown. The other three boards have no visible faces and are uploaded directly. All assets were visually inspected, including the section map during the current-spec review.

Insert the original `course-assets/work-with-ai-opener/work-with-ai-opener-same-tool.jpg` during editing. Upload rules for faces are separate from the allowance for illustrated people in generated scenes.

Request useful drawings and animations, including the camera comparison and checking an answer. Do not show a context-to-model arrow ending in a certified answer or accuracy percentage. Preserve effective generated sequences during the later edit; replace actual course-board recreations with the canonical JPGs. No new illustration is generated for this prep task.

## Handoff and validation

- Editable prompt: `PROMPT.txt`, 472 words, four required blocks in order.
- Narration source: `lessons/Opener-Work.md`.
- Registry: `gemini-notebook/upload-sets.json`, entry `work-with-ai-opener`.
- Upload only `upload/` contents. Paste the prompt into customization; do not upload the prompt, notes, or README.
- Save the raw roll as `Prompts/work-with-ai-opener-reroll.mp4`; if that name has become occupied, use the next unused numbered reroll name.
- Compare the returned narration with the hash-pinned original from the evaluation before choosing a replacement base or donor passages. Audition any proposed joins.

Validation: all nine distinct required sentences occur as standalone Markdown lines and quoted prompt requirements; opening/closing repetition retained; prompt below 500 words; faceless/canonical dimensions match; upload copy hashes and registry synchronization checked with `sync_gemini_notebook.py --lesson work-with-ai-opener --check`.

No generation, edit build, publication, or listening approval is claimed by preparation. Exact board/ring timing follows the selected narration. The existing board plan remains in the evaluation; no blanket pauses or additional cutaways are requested.
