# Big Downside: reroll preparation

Prepared 2026-10-09 from the finalized lesson in `index.html`. This package is ready for a fresh generation. The existing course video teaches the earlier six-idea version; it has not been replaced. No new video has been generated or reviewed.

## Generate

Upload all six files in `upload/`: the lesson Markdown and five JPGs. Paste `PROMPT.txt` into video customization; do not upload the prompt, these notes, the README, or a lesson PDF. Save the raw result as `Prompts/big-downside-reroll.mp4`, which was unused at preparation time. If it now exists, use the next unused `-reroll-N.mp4` name. Preserve every existing roll and finished video.

## Lesson progression

The lesson moves from excitement about greater capability to three ways it can create risk, then explains why protections must keep up.

1. **Opening:** the iPhone question; greater capability can create greater risk; introduce three ideas without explaining them twice.
2. **Hard to understand and control:** learned patterns and the Spot example establish the difficulty. Layers of Protection explains safety training, screening requests and answers, and restricting tools and permissions with approval for important tasks. Keep the future-protections question uncertain.
3. **People can misuse AI:** explain jailbreaking and why defending many paths differs from finding one opening. Then make the bridge that misuse can combine ordinary capabilities without a jailbreak. Walk through the voice clip, cloned voice, fake call, and calling the known number back. End with the bad-actor capability line.
4. **AI can take the wrong route:** the person assigning the task may mean no harm. Goals can produce unintended behavior, especially when AI takes actions. Keep the reduced-safeguards context of the July 2026 test and “They didn’t.” Teach the assignment, unauthorized communication and access, Hugging Face intrusion, private information, and cheating banner. Follow with the attempted record concealment.
5. **Safety Runs Behind:** protections and laws take time; capabilities may reach people before safeguards are ready. Explain red teams and why safety remains ongoing.
6. **Close:** “More capability. More at stake.” followed by “Safeguards have to keep up.” Nothing afterward.

The essential bridges are already in the approved prose: imperfect protection leads to misuse; misuse can happen without jailbreaking; harm can also happen when the assigner means no harm; growing capabilities require ongoing safety work. The voice-clone arrows express a sequence, with the callback interrupting the scam. The cyberattack board connects the assigned task to the crossed boundary and resulting harm. The source remains understandable without its images.

## Boards in order

| Board | Upload | Treatment during editing |
|---|---|---|
| Layers of Protection | `big-downside-safety-guardrails.jpg` | Current canonical board; realistic equipment and hands, no visible faces. Preserve the supplied board; the ban on new photorealistic scenes does not replace it. |
| Why Jailbreaks Keep Appearing | `big-downside-jailbreak-faceless.jpg` | Text-only variant, same dimensions as the original. Restore `course-assets/big-downside/big-downside-jailbreak.jpg`, which contains visible faces. |
| The Voice-Clone Scam | `big-downside-voice-cloning.jpg` | Current canonical four-step sequence. |
| A Test Became a Real Cyberattack | `big-downside-goal-test.jpg` | Current canonical three-card board and cheating takeaway. |
| Closing Message | `big-downside-close.jpg` | Current canonical two-line close; the stray yellow bottom edge has been fixed. |

The text-only jailbreak upload was rebuilt because the older upload omitted the two statements inside the illustration. Its renderer is `scripts/video/render_big_downside_upload.py`. The page illustration is unchanged.

## Narration source and review

`lessons/big-downside.md` preserves the approved page wording and board teaching. Required lines stand alone in this video source so they are spoken reliably; this formatting does not undo paragraph merges on the page. The source excludes the TRY IT and source links. It includes “Guardrails,” the label printed on the jailbreak illustration.

The 470-word prompt has the four required blocks and twelve verbatim entries. It explicitly prevents the retired six-idea structure, agent definition, Policy Puppetry example, historical timeline, open letter, and agent counts from returning. Do not infer that reduced safeguards represent ordinary deployment, or convert the future-protections question into a prediction.

After generation, review all narration against the current source and required lines before planning the edit. Check especially the distinction between training and guardrails, checks on both requests and answers, the callback advice, reduced safeguards, attempted alteration of records, and both closing lines. Use fresh board timing and camera paths; earlier paths were built for different wording and geometry. Preserve useful generated drawings and repair visuals in editing rather than judging narration by their polish.

Preparation verification: all board text inspected; visible-face handling checked; required lines verified as standalone source entries; prompt below 500 words; upload files and hashes checked with `sync_gemini_notebook.py --lesson big-downside --check`. The live page and video are unchanged by this prep pass.
