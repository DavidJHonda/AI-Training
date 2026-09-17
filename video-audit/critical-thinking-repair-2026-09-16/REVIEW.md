# Critical Thinking — repaired review candidate

## Recommendation

**KEEP after a short human audio-seam listen.** The repaired candidate now carries the lesson's essential teaching accurately and completely, including the corrected wording for Habits 4 and 5. The full visual pass, frame-exact transition guard, decode check, protected-file check, and finished-video transcription all pass.

Direct audio playback was not available in this runtime. The candidate is therefore a review artifact, not a publishing recommendation, until the short windows under **Required human listen** have been heard.

## Output

- Candidate: `Prompts/critical-thinking-v3.mp4`
- SHA-256: `6eea25197bc27b95bce3fb4647327ed48a3dece7a4f11e39bdc41d15a102cf60`
- Format: 1280×720, 30 fps, H.264 video, AAC mono at 48 kHz
- Exact decode: 5,938 frames / 3:17.93
- Live course video, source rerolls, `index.html`, lesson Markdown, prompt, upload checklist, and canonical boards: unchanged
- Publishing/deployment: not performed

## Assembly

| Output passage | Source | Treatment |
|---|---|---|
| 0:00.00–0:46.73 | reroll 4 | Canonical “What You Know. How You Think.” board with synced rings |
| 0:46.73–0:47.23 | matched room tone | Approved half-second pause after “for a claim to hold up” |
| 0:47.23–0:57.00 | reroll 4 audio + reroll 3 picture | Hand-drawn newspaper/headline sequence replaces the stock chocolate photograph |
| 0:57.00–1:17.17 | reroll 4 | Canonical “Same Claim. Different Thinking.” board; full establish, complete-card views, full takeaway |
| 1:17.17–2:06.37 | reroll 4 | Study-design, sample-size, website, journalist, and confirmation-bias drawings |
| 2:06.37–2:06.87 | matched room tone | Approved half-second pause after “confirmation bias” |
| 2:06.87–2:37.17 | reroll 4 | Canonical Five Habits board through Habit 3 |
| 2:37.17–2:54.27 | reroll 3 audio | Corrected Habits 4–5 passage under the canonical Five Habits board; −0.4 dB level match |
| 2:54.27–3:01.47 | reroll 4 | Full-board summary through applying the five questions to AI |
| 3:01.47–3:02.27 | reroll 4 | AI laptop drawing |
| 3:02.27–3:09.23 | reroll 4 audio + reroll 3 picture | Accurate AI decision diagram replaces the inaccurate lorem-style paper |
| 3:09.23–3:13.93 | reroll 4 | Exact two-line close under the canonical close board |
| 3:13.93–3:17.93 | generated hold | Settled canonical close; literal final frame |

## Narration findings

- The finished-video medium English transcript contains all of the lesson's essential teaching, worked example, distinctions, and conclusion.
- It preserves the hard lines “Be smarter than the tool,” “Slim by Chocolate,” “Sounds great. I believe it,” “Wait, what's behind the claim?”, the chance-result explanation, and the AI find/repeat distinction.
- Habit 4 now says: “Determine if your belief is based on the evidence, the confident wording, or simply what you want to believe.”
- Habit 5 now says: “Decide what to believe or do, and remember that you can change your mind when you learn more.”
- The exact close is present: “AI amplifies whatever you bring to it. Good thinking in, sharper output.”
- The finished transcript measures 0.86 seconds between “hold up” and “In 2015,” and 0.94 seconds between “confirmation bias” and “This board,” reflecting the two selective half-second room-tone insertions plus the source delivery.
- The corrected donor block enters after a 0.72-second transcript gap following Habit 3 and exits into a 0.78-second gap before “These five questions”; acoustic review classified both as breath/room sound rather than digital silence.

No further narration replacement or reroll is recommended from the transcript and waveform evidence.

## Visual and production notes

