## UNDERSTAND AI

# How AI Answers

When you ask AI a question, it first works out what your words mean together. Then it faces a new problem: how does it begin an answer?

Let’s give AI a simple question and watch how it builds an answer, one token at a time. We’ll show words as single tokens to make the example easier to follow.

## Before the Answer Begins

![Before the Answer Begins. The user asks what to name a new dog. AI breaks the question into tokens, marks their positions, creates starting vectors, and runs them through the layers. AI uses the final token’s updated numbers to predict what comes next.](how-ai-answers-before-answer-begins-v2.jpg)

## Why the Final Token Matters

![Why the Final Token Matters. The question appears as tokens with the final question mark highlighted. The final token gathers information from preceding tokens, and its updated numbers help AI predict a reply that fits the question.](how-ai-answers-where-answer-begins-v2.jpg)

## Starting the Answer

AI is ready to answer your question. It uses the final token’s updated numbers to calculate a probability for every token in its vocabulary.

## The Answer, Token by Token

Now watch the loop. AI selects a token, adds it to the reply, and uses the growing context to predict again. Each selection is a **prediction**.

![The Answer, Token by Token. You ask: What should I name my new dog? Prediction 1 uses the final question mark and selects You from You 18%, A 14%, and Great 9%. Three more predictions add could, name, and him. Prediction 5 uses him as the final token and selects Spot from Spot 22%, Max 17%, and Buddy 14%. The gold banner shows the completed reply: You could name him Spot.](how-ai-answers-token-by-token.jpg)

You asked for a dog name, but AI began with **You**, a possible start to a reply. Each added token changes what can fit next. After **You could name him**, a dog name becomes a likely continuation.

AI keeps predicting tokens until it produces a special token that signals the answer is finished.

![Inference: How AI Builds an Answer. AI ranks every possible next token, selects a next token, adds it to the answer, and repeats using the longer context.](how-ai-answers-inference.jpg)

Every answer is built one token at a time.

The whole run is called inference.
