## UNDERSTAND AI

# Prediction

In Vector Space, you watched a token’s final vector land in its neighborhood on the map. That landing was about meaning: the model understanding the words you put in. And Training turned all of that into a fluent sentence-completer, patterns at the ready. Everything so far has been the model learning and reading. Prediction is the first move of writing: it takes the position at the end of your text and turns it into the next word.

## The ranked list

Start with your phone. As you type a text, it suggests the next word: three chips above the keyboard, picked from the last word or two, the same for everyone.

See you ______.

soon

tomorrow

later

AI follows the same basic logic, but, as you might expect, it goes **way deeper**.

1. AI compares the final position of the last word in the chat so far against **every** possible next token (words or pieces of words), scoring each by how closely the two line up on the map.
2. Then it ranks them by probability: the best fit on top, and a long tail of less likely options below. It builds that list fresh every time, from everything in the chat and anything else in the context window, like personalization.
3. Then the model takes one, almost always from the top of the list, adds it to the text, and runs the whole thing again for the token after that.
Here’s what that looks like for a very simple sentence.

The same blank, three different chats: “See you ______”

## Chat 1

💬

You’re chatting about plans for Saturday night.

Saturday

58%

tonight

22%

there

9%

soon

6%

other words

5%

## Chat 2

💬

You’re chatting about plans for later today.

later

61%

soon

18%

tonight

12%

there

5%

other words

4%

## Chat 3

💬

You’re chatting about tomorrow’s BBQ-club meeting at school.

tomorrow

65%

later

20%

soon

10%

there

3%

again

1%

other words

1%

Three chats, three different lists. The odds come from everything the model can see.

The exact numbers are illustrative.

The pick has a name: **prediction**. Score every possible next token, choose one, then repeat.

And notice where those odds come from. Attention spent dozens of layers blending the whole chat into that final position, so the scores really do come from everything the model can see. It’s why the context window mattered so much back in Work With AI: control the context, and you’re steering the predictions themselves.
