## UNDERSTAND AI

# Training

You’ve seen the word **training** come up again and again throughout this course. It’s how OpenAI, Anthropic, and Google build AI: the same guess, check, and nudge loop you saw back in How an LLM Works.

![The training loop: Guess, the model produces an answer. Check, the model compares its guess to the correct answer, or a person evaluates it. Nudge, adjust the model’s internal numbers. Repeat. Same loop, different lessons.](training-loop-editorial.jpg)

Training happens in three phases, but it can’t start cold. Think of a basketball coach: before the first practice, they need a court and equipment, and a plan for what the team will actually work on. AI needs the same setup.

![Before training starts: Engineers set up the model’s vocabulary, dimensions, layers, and architecture. Teams gather books, websites, conversations, code, images, audio, and video as its curriculum.](training-before-starts-editorial.jpg)

## THREE PHASES OF TRAINING

Now, AI is ready to learn. The first phase is called “Pretraining.” Don’t let the name fool you. The “pre” just means it comes before the phases where humans teach it directly. You’ll also see how the model answers the same question at each phase: “How do I shoot a basketball?”

![Pretraining: The model reads enormous amounts of data, guesses that peanut butter goes with cloud, corrects the answer to jelly, and learns patterns in its weights. It does not yet know it is in a conversation.](training-pretraining-editorial.jpg)

![Instruction tuning: Human-written examples teach the model to answer questions directly. It can give concise basketball instructions but does not yet know what makes one answer feel better than another.](training-instruction-tuning-editorial.jpg)

![Preference tuning: People rank several AI answers and training nudges the model toward the preferred responses. The model becomes fluent and likable, but still does not know whether an answer is true.](training-preference-tuning-editorial.jpg)

![Training is finished: Pretraining data, instruction examples, and human preference rankings feed a completed model that is sealed as a snapshot.](training-finished-editorial.jpg)

When training is finished, the core model becomes a kind of snapshot. It has learned patterns from the data it saw up to a certain point. That is why models can have **knowledge cutoffs**. They can add live search, files, memory, or tools, but the core model is finished learning.

AI learned patterns, not facts.

Fluency comes free. Being right doesn’t.
