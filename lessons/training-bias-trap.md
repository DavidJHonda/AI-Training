## AVOID TRAPS

# Training Bias Trap

Sometimes AI doesn’t invent anything. Every fact in the answer is real, but the picture is still distorted.

That’s training bias. The model learns whatever patterns are in the data it saw. If the data is uneven, incomplete, or full of shortcuts, the model can treat a narrow slice of reality as the default.

Imagine the only driving advice online came from professional race car drivers. If you asked, “What’s the best way to drive?” the model might tell you to drive 180 miles per hour on a closed track.

That answer wouldn’t come from evil intent. It would come from a narrow slice of data treated like the whole picture.

## Cows on the beach

Computer-vision researchers hit a famous version of this. They had a model that could spot cows in photos with high accuracy. Then they showed it a cow on a beach, and it went blank. Same animal, same shape, same spots. No idea.

The training photos almost all showed cows on green pasture, so the model had quietly learned the wrong pattern: green grass means cow. It never learned the animal. It learned the background. Take away the grass, and the cows disappeared.

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

Biased labels

The labels come from past human decisions. If those decisions were biased, the model learns the bias.

## FIGHT THE TRAP

Three moves when the answer feels too clean.

Spotting the trap is half the work. Pushing back is the other half. When an AI answer feels suspiciously default, here are the moves to try.

🔍

Ask who’s missing.

The AI gives you what’s most documented. Push it to surface what isn’t.

Try: “Whose perspective isn’t in this answer?”

🔀

Ask for variation.

The default is rarely the full range. Asking for variety forces the model past the top of the distribution.

Try: “Give me examples from different backgrounds, regions, and time periods.”

🎯

Question the default.

“Typical” often means “most common in the data,” which isn’t the same as “normal in the world.”

Try: “When you say “typical,” what assumptions are you making?”

## Stale information

There’s one more way the data traps you, and it isn’t bias. Even perfect data ages. Training ended on a cut-off date, the weights froze, and the model has been answering from that snapshot ever since. Ask about anything that changed after the cut-off, and it answers as if time never passed.

Notice that this isn’t a hallucination either. The model isn’t inventing anything. It’s remembering, and the memory is out of date. That’s what makes a stale claim dangerous: it was true. It sounds current because nothing in the model’s voice marks it as old. The fix is simple: for anything that can change, check the date, or ask for a live web search. That live search is RAG from the Hallucination lesson, doing its second job: patching stale answers, not just invented ones.

The model learned our shortcuts.

Including the ones we’d rather it didn’t.
