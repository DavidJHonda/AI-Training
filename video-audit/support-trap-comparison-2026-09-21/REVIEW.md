# Support Trap — rolls 1 and 2 against the live video (2026-09-21)

Three files reviewed end to end against the current lesson (`index.html` `SupportTrapSection`, with
`lessons/support-trap.md` as the upload source): `Prompts/support-trap-1.mp4` (4:08.20),
`Prompts/support-trap-2.mp4` (3:25), and the live `support-trap.mp4` (3:40, v2 shipped 2026-09-20 as a
narration repair). Bundles for all three are in this folder.

**Verdict: roll 1 is the base — REPAIR, with two grafts and one added pause. Roll 2 is not a base
(it misses three hard requirements) but it owns one beat nothing else has. Separately and urgently:
the live video contains a broken sentence that is on the site right now.**

This lesson carries the course's strictest accuracy requirements, because it tells a real mother's
account of her daughter's death. The prompt forbids inventing causes. **Neither new roll met that bar**,
and they fail it in different ways — see below. The line the lesson actually asks for survives only in
the live video, which is why the plan grafts it back in.

---

## Live video: a broken sentence is shipped

At 1:48–1:56 the live video says:

> "AI cannot take physical action. **Notice what you leave out of your prompts,** take responsibility,
> or check on you the next day."

That is Board 2's *What Is Missing* list — "AI cannot notice what changed, show up, take responsibility,
or check on you tomorrow" — with its governing "AI cannot" lost and "notice what changed" replaced by an
instruction to the viewer that means something entirely different. The sentence does not parse and does
not teach the board. Confirmed on two decoders (`small.en` and `medium.en` agree word for word), so it is
the narration, not a transcription artifact.

It is worth fixing whatever happens with these rolls. Roll 1 and roll 2 both have a usable replacement.

---

## LESSON: support-trap · CANDIDATE: `Prompts/support-trap-1.mp4` (4:08.20)

**VERDICT: REPAIR** — the only roll that speaks both safety-critical lines verbatim, and the most
complete on Boards 1 and 3. Its one serious fault has an identified donor.

