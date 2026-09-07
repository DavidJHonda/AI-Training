## UNDERSTAND AI

# Layers

Sometimes you need to read a sentence more than once before its meaning clicks. Try this one.

![The Horse Raced Past the Barn Fell. First read: it does not make sense and may seem to be missing a word. More reads test whether the barn fell or whether the horse raced past it afterward. Then the meaning clicks: The horse that was raced past the barn fell. The implied words “that was” are bolded to clarify the sentence. Each read updates the meaning until it clicks.](layers-horse-three-reads-editorial.jpg)

## AI Builds Meaning in Stages

AI splits your message into small pieces called **tokens**. Each token is represented by a row of numbers called a **vector**.

AI processes your message through a series of **layers**. Each layer updates the numbers that represent your tokens, then passes those updated numbers forward. And because language is full of nuance, many AI models use dozens of layers to build up meaning.

At each layer, **attention** and **transformation** work together to update the tokens’ numbers.

The whole stack of layers is called a **neural network**.

![How Every Layer Updates the Vector. A vector passes through many layers. At each layer, attention and transformation work together to update the token’s numbers. Two of the vector's many values are shown changing from the starting vector to the final vector.](layers-inside-layer-editorial.jpg)

## Following One Word Through the Layers

You saw this sentence in the Transformer lesson. Now follow one word, **IT**, as its numbers change from layer to layer.

![How “IT” Changes Through the Layers. IT begins as an ambiguous vector. Its numbers change through Layer 1, Layer 2, and more layers until IT resolves to CAT.](layers-3-resolves-it.jpg)

## Why are there dozens of layers?

Some meaning takes more steps to work out.

![A few layers settle plain meaning and dozens support nuance and reasoning. More layers require more computing power and time, so the extra benefit has to be worth the cost.](layers-3-why-dozens.jpg)

Meaning builds up, layer by layer.

Attention, then transformation. Dozens of times.
