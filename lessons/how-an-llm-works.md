## START SMARTER

# How an LLM Works

If you’ve used AI, you’ve probably used an app like ChatGPT, Claude, or Gemini. The app is what you use. Under the hood, a Large Language Model, or LLM for short, does the work.

### Board 1: What’s an LLM?

**Image file:** `how-an-llm-works-llm.jpg`

![What’s an LLM?](how-an-llm-works-llm.jpg)

**Teaching content:**

Large: trained on huge amounts of text and code. Language: it reads, writes, summarizes, translates, and explains. Model: it predicts likely output from learned patterns. ChatGPT is the app. The LLM is the engine.

So how does an LLM actually turn your words into an answer?

When ChatGPT or Claude write a sentence, they’re running math to predict the likely next words. They aren’t looking up what your words mean; they’re working out which words tend to follow which.

Before you use it, the model learns patterns during training. When you ask a question, it uses those patterns to build an answer, one word at a time.

Let’s follow one example, peanut butter, to see how the model learns a pattern and uses it to build an answer.

## TRAINING

First, the model needs to learn. That happens during training. It guesses the next word, checks the example, and adjusts its internal numbers to make the right word more likely.

### Board 2: How Training Works

**Image file:** `how-an-llm-works-training.jpg`

![How Training Works](how-an-llm-works-training.jpg)

**Teaching content:**

Four steps that repeat. Read: the model reads a training example with the answer included. Guess: given “Peanut butter and blank,” the model guesses cloud. Check: the example says jelly. Compare the guess with that word. Adjust: adjust the model’s internal numbers to make jelly more likely in this situation. Then the next example.

Repeat with more examples. The patterns build.

## PATTERNS

What does the model learn during training? Patterns. Here’s one you picked up as a child. Which word comes next?

### Board 3: How AI Learns Patterns

**Image file:** `how-an-llm-works-patterns.jpg`

![How AI Learns Patterns](how-an-llm-works-patterns.jpg)

**Teaching content:**

One familiar pattern: peanut butter and blank leads to jelly. You knew it. So does AI.

Patterns are everywhere: twinkle, twinkle, little blank leads to star. Once upon a blank leads to time. Better late than blank leads to never.

AI learns patterns by working through billions of examples.

These are easy patterns you already know. AI also learns patterns in places you might not expect: how people explain ideas, ask questions, solve problems, and even misspell words.

## PROBABILITY

Now the model uses those patterns to build your answer. It starts by working out how likely each possible next word is. Those probabilities change with the surrounding text.

### Board 4: Same Word. Different Odds.

**Image file:** `how-an-llm-works-same-word-different-odds.jpg`

![Same Word. Different Odds.](how-an-llm-works-same-word-different-odds.jpg)

**Teaching content:**

Same word, different odds. For “I’d like to buy peanut butter and blank,” the model scores jelly at 41 percent, bread at 27 percent, bananas at 16 percent, and honey at 5 percent. For “I’d like to buy a peanut butter and banana blank,” it scores sandwich at 54 percent, smoothie at 16 percent, toast at 9 percent, and jelly at only 2 percent.

The surrounding words change the odds. In this example, adding “banana” drops the probability of “jelly” from 41 percent to 2 percent.

## PREDICTION

Those probabilities guide its choice of the next word. It adds that word, then repeats the process. Your phone does something similar when you write a text: it suggests a word, you tap it, and it suggests the next.

### Board 5: One Word at a Time

**Image file:** `how-an-llm-works-one-word-at-a-time.jpg`

![One Word at a Time](how-an-llm-works-one-word-at-a-time.jpg)

**Teaching content:**

One word at a time. “I want to buy peanut butter and” leads to jelly. “I want to buy peanut butter and jelly” leads to for. “I want to buy peanut butter and jelly for” leads to lunch. Add a word. Use the updated sentence. Predict again.

A full paragraph runs this loop many times, fast enough to look like thought.

### Close

**Image file:** `how-an-llm-works-close.jpg`

![Close board](how-an-llm-works-close.jpg)

## Closing Message

Training builds the patterns.

The model uses those patterns to build your answer, one word at a time.
