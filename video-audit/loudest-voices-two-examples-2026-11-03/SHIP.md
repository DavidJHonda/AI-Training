# Loudest Voices v13 local release

Shipped locally on 2026-11-03, authorized by David: “Ship it.”

- Commit: `ab801cb702afcc9d963d7e06c393e38387695fdb`
- Installed: `course-assets/loudest-voices/loudest-voices.mp4`
- SHA-256: `21542eafdd39fa9ec4740b1c3d7c0cb5fad23a0d6f914c289775a3e4755751da`
- Runtime: 3:56.133; 7,084 frames at 30 fps. Page label: 4 min.
- Cache key: `20261103ship13`.
- Approved release includes the two-example board without its banner, synchronized lesson copy and prep prompt, renderer changes, and canonical asset metadata.
- Candidate and board hashes verified; candidate fully decoded again before installation. Installed bytes equal the approved candidate. The committed page points to the installed canonical path.
- Entire staged release snapshot passed `verify-course-assets.py --migration-hashes`: 244 retained assets, 515 original path mappings, 263 website references, 55 finished videos.
- The shared working tree had unrelated Pace of Change asset inconsistencies, so the release was validated from the Git index with those working changes excluded. Only Loudest Voices changes were committed.
- Prior visual/transition/audio-correlation checks remain recorded in REVIEW.md and qa.json. Assistant listening was not performed, as disclosed before the owner's shipping instruction. Approval is not represented as proof that a listening pass occurred.
- No push or deployment performed. **Queued for batch deployment.**
