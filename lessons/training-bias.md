## AVOID TRAPS

# Training Bias

Sometimes AI doesn’t invent anything. Every fact in the answer is real, but the picture is still distorted.

One big cause is training bias. The model learns whatever patterns are in the data it saw. If the data is uneven, incomplete, or full of shortcuts, the model can treat a narrow slice of reality as the default.

Imagine the only driving advice online came from professional race car drivers. If you asked, “What’s the best way to drive?” the model might tell you to drive 180 miles per hour on a closed track.

That answer wouldn’t come from evil intent. It would come from a narrow slice of data treated like the whole picture.

## Cows on the beach

Computer-vision researchers hit a famous version of this. They had a model that could spot cows in photos with high accuracy. Then they showed it a cow on a beach, and it went blank. Same animal, same shape, same spots.

The model was training with photos that almost all showed cows on green pasture. So, the model learned the wrong pattern: green grass means cow. It never learned the animal. It learned the background.

## How bias gets in

Not one mechanism. Four overlapping ones, all rooted in the data the model was trained on.

📈

Overrepresentation

Some cases appear too often in the data. The model treats them as the default.

📉

Underrepresentation

Some cases appear too rarely. The model performs worse when those cases come up.

🪤

Shortcuts

A wrong clue happens to work in training. The model learns the clue instead of the real concept.

🏷️

Biased answer key

Even balanced data can be graded wrong. If biased human decisions were the answer key, the model learns that bias as correct.

## Fight the trap

Spotting this trap is the hard part, because most of the time there’s nothing to spot. Every fact in a distorted answer can check out: nothing false to catch, nothing to fix. That’s why one question on your Evaluate the Results dig list isn’t a fact-check at all: ask it who’s missing. Fact-checks cover what’s on the page; this trap hides in what never made the page. So when an answer matters, anything about people, anything you’re about to act on, that one push is enough. Do it a few times and something better happens: you start spotting narrow answers on your own.

## Stale information

One more data trap, and it isn’t bias: even perfect data ages. Training stopped on a cut-off date, and the model has been answering from that snapshot ever since. Ask about anything newer, and it answers as if time never passed.

This isn’t a hallucination either. The model isn’t inventing. It’s remembering, and the memory is out of date. That’s what makes a stale claim dangerous: it was true, and it still sounds current. The fix: for anything that can change, check the date. The model often runs a live search on its own, but not every time, so when it matters, ask for the search yourself.

The model learned our shortcuts.

Including the ones we’d rather it didn’t.
