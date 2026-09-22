# Build Your Skills opener: narrow repair of the live video (2026-09-22)

**Scope:** narrow repair (Edit Spec 1). Two changes David asked for on 2026-09-22; everything else, picture and audio, is the
live's own. No new pauses, no other cuts. Review only: the live video, lessons/, course-assets/, index.html and the registry are
unchanged (hashed as protected files by the build).

**Candidate:** `Prompts/build-your-skills-opener-v3.mp4` (4463 frames, 2:28.77, sha256 9ad9b412a7a20c4e…), built by
`scripts/video/build_opener_build_v3.py`, working folder `build-v3/` here.

## Source identities

| File | Role | sha256 | Notes |
|---|---|---|---|
| `course-assets/build-your-skills-opener/build-your-skills-opener.mp4` | live, the source | ddc11748d78a092e… | 4481 frames, 2:29.37, shipped 2026-09-11 (`?v=20260911ship1`) |
| `course-assets/understand-ai-opener/understand-ai-opener.mp4` | donor (one sentence, audio only) | 2fcdd916bd77a35b… | v7 live of the Understand AI opener |
| `…/build-your-skills-opener-creed.jpg` | card, recaptured today | aa05f461d6aaa667… | 1600x900, card 60,194-1539,705 |
| `…/build-your-skills-opener-section-map.jpg` | section map | 3db3106912da4f7a… | 1600x830, card 81-1519 x 128-661, dividers y 319 and 470, banner 40,702-1560,790 |
| `…/build-your-skills-opener-close.jpg` | page close asset | 0b9a7f703e32a3e1… | not used by this build; see "Boards kept as the live has them" |

Live measurements in this folder: `live-scenes.txt` (scene cuts by sequential decode), `live-words.txt/.json` (small.en word
stamps), `live-key-frames.jpg` (frames at every cut and ring pop). Silences from silencedetect at -35 dB.

## Live timeline (source frames, 30 fps)

| Span | What the live shows |
|---|---|
| 0-473 | old card capture (white frame, smaller type); ring pops at f189, 218, 269, 298, 361 (the closing line is ringed); out on the scene cut at f473 (15.77, "tool." ends 15.06) |
| 473-2211 | Notebook drawings: notebook writing, bike, balance, rink, Human Durability |
| 2211-3407 | section map, arriving 0.28 s after "This map outlines…" begins (73.42); ring pops f2330 row 1 ("We begin" 77.70), f2635 row 2 ("Next" 87.96), f2813 row 3 ("Step three" 93.82), f3238 banner ("The blueprint points to this bottom line", speech resumes 107.98), banner held to the cut at f3407 (113.57) |
| 3407-4184 | Notebook drawings: book/tablet, notebook hands; the final question |
| 4184-4481 | the live's standard close (48 prehold / 150 push / 99 settle), audio "Because as this graphic reminds us, the tool is rented. The skills are yours to keep." to 145.28, tail to 149.37 |

## Output timeline

| Output frames | Source | Content |
|---|---|---|
| 0-473 | live audio 0-473 | **card leg**: recaptured JPG at full view (compact, push=False, min_open=0), five gold rings |
| 473-2190 | live 473-2190 | live picture and audio |
| 2190-2304 | donor audio 2405-2519 (+1.0 dB); picture = map leg frames 0-113 | **graft**: "This roadmap shows what we'll explore in this section." over the unmarked section map at full view |
| 2304-3389 | live 2322-3407; map leg frames 114-1198 | **map leg** continues: row rings at 2312 / 2617 / 2795, banner ring at 3220, held to 3389 |
| 3389-4166 | live 3407-4184 | live picture and audio |
| 4166-4463 | live 4184-4481 | the live's close frames and audio tail, untouched |

Output frame = source frame for f < 2190; source frame - 18 for f >= 2322 (132 live frames out, 114 donor frames in).

## Change 1: the opening navy card

The live's card span is frames 0-473 (the card leaves on the live's own scene cut at f473; f472 is the last card frame, f473 the
notebook drawing). The recaptured JPG is shown at full view for exactly that span. Gold `#f2cf5b` rings, rect = white glyph
extent ±18 px in x, ±9 px in y (extents re-measured on the JPG today and matching the brief within 1 px), radius 18, 5 px stroke at
the wide camera. Onsets are the live's spoken onsets from small.en; the live's own pops are within 1-5 frames of each:

