# Engine-drawn boards that aren't in the kit — 2026-07-28

**Question asked:** across every video except `welcome` and the five marked FINAL & DONE,
which teaching boards did the engine draw for itself that the lesson has no kit board for?
Those are the ones to hand it on the next roll instead of letting it invent them again.

**Scope:** 31 videos. Excluded: `welcome` (kit rebuilt the same day), and FINAL & DONE —
`how-an-llm-works`, `does-school-matter`, `ai-is-different`, `transformer`, `hallucination`.
`transformers-quiz` is in scope but is the TRY IT quiz video and has no lesson boards by
design; nothing to do there.

**Method:** `scripts/video/board_filter.py` — one representative frame per scene (the LAST
frame, since the engine animates builds), ranked by how much each looks like a flat-UI board
rather than marker b-roll, read as contact sheets. Then every candidate was grepped against
the lesson's own `.md` to see whether the content is the lesson's or the engine's.

---

## The headline: most of these are the lesson's OWN page elements, never captured

The strongest finds are not the engine inventing teaching material. They are cards and tables
that **already exist on the lesson page**, in three lessons that have **zero kit boards**. The
engine read the `.md`, saw the structure, and redrew it — badly and inconsistently, because it
was guessing at a layout the page already defines.

So for most of Tier 1 the job is **capture, not author.** No copy to write, no design decision:
point `capture-board.sh` at the element that is already there.

---

## Tier 1 — capture what the page already has (3 lessons, 0 kit boards each)

| Lesson | Board | Video hold | Already on the page? |
|---|---|---|---|
| tokens | **human vs AI on the word "cat"** — HUMAN "Instant Understanding" (soft fur, whiskers, sits on your keyboard) vs AI "Just a Number" (cat → 9246, a number, not meaning yet) | 1:55–2:21 (26s) | ✅ `tokens.md` L96-115 |
| tokens | **the numbered token-split table** — unbelievable → un\|believ\|able; basketball → basket\|ball; ChatGPT → Chat\|G\|PT; "I ❤️ AI"; the URL split into 7 | 2:34–3:12 (38s) | ✅ `tokens.md` L117+ |
| does-ai-think | **"When you think vs. what AI does"** — 5 rows: understand what words mean / matches patterns; draw on real experience / only reads about the world; choose words to make a point / predicts the next likely word; feel when something's beautiful / echoes what others call beautiful; know when you're unsure / can't tell when it's making things up | 2:36–3:25 (**49s**) | ✅ `does-ai-think.md` L28-50 |
| does-ai-think | **"Inside the giant rulebook"** — IF YOU SEE / THE MOST LIKELY NEXT SYMBOL IS, then "Match the shape. Send back the likely reply. Understand nothing." | 1:42–1:59 (17s) | ⚠️ Chinese Room is in prose (L13); the rulebook table is the engine's staging of it |
| vector-space | **"airplane" in two sentences** — folded a paper airplane / NEARBY: paper, fold, toy, glide  vs  roared down the runway / NEARBY: jet, runway, pilot, flight | 1:43–2:11 (28s) | ✅ `vector-space.md` L149+ |

The 49-second does-ai-think hold is the single biggest one in the sweep. A board held that long
with why-carrying rows is exactly the shape that took `layers` from 10 to 13/15 on
teaches-vs-recites.

## Tier 2 — real boards, content is in the lesson, no page element yet

