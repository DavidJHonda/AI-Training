# TRY IT Instructions Audit — 2026-08-31

## Status

Complete. Every live TRY IT now supplies explicit ordered instructions through the
shared `InteractiveBox.instructions` API. The source check covers 35 TRY IT call
sites, including print branches, the shared `ChoiceQuiz` adapter, and retained
legacy code.

LABs are outside this audit. Their numbered task steps already serve as their
instructions.

## House pattern

1. `ActivityLead` places the TRY IT label and purpose statement above the box.
2. `InteractiveBox` renders its `instructions` inside the mint activity surface.
3. `ActivityInstructions` owns the ordered-list typography and spacing.
4. The interactive card, form, calculator, or game follows immediately below.

Instructions are short imperative actions. They explain how to complete the
activity without repeating the lesson's teaching copy.

## Live inventory

| Lesson ID | TRY IT | Instruction pattern |
|---|---|---|
| `welcome` | Six honest questions | Read, answer, complete |
| `whydeeper` | AI Multiplier | Choose, run twice, compare |
| `llms` | Which One Handles This Better? | Read, choose, review |
| `whybother` | Catch It, or Trust It? | Read, judge knowledge, review |
| `control` | AI Stress Game | Start, sort under time, watch meter, review |
| `aiismath` | Bayesian Mind Reader | Choose number, compare, answer, watch odds |
| `attention` | Be the Attention | Read, click supporting word, review |
| `training` | How Did AI Learn to Do This? | Read, classify, review |
| `tokens` | Beat the Tokenizer | Predict, reveal, compare |
| `embeddings` | Build Your Own Vector | Score, hide, match, review |
| `layers` | Transformer claims video | Watch, reveal, classify, review |
| `vectorspace` | How High Can You Score? | Move, combine, score |
| `prediction` | Name the Piece | Read, choose, review |
| `inference` | How Big Is 2 Quadrillion? | Read, estimate, review |
| `modelselection` | It’s in the Name | Read, choose, review |
| `documenttrap` | Pick the Better Move | Read, choose retrieval move, review |
| `critical` | What’s the Problem With These Claims? | Read, diagnose, review |
| `whatitdoesbest` | Does This Match an AI Strength? | Read, judge, review |
| `evaluating` | Good to Go or Dig Deeper? | Read, run checks, decide |
| `agents` | Be the Agent | Read, choose next action, unlock |
| `integrity` | What Should You Share With AI? | Read segments, classify, compare clean prompt |
| `mindtrap` | Who Makes the Call? | Read, assign decision role, review |
| `engagementtrap` | One App, One Year | Enter, calculate, compare, decide |
| `supporttrap` | How Does AI Fit? | Read, decide role, choose, review |
| `faketrap` | Believe It, Check It, or Call It Fake? | Read, judge evidence, choose, review |
| `questionsvaluable` | Match the Quality | Choose both sides, complete pairs |
| `whatpeoplesay` | Right or Wrong? | Read prediction, choose, review history |
| `bigdownside` | Which Idea Explains It? | Read, match idea, review |
| `computecost` | Does It Use More Than an AI Chat? | Read, compare energy, review |
| `unexpected` | The Great Hanoi Rat Quiz | Read, guess, review history |

## Enforcement

Run:

```sh
node scripts/check-try-it-instructions.js
```

The check is also part of `bash design-check.sh`. It fails when an
`InteractiveBox` TRY IT or `ChoiceQuiz` call site lacks an `instructions` prop.

## Verification

- Design consistency check passes.
- Support Trap renders four steps inside its mint TRY IT box.
- Engagement Trap renders four steps inside its mint TRY IT box.
- Both pilots have no activity-box overflow at a 390 × 844 viewport.
- Engagement Trap's hours/minutes fields now stack on narrow screens instead of
  overflowing horizontally.
