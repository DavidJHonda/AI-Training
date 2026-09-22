## UNDERSTAND AI

# One More Thing

One more thing. Actually, three.

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

The probabilities for that next token are Spot at 22%, Max at 17%, Buddy at 14%, Rex at 9%, Biscuit at 6%, and all other tokens combined at 32%. These probabilities stay unchanged across all five tries.

Five separate tries with these same probabilities produce: try one, Max; try two, Spot; try three, Buddy; try four, Rex; try five, Max. The five tries are one possible set. Spot, the top choice, came up once in five tries.

The best chance is not a guarantee.

Two important points follow.

Choosing the most likely token every time can make answers repetitive. Giving other likely tokens a chance adds variety.

Each token AI chooses shapes what comes next, so one different choice can send the answer in a different direction.

## Temperature

Behind the scenes, the app uses a setting called temperature to reshape the probabilities before AI picks a token.

Low temperature makes the most likely choices even more likely. High temperature gives less likely choices a better chance.

Start with the same probabilities. Watch how they change with temperature.

### Board 2: How Temperature Changes the Odds

**Image file:** `one-more-thing-temperature.jpg`

![How Temperature Changes the Odds](one-more-thing-temperature.jpg)

**Teaching content:**

Here is how temperature changes the odds.

The answer so far is still “You could name him,” with the next token open.

For each name, the starting odds are the same as before: Spot 22%, Max 17%, Buddy 14%, Rex 9%, Biscuit 6%, and other tokens combined 32%.

At low temperature, Spot rises to 36%, Max to 21%, and Buddy to 15%. Rex drops to 6%, Biscuit to 3%, and other tokens combined to 19%. Low temperature concentrates the odds on the most likely choices. Spot’s chance goes from 22% to 36%.

At high temperature, Spot falls to 16%, Max to 14%, and Buddy to 13%. Rex rises to 10%, Biscuit to 8%, and other tokens combined to 39%. High temperature spreads the odds and gives less likely choices a better chance.

Temperature changes how far ahead the top choice is.

Temperature reshapes the probabilities. It does not change what the model learned.

## The scale of the math

Now count what an answer takes. Training created the model’s weights, the numbers that shape every prediction.

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

Not a mind. Math, at a scale nobody can picture.

Every time you hit send.
