## UNDERSTAND AI

# Layers

Read the following sentence.

The horse raced past the barn fell.

## First read

It doesn’t make sense. Did someone forget a word?

## Read it again

Wait, did a barn fall? Did the horse race past the barn afterward?

## Read it a third time

Got it. A horse ran past a barn. And after running past the barn, the horse fell.

Each pass, your mind updates the meaning until it clicks.

## AI does the same thing

It reads your message over and over, establishing the meaning a little more with each pass. And because language is full of nuance, it takes dozens of passes to pin the meaning down.

Each pass is called a **layer**, and at every layer AI runs the two moves you just met: **attention** (which words matter) and **transformation** (update the meaning).

And AI does it with math. At each layer, it adjusts the tokens’ numbers, each pass moving them a little closer to what the tokens mean.

## The mechanics

You saw this sentence in the Transformer lesson. Here’s how the numbers adjust for one word: **IT**. Notice the last box is blank. That box gets filled in the next lesson.

The

cat

sat

on

the

mat

during

the

May

rainstorm

because

it

was

tired

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

## A few passes

Simple meaning resolves early. The plain sense of a sentence is settled in a handful of passes.

## Dozens of passes

Catching sarcasm, following a twist in a story, or reasoning through a complicated problem takes many more.

## Why not hundreds?

Past a point, extra depth stops helping. It just makes the model more expensive to run.

A few layers reach only shallow meaning. Stacking dozens leaves room for the deep kind.

## Neural networks

The whole stack of layers is called a **neural network**. The design is loosely borrowed from biology, simple units passing signals forward the way neurons do. But that’s where the resemblance ends. It isn’t a brain and it isn’t thinking: it’s the same arithmetic, repeated billions of times, fast.

Meaning builds up, layer by layer.

Attention, then transformation. Dozens of times.
