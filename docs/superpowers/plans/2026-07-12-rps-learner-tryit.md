# Rock, Paper, Patterns (RPS learner TRY IT) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Vector Space lesson's "Which sits closer?" TRY IT with a playable rock-paper-scissors game whose tiny AI learns the player's throw patterns and reveals its prediction each round.

**Architecture:** One new React component (`RPSLearnerTryIt`) in the single-file app `index.html`, written in the house no-JSX style (`React.createElement`, `var`, tuple `useState`). It keeps the exact contract of the component it replaces (`props.onComplete()` fired once via `useEffect` when done), so `VectorSpaceSection` wiring changes are a one-line swap plus one inserted `KeyInsight`. No build step, no dependencies, no persistence.

**Tech Stack:** Vanilla React 18 via `React.createElement` (no JSX/Babel), inline styles with house CSS custom properties. Verification: `python3 -m http.server` + browser `validate()` + `design-check.sh` + print-mode check.

**Spec:** `docs/superpowers/specs/2026-07-12-rps-learner-tryit-design.md`

## Global Constraints

- Single file: all component code lives in `index.html`. No new files except regenerated lesson exports.
- House style: `var` declarations, `var E = React.createElement`, tuple useState (`var _g = useState(...), game = _g[0], setGame = _g[1];`), inline styles using CSS vars (`var(--tryRule)`, `var(--ink)`, etc.).
- Shell: `InteractiveBox { variant: "try", surface: "mint" }` + `InnerCard`. No `ActivityCounter`, no `FeedbackPill`/`QuizBlock` (bespoke game interior).
- Copy (verbatim from spec): title "Rock, Paper, Patterns"; KeyInsight "A machine that predicts your next move isn't reading your mind. It's counting your habits."; reveal lines "I predicted ✊ (62%) — so I threw ✋." / "No pattern yet — that one was random."
- Tuning knobs (spec values): 10-round gate, 3 warm-up rounds, 0.45 confidence threshold, transition row needs ≥ 2 samples before it beats the frequency fallback.
- TRY IT stays the LAST content block; only `LessonRule` + `NextLessonGate` after it.
- Use curly apostrophes (`’`) in user-facing copy, matching house convention.

---

### Task 1: RPSLearnerTryIt component + VectorSpaceSection wiring

**Files:**
- Modify: `index.html:4949-4976` (replace `WhichSitsCloserTryIt` function with `RPSLearnerTryIt`)
- Modify: `index.html:5112-5114` (insert `KeyInsight` before `closeBoard("vectorspace")`; swap the TryIt call)

Line numbers are pre-edit; the second edit site shifts by the size delta of the first. Anchor on text, not line numbers.

**Interfaces:**
- Consumes: house components already defined above line 4949: `InteractiveBox`, `InnerCard`, `Takeaway`, `KeyInsight`, plus React `useState`/`useEffect` (bare globals in this file).
- Produces: `function RPSLearnerTryIt(props)` — props: `{ onComplete: function }`, called exactly once when the 10th round completes. `VectorSpaceSection`'s existing `vsDone` state and `NextLessonGate` (`ready: vsDone`, target `"prediction"`) are reused untouched.

- [ ] **Step 1: Replace the `WhichSitsCloserTryIt` function (index.html:4949-4976) with `RPSLearnerTryIt`**

Delete the entire `function WhichSitsCloserTryIt(props) { ... }` block (starts line 4949, ends line 4976 with the `}` before `function ItSentenceWalkthrough`). In its place, insert:

