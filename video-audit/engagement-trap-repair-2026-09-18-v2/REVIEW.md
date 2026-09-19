# Engagement Trap repair v2

Status: review candidate only. The live lesson video, `index.html`, lesson Markdown, donors, and course board assets were not modified.

- Candidate: `Prompts/engagement-trap-v2.mp4`
- SHA-256: `8680dea74930020015041167219ff627e6c7ac22175f8e46813db51064a8d102`
- Runtime: 7,748 frames at 30 fps (4:18.267)
- Canvas: 1280×720

## Narration repairs

1. Half-million estimate
   - Donor: `Prompts/engagement-trap-1.mp4`, 2:13.500–2:22.800 (f4005–f4284)
   - Replaces live: 2:37.000–2:45.700 (f4710–f4971)
   - Output spoken interval: 2:37.140–2:45.700
   - Complete passage: “Raskin later regretted what this design became. By his own estimate, the Infinite Scroll now consumes half a million human lifetimes every single month.”
   - A 0.400-second matched-room-tone insert follows the donor. Final strict silence is 0.755 seconds (2:46.123–2:46.878), against the approved 0.75-second target.

2. Business-incentive explanation
   - Donor: `Prompts/engagement-trap-2.mp4`, 2:56.900–3:20.200 (f5307–f6006)
   - Replaces live: 3:07.000–3:18.200 (f5610–f5946)
   - Output spoken interval: 3:08.400–3:31.020
   - The four approved sentences run through “Helpful follow-up offers facilitate that transition smoothly.” The next donor sentence, which overstates platform intent, is excluded.
   - A 0.367-second matched-room-tone insert precedes the donor. Final strict silence is 0.754 seconds (3:07.868–3:08.622), against the approved 0.75-second target.

3. Exact close
   - Donor: `Prompts/engagement-trap-2.mp4`, 3:48.967–3:52.900 (f6869–f6987)
   - Replaces live from 3:54.200 through the end
   - Output spoken interval: 4:07.960–4:11.080
   - Complete passage: “Know what you came for. When you have it, choose what happens next.”
   - The close uses the current canonical JPG with the 48-frame hold, 150-frame push, and 120-frame settled hold.

Every audio seam uses a 5 ms transition through measured room tone. Encoded-sample jumps at the eight audio boundaries range from 1 to 36 PCM units; none exceeds its local waveform variation. Donor/live integrated-loudness differences stay within 1.44 LU of the adjacent passage.

## Visual treatment

- The first “One Answer. Two Endings.” entry now shows the complete canonical board for 60 frames, then cuts to a clean top-chat crop with the full AI answer and its ring. No outcome-card fragments are visible.
- The scroll board’s existing left/right treatment is retained; its takeaway-ring frame holds under the half-million passage.
- Candidate 2’s unsupported metric graphics are not used. The existing live phone/person sequence is evenly retimed under the longer business explanation.
- The live “AI Won’t Quit for You” board and its banner highlight remain intact.
- The canonical close is the final picture.

## QA

- Full encoded transcript reviewed: all three donor passages are complete; the rejected candidate-2 sentence is absent; the live “not inherently malicious” qualification remains.
- Six four-second contact sheets inspected across the full runtime.
- Eight transition strips inspected frame by frame. `transition_guard.py`: PASS, 8/8.
- The v1 review render exposed a three-frame old-board island after graft 1. V2 advances the destination drawing over those silent shoulder frames; the island is gone.
- Source protection: PASS, 9/9 hashes unchanged.

## Remaining human check

I could not perform an acoustic headphone audition or continuous real-time playback in this environment. Before shipping, David should listen through the joins at 2:37, 2:46.9, 3:08.4, 3:31.7, and 4:08 for voice/delivery continuity and natural pacing. Automated transcript, loudness, silence, waveform, frame-count, contact-sheet, and transition checks pass.
