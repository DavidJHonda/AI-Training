## AVOID TRAPS

# Hallucination

**AI can make mistakes. Check important information.**

Wait a second. For something this powerful, it makes mistakes? And you already know the reasons why:

- Training taught it patterns, not facts.
- It builds answers one word at a time, picking each word by probability.
The combination causes the problem: **probable doesn’t always mean true.**

Sometimes AI gives you a false claim delivered in the same confident voice it uses for real facts. That confident-but-wrong claim is called a **hallucination**.

## A Famous Hallucination

This actually happened. When users asked Google “how do I keep cheese from sliding off my pizza,” the AI suggested mixing about an eighth of a cup of non-toxic glue into the sauce. And some people actually tried it! Yuck!

AI didn’t invent this answer. It traced back to an old joke on Reddit that the AI read as sincere advice. And that’s the two reasons above in action: the model works in patterns and probability, not meaning. It can often spot a joke, but only when the joke looks like one. This one was deadpan, written in the exact shape of real advice, so the patterns had nothing to catch. Text that looks like advice gets treated as advice.

## What counts as a hallucination?

Not every wrong answer is a hallucination. These are the four patterns to watch for.

📚

Fake source

A study, article, author, journal, or citation that does not exist.

🔢

Fake detail

A real person, place, event, or idea with invented dates, numbers, quotes, or specifics.

🧩

Blended fact

Real facts combined in a way that creates a conclusion that is false.

🔀

Misread source

The source is real, but the model read it wrong.

Hallucinations come from how the model works, so there’s no quick patch. The industry’s workaround is **RAG** (Retrieval-Augmented Generation): for factual questions, modern chatbots search the web first, pull real documents, and write the answer from what those documents say. It’s why hallucinations are rarer than they used to be.

But rarer isn’t zero. Not every tool uses RAG, and the glue-on-pizza advice happened with RAG on.

Probable isn’t true.

And it sounds the same when it’s wrong.
