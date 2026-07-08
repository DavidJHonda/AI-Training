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

At each layer its numbers shift, as the model reads the surrounding words to work out what **IT** refers to.

→

What does this look like inside the model? Like this.

What happens inside each layer

Each layer refines every token’s vector, then hands it to the next layer.

## Layer 1

## Starting vector

[ 0.42, −1.15, 0.33, 2.08, −0.73, … ]

## Attention

Which words matter?

## Transformation

Update the meaning

## Richer vector out

[ 0.51, −0.87, 0.21, 1.91, −0.26, … ]

## Layer 2

## From layer 1

[ 0.51, −0.87, 0.21, 1.91, −0.26, … ]

## Attention

Which words matter?

## Transformation

Update the meaning

## Richer vector out

[ 0.27, −1.21, 0.67, 2.24, 0.14, … ]

## Layer 3

## From layer 2

[ 0.27, −1.21, 0.67, 2.24, 0.14, … ]

## Attention

Which words matter?

## Transformation

Update the meaning

## Richer vector out

[ 0.31, −0.92, 0.48, 1.74, −0.31, … ]

## Dozens more layers

## From layer 3

[ 0.31, −0.92, 0.48, 1.74, −0.31, … ]

## Attention

Which words matter?

## Transformation

Update the meaning

## Richer vector out

[ 0.19, −1.12, 0.72, 2.13, −0.03, … ]

**Same two moves at every layer.** Each pass, the numbers move closer to what the token means.

## Why are there dozens of layers?

Because some meaning is many steps deep. Simple meaning resolves in a few passes. But catching sarcasm, following a twist in a story, or reasoning through a complicated problem takes many more. A few layers reach only shallow meaning; stacking dozens leaves room for the deep kind.

Why not hundreds more? Past a point, extra depth stops helping and just makes the model more expensive to run.

## Neural networks

The whole stack of layers is called a **neural network**. The design is loosely borrowed from biology, simple units passing signals forward the way neurons do. But that’s where the resemblance ends. It isn’t a brain and it isn’t thinking: it’s the same arithmetic, repeated billions of times, fast.
