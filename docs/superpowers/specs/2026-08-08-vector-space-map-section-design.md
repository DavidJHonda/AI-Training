# Vector Space: rework the map sections

**Date:** 2026-08-08
**File:** `index.html`, the `vectorspace` lesson
**Span:** from the `AI uses a map (kind of)` kicker (line 5692) to just before the
`Distance` kicker (line 5787). `Distance` and everything after it is untouched.

## Goal

Owner's outline. The current text narrates the map exercise at the reader; the rework
hands it to them and then confirms. The load-bearing addition is "let's pretend those are
the only three cities in the United States" — it turns "closest" from a vague question
into a well-defined one.

## Decisions taken during design

1. **Bullets, not a TRY IT.** The coordinate matching reads like an activity prompt, and
   Vector Space has no lesson TRY IT of its own, so an interactive version was considered.
   Rejected for now: it changes the lesson's pacing and it is a much bigger build. Worked
   examples keep the reading rhythm and keep the drinks exercise parallel in form.
2. **Crosshairs survive the map deletion.** The Dallas-only map is the only place in the
   lesson where a latitude and a longitude are drawn as *lines* converging on a point.
   Deleting it outright would leave the opening paragraph's "a north latitude of 33 and a
   west longitude of 97" with nothing showing what those numbers do. The lines move onto
   Dallas in the surviving 3-city map.
3. **The AI turn happens once.** The outline made it twice, one line apart across a section
   break: "You did exactly what AI does" closing the map section, then "Let's apply the same
   concept to AI" opening the next. The closing line is the stronger one and it earns the
   break, so the opener drops its first sentence and goes straight to the complication.
4. **"Distance" is named once before it is defined.** The outline named it three times ahead
   of the `Distance` kicker that defines it. Cut from the map section's close; it now first
   appears in the `How AI does it` opener and is defined one kicker later.

## The new prose

### AI uses a map (kind of)

Paragraph 1 — **unchanged**:

> A regular map works like this. You can find any place by knowing two things: the latitude
> and the longitude. Want to find Dallas, Texas? Just give it a north latitude of 33 and a
> west longitude of 97.

Paragraph 2 — **reworded**:

> Can we add New York City and Mountain View, California? Yep. They track the same
> dimensions.

*[3-city map, Dallas crosshaired]*

Paragraph 3 — **replaces** "Now turn it around…":

> Now, let's pretend those are the only three cities in the United States. Your job is
> simple. You get the coordinates and have to match them to the closest city.

Bullets — **new**:

> - `38 N, 120 W`. That's right. The closest match is Mountain View.
> - `39 N, 70 W`? Of course, New York City.

**Comma, not "and" — forced by the mono treatment, changed during the build.** The outline
reads "38 N and 120 W". Rendered, that put a monospace word-space inside `38 N` that is
visibly *wider* than the proportional space before "and", so the line read as "38 Nand
120 W". Making each pair a single mono unit removes the artifact and matches the map's own
city chips, which already read `37 N, 122 W`. Revert to "and" only by also dropping the
mono on these two bullets.

Paragraph 4 — **replaces** "Notice what you just did there…":

> You did exactly what AI does. There was no match for the numbers, so you found the
> closest match.

### How AI does it

Paragraph 5 — **replaces** the Embeddings callback opener:

> Of course, the way AI does it is much more complicated, because there are many more
> dimensions than two. But the core idea is the same: it establishes meaning based on
> distance.

Paragraph 6 — **new**:

> This is how you learned a token's meaning with numbers: a taste profile of Coke vs.
> Pepsi vs. Coffee.

*[Taste Profile table — unchanged]*

Paragraph 7 — **"Notice how" dropped**:

> Coke and Pepsi's vectors (their rows of numbers) sit much closer to each other than
> either does to Coffee. If this was a map, it might look like this.

*[drinks neighborhoods map — unchanged]*

Paragraph 8 — **unchanged**:

> On the map, Coke and Pepsi sit side by side in the Soft drinks neighborhood. Coffee is
> all the way across, in the Hot drinks neighborhood.

Paragraph 9 — **replaces** "Now ask the same question…":

> Let's try the same exercise you used on a real map. Here are coordinates you need to
> match to a drink. Those numbers don't exist on the table, so you need to figure out
> which drink these numbers mean.

Bullet — **new**, and it states the answer the current text leaves hanging:

> - `9, 1, 10, 2, 3, 8, 9`. A fizz of 10 puts it with the sodas, and a citrus of 9 puts it
>   right beside Pepsi. It doesn't match anything on file exactly, and it doesn't have to.
>   You know it refers to Pepsi.

### Copy fixes applied from the outline

`Coffe` → Coffee. `it established meaning` → establishes. Three semicolons resolved to
house punctuation: `complicated; because` → comma, `numbers; a taste profile` → colon,
`the same; it establishes` → colon.

`If this was a map` keeps its indicative mood — it is already on the page that way and the
lesson's voice is conversational.

## Mechanics

### Delete the Dallas-only map, crosshair the 3-city map

Remove the first `mapBox` (currently lines 5695–5702). Move its two dashed lines into the
surviving 3-city `mapBox`, **before** the three star paths so the stars paint over them:

```js
E("line", { key: "lat", x1: -126, y1: -32.78, x2: -96.8, y2: -32.78, stroke: "#e6394d", strokeWidth: 0.25, strokeDasharray: "1 0.8", opacity: 0.75 }),
E("line", { key: "lon", x1: -96.8, y1: -24.4, x2: -96.8, y2: -32.78, stroke: "#e6394d", strokeWidth: 0.25, strokeDasharray: "1 0.8", opacity: 0.75 }),
```

