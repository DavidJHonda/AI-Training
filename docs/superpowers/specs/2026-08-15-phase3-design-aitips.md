# AI Tips (`aitips`) — lesson design

**Date:** 2026-08-15 · Phase 3, new lesson for Finish Smarter
**Position:** Finish Smarter, beat "THE LAST OF THE AI", after Tune the Model (`choosemodel`), before Habits for the Road (`integrity`)
**Sources:** `THOUGHTPARTNER_INVENTORY` (2026-08-15 dedupe audit), `docs/parking-lot.html` ("Ask AI" + "Thought Partner" entries), neighbor lessons read in `index.html`
**Size target:** becurious-sized. Four short prose beats, one demonstration box, one four-row tip box, one landing beat, one TRY IT.

---

## Thesis

**Good AI users aren't typing magic words: they run a short list of one-sentence moves, on purpose, every time.**

---

## Arc position

**Before:** Tune the Model (`choosemodel`) ends on the temperature dial and the "App. Model. Effort." summary. The student has just finished setting the tool up.

**After:** Habits for the Road (`integrity`) opens with "You now know how AI works and how to use it well. Two habits decide whether that knowledge actually helps you." That opener already carries its own bridge and needs no change: AI Tips is the last of the how-to-use-it material, which is exactly what `integrity` says it is standing on.

**Opening bridge intent:** the previous lesson was about the settings around the box. This one is about what goes in the box. The bridge does that turn in two sentences, names no lesson titles, and lands on the thesis. Per the house rule, the transition lives here, at the top of AI Tips, not at the bottom of Tune the Model.

**Registry note (implementation, not copy):** `openerskills`'s "THE LAST OF THE AI" group currently lists two questions (`choosemodel`, `integrity`). Adding AI Tips means a third question row there, something like "What do the people who get more out of AI actually type?" pointed at `aitips`, placed between the two.

---

## Structure

### Beat 1 — Opening bridge and thesis
**Kicker:** none (lesson opens on prose, house standard).
**Type:** prose, 3 × BodyP.
**Fill (new copy):**

> App, model, effort. The setup is done. Everything from here is just what you type into the box.
>
> And everyone types into the same box. Some people get noticeably more back than everyone else, and it isn't because they found the magic words. There are no magic words. What they have is a short list of moves they run on purpose, most of them one sentence long.
>
> **None of these are tricks, and none of them expire.** Five moves. Steal all five.

### Beat 2 — The staged move: make it interview you
**Kicker:** `SectionKicker` — "THE MOVE ALMOST NOBODY TRIES"
**Type:** BodyP, then a `ShowcaseBox` holding a `UserBubble` / `AIBubble` exchange, then BodyP.
**Fill:** parking lot: Ask AI moves — "Ask me whatever you need about me and this job to do ___ well" (flagged there as the strongest surviving idea in the course), fused with THOUGHTPARTNER_INVENTORY: "Ask me five questions before giving advice." Both are the same move in two costumes; one row, not two. Staged on its own instead of buried in the list because it is the strongest line here and it earns a demonstration.

Lead-in BodyP (new copy):

> AI can't see your class, your teacher, your deadline, or the two things you already decided. Most people handle that by typing more. There's a faster way: make it ask you.

ShowcaseBox (new copy). The box demonstrates the move running, it does not restate it:

> **UserBubble:** "Before you write anything, ask me whatever you need to know about me and this assignment to do it well. One question at a time."
>
> **AIBubble:** "Happy to. First one: what did the assignment actually ask for, in your teacher's words?"

Follow-on BodyP (new copy):

> Answer four or five of those and it knows more about the job than you would ever have thought to type. And the questions are the bonus: they tell you what mattered that you hadn't considered.

### Beat 3 — The other four moves
**Kicker:** `SectionKicker` — "FOUR MORE MOVES"
**Type:** one-line BodyP, then `NumberedRows` (4 items, each with a `prompt` tile; row 2 also uses `after`). NumberedRows is the house component for exactly this: named tips with copyable prompt callouts (reference impls: Best practices in `studying`, How to Fight It in `flattery`).
**Fill:**

Lead-in BodyP (new copy):

> Same shape every time: one sentence, typed on purpose, at the moment it fits.

**Row 1 — "Tell it what you already tried."** (NEW)
Body: "Ask cold and you get the average answer, and the average answer is usually the thing you already did. Rule out your dead ends in the prompt and the model has to go past them."
Prompt: `Here's the problem. I already tried [X] and [Y]. X changed nothing, Y made it worse. Skip both and tell me what else could be going on.`

