## UNDERSTAND AI

# Layers

Read the following sentence.

![The sentence The horse raced past the barn fell becomes clearer over multiple passes, moving from confusion to established meaning.](layers-1-three-reads.jpg)

## AI does the same thing

It reads your message over and over, establishing the meaning a little more with each pass. And because language is full of nuance, it takes dozens of passes to pin the meaning down.

Each pass is called a **layer**, and at every layer AI runs the two moves you just met: **attention** (which words matter) and **transformation** (update the meaning).

And AI does it with math. At each layer, it adjusts the tokens’ numbers, each pass moving them a little closer to what the tokens mean.

## The mechanics

You saw this sentence in the Transformer lesson. Now follow one word, **IT**, as its numbers change from layer to layer. The final box stays blank for now; we fill it in the next lesson.

![With Transformers, AI reads every word at once. Attention connects IT directly to CAT and TIRED, setting up the word we will follow through the layers.](transformer-2-now.jpg)

## Ambiguous “it”

On its own, **IT** is just a pronoun. Its vector could mean almost anything, and certainly not **CAT**.

→

## Through the layers

Each layer reads the surrounding words and shifts the numbers for **IT**. Layer by layer, the model works out what **IT** refers to.

→

What does this look like inside the model? Like this.

![Attention and transformation repeat through the model while the token vector changes after every layer, from its starting values to a richer output vector.](layers-2-inside.jpg)

## Why are there dozens of layers?

Because some meaning is many steps deep.

![A few layers settle plain meaning, dozens support nuance and reasoning, and eventually extra depth adds cost without much additional meaning.](layers-3-why-dozens.jpg)

## Neural networks

The whole stack of layers is called a **neural network**. The design is loosely borrowed from biology, simple units passing signals forward the way neurons do. But that’s where the resemblance ends. It isn’t a brain and it isn’t thinking: it’s the same arithmetic, repeated billions of times, fast.

Meaning builds up, layer by layer.

Attention, then transformation. Dozens of times.