| Lesson | Board | Video hold | Source |
|---|---|---|---|
| embeddings | **Embedding Table** — token ID 9246 → its row of numbers, labelled "Embedding Vector" | 2:31–2:41 | prose L161 describes exactly this |
| flattery-trap | **"The standing instruction"** — *Be blunt with me. Lead with what's weak, skip the empty praise, and tell me when I'm wrong.* | 3:38–3:47 | verbatim, L139 |
| flattery-trap | **Supportive Assistant** — THOUGHTS → INSIGHTFUL, OPINIONS → CORRECT, DRAFTS → STRONG | 0:07–0:12 | the lesson's framing, compressed |
| flattery-trap | **Internal Weights** pulled toward *Agreeable Responses*, away from *Accurate Critique* | 1:44–1:54 | the RLHF passage, L45 |
| layers | **Layer Unit** — Attention and Transformation drawn as one unit, not two steps | 1:06–1:11 | the lesson's pairing |
| ai-is-math | **"Update With New Evidence"** — crosses out ruled-out outcomes, recounts, lands "the evidence didn't just rule things out, it moved the probability from 25% to 50%. That update is conditional probability." | 2:07–2:27 | check against `ai-is-math-1-update` before building |
| ai-is-math | **"List Possible Outcomes" + "The Math"** — the worked formula, two states (1 coin → 50%, 2 coins → 25%) | 0:36–0:52, 1:12–1:31 | the lesson's worked example |
| evaluate-the-results | **Verified Fact vs Hallucination** — two assistant cards side by side | 0:28–0:38 | ⚠️ see factual note below |
| context-window | **what's OUTSIDE the window** — older chats, web pages you didn't send, notes on your computer, other apps and tabs | ~1:00–2:36 | `2-five-sources` covers what's IN; this is the missing half |

## Tier 3 — small, take them or leave them

- **art-of-prompting** 3:26 — the three moves recapped over an effort scale (Quick Facts → Real Work → Major Projects)
- **critical-thinking** 1:15 — Claim → Context / Evidence → Truth
- **training** 4:09 — AI Output: Fluency 100% / Factual Accuracy ? *(engine's framing, not in the lesson)*
- **training** 4:39 — Personal Files + Live Web Search around a Frozen Core Model
- **opener-work** 2:03 — 1 Know What It's For / 2 Use It Well / 3 Think Before You Trust
- **where-ai-works-best** 2:48 — Facts + Constraints → Goal → Answer
- **why-learn-ai** 2:42 — Idea vs Execution
- **embeddings** 0:24 — Word / Token ID (cat 9246, dog 1053)
- **mind-trap** 0:15 — Michigan vs Indiana comparison *(see factual note)*

## No new boards — the engine used the kit

`art-of-prompting` (bar the recap), `document-trap`, `engagement-trap`, `fake-trap`,
`how-ai-answers`, `learn-with-ai`, `one-more-thing`, `opener-avoid`, `opener-understand`,
`questions-matter`, `support-trap`, `what-is-ai`, `what-you-can-control`, `which-app`.

`how-ai-answers` (10 boards) and `opener-understand` are the cleanest: every board-shaped
thing on screen traces to a kit jpg.

---

## Things found along the way, not part of the ask

1. **`training-bias` still has the NotebookLM watermark burned in** — 112 of 146 sampled
   frames, max detector score 0.995, from frame 0. The 7/27 removal pass missed it. Swept the
   full catalogue of 37 to confirm: it is the only real one. Four others tripped the 0.45
   threshold on a single frame each (`ai-is-math` 0.462, `learn-with-ai` 0.476, `what-is-ai`
   0.481 ×3, `where-ai-works-best` 0.467) — that is threshold noise, not a mark: confirmed
   clean videos score 0.33–0.43, and a real mark scores 0.99 on most frames, not one.
2. **`learn-with-ai`'s video says "NotebookLM"** on the feed-in/get-out board, but the lesson
   was renamed to Gemini Notebook (f8f79e6) and its kit board recaptured. Same staleness as
   welcome: the video is now off by a name.
3. **`mind-trap` 0:15 labels Indiana University a "Small College."** It is not.
4. **`evaluate-the-results` 0:28** renders the Petronoski example as "the 1932 winter athletic
   games." The lesson says the 1932 Olympics in Athens, and its whole point is that the 1932
   Games were in Los Angeles. The board softens the claim the lesson is making.
5. **`ai-is-math` has two close boards** — 4:07 "Two ideas, plus the loop." and 4:22 "A chance.
   A clue. One word at a time.", same sticky under both.
6. **`tokens` 1:34 vocabulary chart is NOT invented** — ChatGPT 200,000 / Gemini 256,000 are
   the lesson's own figures (L83). Flagged during the sweep, then cleared.

## Tools added

- `scripts/video/board_scan.py` — one frame per scene, scene-END (built state), contact sheets
- `scripts/video/board_filter.py` — same, ranked by flat-UI-board-ness so boards surface first

Both rank rather than filter; low scorers still get written to `rest*.jpg` so nothing is
silently dropped.
