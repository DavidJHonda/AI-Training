## UNDERSTAND AI

# Tokens

**Math is the magic that powers AI.** But you ask AI questions in words, not numbers. How do your words become numbers that AI can use?

![What using AI feels like: You ask what the best Avengers movie is, and AI answers in natural language with Avengers Endgame and Infinity War as the leading choices.](tokens-using-ai-feels-like-editorial.jpg)

You see a conversation in words. Behind the scenes, your question is converted into numbers before the model processes it.

Why not give every word its own number? People keep inventing words, names, and slang. They also make typos and include things like emojis and code. Even a list of a million words couldn’t cover everything a person might type.

## THE SOLUTION

The solution is to break text into reusable chunks called **tokens**. A token can be a whole word or just part of one. For example, the chunk **un** can be reused in words like **unbelievable** and **unusual**.

![One Chunk, Many Words. The shared token un is highlighted in unbelievable, unmatchable, and unusual. The rest of each word may contain one or more additional tokens.](tokens-one-chunk-editorial.jpg)

Here’s how it works:

![How Tokenization Works. Start With Text: You type a question or message. Split Into Tokens: A program called a tokenizer breaks the text into reusable chunks. Look Up Token IDs: The tokenizer finds each chunk’s number in its vocabulary. In this cl100k_base example, unbelievable becomes un, belie, and vable, with IDs 359, 32898, and 24694. Tokenization turns text into token IDs the model can use.](tokens-how-tokenization-works-editorial.jpg)

Each model knows a fixed set of them, called its **vocabulary**, and these run large: ChatGPT’s holds about **200,000** tokens and Gemini’s about **256,000**. Anthropic hasn’t published Claude’s.

Each token gets a number, its **token ID**. Think of it as an address in the model’s vocabulary: it tells the model which token, but says nothing about what it means.

![Humans See a Cat. AI Starts With a Token ID. A person recognizes the animal. On the AI side, the written word cat becomes token ID 4719, using cl100k_base. A token ID identifies the token. Meaning comes later.](tokens-cat-token-id-editorial.jpg)

Different tokenizers can split the same text differently. Here are examples from one tokenizer.

![How AI Splits Text Into Tokens. Verified cl100k_base examples: unbelievable becomes un (359), belie (32898), vable (24694); basketball becomes basket (60864), ball (4047); ChatGPT becomes Chat (16047), G (38), PT (2898); I ♥ AI becomes I (40), space plus ♥ (68679), space plus AI (15592). https://www.quickbookstraining.com becomes eight tokens: https (2485), :// (1129), www (2185), .quick (92074), book (2239), str (496), aining (2101), .com (916). SP marks a leading space. Numbers below the chunks are token IDs.](tokens-how-ai-splits-text-verified-editorial.jpg)

Once it’s built, the model uses that same fixed vocabulary of tokens every time it reads text.

Computers don’t read text.

Tokens convert language into readable numbers.
