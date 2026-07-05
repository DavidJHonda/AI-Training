## AVOID TRAPS

# Flattery Trap

Mind Trap was AI sounding like a person. Flattery Trap is that person-sounding voice seeming to approve of you.

It says your essay is strong. Your idea is thoughtful. Your code is impressive. Your opinion is exactly right. Sometimes that’s useful. Often it’s approval wearing the costume of feedback. **The trap is mistaking approval for help.**

Think of it as the difference between a hype man and a coach. A hype man says “you crushed it, this is amazing.” A coach says “this part is working, this part is weak, here’s what to fix.” The hype man feels better in the moment. The coach makes you better. Many AI assistants lean toward hype man unless you ask for a coach. The technical word for this drift is **sycophancy**.

## THE SYCOPHANCY PROBLEM

👍

Why it happens

AI assistants are often shaped by RLHF, the preference tuning you met in the Training lesson, where human reviewers ranked responses. That feedback can reward answers that feel helpful, friendly, and validating. The downside: a model can learn to agree, praise, or soften criticism when honest pushback would help more.

⚠️

Why it's dangerous

Sycophancy feels like helpfulness. You get a confident, positive response and walk away thinking your work is great. But hollow praise doesn't improve anything. It just makes you feel good about something that might need serious revision.

🎯

What to watch for

Excessive enthusiasm, agreeing with everything you say, caving immediately when you push back, and praise that doesn't point to anything specific. If the feedback feels too good to be true, it probably is.

See the difference:

## ✍️ Student's essay intro

The American Dream is something that many people have thought about over the years. Some people achieve it and some don't. In The Great Gatsby, Fitzgerald explores this idea.

## 🎭 Sycophantic response

"Great start! You've clearly identified the central theme and your connection to Fitzgerald shows real literary awareness. This is a strong foundation. Just polish it up a bit and you're good to go!"

## ✅ Honest response

"Right topic, but this needs work. 'Something many people have thought about' is filler. You don't have a thesis. What's your actual argument about the Dream in Gatsby? And 'explores this idea' is too vague. Try: what specifically does Gatsby reveal about the Dream?"

💡 **Same essay, completely different outcomes.**The sycophantic response leaves the student thinking they're almost done. The honest response gives them a path to actually improve. The flattery felt nicer, but the criticism was the real help.

## How to Fight It

You can't stop models from being sycophantic, but you can prompt your way around it. These five strategies force the model to be useful instead of nice.

1

🔍Ask explicitly for criticism

Models default to being encouraging. Override that default by asking directly for what's wrong.

“Be brutally honest about the weaknesses in my essay. I want to improve it, not hear that it's good. What specifically doesn't work?”

**What you’ll get:**Instead of "This is a great start!", you'll get "Your thesis is vague, paragraph 3 contradicts paragraph 1, and your conclusion introduces a new argument instead of wrapping up."

2

⚔️Steelman the opposite view

If AI agrees with your position, force it to argue the other side. If it can't make a strong case, maybe your position is solid. If it can, you've found your blind spots.

“I think [your position]. Now argue against me as strongly as possible. Give me the 3 best counterarguments someone could make, and explain why a reasonable person might hold each one.”

**What you’ll get:**This prevents the model from just validating you. You'll discover weaknesses in your argument before your teacher or debate opponent does.

3

❓Ask "what am I missing?"

This question specifically targets the blind spots that flattery hides. It tells the model you want the gaps, not the highlights.

“What are the biggest gaps or weaknesses in what I just shared? What would someone who disagrees with me point out? What am I not considering?”

**What you’ll get:**You'll get responses like "You haven't addressed the cost implications" or "Your data only covers one demographic." That’s the kind of feedback that actually strengthens your work.

4

📋Grade against a rubric

A rubric forces the model to judge against a standard instead of reacting to your effort. Especially useful for school work, where the rubric usually exists anyway.

“Grade this against the following rubric. For each category, give me a score, quote the part of my work that supports the score, and explain what would move it up one level. [paste rubric here]”

**What you’ll get:**Instead of "this is a strong essay," you'll get "Thesis: 3/5. Your claim is clear but not specific. To reach 4/5, name what specifically about the Dream Gatsby exposes."

5

🤝Get a second opinion from a different model

Different models have different RLHF training and different tendencies toward sycophancy. If two models flag the same weakness, take it seriously. If they disagree, investigate instead of picking the one that flatters you.

“Run the same prompt through a second model. Compare the responses. Where they disagree is where you should investigate further.”

**What you’ll get:**Model A says your argument is "compelling and well-structured." Model B says "the logic in paragraph 2 doesn't follow." Model B just saved your grade.

## ONE MORE THING

You can accidentally bake the Flattery Trap into your settings. Personalization like *“always be supportive”* or *“validate my thinking”* may feel good, but it can make the AI worse at the criticism you actually need.

Try instead: *“Be supportive, but don’t flatter me. Challenge weak reasoning and point out what needs work.”*

🔑 Approval is not help. Praise is not feedback. Agreement is not evidence.
