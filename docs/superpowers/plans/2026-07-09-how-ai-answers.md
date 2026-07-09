# How AI Answers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework the Prediction lesson into "How AI Answers": a dog-naming question walks the read pipeline (as section review), the model scores dog names and picks "Spot," and the lesson ends one token short of an answer — Inference's cliffhanger.

**Architecture:** All changes live in `index.html` (single-file React app, `React.createElement` calls, no JSX). The lesson is `PredictionSection` (~line 6057). New pieces follow existing component patterns: recap strip mirrors `ItSentenceWalkthrough`, dog chart reuses `ThreeChatsBox` bar-row markup, chat bubble reuses the old Watch-It-Happen "You" bubble style. Spec: `docs/superpowers/specs/2026-07-09-how-ai-answers-design.md`.

**Tech Stack:** Single HTML file, inline React 18 via createElement, design-check.sh lint, Playwright MCP for render verification against `python3 -m http.server`.

## Global Constraints

- No em-dashes in lesson copy (design-check baseline is 3; do not add any).
- Curly quotes/apostrophes (’ “ ”) in all user-facing strings.
- Static box text uses `BOX_TEXT`/`BOX_LABEL` tokens; TRY IT activities get no counter chip and no closing Takeaway.
- Internal lesson id stays `prediction` everywhere (ids are stable across retitles).
- Cut-but-reusable content goes to `docs/parking-lot.md`, never commented out.
- Run `bash design-check.sh` and reconcile FLAGs before any commit touching index.html.

---

### Task 1: Retitle + rebuild the lesson's top half (beats 1–5)

**Files:**
- Modify: `index.html` — `SECTION_META.prediction` (~line 1631), Vector Space gate (~line 5028, search `"Next: Prediction"`), `PredictionSection` top (~line 6057).

**Interfaces:**
- Produces: `DogRecapStrip` (no-props component) and the statement-card div used only inside `PredictionSection`. Task 2 appends content after the recap strip.

- [ ] **Step 1: Retitle the lesson**

In `SECTION_META`: `prediction: { kicker: "THE PICK", label: "Prediction", icon: "📊" }` → `prediction: { kicker: "FROM MEANING TO WORDS", label: "How AI Answers", icon: "📊" }`.

Vector Space gate: `label: "Next: Prediction"` → `label: "Next: How AI Answers"` (the `completeAndNavigate("prediction")` id is unchanged).

- [ ] **Step 2: Replace the intro and add teaser + question + recap strip**

Replace the current intro BodyP (starts "In Vector Space, you watched a token’s final vector land…") with, in order:

Intro BodyP:
> In Vector Space, you watched a token’s final vector land in its neighborhood on the map. That landing was about meaning: the model understanding the words you put in. Now we move to the next step: how AI answers you.

Teaser setup BodyP:
> The following statement is confusing right now. By the end of this lesson, it won’t be.

Statement card (one-off div, serif statement style):
```js
E("div", { style: { background: "var(--primaryFaint)", borderRadius: 16, padding: "26px 28px", margin: "0 0 18px 0", textAlign: "center" } },
  E("div", { style: { fontFamily: "var(--serif)", fontSize: "clamp(20px, 3.6vw, 27px)", lineHeight: 1.3, letterSpacing: "-0.01em", color: "var(--ink)", fontWeight: 600 } },
    "AI predicts the next word based on what you already typed."))
```

Review-framing BodyP:
> Getting there doubles as a review of this whole section, because this is how AI works.

Question lead BodyP:
> Let’s take a simple question and watch AI build its answer.

Chat bubble (You-bubble pattern):
```js
E("div", { style: { marginBottom: 18 } },
  E("div", { style: { fontSize: 12, fontWeight: 700, color: "var(--ink)", marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.5px" } }, "You"),
  E("div", { style: { background: "var(--card)", border: "1px solid var(--rule)", borderRadius: "4px 12px 12px 12px", padding: "14px 18px", fontSize: 15, fontWeight: 500, color: "var(--ink)", lineHeight: 1.6, maxWidth: 360 } }, "What should I name my new dog?"))
```

Recap lead BodyP:
> First, the part you already know. The question makes the trip you’ve spent this section learning, and every step here is review.

- [ ] **Step 3: Add `DogRecapStrip` component**

New function directly above `PredictionSection`, modeled on `ItSentenceWalkthrough` (chip row box + card row box):

