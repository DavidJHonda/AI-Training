## UNDERSTAND AI

# The Math

Way back at the start of this section, in AI is Math, we made a claim and asked you to take it on faith: AI isn’t a mind, it’s math. Back then, you had no way to check. Now you do.

Over the last seven lessons, you built the machine yourself. Text becomes tokens. Tokens become vectors. Attention and the layers turn those vectors into meaning, and prediction reads the next word off a ranked list. In How AI Answers, you watched the machine write:

## Last token

## Reply so far

## Neighborhood

## Top predictions

?

____

Reply starters

You 18%

A 14%

Great 9%

You

You ____

Ways to suggest

could 24%

can 12%

should 10%

could

You could ____

Naming verbs

name 31%

call 19%

try 7%

name

You could name ____

Who gets named

him 45%

your 21%

the 8%

him

You could name him ____

Dog names

Spot 22%

Max 17%

Buddy 14%

✓

You could name him Spot.

You even gave the journey its name: inference. And everything you watched was arithmetic, start to finish. But there are a couple of things we didn’t tell you about that table.

## What we didn’t tell you #1: no memory

When the model typed “him”, it had already forgotten typing “name”. You remember the start of your own sentence while you write the end of it. The model doesn’t. The moment a token is picked, the work that picked it is thrown away. The only record is the text itself.

So “the reply so far” was the polite version. Before every word, the model re-reads everything it can see: your question, its own reply so far, and the rest of the context window too. Personalization, saved memory, everything earlier in the chat. All of it, tokenized, embedded, and pushed through every layer, for every single word.

Here’s the whole journey in one picture, from your prompt to a finished answer. **It runs in two phases, and the end feeds back to the start.**

## Phase 1

Read the message

One pass over everything you sent: your prompt, the history, all of it.

1

## CONTEXT WINDOW

What the model sees

Your prompt plus everything else in the window: past messages, AI responses, personalization, saved memory.

2

## TOKENS

Text becomes numbers

The whole thing is split into tokens, each mapped to a number. **From here on, it’s all numbers.**

3

## EMBEDDINGS

Starting meaning

Each token’s number becomes a vector, its starting meaning on the map.

4

## TRANSFORMER

## The core

Reads everything at once

The architecture that reads every token at once. Each of ~100 layers runs **attention** (which tokens relate), then **transformation** (what they mean together), using weights frozen in training. One final vector per token comes out.

→

## Read complete · now writing

One final vector per token. Everything you sent, understood.

## Phase 2

Write the reply

One token at a time, looping until the answer is complete.

5

## PROBABILITY

Score every possible next token

Now the model takes everything it just understood and scores all ~100,000 tokens it knows for what comes next. The better the fit, the higher the probability.

6

## PREDICTION

Pick the next token

It picks one token, usually a whole word.

7

## OUTPUT

Types it out

The chosen token is turned back into text (the reverse of tokenizing, using the same token-to-text table) and streamed into your reply. Whole words appear at once; longer words arrive as a few pieces that join up as they stream.

8

## LOOP

No memory, so it loops

The model doesn’t keep the work it just did; the only record is the text. It adds the new token to everything you sent and **runs the whole journey again**, token by token, until the answer is complete.

## no memory · the whole journey runs again

## What we didn’t tell you #2: the bill

Now count what that costs. The calculations aren’t a mystery. They’re the **weights** you met in Layers and Training, frozen since training day, multiplying the numbers that pass through them. Inference just runs them forward: the same machine, the same arithmetic, every time you ask.

So here’s the arithmetic on the arithmetic. A mid-size open model carries about 70 billion weights, and each token takes roughly two calculations per weight. That’s about 140 billion calculations before the model can type one word. (Frontier models are bigger. The companies don’t say how much bigger.)

## The bill

## Calculations

One word

Two calculations for each of 70 billion weights

140 billion

One sentence

“You could name him Spot.” is 7 tokens

≈ 1 trillion

One homework answer

A full reply runs about 300 tokens

≈ 42 trillion

Every calculation done fresh, nothing saved. And this is one question, from one student.

And remember secret #1: the whole window gets re-read for every word. The longer the chat, the more the model re-reads before each new word, so the meter climbs faster as a conversation grows. You already know the advice this explains: long chats get slow, and starting a fresh chat for a new task isn’t tidiness. It’s engineering.

## Every time you hit send

So here’s the picture to leave this section with. Every time you hit send, a warehouse of computers spins up, runs hundreds of billions of calculations for every word it types back, and throws the work away the moment the reply ends. Not a mind. Math, at a scale nobody can picture.

Somebody pays for all that arithmetic: in electricity, in water, and in money. We’ll count that bill later in the course, in The Hidden Cost.

## LOCK IN THE PIECES

You’ve now seen every piece, and what it costs to run them. One last checkpoint to lock the section in.