| Line | Ring rect (image px) | Onset used | Spoken | Live's pop |
|---|---|---|---|---|
| Your choices. | 102,313-427,367 | 6.32 (f190) | "Your choices" | f189 |
| Your questions. | 102,388-471,449 | 7.32 (f220) | "the questions you ask" (paraphrase; ring at the noun phrase) | f218 |
| Your judgment. | 102,461-467,524 | 8.96 (f269) | "your judgment" | f269 |
| Your skills. | 102,533-361,587 | 9.98 (f299) | "and the permanent skills you bring" (paraphrase; at "and", as the live) | f298 |
| And you'll always be Smarter Than the Tool. | 102,602-912,656 | 12.20 (f366) | "Together, these mean you'll always be smarter than the tool" | f361 (inside the 11.63-12.19 silence) |

Full view before the first ring: 190 frames (6.33 s). State frames: `build-v3/states-card.jpg`, `state-card-*.jpg`;
`card-live-vs-new.jpg` shows the live's frame 0 over the new leg's frame 0.

## Change 2: the map-introduction sentence

**Audio.** Live frames 2190-2322 (73.00-77.40) are removed: the cut out sits inside the 72.12-73.81 silence (0.92 s after "you."
ends, no breath blip: the 10 ms profile stays at -60 to -70 dB from 72.4 to 73.7) and the cut in sits inside the 77.16-77.82 silence
(0.25 s after "phases." ends, 0.30 s before "We"). Donor frames 2405-2519 (80.167-83.967, 114 frames) carry "This roadmap shows what
we'll explore in this section." (words 80.52-83.56) with 0.35 s of its own lead-in and 0.41 s of tail, both inside the donor's
silences (79.55-80.95, 83.77-84.19). `Build.graft(..., picture_from=2208, gain_db=1.0, visual="map")`: 5 ms crossfades into the
live's room tone at both seams (tone seed 146.60-146.70 in the live, RMS 14.4 vs pause floor 14.7).

Gaps in the finished file (silencedetect -35 dB): 72.120-73.787 (1.67 s; the live had 1.69) and 76.627-77.216 (0.59 s; the live had
0.66). No pause was added.

**Level match (recorded as asked).** Speech RMS gated at -40 dBFS over 20 ms windows: live "We begin by using AI with strict care
and honesty." -14.31 dBFS, live "We want to build the enduring human skills…" -14.57 dBFS, the replaced live sentence -14.71 dBFS;
donor sentence -16.36 dBFS. Integrated loudness: live next -14.9 LUFS, live prev -15.3 LUFS, donor -16.7 LUFS. A pure match asks
+1.8 to +2.0 dB. **Gain applied: +1.0 dB**, a deliberate deviation: the donor peaks at -1.07 dBFS in sustained vowels ("roadmap" 81.25,
"section" 83.26) and the live is mastered to 0 dBFS, so +1.8 dB would hard-clip 28 samples and +2.0 dB 42; +1.0 dB is clip-free
(peak -0.07 dBFS) and lands within ~1 dB of both neighbours. In the finished file: preceding sentence -15.3 LUFS (mean -14.9 dB),
donor sentence -15.7 LUFS (mean -16.5 dB, max -0.5 dB), following sentence -15.0 LUFS (mean -14.8 dB). If David hears it as soft,
`GAIN_DB = 1.8` is a one-line change (it will clip those 28 samples by 0.7 dB).

**Picture.** The map board now arrives at the graft start (output 2190, 0.35 s before the donor's "This"), where the live's map
arrived at 2211, after its sentence had begun. The leg is rendered from the current section-map JPG (compact, push=False, canvas
1600x900 with the 830-tall board centred) with the live's own ring sequence and colours per Edit Spec 5: row 1 purple `#4f2fc4`
[80,127,1520,319] at the live's f2330 (output 2312), row 2 blue `#1652f0` [80,319,1520,471] at f2635 (2617), row 3 teal `#0e8f86`
[80,471,1520,663] at f2813 (2795), takeaway banner `#6e51ff` tracing the gold banner [40,702,1560,790] at f3238 (3220), held to the
board's end at 3389. Rows re-measured on the current JPG (same rects as the 2026-09-11 build). Full view before the first ring: 122
frames (4.07 s). State frames: `build-v3/states-map.jpg`, `state-map-*.jpg`. Leg origin 2208 is a frame-index origin only (so the graft's
114 leg frames run straight into the kept span at 2322); it is not a live cut.

## Boards kept as the live has them (verification against course-assets/)

- **Close (live 4184-4481 → output 4166-4463):** kept as shipped, frame for frame (mean diff vs the live 1.6, encode noise; the corner
  cleaner is a verified no-op on these frames, 0 px changed). **It differs from the current page asset:** the live's close was rendered
  from the pre-2026-09-15 close capture (pill 590 px wide at frame scale, lavender stage), while today's
  `build-your-skills-opener-close.jpg` (0b9a7f70…, dated 2026-09-15) renders the pill 719 px wide on a white stage
  (`make_close_board.py --lesson openerskills`). Out of scope here per the brief; re-rendering it is `b.mark_close_start()` +
  `b.make_close("openerskills")` before the last `keep`, if David wants it in this ship.
- **Section map:** the live's map picture (2211-3407) also predates the 2026-09-15 asset (title position and banner inset differ by a
  few px, `map-live-vs-current.jpg`); it is replaced by the current asset in this build anyway. The canvas surround is the JPG's own
  matte colour (white) above and below the 830-tall board, as the v10 Understand AI map leg has it; the live bled the lavender stage.
