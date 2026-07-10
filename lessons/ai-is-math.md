## UNDERSTAND AI

# AI is Math

What’s the magic that powers ChatGPT, Claude, and every other AI you’ve used? **Math**. You met these ideas by name back in How an LLM Works. Now you’ll see how each one actually works.

## WHERE PROBABILITY MATH BEGAN

In 1654, two French mathematicians, Blaise Pascal and Pierre de Fermat, traded letters about gambling. That correspondence is where **standard probability** is usually dated from. The math was clean: if you can list all possible outcomes, you can calculate the chance of each one.

## STANDARD PROBABILITY

Take a simple example. If you toss a coin in the air, what’s the probability it lands on heads?

List Possible Outcomes

## Heads

H

## Tails

T

The Math

How do we calculate the probability the coin lands on HEADS? Here’s the formula.

Ways it happens (1)

Total outcomes (2)

=

Probability (50%)

Now make it a little harder. If you toss 2 coins in the air, what’s the probability that both land on heads?

List Possible Outcomes

## 1st Heads

## 2nd Heads

H

H

## 1st Heads

## 2nd Tails

H

T

## 1st Tails

## 2nd Heads

T

H

## 1st Tails

## 2nd Tails

T

T

The Math

How do we calculate the probability that both coins land on HEADS? Here’s the formula.

Ways it happens (1)

Total outcomes (4)

=

Probability (25%)

## CONDITIONAL PROBABILITY

Standard probability could count what you could see, like the coins, but it couldn’t tell you how much to change your mind when fresh evidence arrived. Thomas Bayes worked that part out. A minister, mathematician, and philosopher, he found the math for updating a belief as new evidence arrives, now known as Bayes’ Theorem.

Update With New Evidence

A moment ago, two coins gave you a 25% chance of both landing heads. Now someone peeks and tells you the **first coin landed on heads**. That new evidence rules out every outcome where the first coin was tails, so we cross those out and recount.

## 1st Heads

## 2nd Heads

H

H

## 1st Heads

## 2nd Tails

H

T

## 1st Tails

## 2nd Heads

T

H

## 1st Tails

## 2nd Tails

T

T

The Math

With the first coin known to be heads, only 2 outcomes are still possible. How likely is both HEADS now?

Ways it happens (1)

Total outcomes (2)

=

Probability (50%)

The evidence didn’t just rule things out, it moved the probability from **25%** to **50%**. That update is **conditional probability**.

## AUTOREGRESSIVE GENERATION

Remember your phone’s keyboard suggesting the next word? Autoregressive generation is that, but it doesn’t stop after one word. After AI picks a word, it uses that word to pick the next one. Then it uses both to pick the third. Every prediction depends on every word that came before it. Each new word is its own conditional-probability problem: given everything written so far, which word most likely comes next?

Tying the math together

The same rainy afternoon, **three different jobs**: estimate the chance of rain, sharpen it with a clue, then write the forecast one word at a time.

Standard Probability

Base rate from past years

40%

Over the last 100 years, it rained 40 times on May 21st.

Conditional Probability

Updated with a clue

60%

Rained 40 of the last 100 May 21sts.

+ NEW

Humidity is 90% right now.

Autoregressive Generation

Conditional probability on every word

one word at a time

It

→

is

→

going

→

to

→

?

## Picking the next word

rain

71%

pour

18%

stay

7%

No outside clue this time, the words it already wrote are the clue. Given “It is going to,” it picks the most probable next word, then feeds that back in and does it all over again.

The real math behind LLMs goes way past what’s here. Linear algebra moves the numbers. Calculus tunes the model during training. Plenty of other math is in there too. But two ideas from probability, plus the loop that turns them into language, are the foundation. Once you understand them, you understand the shape of how AI works. Everything else is engineering.