TEACHING POINTS:
- Hook, patient/caring/understanding and "what happens when kind words are not enough" — RICH @0:00
- Board 1 scenario, both replies quoted including "We're at the table by the windows" — RICH @0:16–0:50
- "It might even sound kinder than the sister" — RICH @0:53 (the lesson's own turn)
- Definition — TAUGHT @1:06 "the specific mistake of confusing supportive language for actual support"
  (lesson: "Support Trap is mistaking supportive words for support" — the prompt asks for the Markdown's words)
- Board 2 *What Can Be Real* — THIN @1:16 "name a feeling or prepare for a hard conversation" (drops "organize your thoughts")
- Board 2 *What Is Missing* — THIN @1:22 "cannot notice physical changes. Take responsibility or check on you tomorrow" (drops "show up"; "notice physical changes" is weaker than "notice what changed")
- Board 2 takeaway — RICH @1:29 "Use AI to prepare for people. Never to replace them."
- All three roles, named and explained — RICH @1:33–2:14 (venting ends in the chat; preparation needs the final step; danger ends the chat)
- **Content note — MET, exactly: "The next story discusses suicide." @2:14.20**
- Reiley account — RICH @2:16–2:49: 2025, Laura Reiley, 29-year-old daughter Sophie Rottenberg, months of thoughts hidden from the people around her, the ChatGPT persona Harry, warmth and encouragement to seek help, and could not alert her family, contact her therapist, or bring anyone into the room. "Sophie ultimately died by suicide." @2:49
- **The black-box sentence — WRONG @2:56**: "**Because she relied on the bot**, the AI's isolated digital environment **actively** held details that made it harder for the real people in Sophie's life to understand the severity of her distress." The lesson says only "The chats held details that made it harder for the people around her to understand the severity of her distress." Roll 1 adds a cause for a real death and gives the software intent. The prompt forbids exactly this.
- Board 3, three actions — RICH @3:07–3:50, and the fullest version of step 2 ("cannot call anyone… cannot show up to protect someone… carries zero real-world responsibility")
- **988/911 — MET, exactly: "In the U.S., call or text 988 for crisis support. Call 911 if someone is in immediate danger." @3:21**
- "Safety always outranks secrecy" @3:42 — MET in substance (lesson has no "always")
- Board 3 takeaway — RICH @3:53
- **"Know When to Leave the Chat" — MISSING.** Roll 1 goes from Board 3's takeaway straight to the close.
- Closing lines — RICH @3:59, exact, in order, nothing after

HARD REQUIREMENTS: content note **MET exactly**; 988/911 **MET exactly**; attribution to Laura Reiley MET;
"died by suicide" MET; safety outranks secrecy MET; closing lines MET. **Failed: no invented causes.**

ERRORS: the black-box sentence above. SOURCE_QA: PASS.

EDITING NOTES:
- **No pause after the content note.** Measured gap is 0.52 s; the prompt asks for room for a pause. The
  live video leaves 4.33 s. An added pause is needed (Edit Spec section 6).
- Visuals over the Sophie passage are restrained and appropriate — an empty chair, a phone on torn paper,
  a literal black box, a drawn "real-world support system". No photographs, no people, no logos.
- Board-furniture narration throughout ("This guide defines…", "This is a protocol chart showing…").

---

## CANDIDATE: `Prompts/support-trap-2.mp4` (3:25)

**VERDICT: REROLL as a base** — three hard requirements missed, and it is weakest exactly where this
lesson can least afford it. Keep it as a donor.

- **Content note not exact** @1:52: "Please note, the following story discusses suicide."
- **988/911 not exact** @2:42: "In the US, you can call or text 988 for crisis support or call 911 if the danger is immediate" — merged into one sentence and reworded. The prompt requires the two sentences said distinctly.
- **Drops "by suicide"** @2:20: "After Sophie died, her mother described the chats as a black box." This is precisely the euphemism the 2026-09-19 repair was built to remove from the live video; shipping it would be a regression.
- **Drops Sophie's age** (roll 1 and the live video both have "29-year-old").
- **Invents a general mechanism** @2:24: "Pouring distress into an AI creates a false sense of communication, which can hide the severity of a crisis from the people who have the power to intervene." The lesson makes a specific statement about Sophie's chats; roll 2 converts it into a universal psychological claim.
- Drops "the AI's words might even be the kinder ones" and "We're at the table by the windows".

What it owns, and nothing else does:
- **"Know When to Leave the Chat"** @3:12: "Most of AI literacy is about how to use tools well. Here, using the tool well means knowing when to leave the chat." (lesson: "Most of this course…")
- **"Safety outranks secrecy."** @3:05 — exact, no added word.
- Board 2's "show up" @1:07, which roll 1 drops.

---

## BEST-OF PLAN: support-trap

```
BASE: Prompts/support-trap-1.mp4 — the only roll with the content note and the 988/911 lines verbatim,
      Sophie's age and surname, "died by suicide", and the complete Board 1 and Board 3 treatment.

  The black-box sentence
      roll 1 WRONG @2:56 (invents "because she relied on the bot" and "actively held")
      | roll 2 WRONG @2:24 (invents a general mechanism, and drops "by suicide")
      | live RICH @2:30.36-2:49.20 "After Sophie died by suicide, her mother described the chats as a
        black box. The AI offered empathetic words, but those private conversations held crucial details
        that made it harder for the people around her to understand how serious her distress was and to
        intervene."
      — TAKE the live video, replacing roll 1's 2:49.20-3:07.20. This is the repaired passage from the
        2026-09-19 work; it stays with the lesson's claim and invents nothing.

  "Know When to Leave the Chat"
      roll 1 MISSING | roll 2 TAUGHT @3:12 | live MISSING
      — TAKE roll 2, inserted before the closing lines.

  Pause after the content note
      roll 1 has 0.52 s | live has 4.33 s
      — ADD a selective pause; do not graft, the room tone is roll 1's own.

  Board 2's missing items
      roll 1 drops "organize your thoughts" and "show up"; roll 2 drops "name a feeling" and "notice what
      changed"; the live sentence is broken. No version speaks all of Board 2.
      — DAVID'S CALL, not assumed: grafting roll 2's "cannot take responsibility, show up, or check on you
        tomorrow" buys "show up" and loses roll 1's approximation of "notice what changed". A reroll is the
        only way to get the board whole.

GRAFTS: 2, plus one added pause.
```

**Feasibility.** Roll 1 −16.92 LUFS / 168.4 Hz, roll 2 −17.59 / 170.2, live −17.98 / 170.2 — all within
1.06 LU and 1.8 Hz. Pause floors are −60.6, −59.0 and −63.1 dB, within 4 dB, so no noise cliff (the fault
that disqualified roll 3 as an audio donor on Engagement Trap). Exact in/out frames to be measured against
each donor's own waveform at build time, per the two rules recorded in the Engagement Trap review.

**Provisional board plan** (rects measured at build):

| Board | Asset | Treatment |
|---|---|---|
| 1. Supportive Words versus Support | `support-trap-comparison.jpg` (post-only; refreshed cast, `?v=20260921batch8`) | Ring each reply as it is read, then the takeaway banner |
| 2. Use AI to Get Ready for People | `support-trap-role.jpg` | Two columns; ring each side on its spoken onset, banner on the takeaway |
| 3. If Someone May Be in Immediate Danger | `support-trap-danger.jpg` | Three legs, one per action as it is named; banner on the takeaway |
| Close | `support-trap-close.jpg` | Standard close |

## At ship time

`index.html:1136` already carries a cache key (`?v=20260920ship1`) and "4 min"; both need updating for a
new build. Board 1's refreshed illustration is already committed (`cc7e16e4`).

## Nothing built

No candidate was produced. The live video, rolls, lesson and boards are unchanged.