**Row 2 — "Ask for options, not an answer."** (NEW frame; the `after` line is THOUGHTPARTNER_INVENTORY: "Give me three possible explanations.")
Body: "One answer and you're stuck grading its pick. Several, and you're choosing again, which was always the part that was yours."
Prompt: `Give me five ways I could do this, ranked, with the tradeoff on each. Don't pick for me.`
After: "When something is broken instead of undecided, same move, different shape: 'Give me three possible explanations for why this is happening, most likely first.'"

**Row 3 — "Say what wrong looks like."** (NEW)
Body: "'Try again' gets you a different flavor of the same miss. The model can't see what bothered you. Name it, keep the part that worked, and point the next try somewhere."
Prompt: `Not this. The tone is off. Keep the first paragraph, cut the hype, and make it sound like a text, not a newsletter.`

**Row 4 — "Start a new chat instead of arguing with the old one."** (NEW, grounded in the context-window and no-memory lessons)
Body: "Once a chat goes sideways, the wrong turn is still sitting in there, getting re-read before every new word. Twenty messages of correcting just adds more of it. Take the good part with you and leave the rest behind."
Prompt: `Summarize what we've settled so far in one paragraph I can paste into a new chat.`

### Beat 4 — Landing beat
**Kicker:** `SectionKicker` — "Notice what all five have in common."
**Type:** BodyP.
**Fill:** THOUGHTPARTNER_INVENTORY: opening thesis ("the thinking still has to be yours... you drive the conversation and you make the decisions") plus its closing line ("you stay in the work, AI helps you see what you're not seeing"), rewritten tight and pointed at the five moves instead of at a lesson about thought partnership. New copy:

> Not one of them hands the work over. They pull your situation out of your head, rule out the dead ends you already found, widen the options before you pick, and aim the next try. The AI does more in every one of them, and so do you.

### Beat 5 — Close board
`closeBoard("aitips")`, per the house pattern of board before the TRY IT (matches `becurious`, `choosemodel`, `creativethinking`, `prompting`).

### Beat 6 — Capstone TRY IT
See below.

### Beat 7 — `LessonRule` + `NextLessonGate` → `integrity`, label "Next: Habits for the Road".

---

## What's NEW to write

1. The three-paragraph opening bridge and thesis (Beat 1).
2. The interview demonstration: lead-in paragraph, the UserBubble/AIBubble exchange, the follow-on paragraph (Beat 2). The copyable line itself is inherited from the parking lot; the staging, the exchange, and all surrounding prose are new.
3. Four new tip rows with their bodies and prompt tiles (Beat 3). Three are fully new moves ("what you already tried", "say what wrong looks like", "start a new chat"); the fourth is a new frame around one inherited prompt. That is 4 new tips, at the stated cap.
4. The landing beat paragraph (Beat 4), rewritten from the parked Thought Partner thesis and closing line.
5. The close board pair.
6. The whole capstone TRY IT: 5 situations, 5 pill labels, 5 feedback strings.
7. `SECTION_META.aitips`, `CLOSE_BOARDS.aitips`, `SECTION_GROUPS` insertion, the third question row in `openerskills`, and the gate relabel on `choosemodel` (currently "Next: Habits for the Road"-bound work: its gate points at `integrity` today and must point at `aitips`).

**Deliberately NOT carried over** (dedupe findings, see judgment call 1): three of the five parked thought-partner prompts. "What would a skeptical reader say?" is a near-restatement of `flattery`'s "what's weak, what's missing, and what would someone who disagrees say?"; "Challenge my assumption" and "Where might I be fooling myself?" are covered by `flattery`'s "Make it argue the other side" ("argue against me as strongly as possible... the 3 best counterarguments") and its blind-spots framing. The 2026-08-15 audit called all five untaught; the Flattery Trap fight strategies are the overlap it missed.

**Also checked and cleared:** "make it quiz you" is NOT in this lesson, because `studying` already owns it verbatim with a copyable prompt ("Generate a 10-question quiz from these sources only..."). "Give it an example of what good looks like", "tell it who the reader is", and "one job at a time" are `prompting`'s three moves. `evaluating`'s "Leave the chat" means go verify the claim somewhere else, which is a different move from Row 4's restart; worth keeping the wording distinct so students don't blur them.

---

## Close board

**Pill:** "There are no magic words."
**Sticky:** "Just five moves, run on purpose."

The landing paragraph before it lands a different point (every move keeps you in the work), so the board is not a restatement of the copy above it.

---

## Capstone TRY IT — "Which Move Fits?"

