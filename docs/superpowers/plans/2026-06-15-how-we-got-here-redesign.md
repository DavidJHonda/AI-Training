# How We Got Here Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the passive 9-event timeline in How We Got Here with a demystification-first lesson: an interactive "assemble the four ideas, then ignite them in 2017" SEE IT.

**Architecture:** Single-file inline-React app (`index.html`, `React.createElement` style, no JSX, no build, no test runner). Rewrite `HowWeGotHereSection` and add one new sub-component `HistoryAssembleSeeIt`; change the lesson's kicker in `SECTION_META`. Verification = `bash design-check.sh` + live browser walkthrough.

**Tech Stack:** HTML + inline React (Babel standalone). Reuses house primitives: `LessonHeader`, `BodyP`, `CoreLoopBox`, `InteractiveBox` (variant `see`, surface `sand`), `ActivityInstruction`, `ActivityCounter`, `ActivityButton`, `Takeaway`, `KeyInsight`, `LessonRule`, `NextLessonGate`, `useLocalStorage`, `useReducedMotion`.

**House constraints (verified):**
- New copy must contain **no em-dashes** (`design-check.sh` expects exactly 7 file-wide). Use commas/colons/periods. Use curly punctuation (’ “ ”) to match the file.
- Progress UI must use `ActivityCounter`, never hand-built pills (design-check baseline = 4).
- SEE IT/TRY IT activity interiors are excluded from `BOX_TEXT`/`BOX_CARD_TITLE`/`BOX_LABEL` tokens — this component sets explicit font sizes.
- Do NOT emit the exact string `background: "var(--bg)", border: "1px solid var(--rule)", borderRadius: 12, padding: 24` (design-check "page-bg used as outer band" expects 0). The component below avoids it.
- This is a within-lesson redesign (label + id unchanged, no count change): **no `briefing.md` update needed.**

**Reference (pre-edit line numbers; re-locate by searching, the file shifts):**
- `HowWeGotHereSection`: index.html ~2202–2270 (currently: `IDEA` map, `TIMELINE` array of 9 entries, intro prose, `CoreLoopBox`, the timeline render, `KeyInsight`, gate → `aivscode`).
- `SECTION_META.howwegothere`: index.html line ~1339 — `{ kicker: "THE LONG ROAD", label: "How We Got Here", icon: "📜" }`.
- Component primitives confirmed: `useLocalStorage(key, default) -> [val, set]`; `InteractiveBox({variant, surface, title, action, marginBottom, children})`; `ActivityCounter({count, total})`; `ActivityButton({size, onClick, disabled, style, children})`; `Takeaway({headline, body, merged, accent})`; `useReducedMotion() -> bool`.

---

### Task 1: Replace HowWeGotHereSection and add HistoryAssembleSeeIt

**Files:**
- Modify: `index.html` — replace the entire `HowWeGotHereSection` function (~2202–2270) with the two functions below (the section + its new SEE IT sub-component). This also deletes the now-unused `IDEA` and `TIMELINE` locals.

- [ ] **Step 1: Replace the function**

Find `function HowWeGotHereSection(props) {` and replace everything through its closing `}` (the line before `const WHENNOT_SCENARIOS = [` at ~2271) with EXACTLY:

