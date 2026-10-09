## UNDERSTAND AI

# Embeddings

You’ve learned that text is converted to tokens, and each has a unique identifier called a token ID. But that’s just a number. It doesn’t say anything about what it means.

It’s the same as the number assigned to your Student ID. It might let you in the building, but it doesn’t tell anyone whether you are funny, into hockey, or the person who steals fries at lunch.

### Board 1: An ID Identifies You. It Doesn’t Describe You.

**Image file:** `embeddings-student-id-faceless-no-banner.jpg`

![An ID Identifies You. It Doesn’t Describe You.](embeddings-student-id-faceless-no-banner.jpg)

**Teaching content:**

An ID identifies you. It doesn’t describe you.

Four students at a cafeteria table wear Student ID badges numbered 1024, 2048, 3072, and 4096. One of them is standing, slipping french fries into his shirt pocket. The badge numbers tell you which student is which. They tell you nothing about who each student is.


## How Numbers Can Represent Meaning

Imagine you and your friends rate drinks on six characteristics: Sweet, Bitter, Fizz, Heat, Caffeine, and Dark. Each score runs from 0 to 10. A higher number means more of that characteristic.

### Board 2: Six Characteristics

**Image file:** `embeddings-ratings-headings.jpg`

![Six characteristics with the drink rows still empty](embeddings-ratings-headings.jpg)

**Teaching content:**

The table has a place for each drink and six ratings: Sweet, Bitter, Fizz, Heat, Caffeine, and Dark. Ratings run from 0 for low to 10 for high.

### Board 3: Coffee

**Image file:** `embeddings-ratings-coffee.jpg`

![Coffee fills the first row](embeddings-ratings-coffee.jpg)

**Teaching content:**

You and your friends tasted Coffee and rated it on six characteristics. Let’s put those ratings in the table.

Coffee scores 1 for Sweet, 9 for Bitter, 0 for Fizz, 9 for Heat, 8 for Caffeine, and 10 for Dark.

### Board 4: Add Coke

**Image file:** `embeddings-ratings-coke.jpg`

![Coffee first, Coke second](embeddings-ratings-coke.jpg)

**Teaching content:**

Next, you taste Coke and rate it on the same six characteristics.

Coke scores 9 for Sweet, 1 for Bitter, 10 for Fizz, 2 for Heat, 3 for Caffeine, and 8 for Dark.

Compare Coke and Coffee. Which drink scores 9 for Sweet, 1 for Bitter, and 10 for Fizz? That’s Coke.

A row of numbers like this is called a vector.

Each position is a dimension, such as Sweet, and the number there is its value.

### Board 5: Add Pepsi

**Image file:** `embeddings-ratings-pepsi.jpg`

![Coffee, Coke, and Pepsi; Coke and Pepsi have identical six-number profiles](embeddings-ratings-pepsi.jpg)

**Teaching content:**

Now let’s add Pepsi to the same taste test.

Compare Coke and Pepsi’s six-number profiles. If you hid the drink names, could these numbers tell you which was which? All six values match. With only these numbers, you cannot tell Coke and Pepsi apart.

### Board 6: Add Citrus

**Image file:** `embeddings-ratings-citrus-column.jpg`

![The Citrus column appears with its values still empty](embeddings-ratings-citrus-column.jpg)

**Teaching content:**

Let’s add Citrus, a rating of citrus flavor from 0 to 10.

Citrus gives us a seventh dimension.

Now rate each drink for citrus flavor, using the same 0-to-10 scale.

### Board 7: Compare the Citrus Ratings

**Image file:** `embeddings-ratings-citrus-values.jpg`

![The Citrus values fill in: Coffee 0, Coke 1, Pepsi 10](embeddings-ratings-citrus-values.jpg)

**Teaching content:**

In your taste-test ratings, Coffee scores 0 for Citrus, Coke scores 1, and Pepsi scores 10. The first six values still match for Coke and Pepsi, but their seven-number profiles now differ.

Another dimension can capture a difference the earlier numbers missed.

## How AI Uses This Idea

AI also uses numbers to represent meaning.

Just as each drink has a numerical profile, each token has its own row of numbers.

That row is called an embedding.

### Board 8: From Taste Ratings to AI Embeddings

**Image file:** `embeddings-taste-test-to-ai.jpg`

![From Taste Ratings to AI Embeddings](embeddings-taste-test-to-ai.jpg)

**Teaching content:**

From taste ratings to AI embeddings: the board compares your taste test with AI on five points.

What gets a row: in your taste test, three drinks. In AI, every token in the model’s vocabulary.

Dimensions per row: in your taste test, six, then seven. In AI, typically thousands.

Values: in your taste test, you choose the ratings, from 0 to 10. In AI, AI learns them during training. They are positive and negative numbers, including decimals.

What they capture: in your taste test, named traits like Sweet and Fizz. In AI, patterns in how a token is used.

Dimension labels: in your taste test, you name them. In AI, there are none. The values work together to represent meaning.

Both use a row of numbers to describe something.

## Putting the Pieces Together

What happens when you type “cat” into AI? Follow its token ID to the matching row in the embedding table.

### Board 9: Inside a Real Model

**Image file:** `embeddings-inside-real-model.jpg`

![Inside a Real Model](embeddings-inside-real-model.jpg)

**Teaching content:**

Inside a real model, the token is cat. Its token ID is 4719. The token ID leads to cat’s row in the embedding table.

The embedding table stores one embedding for every token. Cat’s row sits alongside rows for other tokens, such as dog, latte, truck, bicycle, and map.

The table's first two columns are the token ID and the token. The dimensions are the columns after them, labeled d1, d2, d3, d4, and so on up to dn. Each column is one position in the embedding.

Cat’s row begins 0.45, then negative 0.23, then 0.80, then 0.17, and continues across thousands of positions to negative 0.35 in the last one.

A value is one learned number, such as the circled 0.45. A value is also called a parameter.

The embedding is the complete row of numbers for one token.

## Even Pieces of Words Get Embeddings

“Unbelievable” can be split into three tokens: “un”, “belie”, and “vable”. Each piece gets its own embedding, a row of learned numbers.

## Closing Message

AI uses numbers to work with meaning.

Those numbers help AI recognize similarities and differences.
