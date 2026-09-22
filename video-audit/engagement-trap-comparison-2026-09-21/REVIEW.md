# Engagement Trap — rolls 3 and 4 against the live video (2026-09-21)

Five files reviewed end to end against the current lesson (`index.html` `EngagementTrapSection`, with
`lessons/engagement-trap.md` as the upload source): the two new rolls, the live 2026-09-08 video, and
rolls 1 and 2 as donor candidates. Bundles for all five are in this folder.

**Verdict: roll 4 is the base — REPAIR, with two grafts. Roll 3 is a REROLL and should not be built on.
The live video is the weakest of the five and is missing the entire last third of the current lesson.**

The headline is not that roll 4 beats roll 3. It is that **the live video no longer teaches the lesson**:
it has no Meta settlement, no Board 4, no scope distinction, and it does not speak either closing line.
Roll 4 lands all of that correctly.

---

## The live video is out of date, not merely imperfect

`course-assets/engagement-trap/engagement-trap.mp4` (4:01, 2026-09-08) predates the lesson's current
final section. Against today's page:

| Lesson point | Live video |
|---|---|
| Meta settlement (Aug 2026, up to $17.1B, denied wrongdoing, U.S. teen accounts) | **MISSING** — never mentioned |
| Board 4, all four stopping-point items | **MISSING** — board never taught |
| Scope distinction (social media vs. AI chat) | **MISSING** |
| Closing lines, verbatim and in order | **MISSED** — paraphrased into one sentence: "True digital agency requires knowing exactly what you came for and decisively choosing what happens next once it is achieved." |
| "Both chats answered the question. Only one ended there." | **MISSING** |
| "The Engagement Trap is spending time you never decided to spend." | **MISSING** — "This phenomenon is an engagement trap." |
| Half a million human lifetimes | **MISSING** — only "Raskin himself later publicly expressed regret" |
| "No thanks. That's all I needed." | present @3:48.50, but moved out of the slope exchange and used as a closing tip |

That is four hard requirements missed and three essential points absent. The 2026-09-18 repair (v2) was
an attempt to patch two of these from rolls 1 and 2; it was never shipped, and it could not have fixed
the Meta section, because neither donor roll contains one.

---

## LESSON: engagement-trap · CANDIDATE: `Prompts/engagement-trap-4.mp4` (3:38)

**VERDICT: REPAIR** — the strongest spine by a wide margin; two whole-beat grafts close the only real gaps.

