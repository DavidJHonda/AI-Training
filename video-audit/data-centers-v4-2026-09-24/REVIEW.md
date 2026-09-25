# Data Centers v4 — review candidate (built 2026-09-24)

**SHIPPED 2026-09-24** (David: "ship v4") as `course-assets/data-centers/data-centers.mp4`, cache key
`?v=20260924ship1`, pill 4 min. Installed after confirming its sha256 and frame count match the edit manifest.
Not listened to end to end by the editor; the joins listed below were left for David's listening.

**Candidate:** `Prompts/data-centers-v4.mp4` (3:43.13, 6694 frames, sha256 239d5a26ee58…). Review only.
**Scope:** narrow repair of v3 (`video-audit/data-centers-v3-2026-09-24/REVIEW.md`). David updated the neighbors board's
illustrations in place: `course-assets/data-centers/data-centers-physical-footprint.jpg` (sha256 f366b3c09b60…, page
reference `?v=20260924alignment`). v4 uses that asset. The layout is the same 1600×1461, and the card edges were
re-measured and haven't changed, so every highlight is where it was.
**Build:** `scripts/video/build_data_centers_v4.py` (v3's approved plan, rebuilt from the pristine rolls).

## Verification

- v3 against v4, frame by frame: only output frames 2617–3167, 3263–3776 and 3890–4286 differ. Those are the three
  neighbors-board spans; the two donor-drawing breaks between them are unchanged. The decoded audio is
  byte-identical.
- 6694 frames decoded, as planned. `transition_guard.py` passed all 18 splices. The corner mark was declined on 0 frames.
- State sheet `build/states-foot.jpg`: the new illustrations, with every ring around its complete card.
- `gemini-notebook/data-centers/upload/` was re-synced to the same asset for future rolls.

Everything else, including the listening still owed, carries over from the v3 record: the close seam at 3:33.8,
the cuts at 2:22.9 and 2:51.4, and one pass end to end.
