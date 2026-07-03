# Check the Results Rebuild + Critical Thinking Reorder — Design

**Date:** 2026-07-03
**Status:** Approved (design); pending implementation plan
**Sections affected:** Work with AI — Check the Results (`evaluating`, rebuilt), Critical Thinking (`critical`, repositioned + opener retouch), Context Window (`prompt`, gate rewire only)

## Problem

The last two lessons of Work with AI are in the wrong order and the wrong shape.

- **Critical Thinking (`critical`)** currently comes first. It teaches the general
  habit (Spot the Problem TRY IT, five habits) before the learner has any concrete
  procedure for handling an AI answer.
- **Check the Results (`evaluating`)** currently comes last and teaches a different
  question than its title promises: not "is it true?" but "is it usable?" — a
  six-criteria checklist plus a Prompt → Evaluate → Refine iteration walkthrough
  (the basketball recap). Truth-checking is deferred with "You've learned how to
  verify whether AI output is true," which points backward at a lesson that never
  taught a verification *procedure*.

Net effect: the section's practical workflow (pick app → ask good questions →
prompt → context) ends without the obvious final beat — *what do I do with the
answer?* — and the mindset lesson has nothing concrete to generalize from.

## Idea

Swap the two lessons and rebuild Check the Results as the verification procedure.

**New order:** … `prompting` → `prompt` (Context Window) → **`evaluating` (Check
the Results)** → **`critical` (Critical Thinking)** → next section.

- **Check the Results** becomes the concrete procedure: Read → Understand →
  Validate → Decide → deeper checks → next steps. Closes the practical loop.
- **Critical Thinking** becomes the section closer: the skill beyond AI,
  generalizing the procedure into a habit, and bridging into Understand AI
  ("the judgment you've started building gets a lot harder to fool").