```js
function DogRecapStrip() {
  var E = React.createElement;
  var cards = [
    { tag: "Tokens", from: "Tokens", body: "The question splits into tokens, each mapped to its ID number. From here on, it’s all numbers." },
    { tag: "Position stamps", from: "Transformer", body: "Each token gets its position mixed in, #1 through #8, so the order arrives with the words." },
    { tag: "Starting meaning", from: "Embeddings", body: "Each token’s number becomes its vector: its starting position on the map." },
    { tag: "Through the layers", from: "Layers · Vector Space", body: "Dozens of passes of attention and transformation. The question’s meaning is locked in." }
  ];
  return E(React.Fragment, null,
    E("div", { style: { background: "var(--primaryFaint)", border: "1px solid var(--rule)", borderRadius: 16, padding: 20, maxWidth: 880, margin: "8px auto 24px" } },
      E("div", { style: { display: "flex", flexWrap: "wrap", alignItems: "center", justifyContent: "center", gap: 5, rowGap: 8, background: "#fff", border: "1px solid var(--rule)", borderRadius: 12, padding: 14, marginBottom: 14 } },
        ["What", "should", "I", "name", "my", "new", "dog", "?"].map(function(w, i) {
          return E("span", { key: i, style: { background: "#fff", color: "var(--inkSoft)", border: "1px solid rgba(110, 81, 255, 0.3)", boxSizing: "border-box", borderRadius: 7, padding: "5px 8px", fontSize: 12, fontFamily: "var(--mono)", fontWeight: 600 } }, w);
        })),
      E("div", { style: { display: "flex", flexWrap: "wrap", alignItems: "stretch", justifyContent: "center", gap: 8 } },
        cards.map(function(c, i) {
          return E(React.Fragment, { key: i },
            i > 0 ? E("div", { style: { display: "flex", alignItems: "center", color: "var(--primary)", fontSize: 22, fontWeight: 800, flexShrink: 0 } }, "→") : null,
            E("div", { style: { flex: "1 1 180px", minWidth: 165, background: "var(--card)", border: "1px solid var(--rule)", borderRadius: 12, padding: "14px 16px" } },
              E("div", { style: { fontSize: 12, fontWeight: 800, textTransform: "uppercase", letterSpacing: "0.08em", color: "var(--primary)", marginBottom: 2 } }, c.tag),
              E("div", { style: { fontSize: 10.5, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "var(--inkMuted)", marginBottom: 6 } }, "Review · " + c.from),
              E("div", { style: { fontSize: BOX_TEXT, lineHeight: 1.5, color: "var(--ink)" } }, c.body)));
        }))));
}
```

Render `E(DogRecapStrip, null)` after the recap lead BodyP.

- [ ] **Step 4: Verify render**

Run: `python3 -m http.server 8471 &` then Playwright: open `http://127.0.0.1:8471/index.html?print=lesson:prediction`; confirm no console errors, title shows "How AI Answers", statement card, bubble, and 4 recap cards render.

### Task 2: Scoring, dog chart, the pick, teaser resolution (beats 6–8)

**Files:**
- Modify: `index.html` — `PredictionSection` middle, `ThreeChatsBox` (~line 6029, deleted), new `DogNameChartBox`.

