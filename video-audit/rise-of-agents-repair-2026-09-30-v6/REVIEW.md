# Rise of Agents repaired review candidate

**Built:** `Prompts/rise-of-agents-v6.mp4`, **2:56.63**, 5,299 frames at 30 fps, 1280×720. Ready for the owner's review; not installed, committed, or published.

**Approved scope:** remove the withdrawn Gemini deletion example from the video, lesson and Rogue Agents board; correct PocketOS animation labels; preserve the approved opening, basketball example, agent loop and close. User approved the repair plan with “Build it please.”

## Changes

- Removed source **2:27.133–2:38.300** (335 frames, 11.167 seconds): the Gemini example and apology. The new join is at output **2:27.133**: “…I violated every principle I was given.” → “You can never expect an agent to safely navigate poorly defined constraints on its own.”
- Replaced both appearances of the canonical Rogue Agents board with a single PocketOS case, retaining the course's existing database illustration. The new board uses the native course typography and a full, unmarked view on entry. Its quotation receives a fixed 4 px outline on the spoken quotation introduction.
- At **2:09.50–2:22.77**, preserved the Notebook agent, key, server, trash animation, and scene sequence. Replaced the unsupported `403` with **Permission problem**, the invented filename with **Key found / Broad access**, the shell command and total-purge claim with **Deletion request / Database and backups**, and the zero-byte claim with **Database deleted**.
- Updated only the Rise of Agents content in `index.html`, lesson Markdown, prompt, upload registry note, generated upload bundle, and section kit. The local board cache key is now `20260930correction1`. The lesson's MP4 reference remains `20260924ship1` pending separate shipping approval.
- The first render, v5, exposed small text fragments when restoring the moving key over its label. v6 isolates the key's connected component to fix that artifact. v6 was rebuilt from the original finished source, not from v5.

The withdrawn Gemini claim and PocketOS mechanism were verified during the evaluation against the [original reporter's correction](https://github.com/google-gemini/gemini-cli/issues/4586#issuecomment-3125818690) and [Railway's account](https://blog.railway.com/p/your-ai-wants-to-nuke-your-database). The detailed source review remains in `video-audit/rise-of-agents-live-review-2026-09-30/REVIEW.md`.

## Output timing and board treatment

| Output span | Treatment |
|---|---|
| 0:00–2:01.10 | Retained source pictures and narration |
| 2:01.10–2:09.50 | Corrected canonical Rogue Agents board, full view, unmarked |
| 2:09.50–2:22.77 | Original PocketOS animation with targeted label corrections |
| 2:22.77–2:27.47 | Corrected board; quotation outlined from 2:22.87; continuous board through audio join |
| 2:27.47–2:47.00 | Retained goal warning, human-review rule and rule of thumb, shifted earlier by the cut |
| 2:47.00–2:56.63 | Original standard close and final hold, retained |

Longest unbroken board run is the unchanged agent-loop board, approximately 23.27 seconds. No new filler or board break was added. Other existing board camera and ring treatments remain as approved; older ring widths elsewhere were not expanded into this narrow repair.

## Verification completed

- Actual encoded file decoded to **5,299 frames**, exactly the plan. The literal final frame is the standard close (`encoded-frames/005298.jpg`).
- Transition guard **PASS at all five changed boundaries**: frames 3633, 3885, 4283, 4414 and 4424. Every-frame boundary strips were visually inspected; no stray Gemini board or short intermediate scene appears.
- Inspected the corrected board at full resolution, the encoded PocketOS sequence sampled every half second, the key-over-label detail, and both sides of the new join. `encoded-animation-sheet.jpg` records the sequence.
- Compared all **4,508 unaffected video frames** with the source at sampled pixels. Maximum per-frame mean absolute difference was 2.792 on the 0–255 channel scale, consistent with this final encode; timing and scene content match.
- All retained PCM samples are exact outside a **4 ms bridge inside the quiet splice**. No new pauses, speech fades, gain changes, or other audio edits were applied. Source gaps were measured before selecting the frame cuts; resulting speech-to-speech quiet interval is approximately **0.55 seconds**.
- Encoded AAC versus intended PCM correlation: **0.9999897**. The actual encoded join was transcribed separately; it contains the intended PocketOS quotation and following warning, with no Gemini sentence. See `encoded-join-transcript.txt`.
- Upload synchronization passes for `rise-of-agents`. `git diff --check` passes. The canonical MP4's source hash is unchanged.

## Listening and scope limits

**The new join has not been directly auditioned.** Automated transcription and PCM checks do not establish natural cadence or the absence of an audible artifact. Listen around **2:23–2:33**, particularly **2:27.13**, before shipping. `encoded-join.wav` contains the encoded soundtrack from 2:20–2:37; `join-context.wav` contains the intended PCM around the join.

This narrow build retains the earlier approved opening's omission of the delayed-discovery warning and its “A chatbot answers, but an agent acts” wording. It does not claim a new whole-file narration KEEP or full audiovisual shipping certification. The missing-warning restoration was explicitly excluded from the approved repair scope.

The pristine raw rolls and old pre-v4 donor are absent locally. The available source is the verified finished v4; v6 uses one decode and one final H.264 encode at CRF 16, with AAC encoded once after the approved cut. No lossy intermediate was used for the repair.

## Reproduction and identities

Build: `.video-venv/bin/python scripts/video/build_rise_of_agents_v6.py`

QA: `.video-venv/bin/python scripts/video/qa_rise_of_agents_v6.py`

Board source: `scripts/video/render_rise_of_agents_rogue.py`; retained illustration and provenance in `scripts/video/assets/rise-of-agents-repair-2026-09-30/`.

- Source MP4 SHA-256: `d27f50d630ccae490c6d6c9511d6694d638e65dc073e8dd4ff9a4887ebfe8dcd`.
- Candidate SHA-256: `e860afa486b700b28aebc31734b7b1692aa57fc6eefe4788f51381aeeb1253d9`.
- Manifest: `edit-manifest.json`; encoded verification: `qa.json`; transition results: `transitions/transition-guard.md`.

No shipping approval is inferred from the build request. Public video remains the previously verified v4. Unrelated workspace changes were preserved.
