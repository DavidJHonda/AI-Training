## UNDERSTAND AI

# Tokens

You’ve seen the idea already; **Math is the magic that powers AI**.

But that’s not what using AI feels like.

When you type a question into ChatGPT, you ask in plain English and get plain English back.

## You

what’s the best Avengers movie?

## AI

Most people point to Avengers: Endgame. It’s the big payoff to a decade of films, and it broke box-office records. Infinity War is the other top pick if you like a darker ending.

That felt effortless, because you think in language. You read *“Avengers”* and instantly picture the movie.

A computer can’t do that. Here’s the fact underneath everything: **computers work only with numbers. They don’t read text at all**. So before AI can read your question, it must convert all your text to numbers.

An obvious solution is to assign every word in the English language its own number. But, that falls apart fast. Counting names, slang, typos, and code, you’d need **millions** of numbers, and you still couldn’t cover words nobody’s invented yet.

## THE SOLUTION

Software engineers found a smarter way: break language into **reusable chunks**. For example, take every word that starts with **UN**: **UN**believable, **UN**matchable, **UN**tied. Thousands of words reuse that one piece, so the vocabulary stores **UN** once and uses the chunk to help spell all words that use it.

One chunk, thousands of words

un

believable

un

matchable

un

tied

un

lock

un

fair

un

do

un

known

un

usual

un

happy

un

plug

un

fold

un

seen

Plus thousands more

Before your words ever reach the model, a small ordinary program (no AI involved) breaks them into these chunks. The process is called **tokenization**, and the chunks are called **tokens**. A token might be a whole word, part of a word, punctuation, an emoji, or even the space before a word.

Each model knows a fixed set of them, called its **vocabulary**, and these run large: ChatGPT’s holds about **200,000** tokens and Gemini’s about **256,000**. Anthropic hasn’t published Claude’s.

Each token gets a number, its **token ID**. Think of it as an address in the model’s vocabulary: it tells the model which token, but says nothing about what it means.

How a human sees a cat vs. AI

🧠

## Human

#### Instant Understanding

cat

↓

🐱

You see the word and instantly know what it means: soft fur, whiskers, sits on your keyboard.

🤖

## AI

#### Just a Number

cat

↓

9246

The tokenizer turns it into a token ID. The exact number varies by model; either way, it’s a number, not meaning yet.

Here’s how AI splits text into tokens. Each AI does this differently, so this is only an example.

01

"unbelievable"

→

un

359

believ

81928

able

481

3 tokens (broken into known parts)

02

"basketball"

→

basket

60844

ball

4803

2 tokens

03

"ChatGPT"

→

Chat

16047

G

38

PT

2898

3 tokens (brand names get split)

04

"I ❤️ AI"

→

I

40

␠❤️

157644

␠AI

15592

3 tokens (the ␠ marks a leading space)

05

"https://www.quickbookstraining.com"

→

https

5765

://

1358

www

2185

.quick

23489

books

12483

training

6573

.com

916

7 tokens (URLs split into known pieces)

Once it’s built, the model uses that same fixed vocabulary of tokens every time it reads text.

A token ID is an address, not a meaning.

Turning that number into meaning comes next.