- No other course boards appear in the live (the remaining spans are Notebook drawings).
- The live's Notebook spans carry no Gemini corner mark (mark_strength ≤ 0 on sampled frames); the render's cleaner pass over them
  changed only encode-level pixels (corner box max diff 9-27, the same as whole-frame h264 noise).

## Checks (Edit Spec 10)

1. **Frame count.** Decoded 4463 = plan (4481 - 132 + 114). Card leg 473 frames, map leg 1199 frames, each decoded exactly
   (`render_legs` assert).
2. **Transition guard.** 14/14 boundaries passed (`build-v3/guard/`): card rings 190, 220, 269, 299, 366; card out 473; graft in 2190;
   graft out 2304; map rings 2312, 2617, 2795, 3220; map out 3389; close in 4166. Strips inspected at 473 (last card frame f472,
   f473 already the notebook drawing), 2190 (f2189 Human Durability, f2190 the unmarked map at full view), 2304 (held board, delta
   0.0; row-1 ring pops at 2312), 3389 (f3388 map with banner ring, f3389 the book/tablet drawing), 4166 (f4165 notebook hands,
   f4166 the close at z=1). One cut at each, no intermediate frames.
3. **Pauses.** None added. The two gaps around the graft measured 1.67 s and 0.59 s against the live's 1.69 s and 0.66 s (above).
4. **Ring frames.** All settled ring frames inspected at full resolution (`state-card-0216/0246/0295/0325/0392/0472.jpg`,
   `state-map-0148/0453/0631/1056/1198.jpg`): right line or row, complete inside the ring, nothing clipped, 5 px stroke at the wide
   camera (1600-px board filling the 1280 frame). The card's five rings are tight to their lines; the map's three row rings span the
   card's full width including the number chips, as the live's did; the banner ring traces the gold banner edge to edge.
5. **Density / full view.** Both boards compact, static (push=False). Card opens unmarked at frame 0 for 6.33 s; map opens unmarked at
   output 2190 for 4.07 s. Confirmed on `state-card-0000.jpg` and `state-map-0000.jpg`.
6. **Transcript (small.en on the finished file, 60-95 s):** "…yourself through practice. We will cover some specific AI techniques
   here, but our main focus is on that internal balance. We want to build the enduring human skills that belong entirely to you.
   This roadmap shows what we'll explore in this section. We begin by using AI with strict care and honesty. That means knowing what
   information to protect, and improving raw ideas through deliberate conversation. Next, we focus on the skills that appreciate and
   value as technology scales. Step 3 is about maintaining your flexibility." Donor words land at 73.44-76.02 (output). No phantom
   words at either join.
7. **Manifest.** `build-v3/edit-manifest.json`: protected files unchanged (live, donor, three JPGs, `lessons/Opener-Build.md`,
   `index.html`, `course-assets/manifest.json`) all True; corner mark declined 0 (1120 cloned, 1671 inpainted over the live's
   Notebook and close spans, which carried no mark). Nothing committed.

## Not auditioned by ear

Transcripts and level numbers do not certify audio. David should listen to:

- **72.1-73.5** (output): live "…belong entirely to you." → room tone → donor "This roadmap…" (voice, level, floor: live gap floor
  -57.6 dB mean, donor lead-in -64 dB).
- **76.0-77.4**: donor "…in this section." (its 0.4 s tail decays from -42 dB) → live "We begin by using AI…" (the gap after the graft
  averages -48.7 dB against -57.6 dB before it; no cliff measured, but this is the join most worth hearing).
- The card span 0:00-0:16 for ring timing against the paraphrased lines, and 1:13-1:53 for the re-timed map arrival and rings.

## Pre-existing, out of scope

- The live's close is the pre-9/15 close capture (above). The live's 1.5-1.7 s gaps at 0:26, 1:32 and 1:59 are the live's own.

## At ship (not authorized yet)

Copy to `course-assets/build-your-skills-opener/build-your-skills-opener.mp4`; cache key `20260922ship1` on `openerskills` in
index.html (currently `20260911ship1`); pill "3 min" → "2 min" (2:28.77, as the v10 Understand note did for 2:28), David's call;
manifest video sha256/bytes (line ~12275). The recaptured creed JPG and its manifest entry are already in the working tree from
today's capture and ship with it. The close-asset question above needs David's answer first if he wants one commit.