**Interfaces:**
- Consumes: lesson top half from Task 1 (content appends after `DogRecapStrip`).
- Produces: `DogNameChartBox` (no-props component). `PhoneTrayStrip` is untouched (the phone's own "See you ______" example stays as the shallow-autocomplete contrast).

- [ ] **Step 1: Rebuild the middle of the lesson**

Keep `SectionKicker "The ranked list"`. Replace the paragraph before `PhoneTrayStrip` with:

> The trip ends with a final vector: a position on the map that means the whole question. So how does that become an answer? Start with your phone. As you type a text, it suggests the next word: three chips above the keyboard, picked from the last word or two, the same for everyone.

Keep `PhoneTrayStrip` and the "way deeper" BodyP and the existing 3-item `<ol>` verbatim.

Replace the "Here’s what that looks like for a very simple sentence." BodyP + `E(ThreeChatsBox, null)` with:

> Here’s that moment for the dog question. The model has started its reply, and the answer has just reached the name slot.

```js
E(DogNameChartBox, null),
```

Keep the "The exact numbers are illustrative." note div. Replace the "The pick has a name…" BodyP with:

> The model takes the top of the list and types it: Spot. That move has a name: **prediction**. Score every possible next token, pick one.

Then teaser-resolution BodyP (new), before the existing attention paragraph (which stays verbatim):

> Now reread the statement from the top of the lesson: AI predicts the next word based on what you already typed. You can sharpen it yourself now. The “word” is really a token. And “what you already typed” is really everything in the context window.

- [ ] **Step 2: Add `DogNameChartBox`, delete `ThreeChatsBox`**

New component in `ThreeChatsBox`'s place, reusing its bar-row markup in a single card:

```js
function DogNameChartBox() {
  var E = React.createElement;
  var ROWS = [["Spot", 22], ["Max", 17], ["Buddy", 14], ["Rex", 9], ["Biscuit", 6], ["other tokens", 32]];
  return E(ShowcaseBox, { headline: "Score every token: the name slot", marginBottom: 10 },
    E(InnerCard, { pad: "snug" },
      E("div", { style: { fontFamily: "var(--mono)", fontSize: 15, color: "var(--ink)", marginBottom: 12 } },
        "You could name him ______"),
      ROWS.map(function(r, i) {
        var isTop = i === 0;
        return E("div", { key: i, style: { display: "grid", gridTemplateColumns: "110px 1fr", gap: 30, alignItems: "center", paddingTop: 7, paddingBottom: 7, borderTop: i === 0 ? "none" : "1px solid var(--rule)" } },
          E("div", { style: { fontWeight: isTop ? 700 : 500, fontSize: 14, color: isTop ? "var(--primary)" : "var(--ink)" } }, r[0]),
          E("div", { style: { display: "flex", alignItems: "center", gap: 8 } },
            E("div", { style: { flex: 1, background: "var(--rule)", height: 12, borderRadius: 6, overflow: "hidden" } },
              E("div", { style: { width: r[1] + "%", minWidth: 2, height: "100%", background: "var(--primary)", borderRadius: 6 } })),
            E("span", { style: { fontSize: 12, fontWeight: 600, color: "var(--ink)", minWidth: 32, textAlign: "right" } }, r[1] + "%")));
      })));
}
```

Delete the whole `ThreeChatsBox` function (parked in Task 5).

- [ ] **Step 3: Verify render**

Playwright reload; confirm chart renders with Spot on top and no `ThreeChatsBox` remnants (grep `ThreeChatsBox` returns nothing).

### Task 3: TRY IT re-theme + cliffhanger close (beats 9–10)

**Files:**
- Modify: `index.html` — `CTX_TASKS` (~line 6059) and the InteractiveBox lead; add cliffhanger BodyP before the TRY IT.

**Interfaces:**
- Consumes: lesson body from Task 2. Gate stays `completeAndNavigate("inference")`, label "Next: Inference", ready-gated on all rows answered.

- [ ] **Step 1: Replace CTX_TASKS and the TRY IT lead**

```js
var CTX_TASKS = [
  { task: "Earlier in the chat, you said he’s a Great Dane puppy with paws like oven mitts", options: ["Titan", "Spot", "Buddy"], answer: "Titan",
    explain: "Titan. The size is sitting right there in the window, so it tilts the odds hard. The model isn’t guessing from the blank; it’s reading the chat." },
  { task: "The whole chat so far has been about Star Wars movies", options: ["Chewie", "Buddy", "Spot"], answer: "Chewie",
    explain: "Chewie. The chat loads the window with Star Wars, and the name list tilts with it. Change the movie, and the list changes too." },
  { task: "A brand-new chat with no history at all", options: ["Titan", "Chewie", "Buddy"], answer: "Buddy",
    explain: "Buddy. With nothing in the window, only the general pattern is left, so a safe, popular name tops the list. That’s the closest the model ever gets to acting like your phone’s chips." }
];
```

InteractiveBox lead becomes:
> Same blank, different chats. For each chat, pick the name most likely to top the list for “You could name him ______”.

- [ ] **Step 2: Add the cliffhanger before the TRY IT**

New BodyP after the attention paragraph:

> One more thing before you try it yourself: Spot is one token. The answer isn’t finished, and the model doesn’t even remember the work it just did. What turns one pick into a whole reply is the next lesson.

- [ ] **Step 3: Verify + commit lesson rebuild**

Playwright: answer all 3 rows (one wrong on purpose to see explain text), confirm gate "Next: Inference" unlocks. Run `bash design-check.sh` (PASS). Commit: `git add index.html && git commit -m "How AI Answers: rebuild Prediction lesson around the dog-naming walkthrough"` (with Co-Authored-By trailer).

### Task 4: Inference handoff sentence

**Files:**
- Modify: `index.html` — `InferenceSection` intro (~line 5281).

- [ ] **Step 1: Swap the intro sentence**

Replace:
> You’ve met every piece on its own: tokens, embeddings, layers, the context window, and the single prediction that picks one token. Now watch them work together as a single journey from your prompt to a finished answer.

with:
> You just watched the model pick one token: Spot. And you’ve met every piece that made the pick: tokens, embeddings, layers, the context window. Now watch them run as a single journey from your prompt to a finished answer.

- [ ] **Step 2: Verify**

Playwright: `?print=lesson:inference` renders the new sentence; rest of lesson unchanged.

### Task 5: Bookkeeping

**Files:**
- Modify: `docs/parking-lot.md`, `briefing.md` (lesson map line), `index.html` (any stray label references).

- [ ] **Step 1: Park the retired content**

Append to `docs/parking-lot.md`: an entry for ThreeChatsBox (origin: Prediction lesson, replaced by DogNameChartBox when the lesson became How AI Answers; verbatim CHATS data for the three "See you ______" contexts) and one for the old CTX_TASKS rows (Monday/tonight/soon, with their explains).

- [ ] **Step 2: Regenerate briefing map line + sweep label references**

In `briefing.md` Understand AI line: `Prediction (prediction)` → `How AI Answers (prediction)`. Then `grep -n '"Prediction"\|Next: Prediction' index.html` and fix any label stragglers (concept-level uses of the word prediction stay).

- [ ] **Step 3: Commit**

`bash design-check.sh` (PASS), then commit bookkeeping + Task 4 together: `git commit -m "How AI Answers: Inference handoff, parking lot, briefing sync"` (with trailer).

### Task 6: Final verification + push

- [ ] **Step 1: Full lesson walk**

Playwright, full app (not print mode): navigate Understand AI → confirm rail shows "How AI Answers", Vector Space gate label, lesson renders top to bottom, TRY IT unlocks gate, Inference intro receives handoff. No console errors.

- [ ] **Step 2: Push**

`git push`. Report the lesson's final beat structure to David.
