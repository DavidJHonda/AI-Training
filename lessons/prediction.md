## UNDERSTAND AI

# Prediction

You just watched a token’s final vector land in its neighborhood on the map. In Vector Space, that landing was about meaning: the model understanding the words you put in. Prediction is the flip side, the output: it takes the position at the end of your text and turns it into the next word.

## The ranked list

The model doesn’t just grab the single closest token. It compares that final position against **every** possible next token, scoring each by how closely the two line up on the map. Then it ranks them by probability: the best fit on top, and a long tail of less likely options below.

Then it takes one, almost always from the top, adds it to the text, and runs the whole thing again for the token after that. That pick has a name: **prediction**. Score every possible next token, choose one, then repeat.

How prediction works in the sentence “See you _______”

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

## One dial on the pick: temperature

There’s a control on how boldly the model commits to the top of that ranked list: **temperature**.

Temperature changes how predictable or surprising the model is when choosing words. Low temperature makes answers more repeatable. High temperature makes them more varied, creative, and sometimes weird. The middle is the balanced default, best for everyday writing.

Here’s that same ranked list for “See you ___”. The middle column is the default you just saw; see how the odds shift as temperature rises and falls. The exact numbers are illustrative, and temperature isn’t the only sampling control.

How temperature reshapes the picks

❄️ Low

⚖️ Medium

🔥 High

tomorrow

94%

65%

40%

later

2%

20%

28%

soon

1%

10%

17%

there

1%

3%

7%

again

1%

1%

4%

other words

1%

1%

4%

You probably won’t see this dial in regular ChatGPT, Claude, or Gemini. The app usually picks the temperature for you. But the idea still matters: you can ask for the effect instead, requesting “your best single answer” for consistency or “ten different options” for range.

## What temperature is not

Low temperature means repeatable, not correct. A low-temp model will confidently repeat the same wrong answer. Temperature controls variation, not accuracy.
