# Data Centers v3 — review candidate (built 2026-09-24)

**Candidate:** `Prompts/data-centers-v3.mp4` (3:43.13, 6694 frames, sha256 d7d2b1fe2b63…). Review only: the live
`course-assets/data-centers/data-centers.mp4`, the lesson and `index.html` are unchanged (hashes checked).
**Build:** `scripts/video/build_data_centers_v3.py`; manifest `build/edit-manifest.json`.
**Scope:** full production pass on `Prompts/data-centers-3.mp4`, per the plan David approved on 2026-09-24
(`video-audit/data-centers-comparison-2026-09-24/REVIEW.md`). Donors: data-centers-1, -2, -4.

## Narration changes (approved)

| Change | Source | Output | Joined gap |
|---|---|---|---|
| Cut "The digital cloud relies on heavy physical infrastructure, and that infrastructure takes up space in the real world." | roll 3 142.90–150.30 | 2:22.90 | ~0.98 s, silence at both edges |
| Cut "But looking at this chart, you can see the efficiency paradox in action." | roll 3 178.80–183.50 | 2:51.40 | ~0.84 s, silence at both edges |
| Close graft: roll 1 "Every AI chat costs something real. / Now you know what's behind the magic." replaces roll 3's "Every single… And now you know exactly…" | roll 1 271.87–277.20, gain −3.2 dB | 3:33.80 | ~0.53 s before "Every" |

No pauses added. The medium.en transcript of the candidate (`transcript-medium.txt`) reads both cuts cleanly
and the close exactly. At each seam the audio sits −67 to −83 dB for 0.15 s or more, so no word is clipped.

## Pictures

- **Canonical boards:**
  - **Inside a Data Center** (photograph): full view, no rings, 13.1 s.
  - **What a Data Center Means for Its Neighbors** (dense): 5.9 s full view, then a complete-card dive and ring
    at each spoken onset: Electricity purple, Water blue, Noise teal, Jobs amber.
  - **Meeting the Demand** (compact): card rings, then the banner ring.
  - State sheets: `build/states-*.jpg`.
- **Board breaks (8b):**
  - Neighbors board runs 18.4 s, 17.1 s and 13.2 s, broken by:
    - roll 2's high-voltage cable drawing under "raising household bills"
    - roll 2's empty town meeting room under "neighbors have actually sued"
  - Demand board runs 20.0 s and 6.4 s, broken by roll 1's pylon-and-chip drawing under "more work with each unit
    of electricity".
- **Covered:**
  - "THE EFFICIENCY PARADOX" chart (invented −75% / +1000%): now roll 2's LED and server-aisle drawings.
  - Blank frames plus the cost cards ("1M+ Gallons / Day"): now roll 4's CHAT-and-servers drawing, then its data
    center over homes and power lines from "the grid pays in watts".
  - Drawn man with a face: now roll 1's hand holding a phone with a check mark.
- **Close:** standard close (`computecost`) under the grafted lines. Roll 3's close card is gone.
- **Corner mark:** 2484 frames cloned, 1283 inpainted, 0 declined.
- **Kept and flagged:**
  - 0:00–0:01 blank fade-in
  - 0:46–0:50 GPU diagram labelled "2×10¹⁴ OPS/SEC"
  - 1:10–1:14 drawing whose cooling towers read as a power plant
  - brief blank fade frames at 1:03 and 3:02
  - The photograph board sits on dark side bars, taken from the photo's own corner.

## Checks done

1. Decoded 6694 frames, matching the plan.
2. `transition_guard.py` passed all 18 declared splices. Strips are in `transition-audit/` (combined:
   `strips-*.jpg`), and I inspected them: the first frame after every boundary is already the destination.
3. No edited pauses.
4. Settled ring frames inspected (state sheets): the right card, the whole card inside the ring, nothing clipped.
   The dive on the neighbors board crops the board title at the top edge, but never inside a card.
5. Full-view opens confirmed: neighbors 5.9 s, demand 5.4 s, photograph throughout.
6. Protected files unchanged.

## Not yet done: David's listening

- **3:33.8, the close seam.** This is roll 1's voice after roll 3's. Median pitch is 192 Hz against 163 Hz for the
  line it replaces, and the level is matched to −3.2 dB. It's the same narrator, but check that it doesn't sound
  like a different read.
- **2:22.9 and 2:51.4**, the two cuts: listen for pacing.
- One pass end to end. Nothing here has been heard yet, so it can't earn KEEP yet.

## Narration status

Every teaching point is RICH or TAUGHT and the close is exact. Five neighbors-board lines differ from the
required wording without changing a fact ("projected that number could reach", "cool them down", "have actually
sued… after losing sleep", "While initial construction", "roughly the staff"). David accepted these in the
plan. Ready for David's review, not for shipping.
