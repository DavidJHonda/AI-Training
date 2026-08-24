# Pre-review board-treatment audit

Audit date: 2026-08-22

Scope: the 26 staged lesson videos that remained after Welcome, Why Learn AI,
Does School Matter, Learn With AI, and What Is AI were approved.

## Rules enforced

- No text-background highlight is combined with an exterior border.
- Compact boards remain complete on screen while the active component receives
  one exact border.
- Dense boards begin complete, move smoothly to the complete active section,
  and hold there while it is discussed.
- Camera moves take 24 to 30 frames and settle before the explanation continues.
- A wide takeaway border does not appear until the camera has returned to the
  complete board.
- Highlight changes are timed to narration onsets from fresh word-level
  transcripts.
- Existing audio is copied bit-for-bit; every repair retains the exact source
  frame count and 30 fps.

## Repaired before review

| Video | Pre-review repairs |
| --- | --- |
| AI Is Different | Removed text-background effects; corrected the comparison-board border bounds; added smooth left/right camera moves; added three-card moves on the risk board; separated the takeaway pullback from its border. |
| Does AI Think? | Removed the remaining text-background effects and retained the complete-board treatment because every component is legible at 720p. |
| Questions Matter | Removed text-background effects; added smooth moves across Library, Search, and AI; added a complete-board orientation beat; retimed the Pre-AI and With-AI comparison to the narration. |
| What You Can Control | Removed text-background effects; added smooth column and row camera moves; retimed all six item highlights and both recap highlights; retimed the three moves; separated the takeaway pullback from its border. |
| Evaluate the Results | Added full-board orientation, smooth card-to-card moves, and stable holds across all four boards; added unmarked pullbacks before the three wide takeaway borders. |
| How AI Answers | Added smooth moves through Question, Last Token, and Next Token while keeping each complete active panel visible. |
| One More Thing | Added smooth moves through One Word, One Sentence, and Complete Chat so the figures and descriptions are readable. |
| Where AI Works Best | Added smooth moves between What It Does and Examples on all four boards; separated the first board's takeaway pullback from its border. |

## Audited with no additional repair required

AI Is Math; Art of Prompting; Context Window; Critical Thinking; Document Trap;
Embeddings; Engagement Trap; Hallucination; How an LLM Works; Avoid Traps
Opener; Understand AI Opener; Work With AI Opener; Tokens; Training Bias;
Training; Transformer; Vector Space; Which App.

These already use border-only emphasis with narration-aligned geometry. Boards
whose active area spans nearly the full width remain complete on screen because
zooming would crop a row or omit dimensions without materially improving
legibility. Which App already uses a smooth card-to-card camera walk.

## Verification

All highlight-plan JSON files validate, and none contains a `chip` instruction.
The eight rebuilt videos match their staged source frame count and fps and have
bit-identical audio. Maximum internal junction difference is 9.25, below the
course limit of 12.
