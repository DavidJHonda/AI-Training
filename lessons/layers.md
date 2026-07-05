## UNDERSTAND AI

# Layers

Read the following sentence.

**The horse raced past the barn fell.**

- **First read:** it doesn’t make sense. Did someone forget a word?
- **Read it again:** wait, did a barn fall? Did the horse race past the barn afterward?
- **Read it a third time:** I think I got it now. There was a horse that ran past a barn. And, after running past the barn, the horse fell.
Each pass, your mind updates the meaning until it clicks.

AI does the same thing. It reads your message over and over again, establishing the meaning a little more with each pass. Each pass is called a **layer**, and the Transformer stacks dozens of them. At every layer, it runs the same two moves you just met: **attention** (which words matter) and **transformation** (update the meaning).

A token enters each layer as a vector. At the first layer, that vector is the starting meaning it picked up in Embeddings. Attention finds the words that matter to it, transformation updates the vector to fold that context in, and a richer vector comes out, ready for the next layer to refine.

## What a layer is made of

Attention and transformation are carried out by a **neural network**: the whole stack of layers, where each layer is a row of simple units called nodes. A node takes in numbers, multiplies them by its own adjustable numbers, adds up the result, and passes it forward to the next layer. Those adjustable numbers are the model’s **weights**.

The design is loosely borrowed from biology, nodes passing signals forward the way neurons do. But that’s where the resemblance ends. It isn’t a brain and it isn’t thinking: it’s the same arithmetic, repeated billions of times, fast.

## What do different layers do?

Engineers choose the architecture before training: how many layers, how wide each layer is, and how they connect. Training then learns the numbers inside those layers. Different layers often become useful for different kinds of patterns, but they aren’t cleanly labeled jobs like “grammar layer” or “reasoning layer.”

## Why are there dozens of layers?

Because some meaning is many steps deep. Simple meaning resolves in a few passes. But catching sarcasm, following a twist in a story, or reasoning through a complicated problem takes many more. A few layers reach only shallow meaning; stacking dozens leaves room for the deep kind.

There’s no perfect number, though. More depth adds capacity up to a point, and labs trade that against the cost of running it.
