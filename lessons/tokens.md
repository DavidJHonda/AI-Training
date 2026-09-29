## UNDERSTAND AI

# Tokens

Math is the magic that powers AI.

But you ask AI questions in words, not numbers.

### Board 1: You Use Words. AI Uses Numbers.

**Image file:** `tokens-using-ai-feels-like.jpg`

![You Use Words. AI Uses Numbers.](tokens-using-ai-feels-like.jpg)

**Teaching content:**

You use words. AI uses numbers.

You ask: “What’s the best Avengers movie?”

AI answers: “Most people point to Avengers: Endgame. It’s the big payoff to a decade of films, and it broke box-office records. Infinity War is the other top pick if you like a darker ending.”

You ask in words, and the answer comes back in words.

## How Your Words Become Numbers

How do your words become numbers that AI can use?

One idea is to assign each word in every language a unique number. That way, you type the word, AI gets a number.

But that breaks down fast. People keep inventing words, names, and slang. They also make typos and include things like emojis and code. Even a list of a million words couldn’t cover everything a person might type.

## Words Into Pieces

Instead of giving every word its own number, AI uses reusable pieces of text called tokens.

Think of them as building blocks for language.

A token can be a whole word or just part of one.

The full collection of tokens is called the model’s vocabulary. The same pieces can combine in different ways, so the vocabulary doesn’t need a new entry for every new word. For example, un can be reused in unbelievable and unusual.

### Board 2: Building Blocks for Language

**Image file:** `tokens-building-blocks-faceless.jpg`

![Building Blocks for Language](tokens-building-blocks-faceless.jpg)

**Teaching content:**

Tokens are building blocks for language.

The text unbelievable goes in, and three tokens come out: un, belie, and vable. One word, built from three pieces.

The same piece shows up in different words. The piece un starts unbelievable, unmatchable, and unusual. The letters after un may be split into more than one token. The vocabulary reuses the piece un instead of storing a separate entry for every whole word that starts with it.

Reuse the pieces. Build more words.

## Where the Pieces Come From

When setting up AI, engineers choose how text will be split into tokens and how large the vocabulary will be. A program analyzes a large collection of text to build that vocabulary. Each token gets a number, its token ID. Think of it as an address in the vocabulary: it identifies the token, but says nothing about what it means.

The model uses those same tokens and IDs during training and when you chat.

These vocabularies can be large: ChatGPT’s holds about 200,000 tokens and Gemini’s about 256,000. Anthropic hasn’t published Claude’s.

### Board 3: What Happens When You Hit Send

**Image file:** `tokens-how-tokenization-works.jpg`

![What Happens When You Hit Send](tokens-how-tokenization-works.jpg)

**Teaching content:**

Here is what happens when you hit send.

Step one, start with text: you type a question or message.

Step two, split into tokens: a program called a tokenizer breaks the text into reusable chunks.

Step three, look up token IDs: the tokenizer finds each chunk’s number in its vocabulary.

For the word unbelievable, the tokenizer in this example, called cl100k_base, produces three chunks with three IDs. The ID for un is 359, the ID for belie is 32898, and the ID for vable is 24694.

Tokenization turns text into token IDs the model can use.

### Board 4: Humans See a Cat. AI Starts With a Token ID.

**Image file:** `tokens-cat-token-id.jpg`

![Humans See a Cat. AI Starts With a Token ID.](tokens-cat-token-id.jpg)

**Teaching content:**

Humans see a cat. AI starts with a token ID.

For you, it is instant understanding. You know what cat means: fur, whiskers, the animal.

For AI, it starts with a token ID. Here, the tokenizer converts the written word cat to ID 4719. The number identifies the token, not its meaning.

A token ID identifies the token. Meaning comes later.

## All the Text You Send

All the text you send to AI gets split into tokens. Here are some examples.

### Board 5: How AI Splits Text Into Tokens

**Image file:** `tokens-how-ai-splits-text.jpg`

![How AI Splits Text Into Tokens](tokens-how-ai-splits-text.jpg)

**Teaching content:**

Here is how AI splits text into tokens.

These examples use the cl100k_base tokenizer. The numbers below the chunks on the board are token IDs.

Example two: basketball becomes basket and ball. That is two tokens.

Example four: I ♥ AI becomes I, then a space with the heart, then a space with AI. That is three tokens. On the board, SP marks a leading space.

Example five: the web address shown on the board breaks into eight tokens. Even a web address breaks into chunks.

## How the Answer Becomes Words Again

When AI replies, its answer comes out as token IDs. The tokenizer converts those IDs back into pieces of text and joins them together into the answer you read.

## Closing Message

Words become numbers.

That lets AI work with your language using math.