```js
function HowWeGotHereSection(props) {
  return /*#__PURE__*/React.createElement("div", null,
    /*#__PURE__*/React.createElement(LessonHeader, { sectionId: "howwegothere" }),
    /*#__PURE__*/React.createElement(BodyP, null, "AI can feel like it appeared out of nowhere, fully formed, almost like magic. It didn’t. What looks like one sudden invention is really four older ideas, each worked out by different people who weren’t trying to build AI at all."),
    /*#__PURE__*/React.createElement(BodyP, null, "You already met those four ideas in What Is AI? Here, you’ll watch them come together: bring in each one, then connect them at the single moment everything changed."),
    /*#__PURE__*/React.createElement(CoreLoopBox, null),
    /*#__PURE__*/React.createElement(BodyP, { marginBottom: 24 }, "None of them arrived together. Each was figured out decades, even centuries, apart, for reasons that had nothing to do with AI. Bring them in one at a time."),
    /*#__PURE__*/React.createElement(HistoryAssembleSeeIt, null),
    /*#__PURE__*/React.createElement(KeyInsight, { lead: "Not magic. Assembled." }, "Probability, prediction, training, and patterns were each figured out separately, for reasons that had nothing to do with AI. What we call AI is what happened when those understandable pieces finally connected. None of it is beyond you, and you’re about to learn each piece."),
    /*#__PURE__*/React.createElement(LessonRule, null),
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: true, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("aivscode"); }, label: "Next: Rules vs Patterns" })
  );
}
function HistoryAssembleSeeIt(props) {
  var reduced = useReducedMotion();
  var ANCIENT = [
    { key: "probability", icon: "🎲", label: "Probability", color: "#b45309", bg: "#fbedd3", year: "1650s", caption: "Started as gambling math: figuring the odds.", who: "Pascal & Fermat" },
    { key: "prediction", icon: "✍️", label: "Prediction", color: "#b45309", bg: "#fbedd3", year: "1948", caption: "Guess the next word from the last, like your phone’s autocomplete.", who: "Claude Shannon" },
    { key: "training", icon: "📚", label: "Training", color: "var(--primary)", bg: "#ece8fd", year: "1957", caption: "The first machine that learned from examples instead of following instructions.", who: "the perceptron" }
  ];
  var SPARK = { key: "patterns", icon: "🧩", label: "Patterns", color: "var(--primary)", bg: "#ece8fd", year: "2017", caption: "One breakthrough let a machine weigh all the words at once and find the patterns between them: the transformer.", who: "“Attention Is All You Need”" };
  var _st = useLocalStorage("seeit-howwegothere-assembleStep", { lit: [], ignited: false });
  var st = _st[0], setSt = _st[1];
  var lit = st.lit || [];
  var ignited = !!st.ignited;
  var allThreeIn = lit.length >= ANCIENT.length;
  function bringIn(key) { if (lit.indexOf(key) !== -1) return; setSt({ lit: lit.concat([key]), ignited: ignited }); }
  function ignite() { if (!allThreeIn || ignited) return; setSt({ lit: lit, ignited: true }); }

  function ideaCard(idea, isLit, onClick, locked) {
    return /*#__PURE__*/React.createElement("button", {
      key: idea.key, onClick: onClick, disabled: locked || isLit,
      style: { textAlign: "left", border: isLit ? "1.5px solid " + idea.color : "1.5px solid var(--rule)", cursor: (locked || isLit) ? "default" : "pointer", background: isLit ? idea.bg : "var(--card)", borderRadius: 14, padding: "16px 18px", opacity: isLit ? 1 : (locked ? 0.4 : 0.85), boxShadow: "var(--shadowSoft)", transition: "all 200ms ease", fontFamily: "var(--sans)", width: "100%" }
    },
      /*#__PURE__*/React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, marginBottom: isLit ? 10 : 0 } },
        /*#__PURE__*/React.createElement("span", { style: { fontSize: 22, filter: isLit ? "none" : "grayscale(1)", opacity: isLit ? 1 : 0.6 } }, idea.icon),
        /*#__PURE__*/React.createElement("span", { style: { fontSize: 17, fontWeight: 800, color: isLit ? idea.color : "var(--inkMuted)" } }, idea.label),
        /*#__PURE__*/React.createElement("span", { style: { marginLeft: "auto" } },
          isLit
            ? /*#__PURE__*/React.createElement("span", { style: { background: idea.color, color: "#fff", borderRadius: 20, padding: "3px 11px", fontSize: 12, fontWeight: 700 } }, idea.year)
            : /*#__PURE__*/React.createElement("span", { style: { fontSize: 13, fontWeight: 700, color: locked ? "var(--inkFaint)" : idea.color } }, locked ? "Locked" : "Tap to add"))),
      isLit
        ? /*#__PURE__*/React.createElement("div", null,
            /*#__PURE__*/React.createElement("div", { style: { fontSize: 15, color: "var(--inkSoft)", lineHeight: 1.5, marginBottom: 8 } }, idea.caption),
            /*#__PURE__*/React.createElement("div", { style: { fontSize: 12, fontWeight: 700, color: "var(--inkFaint)", textTransform: "uppercase", letterSpacing: "0.08em" } }, idea.who))
        : null);
  }

  var sparkZone = ignited
    ? /*#__PURE__*/React.createElement("div", { style: { animation: reduced ? "none" : "fadeIn 0.5s ease" } },
        ideaCard(SPARK, true, undefined, false),
        /*#__PURE__*/React.createElement("div", { style: { marginTop: 16, display: "flex", alignItems: "stretch", background: "var(--card)", borderRadius: 14, padding: 18, boxShadow: "var(--shadowSoft)" } },
          /*#__PURE__*/React.createElement("div", { style: { flex: "1 1 auto", display: "flex", flexDirection: "column", justifyContent: "center", paddingRight: 14 } },
            /*#__PURE__*/React.createElement("div", { style: { fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "var(--inkFaint)", marginBottom: 10 } }, "About 300 years"),
            /*#__PURE__*/React.createElement("div", { style: { borderTop: "2px dotted var(--inkFaint)", marginBottom: 10 } }),
            /*#__PURE__*/React.createElement("div", { style: { fontSize: 13, color: "var(--inkMuted)", lineHeight: 1.4 } }, "The four ideas sit apart. Progress is slow.")),
          /*#__PURE__*/React.createElement("div", { style: { flexShrink: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "0 16px", borderLeft: "2px solid var(--rule)", borderRight: "2px solid var(--rule)" } },
            /*#__PURE__*/React.createElement("div", { style: { fontFamily: "var(--serif)", fontSize: 28, color: "var(--primary)", lineHeight: 1 } }, "2017"),
            /*#__PURE__*/React.createElement("div", { style: { fontSize: 12, fontWeight: 700, color: "var(--primary)", marginTop: 4 } }, "they connect")),
          /*#__PURE__*/React.createElement("div", { style: { flex: "0 0 auto", display: "flex", flexDirection: "column", justifyContent: "center", paddingLeft: 16 } },
            /*#__PURE__*/React.createElement("div", { style: { fontSize: 22, color: "var(--primary)", fontWeight: 800, lineHeight: 1 } }, "↗"),
            /*#__PURE__*/React.createElement("div", { style: { fontSize: 13, color: "var(--ink)", fontWeight: 700, marginTop: 6, lineHeight: 1.4 } }, "Scaling up"),
            /*#__PURE__*/React.createElement("div", { style: { fontSize: 13, color: "var(--ink)", fontWeight: 700, lineHeight: 1.4 } }, "ChatGPT"),
            /*#__PURE__*/React.createElement("div", { style: { fontSize: 13, color: "var(--primary)", fontWeight: 800, lineHeight: 1.4 } }, "today"))),
        /*#__PURE__*/React.createElement(Takeaway, { merged: true, headline: "Centuries apart, then all at once.", body: "Four ideas, each invented separately and left sitting apart for decades, finally snapped together in 2017. That collision, not any single invention, is the AI you use today." }))
    : /*#__PURE__*/React.createElement("div", { style: { border: "1.5px dashed var(--rule)", borderRadius: 14, padding: "20px 18px", textAlign: "center", background: "var(--card)", opacity: allThreeIn ? 1 : 0.6 } },
        /*#__PURE__*/React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "center", gap: 8, marginBottom: allThreeIn ? 14 : 0 } },
          /*#__PURE__*/React.createElement("span", { style: { fontSize: 22, filter: "grayscale(1)", opacity: 0.6 } }, SPARK.icon),
          /*#__PURE__*/React.createElement("span", { style: { fontSize: 17, fontWeight: 800, color: "var(--inkMuted)" } }, "2017: the fourth idea"),
          /*#__PURE__*/React.createElement("span", { style: { fontSize: 13, fontWeight: 700, color: "var(--inkFaint)" } }, allThreeIn ? "" : "· locked")),
        allThreeIn
          ? /*#__PURE__*/React.createElement(ActivityButton, { size: "large", onClick: ignite }, "Connect them at 2017 →")
          : /*#__PURE__*/React.createElement("div", { style: { fontSize: 14, color: "var(--inkMuted)", lineHeight: 1.5 } }, "Bring in the three ideas above to reach 2017."));

  return /*#__PURE__*/React.createElement(InteractiveBox, {
    variant: "see", surface: "sand", title: "Build the machine",
    action: /*#__PURE__*/React.createElement(ActivityCounter, { count: lit.length + (ignited ? 1 : 0), total: 4 })
  },
    /*#__PURE__*/React.createElement(ActivityInstruction, null, "Bring in each idea, then connect them at the moment everything changed."),
    /*#__PURE__*/React.createElement("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12, marginBottom: 14 } },
      ANCIENT.map(function(idea) { var isLit = lit.indexOf(idea.key) !== -1; return ideaCard(idea, isLit, function() { bringIn(idea.key); }, false); })),
    /*#__PURE__*/React.createElement("div", { style: { textAlign: "center", color: "var(--primary)", fontSize: 20, fontWeight: 800, margin: "2px 0 12px" } }, "↓"),
    sparkZone);
}
```

