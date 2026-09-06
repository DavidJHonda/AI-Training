## UNDERSTAND AI

# Tokens

**Math is the magic that powers AI.** But you ask AI questions in words, not numbers.

![You Use Words. AI Uses Numbers. You ask what the best Avengers movie is, and AI answers in natural language with Avengers Endgame and Infinity War as the leading choices.](tokens-using-ai-feels-like-editorial.jpg)

How do your words become numbers that AI can use?

One idea is to assign each word in every language a unique number. That way, you type the word, AI gets a number.

But that breaks down fast. People keep inventing words, names, and slang. They also make typos and include things like emojis and code. Even a list of a million words couldn’t cover everything a person might type.

## WORDS INTO PIECES

Instead of giving every word its own number, AI uses reusable pieces of text called **tokens**. Think of them as building blocks for language. A token can be a whole word or just part of one. The full collection of tokens is called the model’s **vocabulary**. The same pieces can combine in different ways, so the vocabulary doesn’t need a new entry for every new word. For example, **un** can be reused in **unbelievable** and **unusual**.

![Building Blocks for Language. Luke and Nate feed the written word unbelievable into a brass tokenizer, which produces un, belie, and vable tiles. Below, the same green un piece is highlighted in unbelievable, unmatchable, and unusual; the remaining letters are unboxed and may span multiple tokens. Reuse the pieces. Build more words.](tokens-building-blocks-editorial.jpg)

## WHERE THE PIECES COME FROM

When setting up AI, engineers choose how text will be split into tokens and how large the vocabulary will be. A program analyzes a large collection of text to build that vocabulary. Each token gets a number, its **token ID**. Think of it as an address in the vocabulary: it identifies the token, but says nothing about what it means. The model uses those same tokens and IDs during training and when you chat.

These vocabularies can be large: ChatGPT’s holds about **200,000** tokens and Gemini’s about **256,000**. Anthropic hasn’t published Claude’s.

![What Happens When You Hit Send. Start With Text: You type a question or message. Split Into Tokens: A program called a tokenizer breaks the text into reusable chunks. Look Up Token IDs: The tokenizer finds each chunk’s number in its vocabulary. In this cl100k_base example, unbelievable becomes un, belie, and vable, with IDs 359, 32898, and 24694. Tokenization turns text into token IDs the model can use.](tokens-how-tokenization-works-editorial.jpg)

![Humans See a Cat. AI Starts With a Token ID. A person recognizes the animal. On the AI side, the written word cat becomes token ID 4719, using cl100k_base. A token ID identifies the token. Meaning comes later.](tokens-cat-token-id-editorial.jpg)

All the text you send to AI gets split into tokens. Here are some examples.

![How AI Splits Text Into Tokens. Verified cl100k_base examples: unbelievable becomes un (359), belie (32898), vable (24694); basketball becomes basket (60864), ball (4047); ChatGPT becomes Chat (16047), G (38), PT (2898); I ♥ AI becomes I (40), space plus ♥ (68679), space plus AI (15592). https://www.quickbookstraining.com becomes eight tokens: https (2485), :// (1129), www (2185), .quick (92074), book (2239), str (496), aining (2101), .com (916). SP marks a leading space. Numbers below the chunks are token IDs.](tokens-how-ai-splits-text-verified-editorial.jpg)

When AI replies, its answer comes out as token IDs. The tokenizer converts those IDs back into pieces of text and joins them together into the answer you read.

Words become numbers.

That lets AI work with your language using math.
