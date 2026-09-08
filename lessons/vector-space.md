## UNDERSTAND AI

# Vector Space

AI represents meaning with rows of numbers called **embeddings**. Each row is a **vector**. One way to understand these numbers is to think of them as coordinates on a map. Coordinates tell you a place’s position. Comparing two places’ positions tells you how close they are to each other.

## Start With a Familiar Map

A map uses two numbers to describe a place’s position: latitude and longitude. Dallas, Texas, is roughly 33° north, 97° west. New York City and Mountain View, California, have their own coordinates, using those same two dimensions.

Imagine these are the only three cities on our map.

![Three Cities, Two Coordinates Each. A United States map marks Mountain View at roughly 37 north, 122 west; Dallas at 33 north, 97 west; and New York City at 41 north, 74 west.](vector-space-1-cities.jpg)

Now try two new sets of coordinates. Which city is closest to each one?

- **38 N, 120 W**
- **39 N, 70 W**

![Find the Closest City. The same map now adds two purple outlined points. Dotted lines connect 38 north, 120 west to Mountain View and 39 north, 70 west to New York City, the nearest of the three cities.](vector-space-1-cities-closest.jpg)

The new coordinates don’t match any city exactly. But comparing positions lets you find the closest city.

## From Places to Meaning

Now imagine a map where positions describe characteristics instead of locations. These ratings for Coke, Pepsi, and coffee give each drink a row of numbers, its vector. Drinks with similar ratings sit closer together.

![Comparing Numerical Profiles. Coke, Pepsi, and coffee have colored number tiles on the same seven dimensions, rated from 0 to 10. Citrus is green and every score has equal emphasis. Coke and Pepsi have more similar profiles than either does to coffee.](vector-space-2-taste.jpg)

Coke and Pepsi have similar ratings, so their vectors sit close together. Coffee’s ratings are quite different, so its vector sits farther away. Let’s picture that as a map.

![Meaning Neighborhoods. Coke and Pepsi are nearby points, with coffee farther from both. Each drink shows seven colored scores in this order: Sweet, Bitter, Fizz, Heat, Caffeine, Dark, Citrus. Coke: 9, 1, 10, 2, 3, 8, 1. Pepsi: 9, 1, 10, 2, 3, 8, 10. Coffee: 1, 9, 0, 9, 8, 10, 0. Dotted lines compare the gaps between positions.](vector-space-neighborhoods.jpg)

Now try a new set of ratings. They don’t match any drink exactly. Which drink is closest?

- **9, 1, 10, 2, 3, 8, 9**? A fizz of 10 puts it with the sodas, and a citrus of 9 puts it right beside Pepsi. It doesn’t match anything on file exactly, and it doesn’t have to. You know it refers to Pepsi.

## Distance

Here’s what you just did. Add up the gap between two sets of numbers across every dimension, and you get their **distance**. That is how AI measures closeness.

Of course, AI does it on a massive scale. Every token carries thousands of dimensions, not seven, and AI learned every one of those values during training. And just like on our maps, tokens that mean similar things sit close together, so landing near a token is not a near miss. It is how the meaning gets read.

## Meaning is a position

Back to that one-of-a-kind token. AI can’t look its numbers up, but it can do what we just did with the drinks: read the token’s **position** on a map where similar meanings sit close together. That’s **vector space**.

Now, back to our sentence from the last lesson.

![The final vector for IT travels into the animal neighborhood and lands closest to CAT. KITTEN, DOG, and PET sit nearby, but CAT has the shortest distance.](vector-space-4-meaning-map.jpg)

Meaning is a position.

Close in space is close in meaning.
