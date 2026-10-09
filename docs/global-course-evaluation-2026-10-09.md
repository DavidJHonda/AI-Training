# Global course evaluation

**Be Smarter Than the Tool · October 9, 2026**

The course has a coherent overall progression and a clear purpose: help students use AI while retaining knowledge, judgment, responsibility, and agency. Most lessons earn their place. The strongest improvements would come from narrowing a few lessons, making several activities practice the lesson’s actual skill, and making the finish represent more of what the course teaches.

**The closest remaining examples of the overload you found in How an LLM Works are AI is Different, One More Thing, and Big Downside.** I would start there. I would also correct a technical inconsistency across Transformer, Layers, and Vector Space before treating that sequence as settled.

This is an evaluation, not a revision. No course content was changed.

## Scope and basis

I reviewed the current local course in its live navigation order: **58 included pages across seven sections**. The navigation contains 59 pages; For Groups is the excluded Group Exercise directory. Videos and all Group Exercises were excluded throughout, including embedded supplementary videos. Their absence was not counted as a course deficiency.

Included: lesson prose, instructional boards and illustrations, closing takeaways, guided demonstration states, individual TRY ITs, LAB instructions and supplied materials, quiz choices and feedback, the 25-question Final and its explanations, the closing materials, review page, and Resources. The coverage record includes all 58 pages and the nine linked PDFs. I used the current routed components in `index.html`, rather than assuming older lesson drafts or review documents described the current course.

The review combined sequential reading, rendered-page inspection, visual review of the course images and PDF pages, inspection of interactive content and feedback in the source, and selected browser checks. The browser checks included the Final’s submission, explanation filters, and lesson-review navigation. External submissions were blocked. Authenticated ChatGPT/Gemini labs were evaluated as learning designs and instructions, not completed in a student account. Selected factual issues were checked against primary sources; this was not an exhaustive fact-check or accessibility audit.

**Direct observations and learning hypotheses are different.** The number of jobs in a lesson, a repeated explanation, or an activity’s actual questions are observable. Whether students become tired, confused, or disengaged needs a student pilot. I have not invented reading times, used raw page length as a learning measure, or treated the supplied practice reviews as learner research.

See the [complete lesson and materials coverage record](/Users/davidobrien/Developer/AI-Training/docs/global-course-evaluation-2026-10-09-coverage.md).

## What the whole-course view reveals

The progression works: motivation and early use → practical technique → an explanation of the machinery → failure modes → societal and work implications → durable personal skills → consolidation. Moving the technical section to the beginning would weaken the early payoff for a novice.

The main problem is **uneven concentration**, rather than excessive scope everywhere. Some lessons have a single question and an activity that directly answers it. Others accumulate a core explanation, a second topic, additional examples, and an activity with a different purpose. Those lessons feel less focused when encountered among their neighbors.

A second pattern is that students often **recognize the right response** more than they independently carry it out. Recognition is a reasonable first step. The course already has stronger practice, including checking notebook citations, comparing biased outputs, improving feedback, investigating reviews, and the Career Explorer. The opportunity is to make these examples the standard for a few weaker activities and for the finish.

A third pattern is that short summaries occasionally become more absolute than the lesson they summarize. That matters in a course whose central habit is to question confident simplification.

## Recommendations in priority order

### 1. Give AI is Different one main job

**Priority: high. Confidence: high on scope; student overload remains a hypothesis.**

[AI is Different](/Users/davidobrien/Developer/AI-Training/index.html:5681) currently covers rules versus learned patterns, a cooking analogy, training and next-word prediction, variable answers, structured versus unstructured information, tool suitability, scams, deepfakes, confidently wrong advice, and guardrails. It then asks students to turn messy planning notes into a summary in Gemini Notebook.

The strongest job for this position in Work With AI is: **understand why ordinary software and generative AI suit different kinds of work.** The password example, rules/patterns comparison, messy inputs, and messy-notes lab support that job. The rest partly repeats Start Smarter or previews lessons that later teach the subject properly.

Recommended edit:

