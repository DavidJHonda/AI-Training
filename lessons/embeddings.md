## UNDERSTAND AI

# Embeddings

You’ve learned that text is converted to tokens, and each has a unique identifier called a token ID. But that’s just a number. It doesn’t say anything about what it means.

It’s the same as the number assigned to your Student ID. It might let you in the building, but it doesn’t tell anyone whether you are funny, into hockey, or the person who steals fries at lunch.

![An ID Identifies You. It Doesn’t Describe You. Four students at a cafeteria table wear lanyard badges numbered 1024, 2048, 3072, and 4096. The standing student slips french fries into his shirt pocket. His ID won’t tell you he steals fries.](embeddings-student-id-editorial.jpg)

## How Numbers Can Represent Meaning

Imagine you and your friends rate Coke and coffee on six characteristics: Sweet, Bitter, Fizz, Heat, Caffeine, and Dark. Each score runs from 0 to 10. A higher number means more of that characteristic.

![Meaning Becomes an Ordered Row of Numbers. Coke and coffee have colored number tiles on the same six dimensions: Sweet, Bitter, Fizz, Heat, Caffeine, and Dark. Ratings run from 0 to 10. Each position always means the same thing; the number says how much.](embeddings-meaning-row-editorial.jpg)

If someone asked you, “Which drink scores 9 for Sweet, 1 for Bitter, and 10 for Fizz?” you’d immediately answer Coke.

You’ve turned each drink’s characteristics into a row of numbers that describes it.

The whole row of numbers is a **vector**. Each position in the row is a **dimension**, such as Sweet or Bitter. The number in that position is its **value**.

## When You Need Another Dimension

Now add a third drink to the taste test: Pepsi. Score it on the same six dimensions and a problem shows up. Pepsi scores the same as Coke. On these six numbers alone, you cannot tell them apart.

To tell them apart, you add a seventh dimension, **Citrus**. In your ratings, Pepsi scores 10 and Coke scores 1. Their numerical profiles now capture a difference the first six dimensions missed.

![One New Dimension Separates Similar Meanings. Coke, Pepsi, and coffee have colored number tiles on a 0 to 10 scale. Coke and Pepsi match on the first six dimensions. Citrus is labeled NEW, with green tiles showing Coke 1, Pepsi 10, and coffee 0. Pepsi’s 10 is emphasized in solid green. Six numbers match. The seventh tells them apart.](embeddings-new-dimension-editorial.jpg)

## How AI Uses This Idea

AI also uses numbers to represent meaning. Just as each drink has a numerical profile, each token has its own row of numbers. That row is called an **embedding**.

![From Taste Ratings to AI Embeddings. Your taste test: three drinks; six, then seven dimensions per row; you choose the ratings (0 to 10); named traits like Sweet and Fizz; you name the dimensions. AI: every token in the model’s vocabulary; typically thousands of dimensions per row; AI learns the values during training (positive and negative numbers, including decimals); patterns in how a token is used; no dimension labels, with values working together to represent meaning. Both use a row of numbers to describe something.](embeddings-taste-test-to-ai-editorial.jpg)

## Putting the Pieces Together

What happens when you type “cat” into AI? Follow its token ID to the matching row in the embedding table.

![Inside a Real Model. Token cat has token ID 4719, which selects its highlighted row in the embedding table. The table stores one embedding for every token. Dimensions: the d1 through dn column headings mark positions in the embedding. Value: the circled 0.45 is one learned number, also called a parameter. Embedding: the outlined numerical row is the complete row of numbers for one token.](embeddings-inside-real-model-editorial.jpg)

## Even Pieces of Words Get Embeddings

“Unbelievable” can be split into three tokens: “un”, “belie”, and “vable”. Each piece gets its own embedding, a row of learned numbers.

AI uses numbers to work with meaning.

Those numbers help AI recognize similarities and differences.