- [ ] **Step 2: Verify the old timeline data is gone and the new markers are present**

Run:
```bash
grep -c 'TIMELINE' index.html        # expect 0
grep -c 'Autoregressive Generation' index.html   # expect 0 (Yule beat removed)
grep -c 'Backpropagation' index.html  # expect 0
grep -c 'function HistoryAssembleSeeIt' index.html  # expect 1
grep -c 'seeit-howwegothere-assembleStep' index.html # expect 1
```

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Redesign How We Got Here: assemble-the-ideas SEE IT, drop static timeline"
```

---

### Task 2: Update the lesson kicker

**Files:**
- Modify: `index.html` line ~1339 (`SECTION_META.howwegothere`)

- [ ] **Step 1: Change the kicker**

Change:
```js
  howwegothere: { kicker: "THE LONG ROAD", label: "How We Got Here", icon: "📜" },
```
to (label and icon unchanged; only the kicker string changes, using a curly apostrophe):
```js
  howwegothere: { kicker: "AI ISN’T MAGIC", label: "How We Got Here", icon: "📜" },
```
(The `icon` value in the file is the escaped form `"📜"` — leave it exactly as-is; only edit the kicker text.)

- [ ] **Step 2: Verify**

Run: `grep -c 'kicker: "AI ISN’T MAGIC"' index.html`
Expected: `1`. Also `grep -c 'THE LONG ROAD' index.html` → `0`.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Retitle How We Got Here kicker: THE LONG ROAD -> AI ISN'T MAGIC"
```

