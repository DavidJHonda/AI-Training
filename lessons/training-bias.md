## AVOID TRAPS

# Training Bias

Sometimes AI doesn’t invent anything. Every fact in an answer can be real, but the picture can still be distorted.

## Cows on the beach

Computer-vision researchers saw a famous version of this. A model could recognize cows in familiar photos. Then researchers showed it cows in unusual settings, including a beach, and its performance fell apart. Same animal. Different background.

Most of the cows it learned from appeared on green pasture. The model had picked up a shortcut: green grass means cow. It learned the background along with the animal.

This is training bias. The data showed the model a narrow slice of reality, so the model treated that slice as the whole picture.

Training data can create two different traps. It can be skewed, so AI sees a distorted picture. It can also be stale, so AI sees an old picture.

Skewed data creates three overlapping problems.

### How Skewed Data Distorts the Picture

**Defaults** Some cases appear too often in the data. The model treats them as the default.

**Blind Spots** Some cases appear too rarely. The model performs worse when those cases come up.

**Wrong Patterns** A wrong clue happens to work in training. The model learns the clue instead of the real concept.

The model repeats the shape of its data.

These patterns can have real consequences. Researchers have found major accuracy gaps across demographic groups in some facial-analysis systems. Face-recognition errors have even contributed to wrongful arrests. The stakes are much higher than a cow photo.

You cannot fact-check your way out of this trap because every individual fact may be correct. Look for sameness. **When every example looks alike, you are seeing the model’s default, not the world.** When you spot it, three questions can reveal what the first answer left out:

### Three Questions That Reveal Bias

1. What’s missing from this answer?
2. Show me examples that don’t fit the pattern you just gave.
3. Answer again, leaving out the most famous examples.

The model often has more of the picture. It just doesn’t lead with it.

## When Training Data Gets Old

Skewed data gives AI a distorted picture. Old data gives it an outdated one.

Training eventually stops. Anything that happens afterward was not part of its training, so it may be missing from the answer. This is a different training-data problem. It is stale information, not a hallucination.

We encountered it while building this course. We asked Claude to check an example sentence from the Tokens lesson:

### Stale Information in Real Life

**You:** What about ‘Cooper Flagg is an amazing basketball player for the Dallas Mavericks’?

**Claude:** One flag though: is Cooper Flagg actually on the Mavericks? I believe he was drafted by a different team. You’d want to verify that before committing it to the course.

**You:** Search the web and check the date. Was he the first pick in the 2025 NBA draft?

**Claude:** Yes. Cooper Flagg was selected first overall by the Dallas Mavericks in the 2025 NBA draft. My earlier doubt came from stale information.

Claude answered from older information without searching first. Once we asked it to check a current source, it corrected itself. When the date matters, that is your move too.

## When AI Looks Something Up

AI does not always have to answer from training alone. It can retrieve outside information first, add that information to its context, and then build an answer from it.

This approach is called Retrieval-Augmented Generation, or RAG:

### How RAG Works

1. **Retrieve.** The system finds information connected to your question.
2. **Add to Context.** The retrieved material joins the information AI can use.
3. **Generate.** The model uses that material while it writes the answer.

RAG gives AI more to read. It does not guarantee truth.

RAG is especially useful when information changed after training. But it only gives AI more to read. It does not guarantee that the source is reliable or that AI interprets it correctly.

AI repeats the shape of its data.

Ask what’s missing. Check what’s changed.
