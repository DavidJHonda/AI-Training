# Embrace the Future — Section Rebuild Design

Date: 2026-08-09. Source: David's rough outline (screenshot) + conversation decisions. This is the
first of the last-three-sections pass (Embrace the Future → Build Your Skills → Finish Smarter).

## The spine

Nobody knows where AI lands. Two camps (AI Lovers, AI Haters) say very different things. The section
tours the upside, the accelerant, the downside, then what the deployed world means for the student's
actual life — and ends on agency, not spectacle.

## New lesson order (ids in parentheses; internal ids never change, titles drive asset slugs)

1. **Opener** (`openerrealworld`) — rebuilt around Talking About AI's four soundbites ("AI is going
   to take over," "it'll take all the jobs," "it's just hype," "kids just cheat with it"), presented
   as the two camps' voices, **raised but NOT answered**. Names the worry under each. Promise: by
   the end of this section you can answer all four. No spoilers of later lessons' answers.
2. **What People Say** (`whatpeoplesay`, NEW) — the future-tense disagreement: the experts
   themselves disagree about where this lands, nobody knows where it stops, predictions and their
   track record. Boundary vs opener: opener = today's shouting match, this = where-does-it-land.
3. **The Big Upside** (`bigupside`) — current lesson, expanded for a couple of other areas.
4. **Pace of Change** (`paceofchange`, NEW) — opens on a models-released-by-year graph (2022→now).
   Why: more compute; 2026 AI writes the code that builds models. Concepts: AGI, ASI, recursive
   self-training, automated AI research. **Absorbs Judging AI's Future** (how to judge claims about
   where this lands). Write structural claims with dated specifics as replaceable examples — this
   lesson must survive the club year without rotting.
5. **The Big Downside** (`bigdownside`, NEW) — we don't know why models do what they do (black box);
   pace means guardrails can't keep up; possible negative consequences. **Home of the Hanoi rat
   story** as the optimize-the-metric-not-the-goal analogy (rhymes with aijudges' "every system
   optimizes for something").
6. **The Rise of Agents** (`agents`) — moves later; automation escalation after the downside.
7. **Work Changes** (`workchanges`) — after Agents (automation before jobs).
8. **The Cost** (`computecost`, retitled from The Hidden Cost) — data centers; the physical bill.
   Keeps the answer-cost thread promised in One More Thing.
9. **When AI Judges You** (`aijudges`) — unchanged body + **new section-end beat**: return to the
   opener's four soundbites now answerable, the meet-the-worry-not-the-soundbite skill, and the
   closer line "The smartest people aren't the ones who panic or worship. They're the ones who can
   judge." Decide there whether SpotTheWorryTryIt moves in or retires.

## Retired lessons

- `aifuture` (Judging AI's Future) — rolled mostly into Pace of Change.
- `talkingai` (Talking About AI) — four soundbites → Opener (as questions); meet-the-worry payoff +
  closer line → section end in aijudges. Component deleted once both beats land.

## Locked decisions (David, 2026-08-09)

1. What People Say stays a **separate lesson** (future-tense boundary vs the opener).
2. Hanoi rat story lives in **The Big Downside**.
3. Meet-the-worry + panic/worship/judge line land at **section end** (not the opener).
4. Drafting pace: **lesson-by-lesson checkpoints** — David reads each lesson before the next starts.

## Cross-reference and bookkeeping fixes (same pass)

- One More Thing's "We'll count that bill later in the course, in The Hidden Cost" → The Cost.
- SECTION_GROUPS / SECTION_META / nav chain rewired; validate() + full-chain trace green at every
  checkpoint. New lessons stubbed first so the chain never breaks.
- Close boards: new/rebuilt lessons need CLOSE_BOARDS entries; opener close board carries the
  section promise (NOT the judge line — that's the section-end payoff).
- TRY ITs: surviving lessons keep theirs; new lessons get activities on canonical patterns
  (no counters, no em-dashes, curly apostrophes, activity-last convention).
- Videos: Talking About AI, Judging AI's Future, The Hidden Cost videos go stale; new lessons have
  none. Embrace the Future re-enters the video queue after copy locks. Illustration slugs re-check
  on the computecost retitle.
- PDF/.md exports re-run at the end of the section pass.
