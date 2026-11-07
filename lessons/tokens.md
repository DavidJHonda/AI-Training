## UNDERSTAND AI

# Tokens

Computers only process numbers.

That seems counterintuitive, because when you write an email, send a text, or type on your phone, you see words.

Behind the scenes, those words are converted to numbers so the computer can work with them.

The same applies to AI. How do your words become numbers that AI can work with? And how does its response turn back into words you can read?

## What Doesn’t Work

One idea is to assign each word in every language a unique number. That way, whatever word you type, AI gets a number.

But that breaks down fast. People keep inventing words, names, and slang. They also make typos and include things like emojis and code. Even a list of a million words couldn’t cover everything a person might type.

## Reusable Chunks of Text

Instead, AI uses reusable chunks of text called **tokens**. Think of them as building blocks for language.

### Board 1: What Tokens Look Like

**Image file:** `tokens-how-ai-splits-text.jpg`

![What Tokens Look Like](tokens-how-ai-splits-text.jpg)

**Teaching content:**

Here is what tokens look like.

Unbelievable becomes un, belie, and vable. One word, built from three chunks.

Unusual becomes un and usual. That is two tokens.

Unmatchable becomes un, match, and able. That is three tokens.

All three words reuse the same chunk, un.

Basketball becomes basket and ball. That is two tokens.

I ♥ AI becomes I, then a space with the heart, then a space with AI. That is three tokens. On the board, SP marks a leading space.

The web address shown on the board breaks into eight tokens. Even a web address breaks into chunks.

## Vocabulary and Token IDs

A token can be a whole word or just part of one. The full collection of tokens is called the model’s **vocabulary**.

When setting up AI, engineers run a program that analyzes a large collection of text to build the vocabulary. Each token gets a number, its **token ID**. Think of it as an address: it identifies the token, but says nothing about what it means.

### Board 2: You See a Word. AI Starts With a Number.

**Image file:** `tokens-cat-token-id.jpg`

![You See a Word. AI Starts With a Number.](tokens-cat-token-id.jpg)

**Teaching content:**

You see a word. AI starts with a number.

When you read the word cat, you know what it means: fur, whiskers, the animal.

For AI, it starts with a token ID. Here, the tokenizer converts the written word cat to ID 4719. The number identifies the token, not its meaning.

### Board 3: What Happens When You Hit Send

**Image file:** `tokens-how-tokenization-works.jpg`

![What Happens When You Hit Send](tokens-how-tokenization-works.jpg)

**Teaching content:**

Here is what happens when you hit send.

Step one, start with text: you type a question or message.

Step two, split into tokens: a program called a tokenizer breaks the text into reusable chunks.

Step three, look up token IDs: the tokenizer finds each chunk’s number in its vocabulary.

For unbelievable, the ID for un is 359, the ID for belie is 32898, and the ID for vable is 24694.

Tokenization turns text into token IDs the model can use.

## How the Answer Becomes Words Again

When AI replies, its answer comes out as token IDs. The tokenizer converts those IDs back into pieces of text and joins them together into the answer you read.

## Closing Message

Words become numbers.

That lets AI work with your language using math.
