# How AI Answers

When you ask AI a question, how does it begin an answer? And once it starts, how does it decide what comes next?

Let’s follow one example: “What should I name my new dog?” We’ll show words as single tokens to make the example easier to follow.

Before the answer begins, your question goes through four steps you have already seen.

First, tokens. AI breaks the question into pieces. Next, positions. AI marks where each piece belongs. Then, starting vectors. AI turns each token into a list of numbers. Finally, through layers. Attention and transformation work together to update those numbers.

Here’s the important connection. Each token’s vector is updated using information from the tokens before it.

In this simplified example, let’s follow the last token in your question: the question mark. It begins with a starting vector representing a question mark. As it passes through the layers, its numbers change to reflect your question about naming a dog.

Let’s see what this looks like. Compare “What should I name my new dog?” with “What should I cook for dinner?”

Both questions end with the same token: a question mark. In the first, its updated vector reflects the context of your whole question about naming your new dog. In the second, it reflects your different question about choosing dinner. Same token, different context, different updated vector.

Why is this important?

AI uses the final token’s updated vector to predict the first token of its answer.

Think about *Peanut butter and* or *Salt and*. Both end with **and**, but its updated vector reflects different words before it.

Using patterns learned during training, AI would likely give **jelly** a high probability after *Peanut butter and*, and **pepper** a high probability after *Salt and*. The prediction depends on the context reflected in those numbers.

The same process builds a longer answer. Each token AI adds becomes part of the context for predicting the next one.

Now let’s see how AI uses those numbers to build an answer.

The question is about naming your new dog, and the answer is still empty. Possible first tokens include “You” at 18 percent, “A” at 14 percent, and “Great” at 9 percent. Other tokens together account for 59 percent.

In this example, AI selects “You” and adds it to the answer.

Now the context includes part of the answer, too.

“You” is now the last token. Its updated vector reflects your question plus the answer so far, which is just “You.” AI uses those numbers to predict the next token.

Let’s keep going. AI adds “could,” then “name,” then “him,” one token at a time.

Each added token becomes part of the context.

The answer now reads “You could name him.” “Him” is now the last token. Its updated vector reflects your question plus all four words of the answer so far: “You could name him.”

AI uses those numbers to predict what comes next. A dog name is now a likely choice. Here, “Spot” has a 22 percent probability, “Max” has 17 percent, and “Buddy” has 14 percent. Other tokens together account for 47 percent.

AI selects “Spot” in this example. Another run could select a different name.

Notice what carries forward. The last token’s updated vector reflects both your question and everything AI has written so far.

How does the answer finish? AI adds a period. A special end-of-answer token signals that the reply is complete.

Every answer is built one token at a time.

The whole run is called inference.