```js
// Rock, Paper, Patterns — the Vector Space fun-beat TRY IT (spec:
// docs/superpowers/specs/2026-07-12-rps-learner-tryit-design.md). A tiny pattern-learner
// (order-1 Markov with frequency fallback) predicts the player's next throw and counters
// it. The always-on reveal line is the teaching beat: watch confidence climb as habits
// accumulate. Fun beat, not an assessment; students rebuild this with Claude in a later lab.
function RPSLearnerTryIt(props) {
  var E = React.createElement;
  var THROWS = ["rock", "paper", "scissors"];
  var EMOJI = { rock: "✊", paper: "✋", scissors: "✌️" };
  var COUNTER = { rock: "paper", paper: "scissors", scissors: "rock" };
  var GATE_ROUNDS = 10, WARMUP = 3, CONF = 0.45, ROW_MIN = 2;
  var _g = useState({
    history: [],
    freq: { rock: 0, paper: 0, scissors: 0 },
    trans: {
      rock: { rock: 0, paper: 0, scissors: 0 },
      paper: { rock: 0, paper: 0, scissors: 0 },
      scissors: { rock: 0, paper: 0, scissors: 0 }
    },
    you: 0, ai: 0, ties: 0,
    last: null
  }), game = _g[0], setGame = _g[1];
  var rounds = game.history.length;
  var done = rounds >= GATE_ROUNDS;
  useEffect(function() { if (done && props.onComplete) props.onComplete(); }, [done]);
  function pickAmong(counts) {
    var total = counts.rock + counts.paper + counts.scissors;
    var max = Math.max(counts.rock, counts.paper, counts.scissors);
    var best = THROWS.filter(function(t) { return counts[t] === max; });
    return { guess: best[Math.floor(Math.random() * best.length)], confidence: total > 0 ? max / total : 0 };
  }
  function playRound(playerThrow) {
    var g = game;
    var n = g.history.length;
    var predicted = null, confidence = 0, wasRandom = true;
    if (n >= WARMUP) {
      var prev = g.history[n - 1];
      var row = g.trans[prev];
      var rowTotal = row.rock + row.paper + row.scissors;
      var pick = pickAmong(rowTotal >= ROW_MIN ? row : g.freq);
      predicted = pick.guess;
      confidence = pick.confidence;
      wasRandom = confidence < CONF;
    }
    var aiThrow = wasRandom ? THROWS[Math.floor(Math.random() * 3)] : COUNTER[predicted];
    var result = playerThrow === aiThrow ? "tie" : (COUNTER[aiThrow] === playerThrow ? "you" : "ai");
    var freq = Object.assign({}, g.freq);
    freq[playerThrow] += 1;
    var trans = {
      rock: Object.assign({}, g.trans.rock),
      paper: Object.assign({}, g.trans.paper),
      scissors: Object.assign({}, g.trans.scissors)
    };
    if (n > 0) trans[g.history[n - 1]][playerThrow] += 1;
    setGame({
      history: g.history.concat([playerThrow]),
      freq: freq,
      trans: trans,
      you: g.you + (result === "you" ? 1 : 0),
      ai: g.ai + (result === "ai" ? 1 : 0),
      ties: g.ties + (result === "tie" ? 1 : 0),
      last: { playerThrow: playerThrow, aiThrow: aiThrow, result: result, predicted: predicted, confidence: confidence, wasRandom: wasRandom }
    });
  }
  var last = game.last;
  var resultCopy = last ? (last.result === "you" ? "You win the round." : last.result === "ai" ? "AI wins the round." : "Tie.") : null;
  var resultColor = last ? (last.result === "you" ? "#1f9d5f" : last.result === "ai" ? "#d4334a" : "var(--inkMuted)") : null;
  return E(React.Fragment, null,
    E(InteractiveBox, {
      variant: "try", surface: "mint", title: "Rock, Paper, Patterns",
      lead: "One game before you go. Play at least ten rounds of rock-paper-scissors against a tiny AI. It starts out guessing. Watch what happens once it has seen a few of your throws." },
      E(InnerCard, null,
        E("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 18, flexWrap: "wrap", gap: 8 } },
          E("div", { style: { fontFamily: "var(--sans)", fontSize: 16, fontWeight: 700, color: "var(--ink)" } },
            "You " + game.you + " · AI " + game.ai + " · Ties " + game.ties),
          E("div", { style: { fontSize: 13, color: "var(--inkMuted)" } },
            rounds < GATE_ROUNDS ? "Round " + (rounds + 1) + " of " + GATE_ROUNDS : rounds + " rounds played — keep going if you dare")),
        E("div", { style: { display: "flex", gap: 12, marginBottom: last ? 18 : 0 } },
          THROWS.map(function(t) {
            return E("button", {
              key: t,
              onClick: function() { playRound(t); },
              style: { flex: 1, background: "#fff", border: "1px solid var(--tryRule)", borderRadius: 12, padding: "16px 10px", cursor: "pointer", boxShadow: "var(--shadowSoft)", fontFamily: "var(--sans)" } },
              E("div", { style: { fontSize: 30, lineHeight: 1, marginBottom: 6 } }, EMOJI[t]),
              E("div", { style: { fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "var(--inkSoft)" } }, t));
          })),
        last ? E("div", { style: { borderTop: "1px dashed var(--tryRule)", paddingTop: 16, animation: "fadeIn 0.3s ease" } },
          E("div", { style: { fontFamily: "var(--sans)", fontSize: 17, fontWeight: 700, color: resultColor, marginBottom: 6 } },
            "You threw " + EMOJI[last.playerThrow] + " · AI threw " + EMOJI[last.aiThrow] + " — " + resultCopy),
          E("div", { style: { fontSize: 14, color: "var(--inkSoft)", fontFamily: "var(--mono)" } },
            last.wasRandom
              ? "AI: No pattern yet — that one was random."
              : "AI: I predicted " + EMOJI[last.predicted] + " (" + Math.round(last.confidence * 100) + "%) — so I threw " + EMOJI[last.aiThrow] + ".")) : null)),
    done ? E("div", { style: { marginTop: 18 } },
      E(Takeaway, {
        headline: "It counted, then it predicted.",
        body: "It never read your mind. It counted your throws, spotted your habits, and predicted what comes next. Hold that thought — predicting what comes next is exactly how AI writes. That’s the next lesson." })) : null);
}
```

- [ ] **Step 2: Insert the KeyInsight and swap the call site in `VectorSpaceSection`**

Find (currently index.html:5112-5114, after the first edit the numbers will have shifted — anchor on the text):

```js
      ". Change the words around it, and the same token lands somewhere new."),
    closeBoard("vectorspace"),
    E(WhichSitsCloserTryIt, { onComplete: function() { setVsDone(true); } }),
```

