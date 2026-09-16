# Context Window — roll 4 production candidate

## Recommendation

**READY FOR DAVID'S REVIEW; NOT AUTHORIZED TO SHIP.** The narration remains a
KEEP. The candidate uses roll 4 as the uninterrupted audio master, with no audio
grafts, narration cuts, or added pauses.

- Candidate: `Prompts/context-window-v1.mp4`
- Candidate SHA-256: `c398c04433dcef5cab542722a54e3e04da4c9cb903d7215e34c7dacdaec764c6`
- Runtime: 4:35.967 (8,279 frames at 30 fps)
- Video: 1280x720 H.264
- Audio: mono AAC, 48 kHz, 192 kb/s target
- Source: `Prompts/context-window-4.mp4`
- Source SHA-256: `711858413a652212490e2cb144eb7e72668ac188183c68aa219017f0d9bb524d`
- Visual-only donor: `Prompts/context-window-3.mp4`
- Donor SHA-256: `a6144543f2d88f24ba2fb3a6894d9b0c512cb1d98f61d27454cd271adeaa7f32`

## Build treatment

| Board | Highlighting | Camera | Result |
|---|---|---|---|
| Same Question. Different Answers. | Question, Luke's complete card, Nate's complete card, then takeaway | Full-board opening; complete-card dives; pull back for takeaway | Current JPG replaces the generated stand-in from 0:12.47 to 0:53.77 |
| The Context Window | From This Chat, Personalization and Memory, Project Context, then the context-window tray | Full board throughout | Current five-sources JPG from 1:39.73 to 2:10.60 |
| Give AI a Head Start | Personalization, Saved Memory, Projects | Full-board opening; complete-card dives | Current JPG from 2:16.27 to 3:02.37 |
| Outside the Window | Older Chats, Web Pages, Files on Your Computer, Other Apps and Tabs, then the hard-rule banner | Full-board opening; complete-card dives; pull back for rule | Current JPG from 3:07.73 to 3:48.40 |

All rings are post-crop 5 px outlines. Full-board unmarked openings are 104, 77,
96, and 215 frames respectively. The longest uninterrupted board run is 46.1
seconds.

Notebook treatment:

- Roll 4 frames 2579–2748 provide a clean typing drawing under the Head Start
  introduction, breaking the otherwise 82-second board run. The Head Start board
  returns three seconds before its first named card.
- Roll 3 frames 6888–7323 cover roll 4 audio from 4:11.13 to 4:25.77. This replaces
  the misleading `Working Memory Reset` graphic with a fresh-chat/clean-context
  drawing. The donor is picture only; roll 4 audio is unchanged.
- Kept Notebook frames had the Gemini corner mark removed: 2,592 frames by paper
  clone and 613 by inpaint; zero frames were declined.
- The engine outro was replaced by the canonical standard close: 48-frame hold,
  150-frame push to 1.2x, and 108-frame settled hold. The close is the literal
  final frame.

## Narration

The final-file transcript confirms the complete roll 4 narration is present,
including:

- the full Luke and Nate responses and practical cost cautions;
- "Different doesn't always mean wrong";
- all five context sources in one span;
- complete Personalization, Saved Memory, and Projects examples;
- all four outside-window categories and the hard rule;
- the forgetting explanation, reminder fix, and fresh-chat/clean-context fix;
- the clarification that a fresh chat does not increase or reset the technical
  context-window limit; and
- both required closing lines, with no narration afterward.

The minor grammar slip at 0:48.60 remains: "Luke and Nate types the exact same
prompt..." It was previously judged non-material, and no optional donor graft was
used because avoiding an unnecessary audio seam was the stronger choice.

## Verification completed

- Full video decode: PASS; 8,279 decoded frames, 30 fps, 4:35.967.
- Complete final-file ASR transcript: PASS; 72 segments through the close.
- Transition guard: PASS at all 11 declared boundaries; manual every-frame strip
  review found no stale-frame islands or leaked graphics.
- Board-state review: PASS for all openings, rings, complete-card framing, camera
  moves, pullbacks, and final banner states.
- Whole-file visual contact-sheet review at four-second intervals: PASS. No stock
  photograph outside the canonical course boards was found; no generated board
  substitute remains in a course-board span.
- Fresh-chat spot checks at 4:12, 4:20, and 4:24: PASS; the visual teaches clean
  context and fixed capacity without claiming that the limit resets.
- Corner-mark spot checks and cleanup manifest: PASS; no declined frames.
- Final frame: PASS; canonical closing board.
- Encoded-file silence scan: no pause was inserted. The only long final silence is
  the prescribed settled close hold (4:31.64–4:35.97).
- Protected source and board hashes remained unchanged.

## Verification limitation

This environment did not provide real-time acoustic playback of the encoded MP4.
The roll 4 narration had already been reviewed, the candidate preserves it in
source order without grafts or cuts, the encoded file decodes cleanly, and the
complete final-file transcript matches the reviewed wording. David should still
listen through the review candidate before authorizing publication, especially
the visual-only seams at 2:10.60 and 4:11.13 and the standard close transition at
4:25.77.

## Artifacts

- `edit-manifest.json` — complete frame map, hashes, board specs, and cleanup counts
- `board-state-overview.jpg` — every board's unmarked, highlighted, and final states
- `transitions/transition-guard.md` — 11-boundary automated report
- `transition-overview.jpg` — every-frame seam strips
- `final/context-window-v1/transcript.txt` — final-file transcript
- `final/context-window-v1/all-sheets.jpg` — whole-file contact-sheet overview
- `final-spotchecks/final-frame.jpg` — literal final frame

The live lesson video was not changed, and nothing was deployed.
