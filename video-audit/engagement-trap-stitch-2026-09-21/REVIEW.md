# Engagement Trap v10 — roll 4 plus five grafts (2026-09-21)

`Prompts/engagement-trap-v10.mp4` — 4:30.27 (8108 frames), built by
`scripts/video/build_engagement_trap_v1.py`. Comparison bundle for all five source files is in
`video-audit/engagement-trap-comparison-2026-09-21/`.

Built to David's approval of the three-graft plan. The live 2026-09-08 video predates the lesson's
whole final section; roll 4 teaches it correctly and speaks both closing lines exactly, so it is the
spine, with five whole-beat grafts closing what it compresses.

**SHIPPED 2026-09-21 on David's approval** as `course-assets/engagement-trap/engagement-trap.mp4`,
cache key `20260921ship22`, pill 4 min (the course uses "4 min" up to ~4:30 and "5 min" beyond:
4:25 -> 4, 4:37 -> 5). Board 3's refreshed illustration shipped with it, because the video is built
from it. The audio has been unchanged since v5 — v6 to v10 are picture and ring-colour repairs only.

## What it is made of

| | source | carries |
|---|---|---|
| spine | roll 4 | the lesson's order, the Meta section, all of Board 4, both closing lines |
| `answer` | live video, audio only, −1.0 dB | the AI's reply — "a clear definition and the precise formula, y2 minus y1 over x2 minus x1" and all three offers — which roll 4 reduced to "The AI answers, then offers an example." |
| `trapend` | roll 2, audio only, −0.9 dB | the full trap ending (extra examples, graphs, a quiz) **and** the lesson's own "All of the extra material provided was accurate and useful. None of it was what you opened the chat to do." |
| `regret` | roll 1, audio only, +0.4 dB | Raskin's regret, the half-million estimate, "You see the same underlying mechanic everywhere." |
| `everywhere` | roll 1, with its own footage, +0.4 dB | autoplay countdowns, streak counters, one more round — a beat roll 4 never speaks |
| `definition` | roll 1, audio only, +0.4 dB | "That is the engagement trap. You end up spending time you never originally decided to spend." — replacing roll 4's "never originally budgeted", which softened the lesson's point |

**David's note, 2026-09-21:** at the cut to the right-hand card the narration said only "Accept…", which
gave no signal that this was the second of two choices. Fixed by moving roll 4's own audio cut later so
it keeps **"On the right, you accept."** and starting roll 2's graft after its own "Accept," — so the
word is not spoken twice and the signpost comes from the spine's own voice. THE TRAP card now rings as
it is named. Roll 3's "On the right, the trap." was tried first and rejected: see the noise-floor note
below. David also asked whether the whole first 1:04 should come from roll 1; it should not — roll 1
never says "No thanks. That's all I needed.", never says "Both chats answered the question. Only one
ended there.", paraphrases the lesson's three quoted offers, and narrates that stretch in the third
person.

Roll 4 −16.81 LUFS / 173.9 Hz, roll 1 −17.19 / 173.9 (identical pitch), roll 2 −15.90 / 177.8,
live −15.82 / 183.9. The `regret` and `everywhere` grafts are one continuous run of roll 1 audio split
only so that Board 2 carries the first half and roll 1's own autoplay and streak panels carry the second.

**The grafts fixed the board walk, not just the words.** Board 1 has the AI's full reply printed on it
and the trap card lists Examples / Graphs / Practice problems / A quiz above its own closing line. With
roll 4 alone the camera would have dived to text nobody was reading. Now the blue ring lands on the AI
bubble as the live donor reads it, and the amber ring lands on the trap card as roll 2 lists its contents.

## QA

- **transition_guard: 17/19 pass.** The two remaining flags are the Board 1 camera dives (f1145, f1767),
  inspected frame by frame: continuous motion with per-frame deltas decaying 18.1 → 0.0 and 26.5 → 0.0,
  the ring arriving on cue, no stale frames. The guard's detector counts a smooth dive as repeated cuts.
- **Audio.** Every audio cut sits in measured silence: −55.5 dB or quieter across the seam at all six
  graft edges and the close. The closing line's decay is intact, falling naturally to −35.7 dB before the
  room-tone floor.
- **Noise floors measured on both sides of every seam** (added after the roll 3 attempt below). Every
  seam is within 5 dB except roll 4 resuming after the `definition` graft at 1:26.5, where roll 1's tail
  decays to −67 dB and roll 4's own pause runs −84 dB for about 250 ms before "This design logic…". That
  is a 17 dB step **down** into near-silence between two sentences; both sides sit more than 55 dB below
  speech, so it should be inaudible, but it is the one seam worth an ear.