Replace with:

```js
      ". Change the words around it, and the same token lands somewhere new."),
    E(KeyInsight, null, "A machine that predicts your next move isn’t reading your mind. It’s counting your habits."),
    closeBoard("vectorspace"),
    E(RPSLearnerTryIt, { onComplete: function() { setVsDone(true); } }),
```

(KeyInsight sits ABOVE `closeBoard` so the print/PDF still ends on the close board, per house convention. The `LessonRule` + `NextLessonGate` lines below stay untouched.)

- [ ] **Step 3: Confirm no references to the old component remain**

Run: `grep -n "WhichSitsCloser" index.html`
Expected: no output (component deleted, call site swapped).

Run: `grep -c "RPSLearnerTryIt" index.html`
Expected: `2` (one definition, one call site).

- [ ] **Step 4: Static checks**

Run: `bash design-check.sh`
Expected: passes at its current baselines (this change adds no `ActivityCounter`, no new pill patterns).

- [ ] **Step 5: Serve and verify `validate()` passes**

Run: `python3 -m http.server 8765 --bind 127.0.0.1` (background), then open `http://127.0.0.1:8765/index.html` in the browser (Playwright/Chrome DevTools MCP is fine) and read the console.
Expected: `✓ validate(): all 56 lessons pass structural checks` (green line; count must match pre-change count) and zero uncaught errors.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Rock, Paper, Patterns: RPS pattern-learner game replaces Which sits closer? in Vector Space"
```

---

### Task 2: Behavioral verification in the browser

**Files:**
- No edits. Browser verification of `index.html` served over http (required — file:// breaks the app; see reference_verifying_index_html).

**Interfaces:**
- Consumes: the running app from Task 1, navigated to the Vector Space lesson (Understand AI section → Vector Space chip, or set localStorage progress and reload).
- Produces: verified behavior checklist; no code output.

- [ ] **Step 1: Play an anti-pattern opening (rounds 1-3)**

Click ✊ ✋ ✌️ (one each). Expected after each: scoreboard updates by exactly one round; reveal line reads "AI: No pattern yet — that one was random." (warm-up rounds never show a prediction).

- [ ] **Step 2: Spam one button (rounds 4-10, click ✊ seven times)**

Expected: within ~3 clicks the reveal switches to the prediction form "AI: I predicted ✊ (NN%) — so I threw ✋."; confidence NN climbs toward 100; the AI's score pulls ahead of yours; "Round N of 10" counts up.

- [ ] **Step 3: Gate flips exactly once at round 10**

Expected at 10 rounds: the Takeaway card ("It counted, then it predicted.") appears below the box; the "Next: How AI Answers" gate button becomes enabled; the round line switches to "10 rounds played — keep going if you dare".
Then play 2 more rounds. Expected: game keeps scoring, Takeaway stays, no errors, gate stays enabled.

- [ ] **Step 4: Reload → fresh game (no persistence by design)**

Reload the page, navigate back to Vector Space. Expected: scoreboard reset to 0 · 0 · 0. (Lesson completion state is separate localStorage progress and may keep the gate open — that is correct and matches the old TryIt's behavior.)

- [ ] **Step 5: Print mode is clean**

Open `http://127.0.0.1:8765/index.html?print=lesson:vectorspace`. Expected: NO "TRY IT" text, no game UI, no Takeaway; the new KeyInsight line IS present ("…counting your habits."); the lesson print ends on the close board; console `validate()` still green.

- [ ] **Step 6: Report results**

No commit (no changes). Report any deviation instead of proceeding.

---

### Task 3: Re-export the vectorspace lesson text/PDF

**Files:**
- Regenerate: `lessons/vector-space.md` / `lessons/vector-space.pdf` (exact filenames are whatever `git status` shows changed under `lessons/` — the scripts name by lesson slug).

**Interfaces:**
- Consumes: the committed index.html from Task 1 (the KeyInsight changed the lesson's print content, so the NotebookLM exports are stale).
- Produces: refreshed lesson export files, committed.

- [ ] **Step 1: Regenerate exports for the one lesson**

```bash
bash scripts/make-lesson-texts.sh vectorspace
bash scripts/make-lesson-pdfs.sh vectorspace
```

Expected: both scripts exit 0; `git status` shows the vectorspace-slug files under `lessons/` modified.

- [ ] **Step 2: Spot-check the .md**

Run: `grep -n "counting your habits" lessons/*.md`
Expected: exactly one hit, in the vectorspace-slug file. Also `grep -c "Rock, Paper, Patterns" <that file>` → `0` (TRY IT stripped from export).

- [ ] **Step 3: Commit**

```bash
git add lessons/
git commit -m "Re-export vector-space lesson text/PDF after KeyInsight addition"
```

---

### Post-plan follow-ups (orchestrator, not plan executor)

- Update memory `project_tryit_patterns.md` (bespoke + fun-beat lists, WhichSitsCloser retired) and `project_section_balancing.md` (stale "vectorspace stays read-only" note).
- The section-4+ replication lab (student prompt drafted in the spec) is deliberately NOT in this plan.
