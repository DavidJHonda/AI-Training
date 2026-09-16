# Evaluate the Results — repaired review candidate

## Recommendation

**SHIPPED 2026-09-16** on David's approval ("Evaluate-the-results-v5. Ship it."): copied to `course-assets/evaluate-the-results/evaluate-the-results.mp4` (sha256 0e138f7381612f07…), cache key 20260916ship1, duration pill 5 min → 4 min (4:17); candidates v1–v5 removed from Prompts/. Original recommendation: **KEEP after a short human audio-seam listen.** The repaired candidate now carries the lesson's essential teaching completely and accurately in the transcript, while the visual treatment passes the declared splice and endpoint checks. Direct audio playback was not available in this runtime, so the candidate is not marked ready to publish until the joins listed below have been heard.

## Output

- Candidate: `Prompts/evaluate-the-results-v5.mp4`
- SHA-256: `0e138f7381612f07287636c95549cc5d653dcae2c1521c9db2f7a50e69e57a9a`
- Format: 1280×720, 30 fps, H.264 video, AAC mono at 48 kHz
- Exact decode: 7,708 frames / 4:16.93
- Live course video, source rolls, lesson Markdown, `index.html`, and canonical boards: unchanged
- Publishing/deployment: not performed

## Best-of assembly

| Output passage | Donor | Source passage | Treatment |
|---|---|---|---|
| 0:00.00–0:42.50 | version 2 | 0:00.00–0:42.50 | Full A/V opening; +1.1 dB |
| 0:42.50–3:15.70 | version 1 | Quick Pass through Use It | Framework spine with current canonical boards |
| 3:15.70–3:24.07 | version 2 | 2:09.12–2:17.50 | Complete Fix It narration; +3.0 dB; retained Move board |
| 3:24.07–3:38.30 | version 1 | Walk Away and takeaway | Framework spine |
| 3:38.30–4:05.73 | version 2 | 2:35.08–3:02.50 | Complete scholarship example and evidence conclusion; +2.2 dB; current Check Before You Use board |
| 4:05.73–4:05.80 | room tone | — | Two-frame cleanup replacing the donor's stray next-narration onset; scholarship board holds |
| 4:05.80–4:06.80 | room tone | — | One-second pause; canonical closing board begins immediately |
| 4:06.80–4:12.93 | version 1 | 3:36.40–3:42.52 | Exact closing reminder |
| 4:12.93–4:16.93 | generated hold | — | Settled canonical close frame |

One deliberate one-second pause was inserted after “proof,” as requested. All other timing retains the natural source gaps and 5 ms audio crossfades.

## Narration findings

- The repaired opening ends cleanly after “grade its homework,” then begins “This is the quick pass.” The earlier leaked “Let—” is gone.
- Quick Pass fully teaches Read, Understand, and Validate, including responsibility for forwarded information and checking against knowledge and the original prompt.
- Decide preserves the three distinctions: ability to judge the output, the task's success criteria, and risk/stakes.
- Dig preserves the complete checking toolkit: open sources, challenge the answer, ask what is missing, search current information, and independently calculate/test/consult an expert.
- Move now contains the complete Fix It guidance: “Instruct the AI on what needs to change or edit the text yourself and check the revision before applying it.” It then transitions cleanly to “Finally, if the AI is proving unhelpful…”; the earlier extra “Or” is gone.
- The worked example now explicitly names both the official webpage and the school calendar, notes that both say February 15, and concludes that an AI answer is a claim requiring proof.
- After “proof,” the closing board appears at 4:05.80 and holds under room tone for exactly 30 frames before the retained closing-narration segment begins at 4:06.80.
- Version 4 exposed a short donor-audio onset at approximately 4:05.8. Version 5 removes the final two donor frames and replaces them with matched room tone, without changing the closing-board timing. In the 4:05.70–4:05.90 window, the peak fell from **−1.4 dB** in v4 to **−49.5 dB** in v5; the comparison waveform no longer contains the transient.
- The final ASR pass confirms the closing sequence is “The tool answers, you evaluate. Read. Understand. Validate.” Human listening remains the authority for delivery and seam quality.

Transcript verdict: all essential lesson teaching, examples, distinctions, and conclusions are represented. No narration replacement is currently recommended.

## Visual and production notes

- Current canonical lesson boards are used throughout.
- Compact boards remain in full view and highlight complete cards with 5 px rings.
- Dense Dig and scholarship boards establish the whole board, move to complete-card/panel views, and return to the full takeaway.
- The standard canonical close is the literal final frame.
- Transition guard: **PASS, 11/11 declared boundaries**, with 7,708 decoded frames and no short visual islands. The extra boundary covers the two-frame clean room-tone tail before the example-to-close-board transition.
- No suitable narration-matched Notebook drawing existed inside the long framework run, so the approved board-led treatment was preserved.

## Required human listen before publishing

Listen to these short windows at normal volume and on headphones if possible:

1. **0:40–0:45** — version 2 opening into version 1 Quick Pass.
2. **3:14–3:26** — version 1 → version 2 Fix It → version 1 Walk Away, including voice-level matching.
3. **3:36–3:41** — version 1 framework into the version 2 scholarship example.
4. **4:04–4:14** — confirm the new one-second pause after “proof,” the immediate switch to the closing board, and “Read. Understand. Validate.”

If those four windows sound clean, this candidate should replace the two-roll alternatives for review. If any join is audible, repair that exact join rather than rerolling the lesson.

## Provenance

- Version 1 SHA-256: `ab302d2c330058af33c9dcc730ebd56dbc3f17267bab40264851e9ae4778ab4f`
- Version 2 SHA-256: `f446fdb042b66a670529c2c17c27abd5309ace37bb6f367610a13336a5b5796d`
- Lesson Markdown SHA-256: `904b02fc3c2df988f499bff5cf8ed5c64a958c9d0c802f6b324b7372dbadc2a2`
- `index.html` SHA-256 at the start of the v4 build: `823f393a49b8070787ebe0b351d05850525452282c598582846861d4d0778752`

See `edit-manifest.json` for the frame-exact timeline, source hashes, board geometry, graft metadata, and protected-file verification. See `transitions-v5/transition-guard.md` and its contact sheets for boundary evidence.
