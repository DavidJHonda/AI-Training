## UNDERSTAND AI

# Layers

Have you ever read a passage in English class that only made sense after a few reads? Try the sentence below. You might need to read it more than once before the meaning clicks.

### Board 1: “The Horse Raced Past the Barn Fell”

**Image file:** `layers-horse-three-reads.jpg`

![“The Horse Raced Past the Barn Fell”](layers-horse-three-reads.jpg)

**Teaching content:**

The sentence is “The horse raced past the barn fell.”

First read: it doesn’t make sense. Did someone forget a word? You reach “fell” and the sentence seems to stop short. The horse raced past the barn … fell?

More reads: wait, did a barn fall? Did the horse race past the barn afterward? You try each possibility against the words. “Fell” could go with the barn, or with the horse.

Meaning clicks: someone raced a horse past a barn. Then the horse fell. “Raced” describes the horse, and “fell” is what the horse did. The horse passes the barn, then the horse falls.

Each read updates the meaning until it clicks.

## AI Does Something Similar

AI doesn’t read your message the way you do.

It processes your text through a series of layers. Within each layer, attention and transformation work together to update the numbers, helping AI work out what your words mean together. Those updated numbers pass to the next layer. Like rereading a difficult sentence, the process builds on what came before.

The whole stack of layers is called a neural network.

### Board 2: How Layers Update the Numbers

**Image file:** `layers-inside-layer.jpg`

![How Layers Update the Numbers](layers-inside-layer.jpg)

**Teaching content:**

This is how layers update the numbers.

Numbers go in on one side and final numbers come out the other. In between stands a long line of layers, one after another. Inside every layer are the same two steps, attention and transformation. Each layer takes the numbers it receives, updates them, and passes the updated numbers to the next layer.

Each row contains many numbers. Two are shown here.

The starting numbers for those two positions are .42 and −1.15. After one layer they are .51 and −.87. After many layers they are .27 and −1.21. The final numbers are .19 and −1.12. The values shift at every layer, so the numbers that come out are not the numbers that went in.

Attention and transformation update the numbers at each layer.

## Following One Word Through the Layers

Now follow one word, IT, as its numbers change from layer to layer.

### Board 3: How AI Connects ‘IT’ to ‘CAT’

**Image file:** `layers-resolves-it.jpg`

![How AI Connects ‘IT’ to ‘CAT’](layers-resolves-it.jpg)

**Teaching content:**

This is how AI connects IT to CAT.

The sentence is “The CAT sat on the mat during the May rainstorm because IT was tired.”

Start: IT could refer to different things. The starting numbers don’t tell us which one. Two of IT’s starting numbers are .12 and −.34.

Layer 1: the numbers begin to capture IT’s connection to CAT. The two numbers are now .18 and −.22.

Layer 2: the updated numbers carry more information about that connection. The two numbers are now .25 and −.09.

Repeat: the row continues through more layers. Each layer builds on the previous layer’s numbers.

Result: the two numbers finish at .41 and .06.

AI works out that IT refers to CAT.

## How Many Layers Are There?

AI companies don’t always share how many layers their models use. But published designs give us an idea of the scale: dozens of layers, and sometimes more than a hundred.

The horse sentence took a few reads to untangle. Sarcasm, story twists, and complicated reasoning can take even more work. AI’s layers give it more steps to work through those relationships and build meaning.

Why not keep adding layers? More layers require more computing power and time.

The extra benefit has to be worth the cost.

## Closing Message

Meaning builds up, layer by layer.

Attention and transformation. Dozens of times.
