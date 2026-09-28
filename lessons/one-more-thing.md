## UNDERSTAND AI

# One More Thing

Why can the same prompt produce a different answer? What makes AI’s answers more predictable or more varied? And how much math does one answer require?

## The Top Choice Doesn’t Always Win

You ask AI, “What should I name my new dog?” When AI reaches the name, it calculates a probability for every token in its vocabulary. Spot is the top choice at 22%, so you might expect AI to pick it every time.

But having the highest probability doesn’t guarantee selection.

A 22% probability means AI would pick Spot about 22 times out of 100 tries, on average, if the odds stay the same.

### Board 1: Same Probabilities, Different Choices

**Image file:** `one-more-thing-draws.jpg`

![Same Probabilities, Different Choices](one-more-thing-draws.jpg)

**Teaching content:**

Same probabilities, different choices.

The answer so far is “You could name him,” and the next token is still open.

Keep the probabilities unchanged across all five picks. Spot still has the highest probability at 22%.

Five random picks with these same probabilities produce: pick one, Max; pick two, Spot; pick three, Buddy; pick four, Rex; pick five, Max. The five picks are one possible set.

Spot was picked only once, even with the highest probability. Another five picks could turn out differently.

The best chance is not a guarantee.

## Why the Choices Matter

Two important points follow.

Choosing the most likely token every time can make answers repetitive. Giving other likely tokens a chance adds variety.

Each token AI chooses shapes what comes next, so one different choice can send the answer in a different direction.

## Temperature

So what changes how predictable those choices are?

Temperature reshapes the probabilities before AI picks each token.

In ChatGPT, Claude, and Gemini, it’s handled for you behind the scenes.

Low temperature favors the most likely choices. High temperature gives less likely choices a better chance.

Watch how the same starting probabilities change with temperature.

### Board 2: How Temperature Changes the Odds

**Image file:** `one-more-thing-temperature.jpg`

![How Temperature Changes the Odds](one-more-thing-temperature.jpg)

**Teaching content:**

Here is how temperature changes the odds.

The answer so far is still “You could name him,” with the next token open.

Start with the same odds as before. Spot has a 22% chance.

Low temperature concentrates the odds on the most likely choices. Spot’s chance goes from 22% to 36%.

High temperature spreads the odds and gives less likely choices a better chance. Spot’s chance falls from 22% to 16%.

Temperature changes how far ahead the top choice is.

Temperature reshapes the probabilities. It does not change what the model learned.

## The scale of the math

Every choice starts with calculations. Now count what an answer takes.

Training created the model’s weights, the numbers that shape every prediction.

When you use AI, those weights stay fixed.

For each new token, AI uses those weights in a massive set of calculations.

To picture the scale, imagine a model that uses one trillion weights for each token it produces. At roughly two calculations per weight, that would mean about two trillion calculations for one token.

### Board 3: The Math Adds Up Fast

**Image file:** `one-more-thing-bill.jpg`

![The Math Adds Up Fast](one-more-thing-bill.jpg)

**Teaching content:**

The math adds up fast.

Use the same example model: one trillion weights used for each new token, at roughly two calculations per weight.

One token, such as Spot, is one pass, one trip through our example model’s trillion weights. That is about 2 trillion calculations.

A short answer is about 100 tokens written by AI. One hundred tokens at 2 trillion each is about 200 trillion calculations.

A longer conversation is about 1,000 tokens written by AI across the conversation. One thousand tokens at 2 trillion each is about 2 quadrillion calculations.

These counts cover the tokens AI writes. They are estimates for an imagined model, not measurements of a real one.

Even a short answer takes trillions of calculations.

## Closing Message

Math and probability, one token at a time.

Every time you hit send.
