## UNDERSTAND AI

# Transformer

When you type a message to ChatGPT, you use words, and it responds with words. Underneath, AI splits your text into small pieces called tokens. Each token has an embedding, a row of numbers that represents its starting meaning.

These two examples show how the surrounding words, or context, shape meaning. AI works with tokens, but we’ll use whole words to make the connections easier to see.

### Board 1: Two Problems Context Must Solve

**Image file:** `transformer-context-problems.jpg`

![Two Problems Context Must Solve](transformer-context-problems.jpg)

**Teaching content:**

There are two problems context must solve.

Problem 1 is different meanings. The same word can mean something different in each sentence.

“Please turn on the LIGHT.”

**LIGHT** means brightness

“The empty suitcase felt LIGHT.”

**LIGHT** means not heavy

What AI must figure out: When you use LIGHT in a sentence, how does AI know which meaning you mean?

The surrounding words provide the clues.

Problem 2 is pronouns. The same pronoun can point to a different thing in each sentence.

“The cat was thirsty, so IT drank the milk.”

**IT** means cat

“The milk was fresh, so the cat drank IT.”

**IT** means milk

What AI must figure out: When you use IT in a sentence, how does AI know what you’re referring to?

Again, the surrounding words provide the clues.

The surrounding words help AI figure out the meaning.

## Why this was hard for AI

The surrounding words give us the clues. The challenge for AI is keeping those clues connected.

Our human brains see the right meaning instantly from the surrounding words. For earlier AI, this was a challenge because it read text in order, one word at a time. In longer passages, it could lose track of the earlier words.

### Board 2: How Earlier AI Read Text

**Image file:** `transformer-before-transformers.jpg`

![How Earlier AI Read Text](transformer-before-transformers.jpg)

**Teaching content:**

This is how earlier AI read text.

The sentence is “The tired cat sat on the mat during the May rainstorm. IT soon fell asleep.”

The diagram follows the sentence from left to right, one word at a time, with an arrow from each word to the next.

Earlier AI often struggled to keep that connection, especially in longer passages.

## The breakthrough

That difficulty brings us to the Transformer.

In 2017, eight researchers at Google published a paper called Attention Is All You Need. It introduced the Transformer, a widely used architecture for large language models, and the “T” in ChatGPT.

The Transformer can process the tokens in your message at once.

In our example, **IT** can use information from the earlier word **CAT**, even with several words in between.

### Board 3: How A Transformer Reads

**Image file:** `transformer-how-transformer-reads.jpg`

![How A Transformer Reads](transformer-how-transformer-reads.jpg)

**Teaching content:**

This is how a Transformer reads.

The complete message arrives together. The same sentence, “The tired cat sat on the mat during the May rainstorm. IT soon fell asleep,” is laid out with every word visible at the same time. CAT and IT are highlighted.

IT can draw on CAT, even across several words.

## Only the start

There’s more to reading than taking in the words.

AI needs to figure out which words matter and use that information to update the numbers. In our example, IT needs information from CAT to help represent what it refers to in this sentence. Attention and transformation work together to make that happen.

### Board 4: How Context Changes the Numbers

**Image file:** `transformer-attention-transformation.jpg`

![How Context Changes the Numbers](transformer-attention-transformation.jpg)

**Teaching content:**

This is how context changes the numbers.

Attention weighs information from relevant words and blends it into the token’s numbers. On the board, an arrow curves from IT back to CAT. That connection is the information that matters here.

Transformation uses learned patterns to further process those numbers. On the board, two sets of number bars compare IT after attention with IT with context.

The surrounding words help AI update each token’s numbers.

## Return to the examples

Now let’s return to our two examples.

We’ve seen how the numbers change. Here is how the surrounding words help in each case.

### Board 5: How the Transformer Resolves Meaning

**Image file:** `transformer-resolves-meaning.jpg`

![How the Transformer Resolves Meaning](transformer-resolves-meaning.jpg)

**Teaching content:**

This is how the Transformer resolves meaning.

Problem 1 is different meanings.

“Please turn on the LIGHT.”

**LIGHT** means brightness.

“The empty suitcase felt LIGHT.”

**LIGHT** means not heavy.

Here is how the surrounding words help.

“Turn on” tells us **LIGHT** means brightness.

“Empty” helps us interpret **LIGHT** as not heavy.

Problem 2 is pronouns.

“The cat was thirsty, so IT drank the milk.”

**IT** means cat.

“The milk was fresh, so the cat drank IT.”

**IT** means milk.

Here is how the surrounding words help.

In the first sentence, **IT** points back to the thirsty **cat**.

In the second sentence, **IT** points back to the **milk** that the cat drank.

Attention and transformation help AI work out which meaning fits.

## Sarcasm and idioms

Attention and transformation also help AI interpret sarcasm and idioms.

## One catch: word order

So far, we’ve looked at which words help us interpret the message. There’s one more piece: where those words appear.

The words alone aren’t enough. Their order matters too.

Consider a simple sentence: “Dog bites man.” Same three tokens. Same starting embeddings. But the order carries the meaning.

### Board 6: How a Transformer Keeps Words in Order

**Image file:** `transformer-word-order.jpg`

![How a Transformer Keeps Words in Order](transformer-word-order.jpg)

**Teaching content:**

This is how a Transformer keeps words in order.

Compare DOG BITES MAN with MAN BITES DOG. The same three tokens can describe two different events.

Without position information: without positions, the model has the words but cannot tell which came first. On the board, BITES, DOG, and MAN float scattered, with question marks between them.

Position stamps preserve order: DOG is in position 1, BITES is in position 2, and MAN is in position 3. Positional encoding helps the model keep track of each token’s place.

Positional encoding tells the Transformer where every token belongs.

## Closing Message

Attention is all you need.

AI uses relationships between words to help interpret your message.
