## UNDERSTAND AI

# Vector Space

AI represents meaning with rows of numbers called **embeddings**. As AI processes your message, the layers change the numbers. If the numbers are different, how do they still represent meaning? To understand how, let’s explore **vector space**.

## Let’s Start With a Map

A map uses two numbers to describe position: latitude and longitude. Dallas, Texas, is roughly 33° north, 97° west. New York City and Mountain View, California, have their own coordinates, using those same two dimensions.

Imagine these are the only three cities on our map.

![Three Cities, Two Coordinates Each. A United States map marks Mountain View at roughly 37 north, 122 west; Dallas at 33 north, 97 west; and New York City at 41 north, 74 west.](vector-space-1-cities.jpg)

Someone hands you two sets of coordinates. For each position, which of the three cities is closest?

- **38 N, 120 W**
- **40 N, 76 W**

![Use the Map to Find the Closest City. The same U.S. map shows cities as solid colored dots and new positions as filled dark orange diamonds with matching lines and white callout boxes outlined in dark orange. Dotted lines connect 38 north, 120 west to Mountain View and 40 north, 76 west to New York City, the nearest of the three cities.](vector-space-1-cities-closest.jpg)

The new coordinates don’t match any city exactly. But comparing positions lets you find the closest city.

## From Places to Meaning

These ratings for Coke, Pepsi, and coffee describe seven characteristics. Each drink gets a row of numbers called a **vector**.

![Three Drinks, Seven Dimensions Each. Coke, Pepsi, and coffee have colored number tiles on the same seven dimensions, rated from 0 to 10. Citrus is green and every score has equal emphasis. Coke and Pepsi have more similar profiles than either does to coffee.](vector-space-2-taste.jpg)

We can use these numbers as coordinates on a **map of similarities**. Coke and Pepsi have similar ratings, so their vectors sit close together. Coffee’s ratings are quite different, so its vector sits farther away.

![A Map of Drink Similarities. Coke and Pepsi are nearby points, with coffee farther from both. Each drink shows seven colored scores in this order: Sweet, Bitter, Fizz, Heat, Caffeine, Dark, Citrus. Coke: 9, 1, 10, 2, 3, 8, 1. Pepsi: 9, 1, 10, 2, 3, 8, 10. Coffee: 1, 9, 0, 9, 8, 10, 0. Dotted lines compare the gaps between positions.](vector-space-neighborhoods.jpg)

Now someone gives you the ratings for a mystery drink. They don’t match Coke, Pepsi, or coffee exactly. Just as you did with the cities, use the map to find the closest match.

- **9, 1, 10, 2, 3, 8, 9**

![Use the Map to Find the Closest Drink. The same map keeps Coke, Pepsi, coffee, and their scores in place. A new mystery point with ratings 9, 1, 10, 2, 3, 8, 9 sits close to Pepsi, joined by a short purple dotted line. Its first six scores match Pepsi, and its Citrus score is 9 compared with Pepsi’s 10. The mystery drink’s ratings are closest to Pepsi’s.](vector-space-closest-drink.jpg)

## Distance

The mystery drink’s first six scores match Pepsi’s. Only Citrus differs: 9 instead of 10, a gap of just 1. Compared with Coke, the Citrus gap is 8. That puts the mystery drink closer to Pepsi.

This is the idea behind **distance**: compare the numbers in matching positions across the vectors. Smaller gaps mean closer positions.

AI uses this idea on a much larger scale. Its embeddings have thousands of dimensions, with values learned during training. Similar meanings usually occupy nearby positions in vector space.

## When the Numbers Change

In AI, the layers change the numbers to reflect a word’s meaning in a specific sentence. Let’s see how this works in vector space:

<div style="background: #fff; border: 1px solid #d8cff2; border-left: 4px solid #4f2fc4; border-radius: 12px; padding: 16px 20px; margin: 8px 0 24px;">
  <div style="color: #4f2fc4; font-size: 13px; font-weight: 800; margin-bottom: 10px;">THE SENTENCE</div>
  <p style="color: #3d3752; font-size: 17px; line-height: 2.3; margin: 0;">“The <strong style="display: inline-flex; align-items: center; justify-content: center; width: 2.5em; height: 2.5em; border-radius: 50%; background: #0e8f86; color: #fff; font-size: 0.9em; line-height: 1; vertical-align: middle;">CAT</strong> sat on the mat during the May rainstorm because <strong style="display: inline-flex; align-items: center; justify-content: center; width: 2.2em; height: 1.55em; border-radius: 0.4em; background: #1652f0; color: #fff; line-height: 1; vertical-align: middle;">IT</strong> was tired.”</p>
</div>

On its own, <strong style="display: inline-flex; align-items: center; justify-content: center; width: 2.2em; height: 1.55em; border-radius: 0.4em; background: #1652f0; color: #fff; font-size: 0.82em; line-height: 1; vertical-align: middle;">IT</strong> could refer to many things. As the layers process this sentence, they update <span style="white-space: nowrap;"><strong style="display: inline-flex; align-items: center; justify-content: center; width: 2.2em; height: 1.55em; border-radius: 0.4em; background: #1652f0; color: #fff; font-size: 0.82em; line-height: 1; vertical-align: middle;">IT</strong>’s</span> numbers to carry information connecting it to <strong style="display: inline-flex; align-items: center; justify-content: center; width: 2.4em; height: 2.4em; border-radius: 50%; background: #0e8f86; color: #fff; font-size: 0.68em; line-height: 1; vertical-align: middle;">CAT</strong>. Changing those numbers also changes its position in **vector space**.

![How Context Changes IT’s Position. A realistic tabletop meaning map shows a blue IT marker following a purple path through three intermediate points toward a ragdoll cat. The animal neighborhood also contains a dog, kitten, and pet bowl. Adjoining object and weather neighborhoods contain a mat, chair, cloud, and rainstorm. Starting numbers [.12, −.34, …] change to [.41, .06, …]. The separate IT marker ends near CAT, illustrating their contextual connection. Takeaway: IT’s new position reflects its connection to CAT in this sentence.](vector-space-4-meaning-map.jpg)

Meaning is a position in vector space.

Similar meanings usually sit close together.