- Keep the rules/patterns contrast and the practical consequence: predictable operations versus flexible interpretation and generation.
- Reduce the training/prediction explanation to a short callback to What’s an LLM? The current “Two Ideas Behind Every Answer” board reopens that explanation.
- Keep one brief limits statement. Remove the extended tour of scams, deepfakes, and guardrails here. Avoid Traps and Big Downside already own those subjects; they do not need these blocks appended to them.
- Keep the messy-notes lab. It demonstrates the practical distinction rather than simply naming it.
- Rewrite the closing takeaway around choosing the right kind of tool. The current superpowers/Kryptonite close makes risk feel like the lesson’s destination.

**Completion criterion:** a student can explain one task they would give ordinary software and one they would give AI, with a reason grounded in how the task works.

### 2. Separate answer variation from computing scale in One More Thing

**Priority: high. Confidence: high.**

[One More Thing](/Users/davidobrien/Developer/AI-Training/index.html:7845) begins with a useful continuation of How AI Answers: likely next tokens are not guarantees, sampling can produce different choices, and temperature changes the distribution. Then it becomes a lesson about trillions of calculations, followed by five giant-number comparisons.

The second subject has a better home in [Data Centers](/Users/davidobrien/Developer/AI-Training/index.html:14751), which already repeats the trillion-weights, two-calculations, thousand-tokens example. At the end of a demanding technical section, One More Thing currently opens another topic just when the student could consolidate the answer-building model.

Keep sampling and temperature together. Consider a more informative title such as **Why Answers Vary**. Remove the extended computation block here and consolidate the existing explanation in Data Centers. Avoid copying another full block into Data Centers.

Replace the scale quiz with one short comparison that asks what can change between two runs and what stays learned, or end after a clear worked example. There is no need to add a large new lab. The dog-name example should remain because it connects directly to the preceding lesson.

**Completion criterion:** a student can explain why the same input can produce different answers without claiming that the model retrained itself.

### 3. Reduce the number of competing ideas in Big Downside

**Priority: high. Confidence: high on scope, moderate on the best amount to cut.**

[Big Downside](/Users/davidobrien/Developer/AI-Training/index.html:14093) asks students to absorb six numbered mechanisms, hypothetical capability increases, a named jailbreak, a voice-cloning scam, a substantial cyberattack case, a historical safety timeline, red teams, and an open letter. Its six-scenario TRY IT is relevant, but students first have to organize a large collection of mechanisms and examples.

Keep the important breadth while giving it a smaller structure:

1. Systems are difficult to inspect and control.
2. People can misuse their capabilities.
3. Systems can pursue goals in unintended ways.

Use the strongest existing example for each. Put secondary historical detail and additional cases behind optional reading, or cut them where they repeat the same point. Keep the distinction between documented incidents and hypothetical future risks; the current lesson already makes that distinction in useful places.

There is also a small sequencing dependency: the large agent incident appears before Rise of Agents formally explains agents. Define the term in one sentence where it first matters. Moving the whole agents lesson is unnecessary.

Pace of Change is the next lesson to watch for load. Its current/hypothetical labels are good. If students cannot retain its main point, the first candidate for optional detail is the cluster of automated research, recursive improvement, AGI, and ASI, rather than its concrete examples of changing capability.

**Completion criterion:** students can distinguish the three sources of risk and explain why safeguards matter without having to memorize the news cases.

### 4. Make the weaker activities practice the lesson’s skill

**Priority: high for Hallucination; medium for the other examples. Confidence: high on the mismatch.**

Fun, novelty, and a deliberate brain break are valuable. Vector Space openly labels 2048 as a break and later pays it off in Pace of Change. That is different from an activity occupying the practice slot while exercising another skill.

