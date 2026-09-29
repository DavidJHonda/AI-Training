# Context Window v6 — animation labels

Status: **shipped locally; queued for batch deployment**. Owner authorized “ship it.” Local commit: `24ad75fbc7a131326ede41922ef9e29e5f6c18a9`. Installed SHA-256: `b141d3265b3dddc44ef1ca0f2cb3383e53b86e22ca6020ae59ea61a8d80d346a`. Cache key: `20260929ship6`. No push or deployment performed.

Owner direction: “1:07-1:10. Ok as is. Make the other change.” This approves the forgetting-animation label repair from the live evaluation. The desk scene is accepted as-is and is outside this repair. No board, camera, ring, narration, pause, or close redesign was authorized or performed.

## Change

Only the animation at **3:38.533–3:57.100**, frames **[6556, 7113)**, receives visual edits. It retains its original cards, motion, overlapping layers, arrow, fading, empty-window ending, and timing. Text overlays follow each card through the moving, settled, and faded states. Brief occlusions use measured trajectory interpolation, with foreground cards masking the lettering. The final fade tracks the panels against the original empty ending frame.

| Original label | Revised label |
|---|---|
| SYS | USER |
| System Instructions: Setup | User: Study Goal |
| User: Project Constraints | User: Exam Topics |
| AI: Architecture Outline | AI: Study Plan |
| User: Database Schema | User: Class Notes |
| User: Update Endpoints | User: Practice Quiz |
| AI: Controller Code | AI: Practice Questions |
| Restored: Project Constraints | Restored: Exam Topics |
| Prompt: Remember earlier project constraints… | Prompt: Remember my exam topics. |

The mechanism remains older conversation details leaving the active context, a reminder bringing an important detail back, and a new chat clearing that conversation. It no longer illustrates system instructions being expelled as ordinary chat history.

## Sources and output

- Source: original canonical v5 / cache key `20260926ship9`, preserved at `Prompts/context-window-v5.mp4`. The canonical path now contains approved v6.
- Source SHA-256: `6d3e3ff7d2ad4c0019a460a44e250470a47b19ca2998f4eab0f8539300cb7c12`.
- Candidate: `Prompts/context-window-v6.mp4`.
- Review excerpt: `video-audit/context-window-label-repair-2026-09-29/changed-section.mp4`.
- Build: `scripts/video/build_context_window_v6.py`; per-frame positions retained in `tracking.json`.
- QA: `scripts/video/qa_context_window_v6.py`; exact output hash and measurements in `qa.json`.

The finished v5 is the available source. This is one additional video encode from that file; the AAC audio packets are copied without re-encoding. Frames outside the target span are passed directly from source decode to the encoder with no visual treatment. In particular, the 1:07–1:10 desk scene is unchanged in content and timing.

## Verification

- Exact decoded duration retained: **7,461 frames at 30 fps = 4:08.70**.
- All **11,659 AAC packets** hash identically to the source: `329c9d49f4cc367e44e05e99021539d16a6a3f5e077a2ea0cc6cadcd40682d6b`.
- Transition guard at both edited-span boundaries; encoded strips inspected.
- Encoded frames inspected at entry, settled cards, card crossings/occlusions, reminder arrival, restored detail, final fade, and return to the original close.
- Approved v6 installed at the canonical lesson path, hash verified against the candidate; website cache key and manifest updated.

No fresh listening or continuous real-time playback was performed. This is a visual-only repair with byte-identical audio; previous audio-listening limitations remain unchanged. No new pauses or audio joins exist. The unrelated optional Head Start ring refinement was not applied.

## Reproduction

Run `.video-venv/bin/python scripts/video/build_context_window_v6.py --draft` with the retained `tracking.json`; then `.video-venv/bin/python scripts/video/qa_context_window_v6.py`. The source hash is enforced. The draft path is regenerable working output; the owner-facing v6 candidate is preserved once delivered.