They drop in unchanged. The horizontal runs from lon −126 to Dallas at lat 32.78, passing
south of Mountain View (lat 37.39); the vertical sits in Texas between lat 24.4 and 32.78.
Neither collides with the two new stars.

### A local bullet helper

There is no body-bullet primitive on the page — the only `ul` is a checkmark list inside a
card in a different lesson, and it is card-scale (14px), not body-scale. Add `bulletList`
next to `starAt` / `cityChip` / `usMap` / `mapBox`, which are already local to this lesson:

```js
var bulletList = function(items) {
  return E("ul", { style: { listStyle: "none", padding: 0, margin: "0 0 18px" } },
    items.map(function(item, i) {
      return E("li", { key: i, style: {
        color: "var(--inkSoft)", fontSize: 17, lineHeight: 1.65,
        marginBottom: i === items.length - 1 ? 0 : 10,
        paddingLeft: 22, position: "relative"
      } },
        E("span", { style: { position: "absolute", left: 4, top: 0, color: "var(--primary)", fontWeight: 700 } }, "•"),
        item);
    }));
};
```

Body typography (17px, `--inkSoft`, line-height 1.65) matching `BodyP`, so the bullets read
as prose that happens to be listed rather than as a box. The dot is `--primary`.

**Deliberately local, not a shared component.** A catalogue entry would require a
screenshot recapture plus README and briefing syncs, which one lesson does not justify.
Promote it if bullets appear in a second lesson.

Because `bulletList` is not a `BodyP`, the paragraph immediately before each list keeps its
default 18px bottom margin and the list carries its own 18px below — no spacing override
needed.

### Mono number sequences

Set the coordinate and vector sequences in `var(--mono)` inline — `38 N`, `120 W`, `39 N`,
`70 W`, and `9, 1, 10, 2, 3, 8, 9` — so they read as coordinates rather than sentence text
and tie back to the Taste Profile table, which is already mono. This is an addition to the
owner's outline, flagged here so it can be dropped on review.

## Owner revisions after first render (2026-08-08)

1. **Bullets indented and split across two lines.** They were getting lost against the body
   column. Dot at 34px, text at 62px, and each item is now `{ lead, body }` — the mono
   coordinates on their own line, the answer on the next starting at the same x, so the
   numbers stay a scannable column. All three leads take a `?`: once stacked, the outline's
   period-on-the-first, question-mark-on-the-second read as a mistake rather than a choice.
2. **`Distance` opener reworded**: "AI does the same thing, just on a massive scale." →
   "Of course, AI does it on a massive scale."
3. **The closeness paragraph folded up, not deleted.** The owner asked whether "That
   closeness is no accident…" could go. Two of its four sentences did restate the paragraph
   above ("Training nudged every token's numbers" against "AI learned every one of those
   values during training"; "words used in similar ways ended up in similar places" against
   "tokens that mean similar things sit close together"). But the `c1f0abb` rebuild added
   this beat on purpose — two independent reads had found that "closest" was never made
   legitimate, that nearness reads as a fallback trick. So the paragraph is gone as a
   paragraph and its one non-redundant idea rides on the end of the previous one:
   "…tokens that mean similar things sit close together, so landing near a token is not a
   near miss. It is how the meaning gets read." `Distance` is now two paragraphs.

4. **Map 25% larger**: `mapBox` maxWidth 500 → 625. Safe now that only one map remains. The
   SVG is width-100% and the city chips are positioned in percentages, so everything scales;
   the chip label sizes are fixed px, so they now read proportionally smaller against the
   larger map, which helps. Narrow viewports are unaffected — this is a max, and they were
   already below 500.
5. **`How AI does it` → `AI is way more complicated`**, and its paragraph opener "Of course,
   the way AI does it is much more complicated, because" → "You've learned". The complication
   moves into the kicker so the paragraph can go straight to the reversal: "You've learned
   there are many more dimensions than two. But the core idea is the same: it establishes
   meaning based on distance."

This also resolved the "Of course," echo logged in the previous pass. Two remain in the
lesson and they do not collide: one is a bullet answer ("Of course, New York City."), the
other opens the second `Distance` paragraph.

## Verification

1. `bash design-check.sh` and reconcile every FLAG before committing `index.html`.
2. Load the lesson and read the whole span top to bottom, checking that the two lists sit
   at body scale and do not read as boxes.
3. Confirm the crosshairs land on Dallas in the 3-city map and cross no other star or chip.
4. Confirm only one map now appears before the `How AI does it` kicker.

## Out of scope

Owner's instruction: the lesson itself first. `lessons/vector-space.md`, the PDF, the board
captures, the video prompt and `videos/vector-space.mp4` all drift from this change and are
deliberately left for a later pass.

**The drift is not prose-only — record it now so the later pass does not miss it.**
`lessons/vector-space-1-cities.jpg` is a true capture of the very component this change
edits: the 3-city map, currently three bare stars with coordinate chips. Adding the
crosshairs changes that board, so under the board-content-parity house rule the shipped
`videos/vector-space.mp4` is flagged by this edit and the board needs recapturing before
any re-roll. `vector-space-2-taste.jpg` and `-3-drinks.jpg` capture components this change
does not touch, and `-4-sentence.jpg` and `-5-close.jpg` sit past the reworked span, so
those four stay valid.
