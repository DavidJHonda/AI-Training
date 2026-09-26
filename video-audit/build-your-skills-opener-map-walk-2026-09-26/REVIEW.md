# Build Your Skills opener v4: section-map walk (2026-09-26)

**Candidate:** `Prompts/build-your-skills-opener-v4.mp4` (4928 frames, 2:44.27 at 30 fps, 1280x720, sha256 e1eeb5cb701601a1…). Not shipped; live v3 unchanged.
**Build:** `.video-venv/bin/python scripts/video/build_opener_build_v4.py` → `build-v4/` (edit-manifest.json, leg-map.json, states-map.jpg).
**Scope:** full map-walk rebuild on the live, plan approved by David 2026-09-26 ("Yes. All your suggestions. Build it please.").

## Sources
- Base: live v3 `course-assets/build-your-skills-opener/build-your-skills-opener.mp4` (9ad9b412a7a2…).
- Map narration: roll 2 `Prompts/build-your-skills-opener-2.mp4` (4d3a68804340…), frames 2781-4572 (92.70-152.40), audio only.
- Roll 1 (`-1.mp4`) reviewed, not used: it drops "use AI honestly" and paraphrases the banner.
- Boards: current section-map and close JPGs. Transcripts: `roll1/roll2/live-words.json`, `v4-transcript.txt`.

## Output timeline
| Output | Source | Content |
|---|---|---|
| 0:00-1:13.00 | live 0-2190 | creed card (as shipped), bike story, AI/human skills |
| 1:13.00-1:16.90 | live 2190-2307 audio, our map at full view | "This roadmap shows what we'll explore in this section." |
| 1:16.90-2:16.60 | roll 2 92.70-152.40 audio, our map | "Zooming in on step one…" → "Build the skills you keep when the tool changes." |
| 2:16.60-2:17.23 | live 3594-3613 audio, map held | silence to the live's scene cut |
| 2:17.23-2:35.47 | live 3613-4160 | keep-in-mind question drawings and audio |
| 2:35.47-2:44.27 | live 4236-4380 audio + 120-frame tail, new close | "The tool is rented. The skills are yours to keep." |

Cut from the live: 76.90-119.80 (its map walk and the gloss "The software provides a temporary shortcut. Your cognitive framework provides a lifelong strategic edge.") and 138.67-141.20 ("Because as this graphic reminds us,").

## Section map rings (compact, full view, no push)
Row rings at each spoken title, then phrase rings as each point is spoken (approved exception to 1b's "follow sections"). Output onsets: row 1 1:17.36; "Choose what changes the answer," 1:24.02; "improve ideas through conversation," 1:26.16; "use AI honestly," 1:29.34; "and protect what you share." 1:30.84; row 2 1:32.82; "People skills…" 1:42.18; "Creative thinking…" 1:45.76; row 3 1:52.48; "Keep learning as AI changes," 2:00.78; action clause (two rects) 2:04.20; banner 2:09.94 to the cut. Phrase rings: 3 px on sides shared with a neighbouring phrase (stroke draws outward; the gaps are 10-11 px), 6 px on open sides, radius 8. Inspected at full resolution: no text covered, but they are tight at the shared sides.

Board on screen 1:13.00-2:17.23 (64.2 s, longest unbroken board run). Held unbroken by approval: rings change every 3-9 s; neither roll drew anything for rows 2-3.

## Checks
- Decoded frames 4928 = plan. Protected files unchanged. Corner cleaner: 0 declined frames.
- transition_guard: 5/5 boundaries pass (`transitions/`); strips inspected: first frame after each boundary is the destination.
- Transcript of v4 matches the plan word for word at every join; nothing spoken after "The skills are yours to keep."
- Join gaps (silencedetect -35 dB): 0.62 s "section." → "Zooming"; 1.17 s "changes." → "Keep one central question"; 1.10 s "question." → "The tool is rented." No pauses added.
- Levels: roll 2 pre-leveled +4.5 dB through a limiter (ceiling -0.26 dBFS). Speech RMS: live before -14.79, graft -15.30, live after -15.47 dBFS.
- Final frame: the current close JPG, standard 48 hold / 150 push to 1.2x / 66 settle.

## Not verified / for David
- **Listening (I cannot hear audio):** voice and level match at 1:16.9 (live → roll 2) and 2:16.6 (roll 2 → live); the close join at 2:35.5; whether the limiter is audible on roll 2's loudest words.
- Roll 2's register is stiffer than the page ("necessity," "pivot," "actively appreciates," "overarching mandate"); approved as complete over polished.
- Still open from the 2026-09-24 review, outside this scope: creed and keep-in-mind question are paraphrased; the title "Build Your Skills" is not spoken.
- Shipping not authorized; index.html, manifest, and the live file untouched.

## v5 (2026-09-26): full-row rings only — current candidate
David on v4: "For the highlights, just highlight the full row as it's spoken. That's what we do on the other Openers."
`Prompts/build-your-skills-opener-v5.mp4` (4928 frames, 2:44.27, sha256 bc3f3ff0b1f8b197…), built by
`scripts/video/build_opener_build_v5.py` (the v4 script, renamed; its phrase targets removed) into `build-v5/`.
Row rings at 1:17.36 (row 1), 1:32.82 (row 2), 1:52.48 (row 3); banner at 2:09.94 to the cut. Audio, timeline,
and close identical to v4. transition_guard 5/5 pass (`transitions-v5/`); states-map.jpg inspected.
The v4 section above is superseded for the rings only; everything else in it still applies, including the listening list.

## Shipped 2026-09-26
David: "ship it". v5 copied to `course-assets/build-your-skills-opener/build-your-skills-opener.mp4` (sha256 bc3f3ff0b1f8b197…, 29151451 bytes);
`index.html` LESSON_VIDEOS.openerskills → `?v=20260926ship3`, pill "3 min"; manifest video_assets hash + bytes updated.
Raw rolls and the v4/v5 candidates stay in Prompts/. Render intermediates (legs, wavs, canvases, previews) removed.
