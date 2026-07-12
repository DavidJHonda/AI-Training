## UNDERSTAND AI

# Vector Space

In the last lesson, you watched a token move through the layers, its numbers changing at every step. And you left with a blank box: where do **IT**’s numbers finally land?

In theory, the model could look up those finished numbers in its full table of token embeddings and see which token they match. But it can’t: the transformed numbers are one of a kind, lining up with no token in the table.

## The problem

So how does AI work out what the token means, when its vector matches nothing on file?

To see the answer, go back to the taste test from Embeddings, where Pepsi looked almost exactly like Coke until a Citrus dimension finally told them apart.

Taste Profile · Coke vs. Pepsi vs. Coffee

## Dimensions

## Token

## Token ID

## Sweet

## Bitter

## Fizz

## Heat

## Caffeine

## Dark

## Citrus

🥤Coke

24317

9

1

10

2

3

8

1

🥤Pepsi

38106

9

1

10

2

3

8

10

☕Coffee

51820

1

9

0

9

8

10

0

Notice how Coke and Pepsi’s vectors (their rows of numbers) sit much closer to each other than either does to Coffee.

This matters for AI. The model measures closeness with **distance**: how far apart two vectors are when you add up the gap in every dimension. The model has established that Coke is more like Pepsi than like Coffee.

## Meaning is a position

Back to that one-of-a-kind token. The model can’t look its numbers up, but it can do what we just did with the drinks: read the token’s **position**. That’s the idea of **vector space**: a map where every vector sits somewhere, and similar words share a neighborhood.

Time to fill in the blank box. As **IT** flowed through the layers, its numbers kept moving toward **CAT**. Never an exact match, but closer to **CAT** than to any other word in the sentence.

The

cat

sat

on

the

mat

during

the

May

rainstorm

because

it

was

tired

## Ambiguous “it”

On its own, **IT** is just a pronoun. Its vector could mean almost anything, and certainly not **CAT**.

→

## Through the layers

Each layer reads the surrounding words and shifts the numbers for **IT**. Layer by layer, the model works out what **IT** refers to.

→

## Lands by “cat”

In vector space, the final numbers for **IT** land closer to **CAT** than to any other word in the sentence.

In other words, the model has figured out that **IT** means the cat.

## It’s not just pronouns

The pronoun **IT** was an easy case to watch, but this isn’t special to ambiguous words. Every token gets rewritten by the ones around it, even a plain, concrete noun. Watch the word **airplane** in two different sentences.

She

folded

a

paper

airplane

and

sailed

it

across

the

room

## Nearby on the map

paper

fold

toy

glide

The

airplane

roared

down

the

runway

and

lifted

into

the

sky

## Nearby on the map

jet

runway

pilot

flight

Same word, same starting vector. But *paper*, *folded*, and *room* pull it one way, while *runway*, *roared*, and *sky* pull it the other. It isn’t one keyword flipping a switch: the final vector is the **blend of the whole sentence**. Change the words around it, and the same token lands somewhere new.

🔑 A machine that predicts your next move isn’t reading your mind. It’s counting your habits.

Meaning is a position.

The final vector is the blend of the whole sentence.
