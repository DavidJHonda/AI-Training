# What’s an LLM? — introductory rewrite and video candidate

The owner approved the shorter introductory lesson after checking both later coverage and prerequisites. The page now has three teaching boards: What’s an LLM?, Patterns AI Learns, and One Word at a Time. It retains the app/model distinction, training-before-use, context shaping continuations, the next-word loop, and both story activities. Detailed training mechanics and numerical probability comparisons are reserved for Understand AI.

## Website and source materials

- Stable section ID `aihistory`; title **What’s an LLM?**; current slug `whats-an-llm`.
- Renamed canonical asset folder, Markdown, group-activity folder, references and video metadata. Historical raw generations and dated audit identities are retained.
- Both Group Activities views use the updated shared entry. Directory data cache keys bumped; old asset/activity URLs have Vercel redirects, and the original root activity redirect now targets the new location.
- `lessons/whats-an-llm.md` and the fresh four-board preparation kit match the shortened page. Five upload files: one Markdown plus four JPGs, including the close. No generation was run.
- Updated page 3 of `packets/start-smarter.pdf`, preserving the other six pages. Visually inspected the revised rendered page.
- Replaced the legacy CSV question requiring the removed 41% → 2% example with a conceptual question about surrounding words changing predictions. The current final's stable questions and IDs remain supported.

## Candidate and edit plan

Candidate: `Prompts/whats-an-llm-v1.mp4`, **2:25.267**, 4,358 frames at 30 fps.

Source: approved finished `Prompts/how-an-llm-works-v17.mp4`, SHA-256 `4b19151bdce37d85c012d176dbde24f6ec60f75a806d9fc2a6cdc2e06aa7aea2`. Existing finished assembly reencoded once; no new voice or added pauses.

| Source span | Treatment |
| --- | --- |
| 0:00–0:42.433 | Keep the opening, app/engine distinction, initials and Large/Language/Model explanation. Ends after “predict a likely output.” |
| 0:42.433–1:48.600 | Remove detailed training process and its restatements. |
| 1:48.600–2:20.600 | Keep familiar patterns, broader language/problem patterns, and the transition to building an answer. Ends after “uses those patterns to build an answer.” |
| 2:20.600–3:41.667 | Remove the extra prompt setup, token aside and numerical probability comparison. |
| 3:41.667–4:52.500 | Keep phone example, complete jelly/for/lunch walkthrough and unchanged final close. |

The old numerical board stayed briefly after the narration cut. Its final 23 frames are replaced by the first frame of the retained, previously approved phone scene. This prevents the removed board flashing at the join.

| Retained board | Treatment |
| --- | --- |
| What’s an LLM? | Keep existing full-board entrance and Large/Language/Model highlights and camera treatment. |
| Patterns AI Learns | Enter the existing familiar-pattern explanation; retain its existing camera and card highlights. The earlier full-board introduction was inside the removed training passage, so this candidate enters its existing detail framing. |
| One Word at a Time | Keep phone lead-in, full-board entrance and three-panel walkthrough. |
| Closing message | Keep existing movement and literal final frame. |

The video explains growing context through the jelly/for/lunch sentence, but omits the banana/sandwich contrast and the explanation that more than one continuation can fit. The subsequent [narration evaluation](NARRATION-REVIEW.md) recommends a reroll. The original suggestion to accept this as a companion overview was too lenient: the course standard requires the video to replace the reading, preserving its essential understanding.

## Verification and limits

- Desktop and 390px mobile page verified in Chrome; no overflow or script errors.
- Three teaching boards plus close, both activities, both Group Activities views and renamed standalone activity verified.
- Targeted upload sync check and shared group-directory tests pass.
- Full candidate sequential decode: 4,358 frames. All three declared visual transition guards pass; boundary strips visually inspected.
- Fresh candidate transcript reviewed: complete retained sentences, no numerical comparison or detailed training loop. Definitions, training-before-use, familiar and broader patterns, repeated answer generation, changing context and closing lines remain.
- Cut points fall in low-level pauses (approximately −58, −91, −74 and −67 dBFS in 10ms windows). Five-millisecond fades stay inside those pauses. These measurements and the transcript are not an audible listening review.
- Listen at **0:42.4** and **1:14.4** before approving the candidate. No end-to-end audiovisual listening pass or full production certification is claimed. Review the shortened Patterns board entrance as well.
- The old source issue previously reported around 0:44.5 is inside the removed span.

The shortened candidate is **not installed, committed or published**. The current overview remains the longer approved video at its renamed canonical path, with updated title metadata and identical compressed audio/video stream hashes. The revised lesson and packet are local changes. Deployment requires a separate publishing request.
