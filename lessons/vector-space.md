## UNDERSTAND AI

# Vector Space

AI represents meaning with rows of numbers called **embeddings**. As AI processes your message, the layers change the numbers. If the numbers are different, how do they still represent meaning? To understand how, let’s explore vector space.

## Let’s Start With a Map

A map uses two numbers to describe position: latitude and longitude. Dallas, Texas, is roughly 33° north, 97° west. New York City and Mountain View, California, have their own coordinates, using those same two dimensions.

Imagine these are the only three cities on our map.

![Three Cities, Two Coordinates Each. A United States map marks Mountain View at roughly 37 north, 122 west; Dallas at 33 north, 97 west; and New York City at 41 north, 74 west.](vector-space-1-cities.jpg)

Someone hands you two sets of coordinates. For each position, which of the three cities is closest?

- **38 N, 120 W**
- **39 N, 70 W**

![Use the Map to Find the Closest City. The same U.S. map shows cities as solid colored dots and new positions as purple outlined diamonds. Dotted lines connect 38 north, 120 west to Mountain View and 39 north, 70 west to New York City, the nearest of the three cities.](vector-space-1-cities-closest.jpg)

The new coordinates don’t match any city exactly. But comparing positions lets you find the closest city.

## From Places to Meaning

These ratings for Coke, Pepsi, and coffee describe seven characteristics. Each drink gets a row of numbers called a **vector**.

![Three Drinks, Seven Dimensions Each. Coke, Pepsi, and coffee have colored number tiles on the same seven dimensions, rated from 0 to 10. Citrus is green and every score has equal emphasis. Coke and Pepsi have more similar profiles than either does to coffee.](vector-space-2-taste.jpg)

We can use these numbers as coordinates on a map of similarities. Coke and Pepsi have similar ratings, so their vectors sit close together. Coffee’s ratings are quite different, so its vector sits farther away.

![A Map of Drink Similarities. Coke and Pepsi are nearby points, with coffee farther from both. Each drink shows seven colored scores in this order: Sweet, Bitter, Fizz, Heat, Caffeine, Dark, Citrus. Coke: 9, 1, 10, 2, 3, 8, 1. Pepsi: 9, 1, 10, 2, 3, 8, 10. Coffee: 1, 9, 0, 9, 8, 10, 0. Dotted lines compare the gaps between positions.](vector-space-neighborhoods.jpg)

Someone gives you the ratings for a mystery drink. They don’t match Coke, Pepsi, or coffee exactly. Just as you did with the cities, use the map to find the closest match.

- **9, 1, 10, 2, 3, 8, 9**

![Use the Map to Find the Closest Drink. The same map keeps Coke, Pepsi, coffee, and their scores in place. A new mystery point with ratings 9, 1, 10, 2, 3, 8, 9 sits close to Pepsi, joined by a short purple dotted line. Its first six scores match Pepsi, and its Citrus score is 9 compared with Pepsi’s 10. Pepsi is the closest match.](vector-space-closest-drink.jpg)

Changing Pepsi’s Citrus score from 10 to 9 creates a new vector. It doesn’t match any drink in our table exactly, but it still describes something: a sweet, fizzy drink with a strong citrus taste. **New numbers can represent a new combination of characteristics.**

## Distance

To measure **distance**, compare the numbers in matching positions across the two vectors. The gaps between those numbers tell you how far apart the vectors are. Smaller gaps mean closer positions.

AI uses this idea on a much larger scale. Its embeddings have thousands of dimensions, with values learned during training. Similar meanings usually occupy nearby positions.

## Meaning is a position

A vector’s numbers describe a **position** in a space with many dimensions. That’s **vector space**. As the layers change a token’s numbers, its position changes, reflecting information from the surrounding text.

As the layers change the numbers, they change the information those numbers represent. The updated numbers can capture how a word is being used in this particular sentence. During training, AI learns how to produce and use these numerical patterns.

Consider this sentence:

“The **cat** sat on the mat during the May rainstorm because **it** was tired.”

![Meaning Is a Position. IT’s updated vector is shown on a conceptual map with the label IT WITH CONTEXT. An arrow labeled REFERS TO connects it to CAT, illustrating the contextual relationship represented by the updated numbers. KITTEN, DOG, and PET appear nearby as background examples.](vector-space-4-meaning-map.jpg)

Meaning is a position.

Similar meanings usually sit close together.