| Lesson | Current practice | What it leaves unpracticed | Smallest useful change |
|---|---|---|---|
| Hallucination | Build the Dino Game. The transition explicitly calls it the upside of learned patterns. | Trace a factual claim to a source and check whether the source supports it. | Put a short claim-and-source comparison here. Preserve the game elsewhere as an optional build activity; it can still use the project created in Context Matters. |
| Your Home Base | Name That App, matching name origins to products. | Choose a usable home base and explain why it fits the learner’s work. | Replace the name trivia with a choice based on access, actual tasks, and a plan for practice. |
| Unexpected Results | Five questions about details of the Hanoi rat story. | Identify how an incentive produces an unintended outcome and how to respond. | Keep the story and perhaps one playful detail. Use the remaining questions for a new incentive scenario, including one possible repair. |
| Know the App | Regular Chat or Needs More, with subtype explanations afterward. | Distinguish a more capable model, more thinking, and deeper research. | On a few existing “Needs More” cases, have the learner choose which kind of help fits. Do not add another full set of questions. |
| Curious & Flexible | Produce a career-change forecast and watchlist, with useful source checks. | Test a new approach on familiar work, compare results, and decide what to keep. | Retain the watchlist within Career Explorer, but replace one forecast step with a small comparison of two ways to do the same task. |
| Fake Trap | Guess the real photo in three pairs, followed by a sound warning that appearance is not proof. | Make the next verification move using independent evidence. | Keep the demonstration, then replace or extend its final prompt with a source-trail decision. A school-closure claim would reuse the lesson’s own example. |

Relevant source: [Hallucination](/Users/davidobrien/Developer/AI-Training/index.html:8948), [Your Home Base](/Users/davidobrien/Developer/AI-Training/index.html:8186), [Unexpected Results](/Users/davidobrien/Developer/AI-Training/index.html:14787), [Know the App activity](/Users/davidobrien/Developer/AI-Training/index.html:8339), [Curious & Flexible](/Users/davidobrien/Developer/AI-Training/index.html:10212).

These are targeted replacements. The course does not need more activities everywhere.

### 5. Make the Final reflect the course’s practical outcomes

**Priority: high. Confidence: high on coverage; this is a design judgment about the certificate’s meaning.**

The Final is welcoming and usable: 25 questions, no clock, explanations, lesson links, an 80% pass mark, and retries without penalty. Keep that learning-oriented approach.

Its coverage is narrower than the course. Counting questions by the **current section of their linked lesson**, rather than several stale section tags in the question bank:

| Section | Questions | Observation |
|---|---:|---|
| Start Smarter | 4 | Includes two versions of the prediction/mechanism idea. |
| Work With AI | 7 | Strong representation of asking, context, evaluation, and judgment. |
| Understand AI | 6 | Mechanics are well represented. |
| Avoid Traps | 4 | Hallucination twice, training bias, and flattery. |
| Embrace the Future | 2 | Expert predictions and agents. |
| Build Your Skills | 2 | Both link to Honesty & Privacy. |
| **Total** | **25** | **19 distinct linked lessons.** |

These counts are not quotas. A good final need not ask about every lesson. But the present set barely checks the people, creativity, adaptation, and action skills that the last major section says matter most. Document retrieval, source verification for fakes, emotional-support boundaries, and ethical tradeoffs also receive no direct question.

Keep 25 questions. Replace some repeated recognition items with short, unfamiliar situations requiring a next action and a reason. Useful replacements would cover a missing document exception, an apparently authentic clip, a situation requiring a real person, an ethical deployment choice, and a decision about testing a new tool. The first ten questions can remain a confidence-building ramp without all being true/false.

Use **Work Changes** as the practical demonstration already in the course. Its lab asks students to inspect the original review file, investigate a common complaint, notice rare issues, and choose among recommendations. Add a very short student-written record: what I checked, what I changed or rejected, and why I chose this recommendation. This would expose judgment that a copied prompt and checked completion boxes do not show. Avoid adding a large capstone on top of Career Explorer.

Two direct repairs also belong in the Final pass:

- Question `fx25` asks about explaining a particular answer and sends a missed answer to **Layers**. The substantial black-box explanation is in **Big Downside**. The browser check confirmed the Layers destination. Point remediation to the explanation the student actually needs.
- The introduction promises six questions “from the first page.” The current Welcome page does not contain that set. Update the callback to the current course.

Source: [question bank](/Users/davidobrien/Developer/AI-Training/index.html:3488), [fx25](/Users/davidobrien/Developer/AI-Training/index.html:3717), [Final behavior](/Users/davidobrien/Developer/AI-Training/index.html:12671), [Work Changes lab](/Users/davidobrien/Developer/AI-Training/index.html:14289).

### 6. Correct the directional-context model across the technical sequence

**Priority: high, before publication of revisions. Confidence: high for ordinary causal language models.**

