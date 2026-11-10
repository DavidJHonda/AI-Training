## UNDERSTAND AI

# Why Answers Vary

You ask AI, “What should I name my new dog?” It suggests Spot. You start a new chat and ask the exact same question. This time, it suggests Max.

Why did the same question get a different answer?

### Board 1: Why Answers Vary

**Image file:** `why-answers-vary-overview.jpg`

![Why Answers Vary](why-answers-vary-overview.jpg)

**Teaching content:**

Here are reasons why answers vary.

Model & Thinking: The model you use and how much thinking it does can change the answer.

What AI Receives: Your prompt and the other information available to AI can change its answer.

AI’s Choices: Behind the scenes, AI uses techniques that give different tokens a chance to be selected.

Two techniques help explain AI’s choices: **sampling** and **temperature**.

## Sampling

When AI reaches the dog’s name, it calculates a probability for every token in its vocabulary. In our example, Spot is the top choice at 22%, so you might expect AI to pick it every time.

But it doesn’t.

A 22% probability means AI would pick Spot about 22 times out of 100 tries, on average, if the odds stay the same.

That’s called **sampling**.

### Board 2: Same Probabilities, Different Choices

**Image file:** `why-answers-vary-draws.jpg`

![Same Probabilities, Different Choices](why-answers-vary-draws.jpg)

**Teaching content:**

Same probabilities, different choices.

The answer so far is “You could name him,” and the next token is still open.

Keep the probabilities unchanged across all five picks. Spot still has the highest probability at 22%.

Five random picks with these same probabilities produce: pick one, Max; pick two, Spot; pick three, Buddy; pick four, Rex; pick five, Max.

Spot was picked only once, even with the highest probability. Another five picks could turn out differently.

## Why does AI work this way?

Choosing the most likely token every time can make answers repetitive. Giving other likely tokens a chance adds variety and can make answers more creative.

Choosing a different token shapes what comes next and can send the answer in a different direction.

## Temperature

Sampling selects a token using probabilities.

Temperature adjusts those probabilities.

In ChatGPT, Gemini, and Claude, temperature is set for you behind the scenes.

Compare how different temperature settings change the probabilities for each dog name.

### Board 3: How Temperature Changes the Odds

**Image file:** `why-answers-vary-temperature.jpg`

![How Temperature Changes the Odds](why-answers-vary-temperature.jpg)

**Teaching content:**

The answer so far is “You could name him,” and the next token is still open.

Low Temperature: Concentrates the odds.

Starting Odds: From training and context.

High Temperature: Spreads the odds.

| Token | Low Temperature | Starting Odds | High Temperature |
| --- | --- | --- | --- |
| Spot | 36% | 22% | 16% |
| Max | 21% | 17% | 14% |
| Buddy | 15% | 14% | 13% |
| Rex | 6% | 9% | 10% |
| Biscuit | 3% | 6% | 8% |
| All other tokens | 19% | 32% | 39% |

Spot leads at 22%. At low temperature, its chance rises to 36%. At high temperature, its chance falls to 16%. Lower temperature concentrates more probability on the leading choices. Higher temperature spreads it more widely. Both settings change the same starting odds.

Spot remains the most likely individual token at all three settings. Temperature changes its probability.

## Closing Message

AI answers vary.

Different inputs. Different odds. Different choices.
