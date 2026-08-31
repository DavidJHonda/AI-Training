## UNDERSTAND AI

# AI is Math

What’s the magic that powers ChatGPT, Claude, and every other AI you’ve used? **Math**. You met these ideas by name back in How an LLM Works. Now you’ll see how each one actually works.

## WHERE PROBABILITY MATH BEGAN

In 1654, two French mathematicians, Blaise Pascal and Pierre de Fermat, traded letters about gambling. That correspondence is where **standard probability** is usually dated from. The math was clean: list every possible outcome, confirm they’re equally likely, and you can calculate the chance of each one.

![The probability formula: ways an outcome happens divided by total possible outcomes equals probability.](ai-is-math-the-math-editorial.jpg)

![Toss a coin. The chance it lands on heads is one favorable outcome out of two, or 50 percent.](ai-is-math-one-coin-editorial.jpg)

![Toss two coins. The chance that both land on heads is one favorable outcome out of four, or 25 percent.](ai-is-math-two-coins-editorial.jpg)

## CONDITIONAL PROBABILITY

Standard probability could count what you could see, like the coins, but it couldn’t tell you how much to change your mind when fresh evidence arrived. Thomas Bayes worked that part out. A minister, mathematician, and philosopher, he found the math for updating a belief as new evidence arrives, now known as Bayes’ Theorem.

Now someone peeks at the first coin and tells you it landed heads. That new evidence rules out every outcome where the first coin is tails.

![New evidence says the first coin landed on heads. Two outcomes are ruled out, so the probability both coins landed on heads becomes one out of two, or 50 percent.](ai-is-math-conditional-probability-editorial.jpg)

The evidence didn’t just rule things out, it moved the probability that both coins are heads from **25%** to **50%**. That update is **conditional probability**.

## AUTOREGRESSIVE GENERATION

Remember your phone’s keyboard suggesting the next word? Autoregressive generation is that, but it doesn’t stop after one word. After AI picks a word, it uses that word to pick the next one. Then it uses both to pick the third. Every prediction depends on every word that came before it. Each new word is its own conditional-probability problem: given everything written so far, which word most likely comes next?

![What is the chance of rain? Standard probability starts with 40 rainy May 21sts out of 100. Current humidity updates the chance to 60 percent. The words It is going to become evidence for the next word, with rain at 71 percent.](ai-is-math-chance-rain-editorial.jpg)

No outside clue this time, the words it already wrote are the clue. Given “It is going to,” it picks the most probable next word, then feeds that back in and does it all over again.

![From base rate to next word: Luke and Nate trace a rain prediction from the historical base rate, through a new humidity clue, to the model’s next-word choice.](ai-is-math-base-rate-teaching-editorial.jpg)

The real math behind LLMs goes way past what’s here. Linear algebra moves the numbers. Calculus tunes the model during training. Plenty of other math is in there too. But two ideas from probability, plus the loop that turns them into language, are the foundation. Once you understand them, you understand the shape of how AI works. Everything else is engineering.

A chance. A clue. One word at a time.

Everything else is engineering.
