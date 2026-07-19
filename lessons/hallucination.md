## AVOID TRAPS

# Hallucination

**AI can make mistakes. Check important information.**

That’s the warning under every chat box you’ve ever used. Wait a second. For something this powerful, it makes mistakes? Yes. And you already know the reasons why:

- Training taught it patterns, not facts.
- It builds answers one token at a time, picking each token by probability.
The combination causes the problem: **probable doesn’t always mean true.**

Sometimes AI gives you a false claim delivered in the same confident voice it uses for real facts. That confident-but-wrong claim is called a **hallucination**.

## A Famous Hallucination

This actually happened. When searchers asked Google “how do I keep cheese from sliding off my pizza,” the AI suggested mixing about one-eighth of a cup of non-toxic glue into the sauce. And some people actually tried it.

AI didn’t invent this answer. It traced back to an old joke on Reddit that the AI read as sincere advice. And that’s the two reasons above in action: the model works in patterns and probability. It can often spot a joke, but only when the joke looks like one. But this one didn’t look like a joke. It was written as sincere advice.

## What counts as a hallucination?

Not every wrong answer is a hallucination. These are the four patterns to watch for.

📚 **Fake source** A study, article, author, journal, or citation that does not exist.

🔢 **Fake detail** A real person, place, event, or idea with invented dates, numbers, quotes, or specifics.

🧩 **Blended fact** Real facts combined in a way that creates a conclusion that is false.

🔀 **Misread source** The source is real, but the model read it wrong.

## Retrieval-Augmented Generation

The industry’s workaround is **RAG** (Retrieval-Augmented Generation). For factual questions, modern chatbots search the web and write the answer from the real documents they find. It’s why hallucinations are rarer than they used to be.

But rarer isn’t zero. Even the big three don’t search for every answer, plenty still come straight from the model’s memory, and the glue-on-pizza advice happened with RAG on.

Probable isn’t true.

And it sounds the same when it’s wrong.
