## UNDERSTAND AI

# Training

You’ve seen the word **training** come up again and again throughout this course. It’s how OpenAI, Anthropic, and Google build AI: the same guess, check, and nudge loop you saw back in How an LLM Works.

Training runs billions of times over mountains of data. It’s also where every number you’ve been watching gets set: the embedding table, attention, the weights in every layer. This lesson is the deep dive, where you finally see how it actually happens.

When training is finished, the core model becomes a kind of snapshot. It has learned patterns from the data it saw up to a certain point. That is why models can have **knowledge cutoffs**. They can add live search, files, memory, or tools, but the core model is finished learning. So when your app “knows” last night’s Stars score, that isn’t the frozen model: the app ran a web search and read the results into the context window.

## HOW AI IS TRAINED

Here’s an outline of the training process.

Before training starts

👤Humans

Set up the system

Engineers set up the architecture you’ve already seen: the token vocabulary, the dimensions, the layers. Every token starts with a random vector that means nothing yet. Training is what fills those with meaning.

👤Humans

Gather the data

Teams at the AI company collect huge amounts of training data: books, websites, conversations, and code, plus images, audio, or video for models that handle those. Most of it is messy and unstructured. This becomes the model’s curriculum.

Phase 1 · Pretraining

The name is confusing. This is real training, not a warm-up: the model grinds through that data and learns its broad patterns on its own. The “pre” just means it comes before the phases where humans step in to teach it directly.

🤖AI

One loop runs, over and over

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

Repeat that loop billions of times, and that’s the heart of training. Each pass nudges the model’s internal numbers, its **weights** (also called its parameters), a little closer to right. The next two phases run this same loop. What changes is that humans check the answers.

Phase 2 · Instruction tuning

👤Humans

Teach it to have conversations (Supervised Fine-Tuning)

Humans write examples of ideal conversations: a question paired with a strong answer, repeated across many topics. The model studies them and learns to respond helpfully instead of just continuing text.

Phase 3 · Preference tuning

Nudges it toward better answers.

👤Humans

Rank AI’s answers (RLHF)

The model writes multiple answers to the same prompt, and human reviewers rank which are best: this one is helpful, that one misses the point. Over thousands of rankings, the model gets nudged toward more helpful, honest, and safe answers. RLHF (Reinforcement Learning from Human Feedback) is one common version of this.

Watch It Happen

## You

How do I shoot a basketball?

After Pretraining (the base model): It can produce fluent text, but it doesn’t know it’s talking to a person. It just continues the sentence.

How do I shoot a basketball? The basketball shot is one of the most fundamental skills in the sport. In this guide, we will cover the basics of shooting form, including stance, grip, and follow-through...

After Instruction tuning (Supervised Fine-Tuning): Example conversations taught it to answer the person directly instead of just continuing the text. Helpful now, but still a little flat.

To shoot a basketball, square your feet to the hoop, put your shooting hand under the ball with your guide hand on the side, bend your knees, and push up, releasing off your fingertips with a follow-through.

After Preference tuning (RLHF): Human rankings taught it to be engaging, use analogies, and offer follow-up. This is what you experience today.

Great question! The biggest thing beginners get wrong is using two hands to push the ball. Try this: elbow under the ball, flick your wrist like you’re reaching into a cookie jar on a high shelf. Want tips on free throws vs three-pointers?

## The takeaway

Fluent came first. Helpful was taught.

By the base-model stage, the model could already produce fluent text about basketball. It took human examples and rankings to turn a sentence-completer into something that answers you: engaging, useful, and ready with a follow-up.