TEACHING POINTS:
- Hook, "helpful conversation that keeps going" — RICH @0:00
- The three follow-up offers, quoted — RICH @0:08.56 "want me to expand on this? Should I add examples? Want me to format it as a study guide?"
- Extra help is useful, which makes it easy to accept — RICH @0:20.60
- The trap is continuing **without deciding** — RICH @0:24.36 "You fall into the trap when you continue the interaction without making a conscious decision to do so."
- Board 1, the slope question — RICH @0:33.66, quoted from the lesson
- Board 1, the AI's actual answer (what slope means, the formula) — **THIN** @0:38.50 "The AI answers, then offers an example." The live video is the only one of the five that speaks the formula.
- Board 1, the stop ending — RICH @0:41.14 "No, thanks. That's all I needed." / "Done in one minute."
- Board 1, the trap ending — TAUGHT @0:47.62 "Sure." / "25 minutes later, you're taking a quiz."
- **"All of it was useful. None of it was what you opened the chat to do."** — **MISSING**
- Board 1 takeaway — TAUGHT @0:51.10 "Both answered the initial question, but only one ended there."
- Definition line — TAUGHT @0:54.86 "spending time you never originally budgeted" (lesson: "never decided to spend"; "budgeted" softens the decision, which is the lesson's whole point)
- Raskin, 2006, friction, removed the click — RICH @0:59.22
- Board 2, both sides and the takeaway — RICH @1:06.26 … "That missing click was friction, but it was also a choice."
- Half a million human lifetimes — RICH @1:28.22
- **Autoplay / streaks / games ("once you see it, you see it everywhere")** — **MISSING**
- Board 3, the missing page break, answer ends / conversation doesn't — RICH @1:34.22
- Board 3 takeaway, knowing when you have what you came for — RICH @1:48.42
- Why companies want engagement (return frequency, session length, ads/purchases/subscriptions, habit) — RICH @1:56.14
- Meta settlement — RICH @2:13.26, every element correct
- Board 4, all four items with their numbers — RICH @2:44.98 (parent-only two-hour cap; after 15 minutes continuous and again at 60 and 90 minutes total; midnight to 6 a.m.; "A forced stopping point gives you a chance to choose.")
- Scope distinction — TAUGHT @3:19.38
- Closing lines — RICH @3:35.10, exact, in order, nothing after

HARD REQUIREMENTS:
- "No thanks. That's all I needed." — **MET** @0:43.46
- Both chats answered / only one ended there — **MET in substance** @0:51.10 ("Both answered the initial question")
- "up to $17.1 billion", not paid — **MET** @2:18.74
- Meta denied wrongdoing — **MET** @2:25.50
- U.S. teen accounts — **MET** @2:29.98
- Board 4, every item spoken — **MET**
- Two closing lines, exact, nothing after — **MET** @3:35.10–3:38.70

ERRORS: none.

SOURCE_QA: PASS.

EDITING NOTES:
- Notebook invents an on-screen phone panel captioned "U.S. TEEN ACCOUNT — Default State: Unrestricted"
  with invented rows (Continuous Autoplay / Unbounded Screen Time / Night Notifications). Those are not
  Meta's stated defaults; cover with Board 4 or a drawn scene.
- An on-screen card reads "$17.1B REGULATORY SETTLEMENT" with no "up to". The narration is correct; the
  card is not. Cover it.
- Persistent board-furniture narration: "This comparison chart shows…", "On the left… On the right…",
  "This graphic breaks down…", "The left panel shows…". The content is taught underneath, so this is a
  style cost rather than a teaching failure, but it is the one place roll 4 reads the screen instead of
  the student.
- Carries the Gemini corner mark (5/148 sampled), as every roll does; removed at build.

---

## CANDIDATE: `Prompts/engagement-trap-3.mp4` (3:50)

**VERDICT: REROLL — do not build on it.** Two failures are disqualifying on their own.

- **Factual, @3:04:** "This **$17 billion price tag is the cost** of building a system that valued time on
  screen over the well-being of the people using it." That states the settlement as money paid, which the
  prompt explicitly forbids ("'Up to' is a conditional maximum; do not say that Meta paid $17.1 billion").
  It says "up to" correctly at 2:48 and then undoes it sixteen seconds later.
- **Visual, 2:36–2:46:** the Meta beat is a **photograph of a real Meta corporate building carrying the
  trademarked logo** — confirmed by eye at frames 4740–5010. The prompt bans logos and stock photos, and
  the ship checklist bans unlicensed stock photography. The narration points at it: "the company behind
  **this meta logo**", which also means the roll never says "Meta, the company behind Facebook and Instagram."
- **Board 4 is not taught**, only pointed at: "The left panel shows a two-hour daily limit. The center
  describes prompts interrupting continuous use. Finally, the right panel shows nighttime blocks."
  Not one number survives — no parent-only, no 15/60/90, no midnight to 6 a.m.
- Board 1 is generic ("You ask an AI for a math formula"); the slope question and the AI's answer are gone.
- The opening replaces the lesson's AI-chat framing with a scrolling-app one ("opening an app… it's been an hour").
- Good beats it does own: autoplay/streaks/games @1:38, and the closing lines are exact @3:45.

Roll 3's only unique contribution is its autoplay run, and rolls 1 and 2 both carry a better one.

---

## BEST-OF PLAN: engagement-trap

```
BASE: Prompts/engagement-trap-4.mp4 — the only roll that teaches the Meta section and Board 4
      correctly, speaks both closing lines exactly, and keeps the lesson's own framing throughout.

  Board 1's trap ending (examples, graphs, practice problems, a quiz) + "All of it was useful.
  None of it was what you opened the chat to do."
      roll 4 THIN/MISSING @0:47.62 "Sure. 25 minutes later, you're taking a quiz." (one item of four,
      and the useful/none line absent) | roll 2 RICH @0:49.86-1:01.54, both beats in one run, second
      person | roll 1 RICH @1:04.50-1:24.50 but THIRD person ("the student... they")
      — TAKE roll 2, under Board 1, as a replacement rather than an insert

  Autoplay / streaks / games
      roll 4 MISSING | roll 1 RICH @2:22.50–2:42.50 | roll 2 TAUGHT @2:00.50 | roll 3 TAUGHT @1:38
      — TAKE roll 1, under Board 2 / the Notebook scroll scene (replacing roll 4's 84.5-99.1)

  Board 1, the AI's answer and formula, and its three offers
      roll 4 THIN @0:38.50 "The AI answers, then offers an example." | live RICH @0:19-0:27 "It
      provides a clear definition and the precise formula, y2 minus y1 over x2 minus x1" AND
      @0:33.50-0:39.50 "It asks if you want it to walk through an example, draw a graph, or generate
      a few practice questions" - second person, so compatible | roll 1 has the three offers but in
      third person; rolls 2-3 no better than roll 4
      — DAVID'S CALL, not assumed. The live video is the only donor, and at 183.9 Hz against roll 4's
        173.9 Hz it is the widest voice gap in the set (within the 167-186 Hz spread Document Trap
        shipped, but audible as a slightly different delivery). Needs -1.0 dB.

GRAFTS: 2 planned, both under boards; a third (the AI answer/offers, from the live video) is
offered rather than assumed.
```

**Measured feasibility.** Boundaries below are verified against word-level timings, not segment
transcripts; every cut sits inside a measured silence (ffmpeg silencedetect, −40 dB / 0.12 s) rather
than on its edge, so no first or last word is clipped.

| Graft | Donor span | Lands in roll 4 at | Level / voice |
|---|---|---|---|
| Board 1's trap ending **and** the "useful / none of it" line (one run) | roll 2 **49.75 → 62.0** (12.2 s): "Accept, and 25 minutes later, you've read extra examples, analyzed graphs, and taken a quiz. All of the extra material provided was accurate and useful. None of it was what you opened the chat to do." — in the quiet 49.62–49.87, out in the quiet 61.76–62.26 | replaces roll 4 **45.8 → 50.65** (4.85 s): "On the right, you accept. Sure. 25 minutes later, you're taking a quiz." — in the quiet 45.57–46.01, out in the quiet 50.48–50.83 | roll 2 −15.90 LUFS vs roll 4 −16.81 → **−0.9 dB**; 177.8 Hz vs 173.9 Hz |
| regret + half-million + autoplay/streaks/games | roll 1 **133.82 → 166.85** (33.0 s): "Raskin later regretted…" (133.76) through "…their own invisible version of the missing page break." (ends 166.66), both ends bracketed by quiet | replaces roll 4 **84.5 → 99.1** (14.6 s): "Raskin later expressed regret…" (84.78) through "…to hold your attention." (ends 98.56); roll 4 resumes at "When the answer ends, the conversation continues." | roll 1 −17.19 LUFS → **+0.4 dB**; **173.9 Hz, identical to roll 4** |

The second graft is a replacement rather than an insert because roll 4 runs "…every single month."
(93.28) straight into "AI chat interfaces…" (93.88) with no gap over 0.08 s at −42 dB — there is nowhere
to insert. Taking roll 1's longer run swallows that seam, lands both ends in real silence, and hands back
the regret sentence and the half-million estimate in the same breath. Net **+18.5 s**, putting the
candidate near **3:57**.

**Provisional board plan** (rects measured at build, per Edit Spec 1b):

| Board | Asset | Treatment |
|---|---|---|
| 1. One Answer. Two Endings. | `engagement-trap-comparison.jpg` 1600×1508 | Dense. Full view, then dive to the exchange, then to each outcome column as it is spoken; banner ringed on "Both answered…" |
| 2. What Infinite Scroll Removed | `engagement-trap-scroll.jpg` 1600×885 | Compact. Ring each side on its spoken onset; banner on "friction, but it was also a choice" |
| 3. AI Won't Quit for You | `engagement-trap-stopping-point.jpg` 1387×1134 | Post-only course image, never uploaded. Illustration walk, no rings on the drawing |
| 4. Putting the Stopping Points Back | `engagement-trap-stopping-points.jpg` 1600×860 | Dense, three legs — one per card as its numbers are spoken; banner on the takeaway |
| Close | `engagement-trap-close.jpg` 1284×600 | Standard close |

Note: `engagement-trap-stopping-point.jpg` (Board 3) is the **uncommitted** refreshed illustration from
the cast batch. If the build uses it, it ships with the video, exactly as Document Trap's did.

---

## At ship time

`index.html:1120` carries **no cache key** (`engagement-trap.mp4`, "4 min"), the same gap Document Trap
had. A shipped rebuild needs a key, and the pill re-checked against the final runtime.

## Nothing built

No candidate was produced. The live video, rolls, lesson and boards are unchanged.
