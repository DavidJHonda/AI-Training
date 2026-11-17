# 10. How AI Answers

`course-assets/how-ai-answers/how-ai-answers.mp4` · 3:35 · 600 words

**[0:00]** When you ask a question, the system first processes your words together. Then it faces a new problem. How does it actually begin an answer? We'll show words as single tokens to make this example much easier to follow.

**[0:12]** Imagine you ask, what should I name my new dog? Before the answer begins, the question goes through four steps you've already seen.

**[0:20]** Tokens breaks the question into pieces. Positions marks where each piece belongs. Starting vectors turns each token into numbers that carry its starting meaning. And finally, through layers, where attention and transformation work together to update those numbers.

**[0:36]** As the tokens pass through the layers, each token's vector is updated using information from the tokens before it. In this simplified example, let's follow the last token in the question, what should I name my new dog? It begins with a starting vector representing a question mark. As it passes through the layers, those numbers change to reflect your question about naming a dog. After running through all the layers, the question marks vector reflects the context of your specific question.

**[1:02]** Looking at naming a dog versus choosing dinner, we see the identical final token gets different updated vectors because the different contexts change the question marks numbers. For naming your new dog, the question marks updated vector reflects the context of your whole question. For choosing your dinner, the exact same question mark now has a completely different updated vector, reflecting this different question. Why is this important?

**[1:26]** AI uses the final token's updated vector to predict the first token of its answer. Think about peanut butter ant and salt ant. Now, both end with and.

**[1:36]** But its updated vector reflects different words before it. So using patterns learned during training, an AI would likely give jelly a high probability after peanut butter and, and pepper a high probability after saltant. The prediction depends on the context reflected in those numbers. It adds the chosen token to the context and then predicts the next one. That's exactly how our response is built, using your question and the answer so far. For the dog naming question, the answer has no tokens yet. AI predicts possible starts to its reply, which include you at 18%, A at 14%, and great at 9%, with other tokens together accounting for 59%. AI selected you. You is now the last token.

**[2:21]** The last token's updated vector reflects both your question and everything the AI has written so far. Now, the context includes part of the answer, too. Its updated vector reflects the question plus the one-word answer, you. The system uses those numbers to predict exactly what comes next. To continue the growing reply, AI adds the word could to the sequence. Next, AI adds the word name.

**[2:47]** Then, AI adds the word him. Each added token becomes part of the context. Him is now the last token, and its updated vector reflects the question plus all four answer words to predict a dog name. A dog name is now a highly likely choice. Possibilities include Spot at 22%, Max at 17%, and Buddy at 14%, with other tokens accounting for 47%. AI selected Spot to build this answer, but it is important to note that another run could select a different name entirely. The answer now reads, you could name him Spot.

**[3:19]** Finishing the reply, AI adds a period, then an end of answer token.

**[3:24]** A special end of answer token signals that the reply is complete.

**[3:29]** Every answer is built one token at a time. The whole run is called inference.
