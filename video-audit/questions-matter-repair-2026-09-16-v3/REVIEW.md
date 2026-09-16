# Questions Matter — v3 build review

## Status

- Candidate: `Prompts/questions-matter-v3.mp4`
- Build status: review candidate only; not published and not copied over the live lesson video.
- Narration-content verdict: **KEEP**. The exact assembled export was retranscribed in full and retains the lesson's complete teaching sequence, examples, distinctions, and conclusion.
- Picture verdict: **KEEP**. The complete sampled progression, all declared boundaries, board states, and literal final frame passed visual inspection.
- Remaining gate: David should listen to the complete export once, with special attention to the two audio grafts and the post-cut closing transition. This environment did not provide direct audible playback, so delivery, timbre matching, and join naturalness were not personally heard.

## Editorial construction

- Primary narration/edit: `Prompts/questions-matter-2.mp4`
- Donor narration: `Prompts/questions-matter-1.mp4`
- Roll 1 opening graft: source frames 226–575 (about 00:07.53–00:19.17), spoken passage beginning “For decades, technology has steadily reduced the friction of getting answers…” and ending “…framing the actual question.”
- Roll 1 value-shift graft: source frames 1752–2429 (about 00:58.40–01:20.97), beginning “But that does not make human effort less valuable…” and ending “Questions didn’t.”
- Removed from roll 2: source frames 6128–6425 (about 03:24.27–03:34.17), including the jargon-heavy “parameters wide open” passage.
- Preserved the natural 22-frame / 0.733-second gap after the final worked example; no automatic one-second pauses were added.
- Roll 1 graft audio received +0.6 dB gain to match the base narration's measured whole-file level.

## Visual treatment

- Replaced the three answer-speed sections with the canonical compact course board and timed rings for Library, Search, AI, and the takeaway.
- Replaced the value-shift section with the canonical compact board and timed rings for Pre-AI, With AI, and the takeaway.
- Used both canonical “Four Qualities” boards, first established at full view and then zoomed to complete cards for Open-Minded, Specific, On Target, and Open-Ended.
- Retained the useful Notebook drawings for the Socratic method, scientific method, leading-question comparison, basketball example, root-cause example, and debate example.
- Covered the Socrates stock-bust photograph with the preceding hand-drawn Socrates scene.
- Replaced the generated outro with the standard unmarked course close: “Answers got cheap. Questions didn’t.” / “Frame the problem. Ask the next better question.”
- Corner-mark cleanup: 2,679 cloned frames, 98 inpainted frames, 0 declined frames.

## Verification

- Output: 1280×720, 30 fps, 48 kHz mono AAC.
- Planned frames: 6,688.
- Metadata frames: 6,688.
- Decoded frames: 6,688.
- Duration: 222.933 seconds.
- Candidate SHA-256: `36dc8dd531d26d1f1afe4fe3e4505bc0c5fd562771bf034c3457f6b9d55a4487`.
- Source SHA-256 (`questions-matter-1.mp4`): `e6f5f3b1541208651f7c6b0ee79069a76a66c291981750c6266a20899c32d58f`.
- Source SHA-256 (`questions-matter-2.mp4`): `bd7fb1dc1a96ec40f6a5f744c9a6a627b1be486e48f73fdab35cd8a9ba301bcb`.
- Transition guard: 16/16 declared boundaries passed; every generated boundary strip was visually inspected.
- Final silence measurement: 00:03:32.864–00:03:33.600, duration 0.737 seconds at a −42 dB threshold.
- Exact-export transcript: 617 words. It contains both intended donor passages, omits the removed jargon passage, and ends with the complete two-line close.
- Five whole-video contact sheets were visually inspected. No uncovered stock photograph, engine-logo tail, malformed board, clipped ring, or unexpected final frame was found.
- Protected sources, lesson materials, canonical board assets, and the live lesson video were hash-checked and left unchanged.

## Listening checkpoints

1. Around 00:07.83: base opening into the roll 1 conceptual bridge.
2. Around 00:19.47: roll 1 bridge back into “In the library era…”
3. Around 01:03.53: base narration into the roll 1 value-shift passage.
4. Around 01:26.10: roll 1 value shift back into “Asking good questions…”
5. Around 03:32.87–03:38.82: preserved pause, cut past the removed jargon, and both closing lines.

Supporting artifacts are in this directory: `edit-manifest.json`, `transcript/`, `transition-guard/`, `final-sheets/`, board state sheets, and `final-frame.jpg`.
