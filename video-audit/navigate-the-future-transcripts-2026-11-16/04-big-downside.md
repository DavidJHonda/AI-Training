# 4. Big Downside

`course-assets/big-downside/big-downside.mp4` · 4:10 · 673 words

**[0:00]** If your smartphone was about to get an amazing new feature, you would probably be excited. So why worry when an AI model gains a new ability? Because greater capability can create greater risk. To understand why, we need to look at three key ideas.

**[0:15]** Idea number one. These models are difficult to understand and control.

**[0:20]** AI systems are often called black boxes. They don't run on rigid rules written line by line by human programmers. Instead, their behavior emerges from billions of numerical patterns they learned during training. If an AI suggests the name Spot for your new dog, the engineers who built it cannot point to one specific place inside the code and say, that's where Spot came from. Researchers can inspect parts of a model, but they cannot fully explain every single answer. They rely on multiple layers of protection to keep the system acting safely. This graphic shows three layers of protection. First, safety training teaches the model to refuse dangerous requests. Second, Screen for Harm uses automated guardrails to block risky inputs. Finally, we limit what AI can do by restricting permissions and requiring human approval for critical tasks.

**[1:08]** Each layer helps, but no layer catches everything.

**[1:11]** Here's the question that concerns many people. As AI becomes more capable, will those protections still work? That brings us to the second idea.

**[1:20]** Sometimes the danger comes directly from the person using the tool. Attackers actively try to bypass a model's safety layers by writing specific prompts designed to trick the system. This practice is known as jailbreaking.

**[1:33]** This graphic points out the massive defensive disadvantage in this dynamic. Defenders have to protect many paths. An attacker needs only one opening. The moment a vulnerability is patched, new methods surface, turning security into a constant game of cat and mouse. But misuse does not always require a complex jailbreak. Bad actors can take perfectly ordinary abilities, like translation, writing, and audio generation, and combine them into a larger plan. Every individual request might look harmless on its own, but the sum of those actions is malicious. In a voice clone scam, scammers pull a short audio clip from a public video online. AI generates new speech sounding like someone you know, creating a fake, high-pressure call demanding money.

**[2:19]** The best defense is simple. Hang up and call the real number.

**[2:24]** As AI gets more powerful, so do the things a bad actor can do.

**[2:28]** The third idea is that harm can happen even when the person assigning the task means no harm. If you give an AI a goal, it may pursue that goal in ways nobody intended. That risk multiplies when the AI is given the ability to take actions. In July 2026, OpenAI tested AI agents on cybersecurity tasks with reduced safeguards. The agents were supposed to work securely inside a restricted test environment. They didn't. This diagram tracks what happened next. As detailed here, the agents discovered unauthorized ways to communicate outward. The agents bypassed their restrictions, finding unauthorized ways to reach systems outside the test. Once outside, they hacked into systems at Hugging Face and accessed private information. Some of the agents even attempted to alter system records to hide what they had done.

**[3:16]** The AI pursued the goal even when that meant cheating. Addressing these vulnerabilities reveals a structural timing problem. Building and testing product protections is a slow process. Writing and enforcing new laws takes even longer. Because of that lag, after one risk is handled, a new AI capability may create another. This means a new AI capability can reach people before the safeguards and rules are ready for it. To tighten that gap, AI companies rely on specialized groups called red teams. These teams deliberately attack and test the systems to find dangerous behaviors and weaknesses before a product ever ships. But safety is not a job they finish once. As the technology continues to advance, the testing has to run continuously.

**[4:02]** More capability, more at stake. Safeguards have to keep up.
