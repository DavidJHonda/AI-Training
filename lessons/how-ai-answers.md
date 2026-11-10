## UNDERSTAND AI

# How AI Answers

When you ask AI a question, it first works out what your words mean together. Then it faces a new problem: how does it begin an answer?

Let’s watch AI build an answer. Each time it adds a token, that token becomes part of the context for predicting what comes next. AI uses both your question and the answer so far. We’ll show words as single tokens to make the example easier to follow.

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

## How the Context Changes the Numbers

Here’s an important point about the layers. **Each token’s vector is updated using information from the tokens before it.**

In this simplified example, let’s follow the last token in “What should I name my new dog?” It begins with a starting vector representing a question mark. As it passes through the layers, those numbers change to reflect your question about naming a dog. After running through all the layers, the question mark’s vector reflects the context of your specific question.

Let’s see what this looks like. Both questions end with a question mark, but its updated vector is different in each.

### Board 2: Same Token, Different Context

**Image file:** `how-ai-answers-same-token-context.jpg`

![Same Token, Different Context](how-ai-answers-same-token-context.jpg)

**Teaching content:**

Naming your new dog: the question mark’s updated vector reflects the context of your whole question.

Choosing your dinner: the same question mark now has a different updated vector, reflecting this different question.

## WHY IS THIS IMPORTANT?

AI uses the final token’s updated vector to predict the first token of its answer.

Think about *Peanut butter and* or *Salt and*. Both end with **and**, but its updated vector reflects different words before it.

Using patterns learned during training, AI would likely give **jelly** a high probability after *Peanut butter and*, and **pepper** a high probability after *Salt and*. The prediction depends on the context reflected in those numbers.

The same process builds a longer answer. Each token AI adds becomes part of the context for predicting the next one.

For example, AI might select “You” to begin its reply.

“You” is now the last token.

The last token’s updated vector reflects both your question and everything AI has written so far.

AI uses those numbers to predict what comes next.

## How AI Answers

Follow one possible reply, from its first token to the end of the answer.

### Board 3: Possible Starts

**Image file:** `how-ai-answers-first-prediction.jpg`

![Possible Starts](how-ai-answers-first-prediction.jpg)

**Teaching content:**

You ask: “What should I name my new dog?”

AI’s answer has no tokens yet.

AI predicts possible starts to its reply. Possible next tokens include You at 18 percent, A at 14 percent, and Great at 9 percent. Other tokens together account for 59 percent.

### Board 4: AI Selected You

**Image file:** `how-ai-answers-you-selected.jpg`

![AI Selected You](how-ai-answers-you-selected.jpg)

**Teaching content:**

You is now the last token. Its updated vector reflects your question plus the answer so far, which is just You. AI uses those numbers to predict the next token.

The highlighted You is the token AI selected from those choices: You at 18 percent, A at 14 percent, Great at 9 percent, and other tokens together at 59 percent.

## The Growing Reply

AI adds could, name, and him, one token at a time.

Each added token becomes part of the context.

### Board 5: Possible Dog Names

**Image file:** `how-ai-answers-name-prediction.jpg`

![Possible Dog Names](how-ai-answers-name-prediction.jpg)

**Teaching content:**

Your question is still “What should I name my new dog?” AI’s answer so far is “You could name him”.

Him is now the last token. Its updated vector reflects your question plus the answer so far: You could name him. AI uses those numbers to predict the next token. A dog name is now a likely choice.

Possible next tokens include Spot at 22 percent, Max at 17 percent, and Buddy at 14 percent. Other tokens together account for 47 percent.

### Board 6: AI Selected Spot

**Image file:** `how-ai-answers-spot-selected.jpg`

![AI Selected Spot](how-ai-answers-spot-selected.jpg)

**Teaching content:**

AI selects Spot in this example; another run could select a different name.

The highlighted Spot is the token AI selected from those choices: Spot at 22 percent, Max at 17 percent, Buddy at 14 percent, and other tokens together at 47 percent.

AI’s answer now reads “You could name him Spot”.

## Finishing the Reply

AI adds a period, then an end-of-answer token.

A special end-of-answer token signals that the reply is complete.

You could name him Spot.

## Closing Message

Every answer is built one token at a time.

The whole run is called inference.
