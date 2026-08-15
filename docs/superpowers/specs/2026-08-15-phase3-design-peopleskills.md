# Phase 3 design — Communication & People (`peopleskills`)

**Date:** 2026-08-15 · Task 1 of `docs/superpowers/plans/2026-08-15-finish-smarter-phase3-new-lessons.md`
**Sources read:** `2026-08-15-finish-smarter-dedupe-audit.md` (David's additions, items 1a/1b), `index.html`
(`IntegritySection` + embedded `PrivacySection` 9831–10529, `CreativeThinkingSection` 8411–8514,
`BeCuriousSection` 8515–8579, `SECTION_META`/`SECTION_GROUPS`/`CLOSE_BOARDS`), `briefing.md`,
`docs/parking-lot.html`.

All copy below is drafted in David's voice and is meant to be built as written. No em-dashes, no
exclamation points. Numbers inside scenarios are fictional student-project data, clearly framed as
such; there are no real-world statistics in this lesson and none should be added.

---

## Thesis

**Everyone got the same AI on the same day, so what is left to be good at is people: saying it so it
lands, being someone worth working with, and getting a group to actually move.**

---

## Arc position

**Before:** Habits for the Road (`integrity`, the merged integrity + privacy lesson). It is the last
lesson about the tool. It ends on privacy as a reflex and hands the reader off with two habits.

**After:** Creative Thinking (`creativethinking`). That lesson owns the angle you bring to a problem
before AI sees it: See the obvious, Question the assumption, Connect the unconnected, Push past the
first decent idea, Pick the angle and own it. This lesson must not touch idea generation,
cross-domain thinking, or "what makes your work yours." It stays human-to-human: delivery,
collaboration, leadership. The handoff is clean because this lesson ends on people and that one
opens on the work.

**Gates:** `integrity` → `peopleskills` ("Next: " + approved label); `peopleskills` →
`creativethinking` ("Next: Creative Thinking").

**Opening bridge intent:** the transition lives at the top of this lesson, per the house rule. It
does two things in three paragraphs and names no other lesson: it marks the pivot (everything until
now was about a machine, this one is not), and it earns the pivot with the design insight (the day
everyone got the same AI, the output stopped separating people, so something else has to). No
forward reference at the bottom; the lesson lands on its own beat.

**Known collision to manage:** `creativethinking`'s opener currently runs the same premise
("Everyone in the room has the same AI"). In the final order this lesson says it first, which turns
Creative Thinking's second paragraph into a restatement. See Judgment call 2.

---

## Structure

Ordered beats. No illustration is proposed; the three boxes carry the visual load and the lesson is
already the section's densest new build. Component vocabulary is the shared kit only.

### Beat 1 — LessonHeader

`LessonHeader` with subtitle: **"The part the tool can't reach."**

### Beat 2 — Opener (3 × BodyP, no kicker)

> Everything until now has been about a machine. What it does, how it works, where it breaks, and
> how not to get played by it. This lesson is about people, and it's the first one here that has
> nothing to do with the tool.

> Here's why it belongs at this point. The day everyone got the same AI, everyone got the same first
> draft. Your classmates can generate a solid essay. So can the kid who never reads. So can you.
> When the output stops separating people, something else has to.

> AI can synthesize almost anything. It can't be trusted by anyone. People still choose who to work
> with the way they always have: by who explains things clearly, who does what they said they'd do,
> and who they believe when it counts. Three skills sit on top of each other here, in order. Each
> one is more human than the last, and that is exactly the order of how hard they are to hand off.

### Beat 3 — Rung 1 kicker + prose

`SectionKicker`: **"1. SAY IT SO IT LANDS"**

> AI can write your presentation. Then Thursday comes, and it's you standing up there, and none of
> the writing helps. Delivery is a live skill. You are watching faces, hearing the room go quiet or
> go restless, and adjusting while you talk. There is no draft for that.

### Beat 4 — Rung 1 demonstration (`ShowcaseBox`)

Kicker: **"SAME IDEA, TWO DELIVERIES"**
Intro: "One group project on water use in your district. One point to make. Here's the version that
came out of a chat window, and the version that works out loud."

Two white inner cards:

- **WHAT THE DRAFT SAYS** — "Our research indicates that residential water consumption in the
  district has increased 18% over the past decade, driven primarily by outdoor irrigation during the
  summer months."
- **WHAT YOU SAY** — "Our district uses 18% more water than it did ten years ago. Almost all of the
  increase goes on lawns, in July and August. We're not drinking more. We're watering more."

Closing line inside the box: "Same fact, two builds. One is written to be read. One is built to be
heard: short sentences, one number, and a picture you can hold."

### Beat 5 — Rung 1 landing (BodyP)

> Two more moves live inside this one, and both happen while you're talking. Reading the room is
> noticing you lost people at slide three, and stopping to fix it instead of pushing to slide four.
> Listening is the harder one, because most people spend the other person's sentence loading their
> own. When your teammate says "I guess we could cut the survey," the whole message is in the
> "I guess." Ask about it.

### Beat 6 — Rung 2 kicker + prose

`SectionKicker`: **"2. BE THE ONE PEOPLE WANT ON THE TEAM"**

> Four people, one slide deck, one grade. AI can write every section of it. What AI cannot do is the
> part that actually sinks group projects, and it is never the work. It's the guy who stopped
> answering the group chat five days ago.

> Most group problems aren't people being lazy. They're people being something, and you can usually
> tell which.

### Beat 7 — Rung 2 demonstration (`LabeledCardStack`, stack form, per-card accents, `meansLabel: "WHAT YOU DO"`)

1. eyebrow **THE ONE WHO WENT QUIET** · headline "Two check-ins, no reply."
   body: "Quiet usually isn't lazy. It's someone who is behind, embarrassed, or buried in something
   you can't see from a group chat."
   means: "Text him directly, not the group. Ask if he's okay before you ask where the slides are."
2. eyebrow **THE ONE WHO TOOK OVER** · headline "She's done four sections and rewritten yours."
   body: "Taking over usually comes from not believing it'll get done otherwise. Every time it slides,
   the belief gets stronger."
   means: "Claim a piece out loud with a day attached, then deliver it. That's how the belief changes."
3. eyebrow **THE ONE WHO AGREES WITH EVERYTHING** · headline "'Yeah, sounds good' to every idea."
   body: "Agreement that costs nothing tells you nothing. Sometimes it's politeness. Sometimes it's
   someone who thinks the plan is bad and doesn't want the fight."
   means: "Ask for the objection on purpose: 'What's the worst part of this plan?' Get the real answer
   before Thursday."

### Beat 8 — Rung 2 landing (BodyP ×2)

> Notice what those three moves have in common. They're direct, they're private, and they're about
> the person before the task. That's most of what conflict resolution actually is. The version that
> fails is the one everybody reaches for instead: posting "some people aren't pulling their weight"
> in the group chat and hoping the right person feels bad.

> And none of it works if you start the week the project is due. The people who get help fast are
> the ones who gave it first, back when nothing was riding on it.

### Beat 9 — Rung 3 kicker + prose

`SectionKicker`: **"3. GET A GROUP TO ACTUALLY MOVE"**

> Leading peers is the hardest one on the list, because you have no authority at all. Nobody made
> you the boss. Everyone can walk away. In a club, on a team, in a group project, the only thing you
> have is whether people want to go along with you. Which means leadership stops being a personality
> and turns into a few things you say out loud.

### Beat 10 — Rung 3 demonstration (`ShowcaseBox`, three quoted lines)

Kicker: **"WHAT IT SOUNDS LIKE"**
Intro: "Three sentences. Each one costs the person saying it something, and that's exactly why it
works."

- "I'll take the setup shift." → "The leader takes the worst job first. Everything you ask for after
  that costs less."
- "That was Priya's idea, and it's better than mine." → "Credit given in public is the cheapest thing
  you will ever buy trust with."
- "We're deciding this today. I say option two." → "A group with no decision drifts. Somebody has to
  say the sentence and be the one who's wrong if it's wrong."

### Beat 11 — Rung 3 landing (BodyP)

> None of that needs a title, a personality type, or a speech. It needs you to say something true,
> take the hard part, and then actually do it. Do that three times in a row and people start looking
> at you when it's time to decide.

### Beat 12 — Payoff (`SectionKicker` + BodyP)

`SectionKicker`: **"The more human it is, the harder it is to hand off."**

> Run the three back down the ladder and watch where AI stops. It can draft your script, and it
> can't stand up in front of the class. It can write the message to your teammate, and it can't be
> the person he trusts enough to answer. It can produce a flawless plan for Saturday, and it cannot
> make five people show up. That isn't a gap a better model closes. The higher you go up those
> three, the less of it there is to hand off.

### Beat 13 — `closeBoard("peopleskills")`

### Beat 14 — Capstone TRY IT (see below)

### Beat 15 — `LessonRule` + `NextLessonGate` ("Next: Creative Thinking")

---

## What's NEW to write

Everything. This lesson inherits no survivor copy from the audit's named lists. Units to write:

1. Lesson subtitle.
2. Opener, three paragraphs (pivot + design insight + ladder preview).
3. Rung 1: kicker, intro paragraph, `ShowcaseBox` "SAME IDEA, TWO DELIVERIES" (2 cards + closing
   line), landing paragraph carrying reading-the-room and active listening.
4. Rung 2: kicker, two intro paragraphs, `LabeledCardStack` (3 cards × eyebrow/headline/body/means),
   two landing paragraphs (conflict resolution + relationships built early).
5. Rung 3: kicker, intro paragraph, `ShowcaseBox` "WHAT IT SOUNDS LIKE" (3 quoted lines + gloss),
   landing paragraph.
6. Payoff kicker + paragraph.
7. `CLOSE_BOARDS.peopleskills` pill + sticky.
8. Capstone TRY IT: title, lead, 4 scenarios × 3 options × headline + feedback (12 feedback blocks).
9. Registry entries: `SECTION_META`, `SECTION_COMPONENTS`, `SECTION_GROUPS`, gate re-chains, opener
   overview card + bridge line.

Concepts sourced from the audit's David's additions 1a (persuasive speaking, storytelling, reading a
room, active listening) and 1b (teamwork, conflict resolution, leading peers, authentic
relationships). The source register is edu-consultant; none of its wording appears above.

---

## Close board

- **pill:** "AI can write it. It can't be the person in the room."
- **sticky:** "Say it clearly, be easy to work with, and people follow."

The payoff paragraph deliberately ends on the ladder ("the less of it there is to hand off") so the
board is not a restatement of the line above it.

**Parked line check:** "curiosity is the new currency, judgment is the new expertise, adaptability is
the ultimate security" lives only in the audit doc (David's additions, item 4), not in
`docs/parking-lot.html`. Leaving it unclaimed: it names curiosity, judgment, and adaptability, and
none of the three is this lesson's rungs. It belongs on Skills That Matter, Make Your Move, or the
section's final board.

---

## Capstone TRY IT

**Title:** "What's the Human Move?"
**Mechanic:** four scenarios, each a short setup plus one `QuizBlock` with three full-sentence
options. Same pattern as Creative Thinking's "Same Problem, Different Thinking" (setup text above a
`QuizBlock`), inside a mint `InteractiveBox` with a numbered rule between items. Per-option
`headline` + `feedback`. No `Takeaway` afterward.

