## AVOID TRAPS

# Training Bias

Sometimes AI doesn’t invent anything. Every fact in an answer can be real, but the picture can still be distorted.

## Cows on the beach

### Board 1: Wrong Pattern. Wrong Answer.

**Course image (post-production only; not a Notebook upload):** `training-bias-wrong-pattern.jpg`

**Teaching content:**

Computer-vision researchers saw a famous version of this. A model could recognize cows in familiar photos. Then researchers showed it cows in unusual settings, including a beach, and its performance fell apart. Same animal. Different background.

Most of the cows it learned from appeared on green pasture. The model had picked up a shortcut: green grass means cow. It learned the background along with the animal.

**Takeaway:** A model can learn the background instead of the thing that matters.

**Scene (your own drawing, no board):**

This is training bias. The data showed the model a narrow slice of reality, so the model treated that slice as the whole picture.

Training data can create two different traps. It can be skewed, so AI sees a distorted picture. It can also be stale, so AI sees an old picture.

Skewed data creates three overlapping problems.

### Board 2: How Skewed Data Distorts the Picture

**Image file:** `training-bias-how-bias-happens.jpg`

![How Skewed Data Distorts the Picture](training-bias-how-bias-happens.jpg)

**Teaching content:**

1. **Defaults.** Common cases appear often, so the model treats them as the standard answer.
2. **Blind Spots.** Rare cases barely appear, so the model learns less about them.
3. **Wrong Patterns.** A clue works during training, so the model learns the clue instead of the concept.

**Takeaway:** The model repeats the shape of its data.

**Scene (your own drawing, no board):**

These patterns can have real consequences. Researchers have found major accuracy gaps across demographic groups in some facial-analysis systems. Face-recognition errors have even contributed to wrongful arrests. The stakes are much higher than a cow photo.

You cannot fact-check your way out of this trap because every individual fact may be correct. Look for sameness. **When every example looks alike, you are seeing the model’s default, not the world.** When you spot it, three questions can reveal what the first answer left out:

### Board 3: Three Questions That Reveal Bias

**Image file:** `training-bias-questions-to-ask.jpg`

![Three Questions That Reveal Bias](training-bias-questions-to-ask.jpg)

**Required spoken prompts — say each line exactly as written:**

1. **Ask What’s Missing.** “What’s missing from this answer?”
2. **Ask for Exceptions.** “Show me examples that don’t fit the pattern you just gave.”
3. **Remove the Famous.** “Answer again, leaving out the most famous examples.”

**Takeaway:** The model often has the rest of the picture. It just doesn’t lead with it.

## When Training Data Gets Old

Skewed data gives AI a distorted picture. Old data gives it an outdated one.

Training eventually stops. Anything that happens afterward was not part of that training, so it may be missing from the answer. AI can miss information that changed after training. Checking a current source helps you catch an outdated or incorrect answer.

We encountered a wrong answer about a current fact while building this course. We asked Claude to check an example sentence from the Tokens lesson.

This historical conversation shows why a current fact needs a current-source check. It does not establish why the first answer was wrong. Stale training is one possible explanation, but the conversation alone cannot distinguish stale information from hallucination or another error.

### Board 4: Stale Information in Real Life

**Image file:** `training-bias-stale.jpg`

![Stale Information in Real Life](training-bias-stale.jpg)

**Teaching content:**

You: What about “Cooper Flagg is an amazing basketball player for the Dallas Mavericks”?

AI: One flag: is Cooper Flagg actually on the Mavericks? I believe he was drafted by a different team. You should verify that.

You: Search the web and check the date. Was he the first pick in the 2025 NBA draft?

AI: Yes. Dallas selected Cooper Flagg with the first pick in 2025. My earlier answer relied on older information.

**Takeaway:** When the date matters, verify with a current source.

**Scene (your own drawing, no board):**

The conversation establishes two things: Claude questioned a correct fact, and it corrected the answer after checking a current source. Claude attributed its earlier answer to older information, but that self-explanation is not evidence of the root cause. When the date matters, verify the fact with a current source.

## When AI Looks Something Up

AI does not always have to answer from training alone. It can retrieve outside information first, add that information to its context, and then build an answer from it. Retrieval does not update the model’s training data or change its weights. The system places the retrieved material into the active context for this answer.

This approach is called Retrieval-Augmented Generation, or RAG:

### Board 5: How RAG Works

**Image file:** `training-bias-rag.jpg`

![How RAG Works](training-bias-rag.jpg)

**Teaching content:**

1. **Retrieve.** The system finds information connected to your question.
2. **Add to Context.** The retrieved material joins the information AI can use.
3. **Generate.** The model uses that material while it writes the answer.

**Takeaway:** RAG gives AI more to read. It does not guarantee truth.

RAG is especially useful when information changed after training. But it only gives AI more to read. It does not guarantee that the source is reliable or that AI interprets it correctly.

## Closing Message

AI repeats the shape of its data.

Ask what’s missing. Check what’s changed.
