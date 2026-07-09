## UNDERSTAND AI

# Transformer

When you type a message to ChatGPT, you type real words and it responds the same way. You’ve already learned what happens underneath: AI turns your text into tokens, and each token’s vector carries its meaning. If only it were that easy.

Here are two nuances in language that break this idea. In both, the word’s meaning isn’t clear until you read the words around it.

1

Different Meanings

Sometimes a word can mean different things. Look at the word **LIGHT** in these two sentences. It means something different in each, based on the words around it.

Please turn on the **LIGHT**.

The suitcase is **LIGHT** enough to carry.

See the problem? Which meaning of **LIGHT** should AI use?

2

Pronouns

Most words are unambiguous: cat means cat and milk means milk. But the sentence can still shift. Watch the word **IT** in these two sentences. We only change the last word.

The cat drank the milk because **IT** was **thirsty**.

The cat drank the milk because **IT** was **fresh**.

See the problem? What does **IT** point to: the cat or the milk?

## WHY THIS WAS HARD FOR AI

Our human brains see the right meaning instantly from the surrounding words. For AI, this was the big challenge, because of how it used to read text: in order, one word at a time. The further it read, the more the early words faded. Try it yourself with the sentence below. What does **IT** point to: cat, mat, May, or the rainstorm?

How AI used to read

The

→

cat

→

sat

→

on

→

the

→

mat

→

during

→

the

→

May

→

rainstorm

→

because

→

IT

→

was

→

tired

We instantly know **IT** points back to **CAT**, even ten words later. A computer reading strictly in order doesn’t, and that’s what kept old AI from reading like we do.

## THE BREAKTHROUGH

In 2017, eight researchers at Google published a paper called **Attention Is All You Need**. It introduced the **Transformer**, the architecture behind every modern LLM, and the “T” in ChatGPT. We’ll share the specific concepts next, but for now, let’s focus on the impact.

Instead of reading information sequentially, one word (token) at a time, the Transformer reads your whole message at once. That means it can establish the meaning of the word **IT** based on the words around it, like **CAT**, no matter how far apart they sit. And, it sees that the **CAT** is **TIRED**.

How AI reads now

The

CAT

sat

on

the

mat

during

the

May

rainstorm

because

IT

was

TIRED

## One catch: word order

Reading everything at once creates a problem reading-in-order never had. If all the tokens arrive together, what tells the model that “dog bites man” isn’t “man bites dog”? Same three tokens. Same three vectors. Only the order is different, and the order carries the meaning.

Same tokens. One difference.

dog#1

bites#2

man#3

man#1

bites#2

dog#3

Without the stamps, these two sentences would look identical to the model.

The fix happens before the first layer. Every token’s vector gets a **position stamp**: a second pattern of numbers mixed in that says “I’m token #1,” “I’m token #3.” Same word, different seat, slightly different numbers. Now the sentence can arrive all at once without losing its order. The order rides inside the vectors, and the proper name for the stamp is **positional encoding**.

Reading your whole message at once was only the start. To turn reading into meaning, AI has to do two things. First, figure out which other words matter. For **IT**, the words that matter are **CAT** and **TIRED**. Second, update **IT**’s vector to lock in the right meaning: the cat, not the mat, May, or the rainstorm.

Here are the two steps:

1

Attention

Which words matter?

CAT

IT

Reading **IT**, the model weighs every word and leans hardest on **CAT**.

→

2

Transformation

Update the meaning

IT (raw)

→

IT ≈ CAT

**IT**’s vector updates to mean **CAT**.

Now let’s answer the two questions we left open.

1

Different Meanings

Please turn on the **LIGHT**.

The suitcase is **LIGHT** enough to carry.

**Attention:** **LIGHT** links to “turn on” in the first sentence, to “carry” in the second.

**Transformation:**It sets **LIGHT**’s meaning: brightness in one, not-heavy in the other.

2

Pronouns

The cat drank the milk because **IT** was **thirsty**.

The cat drank the milk because **IT** was **fresh**.

**Attention:**“Thirsty” links **IT** to the cat; “fresh” links **IT** to the milk.

**Transformation:**It sets **IT**’s meaning: the cat in one sentence, the milk in the other.

And it goes beyond these examples. Sarcasm, idioms, even an “it” that points to nothing at all (“it was a cold day”): every nuance in language gets resolved the same way, by weighing all the words around it. That’s why eight researchers dared to put such a bold claim in their title. **Attention is all you need.**
