# Transformer v14 paper correction

Created with the built-in ImageGen tool on 2026-10-22, using
`../transformer-v13/brain-paper-imagegen.png` as the edit target.
Saved asset: `brain-paper-imagegen.png`.

Prompt:
> Use case: text-localization. Edit target: attached brain and computer illustration. Change ONLY the lettering on the cream paper over the yellow brain at left. Replace the entire old sentence with EXACT text: "The tired CAT sat on the mat. IT soon fell asleep." Set as five clear centered handwritten lines: "The tired CAT" / "sat on the mat." / "IT soon" / "fell asleep." (four lines acceptable). Keep cyan marker highlighting behind CAT and IT only. Match original black handwritten style, use slightly smaller lettering so all words fit comfortably within the same paper. Keep paper boundaries and position exactly unchanged. Preserve yellow brain, blue computer, knowledge is power text, dotted background, colors, composition, and aspect ratio. No other edits.

The approved four-line output was inspected. Only its paper interior is used in
`build_transformer_v14.py`; the original moving scene supplies all other pixels.
The text is a shortened supporting example. Current lesson boards and narration
carry the full May-rainstorm sentence. No canonical lesson image was changed.
