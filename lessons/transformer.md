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

Sentence 1: “Please turn on the LIGHT.” Here, LIGHT means brightness.

Sentence 2: “The suitcase is LIGHT enough to carry.” Here, LIGHT means not heavy.

The problem: which meaning should AI use?

Problem 2 is pronouns. The same pronoun can point to a different thing in each sentence.

Sentence 1: “The cat drank the milk because IT was thirsty.” Here, IT refers to the cat.

Sentence 2: “The cat drank the milk because IT was fresh.” Here, IT refers to the milk.

The problem: what does IT point to?

Context determines which meaning fits.

## Why this was hard for AI

Our human brains see the right meaning instantly from the surrounding words. For earlier AI, this was a challenge because it read text in order, one word at a time. In longer passages, it could lose track of the earlier words.

### Board 2: How Earlier AI Read Text

**Image file:** `transformer-before-transformers.jpg`

![How Earlier AI Read Text](transformer-before-transformers.jpg)

**Teaching content:**

This is how earlier AI read text.

The sentence is “The cat sat on the mat during the May rainstorm because it was tired.”

The diagram follows the sentence from left to right, one word at a time, with an arrow from each word to the next.

We know IT refers to CAT.

Earlier AI often struggled to keep that connection, especially in longer passages.

## The breakthrough

In 2017, eight researchers at Google published a paper called Attention Is All You Need. It introduced the Transformer, a widely used architecture for large language models, and the “T” in ChatGPT.

The Transformer reads your whole message at once.

In our example, IT can draw on information from the earlier word CAT, even with several words in between.

### Board 3: How a Transformer Reads a Sentence

**Image file:** `transformer-how-transformer-reads.jpg`

![How a Transformer Reads a Sentence](transformer-how-transformer-reads.jpg)

**Teaching content:**

This is how a Transformer reads a sentence.

The complete message arrives together. The same sentence, “The cat sat on the mat during the May rainstorm because it was tired,” is laid out with every word visible at the same time. CAT, IT, and TIRED are highlighted.

All words are present from the start.

Reading your whole message at once is only the start. AI needs to figure out which words matter and use that information to update the numbers. In our example, IT needs information from CAT to help represent what it refers to in this sentence. Attention and transformation work together to make that happen.

### Board 4: How Context Changes the Numbers

**Image file:** `transformer-attention-transformation.jpg`

![How Context Changes the Numbers](transformer-attention-transformation.jpg)

**Teaching content:**

This is how context changes the numbers.

Attention: weigh information from relevant words and blend it into the token’s numbers. On the board, an arrow curves from IT back to CAT. That connection is the information that matters here.

Transformation: use learned patterns to further process those numbers. On the board, two sets of number bars compare IT after attention with IT with context.

Both steps update the numbers that represent the token.

Attention and transformation work together to build meaning from context.

The model’s learned weights stay fixed.

What changes is the row of numbers representing each token in your message.

Now let’s return to our two examples.

### Board 5: How the Transformer Resolves Meaning

**Image file:** `transformer-resolves-meaning.jpg`

![How the Transformer Resolves Meaning](transformer-resolves-meaning.jpg)

**Teaching content:**

This is how the Transformer resolves meaning.

Problem 1, different meanings. Which words provide the clues? In “Please turn on the LIGHT,” the words “turn on” tell us LIGHT means brightness. In “The suitcase is LIGHT enough to carry,” the word “carry” tells us LIGHT means not heavy.

Problem 2, pronouns. Which words provide the clues? In “The cat drank the milk because IT was thirsty,” the word “thirsty” describes the cat, so IT refers to the cat. In “The cat drank the milk because IT was fresh,” the word “fresh” describes the milk, so IT refers to the milk.

Attention and transformation help AI work out which meaning fits.

Attention and transformation also help AI interpret sarcasm, idioms, and even an “it” that points to nothing at all, as in “it was a cold day.”

## One catch: word order

Reading everything at once creates a problem that reading in order never had. Consider a simple sentence: “Dog bites man.” Same three tokens. Same starting embeddings. But the order carries the meaning.

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