**The ONE skill it drills:** recognizing which part of a situation only a person can do, and doing
it instead of routing around it.

**Wrong-answer design:** every item carries exactly one over-delegation wrong answer (hand it to AI,
or let a document stand in for a conversation) and one social-avoidance wrong answer (go indirect,
go quiet, or absorb the work alone). Both wrongs are the comfortable choice, which is the point.

**Lead:** "Four situations, three options each. Some are fast, some are comfortable, and one of them
is the move that changes the outcome."

### Item 1 — delivery

**Setup:** "Your group's presentation is Thursday. The slides are done and they look good. You're
the one presenting."
**Statement:** "It's Wednesday night. What do you do?"

- ✗ "Have AI write a word-for-word script and memorize it." · **You'll sound like a page.** ·
  "A script written to be read isn't built to be heard, and the second you lose your place you have
  nothing underneath it. Worse, you can't adjust: if the room checks out at slide three, the script
  marches on to slide four anyway. Know your three points cold, then say them like a person."
- ✗ "Trade jobs so someone else presents and you make the handout." · **That's the swap that costs
  you.** · "It's the comfortable option, and it's the one that keeps you bad at this. Presenting only
  improves with reps in front of actual people, and there is no way to get the reps without the
  people. Thursday is a cheap one. Take it."
