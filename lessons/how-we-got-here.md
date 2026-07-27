## FINISH SMARTER

# How We Got Here

AI can feel like it appeared out of nowhere, fully formed, almost like magic. It didn’t. What looks like one sudden invention is really four older ideas, each worked out by different people who weren’t trying to build AI at all.

You already met those four ideas in How an LLM Works. Here’s how they come together: four separate breakthroughs that finally connected at the single moment everything changed.

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

None of them arrived together. Each was figured out decades, even centuries, apart, for reasons that had nothing to do with AI.

Four ideas, invented separately, that finally connected

🎲

Probability

1650s

Started as gambling math: a way to figure the odds. It lets a model answer with how likely something is, never a flat certainty.

## Pascal & Fermat

✍️

Prediction

1948

Treat language as guessing the next word from the words before it, the same idea behind your phone’s autocomplete.

## Claude Shannon, A Mathematical Theory of Communication

📚

Training

1957

The first machine that could learn patterns from examples instead of following hand-written instructions.

## Frank Rosenblatt, the perceptron

↓

🧩

Patterns

2017

Eight researchers at Google published one breakthrough that let a machine weigh all the words at once and find the patterns between them: the transformer, the spark that finally connected the other three.

## Vaswani and colleagues, Attention Is All You Need

1650s

Probability

1948

Prediction

1957

Training

2017

they connect

ChatGPT, Claude,

& Gemini

today

## The machine, end to end

And those four ideas didn’t just connect once. They run, in order, every time you hit send. Here’s the full journey your prompt takes through the machine this course taught you to read.

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

Now the model takes everything it just understood and scores all ~200,000 tokens it knows for what comes next. The better the fit, the higher the probability.

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

None of this was magic.

It was steps, stacked over time.