---

### Task 3: Design-check and live browser verification

**Files:** none (verification only)

- [ ] **Step 1: Run the design check**

Run: `bash design-check.sh`
Expected: `PASS - no new drift against baselines.` In particular `em-dashes in copy` must stay `OK ... 7`. If it FLAGs em-dashes, new copy introduced one — replace it. If "hand-built counter pills" FLAGs (>4), replace any hand-built pill with `ActivityCounter`.

- [ ] **Step 2: Serve and open the app**

```bash
( python3 -m http.server 8731 >/tmp/aitrain.log 2>&1 & ) ; sleep 1
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8731/index.html   # expect 200
```
Open `http://localhost:8731/index.html` in a browser (or drive with the playwright/chrome-devtools MCP). Enter a name on the welcome screen to unlock the lesson nav.

- [ ] **Step 3: Jump to the lesson and verify render**

In the browser console (or via MCP `browser_evaluate`), set the active section and reload:
```js
var p = JSON.parse(localStorage.getItem('llm-explorer-progress'));
p.activeSection = 'howwegothere';
if (!p.visited.includes('howwegothere')) p.visited.push('howwegothere');
localStorage.setItem('llm-explorer-progress', JSON.stringify(p));
location.reload();
```
Confirm, top to bottom:
- Lesson header kicker reads **AI ISN'T MAGIC**, title "How We Got Here".
- Hook prose ("AI can feel like it appeared out of nowhere…"), then `CoreLoopBox`, then the SEE IT titled "Build the machine" with a 0 of 4 counter.
- Three idea cards render faded with "Tap to add"; the 2017 card is dashed/locked with "Bring in the three ideas above to reach 2017."

