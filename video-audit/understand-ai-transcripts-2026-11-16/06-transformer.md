# 6. Transformer

`course-assets/transformer/transformer.mp4` · 4:26 · 657 words

**[0:00]** When you type a message to ChatGBT, you use words, and it responds with words. Underneath, AI splits your text into small pieces, called tokens. Each token has an embedding, a row of numbers that represents its starting meaning. AI works mathematically, but to make the connections easier to see, we will use whole words.

**[0:20]** Two problems.

**[0:22]** Let's look at the left side, problem one. The same word can mean something completely different, depending on the sentence. If you say, please turn on the light, light means brightness. But if you say, the empty suitcase felt light, it means not heavy. So when you type light, how does the AI know which version you mean?

**[0:43]** Now look at the right side. Problem 2, pronouns.

**[0:47]** The cat was thirsty, so it drank the milk. Here, it means the cat. But in the sentence, the milk was fresh, so the cat drank it, it means the milk. When you use a pronoun like it, how does the AI know what you're actually referring to? The answer is right there in the rest of the sentence. The surrounding words help AI figure out the meaning. Our human brains use those surrounding words to lock on to the right meaning almost instantly. But for earlier AI, keeping that context connected was a serious challenge, because it read text strictly in order, one word at a time. Let's follow this sentence. the tired cat sat on the mat during the May rainstorm. It soon fell asleep.

**[1:30]** Notice the growing distance between cat and it. Earlier AI often struggled to keep that connection, especially in longer passages. That limitation set the stage for a new architecture.

**[1:42]** In 2017, eight researchers at Google published a paper called, Attention is All You Need. It introduced the transformer, which is the T in chat GPT. This diagram shows a completely different mechanical approach. The transformer can process the tokens in your message at once. By taking in the complete message together, the word IT can immediately draw on information from CAT, bypassing the gap of the words in between. There's more to reading than taking in the words. AI actually needs to figure out which words matter most and use that information to update the underlying numbers.

**[2:17]** This board shows two mechanisms updating a token's meaning. First, attention weighs information from relevant words and blends it into the token's numbers. Notice the connection flowing from it to cat.

**[2:31]** Second, transformation uses learned patterns to further process those numbers. The surrounding words help update each token's numbers. Applying this to our examples shows how the transformer resolves meaning.

**[2:45]** Please turn on the light, means brightness. The empty suitcase felt light means not heavy. On the left turn on acts on the token light pulling its mathematical meaning toward brightness. Below empty establishes light as not heavy. It works similarly for pronouns.

**[3:05]** The cat was thirsty so it drank the milk. It means cat. The milk was fresh so the cat drank it. It means milk. First it points to the thirsty cat. Next to the The combination of attention and transformation is exactly how AI deduces which meaning fits.

**[3:25]** Because the Transformer continually weighs relationships across the entire text simultaneously, this same mathematical blending scales up to capture broader structural patterns, allowing AI to interpret human nuances like sarcasm and idioms. The words alone aren't enough. Their order matters too. This board contrasts two phrases, dog bites man and man bites dog. Without positional information, these identical tokens and starting embeddings are completely ambiguous. They float without sequence, capable of describing two entirely different events. The solution is positional encoding. It acts as a numerical stamp, one, two, three, that helps the model keep track of every token's precise place in the sequence.

**[4:14]** Positional encoding tells the transformer where every token belongs. Attention is all you need. AI uses relationships between words to help interpret your message.
