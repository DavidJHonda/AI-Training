# Fake Trap review candidate

Status: shipped on 2026-09-07 with owner approval to `videos/fake-trap.mp4`, 3:40.033 (6,601 frames, 30 fps). Approved source: `Prompts/fake-trap-patched.mp4`.

Shipping verification: source and live SHA-256 both `4f25e5fbfa358dcafb8e3e8f6ca359074693522c6a93746c138ac3bc7070c13f`. Native macOS playback and first-frame decoding pass. Previous live video retained as `live-before-ship.mp4` in this audit folder. No lesson-page or `index.html` edits, candidate deletions, or commits. The notes below document pre-shipping review history.

## Latest revision: pauses, current faces, no bank detour

- Added exactly 30 silent frames at 0:58.700 before the harmless-fakes point, holding the prior picture.
- Replaced the pause-before-sharing cutaway with `assets/pause-before-sharing-v2.png`. Current face/hair identity comes from `illustrations/make-your-move-note-v1.png`: darker loose/shaggy hair in #4, lighter brown curls in #96. Kept this corrected scene throughout 1:59.367–2:20.100 rather than briefly returning to the obsolete character artwork. The new prompt is `assets/pause-before-sharing-prompt-v2.md` (built-in image-generation edit).
- Removed the entire 10.333-second bank-voicemail donor passage, both audio and graphics. Kept the following lesson-relevant advice about viral claims and marking claims unverified. The cut now joins the independent-verification banner to that guidance at 2:41.200.
- Retained the existing one-second pause before the close and expanded the final silent closing hold to one full second, 3:39.033–3:40.033.
- Page assets and live video remain unchanged. Earlier sections below are historical and superseded where they describe the removed bank example, older faces, duration, or audio hash.

### Final checks for this revision

- Sequentially decoded all 6,601 frames; audio decoded without errors. Native macOS playback and first-frame decoding pass.
- Confirmed each of the three silent holds is exactly 30 frames, with zero amplitude in its central audio interval.
- Inspected all 24 every-frame boundary strips. Nine automatic alerts correspond to continuous planned zoom/pan motion, not flashes of discarded graphics. The bank-removal join, new illustration entries/exits, and pause boundaries are clean in these checks.
- Re-transcribed the edited audio: the bank example is absent, viral-claim/unverified guidance remains, and the final words remain intact. Source video, live video, and lesson asset hashes are unchanged.

## Earlier owner follow-up (superseded history)

- 0:13.400–0:19.100: highlight the complete THE SCENARIO box at its measured outer boundaries (40,112)–(1560,239).
- 1:58.367–2:15.500: new realistic Nate and Luke pause-before-sharing cutaway, in Dallas Stars jerseys. Built-in image generation; see `assets/pause-before-sharing-v1.png` and `assets/pause-before-sharing-prompt.md`. At 2:15.500, return to the existing source-trail lesson illustration as that action is spoken. Lesson page unchanged.
- Takeaway-banner outline now uses standard neutral purple #6e51ff, not amber.
- Owner identified the unwanted CONTROL / INDEPENDENT SPACE donor graphic at about 2:41. This was a 1.667-second opening remnant, longer than the automatic six-frame flash threshold; the earlier boundary-only check did not identify it as unwanted. It is now fully covered with our banner through source frame 5915. The first clean phone image is source frame 5916, output frame 4856 (2:41.867). No narration was cut.
- Expanded manifest now records 26 boundaries, including the new illustration switch and exact first-clean-phone frame. Those joins and the scenario entry pass automatic checks and were inspected frame by frame. The same nine planned camera-movement alerts remain.
- Encoded audio stream hash is unchanged from before these visual edits: `6d4d7d8be50ea8aa41125ea07d9e718af7757ce341aa93cfd08c859683334429`. Duration remains 6,869 frames. Native macOS playback and first-frame decode both pass.

The earlier verification below documents the initial candidate; the owner follow-up above supersedes its visual-boundary assessment.

## Applied approved changes

- Removed the categorical eyes/ears passage, categorical algorithm passage, redundant final transition, and Notebook outro.
- Replaced the comparison, motives, source-trail illustration, three checks, and closing graphics with the current lesson assets. No page assets were modified.
- Highlight rails use measured current card/band boundaries and the corresponding accent color. The v3 motives PNG uses its own measured 1329-pixel geometry, not legacy 1600-pixel coordinates.
- Introduced full boards, then zoomed/panned through individual cards. Masked unrelated heading/footer fragments from zoom margins while preserving the full target card. The illustration keeps its title and full banner visible.
- Replaced the entire NHL photograph interval with original fictional amateur-hockey celebration art. Built-in image generation was used; the asset and complete prompt are in `assets/`.
- At output 2:40.200–2:50.533, used the complete live-video passage explaining not to call the message's number, but to independently look up the bank's official number and call it instead. Both donor narration and its native supporting phone graphics are retained.
- Kept the full targeted-help instructions, including the exception against saving/sharing private images of minors, reporting resources, and reassurance.
- Added a one-second silent transition after reassurance and a short silent hold at the end of the standard closing push-in.

## Verification

- Sequentially decoded all 6,869 final frames. No decode errors.
- Inspected all 24 output-timeline boundary strips, with every frame shown for 12 frames on each side. No leaked discarded graphics identified. Nine automatic alerts were caused by continuous planned camera movement, not intermediate shots; raw alerts remain in the transition report.
- Inspected highlight-state frames and native middle passages, including the donor phone sequence and targeted-help guidance. Original art remains inside the frame during its subtle push-in.
- Re-transcribed the edited audio through the final spoken word. Trusted-number instruction, edit-adjacent sentences, the private-image exception, reporting resources, reassurance, and exact two-line close remain intelligible in that check. This is not a substitute for the owner's subjective audio review.
- Confirmed exact digital silence in the central portion of the one-second transition and final hold.
- macOS AVFoundation reported `Playable: YES` and decoded the first frame successfully.
- Hash checks confirm the raw video, live video, current lesson illustrations, and closing asset are unchanged. No `index.html` edits, live replacement, or candidate deletion performed.

Evidence: `manifest.json`, `integrity.json`, `qa/`, `transitions/transition-guard.json`, and every-frame boundary JPEGs. Build recipe: `scripts/video/build_fake_trap_review.py`.
