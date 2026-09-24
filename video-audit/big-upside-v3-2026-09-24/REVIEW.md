# Big Upside v3: review candidate (2026-09-24)

v3 is v2 (`video-audit/big-upside-v2-2026-09-24/REVIEW.md`) plus one cut David asked for after watching v2:
"Delete from 1:21 to 1:26. It's redundant."

Build: `scripts/video/build_big_upside_v3.py` (v2's script with the cut; board legs reused from v2's build,
same specs). Output: `Prompts/big-upside-v3.mp4`, 8728 frames at 30 fps, 4:50.9, sha256
`f82ce9e44cd9565f71e47634764db5d201d99c25a3cf0519266dc17ed901f61d`. v2 is kept. The live video, lesson,
boards, both rolls and index.html are unchanged (hashes verified by the render). Not shipped.

## The change

- Cut source 1:37.97-1:43.23 (v2 output 1:21.0-1:26.3): "The sequence of those acids determines the
  folding, and that final shape determines the function."
- Join at v3 output 1:21.7: "...built from just 20 amino acids." / "Across 50 years of careful lab
  work...". The gap measures 0.42 s (81.50-81.92), inside silence. A medium.en transcript of 1:12-1:35
  reads cleanly across it.
- Break D (the live video's bead-chain drawing) lay entirely inside the deleted sentence, so it is gone.
  The Protein Facts ring holds unbroken across the join (strip `transitions/boundary-002452-*.jpg`).
- Everything after 1:21.7 is 5.27 s earlier than in v2. For the v2 table's later rows, subtract 5.3 s.

## Consequence

The protein board's last unbroken run is now 24.9 s (1:04.4-1:29.3), up from 16.6 + 8.3 s. That is
over the twenty-second guideline. The only drawing made for that span was the bead chain under the
sentence you cut, so I left the run as is rather than insert a 1-2 s flash.

## Checks

- Decoded frames: 8728, matching the plan. The final frame is the canonical close.
- transition_guard: 30/33 pass. The three flags (f1212, f1334, f1969) are the same false positives
  inspected in v2, at the same frames, all before the new cut.
- Corner mark: 2851 cloned, 1811 inpainted, 0 declined.

## Not auditioned

Everything listed in v2's record, plus the new join at 1:21.7. The v2 listening times after 1:21 move
5.3 s earlier: graft 2:58.5-3:07.6, cut 4 at 2:34.2, "Hassabis" at 1:53.5 and 4:22.8, "scenes" at 4:03.2.
