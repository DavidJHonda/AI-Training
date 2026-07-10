## UNDERSTAND AI

# How AI Answers

In Vector Space, you watched a token’s final vector land in its neighborhood on the map. That landing was about meaning: the model understanding the words you put in. Now we move to the next step: how AI answers you.

The following statement is confusing right now. By the end of this lesson, it won’t be.

**AI predicts the next word based on what you already typed.**

Let’s take a simple question and watch AI build its answer.

You: “What should I name my new dog?”

First, the part you already know. The question makes the trip you’ve spent this section learning, and every step here is review.

What

should

I

name

my

new

dog

?

## Tokens

## Review · Tokens

The question splits into tokens, each mapped to its ID number. From here on, it’s all numbers.

→

## Position stamps

## Review · Transformer

Each token gets its position mixed in, #1 through #8, so the order arrives with the words.

→

## Starting meaning

## Review · Embeddings

Each token’s number becomes its vector: its starting position on the map.

→

## Through the layers

## Review · Layers · Vector Space

Dozens of passes of attention and transformation. The question’s meaning is locked in.

## The ranked list

The trip ends with a final vector: a position on the map that means the whole question. So how does that become an answer? Start with your phone. As you type a text, it suggests the next word: three chips above the keyboard, picked from the last word or two, the same for everyone.

See you ______.

soon

tomorrow

later

AI follows the same basic logic, but, as you might expect, it goes **way deeper**.

1. AI compares the final position of the last word in the chat so far against **every** possible next token (words or pieces of words), scoring each by how closely the two line up on the map.
2. Then it ranks them by probability: the best fit on top, and a long tail of less likely options below. It builds that list fresh every time, from everything in the chat and anything else in the context window, like personalization.
3. Then the model takes one, almost always from the top of the list, adds it to the text, and runs the whole thing again for the token after that.
Here’s that moment for the dog question. The model has started its reply, and the answer has just reached the name slot.

Score every token: the name slot

You could name him ______

Spot

22%

Max

17%

Buddy

14%

Rex

9%

Biscuit

6%

other tokens

32%

The exact numbers are illustrative.

The model takes the top of the list and types it: Spot. That move has a name: **prediction**. Score every possible next token, pick one.

Now reread the statement from the top of the lesson: AI predicts the next word based on what you already typed. You can sharpen it yourself now. The “word” is really a token. And “what you already typed” is really everything in the context window.

And notice where those odds come from. Attention spent dozens of layers blending the whole chat into that final position, so the scores really do come from everything the model can see. It’s why the context window mattered so much back in Work With AI: control the context, and you’re steering the predictions themselves.

One more thing before you try it yourself: Spot is one token. The answer isn’t finished, and the model doesn’t even remember the work it just did. What turns one pick into a whole reply is the next lesson.