- [ ] **Step 4: Verify the interaction**

- Click each of the three idea cards: each lights up (color fill, year chip, caption, the small name), counter climbs 1→2→3.
- After the third, the 2017 zone enables a "Connect them at 2017 →" button.
- Click it: the Patterns/2017 card appears lit, the "About 300 years … 2017 they connect … Scaling up / ChatGPT / today" two-eras strip fades in, the Takeaway "Centuries apart, then all at once." shows, counter reads 4 of 4.
- Confirm the KeyInsight "Not magic. Assembled." renders below, and "Next: Rules vs Patterns" navigates to `aivscode`.
- Reload the page: the assembled/ignited state persists (localStorage).
- Check the browser console: no errors except an unrelated `favicon.ico` 404.

- [ ] **Step 5: Stop the server and clean up**

```bash
pkill -f "http.server 8731" 2>/dev/null; rm -rf .playwright-mcp 2>/dev/null; echo done
```

---

### Task 4: Park the cut timeline copy

**Files:**
- Modify: `docs/parking-lot.md`

- [ ] **Step 1: Append the removed timeline**

Read `docs/parking-lot.md` to match its format, then append a dated section ("How We Got Here static timeline (2026-06-15)") with Origin = "Cut from HowWeGotHereSection in the assemble-the-ideas redesign; full prior version in git history before commit `Redesign How We Got Here`." Include this verbatim cut copy (the three milestones fully dropped, plus the whole 9-entry timeline and old KeyInsight for retrievability):

```
Old KeyInsight — "AI was centuries in the making.": "No one set out to build it. Probability, prediction, training, and patterns were each worked out by different people, decades and even centuries apart, for reasons that had nothing to do with AI. What we call AI today is what happened when those separate ideas finally came together."

Full 9-entry timeline:
- 1654 Standard Probability (probability): "Blaise Pascal and Pierre de Fermat traded letters about games of chance, the start of modern probability math."
- 1763 Conditional Probability (probability) [DROPPED]: "Thomas Bayes found a formal way to update probabilities as new evidence comes in."
- 1927 Autoregressive Generation (prediction) [DROPPED]: "George Udny Yule proposed the autoregressive model: predict each step in a sequence from the ones before it."
- 1948 Generating English (prediction): "Claude Shannon applied the autoregressive idea to language, picking each word from the probability of the one before it: an early statistical model of language."
- 1957 The Perceptron (training): "One of the first machines that could learn from examples. It was primitive, but it proved the concept: machines can learn, not just follow instructions."
- 1986 Backpropagation (training) [DROPPED]: "How a machine learns from its mistakes: each wrong answer makes the next one better, over billions of tries."
- 2017 Attention Is All You Need (patterns): "A team at Google published one paper that changed everything. AI could now read all your words at once instead of one at a time. The transformer was born."
- 2018 to 2021 Scaling Up: "Researchers fed transformers more of the internet and more computing power. The bigger they got, the more capable they got, turning a research idea into something powerful."
- 2022 ChatGPT Launches: "The public finally saw what large language models could do. AI started feeling like a tool anyone could use."
```

- [ ] **Step 2: Commit**

```bash
git add docs/parking-lot.md
git commit -m "Park cut How We Got Here timeline copy"
```

---

## Notes for the implementer

- **No automated tests exist.** Task 3's design-check + browser walkthrough is the verification gate — do not skip it. The previous lesson change shipped a wrong count that only a live render caught.
- **createElement balance is the main risk.** After Step 1, sanity-check that `HistoryAssembleSeeIt` and `HowWeGotHereSection` are balanced (the quality reviewer can parse the function bodies with `new Function`).
- **Curly punctuation:** the apostrophes in the copy above (`didn’t`, `weren’t`, `you’ll`, `phone’s`, `you’re`, `ISN’T`) and the quotes around `“Attention Is All You Need”` are curly on purpose, matching house style. Em-dashes are intentionally absent.
