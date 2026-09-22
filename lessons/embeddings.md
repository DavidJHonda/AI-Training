## UNDERSTAND AI

# Embeddings

You’ve learned that text is converted to tokens, and each has a unique identifier called a token ID. But that’s just a number. It doesn’t say anything about what it means.

It’s the same as the number assigned to your Student ID. It might let you in the building, but it doesn’t tell anyone whether you are funny, into hockey, or the person who steals fries at lunch.

### Board 1: An ID Identifies You. It Doesn’t Describe You.

**Image file:** `embeddings-student-id-faceless.jpg`

![An ID Identifies You. It Doesn’t Describe You.](embeddings-student-id-faceless.jpg)

**Teaching content:**

An ID identifies you. It doesn’t describe you.

Four students at a cafeteria table wear ID badges numbered 1024, 2048, 3072, and 4096. One of them is standing, slipping french fries into his shirt pocket. The badge numbers tell you which student is which. They tell you nothing about who each student is.

His ID won’t tell you he steals fries.

## How Numbers Can Represent Meaning

Imagine you and your friends rate Coke and coffee on six characteristics: Sweet, Bitter, Fizz, Heat, Caffeine, and Dark. Each score runs from 0 to 10. A higher number means more of that characteristic.

### Board 2: Meaning Becomes an Ordered Row of Numbers

**Image file:** `embeddings-meaning-row.jpg`

![Meaning Becomes an Ordered Row of Numbers](embeddings-meaning-row.jpg)

**Teaching content:**

Ratings run from 0 for low to 10 for high. Coke and coffee are scored on the same six characteristics in the same order: Sweet, Bitter, Fizz, Heat, Caffeine, and Dark.

Coke scores 9 for Sweet, 1 for Bitter, 10 for Fizz, 2 for Heat, 3 for Caffeine, and 8 for Dark.

Coffee scores 1 for Sweet, 9 for Bitter, 0 for Fizz, 9 for Heat, 8 for Caffeine, and 10 for Dark.

The scores describe the drinks. Coke is sweet and fizzy. Coffee is bitter and hot, with much more caffeine.

Each position always means the same thing. The number says how much.

If someone asked you, “Which drink scores 9 for Sweet, 1 for Bitter, and 10 for Fizz?” you’d immediately answer Coke.

You’ve turned each drink’s characteristics into a row of numbers that describes it.

The whole row of numbers is a vector.

Each position in the row is a dimension, such as Sweet or Bitter.

The number in that position is its value.

## When You Need Another Dimension

Now add a third drink to the taste test: Pepsi. Score it on the same six dimensions and a problem shows up. Pepsi scores the same as Coke. On these six numbers alone, you cannot tell them apart.

To tell them apart, you add a seventh dimension, Citrus. In your ratings, Pepsi scores 10 and Coke scores 1. Their numerical profiles now capture a difference the first six dimensions missed.

### Board 3: One New Dimension Separates Similar Meanings

**Image file:** `embeddings-new-dimension.jpg`

![One New Dimension Separates Similar Meanings](embeddings-new-dimension.jpg)

**Teaching content:**

Ratings still run from 0 to 10. The six original dimensions are Sweet, Bitter, Fizz, Heat, Caffeine, and Dark. Citrus is the new seventh dimension.

Coke scores 9 for Sweet, 1 for Bitter, 10 for Fizz, 2 for Heat, 3 for Caffeine, and 8 for Dark. Pepsi scores exactly the same on all six: 9, 1, 10, 2, 3, and 8. Coffee scores 1, 9, 0, 9, 8, and 10 on the same six.

On Citrus, Coke scores 1, Pepsi scores 10, and coffee scores 0.

Coke and Pepsi match on the first six dimensions. The seventh, Citrus, is where they differ.

Six numbers match. The seventh tells them apart.

## How AI Uses This Idea

AI also uses numbers to represent meaning.

Just as each drink has a numerical profile, each token has its own row of numbers.

That row is called an embedding.

### Board 4: From Taste Ratings to AI Embeddings

**Image file:** `embeddings-taste-test-to-ai.jpg`

![From Taste Ratings to AI Embeddings](embeddings-taste-test-to-ai.jpg)

**Teaching content:**

The board compares your taste test with AI on five points.

What gets a row: in your taste test, three drinks. In AI, every token in the model’s vocabulary.

Dimensions per row: in your taste test, six, then seven. In AI, typically thousands.

Values: in your taste test, you choose the ratings, from 0 to 10. In AI, the model learns the values during training. They are positive and negative numbers, including decimals.

What they capture: in your taste test, named traits like Sweet and Fizz. In AI, patterns in how a token is used.

Dimension labels: in your taste test, you name them. In AI, there are none. The values work together to represent meaning.

Both use a row of numbers to describe something.

## Putting the Pieces Together

What happens when you type “cat” into AI? Follow its token ID to the matching row in the embedding table.

### Board 5: Inside a Real Model

**Image file:** `embeddings-inside-real-model.jpg`

![Inside a Real Model](embeddings-inside-real-model.jpg)

**Teaching content:**

The token is cat. Its token ID is 4719. The token ID leads to cat’s row in the embedding table.

The embedding table stores one embedding for every token. Cat’s row sits alongside rows for other tokens, such as dog, latte, truck, bicycle, and map.

The dimensions are the columns, labeled d1, d2, d3, d4, and so on up to dn. Each column is one position in the embedding.

Cat’s row begins 0.45, then negative 0.23, then 0.80, then 0.17, and continues across thousands of positions to negative 0.35 in the last one.

A value is one learned number, such as the circled 0.45. A value is also called a parameter.

The embedding is the complete row of numbers for one token.

## Even Pieces of Words Get Embeddings

“Unbelievable” can be split into three tokens: “un”, “belie”, and “vable”. Each piece gets its own embedding, a row of learned numbers.

## Closing Message

AI uses numbers to work with meaning.

Those numbers help AI recognize similarities and differences.
