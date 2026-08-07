## UNDERSTAND AI

# Vector Space

In the last lesson, you watched a token move through the layers, its numbers changing at every step. In theory, AI could look up those finished numbers in its full table of token embeddings and see which token they match. **But it can’t: the transformed numbers are one of a kind, lining up with no token in the table.**

So how does AI work out what the token means, when its vector matches nothing on file? It finds the closest match. That sounds simple, but there’s more to it.

## AI uses a map (kind of)

A regular map works like this. You can find any place by knowing two things: the latitude and the longitude. Want to find Dallas, Texas? Just give it a north latitude of 33 and a west longitude of 97.

Dallas, Texas

33 N, 97 W

But what if we want to find New York City and Mountain View, California? No worries. They track the same dimensions.

New York City

41 N, 74 W

Mountain View, CA

37 N, 122 W

Dallas, Texas

33 N, 97 W

Now turn it around. Say all you have is those two numbers for each city. If I give you 38 N and 120 W, could you tell which city it’s closest to? You could: Mountain View. What about 39 N and 70 W? Of course, New York City.

Notice what you just did there. Neither of those pairs is a city. They’re just positions, matching nothing on file. You found the closest one anyway.

## How AI does it

In the Embeddings lesson, you learned how meaning is represented by values crossed against thousands of dimensions. You saw a simple example of Coke vs. Pepsi vs. Coffee.

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

Notice how Coke and Pepsi’s vectors (their rows of numbers) sit much closer to each other than either does to Coffee. If this was a map, it might look like this.

## Sweet · Bitter · Fizz · Heat · Caffeine · Dark · Citrus

## Soft drinks neighborhood

SWE

BIT

FIZ

HEA

CAF

DAR

CIT

🥤Coke

9

1

10

2

3

8

1

🥤Pepsi

9

1

10

2

3

8

10

## Sports and energy neighborhood

SWE

BIT

FIZ

HEA

CAF

DAR

CIT

Gatorade

7

1

0

1

0

1

6

Powerade

7

1

0

1

0

1

5

## Juices neighborhood

SWE

BIT

FIZ

HEA

CAF

DAR

CIT

lemonade

8

1

0

1

0

0

10

orange juice

7

1

0

1

0

1

10

## Hot drinks neighborhood

SWE

BIT

FIZ

HEA

CAF

DAR

CIT

☕Coffee

1

9

0

9

8

10

0

espresso

0

10

0

9

10

10

0

On the map, Coke and Pepsi sit side by side in the Soft drinks neighborhood. Coffee is all the way across, in the Hot drinks neighborhood.

Now ask the same question you just answered with cities. If the numbers were 9, 1, 10, 2, 3, 8, 9, which drink would that be closest to? A fizz of 10 puts it with the sodas, and a citrus of 9 puts it right beside Pepsi. It matches nothing on file exactly, and it does not have to.

## Distance

Here’s what you just did. Add up the gap between two sets of numbers across every dimension, and you get their **distance**. That is how AI measures closeness.

AI does the same thing, just on a massive scale. Every token carries thousands of dimensions, not seven, and AI learned every one of those values during training. And just like on our maps, tokens that mean similar things sit close together.

That closeness is no accident. Training nudged every token’s numbers until words used in similar ways ended up in similar places. So landing near a token is not a near miss. It is how the meaning gets read.

## Meaning is a position

Back to that one-of-a-kind token. AI can’t look its numbers up, but it can do what we just did with the drinks: read the token’s **position** on a map where similar meanings sit close together. That’s **vector space**.

Now, back to our sentence from the last lesson.

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

On its own, **IT** could have pointed at almost anything. As it flowed through the layers, its numbers kept moving toward **CAT**. By the end they matched no token exactly, but of every meaning AI knows, they sat closest to **CAT**.

In other words, AI has figured out that **IT** means the cat.

Meaning is a position.

Close in space is close in meaning.
