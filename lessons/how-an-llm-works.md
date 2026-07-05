## START SMARTER

# How an LLM Works

You’ve met the two kinds of AI and named the generative one: a Large Language Model, or LLM. So how does an LLM actually turn your words into an answer?

When ChatGPT or Claude write a sentence, they're running math to predict the likely next words. They aren't looking up what your words mean; they're working out which words tend to follow which.

How do they do it? In two phases. First the model learns, once, by soaking up patterns from mountains of text. Then, every time you chat, it uses those patterns to build your answer one word at a time.

## Learn once

🌱 Training

↓

🍀 Patterns

→

patterns power every answer

Answer· every word

🎲 Probability

↓

✍️ Prediction

Four ideas carry it. Below, we follow one example, peanut butter, through all four.

01

🌱

Training

## Learn once

The model **teaches itself**: guess the next word, check, and nudge its numbers toward the right word.

## 1 · Reads

📖 books

🌐 web

💬 chats

💻 code

more than you could read in 1,000 lifetimes

→

## 2 · Guesses

Peanut butter and __

cloud

✗

wrong → nudge the internal numbers

→

## 3 · Corrects

Peanut butter and __

jelly

✓

a little more accurate every pass

Repeat that loop billions of times, and that's training.

02

🍀

Patterns

## Learn once

So what is it actually learning? **Patterns**. Here's one you picked up as a child. Which word comes next?

Peanut butter and

→

jelly

you knew it, so does AI

## Patterns are everywhere

Twinkle, twinkle, little __

→

star

Once upon a __

→

time

Better late than __

→

never

AI didn’t memorize these. It absorbed the pattern by running through billions of examples.

03

🎲

Probability

## Every word

AI doesn't make one guess. It scores **every** possible next word: a ranked list with a probability on each, and those numbers shift with the surrounding text.

## Same word, different odds

I'd like to buy peanut butter and _____.

jelly

41%

bread

27%

bananas

16%

honey

5%

I'd like to buy a peanut butter and banana _____.

sandwich

54%

smoothie

16%

toast

9%

jelly

2%

Add the word banana, and jelly’s probability drops from 41% to 2%. The word banana changed everything.

04

✍️

Prediction

## Every word

Probability handled one word. But your answer is hundreds of words long, so the model just repeats the move. Your phone does this when you write a text: it suggests a word, you tap it, it suggests the next. AI works the same way, with no fixed plan for where the sentence will end up. One word, look again, the next.

1

I want to buy peanut butter and

+

jelly

2

I want to buy peanut butter and jelly

+

for

3

I want to buy peanut butter and jelly for

+

lunch

A full paragraph runs this loop many times, fast enough to look like thought.

That clears up three big myths:

- AI isn’t **magic**: it’s math working out probabilities.
- It isn’t **a person**: no thoughts, no understanding, even when it sounds like it has both.
- It isn’t **a truth machine**: it predicts what sounds likely, so a wrong answer can sound just as confident as a right one.
Keep those three straight and much of the confusion falls away.
