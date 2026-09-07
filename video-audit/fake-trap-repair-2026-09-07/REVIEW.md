# Fake Trap review candidate

Status: ready for owner review, not shipped. Output: `Prompts/fake-trap-patched.mp4`, 3:48.967 (6,869 frames, 30 fps).

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
