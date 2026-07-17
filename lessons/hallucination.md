## AVOID TRAPS

# Hallucination

**AI can make mistakes. Check important information.**

Wait a second. For something this powerful, it makes mistakes?

Yes. And you already know the reasons why.

1. During Training, AI learns patterns from data.
2. It builds answers one word at a time, picking each word by probability.
That creates the problem: **likely does not always mean true.**

AI can give you a false claim delivered in the same confident voice it uses for real facts. That confident-but-wrong claim is called a **hallucination**. The word is strange, because AI doesn’t have physical eyes and can’t "see" anything. But the idea is simple: **AI presents a false or unsupported claim as if it were true**.

Sometimes it invents something completely. Sometimes it stitches true facts into a false conclusion. Sometimes it misreads a real source.

Some hallucinations get famous. When Google added AI Overviews to its search results, one answer went viral: asked how to keep cheese from sliding off pizza, the AI suggested mixing about an eighth of a cup of non-toxic glue into the sauce. (Some people actually tried it.) The answer wasn’t invented from nothing. It traced back to an old joke comment on Reddit that the AI read as sincere advice.

## WHAT COUNTS AS A HALLUCINATION?

Not every wrong answer is a hallucination. These are the four patterns to watch for.

Fake source

A study, article, author, journal, or citation that does not exist.

Fake detail

A real person, place, event, or idea with invented dates, numbers, quotes, or specifics.

Blended fact

Real facts combined in a way that creates a conclusion that is false.

Misread source

The source is real, but the model read it wrong. A joke taken as advice, a finding summarized backwards.

Hallucinations come from how the model works, so there’s no quick patch. The industry’s workaround is **RAG** (Retrieval-Augmented Generation): for factual questions, modern chatbots search the web first, pull real documents, and write the answer from what those documents say. It’s why hallucinations are rarer than they used to be.

But the underlying issue is still there. Not every tool uses RAG, and search adds its own trap shape: instead of inventing a source, the model can misread a real one. That’s what happened with the glue. The fix is the same either way: check the source, not the confidence.

🔑 Probable is not the same as true. The same confident voice carries the real facts and the made-up ones. Verification is the skill.

Probable isn’t true.

Confidence is a style, not a fact-check.
