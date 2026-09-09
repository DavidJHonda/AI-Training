## UNDERSTAND AI

# Training

AI can explain chemistry, write code, and help you improve an essay. How did it learn to do those things?

Think about learning to shoot a basketball. You take a shot, check where it goes, and adjust your aim or how much force you use. AI training follows a similar pattern: guess, check, and adjust. But instead of adjusting aim or force, training adjusts the numbers inside the model to help it make a better guess next time.

### Board 1: The Training Loop

**Image file:** `training-loop-editorial.jpg`

![The Training Loop](training-loop-editorial.jpg)

**Teaching content:**

**Training example:** “Peanut butter and jelly.”

1. **Guess:** Given “Peanut butter and ___,” the model guesses “cloud.”
2. **Check:** The example says “jelly.” Compare the guess with that word.
3. **Adjust:** Adjust the model’s internal numbers to make “jelly” more likely in this situation.

**Takeaway:** Repeat with more examples. The patterns build.

Before training begins, engineers set up the model and gather the data.

### Board 2: Before Training Starts

**Image file:** `training-before-starts-editorial.jpg`

![Before Training Starts](training-before-starts-editorial.jpg)

**Teaching content:**

**Set Up the System:** Engineers design the model and give its internal numbers starting values. Training will adjust those numbers as the model learns.

**Gather the Data:** Teams collect books, websites, conversations, code, images, audio, and video. This becomes the curriculum.

## THREE PHASES OF TRAINING

Training has different jobs: learning patterns from data, learning how to answer questions, and improving responses through feedback. We’ll follow three main stages and watch how each shapes the answer to the same question: ‘How do I shoot a basketball?’

### Board 3: 1 · Pretraining

**Image file:** `training-pretraining-editorial.jpg`

![1 · Pretraining](training-pretraining-editorial.jpg)

**Teaching content:**

**Learn from Vast Amounts of Data:** More than you could read in 1,000 lifetimes.

The model guesses what comes next in vast amounts of text and code, then checks its guess against the example. Training adjusts its internal numbers, called **weights**. Across many examples, it learns patterns that help it write sentences, explain ideas, and produce code.

**What an Answer Might Look Like:**

“The basketball shot is one of the most fundamental skills in the sport. In this guide, we will cover...”

**What Still Needs Work:** The model can produce fluent text, but it doesn’t reliably follow your instructions yet.

### Board 4: 2 · Instruction Tuning

**Image file:** `training-instruction-tuning-editorial.jpg`

![2 · Instruction Tuning](training-instruction-tuning-editorial.jpg)

**Teaching content:**

**Learn to Follow Instructions:** People provide questions paired with helpful example answers. The model practices answering those questions, comparing its guesses with the examples. Training adjusts its weights so its answers become more like those examples.

**What an Answer Might Look Like:**

“To shoot a basketball, square your feet to the hoop, bend your knees, and push up, releasing off your fingertips with a follow-through.”

**What Still Needs Work:** The model can follow a request, but its answer may still be unclear, incomplete, or unhelpful.

### Board 5: 3 · Preference Tuning

**Image file:** `training-preference-tuning-editorial.jpg`

![3 · Preference Tuning](training-preference-tuning-editorial.jpg)

**Teaching content:**

**Learn from Feedback:** People provide a question, and the model produces several answers. People compare the answers and select the one they think is best, looking for clear, useful, and accurate information. Training adjusts the model’s weights to make answers like the selected one more likely.

**What an Answer Might Look Like:**

“Great question! Start close to the hoop. Use one hand to shoot and the other to steady the ball. Bend your knees, then push up as you shoot. Finish with your wrist bent and your fingers pointing toward the hoop. Practice from the same spot before moving farther away.”

**What Still Needs Work:** Feedback helps improve the answers, but AI can still give a wrong answer that sounds right.

When training ends, the model is ready to use. During a normal chat, it uses the weights that training produced. It can work with new information you give it, but your conversation does not change those weights.

## Closing Message

AI learns from examples and feedback.

Guess. Check. Adjust. Repeat.
