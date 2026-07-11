## UNDERSTAND AI

# One More Thing

One more thing. Actually, three more things. Across this section you built the whole machine: text becomes tokens, tokens become vectors, attention and the layers turn those vectors into meaning, and prediction reads the answer off a ranked list, one token at a time. But three facts about the machine never fit any single piece. They go here.

They’re worth the stop. Understand these three, and you’ll know more about what actually happens when you hit send than almost anyone who uses AI every day.

## Temperature

Start with a confession. In How AI Answers, we told you the model takes the top of the list and types it: Spot. We should have said **usually**. You’ve seen the evidence yourself: ask the exact same question in two brand-new chats, and the answers come back different. Same model, same question, same everything the model can see, and still two different replies.

Here’s the missing piece: the model doesn’t simply grab the top of its ranked list. It runs a weighted drawing across the whole list, where every token holds tickets equal to its probability. Spot, at 22%, holds 22 tickets out of 100. So Spot usually wins, but Max wins his share of drawings too. That drawing is why two identical chats come back with two different replies.

**Temperature** is the dial on that drawing. Low temperature hands the top pick nearly every ticket, so answers become repeatable. High temperature spreads tickets far down the list, so answers get more varied, creative, and sometimes weird. The middle is the balanced default, best for everyday writing.

Here’s the name slot from last lesson at three settings. The middle column is the balanced list you already know; watch the odds sharpen and flatten as the dial moves. And keep an eye on Beowulf: impossible at low, alive at high. Temperature isn’t the only sampling control, but it’s the one worth knowing.

How temperature reshapes the picks

You could name him

❄️ Low

⚖️ Medium

🔥 High

Spot

58%

22%

13%

Max

19%

17%

12%

Buddy

10%

14%

11%

Rex

5%

9%

9%

Biscuit

2%

6%

8%

Beowulf

0%

3%

6%

other tokens

6%

29%

41%

You won’t see this dial in ChatGPT, Claude, or Gemini. The apps set the temperature for you; the dial itself lives in the tools developers use to build on these models. But the idea still matters, because you can ask for the effect instead: request “your best single answer” for consistency, or “ten different options” for range.

## No memory

The second thing sounds like it can’t be true: **AI has no memory.** None. To see it, go back to the prompt about naming your new dog, and imagine it came at the end of a longer chat. You’d been debating whether to get a dog or a cat at all, brainstorming with AI, and after plenty of typing and reading, you settled on the dog. Then you asked: “What should I name my new dog?”

Here’s what happened each time you typed a message. AI ran **everything**, all your messages and its own responses, through the full process: tokens, positions, attention and transformation through the layers. Think about it like this: every word of the chat is written on one long transcript, and AI re-reads the full transcript every time you send a message.

## TWO SIDES OF THE SAME CHAT

🧠

## You

#### You carry the chat in your head

You remember deciding on a dog over a cat, and why.

You remember what you typed ten seconds ago.

You’d recognize your own last sentence anywhere.

You reply from memory.

📄

## AI

#### AI carries nothing

It remembers nothing, not even the reply it’s in the middle of writing.

Everything lives in the transcript: your messages, its replies, all of it.

Before every word, it re-reads the whole transcript, in milliseconds.

So you never notice. The chat just flows.

AI really doesn’t have a memory. And it goes further: it doesn’t even remember the last word it typed. Before every word, the model re-reads everything it can see: your question, its own reply so far, and the rest of the context window too. Personalization, saved memory, everything earlier in the chat. All of it, tokenized, embedded, and pushed through every layer, for every single word. The transcript is the memory.

## The scale of the math

Now count what that costs. The calculations aren’t a mystery. They’re the **weights** you met in Layers and Training, frozen since training day, multiplying the numbers that pass through them. Inference just runs them forward: the same machine, the same arithmetic, every time you ask.

So here’s the arithmetic on the arithmetic. A mid-size open model carries about 70 billion weights, and each token takes roughly two calculations per weight. That’s about 140 billion calculations before the model can type one word. (Frontier models are bigger. The companies don’t say how much bigger.)

## The bill

## Calculations

One word

Two calculations for each of 70 billion weights

140 billion

One sentence

“You could name him Spot.” is 7 tokens

≈ 1 trillion

One homework answer

A full reply runs about 300 tokens

≈ 42 trillion

Every calculation done fresh, nothing saved. And this is one question, from one student.

And remember: no memory. The whole transcript gets re-read for every word. The longer the chat, the more the model re-reads before each new word, so the meter climbs faster as a conversation grows. You already know the advice this explains: long chats get slow, and starting a fresh chat for a new task isn’t tidiness. It’s engineering.

## Every time you hit send

So here’s the picture to leave this section with. Way back in AI is Math, we made a claim and asked you to take it on faith: AI isn’t a mind, it’s math. Now you’ve counted it. Every time you hit send, a warehouse of computers spins up, runs hundreds of billions of calculations for every word it types back, and throws the work away the moment the reply ends. Not a mind. Math, at a scale nobody can picture.

Somebody pays for all that arithmetic: in electricity, in water, and in money. We’ll count that bill later in the course, in The Hidden Cost.

## LOCK IN THE PIECES

You’ve now seen every piece, and what it costs to run them. One last checkpoint to lock the section in.