- ✓ "Say it out loud twice to one friend and ask what didn't make sense." · **One friend beats ten
  rehearsals.** · "Out loud is the only way to find out that the sentence you wrote is unsayable. And
  the question does the real work: 'what didn't make sense' hands you the confusion you can't see from
  inside your own head. Fix those two spots and you're ready."

### Item 2 — conflict

**Setup:** "Your teammate has the sources section. It's due Thursday. He hasn't answered the group
chat in five days."
**Statement:** "It's Tuesday. What's your move?"

- ✗ "Have AI write his section so the project goes in on time." · **The project survives. Nothing else
  does.** · "You solved Thursday and kept the actual problem. You still don't know what happened, he
  still hasn't done anything, and now there's a quiet grudge inside a group that has to work together
  again next month. Submitting a section nobody in the group wrote is its own problem on top of that."
- ✗ "Post in the group chat that some people aren't pulling their weight." · **That's a message to
  everyone except him.** · "Indirect callouts land on the people already doing the work, and the one
  person you meant it for gets to ignore it without ever answering. If you have something to say to
  one person, say it to one person."
- ✓ "Text him directly: ask if he's okay, name Thursday, offer to split it." · **Direct, private,
  person first.** · "Five days of silence usually isn't laziness. It's someone who is behind, buried,
  or dealing with something you can't see from a group chat. Asking first costs you nothing and
  changes what you learn. Naming the deadline and offering to split it gives him a way back in that
  doesn't require an apology."