- **Gemini mark: 0 hits across 181 sampled frames, 0 declined.**
- **All 19 row boundaries measured for a dropout**: none dips below its own quieter neighbour. Re-measured for a dropout, not just the graft edges: each cut sits at −55 dB or
  quieter with no dip below its own local floor. (A first pass flagged the Board 1 → Board 2 boundary at
  28 dB; inspected at 1 ms it is a clean silence-to-speech edge, the word rising from the floor after the
  cut. The metric was reading the edge, not a notch.)
- **Boards.** All four ring their own measured card bodies with no shadow trace or clipped text. Board 3
  rings only its banner, never the photograph, and its walk lands on the ribbon, then the STOP lever and
  hourglass, then pulls back.
- **Protected sources: 8/8 hashes unchanged.**
- **Transcript reads continuously**; all five grafts are undetectable in the prose.

### Three defects QA caught, and what caused them

All three were mine, not the engine's, and each is recorded in the build script so it is not repeated.

1. **v1 leaked Notebook's own board render.** As the canonical Board 4 left the screen, roll 4's *own
   recreation* of the stopping-points board showed for four frames (source 5973–5976) — near-invisible
   because it resembles the real board. The same family of leak sat at Board 3's exit, where roll 4's
   leftover "Goal Achieved – Trap Avoided" panel held for two frames. Fixed with `picture_advance`: both
   rows resume the picture at the first clean source frame (3467, 5977) with `video_end` set so the
   borrowed picture holds rather than running into the next board render.
2. **v2 clipped two word tails.** The junction between the two roll-1 grafts was placed at 145.20 s
   because that sat in a measured silence — **in roll 4's silence list, not roll 1's**, which is the file
   being cut. In roll 1 that is the decaying tail of "everywhere."; its real floor is 145.50–145.72. The
   close had the same fault from the other direction: Whisper put the last word's end at 218.42 and the
   detector put silence at 218.67, but measured directly the word still sounds at −35 dB at 218.68, so
   cutting at 218.67 shaved the decay off "choose what happens next." Junction moved to 145.60, close
   extended to 218.78, both verified against the waveform.
3. **v4 used a donor with a 17 dB noisier room.** Roll 3 is the only roll that names the right-hand card
   ("On the right, the trap."), so it was grafted in first. Its pause floor is **−48.4 dB against roll 4's
   −65.9**: the faint tick at the cut was not a crossfade artifact but roll 3's room arriving, and it
   would have swelled under the whole sentence and dropped away again — the "noise-floor cliff" the ship
   checklist names. Dropped in favour of roll 4's own "On the right, you accept.", which needs no third
   donor and one fewer seam.

4. **v6 repaired David's three viewing notes and introduced a fourth fault doing it.** Swapping a picture
   for part of a row means splitting the row, and `keep()` crossfades its own edges into room tone — so a
   split inside running speech punches a hole. Measured in v6: the close split landed mid-word in "This
   rule applies to every digital tool you use." and dropped **30 dB for about 2 ms**, an audible click;
   the photo-cover split dipped 10 dB in a quiet inter-word gap. Both boundaries moved into measured roll 4
   silences (4129 and 6342). **A picture boundary may sit anywhere; an audio boundary may not.**

**The rules these failures point at:** Whisper's word timings run early, and a silence map only describes
the file it was measured from — verify a boundary against the waveform of the donor being cut. And match
the donor's **noise floor**, not just its loudness and pitch: a roll can sit within 1 dB LUFS and still
carry a room 17 dB louder in the pauses, which is where a graft actually joins.

## David's viewing notes, 2026-09-21 — all three repaired

1. **Wrong ring colour on Board 1's left card (0:59).** Correct, and it was three rings rather than one.
   Ring colour is measured off the artwork (Edit Spec section 5), and I had invented it: YOU STOP's own
   accent is **#1f58ee → BLUE** (v5 ringed it TEAL), and the two chat bubbles sit in a card with no locked
   accent so they take the neutral video purple (v5 had them PURPLE and BLUE). THE TRAP's #aa7a14 → AMBER
   was already right.
2. **A stock photograph at 3:07.** Roll 4 illustrates "harmed children and teens" with a photograph of four
   **identifiable real teenagers**, its own frames 4233–4358. Covered picture-only with roll 3's drawn
   gavel-and-binders panel, which now runs under "agreed to a settlement of up to $17.1 billion over claims
   that addictive social media features harmed children and teens." Roll 3 was rejected earlier for its
   noisy room, but that disqualified only its audio — a picture-only borrow carries no room tone. The whole
   video was then re-scanned for photographic frames: this was the only one.
