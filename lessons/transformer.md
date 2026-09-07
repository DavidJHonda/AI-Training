## UNDERSTAND AI

# Transformer

When you type a message to ChatGPT, you use words, and it responds with words. Underneath, AI splits your text into small pieces called **tokens**. Each token has an **embedding**, a row of numbers that represents its starting meaning.

These two examples show how the surrounding words, or **context**, shape meaning. AI works with tokens, but we’ll use whole words to make the connections easier to see.

![Two Problems Context Must Solve. Different meanings: Please turn on the LIGHT means brightness, while The suitcase is LIGHT enough to carry means not-heavy. Pronouns: The cat drank the milk because IT was thirsty points to the cat, while IT was fresh points to the milk. Context determines which meaning fits.](transformer-context-problems-editorial.jpg)

## WHY THIS WAS HARD FOR AI

Our human brains see the right meaning instantly from the surrounding words. For earlier AI, this was a challenge because it read text in order, one word at a time. The further it read, the more the early words faded.

![How Earlier AI Read Text. The diagram follows the full sentence The cat sat on the mat during the May rainstorm because it was tired. We know IT refers to CAT. Earlier AI often struggled to keep that connection, especially in longer passages.](transformer-before-transformers-editorial.jpg)

## THE BREAKTHROUGH

In 2017, eight researchers at Google published a paper called **Attention Is All You Need**. It introduced the **Transformer**, a widely used architecture for large language models, and the “T” in ChatGPT.

The Transformer reads your whole message at once. In our example, **IT** can draw on information from the earlier word **CAT**, even with several words in between.

![How a Transformer Reads a Sentence. The complete message arrives together: The cat sat on the mat during the May rainstorm because it was tired. All words are present from the start.](transformer-how-transformer-reads-editorial.jpg)

Reading your whole message at once is only the start. AI needs to figure out which words matter and use that information to update the numbers. In our example, **IT** needs information from **CAT** to help represent what it refers to in this sentence. Attention and transformation work together to make that happen.

![How Context Changes the Numbers. Attention weighs information from relevant words and blends it into the token’s numbers, illustrated by IT connecting back to CAT. Transformation uses learned patterns to further process those numbers, shown as IT after attention becoming IT with context. Attention and transformation work together to build meaning from context.](transformer-attention-transformation-editorial.jpg)

Now let’s return to our two examples.

![How the Transformer Resolves Meaning: Different meanings: “turn on” tells us LIGHT means brightness; “carry” tells us LIGHT means not-heavy. Pronouns: “thirsty” describes the cat, so IT refers to the cat; “fresh” describes the milk, so IT refers to the milk. Each panel asks which words provide the clues. Attention and transformation help AI work out which meaning fits.](transformer-resolves-meaning-editorial.jpg)

Attention and transformation also help AI interpret sarcasm, idioms, and even an “it” that points to nothing at all, as in “it was a cold day.”

## One catch: word order

Reading everything at once creates a problem that reading in order never had. Consider a simple sentence: “Dog bites man.” Same three tokens. Same starting embeddings. But the order carries the meaning.

![How a Transformer Keeps Words in Order. The top strip compares Dog bites man with Man bites dog: the same tokens describe different events. Below, Without Position Information shows scattered words; Position Stamps Preserve Order marks Dog as 1, bites as 2, and man as 3. Positional encoding tells the Transformer where every token belongs.](transformer-word-order-editorial.jpg)

Attention is all you need.

AI uses relationships between words to help interpret your message.