- Every lesson board is the current canonical JPG; no Notebook-rendered board survives.
- Board 1 remains readable in a complete full view while rings follow Knowledge, Critical Thinking, Better Questions + Better Decisions, and the takeaway.
- Boards 2 and 3 establish the whole board, move to complete-card views, and return to the full takeaway.
- Reroll 3's illustrated newspaper/headline replaces reroll 4's stock chocolate photograph.
- Reroll 3's accurate AI decision diagram replaces reroll 4's inaccurate lorem-style page.
- The Notebook engine mark was cleaned on 2,002 retained or borrowed frames: 1,558 cloned and 444 inpainted, with no declined frames.
- The Gemini outro is gone. The canonical close is the literal final frame at the prescribed settled size.
- Transition guard: **PASS, 12/12 declared boundaries**, with no short stale-frame islands.
- Whole-video visual contact-sheet review: **PASS**.
- Decoder and planned-count check: **PASS**, 5,938/5,938 frames.

## Required human listen before publishing

Listen at normal volume, preferably on headphones:

1. **0:45.8–0:48.2** — confirm the half-second pause after “hold up” feels deliberate and that “In 2015” begins cleanly.
2. **2:05.5–2:07.8** — confirm the half-second pause after “confirmation bias” and the entry into “This board outlines five habits.”
3. **2:36.2–2:38.3** — reroll 4 into reroll 3 at the Habit 4 graft; check for a click, clipped consonant, or voice-level jump.
4. **2:53.3–2:55.3** — reroll 3 back into reroll 4 before “These five questions”; check the breath and voice match.
5. **3:08.4–3:14.3** — transition into the exact two-line close and its initial tail.

If those five windows sound clean, the candidate merits a final **KEEP**. If a seam is audible, repair that exact join; do not reroll the lesson.

## Provenance

- Reroll 4 SHA-256: `91a35ac09aeb1bdc43fd33eac553df5ab62159a1a28e806bfb3d91f12ab01213`
- Reroll 3 SHA-256: `42eec2dd26866ccb2dfe63bfd935c3557e8c43a78b5ccb3bc636c650e9f7213d`
- Lesson Markdown SHA-256: `53e7901f5e36c55f8e731c424915f31608b24424b7338dc33d5a1ad8947bc69c`
- `index.html` SHA-256: `44ec998a1ebd82bcc8ef49b0b16fdcdbf118511173d6c32b2d20096cabb625a4`
- Donor audio: reroll 3 frames 4,604–5,117 (2:33.47–2:50.57)
- Replaced base audio: reroll 4 frames 4,685–5,221 (2:36.17–2:54.03)

See `edit-manifest.json` for the frame-exact timeline, board geometry, source hashes, graft metadata, room-tone source, close plan, and protected-file verification. See `transition-guard/`, `full-pass/`, `states-*.jpg`, `final-frame.jpg`, `transcript/`, and `audio-gap-review/` for QA evidence.

## Reproduction and QA commands

```bash
PYTHONDONTWRITEBYTECODE=1 .video-venv/bin/python scripts/video/build_critical_thinking_review.py --prepare-only
PYTHONDONTWRITEBYTECODE=1 .video-venv/bin/python scripts/video/build_critical_thinking_review.py --reuse-prepared
bash scripts/video/ffmpeg.sh -v error -i Prompts/critical-thinking-v3.mp4 -map 0:v:0 -map 0:a:0 -f null /dev/null
.video-venv/bin/python scripts/video/transition_guard.py Prompts/critical-thinking-v3.mp4 --boundary 1402:pause-one --boundary 1417:newspaper --boundary 1710:board-two --boundary 2315:study --boundary 3791:pause-two --boundary 3806:board-three --boundary 4715:habits-graft-in --boundary 5228:habits-graft-out --boundary 5444:laptop --boundary 5468:ai-diagram --boundary 5677:close --boundary 5818:close-tail --outdir video-audit/critical-thinking-repair-2026-09-16/transition-guard
.video-venv/bin/python scripts/video/frames.py Prompts/critical-thinking-v3.mp4 video-audit/critical-thinking-repair-2026-09-16/full-pass --sheet
.video-venv/bin/python scripts/video/transcribe_selected_videos.py Prompts/critical-thinking-v3.mp4 --output-dir video-audit/critical-thinking-repair-2026-09-16/transcript --model medium.en
```