3. **A second, zoomed-out closing message at 4:18–4:20.** Roll 4 plays its own close board from frame 6351.
   `mark_close_start()` is now called at frame 6342 — inside the preceding silence and nine frames ahead of
   it — which is that function's documented use: the standard close takes the screen exactly where the
   engine's own close arrives. Roll 4's version never appears.

## David's second viewing pass, 2026-09-21 — two board holds replaced with real footage

Both of these swap a board the narration had already moved past for footage that teaches the beat, and
between them they take 19 seconds off the board holds.

4. **Roll 4's own infinite-scroll panel (its 0:59-1:06) under the Aza Raskin narration (1:27-1:33).**
   Roll 4 draws "Aza Raskin / 2006 - Interaction Concept" contrasting **BOUNDED (PAGED)** — a list with a
   "Next [1] [2] [3] More" control — against **UNBOUNDED (STREAM)**. Board 1 had been holding here with
   the narration already onto infinite scroll. Board 1 now ends on time: **63.5 s -> 56.2 s**.
5. **Roll 1's own footage (its 2:14-2:22) under its regret / half-million narration (1:52-2:01).**
   An infinite feed on a phone beside a MONTHLY TIME CONSUMED counter animating up and landing on
   **500,000 Human Lifetimes / Month** exactly as the narration says "half a million". Board 2 had been
   holding over it: **30.4 s -> 18.4 s**. Because `regret` and `everywhere` are contiguous in roll 1,
   giving `regret` its own picture also erases the join between them - roll 1 now runs unbroken from
   1:52 to 2:25 under its own narration.

Two leaks surfaced doing this. Both fixed: roll 1 holds **its own recreation of the scroll board**
for three frames at 4008 before its scene cuts, which appeared as Board 2 left. `cover_intro=True` covers
them (`intro_cover_frames: 3` in the manifest).

And **David caught a fifth at 1:26** (v9): roll 4 holds its own recreation of the comparison board for
9 frames (1763-1771) before cutting to the Aza Raskin panel, so our Board 1 handed straight to its
lookalike. `RASKIN_PIC = 1772` advances the picture past it, and `video_end = 1983` stops the borrowed
picture before roll 4's own scroll-board recreation at the other end.

**The standing lesson.** Notebook holds its previous panel for a few frames after the audio has moved on,
so *every* picture boundary risks a stale leak at its leading edge - five instances in this one lesson
(Board 3's exit, Board 4's exit, roll 1's entry, roll 4's close, and the Aza Raskin entry).
`transition_guard` does **not** reliably catch them: it flags two visual cuts within six frames, and the
1:26 leak ran nine, so it passed the gate and only a human eye found it. Every picture edge in v10 has
since been inspected frame by frame - the four board arrivals, the four board exits, both roll-3 gavel
edges, roll 1's entry, roll 4's re-entry after the covered photo, and the close - and all are single
clean cuts.

## Still open (David's call)

- The on-screen card at ~3:25 reads **"$17.1B REGULATORY SETTLEMENT"** with no "up to", while the narration
  says it correctly. Flagged since the first review and still not covered; it can be covered the same way
  as the photograph.

## Notes for the eye test

- **Board 1 holds for 56.2 s**, down from 63.5 s. Still the longest board run in the course, but the
  camera dives to a different card for each beat and the board now leaves exactly when the narration
  turns to infinite scroll.
- **Two decode artifacts, not audio faults.** "Azaraskin" is Aza Raskin (the roll says "Raskin" correctly
  later). "daily street counters" is "streak counters": the word flips to "streak" under prompt bias
  because the /k/ assimilates into "counters", and roll 1's own on-screen panel reads "DAILY STREAK
  MECHANIC / 9 DAY STREAK".
- **The definition line is now roll 1's** "You end up spending time you never originally decided to
  spend.", against the lesson's "spending time you never decided to spend" — one word off rather than the
  paraphrase v3 carried.

## If David approves

1. Install over `course-assets/engagement-trap/engagement-trap.mp4`.
2. `index.html:1120` carries **no cache key** (`engagement-trap.mp4`, "4 min") — the same gap Document
   Trap had. It needs a key, and "4 min" is still right for 4:28.
3. `engagement-trap-stopping-point.jpg` (Board 3) is the **uncommitted** refreshed illustration from the
   cast batch; if this ships, that asset ships with it, exactly as Document Trap's did.
4. Committed with the build script, this bundle and the five-way comparison bundle. The nine superseded
   transition-audit rounds were deleted before committing; `transition-audit-v10/` is the shipped one,
   and this review records what each earlier round found.
