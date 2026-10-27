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

This is training bias.

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

Stale data is a separate limitation: information that was accurate during training may no longer be current. When the date matters, verify with a current source.

## Closing Message

AI repeats the shape of its data.

Ask what’s missing. Check what’s changed.