### Item 3 — reading the room

**Setup:** "First meeting of the club you're starting. Eight people came. You're four minutes into
the pitch and three of them are on their phones."
**Statement:** "What do you do?"

- ✗ "Finish the pitch. It's good, and cutting it short looks weak." · **You're presenting to a room
  that left.** · "The pitch being good is not the same as the pitch landing, and the room already told
  you which one is happening. Pushing through is the most common version of this mistake: treating
  your plan as the thing that matters instead of the people in front of you."
- ✗ "Wrap up early and post the full plan in the group chat tonight." · **You moved it somewhere
  quieter.** · "The people who stopped listening in the room are not going to read it later. And you
  just gave away the one thing a room gives you that a chat doesn't: you can ask a question and watch
  what happens on eight faces."
- ✓ "Stop, and ask them what would actually make them come to this." · **Hand the room back.** · "The
  phones are information, so use them. A real question flips people from audience to participants, and
  the answers tell you what this club has to be if you want anyone there in week three. Reading the
  room only counts if you do something with what you read."

### Item 4 — leading peers

**Setup:** "The fundraiser is Saturday. Five people said yes to helping. It's Sunday night and
nobody has done anything."
**Statement:** "You're not in charge of anyone. What works?"

- ✗ "Ask AI for a project plan and post it in the group chat." · **A plan is not a commitment.** ·
  "You'll get a clean list of tasks with nobody's name on any of them, and a task with nobody's name
  on it doesn't get done. AI is genuinely good at breaking a job into steps. Getting one specific
  person to own step three on a specific day is the part it can't do for you."
- ✗ "Do all of it yourself on Friday night." · **It gets done, and it never gets easier.** · "This is
  avoidance dressed up as responsibility. You dodge five uncomfortable asks, and you teach five people
  that nothing happens if they do nothing. Next time is the same Friday night, alone, with more to
  carry."
- ✓ "Call three of them, give each one job and one day, and take the worst one yourself." · **Names,
  days, and you first.** · "One person, one job, one day is the whole mechanic. A call is also harder
  to scroll past than a message in a chat. And taking the worst shift yourself is what buys you the
  right to ask for the rest."

---

## SECTION_META proposal

- **kicker:** `"PEOPLE STILL PICK PEOPLE"` (kickers are often vestigial; harmless either way)
- **label:** **"People Skills"** · alternative: **"In the Room"**
- **title:** not needed (label is short enough for the sticky bar)
- **icon:** 🤝 (`🤝`) — unused elsewhere in `SECTION_META`
- **slug:** `people-skills` (or `in-the-room`); the plan's placeholder `communication-and-people` goes
  away with the working title.

---

## Judgment calls for David

1. **Label.** "People Skills" is plain, matches the id, and reads clearly in the nav list. "In the
   Room" is sharper and matches the thesis and the close board, but it's opaque until you've read the
   lesson. Recommend "People Skills."
2. **The shared premise with Creative Thinking.** Both lessons hang on "everyone has the same AI," and
   in the final order this one says it first. Option A: keep this opener as drafted and trim Creative
   Thinking's second paragraph at build time (its first paragraph already carries the sameness point
   through the grader who has read it eight times before lunch). Option B: drop the same-AI framing
   here and open the lesson on trust alone. Recommend A: the design insight is the reason this lesson
   exists, and it should be stated where it's earned.
3. **Storytelling.** David's source item names "persuasive speaking & storytelling." The draft gives
   delivery a full box and treats storytelling as one line inside it ("a picture you can hold"). The
   fork is whether storytelling gets its own demonstration: one fact told as a statistic, then as
   thirty seconds about one person. It's a strong beat and it's another box in an already dense
   lesson. Recommend keeping it compressed; the delivery box already carries a plain-language rewrite.
4. **How loud the pivot is.** The opener names the turn outright ("this lesson is about people, and
   it's the first one here that has nothing to do with the tool"). The alternative is to just start
   with the group project and let the reader notice. Naming it makes the course's shape visible at the
   exact moment it changes, which argues for keeping it. Recommend as drafted.
