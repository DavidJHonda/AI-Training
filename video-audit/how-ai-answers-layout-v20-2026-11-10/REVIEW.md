# How AI Answers v20 — visual revision

Review candidate: `Prompts/how-ai-answers-v20.mp4` (155.367 seconds, 4661 frames, 1280×720, 30 fps).

The demonstration beginning at 0:59.2 now uses the actual lesson components: both white panels inside the blue GuidedDemoShell, including question, growing answer, instructions, controls, and choices. All four demonstration states use the same layout. Spoken-choice highlights follow the captured DOM geometry.

The completed-answer-only flash at 2:26.067–2:26.767 is removed. The finishing animation holds until the existing closing board begins. No duration or narration changes.

Pictures were rendered from the pristine roll-2 source using the v19 composition, with only the requested replacements. Audio was copied directly from v19; extracted AAC hashes match exactly. The lesson, installed course video, source recordings, canonical board assets, and v19 remain unchanged.

Verification: all 4661 frames and audio decode; 31 encoded states agree with prepared frames (maximum mean absolute pixel error 3.16); 94 samples outside changed scenes agree with v19 (maximum error 0.151); all 13 transition guards pass. Captured layout, encoded choice highlights, selected-token emphasis, and ending transition were visually inspected. Direct listening and uninterrupted playback were not performed; audio is unchanged from v19.

The context concept is already narrated at approximately 1:28: the updated vector reflects “your question and the reply so far.” At approximately 1:45, each added token becomes part of the context. Suggested future clarification, not inserted in this visual revision: “The last token’s updated vector reflects both your question and everything AI has written so far.”

This is a review candidate; no course installation, commit, or push was performed.