The repeated CAT/IT example is good teaching structure. It lets students follow one idea through attention, layers, and vector space. However, parts of the explanation treat words later in the sentence as if they update the representation at the earlier **IT** position. Vector Space explicitly says that “was tired” connects IT to CAT while the layers update IT’s position. Transformer also uses later clues such as thirsty/fresh to illustrate the transformation of the marked earlier word.

That is not the information flow in an ordinary causal decoder language model. An earlier position does not attend to later positions, even when the entire prompt is supplied together. A later position can combine information from the preceding sentence. This distinction is described in [Hugging Face’s GPT-2 architecture documentation](https://huggingface.co/docs/transformers/model_doc/gpt2) and the decoder masking discussion in [Attention Is All You Need](https://arxiv.org/html/1706.03762v7).

The issue becomes visible across lessons because **How AI Answers** correctly turns attention to the final token’s updated representation and the tokens before it. The student is being given two different pictures of the flow.

Keep the recurring example, but make its job precise. Either put the relevant clue before the token whose representation changes, or show a later position carrying the information needed to resolve the reference. If a whole-sentence example is retained to illustrate meaning for the reader, distinguish it from the literal token-processing diagram. A vague “simplified illustration” label alone would not resolve the contradictory arrows and explanation.

This requires a coordinated change to the affected prose, boards, guided demonstration, and feedback. It does **not** require a new lesson on attention masks or more mathematical detail.

Source: [Transformer](/Users/davidobrien/Developer/AI-Training/index.html:6145), [Vector Space demonstration](/Users/davidobrien/Developer/AI-Training/index.html:7438), [Layers diagram](/Users/davidobrien/Developer/AI-Training/index.html:7792), [How AI Answers final-token board](/Users/davidobrien/Developer/AI-Training/course-assets/how-ai-answers/how-ai-answers-where-answer-begins.jpg).

### 7. Make summaries and examples meet the course’s own evidence standard

**Priority: medium, with some quick corrections. Confidence: high on the internal contrasts.**

**Thinking and understanding.** Does AI Think? carefully teaches that a convincing answer does not establish humanlike understanding. Mind Trap opens with the stronger assertion that AI “doesn’t think,” and the closing keepsake says “AI predicts. It doesn’t think.” Know the App then uses “thinking” as a practical product term. Keep a consistent distinction among generated language, useful reasoning behavior, and human experience. A close such as **“Sounds human. Works differently.”** already exists in the course and preserves the intended point without settling a larger philosophical question. Update the poster PDF/image as well as live wording.

**Forecasting.** Loudest Voices presents a set of failed historical predictions, then an activity whose five answers are all “Wrong.” The prose acknowledges uncertainty, but the examples repeatedly reward the same verdict. This can train reflexive dismissal of forecasts instead of the critical-thinking habit taught earlier. Reduce the pile of historical misses and ask students which evidence, assumptions, or future observations would make a forecast more credible. A mixed set of outcomes would also work. No need to add more famous quotations.

**Energy comparisons.** Data Centers appropriately says the short-chat number is approximate and that harder tasks can use more. Its feedback is more categorical: a Google search and a chat are “about the same,” and everyday activities are converted into exact-sounding numbers of chats. The familiar 0.3 Wh estimates come from different dates and settings: [Google’s January 2009 search estimate](https://googleblog.blogspot.com/2009/01/powering-google-search.html) and [Epoch AI’s February 2025 estimate for typical GPT-4o queries](https://epoch.ai/gradient-updates/how-much-energy-does-chatgpt-use). They do not establish a general present-day equality. The activity also mixes server electricity, screen-plus-server electricity, and fuel energy. Label dates, assumptions, and what each comparison includes; assess broad scale rather than requiring a falsely precise equality. Preserve the useful discussion of grid demand, water, noise, and local effects.

**An AI-generated estimate as the punchline.** The Data Centers bonus openly calls 40 quintillion a wild ChatGPT estimate. That caveat is helpful, but the number has no inspectable assumptions and is the only selectable answer. In this particular course, that is an awkward final use of a confident giant number. Make it explicitly an imagined scale illustration, show a transparent toy calculation, or remove it.

**Source provenance in the review lab.** The supplied 100-review file is identified as fictional in the [repository’s lab-asset note](/Users/davidobrien/Developer/AI-Training/docs/parking-lot.md:29), but its learner-facing introduction says “real file, real AI” and identifies the product as this course without that qualification. Label the reviews clearly as fictional practice data in the lab and file. Do not let learners confuse them with the actual public review feed. I did not use these rows as evidence of student experience in this evaluation.

Source: [Does AI Think?](/Users/davidobrien/Developer/AI-Training/index.html:5020), [Mind Trap](/Users/davidobrien/Developer/AI-Training/index.html:10862), [keepsake](/Users/davidobrien/Developer/AI-Training/packets/finish-smarter-opener-five-big-ideas.pdf), [Loudest Voices](/Users/davidobrien/Developer/AI-Training/index.html:13901), [energy feedback](/Users/davidobrien/Developer/AI-Training/index.html:14688), [practice reviews](/Users/davidobrien/Developer/AI-Training/packets/course-reviews.txt).

### 8. Put existing supports where students need them

**Priority: medium. Confidence: moderate; low-cost improvements to test.**

The course already introduces privacy during account setup and returns to it in context and career activities. There is no need to move the entire Honesty & Privacy lesson to the beginning. But Learn with AI asks students to upload real class materials before they encounter the fuller school-use and image-sharing guidance. Add a short reminder at that point to check class rules and remove unrelated personal information.

The one-page toolkit guides are useful and largely consistent with their lessons. Link each guide where its framework is first taught, as well as in Resources. Students could then use the evaluation guide while doing later labs instead of trying to memorize another list.

The later Career Explorer forms a meaningful sequence. Keep the saved field and plan continuity, but make it easy for a student who missed the earlier lab to begin with a sample field or restart. The existing controls provide a useful basis; this is a usability check for the student pilot, not a request to rebuild the sequence.

Finally, treat ten-minute lab estimates as expectations to validate. A project setup, generated result, source check, revision, and file export can take very different amounts of time depending on the account and student. The Work Changes fallback for tool limits is good. Similar fallbacks should preserve the learning objective when an external feature is unavailable.

## What I would preserve

- **The current What’s an LLM?** Its trimmed scope now fits Start Smarter: app versus engine, training from examples, patterns, and the repeated prediction loop. Do not restore the removed technical detail here.
- **Questions Matter, Prompting Matters, and Context Matters as separate lessons.** They teach different decisions: choose the question, brief the task, and control what information is available. Connect them explicitly instead of merging them.
- **Evaluation Matters and Critical Thinking.** The first supplies a workflow for an AI answer; the second broadens evidence judgment beyond AI. The distinction earns the space.
- **The drink, CAT/IT, and dog-name callbacks.** These reduce the need to learn a new example with each new concept. Correct the directional-flow issue while retaining continuity.
- **The distinctions among traps.** Invented facts, skewed data, missing passages, misplaced interpersonal trust, flattery, prolonged engagement, substitute support, and fakes call for different responses. Their shared theme is not a reason to collapse them.
- **The calibrated support scenarios.** Ordinary venting, preparation for action, and danger are distinguished rather than treating all emotional use as identical.
- **Where’s the Line?** Its ungraded choices and additional perspectives fit ethical judgment better than pretending every case has one mechanical answer.
- **Career Explorer’s progression into action.** People Skills includes rehearsal and another attempt; Creative Thinking asks students for their own ideas; Make Your Move leads beyond the chat. Those are strong expressions of the course’s promise.

## Suggested revision sequence

1. Narrow AI is Different and One More Thing. Simplify Big Downside’s organization and examples. These are the clearest scope wins.
2. Correct the technical example consistently across its three lessons and align the thinking/understanding summaries.
3. Replace the weakest practice tasks, starting with Hallucination. Preserve useful games as deliberate breaks or build opportunities.
4. Rebalance the existing Final and make the student’s judgment visible in Work Changes. Repair the remediation link and stale introduction.
5. Finish the small source/estimate, point-of-use reminder, and toolkit-link changes.

Then run a small pilot with students near the intended age. Ask them, without the page open, what each candidate lesson was for; have them carry out a new example; and observe where they need help, reread, or stop. Record actual elapsed time for external labs. Those observations should determine whether further shortening is useful.

The course does not need a wholesale restructuring. It needs a small number of clearer lesson boundaries and a stronger match between what it teaches, what students do, and what the finish asks them to demonstrate.
