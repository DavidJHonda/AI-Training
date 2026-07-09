## UNDERSTAND AI

# Inference

You’ve met every piece on its own: tokens, embeddings, layers, the context window, and the single prediction that picks one token. Now watch them work together as a single journey from your prompt to a finished answer.

Your prompt runs all the way through the model to make one prediction: a single token. Then it runs again for the next, and again, until the answer is complete. That whole repeating journey has a name: **Inference**.

It isn’t training again. It’s using what training already built, reading those frozen patterns back out one token at a time.

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

## The engine, running frozen

At the center of that whole journey is the neural network you met in Layers: the stacked nodes and **weights**. Training set those weights; inference just runs them forward, the same machine doing the same arithmetic every time you ask.

## LOCK IN THE PIECES

You’ve now watched every piece work together as one journey. Here’s a quick checkpoint to lock them in.