**Mechanic:** house parallel sort. `InteractiveBox` variant "try", surface "mint", one `InnerCard` holding 5 `ScenarioRow`s, each with the same row of 5 short `FeedbackPill`s. Same shape as `becurious`'s "Curiosity or Outsourcing?" and `choosemodel`'s "Read the Picker", so it needs no new interaction pattern.

**Item count:** 5.

**Single skill drilled:** matching the move to the moment. Not recall of the move names, and not prompt-writing from scratch: the student reads a real situation and picks which of the five one-sentence moves they would run. That is the only decision the lesson actually asks a student to make in the wild.

**Pill labels (short, so five fit a row):** "Interview me" · "What I tried" · "Options" · "Aim the retry" · "New chat"

**Per-item feedback approach:** each feedback string names the move and then hands over the exact line to type in that situation, so the drill also doubles as five more worked copy examples. No Takeaway after the activity; the per-item feedback is the teaching.

**Items (proposed copy):**

1. *"You've been going back and forth on a lab report intro for twenty minutes, and it keeps handing back the same stiff paragraph with different words."* → **New chat.** "Everything it has given you so far is still in that window, getting re-read before every new word, which is why it keeps circling the same paragraph. Ask for a paragraph you can carry over, open a fresh chat, and paste it in."
2. *"You need a topic for a five-minute presentation, in a class the AI knows nothing about."* → **Interview me.** "You could type out the class, the teacher, the rubric, and the three topics already taken. Faster: 'Before you suggest anything, ask me whatever you need to know about this class and me to pick a topic that works. One question at a time.'"
3. *"Your bike's back brake still rubs. You already re-centered the caliper and swapped the pads."* → **What I tried.** "Ask cold and the first two suggestions will be re-center the caliper and check the pads. Put those in as dead ends and the model has to go past them."
4. *"The fundraiser email it wrote is fine. It just doesn't sound like anyone at your school."* → **Aim the retry.** "'Try again' gets you the same email in a new outfit. Name the miss: 'Too corporate. Keep the first line, cut the hype, and make it sound like a text, not a newsletter.'"
5. *"Your group can't agree on how to run the fundraiser, and you're the one bringing a plan tomorrow."* → **Options.** "One recommendation and you're just grading its pick, in front of your whole group. 'Give me five ways we could run this, ranked, with the tradeoff on each. Don't pick for me.'"

Note for the builder: with five items and five moves, a student can solve the last row by elimination. That is fine for a practice drill; if it bothers anyone, cut item 3 and leave "What I tried" undrilled rather than adding a sixth row.

**On TP_MOVES:** not the capstone, and not fused in. Its three scenarios test a binary ("keeps the thinking yours" vs. "hands over the thinking"), which drills the landing beat's thesis rather than the lesson's actual skill, and it would make the last beat of the lesson be about thought partnership instead of about the five moves. Its scenario surfaces (the rewritten history essay, the AP-Stats-vs-CS lean, the ten ranked fundraiser ideas) stay available in the parking lot as donor material if any item above needs replacing.

---

## SECTION_META proposal

```
aitips: { kicker: "WHAT GOOD USERS TYPE", label: "AI Tips", icon: "🧰" },
```

Kicker "WHAT GOOD USERS TYPE" (the lesson's angle: not what to know, what to type). Label "AI Tips". Icon 🧰, unused elsewhere in `SECTION_META`.

---

## Judgment calls for David

1. **Three of the five parked thought-partner prompts are near-duplicates of Flattery Trap.** "What would a skeptical reader say?", "Challenge my assumption", and "Where might I be fooling myself?" all live inside `flattery`'s fight strategies already, with copyable prompts. This design cuts all three and keeps the two that are clean ("ask me questions first", "three possible explanations"). Alternative: keep "Where might I be fooling myself?" as a sixth move, since it is the least duplicated of the three, and accept the echo one section earlier.
2. **ThinkingTogetherStatic's 6-exchange worked conversation: earn its length here, or stay parked?** Recommendation: stay parked. This lesson already has one demonstration (the interview exchange), and a six-turn transcript would roughly double the reading and turn a tips lesson back into a Thought Partner lesson wearing a new label. If you want it, it belongs after Beat 3 and something else has to come out.
3. **Close board: new pair or the parked one?** Proposed: "There are no magic words." / "Just five moves, run on purpose." The parked Thought Partner pair, "Think with it, not for you." / "It's a partner, not the author.", is still available and lands the landing beat instead of the lesson.
4. **Fresh-chat advice now sits in two consecutive lessons.** Tune the Model's free-plan paragraph already ends "Start fresh chats when you can", and Row 4 here is the fuller version. Leave both (they give different reasons: rate limits there, drift here), or trim the earlier one to a clause so AI Tips owns the move outright.
