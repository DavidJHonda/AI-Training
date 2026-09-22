## UNDERSTAND AI

# How AI Answers

When you ask AI a question, it first works out what your words mean together. Then it faces a new problem: how does it begin an answer?

Let’s give AI a simple question and watch how it builds an answer, one token at a time. We’ll show words as single tokens to make the example easier to follow.

### Board 1: Before the Answer Begins

**Image file:** `how-ai-answers-before-answer-begins.jpg`

![Before the Answer Begins](how-ai-answers-before-answer-begins.jpg)

**Teaching content:**

You ask: “What should I name my new dog?”

Before the answer begins, the question goes through four steps you have already seen.

Step 1, Tokens: AI breaks the question into pieces.

Step 2, Positions: AI marks where each piece belongs.

Step 3, Starting Vectors: AI turns each token into numbers that carry its starting meaning.

Step 4, Through Layers: attention and transformation work together to update the numbers.

AI uses the final token’s updated numbers to predict what comes next.

### Board 2: Why the Final Token Matters

**Image file:** `how-ai-answers-where-answer-begins.jpg`

![Why the Final Token Matters](how-ai-answers-where-answer-begins.jpg)

**Teaching content:**

Here is why the final token matters.

The question sits in a row of tokens: What, should, I, name, my, new, dog, and a question mark. In this example, the question mark is the final token.

The Question: the final token gathers information from every token before it.

The Final Token: its updated numbers are its final vector, and they help AI predict a reply that fits the question.

AI uses the final token’s vector to predict the first token of its answer.

## Starting the Answer

AI is ready to answer your question. It uses the final token’s updated numbers to calculate a probability for every token in its vocabulary.

Now watch the loop. AI selects a token, adds it to the reply, and uses the growing context to predict again.

### Board 3: The Answer, Token by Token

**Image file:** `how-ai-answers-token-by-token.jpg`

![The Answer, Token by Token](how-ai-answers-token-by-token.jpg)

**Teaching content:**

Here is the answer, token by token.

You ask: “What should I name my new dog?”

Prediction 1. The reply has not started, so the final token is the question mark. The top predictions are You at 18 percent, A at 14 percent, and Great at 9 percent. AI selects You in this example.

Three more predictions add could, name, and him.

Prediction 5. The reply so far is You could name him, so the final token is him. The top predictions are Spot at 22 percent, Max at 17 percent, and Buddy at 14 percent. AI selects Spot in this example.

The completed answer is a full sentence.

You could name him Spot.

## What Can Fit Next

You asked for a dog name, but AI began with You, a possible start to a reply.

Each added token changes what can fit next.

After You could name him, a dog name becomes a likely continuation.

AI keeps predicting tokens until it produces a special token that signals the answer is finished.

### Board 4: Inference: How AI Builds an Answer

**Image file:** `how-ai-answers-building-an-answer.jpg`

![Inference: How AI Builds an Answer](how-ai-answers-building-an-answer.jpg)

**Teaching content:**

This is inference: how AI builds an answer.

You ask: “What should I name my new dog?” The answer so far is You could name him. Follow the repeating process as AI adds the next token.

Step 1, Rank: AI scores every possible next token. Here Spot scores 22 percent, Max 17 percent, and Buddy 14 percent.

Step 2, Pick: AI selects a next token. Here it picks Spot.

Step 3, Add: AI attaches that token to the answer. The answer now reads You could name him Spot.

Step 4, Repeat: AI uses the longer context to predict again, asking what the next token should be.

Inference is the process AI uses to generate an answer one token at a time.

## Closing Message

Every answer is built one token at a time.

The whole run is called inference.
