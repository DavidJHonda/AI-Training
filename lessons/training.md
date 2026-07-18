## UNDERSTAND AI

# Training

You’ve seen the word **training** come up again and again throughout this course. It’s how OpenAI, Anthropic, and Google build AI: the same guess, check, and nudge loop you saw back in How an LLM Works.

Training happens in three phases, but it can’t start cold. Think of a basketball coach: before the first practice, they need a court and equipment, and a plan for what the team will actually work on. AI needs the same setup.

0

Before training starts

👤Humans

Set up the system

Engineers set up the model’s architecture: the vocabulary of word-pieces it will read, the dimensions, the layers. You’ll meet each of these later in this section. Every internal number starts out random and means nothing yet.

Gather the data

Teams at the AI company collect huge amounts of training data: books, websites, conversations, and code, plus images, audio, or video for models that handle those. This becomes the model’s curriculum.

## THREE PHASES OF TRAINING

Now, AI is ready to learn. The first phase is called “Pretraining.” Don’t let the name fool you. The “pre” just means it comes before the phases where humans teach it directly. You’ll also see how the model answers the same question at each phase: “How do I shoot a basketball?”

1

Pretraining

🤖AI

The LLM grinds through the data and learns its broad patterns on its own. **It runs this loop billions of times.**

## 1 · Reads

📖 books

🌐 web

💬 chats

💻 code

more than you could read in 1,000 lifetimes

→

## 2 · Guesses

Peanut butter and __

cloud

✗

wrong → nudge the internal numbers

→

## 3 · Corrects

Peanut butter and __

jelly

✓

a little more accurate every pass

**What happened:**The model now has knowledge from learned patterns. It knows jelly follows “Peanut butter and,” and that star follows “Twinkle Twinkle Little.” Those patterns live in the model’s internal numbers, its **weights**.

**What it doesn’t know:**It doesn’t know it’s in a conversation.

🤖

## How it answers

“How do I shoot a basketball? The basketball shot is one of the most fundamental skills in the sport. In this guide, we will cover...”

2

Instruction tuning

👤Humans

Teach it to have conversations (Supervised Fine-Tuning)

Same loop, new curriculum: ideal conversations written by humans, each a question paired with a strong answer. The model reads the question and guesses the answer. Every pass nudges its guess toward the human’s.

**What happened:**The model now knows it’s in a conversation. Ask a question and it answers you directly instead of continuing your text.

**What it doesn’t know:**It doesn’t know what makes one answer feel better than another.

🤖

## How it answers

“To shoot a basketball, square your feet to the hoop, bend your knees, and push up, releasing off your fingertips with a follow-through.”

3

Preference tuning

👤Humans

Rank AI’s answers (RLHF)

This time, humans don’t write the answers. They ask a question, the model writes several answers, and reviewers rank them, best to worst. Every pass nudges the model toward answers like the winners. This is called RLHF (Reinforcement Learning from Human Feedback).

**What happened:**Training is complete. Human rankings gave the model a feel for which answers people prefer. The weights freeze, and the finished model is ready to meet you.

**What it doesn’t know:**It doesn’t know whether its answers are true. Training taught it to sound fluent, confident, and likable, and none of that guarantees an answer is right.

🤖

## How it answers

“Great question! The biggest thing beginners get wrong is using two hands to push the ball. Try this: flick your wrist like you’re reaching into a cookie jar on a high shelf. Want tips on free throws?”

When training is finished, the core model becomes a kind of snapshot. It has learned patterns from the data it saw up to a certain point. That is why models can have **knowledge cutoffs**. They can add live search, files, memory, or tools, but the core model is finished learning.

The finished model is a snapshot.

That’s why models have knowledge cutoffs.
