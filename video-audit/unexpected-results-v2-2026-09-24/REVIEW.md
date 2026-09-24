# Unexpected Results v2 — build record, 2026-09-24

Candidate: `Prompts/unexpected-results-v2.mp4` (3:59.07, 7172 frames, matches plan). Review only; live video,
lesson and boards unchanged (hashes asserted). Build: `scripts/video/build_unexpected_results_v2.py` (uses v1's
`road-patched.mkv`). Manifest: `build/edit-manifest.json`.

v2 = v1 (`../unexpected-results-v1-2026-09-24/REVIEW.md`) plus the live video's Text Messaging and GPS explanations,
after David said the live board explanations felt stronger ("Agree. Yes build it.", 2026-09-24).

## Narration in the board run (output times)
- 1:35.4 live: "SMS text messaging was originally designed as a narrow, basic service to pass short notes across
  mobile networks. Those early phones were built almost entirely for voice calls. But users took that secondary,
  short-form feature and turned it into their primary method of communication, creating the foundational backbone
  of traditional texting." (live 135.15–156.45; "Let's start with the top left." dropped)
- 1:56.3 roll 2: "GPS was built by the US military to guide ships, aircraft, and weapons." (roll 2 103.55–108.10)
- 2:01.4 live: "But once available in civilian hands, human ingenuity took over. Today, it is the invisible engine
  powering everyday location tools like Google Maps." (live 165.40–175.20)
- Change from the proposal: the live GPS opening ("Or look at the GPS panel on the top right. That system was built
  exclusively…") is not used. Cutting the position line left "That system" with nothing before it and GPS never
  named, so roll 2's own lesson sentence opens the beat.
- 2:11.0 on: roll 2 Cane Toads, Wider Highways, two better / two worse, title (as v1).
- Measured join gaps: 0.60 s (roll 2 → live SMS), 0.64 s (live SMS → roll 2 GPS), 0.42 s (roll 2 GPS → live),
  0.56 s (live → roll 2 Cane Toads). Live audio +2.2 dB. The live file's pauses were ~10 dB quieter than roll 2's
  room tone; 10 pauses inside the grafts refilled with roll 2's tone (listed in the manifest).
- The v1 road graft is unchanged (now at 2:55.7–2:59.1).

## Pictures in the board run
- Board 1:30.9–2:39.6 (canonical, dense), rings: Text Messaging 1:35.4, GPS 1:56.7, Cane Toads 2:11.1, Wider
  Highways 2:19.7, top row 2:32.4, bottom row 2:35.3, title 2:37.0.
- Breaks: roll 1 SMS diagram 1:42.9–1:52.9 under "Those early phones…" (it ends on "Text Data Displaces Voice",
  which matches the line); roll 2 US map 2:01.0–2:05.5 under "once available in civilian hands"; cane toad map and
  51% chart as v1. Longest unbroken board run 12.0 s (1:30.9–1:42.9).

## Checks
- transition_guard: 29 boundaries, 1 flag at f3934 (2:11.1). Strip inspected: it is the planned camera move from
  the GPS card to Cane Toads at the ring onset, not a stale frame (the same flag appeared and was inspected in the
  first v2 render).
- Corner mark: 0 declined. Output transcript reads correctly through the board run.

## For David
- Listen first: 1:35.4, 1:56.3 and 2:01.4 (the live voice against roll 2's), and 2:11.0 (back to roll 2).
- The live explanations are additions the lesson page does not carry (candidate lesson edit: why SMS and GPS
  turned out better than planned).
- Everything else, and what is still unauditioned, as in the v1 record. Not ready to ship until David watches it.