Concrete before abstract; the procedure surfaces the limitation ("what if the
topic is beyond what I know?") that the mindset lesson then answers ("Know Your
Limits" habit).

## Decisions (locked during brainstorming)

1. **Order swap approved.** `evaluating` before `critical` in SECTION_GROUPS.
2. **The Decide gate asks two questions**, not one:
   - *What kind of task was this?* — factual (research, claims, summaries of real
     events) vs. generative (first drafts, brainstorms). Task type routes which
     deeper checks apply.
   - *How much is riding on it?* — stakes decide depth. Movie-night chat: done.
     College-essay help: keep going.
3. **Task type is not an exemption.** Read → Understand → Validate apply to every
   answer. A draft skips the *research* checks, not the *reading* checks — for
   generative tasks "validate" means "did AI slip in anything I never gave it?"
   (the basketball recap's invented "51-49 lead" is the canonical example of why).
4. **The Prompt → Evaluate → Refine loop is cut, not relocated.** It teaches
   prompt-writing, which is Check the Results' wrong altitude — and The Art of
   Prompting can't absorb it either: that lesson's thesis is explicitly "you don't
   need a prompting class, just three moves." A 3-round iteration walkthrough
   fights that message. Loop goes to the parking lot.
5. **"Next steps" replaces the loop** — three verdicts, a close rather than a
   process: Use it / Fix it / Walk away (details below).
6. **The two-false-statements example is reframed.** Both statements are false;
   the draft's "you'll know which is right" framing is replaced by "they fail
   differently" (see Validate step below).
7. **The `AIStrengthsSection` scenario quiz survives.** Currently embedded at the
   top of `evaluating`, its "good fit vs. needs follow-up" scenarios (brainstorming,
   citations, medical advice, judgment calls, summarizing, acting-for-you) are
   task-type judgment — exactly the Decide step. It moves to sit after Decide as
   that step's practice, instead of being an unexplained preamble.

## Check the Results — teaching flow

Kicker stays: BEFORE YOU TRUST IT. Icon stays: 🔍.

1. **Opener.** Everyone knows AI makes mistakes. So what do you do with an AI
   answer — ignore AI? No: it's too powerful to leave on the shelf. The answer is
   a process for evaluating results.
2. **Read.** Weak AI users take AI's output and share it without even reading it.
   Reading is the floor.
3. **Understand.** You'll never know if it's right unless you understand what it's
   saying. TIP: if something is unclear, ask AI to explain it.
4. **Validate** — against your own knowledge. This is where learning pays off.
   Two false statements that fail differently:
   - *"The American Civil War started in 1083, on the border of England and
     Argentina."* — your learned knowledge catches this instantly. Validation works.
   - *"Maria Petronoski won 3 gold medals at the 1932 Olympics in Athens."* —
     sounds completely plausible; unless you know the 1932 Games were in Los
     Angeles (and that she doesn't exist), validation fails.
   The first shows why your knowledge matters; the second shows why "sounds fine
   to me" isn't enough — motivating the deeper checks, and planting the hook that
   Critical Thinking's "Know Your Limits" habit later resolves.
5. **Decide** — the two-question gate (task type × stakes). Low stakes, either
   type → done: *sometimes this is all you do.* The relocated `AIStrengthsSection`
   scenario TRY IT practices this judgment here.
6. **Go deeper — factual task + it matters:**
   - *Check citations.* AI got the information from somewhere. Reply "Give me
     citations in your response," click the links, read whether the page actually
     supports the claim.
   - *Is it current?* Forward-reference: LLMs have a training cut-off date (taught
     in Training). Ask the AI to run a web search to update the information.
   - *Personal/professional advice.* Some answers belong to a professional —
     medical advice is the standing example.
7. **Go deeper — draft task + it matters:** does it match what you asked for, does
   it fit your audience, and did AI add anything you never gave it? Light prose,
   not a checklist revival.
8. **Next steps** — three verdicts, closing the lesson:
   - **Use it** — it passed. Most answers end here.
   - **Fix it** — something's off and you can name it. Say *what's wrong* in a
     follow-up ("cut the stat I never gave you"), not a rewritten prompt from
     scratch. ("Be specific about what's wrong" survives as this one line.)
   - **Walk away** — wrong tool or stakes too high. Do it yourself, or take it to
     a person who actually knows.

Why-AI-makes-things-up stays out of scope — that's Hallucination's job (Avoid the
Traps); this lesson may forward-reference it the same way it forward-references
the training cutoff.

## Critical Thinking — repositioning retouch

Content largely survives as-is (Spot the Problem TRY IT, five habits). Changes:

- **Opener retouched to receive the handoff** from Check the Results instead of
  leading into it: you now have a procedure; critical thinking is the habit that
  procedure comes from, and it works on any claim from any source — AI included.
- **"Know Your Limits" habit** now pays off the Petronoski hook explicitly.
- **Closer bridges to Understand AI:** the deepest check is understanding the
  machine itself.
- **Gates rewire:** `prompt` (Context Window) gate → `evaluating`
  ("Next: Check the Results"); `evaluating` gate → `critical`
  ("Next: Critical Thinking"); `critical` gate → `openerfoundations`
  ("Next: Foundations", `evaluating`'s current target). The standalone `AIStrengthsSection` gate
  ("Next: Evaluate Results") is revisited as part of the embed move.

## Cut to parking lot (per house rules)

- Prompt → Evaluate → Refine basketball-recap walkthrough (3 rounds, invented-stat
  catch) — good material, no current home.
- The six-criteria "usable" checklist and "correct doesn't mean usable" cards.
- "2–3 rounds is normal" refine framing.

## Out of scope

- The Art of Prompting, Questions Matter, Context Window content (gate label
  aside).
- Avoid the Traps lessons (Hallucination owns "why it makes things up").
- Lesson PDFs and briefing.md lesson map — regenerated/updated at implementation
  time per house rules.
- Any new video pill for these lessons.
