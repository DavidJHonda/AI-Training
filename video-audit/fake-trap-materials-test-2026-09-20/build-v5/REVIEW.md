# Fake Trap v5 — build review (2026-09-20)

Status: review candidate only. Supersedes v4 on one owner request (2026-09-20, after viewing
v4: "the video is excellent"; Board 1 should highlight its individual sections as spoken).
Everything outside Board 1 is byte-identical to v4 (sampled every 97th frame: zero difference
outside output frames 804–2037). The v4 review in `../build-v4/REVIEW.md` covers the narration,
the graft, the covers, and the listening checks; none of that changed.

- Candidate: `Prompts/fake-trap-v5.mp4`
- SHA-256: `5d9b0f00bfa41ddd911a5586fbfa27b0e449c558d2c56ad126754ae31ec00c4a`
- Runtime: 9,240 frames at 30 fps (5:08.00), unchanged
- Build: `scripts/video/build_fake_trap_v4.py --revision-v5`; manifest `edit-manifest.json`

## Board 1, The Same Clip. Two Eras. (0:26.80–1:07.90, dense)

Section rings share each card's rails 16 px inside the card edge; the camera holds the complete
card while the rings step through it. Text bands were measured on the canonical JPG.

| Output time | Narration | Ring |
|---|---|---|
| 0:26.8 | "This chart compares how we evaluate media across two eras." | full view, unmarked (4.1 s) |
| 0:30.9 | "Before artificial intelligence, the first question was, does it look real?" | dive to Before AI; era label + "Does It Look Real?" (amber) |
| 0:35.6 | "You would study the face, listen to the voice, and check the hallway…" | body + Checked "Face and voice." together (amber) |
| 0:40.6 | "If you matched how the principal talks…" | Matched "How the principal talks." |
| 0:42.6 | "…you reached a verdict. The video is real." | Verdict "Real." |
| 0:45.7 | "In the AI era, that old test fails." | camera moves to The AI Era, no ring yet |
| 0:48.6 | "The new question is, where is it from?" | era label + "Where Is It From?" (blue) |
| 0:51.2 | "You ignore the pixels entirely and check the trail." | body |
| 0:54.4 | "You skip studying the face and voice…" | Skipped "Face and voice." |
| 0:56.8 | "…and instead check the source that would actually know." | Checked "The source that would know." |
| 0:59.4 | "If nothing appears on the official school website…" | body again (its second sentence) |
| 1:02.2 | "…the claim remains unverified." | Verdict "Unverified." |
| 1:04.8 | "Appearance can mislead. The source trail can be checked." | full view; banner (neutral purple) |

State sheet: `states-comparison.jpg`; every settled ring frame inspected at full resolution
(right section, complete text inside the ring, 5 px stroke, nothing clipped).

## Verification

- Decoded 9,240 frames, matches the plan; audio identical to v4.
- Corner mark: 4,802 cloned, 1,049 inpainted, 0 declined (same frames as v4).
- `transition_guard.py` on the Board 1 seams (804, 2037) and the unchanged audio seams: the only
  flag is again output frame 2931, the reasons board's own camera dive (inspected in v4).
- Protected files unchanged.
- Not auditioned; the v4 listening list still applies.
