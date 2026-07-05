## UNDERSTAND AI

# Training

You’ve seen the word **training** come up again and again throughout this course. It’s how a company builds AI: the same guess, check, and nudge loop you saw back in How an LLM Works. It runs billions of times over mountains of data. It’s also where the odds you just watched the model pick from get set in the first place. This lesson is the deep dive, where you finally see how it actually happens.

When training is finished, the core model becomes a kind of snapshot. It has learned patterns from the data it saw up to a certain point. That is why models can have **knowledge cutoffs**. They can add live search, files, memory, or tools, but the core model is finished learning.

## HOW AI IS TRAINED

Training happens in three phases, each building on the one before.

Phase 1 · Pretraining

Teaches the model broad patterns from massive data.

👤Humans

Set up the system

Engineers set up the architecture you’ve already seen: the token vocabulary, the dimensions, the layers. Every token starts with a random vector that means nothing yet. Training is what fills those with meaning.

👤Humans

Gather the data

Teams at the AI company collect huge amounts of training data: books, websites, conversations, and code, plus images, audio, or video for models that handle those. Most of it is messy and unstructured. This becomes the model’s curriculum.

🤖AI

Then one loop runs, over and over

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

Repeat that loop billions of times, and that’s training. Each pass nudges the model’s internal numbers, its **weights** (also called its parameters), a little closer to right.

Phase 2 · Instruction tuning

Teaches it to follow instructions and answer your questions.

👤Humans

Teach it to have conversations (SFT)

Humans write examples of ideal conversations: a question paired with a strong answer, repeated across many topics. The model studies them and learns to respond helpfully instead of just continuing text. This step is called Supervised Fine-Tuning.

Phase 3 · Preference tuning

Nudges it toward better answers.

👤Humans

Rank AI’s answers (RLHF)

The model writes multiple answers to the same prompt, and human reviewers rank which are best: this one is helpful, that one misses the point. Over thousands of rankings, the model gets nudged toward more helpful, honest, and safe answers. RLHF (Reinforcement Learning from Human Feedback) is one common version of this.

## HOW DOES THE APP KNOW YESTERDAY’S SCORE?

Last night there was a great game between the Dallas Stars and the New York Rangers, and you missed it. You ask your AI app for the score, and it “knows” the result. It even tells you one of the Stars got a hat trick.

That should feel contradictory. The model is frozen once training ends, with a knowledge cutoff from before the puck ever dropped. The model itself can’t know.

Here’s how it did it. The app, not the model, ran a web search, pulled the results into the context window, and answered from what it just read, often with links.

Watch It Happen

## You

How do I shoot a basketball?

After Pretraining (the base model): It can produce fluent text, but it doesn’t know it’s talking to a person. It just continues the sentence.

How do I shoot a basketball? The basketball shot is one of the most fundamental skills in the sport. In this guide, we will cover the basics of shooting form, including stance, grip, and follow-through...

After Instruction tuning (SFT): Example conversations taught it to answer the person directly instead of just continuing the text. Helpful now, but still a little flat.

To shoot a basketball, square your feet to the hoop, put your shooting hand under the ball with your guide hand on the side, bend your knees, and push up, releasing off your fingertips with a follow-through.

After Preference tuning (RLHF): Human rankings taught it to be engaging, use analogies, and offer follow-up. This is what you experience today.

Great question! The biggest thing beginners get wrong is using two hands to push the ball. Try this: elbow under the ball, flick your wrist like you’re reaching into a cookie jar on a high shelf. Want tips on free throws vs three-pointers?

## The takeaway

Fluent came first. Helpful was taught.

By the base-model stage, the model could already produce fluent text about basketball. It took human examples and rankings to turn a sentence-completer into something that answers you: engaging, useful, and ready with a follow-up.
