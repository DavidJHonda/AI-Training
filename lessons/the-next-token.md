## UNDERSTAND AI

# The Next Token

AI builds an answer one token at a time. At each step, the model calculates probabilities for the tokens that could come next.

But AI doesn’t always pick the highest-probability token. To understand why, we’ll look at two things: **sampling** and **temperature**.

## Sampling

You ask AI, “What should I name my new dog?” When AI reaches the name, it calculates a probability for every token in its vocabulary. Spot is the top choice at 22%, so you might expect AI to pick it every time.

But having the highest probability doesn’t guarantee selection.

A 22% probability means AI would pick Spot about 22 times out of 100 tries, on average, if the odds stay the same.

That’s called sampling.

### Board 1: Same Probabilities, Different Choices

**Image file:** `the-next-token-draws.jpg`

![Same Probabilities, Different Choices](the-next-token-draws.jpg)

**Teaching content:**

Same probabilities, different choices.

The answer so far is “You could name him,” and the next token is still open.

Keep the probabilities unchanged across all five picks. Spot still has the highest probability at 22%.

Five random picks with these same probabilities produce: pick one, Max; pick two, Spot; pick three, Buddy; pick four, Rex; pick five, Max. The five picks are one possible set.

Spot was picked only once, even with the highest probability. Another five picks could turn out differently.

The best chance is not a guarantee.

## How One Choice Shapes the Answer

Choosing the most likely token every time can make answers repetitive. Giving other likely tokens a chance adds variety.

Each token AI chooses shapes what comes next, so one different choice can send the answer in a different direction.

## Temperature

Temperature changes how concentrated or spread out the probabilities are.

In chat apps, it’s already set for you behind the scenes.

Watch what different settings do to the dog-name choices.

### Board 2: How Temperature Changes the Odds

**Image file:** `the-next-token-temperature.jpg`

![How Temperature Changes the Odds](the-next-token-temperature.jpg)

**Teaching content:**

The answer so far is “You could name him,” and the next token is still open.

The model uses what it learned during training and the current context to calculate probabilities for the next token. In our example, Spot has the highest probability at 22%.

Watch what happens when we lower the temperature.

Lower temperature concentrates the odds on the most likely tokens. Spot’s chance rises from 22% to 36%. Less likely names get smaller chances.

Now see what higher temperature does to the same starting odds.

Higher temperature spreads the odds more widely. Spot’s chance falls from 22% to 16%, while less likely names get a better chance.

Compare Spot’s chance across all three settings.

Spot’s chance is 22% to start, 36% with lower temperature, and 16% with higher temperature.

Temperature reshapes the probabilities used to pick the next token. It doesn’t change what the model learned.

Illustrative probabilities. Other combines the rest of the vocabulary.

## Closing Message

The best chance isn’t a guarantee.

Different choices. Same learned weights.
