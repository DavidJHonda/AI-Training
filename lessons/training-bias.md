## AVOID TRAPS

# Training Bias

Sometimes AI doesn’t invent anything. Every fact is real, but the picture is still distorted.

Imagine the only driving advice online came from professional race car drivers. If you asked, “What’s the best way to drive?” Claude or ChatGPT might tell you to drive 180 miles per hour on a closed track.

This is called Training Bias. The data the model learned from during training was uneven, incomplete, or full of shortcuts, so AI treats a narrow slice of reality as the whole picture.

## Cows on the beach

Computer-vision researchers hit a famous version of this. They had a model that could spot cows in photos with high accuracy. Then they showed it a cow on a beach, and it went blank. Same animal, same shape, same spots.

The model trained on photos that almost all showed cows on green pasture. So, the model learned the wrong pattern: green grass means cow. It never learned the animal. It learned the background.

## How Training Bias gets in

Not one mechanism. Three overlapping ones, all rooted in the data the model was trained on.

📈

Defaults

Some cases appear too often in the data. The model treats them as the default.

📉

Blind Spots

Some cases appear too rarely. The model performs worse when those cases come up.

🪤

Wrong Patterns

A wrong clue happens to work in training. The model learns the clue instead of the real concept.

You can’t fact-check your way out of this trap: every fact in a distorted answer can check out. The tell is sameness: **when every example looks alike, you’re seeing the model’s default, not the world.** When you spot it, three questions crack the picture open:

1

“What’s missing from this answer?”

2

“Show me examples that don’t fit the pattern you just gave.”

3

“Answer again, leaving out the most famous examples.”

The model usually has the rest of the picture. It just doesn’t lead with it.

## Stale information

One more data trap, and this one isn’t bias or hallucination. We hit it ourselves while building this course. We asked Claude to check an example sentence for the Tokens lesson:

## You

What about “Cooper Flagg is an amazing basketball player for the Dallas Mavericks”?

## Claude

One flag though: is Cooper Flagg actually on the Mavericks? I believe he was drafted by a different team. You’d want to verify that before committing it to the course.

Claude was wrong to doubt it. Flagg went to the Mavericks with the first pick of the 2025 draft. But Claude’s training ended before draft night, so a true sentence looked wrong to it. Notice what it did right, though: it flagged its doubt and asked us to verify instead of asserting. When the date matters, that’s your move too.

## What happens

Training stopped on a cut-off date. Ask about anything newer, and the model answers as if time never passed.

## The fix

For anything that can change, check the date. The model doesn’t always search the web on its own. When it matters, ask it to search.

AI learned from what we wrote.

Flaws in the data become flaws in the answers.
