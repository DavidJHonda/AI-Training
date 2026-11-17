# 4. Tokens

`course-assets/tokens/tokens.mp4` · 3:22 · 547 words

**[0:00]** Computers only process numbers. That seems counterintuitive because when you write an email, send a text or type on your phone, you see words. But behind the scenes, those words are converted to numbers so the computer can work with them. The exact same rule applies to AI. How did your words become numbers that AI could work with, and how did AI's response turn back into words you could read?

**[0:23]** One idea is to assign each word in every language a unique number. That way, whatever word you type, the AI gets a corresponding number. But that whole word approach breaks down fast. People constantly invent new words, names, and slang. They also make typos and include things like emojis and computer code. Even a list of a million words couldn't cover everything a person might type. Instead, AI uses reusable chunks of text called tokens. Think of them as building blocks for language. Here is what tokens look like. Unbelievable becomes un, belie, and vol. It is one word built from three distinct chunks.

**[1:02]** Unusual becomes un and usual. That is two tokens.

**[1:07]** Unmatchable becomes un, match, and able. That is three tokens. Notice how all three of these un words reuse the exact same chunk, un.

**[1:18]** Tokens handle compound words effortlessly. Basketball becomes basket and ball, that is two tokens.

**[1:25]** I heart AI becomes I, then a space with the heart, then a space with AI. That is three tokens. On the board, you can see SP marks a leading space. Even complex inputs break down into chunks. The web address shown on the board breaks into eight disparate tokens. A token can be a whole word or just part of one. The full collection of tokens is called the model's vocabulary. This proves how a finite set of chunks can build infinite variations of human text. When setting up AI, engineers run a program that analyzes a massive collection of text to build this vocabulary database. Each token in that newly built vocabulary is then assigned a specific number, known as its token ID. Think of it like a street address. It perfectly identifies where and what the token is, but it tells the computer absolutely nothing about what the word actually means.

**[2:15]** Look at this diagram contrasting how you and an AI process the same text. When you read the word cat, you instantly know what it means. Fur, whiskers, be animal. For AI, it starts with a token ID. Here, the tokenizer converts the written word cat to ID 4719. The number identifies the token, not its meaning. Here is a diagram showing the full process of what happens when you hit send. Step one, start with text. You type a question or message. Step two, split into tokens. A program called a tokenizer breaks the raw text down into reusable chunks.

**[2:51]** Step three, look up token IDs. The tokenizer finds each chunk's assigned number within its vocabulary.

**[2:58]** Tokenization turns text into token IDs the model can use.

**[3:02]** When the AI replies, its initial answer is generated as token IDs. The tokenizer then converts those IDs back into pieces of text and joins them together into the final answer. Words become numbers. That lets AI work with your language using math.
