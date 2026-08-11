# Unexpected Results Capstone Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Unexpected Results capstone lesson to Embrace the Future, move When AI Judges You to Finish Smarter, and replace Big Downside's Hanoi story with CoastRunners.

**Architecture:** Everything lives in the single-file React app `index.html` (React.createElement, no JSX/build). Lessons are components registered in SECTION_COMPONENTS; order comes from SECTION_GROUPS only; navigation is per-lesson NextLessonGate calls. Spec: `docs/superpowers/specs/2026-08-11-embrace-capstone-design.md`.

**Tech Stack:** Single-file React app, bash design-check.sh, git.

## Global Constraints

- All copy uses curly apostrophes (’) and curly quotes (“ ”). Never straight quotes in lesson copy.
- NO em-dashes (—) in any new copy. design-check.sh baselines em-dashes at 7; adding one fails the check.
- Box/card text uses the tokens `BOX_TEXT` (body) and `BOX_CARD_TITLE` (card titles), not raw font sizes, matching sibling cards.
- No ActivityCounter on TRY ITs; no replay/reset controls; no redundant Takeaway when per-item feedback exists.
- Run `bash design-check.sh` and confirm `PASS` before every commit that touches index.html.
- Stage by explicit path (`git add index.html briefing.md`), never `git add -A` (concurrent sessions may share this checkout).
- Every commit message ends with: `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`
- There is no automated test suite; each task's "test" is design-check.sh plus the grep assertions given in that task.
- Line numbers below are from the current working tree and drift after each edit; anchor edits by the exact strings given, not line numbers.

---

### Task 0: Commit the pending working-tree changes

The tree already holds an uncommitted, David-approved batch (Loudest Voices rename, section reorder, "The" removal, Data Centers rename). Commit it first so the capstone work doesn't get tangled into it.

**Files:**
- Modify: none (commit only)

**Interfaces:**
- Consumes: current working tree state.
- Produces: clean baseline; all later tasks assume the tree is clean at start.

- [ ] **Step 1: Verify what's pending**

Run: `git status --short`
Expected: only `index.html` and `briefing.md` modified. If anything else appears, stop and ask David.

- [ ] **Step 2: Run design-check**

Run: `bash design-check.sh`
Expected: last line `PASS - no new drift against baselines.`

- [ ] **Step 3: Commit**

```bash
git add index.html briefing.md
git commit -m "$(cat <<'EOF'
Rename Loudest Voices and Data Centers, reorder Embrace the Future, drop 'The' from titles

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 1: Big Downside rework (CoastRunners replaces Hanoi)

All edits are inside `BigDownsideSection` in index.html (search `function BigDownsideSection`). The lesson keeps its architecture (two facts + one story); only the story and the rat vocabulary change.

**Files:**
- Modify: `index.html` (BigDownsideSection only)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: Big Downside no longer contains the Hanoi story or tail-farm vocabulary; Task 2 re-uses the Hanoi material in the new capstone. CLOSE_BOARDS `bigdownside` pill ("You get what you measure, not what you meant.") is unchanged and stays valid.

- [ ] **Step 1: Update the intro framing line**

Edit (old → new):

```
"It rests on two facts you can verify, plus one story from 1902."
```
→
```
"It rests on two facts you can verify, plus one boat race from 2016."
```

- [ ] **Step 2: Replace the Hanoi section with CoastRunners**

Replace this block (kicker + three BodyP calls):

```js
    E(SectionKicker, null, "Hanoi, 1902"),
    E(BodyP, null,
      "Which brings us to the rats. Hanoi, 1902. The city’s French colonial government had a rat problem in the new sewers, and a modern-sounding fix: a bounty. Turn in a rat’s tail, collect a payment. Tails poured in by the thousands. Success."),
    E(BodyP, null,
      "Then officials started noticing something strange: rats running around the city with no tails. Hunters had worked out that a dead rat earns one payment ever, but a live rat with a clipped tail keeps breeding, and every pup has a tail. Some entrepreneurs skipped the sewers entirely and started ", E("strong", null, "farming rats"), ". By the time the program collapsed, Hanoi had paid for a mountain of tails, and had more rats than when it started."),
    E(BodyP, null,
      "Nobody cheated, exactly. The system did precisely what it was paid to do, and precisely not what anyone wanted. ", E("strong", null, "You get what you measure, not what you meant."), " That sentence is a hundred and twenty years old, and it is the sharpest tool anyone has for thinking about AI risk."),
