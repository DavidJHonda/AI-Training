## UNDERSTAND AI

# One More Thing

One more thing. Actually, three more things. Across this section you built the whole machine: text becomes tokens, tokens become vectors, attention and the layers turn those vectors into meaning, and prediction reads the answer off a ranked list, one token at a time. But three facts about the machine never fit any single piece. They go here.

They’re worth the stop. Understand these three, and you’ll know more about what actually happens when you hit send than almost anyone who uses AI every day.

## Randomness

Start with a confession. In How AI Answers, we told you the model takes the top of the list and types it: Spot. We should have said **usually**. You’ve seen the evidence yourself: ask the exact same question in two brand-new chats, and the answers come back different. Same model, same question, same everything the model can see, and still two different replies.

Here’s the missing piece: the model doesn’t simply grab the top of its ranked list. It runs a weighted drawing across the whole list, where every token holds tickets equal to its probability. Spot, at 22%, holds 22 tickets out of 100. So Spot wins more drawings than any other single name. But with 78 tickets spread across everyone else, most drawings go to someone who isn’t Spot. Why run a drawing at all? Because text built from only the safest word at every step turns out repetitive and lifeless. The randomness is what keeps the writing from sounding robotic.

Same list, five draws

You could name him

Spot

22% · 22 tickets

Max

17% · 17 tickets

Buddy

14% · 14 tickets

Rex

9% · 9 tickets

Biscuit

6% · 6 tickets

other tokens

32% · 32 tickets

## Five draws, same tickets every time

1.

Max

2.

Spot

3.

Buddy

4.

Rex

5.

Max

Same odds every time. The favorite won just once.

That drawing is why two identical chats come back with two different replies. And once the first word differs, everything after it starts from a different context, so the replies don’t just differ by a word. They diverge.

## No memory

The second thing sounds like it can’t be true: **AI has no memory.** None. Let’s assume your question about naming your new dog came at the end of a long chat. You’d been debating whether to get a dog or a cat at all, brainstorming with AI, and after plenty of typing and reading, you settled on the dog. Then you asked: “What should I name my new dog?”

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

So here’s the arithmetic on the arithmetic. Nobody outside OpenAI knows how big ChatGPT’s model really is; the companies stopped publishing sizes. So let’s make an honest guess and call it one trillion weights. Each word takes roughly two calculations per weight: a multiply and an add. That’s about 2 trillion calculations before ChatGPT can type one word.

The Bill

## One word

Two calculations for each of a trillion weights

≈ 2 trillion

## One sentence

“You could name him Spot.” is 7 tokens

≈ 14 trillion

## Your complete chat about your new dog

2,000 words back and forth, about half of them typed by ChatGPT

≈ 2 quadrillion

The calculations required to name your dog Spot? 2 quadrillion.

2,000,000,000,000,000

And remember: no memory. The whole transcript gets re-read for every word. The longer the chat, the more the model re-reads before each new word, so the meter climbs faster as a conversation grows. You already know the advice this explains: long chats get slow, and starting a fresh chat for a new task isn’t tidiness. It’s engineering.

## Every time you hit send

So here’s the picture to leave this section with. Way back in AI is Math, we made a claim and asked you to take it on faith: AI isn’t a mind, it’s math. Now you’ve counted it. Every time you hit send, a warehouse of computers spins up, runs trillions of calculations for every word it types back, and throws the work away the moment the reply ends. Not a mind. Math, at a scale nobody can picture.

Somebody pays for all that arithmetic: in electricity, in water, and in money. We’ll count that bill later in the course, in The Hidden Cost.
