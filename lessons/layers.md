## UNDERSTAND AI

# Layers

Read the following sentence.

![The Horse Raced Past the Barn Fell. First pass: it does not make sense and may seem to be missing a word. More passes test whether the barn fell or whether the horse raced past it afterward. Then the meaning clicks: a horse ran past a barn, and after running past it, the horse fell. Each pass updates the meaning until it clicks.](layers-horse-three-reads-editorial.jpg)

## AI does the same thing

It reads your message over and over, establishing the meaning a little more with each pass. And because language is full of nuance, it takes dozens of passes to pin the meaning down.

Each pass is called a **layer**, and at every layer AI runs the two moves you just met: **attention** (which words matter) and **transformation** (update the meaning).

And AI does it with math. At each layer, it adjusts the tokens’ numbers, each pass moving them a little closer to what the tokens mean.

![How Every Layer Updates the Vector. A vector passes through many layers. Each layer applies attention to determine which words matter, then transformation to update the meaning. Two of the vector's many values are shown changing from the starting vector to the final vector.](layers-inside-layer-editorial.jpg)

## The mechanics

You saw this sentence in the Transformer lesson. Now follow one word, **IT**, as its numbers change from layer to layer.

![Three stages show how layers resolve IT: the starting vector is ambiguous, repeated attention and transformation shift its numbers, and the final vector lands closest to CAT.](layers-3-resolves-it.jpg)

## Why are there dozens of layers?

Because some meaning is many steps deep.

![A few layers settle plain meaning, dozens support nuance and reasoning, and eventually extra depth adds cost without much additional meaning.](layers-3-why-dozens.jpg)

## Neural networks

The whole stack of layers is called a **neural network**. The design is loosely borrowed from biology, simple units passing signals forward the way neurons do. But that’s where the resemblance ends. It isn’t a brain and it isn’t thinking: it’s the same arithmetic, repeated billions of times, fast.

Meaning builds up, layer by layer.

Attention, then transformation. Dozens of times.