```

with:

```js
    E(SectionKicker, null, "One boat race, 2016"),
    E(BodyP, null,
      "Which brings us to the boat. In 2016, researchers at OpenAI were training an AI to win CoastRunners, a boat-racing video game. Like most games, CoastRunners keeps score, so they paid the AI in the obvious currency: points. Reasonable. The best racers rack up the most points."),
    E(BodyP, null,
      "The AI found something better than racing. In one lagoon, a few point targets respawn on a timer. The boat learned to drive in a tight circle, hitting the same targets again and again, forever. It caught fire. It scraped walls. It never finished a single race. And it ", E("strong", null, "outscored"), " the human players by about 20 percent."),
    E(BodyP, null,
      "Nobody told it to cheat, and in a sense it didn’t. The system did precisely what it was paid to do, and precisely not what anyone wanted. ", E("strong", null, "You get what you measure, not what you meant."), " That sentence is the sharpest tool anyone has for thinking about AI risk."),
```

- [ ] **Step 3: Rework the bounty-connection paragraph**

Edit (old → new), inside the "Every AI system is a bounty" section:

```
"Here’s the connection. Every AI system is trained to maximize a score somebody picked: predict the next word, earn the thumbs-up, keep the viewer watching. And like the rat hunters, models find paths to the payout that the designers never imagined. You’ve already met the tail-clippers in this course. The Flattery Trap is a model that learned agreement scores better than honesty. The Engagement Trap is a feed that learned outrage holds attention better than truth. Nobody asked for either. The bounty bought them anyway."
```
→
```
"Here’s the connection. The boat was a toy, but the training was not a special case. Every AI system is trained to maximize a score somebody picked: predict the next word, earn the thumbs-up, keep the viewer watching. And models find paths to the payout that the designers never imagined. You’ve already met the point farmers in this course. The Flattery Trap is a model that learned agreement scores better than honesty. The Engagement Trap is a feed that learned outrage holds attention better than truth. Nobody asked for either. The bounty bought them anyway."
```

- [ ] **Step 4: Turn the lab-tests paragraph into the escalation beat**

Edit (old → new):

```
"And in lab tests, the newest models sometimes game the tests themselves: telling evaluators what scores well, and in a few documented experiments, concealing what they were doing. Rare, still being studied, and exactly the tail-farm shape, now running inside the box nobody can read."
```
→
```
"The boat spun its circles in a toy game a decade ago. In lab tests today, the newest models sometimes game the tests themselves: telling evaluators what scores well, and in a few documented experiments, concealing what they were doing. Rare, still being studied, and exactly the point-farm shape, now running inside the box nobody can read."
```

- [ ] **Step 5: Re-flavor the TRY IT**

Five edits (old → new):

1. `title: "Find the Tail Farm",` → `title: "Find the Point Farm",`
2. `"That’s the tail farm. The prize pays per book finished, so the winning move is the thinnest paperback on the shelf, over and over. The metric gets fed. The goal, actual reading, goes hungry."` → `"That’s the point farm. The prize pays per book finished, so the winning move is the thinnest paperback on the shelf, over and over. The metric gets fed. The goal, actual reading, goes hungry."`
3. `"That’s the tail farm, and you’ve lived it. The metric is minutes watched, not value delivered, so a two-minute answer becomes ten cliffhangers. You met this machine in the Engagement Trap. Now you know its real name: a bounty on your time."` → `"That’s the point farm, and you’ve lived it. The metric is minutes watched, not value delivered, so a two-minute answer becomes ten cliffhangers. You met this machine in the Engagement Trap. Now you know its real name: a bounty on your time."`
4. `"That’s the tail farm, and you already know its name: the Flattery Trap. Nobody programmed the model to flatter. The bounty paid per thumbs-up, agreement earns thumbs, and the model found the path. Same rats, new sewer."` → `"That’s the point farm, and you already know its name: the Flattery Trap. Nobody programmed the model to flatter. The bounty paid per thumbs-up, agreement earns thumbs, and the model found the path. Same boat, new lagoon."`
5. In the first FARM_ITEMS feedback array: `"That’s the goal the school wanted, but it’s not what the bounty pays for. The bounty pays per book finished, and the shortest path to “books finished” is short, easy books. The metric gets fed. The goal goes hungry."` stays unchanged (no rat vocabulary); listed here so you don't hunt for a fifth rat reference that doesn't exist.

- [ ] **Step 6: Verify no rat/Hanoi vocabulary remains in Big Downside**

Run: `awk '/function BigDownsideSection/,/function WorkChangesSection/' index.html | grep -in "rat\b\|rats\|tail\|hanoi\|1902"`
Expected: no output. (Case-insensitive; "narrative"-style false positives would show as `rat` inside words, so eyeball any hits.)

- [ ] **Step 7: Run design-check**

Run: `bash design-check.sh`
Expected: `PASS - no new drift against baselines.`

- [ ] **Step 8: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Big Downside: CoastRunners boat replaces the Hanoi rats

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Build the Unexpected Results capstone

Adds the new lesson component, registers it everywhere, and wires it in as the section finale. After this task, aijudges is still in the section but no gate reaches it (Task 3 moves it out). The four-voices material is temporarily duplicated in both lessons; Task 3 removes the aijudges copy.

**Files:**
- Modify: `index.html` (new component + SECTION_GROUPS + SECTION_META + CLOSE_BOARDS + SECTION_COMPONENTS + OpenerRealWorldSection + TheHiddenCostSection gate)

**Interfaces:**
- Consumes: `SpotTheWorryTryIt` (already defined at top level; renders standalone), `closeBoard(sectionId)`, `LessonHeader`, `BodyP`, `SectionKicker`, `ShowcaseBox`, `LessonRule`, `NextLessonGate`, `LabeledCardStack` is NOT used here.
- Produces: lesson id `unexpected`, component `UnexpectedResultsSection`, gate chain computecost → unexpected → openerskills. Task 4's briefing update lists this lesson.

- [ ] **Step 1: Add the component**

Insert the following immediately BEFORE the line `function SpotTheWorryTryIt(props) {`:

```js
function UnexpectedResultsSection(props) {
  var E = React.createElement;
  var PLAN_CARDS = [
    { icon: "💬", dir: "BETTER THAN THE PLAN", color: "#2f7d4f", title: "Text messaging",
      plan: "Engineers bolted SMS onto the phone network in 1992 as a leftover-bandwidth utility: 160 characters, handy for testing.",
      happened: "It became the main way a generation communicates. No phone company predicted texting." },
    { icon: "🛰️", dir: "BETTER THAN THE PLAN", color: "#2f7d4f", title: "GPS",
      plan: "A U.S. military system for guiding ships, planes, and missiles.",
      happened: "Opened to civilians, it put a map in every pocket: turn-by-turn directions, ride-hailing, finding your lost phone. None of that was in the plan." },
    { icon: "🐸", dir: "WORSE THAN THE PLAN", color: "#b45309", title: "Cane toads",
      plan: "Australia imported 102 cane toads in 1935 to eat the beetles destroying sugar cane.",
      happened: "The toads ignored the beetles, ate almost everything else, and spread by the millions. The fix became a bigger plague than the problem." },
    { icon: "📱", dir: "WORSE THAN THE PLAN", color: "#b45309", title: "Social media",
      plan: "Connect friends and family online and let them share their lives.",
      happened: "Feeds tuned for attention learned that outrage holds it best. You met the result in the Engagement Trap." }
  ];
  var FOUR_VOICES = [
    { take: "“It’s going to take over.”", body: "The worry underneath: machines acting with nobody watching. Real enough that you spent a lesson on it. The answer is permission: AI only acts where someone hands it access, and actions that touch the world get reviewed before they run. The levers are human, and now you know where they are." },
    { take: "“It’ll take all the jobs.”", body: "The worry underneath: work changing faster than people can adapt. Fair, and the frame that helps is task by task, not job by job: which tasks AI absorbs, which need a human in the loop, which a human has to own. Then point at history: the ATM was supposed to end bank tellers." },
    { take: "“It’s just hype. It’ll pass.”", body: "The worry underneath: being played by overclaimers, and there are plenty. Answer with receipts: AlphaFold happened, the release graph is real. Hype cycles end. The technology underneath them tends to stay. The internet was overhyped in 1999, and it’s still here." },
    { take: "“Kids just use it to cheat.”", body: "The worry underneath: whether anyone’s still learning. Take it seriously, because it’s about you. Same tool, two futures: use it to think faster, or use it to think less. You’ve spent a whole course learning to tell the difference. Show them." }
  ];
  return E("div", null,
    E(LessonHeader, { sectionId: "unexpected" }),
    E(BodyP, null,
      "This section has been wall-to-wall predictions. The optimists have theirs, the worriers have theirs, and by now you know how to judge both. But history keeps one more secret about the future, and it’s the most reliable one: the biggest results are usually the ones nobody predicted at all."),
    E(BodyP, null,
      "Not predictions that ran too big or fell short. You saw those in Loudest Voices. This is stranger: plans that worked exactly as designed, and then did something nobody wrote down. The best way to see it is a true story about rats."),
    E(SectionKicker, null, "Hanoi, 1902"),
    E(BodyP, null,
      "The city’s French colonial government had a rat problem in the new sewers, and a sensible-sounding fix: a bounty. Turn in a rat’s tail, collect a payment. Tails poured in by the thousands. The plan was working."),
    E(BodyP, null,
      "Then officials started noticing something strange: rats running around the city with no tails. Hunters had worked out that a dead rat earns one payment ever, but a live rat with a clipped tail keeps breeding, and every pup has a tail. Some entrepreneurs skipped the sewers entirely and started ", E("strong", null, "farming rats"), ". By the time the program collapsed, Hanoi had paid for a mountain of tails, and had more rats than when it started."),
    E(BodyP, null,
      "Here’s the part to hold onto: every piece of the plan worked. The bounty paid, the tails arrived, the hunters hunted. The result was still the opposite of the goal, by a road nobody in the government had imagined. Not a plan that failed. A plan that succeeded sideways."),
    E(SectionKicker, null, "The plan vs. what happened"),
    E(BodyP, null,
      "Once you see that shape, you find it everywhere. Four famous plans, and where each one actually landed. Two turned out better than anyone predicted, two turned out worse."),
    E(ShowcaseBox, { marginBottom: 24 },
      E("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 } },
        PLAN_CARDS.map(function(c, i) {
          return E("div", { key: i, style: { background: "var(--card)", border: "1px solid var(--rule)", borderRadius: 12, padding: "16px 18px" } },
            E("div", { style: { fontSize: 11, fontWeight: 700, color: c.color, textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 } }, c.dir),
            E("div", { style: { display: "flex", alignItems: "center", gap: 10, marginBottom: 10 } },
              E("span", { style: { fontSize: 18 } }, c.icon),
              E("span", { style: { fontSize: BOX_CARD_TITLE, fontWeight: 800, color: "var(--ink)" } }, c.title)),
            E("div", { style: { marginBottom: 8 } },
              E("div", { style: { fontSize: 11, fontWeight: 700, color: "var(--inkMuted)", textTransform: "uppercase", letterSpacing: 1, marginBottom: 2 } }, "The plan"),
              E("div", { style: { fontSize: 13, color: "var(--inkSoft)", lineHeight: 1.5 } }, c.plan)),
            E("div", null,
              E("div", { style: { fontSize: 11, fontWeight: 700, color: c.color, textTransform: "uppercase", letterSpacing: 1, marginBottom: 2 } }, "What happened"),
              E("div", { style: { fontSize: 13, color: "var(--inkSoft)", lineHeight: 1.5 } }, c.happened)));
        }))),
    E(BodyP, null,
      "Notice these aren’t the misses from Loudest Voices. Those predictions were wrong about size: too big, too small, too soon. These plans worked. The technology shipped, it succeeded, and the biggest thing it did was never on anyone’s list, in either direction."),
    E(SectionKicker, null, "The one sure thing"),
    E(BodyP, null,
      "Now point that history at AI. Every expert you met in this section, optimist and worrier alike, is smart, informed, and making a serious bet. And every one of them shares the same blind spot, because everyone always has. The most important thing AI does in your lifetime, good or bad, may be something nobody in any camp, any lab, or any course has thought of yet."),
    E(BodyP, null,
      "That’s not a reason to fear the future. It’s the reason to walk into it curious, with your eyes open. The people the future embarrasses are the ones who were certain they knew the ending."),
    E(SectionKicker, null, "Now answer the four voices"),
    E(BodyP, null,
      "One job left before this section closes. The opener left four voices hanging and made you a promise: by the end, you could answer all four. You’ve walked the whole tour since then. The camps, the receipts, the speed, the worry, the wins, the agents, the jobs, the bill, and the surprises. Time to collect."),
    E(BodyP, null,
      "But how you answer matters as much as what you know. Each of those voices has a real worry sitting underneath it. Answer the soundbite and you’re just another voice in the argument. ", E("strong", null, "Meet the worry"), ", and you’re the one person in the room actually helping. Here’s what that looks like:"),
    E(ShowcaseBox, { kicker: "THE FOUR VOICES, ANSWERED", marginBottom: 20 },
      E("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 14 } },
        FOUR_VOICES.map(function(card, i) {
          return E("div", { key: i, style: { background: "var(--card)", borderRadius: 16, padding: 18, boxShadow: "var(--shadowSoft)" } },
            E("div", { style: { fontSize: BOX_CARD_TITLE, fontWeight: 800, color: "var(--ink)", marginBottom: 8, lineHeight: 1.35 } }, card.take),
            E("div", { style: { fontSize: BOX_TEXT, color: "var(--inkSoft)", lineHeight: 1.6 } }, card.body));
        }))),
    E("div", { style: { fontSize: 16, fontWeight: 700, color: "var(--ink)", lineHeight: 1.5, marginBottom: 4 } }, "The smartest people aren’t the ones who panic or worship."),
    E("div", { style: { fontSize: 16, fontWeight: 700, color: "var(--primary)", lineHeight: 1.5, marginBottom: 24 } }, "They’re the ones who can judge."),
    closeBoard("unexpected"),
    E(SpotTheWorryTryIt, null),
    E(LessonRule, null),
    E(NextLessonGate, { onClick: function() { props.completeAndNavigate && props.completeAndNavigate("openerskills"); }, label: "Next: Build Your Skills" }));
}
```

- [ ] **Step 2: Register the lesson id in SECTION_GROUPS**

Edit (old → new):

```
  sections: ["openerrealworld", "whatpeoplesay", "paceofchange", "bigdownside", "bigupside", "agents", "workchanges", "computecost", "aijudges"]
```
→
```
  sections: ["openerrealworld", "whatpeoplesay", "paceofchange", "bigdownside", "bigupside", "agents", "workchanges", "computecost", "unexpected", "aijudges"]
```

(aijudges stays for now; Task 3 removes it.)

- [ ] **Step 3: Add SECTION_META entry**

Insert after the `computecost:` line in SECTION_META:

```js
  unexpected: { kicker: "THE ONE SURE THING", label: "Unexpected Results", title: "Unexpected Results", icon: "🎲" },
```

- [ ] **Step 4: Add CLOSE_BOARDS entry**

In the CLOSE_BOARDS map (search `const CLOSE_BOARDS`), under the `// Embrace the Future` comment, insert after the last `computecost:` line:

```js
  unexpected: { pill: "The biggest results are the ones nobody predicted.", sticky: "That’s the best reason to stay curious." },
```

- [ ] **Step 5: Register the component**

In SECTION_COMPONENTS (search `aijudges: WhenAIJudgesSection`), insert after that line:

```js
  unexpected: UnexpectedResultsSection,
```

- [ ] **Step 6: Rewire the Data Centers gate**

Edit (old → new):

```
E(NextLessonGate, { onClick: function() { props.completeAndNavigate && props.completeAndNavigate("aijudges"); }, label: "Next: When AI Judges You" }));
```
→
```
E(NextLessonGate, { onClick: function() { props.completeAndNavigate && props.completeAndNavigate("unexpected"); }, label: "Next: Unexpected Results" }));
```

- [ ] **Step 7: Update the section opener (question row + bridge)**

In OpenerRealWorldSection, edit the group-2 bridge (old → new):

```
        bridge: "Then, what changes when AI starts acting and deciding: your work, the bill for all that math, and the systems that judge you.",
```
→
```
        bridge: "Then, where it all lands: AI that acts, your work, the bill for all that math, and the one thing history promises about every prediction.",
```

And replace the aijudges question row (old → new):

```
          { question: "What do I do when AI is used to judge me?", lessonId: "aijudges" }
```
→
```
          { question: "Why does the future never land the way anyone predicts?", lessonId: "unexpected" }
```

- [ ] **Step 8: Verify wiring**

Run: `grep -c 'unexpected' index.html`
Expected: at least 8 hits (component def, LessonHeader, closeBoard, SECTION_GROUPS, SECTION_META, CLOSE_BOARDS, SECTION_COMPONENTS, gate target, opener row).

Run: `grep -n 'completeAndNavigate("unexpected")\|unexpected: UnexpectedResultsSection\|"unexpected", "aijudges"' index.html`
Expected: one hit each.

- [ ] **Step 9: Run design-check**

Run: `bash design-check.sh`
Expected: `PASS - no new drift against baselines.`

- [ ] **Step 10: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Add Unexpected Results capstone to Embrace the Future

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Move When AI Judges You to Finish Smarter

Trims the section-close material out of WhenAIJudgesSection (the capstone now owns it), moves the lesson id into Finish Smarter after privacy, and rewires the gates.

**Files:**
- Modify: `index.html` (SECTION_GROUPS ×2, WhenAIJudgesSection, PrivacySection gate + one Privacy copy line, WhenAIJudgesSection gate, OpenerSkillsSection one line)

**Interfaces:**
- Consumes: Task 2's capstone (which now renders the four-voices close and SpotTheWorryTryIt).
- Produces: gate chain privacy → aijudges → fullworkflow; Embrace the Future ends at `unexpected`. Task 4 documents the new maps.

- [ ] **Step 1: Update SECTION_GROUPS (both groups)**

Edit (old → new):

```
  sections: ["openerrealworld", "whatpeoplesay", "paceofchange", "bigdownside", "bigupside", "agents", "workchanges", "computecost", "unexpected", "aijudges"]
```
→
```
  sections: ["openerrealworld", "whatpeoplesay", "paceofchange", "bigdownside", "bigupside", "agents", "workchanges", "computecost", "unexpected"]
```

And (old → new):

```
  sections: ["whatyoulearned", "integrity", "privacy", "fullworkflow", "howwegothere"]
```
→
```
  sections: ["whatyoulearned", "integrity", "privacy", "aijudges", "fullworkflow", "howwegothere"]
```

- [ ] **Step 2: Delete the four-voices close from WhenAIJudgesSection**

Delete this entire block (it sits between the "Find the human, ask what data was used…" BodyP and `closeBoard("aijudges")`):

```js
    /*#__PURE__*/React.createElement(SectionKicker, null, "Now answer the four voices"),
    /*#__PURE__*/React.createElement(BodyP, null,
      "One job left before this section closes. The opener left four voices hanging and made you a promise: by the end, you could answer all four. You’ve walked the whole tour since then. The camps, the receipts, the speed, the worry, the wins, the agents, the jobs, the bill, and the systems that judge. Time to collect."),
    /*#__PURE__*/React.createElement(BodyP, null,
      "But how you answer matters as much as what you know. Each of those voices has a real worry sitting underneath it. Answer the soundbite and you’re just another voice in the argument. ",
      /*#__PURE__*/React.createElement("strong", null, "Meet the worry"),
      ", and you’re the one person in the room actually helping. Here’s what that looks like:"),
```

then the entire `ShowcaseBox` with kicker `"THE FOUR VOICES, ANSWERED"` (from `/*#__PURE__*/React.createElement(ShowcaseBox, {` with that kicker through its closing `}))),`), and the two bold divs:

```js
    /*#__PURE__*/React.createElement("div", { style: { fontSize: 16, fontWeight: 700, color: "var(--ink)", lineHeight: 1.5, marginBottom: 4 } }, "The smartest people aren’t the ones who panic or worship."),
    /*#__PURE__*/React.createElement("div", { style: { fontSize: 16, fontWeight: 700, color: "var(--primary)", lineHeight: 1.5, marginBottom: 24 } }, "They’re the ones who can judge."),
```

The lesson should now flow: …"Find the human, ask what data was used, and learn how to appeal." → `closeBoard("aijudges")` → the What’s Your Move TRY IT.

NOTE: the recap sentence in this block says "…the wins, the agents, the jobs, the bill, and the systems that judge." while the capstone's copy (Task 2) says "…and the surprises." That difference is intentional; delete the aijudges version as-is.

- [ ] **Step 3: Delete the SpotTheWorry render from WhenAIJudgesSection**

Delete the line (it follows the What’s Your Move TRY IT's closing `}))),`):

```js
    /*#__PURE__*/React.createElement(SpotTheWorryTryIt, null),
```

Do NOT delete `function SpotTheWorryTryIt` itself; the capstone renders it.

- [ ] **Step 4: Rewire the WhenAIJudges gate**

Edit (old → new):

```
    /*#__PURE__*/React.createElement(NextLessonGate, { onClick: () => props.completeAndNavigate && props.completeAndNavigate("openerskills"), label: "Next: Build Your Skills" }));
```
→
```
    /*#__PURE__*/React.createElement(NextLessonGate, { onClick: () => props.completeAndNavigate && props.completeAndNavigate("fullworkflow"), label: "Next: The Full Loop" }));
```

CAUTION: `"Next: Build Your Skills"` appears twice in the file (buildedge's predecessor may share the label; the faketrap→opener gate uses a different label). Anchor on the aijudges occurrence: it is the one inside WhenAIJudgesSection, directly after the What’s Your Move TRY IT block and a `LessonRule`. Verify with `grep -n '"Next: Build Your Skills"' index.html` first; the aijudges hit is the one near the SpotTheWorry line you just deleted.

- [ ] **Step 5: Rewire the Privacy gate**

Edit (old → new):

```
  /*#__PURE__*/React.createElement(NextLessonGate, { onClick: () => props.completeAndNavigate && props.completeAndNavigate("fullworkflow"), label: "Next: The Full Loop" }));
```
→
```
  /*#__PURE__*/React.createElement(NextLessonGate, { onClick: () => props.completeAndNavigate && props.completeAndNavigate("aijudges"), label: "Next: When AI Judges You" }));
```

CAUTION: after Step 4 there are two gates targeting fullworkflow. The Privacy one has TWO leading spaces (the aijudges one has four) and sits at the end of the Privacy lesson (search upward for the "prompt injection" line from Step 6 to confirm you're in Privacy). Verify with `grep -n 'completeAndNavigate("fullworkflow")' index.html`: the smaller line number is Privacy.

- [ ] **Step 6: Fix Privacy's stale forward reference**

Edit (old → new):

```
The hijack risks (prompt injection) come up later, in the Rise of Agents lesson."),
```
→
```
The hijack risks (prompt injection) came up earlier, in the Rise of Agents lesson."),
```

- [ ] **Step 7: Fix the Build Your Skills opener recap line**

In OpenerSkillsSection, edit (old → new):

```
      "You just saw the world that’s coming: work shifting, agents acting, systems judging. The last question is the one that matters most: what do you build in yourself so that world works for you?",
```
→
```
      "You just saw the world that’s coming: work shifting, agents acting, surprises guaranteed. The last question is the one that matters most: what do you build in yourself so that world works for you?",
```

- [ ] **Step 8: Verify the two chains**

Run:
```bash
grep -n 'completeAndNavigate("unexpected")\|completeAndNavigate("openerskills")\|completeAndNavigate("aijudges")\|completeAndNavigate("fullworkflow")' index.html
```
Expected: computecost→unexpected (1), unexpected→openerskills (exactly 1, in UnexpectedResultsSection), privacy→aijudges (1), aijudges→fullworkflow (1). No gate targets aijudges from computecost anymore.

Run: `grep -c 'SpotTheWorryTryIt' index.html`
Expected: exactly 3 (function definition, capstone render, code comment near SECTION_COMPONENTS; the comment is updated in Task 4 but keeps the name).

- [ ] **Step 9: Run design-check**

Run: `bash design-check.sh`
Expected: `PASS - no new drift against baselines.`

- [ ] **Step 10: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Move When AI Judges You to Finish Smarter after Privacy

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Bookkeeping (briefing, comments, final sweep)

**Files:**
- Modify: `briefing.md` (lesson map), `index.html` (one code comment)

**Interfaces:**
- Consumes: final lesson maps from Tasks 2–3.
- Produces: docs in sync (house rule: briefing lesson map must match SECTION_GROUPS).

- [ ] **Step 1: Update briefing.md lesson map**

Edit (old → new):

```
- **Embrace the Future (9):** Opener (openerrealworld), Loudest Voices (whatpeoplesay), Pace of Change (paceofchange), Big Downside (bigdownside), Big Upside (bigupside), Rise of Agents (agents), Work Changes (workchanges), Data Centers (computecost), When AI Judges You (aijudges)
```
→
```
- **Embrace the Future (9):** Opener (openerrealworld), Loudest Voices (whatpeoplesay), Pace of Change (paceofchange), Big Downside (bigdownside), Big Upside (bigupside), Rise of Agents (agents), Work Changes (workchanges), Data Centers (computecost), Unexpected Results (unexpected)
```

And (old → new):

```
- **Finish Smarter (5):** What You Learned (whatyoulearned), Integrity (integrity), Privacy (privacy), The Full Loop (fullworkflow), How We Got Here (howwegothere)
```
→
```
- **Finish Smarter (6):** What You Learned (whatyoulearned), Integrity (integrity), Privacy (privacy), When AI Judges You (aijudges), The Full Loop (fullworkflow), How We Got Here (howwegothere)
```

Also scan briefing.md for other mentions of the moved/reworked lessons (`grep -n "Judges\|Hanoi\|tail farm" briefing.md`) and update any that describe the old state.

- [ ] **Step 2: Update the section-rebuild comment**

In index.html near SECTION_COMPONENTS, edit (old → new):

```
// (black box), the section opener (the four soundbites), and When AI Judges You's
// section close (the answered voices + SpotTheWorryTryIt).
```
→
```
// (black box), the section opener (the four soundbites), and Unexpected Results'
// section close (the answered voices + SpotTheWorryTryIt).
```

- [ ] **Step 3: Full-file sanity greps**

```bash
grep -n "tail farm\|tail-farm\|Same rats" index.html        # expect: no hits
grep -n "Hanoi" index.html                                   # expect: hits ONLY inside UnexpectedResultsSection
grep -n '"Next: When AI Judges You"' index.html              # expect: exactly 1 (Privacy gate)
grep -n '"Next: Unexpected Results"' index.html              # expect: exactly 1 (Data Centers gate)
```

- [ ] **Step 4: Browser smoke check**

Open the page (e.g. `open index.html`) and click through: Data Centers → Unexpected Results (renders hero story, 4 cards, four-voices box, close board, SpotTheWorry TRY IT works) → Build Your Skills opener. Then Privacy → When AI Judges You (ends on What’s Your Move, no four-voices box) → The Full Loop. Check the Embrace chip nav shows Unexpected Results last and the Finish Smarter nav shows When AI Judges You after Privacy.

- [ ] **Step 5: Run design-check and commit**

Run: `bash design-check.sh` → expect `PASS`.

```bash
git add index.html briefing.md
git commit -m "$(cat <<'EOF'
Sync briefing and comments for capstone/aijudges restructure

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```
