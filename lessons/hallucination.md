## AVOID TRAPS

# Hallucination

You have probably seen the warning: **AI can make mistakes. Check important information.** For something so amazing and powerful, AI makes mistakes?

Yes. And you’ve already learned 3 reasons **why**:

- AI learns patterns from data.
- It builds answers one word at a time.
- It picks words that fit the context and sound likely.
That creates the problem: **likely does not always mean true.**

That mismatch is the first trap of this section. AI can give you a claim that is false, unsupported, or outdated while saying it in the same confident voice it uses for true facts. **The trap is treating confidence like evidence.**

That confident-but-wrong claim is called a **hallucination**. The word is strange, because AI doesn’t have physical eyes and can’t "see" anything. But the idea is simple: AI presents a false or unsupported claim as if it were true. Sometimes it invents something completely. Sometimes it blends real facts with fake details. Sometimes it delivers outdated information with total confidence.

## WHAT COUNTS AS A HALLUCINATION?

Not every wrong answer is a hallucination. These are the four patterns to watch for.

Fake source

A study, article, author, quote, journal, or citation that does not exist.

Fake detail

A real person, place, event, or idea with invented dates, numbers, quotes, or specifics.

Blended fact

Real facts combined in a way that creates a conclusion that is false.

Stale claim

A claim that used to be true, or sounds current, but is now outdated.

## HOW THE INDUSTRY COUNTERACTS IT

Hallucinations come from how the model works. It picks likely-sounding words one at a time, and likely isn’t always true. That can’t be patched with a quick fix. So the industry built a workaround called **RAG** (Retrieval-Augmented Generation). For factual questions, modern chatbots search the web first, pull real documents, and write the answer using only what those documents say.

This is why hallucinations are rarer than they used to be. But the underlying issue is still there, not every tool uses RAG, and even RAG sometimes pulls weak sources. When one slips through, it looks just like everything else the model says. And search adds its own trap shape: instead of inventing a source, the model can misread a real one. The fix is the same either way. Check the source, not the confidence.

🔑 Probable is not the same as true. The same confident voice carries the real facts and the made-up ones. Verification is the skill.
