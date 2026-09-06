## UNDERSTAND AI

# Embeddings

You’ve learned that text is converted to tokens, and each has a unique identifier called a token ID. But that’s just a number. It doesn’t say anything about what it means.

It’s the same as the number assigned to your Student ID. It might let you in the building, but it doesn’t tell anyone whether you are funny, into hockey, or the person who steals fries at lunch.

![Four students at a cafeteria table; one student slips french fries into his shirt pocket.](embeddings-0-cafeteria.jpg)

AI uses each token ID to look up a row of numbers called an **embedding**. These numbers are learned during training and help the model work with the token’s meaning and how it is used.

Imagine you and your friends rate Coke and coffee on six characteristics: Sweet, Bitter, Fizz, Heat, Caffeine, and Dark. Each score runs from 0 to 10. A higher number means more of that characteristic.

Here are your results. Compare what the ID tells you about each drink with what its scores tell you.

![Meaning Becomes an Ordered Row of Numbers. Coke and coffee are scored on the same six dimensions, with each value shown beneath its slider.](embeddings-meaning-row-editorial.jpg)

If someone asked you, “Which drink has sweet of 9, bitter of 1, and fizz of 10?” you’d immediately answer Coke.

You’ve turned each drink’s characteristics into a row of numbers. The row tells you something about the drink that its ID alone cannot.

A row of numbers in a specific order, like this, is called a **Vector**. Each slot (Sweet, Bitter, etc.) is a **Dimension**. And each number is a **Value**.

## What about Pepsi?

Now add a third drink to the taste test: Pepsi. Score it on the same six dimensions and a problem shows up. Pepsi looks almost exactly like Coke: both sweet, both fizzy, both lightly caffeinated, neither bitter nor hot. On these six numbers alone, you cannot tell them apart.

![One New Dimension Separates Similar Meanings. Coke, Pepsi, and coffee are scored on the same dimensions, with Citrus added as a seventh coordinate that separates Coke from Pepsi.](embeddings-new-dimension-editorial.jpg)

To tell them apart, you add a seventh dimension, **Citrus**. In your ratings, Pepsi scores 10 and Coke scores 1. Their numerical profiles now capture a difference the first six dimensions missed.

In a real model, engineers choose the number of dimensions, often thousands. Training learns the values in each token’s row. Those values work together to capture patterns in how the token is used. They aren’t simple ratings for traits like Sweet or Fizz.

Every token in the model’s vocabulary gets a row with the same number of dimensions, in the same order. What changes from token to token is the values. That shared structure helps the model recognize similarities and differences in meaning.

## INSIDE A REAL MODEL

In this example, the token **cat** has the **token ID** 4719. AI uses that ID to find cat’s row in the **embedding table**, which stores an embedding for every token. That row is cat’s **embedding vector**. The numbers that fill the table, plus many more throughout the model, are called **parameters**.

![From Token ID to Embedding. The cat token has ID 4719, which selects its highlighted row in the embedding table. That row is the token’s embedding vector. Each dimension is a position in the vector, and each value in the table is a parameter adjusted during training. The values work together to represent meaning.](embeddings-inside-real-model-editorial.jpg)

## Does every token get its own vector?

Yes. Remember how ‘unbelievable’ became three tokens? Each one (‘un’, ‘belie’, ‘vable’) gets its own vector with thousands of values. The model does not start with the meaning of the full word. Combining those pieces into the meaning of the whole word happens later, in the layers.

An ID identifies. An embedding describes.

A row of learned numbers helps AI work with meaning.
