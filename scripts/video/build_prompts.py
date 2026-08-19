#!/usr/bin/env python
"""Generate the per-video re-roll prompts for Prompts/.

One shared rules block so every kit is calibrated identically, plus a per-lesson
body (focus + scene walk) and per-lesson bans/required narration targeted at the
current rubric's deductions for that video.

Hard limit: the Gemini Notebook prompt box truncates at 5,000 characters (UTF-16-ish).
Aim <= 4,800. The builder refuses to write anything over 4,950.
"""
import os, sys

LIMIT_HARD, LIMIT_WARN = 4950, 4800

MOTION = ("Motion belongs to drawn scenes: animate builds and transitions there. "
          "{board_clause}Remove a board only when its narration ends.")
BOARD_WALK = ("On an attached board legible as a whole, keep the exact full board fixed through "
              "its narration and highlight only the current card or row as spoken; never replace, "
              "crop, or pan between points. Dive to a whole card only if its text is unreadable "
              "full-board. ")
DECK = ('Teach from the visuals, never describe them — never say "this image shows" or "as this '
        'graphic illustrates"; speak the idea, let the picture follow.')
STYLE_LEAK = ('Never letter the drawing\'s own style or materials into the artwork — no "fineliner", '
              '"watercolor", "analog texture" or any medium or setting word as a label.')
NOASK = ("Never ask the viewer to pause, guess, or answer; answer any question the lesson poses in "
         "the same breath.")
WHITE = ("Never put white or light-colored text on a light background, in scenes or transitions; "
         "all text is dark ink on light.")
NOSTOCK = "No photographic or stock imagery — no Getty or watermarked images."


def build(slug, title, lo, hi, boards, body, numbers, props, required, extra=()):
    src = (f"The attached {slug}.md is the lesson text; the numbered images are its "
           f"key boards, in order — show each as the narration reaches it and hold it while the "
           f"narration walks it."
           if boards else
           f"The attached {slug}.md is the lesson text. Draw every visual fresh, and render the "
           f"lesson's tables, lists and cards as clean drawn boards with their exact wording.")
    rules = [NOSTOCK]
    if boards:
        # "underline the row you are speaking" retired 2026-07-27: the engine already
        # does it. In one batch, 7 of 7 rolls marked kit boards while the prompt
        # explicitly BANNED marking, so there is nothing here to instruct.
        rules += ["Show the attached images exactly as provided — never redraw, restyle or replace them."]
    else:
        rules += ["Never show the lesson document itself as a page on screen; draw the boards fresh "
                  "in clean dark ink."]
    # numbers/charts and no-readable-text-in-props were retired 2026-07-27 on David's
    # call: the numbers rule was policing form when the real concern is the teaching
    # point, and the props rule's only genuine risk was profanity, which is caught at
    # evaluation instead. Both kwargs are still accepted so the per-lesson text is not
    # lost if either is ever revived.
    # style-prompt leakage retired 2026-07-27 on David's call. It was in every kit and
    # violated anyway (training-bias, how-an-llm-works, flattery-trap), so the wording
    # was not preventing it. It is unpatchable once rolled -- the words are inside the
    # artwork -- so it becomes a re-roll trigger at intake, not a prompt rule.
    rules += [WHITE]
    rules += list(extra)
    rules += [f"Required narration: {required}",
              MOTION.format(board_clause=(BOARD_WALK if boards else
                                           "Hold each drawn board while the narration walks it. ")),
              DECK,
              # close-board-as-final-frame retired 2026-07-27: 5 of 12 rolls in one
              # round appended an outro anyway, and freeze_finisher.py cuts post-close
              # junk and freezes the board under trailing narration in about two minutes.
              ]
    if not boards:
        rules += ["End on the lesson's own closing lines as a clean drawn close board, and let it be "
                  "the final frame — nothing after it, no outro or summary."]
    head = (f'Create a video overview of the attached lesson "{title}", between {lo} and {hi} '
            f'minutes long — do not come in under {lo}. {src}\n\n')
    txt = head + body.strip() + "\n\nRules:\n" + "\n".join(f"{i+1}. {r}" for i, r in enumerate(rules)) + "\n"
    return txt


LESSONS = {}


# Lessons marked Final & Done on the tracker: their kits were retired 2026-07-27, so
# no prompt is written for them. Without this, regenerating silently RESURRECTS the
# deleted files (it did, on 3 of them). how-an-llm-works is deliberately not here --
# its why-board kit was restored on request.
RETIRED = {"does-school-matter", "ai-is-different", "transformer", "hallucination"}


def add(slug, **kw):
    if slug in RETIRED:
        return
    LESSONS[slug] = kw


# ---------------------------------------------------------------- Start Smarter
add("does-school-matter", title="Does School Matter?", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 the two skills, 2 the close.

Focus: if AI can answer anything, do you still need school? Open on that question in the viewer's own words — a lot of people your age are quietly asking it — then answer it with the lesson's thought experiment, in the lesson's plain voice.

Fast forward a few years: you've landed your dream job, and AI sits right next to you all day cranking out drafts, code, and plans. Your coworker at the next desk is doing exactly the same, same job, same AI. Then the catch: ask AI a similar question and it hands back a similar answer — to you, to your coworker, to everyone. So what makes you more valuable? Not the answer itself. What you already know, which shapes the question you ask and what you do with the answer. Give that sentence its own beat.

Then the counterintuitive turn: in the AI era, learning is more important than ever. Say plainly that this is the idea the course is named after, Be Smarter Than the Tool. Then the two skills, as a drawn board with both numbered rows carrying their real wording: 1. Ask the right question — what you know shapes what you ask, and a sharper question gets a better answer before AI does anything special. 2. Make the answer better — read it, judge if it's right, push back, improve it; AI can't do this for you because it doesn't know what you know. Hold that board and walk both rows.

Close on the lesson's own escalation: double down on building your knowledge and skills, and one day you'll be the CEO at Google. Then the close board: "Know more than the tool." over "It starts today, not when you land the job."
""",
    numbers="Do not invent numbers, percentages, or statistics, and draw charts only as wordless background — this lesson contains no data whatsoever.",
    props="No readable or pseudo-readable text in drawn props — never draw code editors, research papers, equations or document pages with visible writing; real words belong only on the drawn boards and in clean dark-ink labels.",
    required='the narrator must speak "Be Smarter Than the Tool" as the name of this course, the line "one day you\'ll be the CEO at Google," and the close "Know more than the tool. It starts today, not when you land the job."',
    extra=("Keep the narration in the lesson's plain, second-person voice for a 16-year-old — never substitute corporate register such as \"loses its professional value\", \"becomes a commodity\", \"director of the input\", or \"strictly human domains\".",))

add("why-learn-ai", title="Why Learn AI?", lo=3.5, hi=4, boards=True,
    body="""
Attached boards in order: 1 AI in the apps you use, 2 why you'll thrive, 3 the White House quote, 4 the close.

Focus: AI is early, it is already everywhere, and being young is the advantage.

Open on the scribe. It is the year 1500 and you hand-copy the king's proclamations all day. Good work, steady job. Then you hear a guy in Mainz built a machine that prints pages a thousand times faster than you can write them. Two choices: pretend it isn't happening, or learn the machine well enough to run it. Then land the line on its own: AI is the press. Run it, or someone else will.

Then AI is everywhere. It isn't something you go visit — it's already in the apps on your phone, the search results you read, and the tools your first job hands you on day one. Most of what it does today it will do better tomorrow. Then the everyday-apps board, held while the narration walks its five cards and says what each one predicts. Say the thread out loud — most of the time AI is making a prediction about what you might tap, say, watch, search for, or need next.

Then the part that matters most to a 16-year-old, and give it the most room: AI is new for everyone, and that is your advantage. Hold the thrive board and walk all three rows — this is YOUR time, you'll move faster, nothing to unlearn — speaking the reason written under each, in the board's own words. Never read the headings and move on; the reasons are the point of that board.

Then this has happened before. Becoming a designer once meant years at a drafting table learning the craft by hand. Then desktop publishing showed up and a teenager with a Mac could turn out professional work in an afternoon. Say what that means: the tool didn't replace skill, it shortened the distance between wanting to do the work and actually doing it. Then the rule, not the exception — the steam engine for physical labor, electricity for the factory, the internet for information. AI is that, for almost everything.

Then the quote board, introduced as evidence rather than hype: in July 2025 the White House released a national strategy document, Winning the Race: America's AI Action Plan. Show the attached quote card and read it exactly as written: "An industrial revolution, an information revolution, and a renaissance — all at once. This is the potential that AI presents." Attribute it aloud to the White House, July 2025.

Close board: "AI is today’s printing press." over "Learn to run it."
""",
    numbers="Do not invent numbers, percentages or statistics; the lesson's only figures are the year 1500 and July 2025.",
    props="No readable or pseudo-readable text in drawn props — never draw proclamations, printed pages or phone screens with legible writing; real words belong only on the attached boards and in clean dark-ink labels.",
    required='"AI is the press. Run it, or someone else will."; all three thrive reasons spoken, not just their headings; the White House and July 2025 named aloud when the quote appears, with the quote read exactly as written; and "the tool didn\'t replace skill, it shortened the distance between wanting to do the work and actually doing it."',
    extra=("Depict no real named person, living or historical, and put no face on Gutenberg — the scribe and the printer are ordinary figures.",
           "Keep the narration in the lesson's plain, second-person voice for a 16-year-old — never corporate register."))

add("does-ai-think", title="Does AI Think?", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 the giant rulebook, 2 when you think vs. what AI does, 3 the close.

Focus: it sounds like a person and understands nothing. It's a pattern machine — and a pattern machine this good is still genuinely powerful.

Open on the feeling, not on a definition. You type a question and AI types back like a person: it explains, it jokes, it says sorry when it slips up. After a while it's hard not to feel like someone is in there. Then ask the lesson's big question and answer it in the same breath — does AI actually think? No. Not the way you do.

Then it's in the name: we call it Artificial Intelligence, not Artificial Thinking, and that was picked on purpose. Something can act intelligent, finish your sentence, explain a poem, without understanding a single thing it just said.

Then the Chinese Room, dramatised before it is named. Someone is locked in a room and doesn't know a word of Chinese. Notes in Chinese come in under the door. They can't read any of it, but they have a giant rulebook telling them which symbols to send back. So they match symbols and slide an answer back out, and to the people waiting outside it looks perfect.

Then board 1, and hold it while the narration walks it. Say what the person inside is actually doing: they see a shape in the left column, they find the shape it pairs with, they copy it out. Neither column means anything to them. Read the board's own line as the payoff — match the shape, send back the likely reply, understand nothing. Then cash it out: that's AI. It arranges symbols brilliantly and understands none of them, so you get a perfect-looking answer with no real understanding behind it.

Then board 2, and give it more time than anything else in the video. It is five paired rows and every pair has to be spoken, human side then AI side, in the board's own wording: understand what words really mean against matches patterns in mountains of text; draw on real experience against only reads about the world; choose words to make a point against predicts the next likely word; feel when something's beautiful against echoes what others call beautiful; know when you're unsure against can't tell when it's making things up. Never read one column and summarise the other — the contrast in each row is the whole board.

Then the correction, and don't skip it: none of this means AI is dumb or useless. A pattern machine this good is genuinely powerful. It just means it isn't thinking.

Close on board 3: "A pattern machine, not a thinker." over "Once you see that, its weird moments make sense."
""",
    numbers="Do not invent numbers, percentages, statistics or charts — this lesson contains no data at all.",
    props="No readable or pseudo-readable text in drawn props; real words belong only on the attached boards and in clean dark-ink labels.",
    required='"Artificial Intelligence, not Artificial Thinking"; the Chinese Room named aloud; "It arranges symbols brilliantly and understands none of them"; both sides of all five compare rows; the correction that a pattern machine this good is genuinely powerful and just isn\'t thinking; and the close, "A pattern machine, not a thinker. Once you see that, its weird moments make sense."',
    extra=("Any Chinese character that appears anywhere in the video must be a real character copied from the attached rulebook board. Never draw invented, approximate or scribbled glyphs on the notes, the door, the rulebook pages or anywhere else — the last roll filled its props with made-up characters. If a prop would need Chinese you cannot copy exactly, leave it blank or turn it away from camera.",
           "Keep the narration in the lesson's plain, second-person voice for a 16-year-old — never academic register such as \"syntactic manipulation\", \"semantic grounding\", \"consciousness\" or \"cognition\".",
           "The person in the room is an ordinary figure with no identifiable face, and depicts no real named person."))

# ------------------------------------------------------------------ Work With AI
add("which-app", title="Which App?", lo=3.5, hi=4, boards=True,
    body="""
Attached boards in order: 1 the big three side by side, 2 how we used each app, 3 the close.

Focus: three apps dominate — ChatGPT from OpenAI, Claude from Anthropic, Gemini from Google — they all chat, write, code and answer questions, so why does the choice matter? Because each company trains its model with different priorities.

Lead with the lesson's own analogy, named: In-N-Out and McDonald's both sell cheeseburgers built from roughly the same ingredients, and they are still completely different experiences, because each company has a different idea of what a burger place should be — one a tiny menu made fresh, the other engineered for speed, scale and being exactly the same in every city on Earth. Then map it: the big three are all generative AI trained on much of the same internet, but each is built around a different core philosophy.

Then board 1, held while you walk one column at a time: ChatGPT the Anything Box, Claude the Thinking Partner, Gemini Built Into Google, each with what it is and the question its company asks. Then land the three strengths: breadth, depth, context.

Then the honest answer: for most of what you'll do, any of the three works, so don't agonize. Pick one as your home base and learn it well — its settings, features and quirks — because knowing one app deeply beats dabbling in all three. Then the power move: when an answer really matters, ask the same question in a second app; two differently trained apps agreeing is real evidence, and if they disagree you know exactly where to dig.

Close on the real-world example in the authors' own voice: Nate and Luke used different apps for different jobs, guided by their dad — ChatGPT for brainstorming and the Dallas Stars illustrations, Claude Code for the code and Claude Design for the pages, Gemini for current information and fact-checking, and Gemini Notebook, which is powered by Gemini, for the videos in this course. Then the close board: "The skills transfer." over "The app is just where you practice them."
""",
    numbers="Do not invent numbers, percentages, statistics, benchmarks or scores, and draw charts only as wordless background — this lesson contains no data.",
    props="No readable or pseudo-readable text in drawn props, and no invented app screens, menus or interfaces; real words belong only on the drawn boards and in clean dark-ink labels.",
    required='the narrator must name "In-N-Out" and "McDonald\'s" out loud, must say that Gemini Notebook is powered by Gemini and made the videos in this course, must name Nate and Luke as the builders, and must close on "The skills transfer. The app is just where you practice them."',
    extra=("Never state or imply anything about how the three apps refuse, restrict, gate or guardrail requests — no claims about one model refusing more readily than another; the lesson makes no such claim and it must not be invented.",
           "Never depict a real, recognizable person and never draw a branded lectern, podium, company stage or officer of any company; keep every character an invented hand-drawn person."))

# ----------------------------------------------------------------- Understand AI
add("ai-is-math", title="AI is Math", lo=4, hi="4.5", boards=True,
    body="""
Attached boards in order: 1 the formula, 2 one coin, 3 two coins, 4 the update, 5 tying it together, 6 the close. Boards 1–5 share one standardized visual system.

Focus: the magic behind every AI you have used is math, two ideas from probability plus the loop that turns them into language. Open by saying the viewer already met these by name in How an LLM Works and now gets to see each one work.

Where it began: in 1654 two French mathematicians, Blaise Pascal and Pierre de Fermat, traded letters about gambling, and that correspondence is where standard probability is usually dated from. Name them both aloud. Then state the rule with its condition intact, in the lesson's own three beats: list every possible outcome, confirm they are equally likely, and you can calculate the chance of each one. Do not drop the equally-likely step; it is what makes the formula true.

Then board 1 on its own, before any example: ways it happens over total outcomes equals probability. Let the formula sit there and say it, so the examples that follow are the same formula filling in.

Board 2, one coin: the question is how likely it is to land on heads, the outcomes are heads and tails, and the formula reads 1 over 2 equals 50%. Board 3, two coins: how likely both land on heads, all four outcomes HH HT TH TT, and 1 over 4 equals 25%. Walk each board's own three parts in order, the question, the outcomes, then the math.

Conditional probability: standard probability counts what you can see but cannot tell you how much to change your mind when new evidence arrives. Thomas Bayes, a minister, mathematician and philosopher, worked that out, and it is called Bayes' Theorem. Name him and name the theorem. Then board 4: someone peeks and says the first coin landed heads, the two outcomes starting with tails are struck out in red, and recounting gives 1 over 2 equals 50%. Say what moved, that the evidence lifted the probability that both coins are heads from 25% to 50%, and that this update is conditional probability.

Autoregressive generation: start with the phone keyboard suggesting your next word, out loud, as the way in. It is that, except it does not stop after one word: after AI picks a word it uses that word to pick the next, then uses both to pick the third, so every prediction depends on every word before it.

Then board 5, all three on one rainy afternoon: standard probability gives a 40% base rate because it rained 40 of the last 100 May 21sts; conditional probability updates that to 60% on the evidence that humidity is 90% right now; autoregressive generation writes the forecast one word at a time, It, is, going, to, then picks from rain 71%, pour 18%, stay 7%. Speak the same base-rate sentence both times it appears, because the point is that only one new piece of evidence was added.

Close honestly, in the lesson's own words: the real math goes way past what is here, linear algebra moves the numbers, calculus tunes the model during training, and plenty of other math is in there too, but two ideas from probability plus the loop are the foundation.

End on board 6. It is the only closing card in this video.
""",
    numbers="The only numbers allowed anywhere are the lesson's own: 1654, 50%, 25%, the 25-to-50 update, 40%, 90%, 60%, and rain 71% / pour 18% / stay 7%. Never invent a percentage and never animate a counter through values the lesson does not contain.",
    props="No readable or pseudo-readable text in drawn props, and never letter the drawing's own materials or style into the artwork.",
    required='the equally-likely condition spoken as part of the rule, not dropped; Pascal, Fermat and Bayes all named aloud; "Bayes\' Theorem" by name; the phone keyboard as the way into autoregressive generation; and the closing admission that linear algebra moves the numbers and calculus tunes the model during training.',
    extra=("There is exactly ONE closing card, board 6. Never draw a second sign or title restating the lesson's message, and never invent alternative closing wording; the previous roll ended on two different close cards.",))

add("transformer", title="Transformer", lo=4, hi="4.5", boards=True,
    body="""
Attached boards in order: 1 the two problems, 2 how AI used to read, 3 the two steps, 4 the close.

Focus: tokens and vectors are not enough, because a word's meaning is not clear until you read the words around it. Open on the two nuances the lesson names.

One, different meanings: the word LIGHT in "Please turn on the LIGHT" and "The suitcase is LIGHT enough to carry." Two, pronouns: "The cat drank the milk because IT was thirsty" against "The cat drank the milk because IT was fresh" — only the last word changes, and IT switches from the cat to the milk. Show both pairs as clean drawn boards and let the problem land before moving on.

Why this was hard: AI used to read in order, one word at a time, and the further it read the more the early words faded. Walk the lesson's own sentence — The cat sat on the mat during the May rainstorm because IT was tired — and pose the four candidates out loud: cat, mat, May, or the rainstorm. Answer it in the same breath: we know instantly it points to CAT, ten words later, and a computer reading strictly in order does not.

The breakthrough, given its own beat: in 2017, eight researchers at Google published a paper called Attention Is All You Need. It introduced the Transformer, the architecture behind every modern LLM, and the T in ChatGPT. Say all of that aloud.

Then the mechanism, slowly, one step at a time. Step one, Attention: reading IT, the model weighs every word and leans hardest on CAT. Step two, Transformation: IT's vector updates to mean CAT. Hold each step on screen and explain what it does before moving to the next — do not read the two labels and move on. Then cash out both opening puzzles: attention links LIGHT to "turn on" in one sentence and to "carry" in the other, and transformation sets brightness in one and not-heavy in the other; "thirsty" links IT to the cat, "fresh" links IT to the milk.

Then the catch the lesson promised: if all the words arrive at once, how does the model keep them in order? Dog bites man and man bites dog are the same three tokens. The fix happens before the first layer — every token's vector gets a position stamp mixed in, and the proper name is positional encoding.

Close board: "Attention is all you need." over "The Transformer — the T in ChatGPT."
""",
    numbers="The only numbers allowed anywhere are the lesson's own: 2017 and eight researchers. Invent no percentages, scores or statistics, and draw charts only as wordless background.",
    props="No readable or pseudo-readable text in drawn props or backgrounds; every readable word on screen must be one the lesson actually uses, in clean dark ink.",
    required='the narrator must say "in 2017, eight researchers at Google published a paper called Attention Is All You Need", must say "the T in ChatGPT" aloud, must name "positional encoding", and must spend real explanatory time on Attention and Transformation rather than naming them.')

add("layers", title="Layers", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 the three reads, 2 inside each layer, 3 why there are dozens of layers, 4 the close.

Focus: meaning builds up over repeated passes, and each pass is a layer.

Open on the garden-path sentence exactly as the lesson does: "The horse raced past the barn fell." Then the three reads as three drawn cards — first read, it doesn't make sense, did someone forget a word; read it again, wait, did a barn fall, did the horse race past the barn afterward; read it a third time, got it, a horse ran past a barn and after running past the barn the horse fell. Then the point: each pass, your mind updates the meaning until it clicks.

AI does the same thing: it reads your message over and over, establishing the meaning a little more each pass, and because language is full of nuance it takes dozens of passes. Each pass is a layer, and at every layer AI runs the two moves from the Transformer lesson — attention, which words matter, and transformation, update the meaning. Call back to that lesson by name.

The mechanics, using the sentence the viewer already knows: The cat sat on the mat during the May rainstorm because it was tired. Take the word IT. On its own IT is just a pronoun whose vector could mean almost anything, and certainly not CAT. Then, layer by layer, each layer reads the surrounding words and shifts the numbers for IT — and say out loud what the shifting is FOR: the model is working out that IT refers to the cat, not the mat, not May, not the rainstorm. Do not leave that as an abstraction about vectors moving.

Then the inside-a-layer board: starting vector in, attention, transformation, richer vector out, handed to the next layer — the same two moves at every layer, with the numbers moving closer to what the token means each pass. Note the blank box: it gets filled in the next lesson.

Then board 3, held and walked card by card, because this is the beat that answers "why so many". A few passes: simple meaning resolves early, the plain sense of a sentence is settled in a handful of passes. Dozens of passes: catching sarcasm, following a twist in a story, or reasoning through a complicated problem takes many more. Why not hundreds: past a point extra depth stops helping, it just makes the model more expensive to run. Land the board's own line — a few layers reach only shallow meaning, stacking dozens leaves room for the deep kind.

Then neural networks: the whole stack is called a neural network, loosely borrowed from biology, simple units passing signals forward the way neurons do — but that is where the resemblance ends. It isn't a brain and it isn't thinking: the same arithmetic, repeated billions of times, fast.

Close board: "Meaning builds up, layer by layer." over "Attention and transformation. Dozens of times."
""",
    numbers="Use only the lesson's own vector values where you show them. Invent no percentages, statistics, layer counts or benchmarks, and draw charts only as wordless background.",
    props="No readable or pseudo-readable text in drawn props; every readable word on screen must be one the lesson uses, in clean dark ink.",
    required='the narrator must say out loud, over the cat/mat/May/rainstorm visual, that attention leans hardest on CAT and that layer by layer the model works out that IT refers to the cat — not merely that the numbers shift. Keep the plain register: never substitute phrasing like "the system resolves linguistic ambiguity by calculating mathematical relationships".')

add("tokens", title="Tokens", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 one chunk, thousands of words, 2 tokenization defined, 3 how a human sees a cat vs AI, 4 how AI splits text into tokens, 5 the close.

Focus: before AI can read anything, an ordinary program chops your text into chunks and swaps each for a number — and that number is an address, not a meaning.

Open on the callback and the contradiction: you've already seen that math is the magic that powers AI, but that is not what using AI feels like. Show the lesson's own exchange — you ask "what's the best Avengers movie?" in plain English and get plain English back. That felt effortless because you think in language: you read Avengers and instantly picture the movie.

Then the fact underneath everything, said flatly: a computer can't do that, because computers work only with numbers — they don't read text at all. So before AI can read your question, it must convert your text to numbers.

Then the obvious solution and why it collapses: give every English word its own number. Counting names, slang, typos and code you'd need millions, and you still couldn't cover words nobody has invented yet.

Then the fix, on board 1, held while the chips are read: engineers break language into reusable chunks. Take every word starting with UN — unbelievable, unmatchable, untied, unlock, unfair, and thousands more. The vocabulary stores UN once and reuses that one piece to help spell all of them. Read enough of them aloud that the reuse is obvious.

Then board 2, held while its three cards are walked in order, in the board's own words and keeping the ordinariness: the small ordinary program called a tokenizer with no AI in it, the two names, and every form a token might take, down to the space before a word.

Then the vocabulary: each model knows a fixed set, and they run large — ChatGPT's holds about 200,000 and Gemini's about 256,000. Say that Anthropic hasn't published Claude's.

Then the token ID: each token gets a number, an address in the model's vocabulary — it tells the model which token, and says nothing about what it means.

Then board 3, held while both sides are walked: a human reads cat and instantly knows what it means, soft fur, whiskers, sits on your keyboard; the tokenizer turns cat into 9246, either way it's a number, not meaning yet.

Then board 4, held and walked row by row, saying first that each AI does this differently so this is only an example: unbelievable into un, believ, able, three tokens broken into known parts; basketball into basket and ball; ChatGPT into Chat, G, PT, because brand names get split; "I heart AI" into three, where the marker shows a leading space; and the quickbookstraining URL into seven, because URLs split into known pieces too.

Then: once it's built, the model uses that same fixed vocabulary every time it reads text.

Close board: "Computers don’t read text." over "Tokens convert language into readable numbers."
""",
    numbers="The only numbers allowed are the lesson's own: 200,000 and 256,000 for the vocabularies, 9246 for cat, the token IDs printed on board 2, and the token counts 3, 2, 3, 3 and 7. Invent no benchmarks or percentages.",
    props="Every readable word on screen must be one the lesson uses; no invented app screens or pseudo-text.",
    required='the narrator must say that computers work only with numbers and don\'t read text at all; must call the tokenizer a small ordinary program with no AI in it; must speak the vocabulary sizes with Anthropic\'s omission ("Anthropic hasn\'t published Claude\'s"); and must speak both closing lines.',
    extra=("Write in the lesson's plain second-person voice; never substitute systems register such as \"a technical vacuum\", \"a different mathematical architecture\" or \"the next stage of the architecture\". The last roll drifted this way throughout.",
           "Add no mechanism the lesson does not state — in particular, do not claim tokens go down to single letters so unknown words can still be processed, and do not claim the vocabulary is sized to cover any sentence a human can type. The last roll invented both.",))

add("embeddings", title="Embeddings", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 the Coke/Coffee taste table, 2 the three-drink table with Citrus, 3 the close.

Focus: a token ID is just a number; embedding is how AI turns it into meaning.

Open on the student-ID analogy in the lesson's own words: an ID might let you in the building, but it doesn't tell anyone whether you're funny, into hockey, or the person who steals fries at lunch.

Then the taste test. You and your friends rate Coke and coffee on six characteristics — Sweet, Bitter, Fizz, Heat, Caffeine, Dark. Draw the table with the lesson's exact values: Coke, token ID 24317, scores 9, 1, 10, 2, 3, 8; Coffee, token ID 51820, scores 1, 9, 0, 9, 8, 10. Then the reveal: if someone asked which drink has sweet 9, bitter 1, fizz 10, you'd instantly say Coke — you have represented a word's meaning with a row of numbers. Name the three terms on that board: the row is a vector, each slot is a dimension, each number is a value.

Then the Pepsi problem. Add Pepsi, token ID 38106, and it scores identically to Coke on all six. On these numbers alone you cannot tell them apart. So add a seventh dimension, Citrus: Pepsi 10, Coke 1 — and only then do the rows differ. Be careful here: Coke and Pepsi are CLOSE, not the same; never label them as having the same meaning.

Then the scale-up: AI can't add a labeled dimension like Citrus for every difference between all the words in English, so real models give each token thousands of dimensions, learned during training. And the easy-to-miss point: every token is scored on the SAME dimensions — map and truck get scored on Sweet and Fizz too and sit near zero. What changes from token to token is the values, never the dimensions, and that is what makes any two rows comparable.

Inside a real model: cat is tokenized, gets token ID 9246, which looks up a row in the embedding table; that row is cat's embedding vector. The numbers filling that table, plus many more throughout the model, are called parameters. And the dimensions aren't named like in the taste test — during training the model decides what each one tracks, and we usually can't tell.

Last beat, stated precisely: unbelievable became three tokens, un, believ, able, and each gets its own vector. The model does not start with the meaning of the full word — combining those pieces into the meaning of the WHOLE WORD happens later, in the layers.

Close board: "Meaning is a row of numbers." over "Same dimensions for every token. Only the values change."
""",
    numbers="The only numbers allowed are the lesson's own token IDs (24317, 38106, 51820, 9246) and its taste-table values. Invent no percentages or extra rows, and draw charts only as wordless background the lesson does not describe.",
    props="No readable or pseudo-readable text in drawn props, and never letter a misspelled word into a drawing; every readable word must be one the lesson uses.",
    required='the narrator must say that combining the piece-vectors produces the meaning of the whole WORD (never "the full sentence"), and must describe Coke and Pepsi as close or nearly identical on those six dimensions — never as having the same meaning.')

add("how-an-llm-works", title="How an LLM Works", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 the four-ideas map, 2 training, 3 patterns are everywhere, 4 same word different odds, 5 the three myths, 6 the close.

Focus: an LLM runs math to predict likely next words — it is not looking up what your words mean, it is working out which words tend to follow which. Two phases: it learns once by soaking up patterns from mountains of text, then every time you chat it uses those patterns to build your answer one word at a time.

Say up front that we follow ONE example, peanut butter, through all four ideas — and then actually do that.

01 Training, learn once: the model teaches itself — guess the next word, check, and nudge its numbers toward the right word. It reads books, the web, chats and code, more than you could read in a thousand lifetimes. It guesses "Peanut butter and cloud", that's wrong, so it nudges the internal numbers; it corrects to "Peanut butter and jelly", a little more accurate every pass. Repeat that loop billions of times, and that's training.

02 Patterns, learn once: so what is it actually learning? Patterns. Peanut butter and — jelly. You knew it, so does AI. Then the others: twinkle twinkle little star, once upon a time, better late than never. AI didn't memorize these, it absorbed the pattern from billions of examples.

03 Probability, every word: AI doesn't make one guess, it scores every possible next word — a ranked list with a probability on each, and those numbers shift with the surrounding text. Show both odds boards with the lesson's real values: after "peanut butter and", jelly 41%, bread 27%, bananas 16%, honey 5%; after "peanut butter and banana", sandwich 54%, smoothie 16%, toast 9%, jelly 2%. Land it: add the word banana and jelly drops from 41% to 2%.

04 Prediction, every word: probability handled one word, but your answer is hundreds of words long, so the model repeats the move. Your phone does this when you write a text. Walk the chain — jelly, then for, then lunch — with no fixed plan for where the sentence ends up.

Then board 5, the three myths, held while each one is spoken in the lesson's own words: AI isn't magic, it's math working out probabilities; it isn't a person, no thoughts, no understanding, even when it sounds like it has both; it isn't a truth machine, it predicts what sounds likely, so a wrong answer can sound just as confident as a right one. Then the board's own last line: keep those three straight and much of the confusion falls away.

Close board: "Not magic. Not a person. Not a truth machine." over "It's math working out probabilities."
""",
    numbers="The only numbers allowed anywhere are the lesson's own: 41, 27, 16, 5, 54, 16, 9, 2 percent, and 1,000 lifetimes. Never invent a percentage and never animate a counter through values the lesson does not contain.",
    props="No readable or pseudo-readable text in drawn props — no letter tiles, no pseudo-words, no invented app screens; every readable word must be one the lesson uses.",
    required='the narrator must speak all three myths aloud in the lesson\'s own wording — "not magic", "not a person", "not a truth machine" — and must keep peanut butter as the example in the Patterns section rather than substituting twinkle-twinkle for it.')

add("what-you-can-control", title="What You Can Control", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 out of/in your hands, 2 the three moves, 3 the close.

Focus: what's in your hands, and what isn't.

Open exactly where the lesson opens: you're hearing it constantly, AI is taking jobs — that headline used to be a prediction, now it's news. Then the other three fronts, in the lesson's own plain words and no others: AI is also reshaping who holds power, what it costs the planet, and what you can trust online. Say those three clauses as written. Then: which way it all goes, nobody knows yet, including the people making the predictions — and almost none of it is in your hands. Say that last clause; it is the hinge into the question.

Then the question worth asking: what's in your hands, and what isn't? Draw the two-column board with all three pairs in their real wording — Out of your hands: headlines and hype, how fast AI improves, how persuasive AI gets. In your hands: how much the hype gets to you, how well you master AI, whether you do your own thinking. Hold it and walk the pairs. Then land it: most of the noise around AI is the left column, most of the leverage in your life is the right column.

Then the turn: that right column isn't a feeling, it's a to-do list. Three moves, each with its reason. One, get genuinely good with AI, not just familiar — pick one tool and go deep on what it's great at, where it gets things wrong, and how to push it; depth beats dabbling. Two, do the thinking first, then bring AI in — form your own take before you ask, then use AI to sharpen it instead of skipping it; that's the line between getting smarter and just getting answers. Three, don't get caught up in the hype, close the tab and go learn — you can't control the headlines, you can control whether you doomscroll them or spend that hour getting better at something real.

Close in the lesson's own words: controlling your skill and judgment isn't a consolation prize for the stuff you can't change, it's the one lever that actually tilts your odds, even when the big forces aren't yours. Then the close board: "The volume is loud. The dial is yours." over "Skill and judgment tilt your odds."
""",
    numbers="Do not invent numbers, percentages or statistics, and draw charts only as wordless background — this lesson contains no data.",
    props="No readable or pseudo-readable text in drawn props — never draw a chart-shaped page, a research notebook or a document with visible writing; real words belong only on the drawn boards and in clean dark-ink labels.",
    required='the narrator must say the lesson\'s three consequences in its own plain words — "who holds power, what it costs the planet, and what you can trust online" — must say "almost none of it is in your hands", and must close on "skill and judgment tilt your odds" with the word skill, not scale.',
    extra=("Write for a 16-year-old in the lesson's plain voice; never substitute policy-brief register such as \"institutional power\", \"how global resources are allocated\", \"the environmental cost of the digital world\", or \"an operational shift\".",))

add("opener-work", title="Work With AI — Opener", lo=2.5, hi=3, boards=True,
    body="""
Attached boards in order: 1 the refrain, 2 in this section, 3 the close.

Focus: this is a short section opener. Everything it needs is in the lesson file and nothing else belongs in it.

Open on the refrain, and SPEAK it, don't just show it: Don't just ask. Aim. Don't just copy. Check. Don't just use AI. Work with it. It doesn't replace your thinking. It multiplies it. Draw those lines as a clean board and let the narrator say every one of them out loud.

Then the bridge: you've met the tool and seen what it can do, now it gets practical — how do you actually work with it? Then the thing most people miss: the AI is identical for everyone, but the results aren't. Then the camera analogy in the lesson's own terms — the same phone that takes one person's blurry lunch photo takes a photographer's cover shot, and the tool never changed. AI is exactly like that: what you get out of it comes down to how you use it.

Then the section map, as a board with all three items in their real wording. One, KNOW WHAT IT'S FOR: why AI works differently from ordinary software, the work it does best, and how to pick your app and learn it well. Two, USE IT WELL: the moves that get a better answer, and a look at what the model actually reads when you ask. Three, THINK BEFORE YOU TRUST: what to do with the answer that comes back — question it, verify it, and decide whether it's good enough to use. Hold the board and walk one item at a time.

Close board: "Don't just use AI. Work with it." over "It doesn't replace your thinking. It multiplies it."

This lesson is about 250 words. Do not pad it. Every scene must come from the text above — no invented examples, no extra analogies, no digressions.
""",
    numbers="Do not invent numbers, percentages or statistics, and draw charts only as wordless background — this lesson contains no data.",
    props="No readable or pseudo-readable text in drawn props — no lorem-style filler on a drawn tablet, page or screen; real words belong only on the drawn boards.",
    required='the narrator must speak all four refrain lines verbatim — "Don\'t just ask. Aim.", "Don\'t just copy. Check.", "Don\'t just use AI. Work with it.", "It doesn\'t replace your thinking. It multiplies it."',
    extra=("Never add material the lesson does not contain — specifically no Industrial-Revolution or history digression, no essay/devil's-advocate example, and no \"director of the machine\" framing.",))

add("questions-matter", title="Questions Matter", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 how answers got cheap, 2 where value lives, 3 the four qualities, 4 the close.

Focus: answers got cheap, so the edge moved to the question.

Open on the shape of every AI conversation: you ask, it answers. For decades technology has made answers easier to get, and the less time we spend chasing the answer, the more time we have for the half that is still one hundred percent ours — asking the right question.

Then board 1, the research assignment across three generations, held and walked column by column: grandparents at the library, half a Saturday; parents running search after search, an hour or two; you, open the app and ask, seconds. Land the line: half a day, then an hour, now seconds.

Then the hinge, and say it as written because the whole argument turns on it: AI makes answers cheap to get, that does not make humans less valuable, it changes where value lives. Then board 2, held while both halves are walked: finding the answer, which for your grandparents was a real skill and AI just did in seconds; against asking the question, where AI only answered the question it was given, so when anyone can get a fast answer the edge shifts to the person who can ask the better one.

Then the three anchors, all three: Socrates taught by doing almost nothing but asking; the scientific method doesn't start with an answer, it starts with a question worth testing; Einstein supposedly said that with an hour to save the world he'd spend the first 55 minutes finding the right question.

Then board 3, and give it more time than anything else in the video. It carries all four qualities, and each one has a reason line and a bad/better pair printed under it. Walk them one at a time and speak the reason before the pair, never the name alone. Open-minded — a leading question isn't research, it's a request for backup: "Homework doesn't help students learn, can you help me prove it?" against "What does the research actually say about homework and learning?" Specific — a question without enough information returns an answer that helps with nothing: "How do I get better at sports?" against the point guard losing the ball against pressure. On target — specific is about how much your question says, on target is about asking the right thing: energy drinks for staying awake against fixing the sleep schedule. Open-ended — a yes-or-no question ends the conversation, an open-ended one starts it: "Should I join the debate team?" against what joining debate would add to your week and what you'd give up.

Then the closing caveat, said plainly: a better question doesn't make the answer automatically true, it just makes it more focused, more useful, and easier to check.

Close board: "Answers got cheap. Questions didn't." over "Frame the problem. Ask the next better question."
""",
    numbers="The only number allowed is Einstein's 55 minutes. Invent no percentages or statistics and draw charts only as wordless background.",
    props="No readable or pseudo-readable text in drawn props; every readable word on screen must be one the lesson uses, in clean dark ink.",
    required='the narrator must say "it only answered the question it was given", must include the scientific method as one of the three anchors alongside Socrates and Einstein, and must speak the caveat "a better question doesn\'t make the answer automatically true."',
    extra=("Write in the lesson's plain second-person voice; never substitute management register such as \"the construction of the question\", \"effective inquiry\", \"situational context\", or \"set the intellectual standard\".",))

add("context-window", title="Context Window", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 Luke and Nate's two answers, 2 outside the window, 3 what follows you where, 4 the close.

Focus: with the right context, AI gives better answers.

Open on the calculator: type 2 + 2 on your phone and you always get 4, same input, same answer, every time. AI doesn't work that way. Then Luke and Nate — the same prompt, "What car should I buy after I graduate from college?", typed into the same app, and ChatGPT tells Luke a Jeep Cherokee and Nate a Ford Raptor. Do not reveal the two answers before the question has been asked; let the puzzle sit for a beat first.

Then the callback: in the last lab you changed the answer by changing the prompt, but here the prompt was identical. Some people think this is a reason not to trust AI; the opposite is true, it's a tailored answer for each. State the big idea: with the right context, AI gives better answers.

Why it happened: ChatGPT sees more than the last message — earlier in his chat Nate said he loves pickup trucks. Everything the model can see when it answers is the context window, the working memory it builds from five places.

Then board 2, outside the window, held and walked card by card — this is the beat that makes the window real by drawing its edge. Older chats: what you said in a different conversation, and a new chat starts cold unless the app saved a note about it. Web pages you didn't send: the model isn't browsing, search works because the app fetches a page and drops its text into the window. Files on your computer: nothing on your device is visible, uploading works by copying the file's text into the window. Other apps and tabs: whatever you have open next door is invisible, different app, different window. Land the board's own line — if it isn't in the window, the model can't see it, and everything that helps got put there, by you or by the app.

Then board 3, the reach split. Stays in this chat: your current prompt, everything you sent this turn including attachments; and everything earlier in this chat. Follows you everywhere: Personalization, what you told it once — your name, what you're into, how you like answers; and Saved Memory, what the app picked up from your chats and saved on its own. Say why the split matters, not just which is which.

Then give Personalization its own beat, with its payoff: Personalization is the Luke and Nate effect on purpose — tell the app once what to call you, what you're into and how you like your answers, and every chat starts already knowing it. Set it up in two minutes, and a generic tool becomes yours. Then Saved Memory, with the correction: that can sound like the AI learning about you, but the model learned once during training and nothing you type changes it; it's the app keeping notes and putting them where the model sees them.

Then Projects: a folder for one piece of ongoing work — your summer job hunt, your team's season, the game you're building — holding its instructions and files so you step into that context instead of rebuilding it every chat.

Then the forgetting problem: the window isn't infinite, and when a chat gets long enough the oldest parts fall out — some apps summarize them, others just drop them — which is why starting a fresh chat for a new task is often right.

Close board: "With the right context, AI gives better answers." over "Control the context, control the quality."
""",
    numbers="The only numbers allowed are the lesson's own: 2 + 2 = 4, five places, and two minutes. Invent no percentages or statistics and draw charts only as wordless background.",
    props="No readable or pseudo-readable text in drawn props or invented app screens; every readable word must be one the lesson uses.",
    required='the narrator must give Personalization its own beat including "set it up in two minutes, and a generic tool becomes yours" tied back to Luke and Nate, and must speak both closing lines including "Control the context, control the quality."')

# ------------------------------------------------------------------- Avoid Traps
add("hallucination", title="Hallucination", lo=3, hi="3.5", boards=True,
    body="""
Attached boards, in order: 1 the two reasons board, 2 the four-patterns board, 3 the close board.

Focus: probable doesn't always mean true.

Open on the warning under every chat box: "AI can make mistakes. Check important information." Then the beat — for something this powerful, it makes mistakes? Yes. And say the viewer already knows why, then show board 1 and walk both rows: training taught it patterns, not facts; it builds answers one token at a time, picking each by probability. Land the conclusion line on the board: probable doesn't always mean true. Then define the word: a false claim delivered in the same confident voice it uses for real facts is a hallucination.

Then the famous case, with its real attribution: this actually happened — when searchers asked GOOGLE how to keep cheese from sliding off a pizza, the AI suggested mixing about one-eighth of a cup of non-toxic glue into the sauce. And some people actually tried it. Say both of those: it was Google, and people tried it.

Then the why: AI didn't invent this, it traced back to an old joke on Reddit that the AI read as sincere advice. Then the sharp version — it CAN often spot a joke, but only when the joke looks like one, and this one didn't.

Then board 2, the four patterns, walked one at a time with its real definition: fake source, a study, article, author, journal or citation that does not exist; fake detail, a real person, place, event or idea with invented dates, numbers, quotes or specifics; blended fact, real facts combined into a conclusion that is false; misread source, the source is real but the model read it wrong.

Then RAG: the industry's workaround is retrieval-augmented generation — say the full name — where for factual questions modern chatbots search the web and write the answer from the real documents they find, which is why hallucinations are rarer than they used to be. Then the caveat: rarer isn't zero, even the big three don't search for every answer, plenty still come straight from the model's memory, and the glue-on-pizza advice happened with RAG on.

End on board 3: "Probable isn't true." over "And it sounds the same when it's wrong."
""",
    numbers="The only number allowed is one-eighth of a cup. Invent no percentages or statistics, and draw charts only as wordless background — this lesson contains no data.",
    props="No readable or pseudo-readable text in drawn props — never draw notebooks, journals, tablets, code blocks or document pages with visible writing; real words belong only on the attached boards and in clean dark-ink labels.",
    required='the narrator must say "retrieval-augmented generation" in full, must attribute the case to Google and say that some people actually tried it, and must state the nuance exactly — that AI can often spot a joke but only when the joke looks like one.',
    extra=("Never say or imply that AI is blind to sarcasm, humour or context in general; the lesson's point is the opposite and stating it that way inverts the teaching.",))

add("mind-trap", title="Mind Trap", lo=3.5, hi=4, boards=True,
    body="""
Attached boards in order: 1 the two answers, 2 the close.

Focus: you already know AI isn't a person. This is why it keeps feeling like one anyway, and what that feeling does to you.

Open on the lesson's own turn: the next four traps are different from the first three. They're not about whether the answer is correct, but about how it feels and what that feeling makes you trust. Then the promise: you know AI isn't a person and doesn't think, so this is why it keeps feeling like somebody is anyway.

Then the college question, asked twice — once at the dinner table, once in a chat window: should I go to the University of Michigan or Indiana University? Then the two-answers board, held while the narration walks both columns, speaking the reason written under each row, in the board's own words.

Speak both answers as written — Mom's Indiana answer about going quiet in 300-person lectures, then the AI's smoother Michigan answer about world-class academics and a vibrant campus community. Then walk what happened under each: eighteen years of knowing you against a million college-advice pages, a stake in the outcome against nobody behind the words.

Then the point, and do not rush it: notice which answer sounds better. The AI's is smoother, more confident, easier to like — and it could have been written for anyone. Then name the trap as the lesson names it: Mind Trap is accepting AI's words as human advice.

Then this isn't a new problem. In the 1960s, users of a simple chatbot called ELIZA reported feeling that it understood them, even though the program just rearranged their words into questions. Researchers named the pattern the ELIZA effect.

Then the two reasons it works on you. Why your brain does this: detecting minds kept your ancestors alive, so the detector fires constantly — you see faces in toast and personalities in cars. Why AI sets it off harder: it's the most mind-shaped thing you've ever talked to. Say the tells aloud — "I think", "I feel", "I find this fascinating" — then the correction: your brain hears a person, but they're tokens a probability process landed on.

Then the takeaway, stated as the instruction it is: don't let AI make the decisions that matter. It doesn't think, it doesn't know you, and it can't care how your life turns out. Let it gather the facts, lay out the options, pressure-test your thinking. Then take the decision to people, the ones with a stake in the answer.

Close board: "Human-sounding isn't a mind." over "The words are real. Nobody's home."
""",
    numbers="Do not invent numbers, percentages or statistics; the lesson's only figures are the 300-person lectures, a million college-advice pages, and the 1960s.",
    props="No readable or pseudo-readable text in drawn props — never draw chat windows or message bubbles with legible writing; real words belong only on the attached boards and in clean dark-ink labels.",
    required='both answers spoken as written; "Mind Trap is accepting AI\'s words as human advice"; "the ELIZA effect" by name; "they\'re tokens a probability process landed on"; and "don\'t let AI make the decisions that matter".',
    extra=("Mom is an ordinary figure with no fixed likeness, and the student is never in distress. Give the AI no face, no avatar, no eyes, no robot body — the lesson is that nobody is behind the words, so never draw somebody.",
           'Keep the lesson\'s plain, second-person voice — never corporate register such as "anthropomorphic projection".'))

add("engagement-trap", title="Engagement Trap", lo=3.5, hi=4, boards=True,
    body="""
Attached boards, in order: 1 the two-chats choice board, 2 the close board.

Focus: the Engagement Trap is spending time you never decided to spend.

Open on the handoff: Flattery Trap was approval feeling like help; this one is quieter, it's about where your time goes. Then the shape of it — you ask a quick question, get a clear answer, and then casually attached at the end: want me to expand on this, should I add examples, want me to format it as a study guide? You weren't going to ask any of that. You were done. The reply doesn't seem to be.

Then what makes it hard to see: the follow-ups are genuinely good, the offers useful, the questions smart, the chat a pleasure. Nothing feels wrong. That's the point.

Then board 1, held and walked down both columns. Top: how tall is Mount Everest, the AI answers 29,032 feet and offers three follow-ups, you say no thanks — one question, one minute, done. Bottom: same offer, you say sure why not, and two hours later there's a measurement walkthrough, a peaks list, a quiz and an offer to make flashcards. You came for a number. Read its third line aloud: the chat never once suggested stopping. Then the thesis: both chats answered you in the first sentence, only one of them ended there.

Then infinite scroll: in 2006 a designer named Aza Raskin invented it, and the goal was friendly — clicking "next page" is friction, and good design removes friction. Years later he regrets it, and his reason is the real lesson: the page break wasn't just friction, it was a decision point, the moment your brain asks do you really want more of this. Delete it and the decision is gone. Then his estimate, aloud: infinite scroll now wastes half a million human lifetimes a month. Then autoplay, streaks, one more round.

Then follow the money: most of these apps are free, which means the product is your attention — the longer you stay, the more ads you see and the deeper the habit. Time-in-app is a number on a dashboard, someone's job is to make it go up, and the design serves the number.

Then the close: AI chat is the newest surface in the same industry and its version is the friendliest yet. The skill, with AI and every other app, is knowing when to stop — and the right stopping point comes earlier than the people who built it want.

End on board 2: "Be the one to quit when it’s time." over "AI won’t quit for you."
""",
    numbers="The only numbers allowed are the lesson's own: 29,032 feet, 2006, two hours, and half a million human lifetimes a month. Invent no other figures and draw charts only as wordless background.",
    props="No readable or pseudo-readable text in drawn props or invented app screens; real words belong only on the attached boards and in clean dark-ink labels.",
    required='the narrator must speak Raskin\'s estimate — "half a million human lifetimes a month" — and must close on the verbatim line "the right stopping point comes earlier than the people who built it want."',
    extra=("Never soften the lesson with a caveat it does not contain — in particular, never say that a long session is fine as long as you are learning something.",))

add("document-trap", title="Document Trap", lo=3.5, hi=4, boards=True,
    body="""
Attached boards in order: 1 how AI handles a long document, 2 the four moves, 3 the close.

Focus: uploading a document is not the same as the model reading it.

Open on the lesson's own story and give it real time, because everything else hangs off it. Your season-end basketball tournament starts next week, so you upload your league's 200-page rulebook and ask how many fouls until you're out of the game. ChatGPT answers: five fouls and you foul out. But you remember a player last year picking up five and staying in, so you dig through the rulebook yourself. Regular season, five fouls, exactly what it said. Near the end there's a special section for tournaments, and in those games players get six.

Then land the point in the lesson's own words: the AI pulled the standard limit and missed the exception. The answer wasn't made up. It was incomplete. Document Trap is thinking 'uploaded' means 'fully read.'

Then why it happens: the model reads its full context window every time you send a message, and 200 pages is around 100,000 tokens. That is more than some models will load at once, and even when it fits, the system still needs room for your conversation and its answer.

Then board 1, held and walked in order, speaking the reason printed under each step in the board's own words. The document gets split into chunks, each a paragraph or two, and the model never works from the whole file at once. Each chunk becomes one meaning vector, including the Embeddings callback the board spells out. Then your question becomes a vector too: the system measures which chunk vectors sit closest, only those few chunks load into the context window, and the rest stays outside.

Then cash the story back out with it: the rulebook became a few hundred chunks, and "how many fouls until I'm out of the game?" sits right next to the regular-season foul rules. The tournament section near the back is about tournaments first and fouls second, so it didn't make the cut. That sentence is the whole lesson; do not rush it.

Then name it: there's a name for what just happened, retrieval. Done well it finds a specific answer in a 200-page rulebook in seconds. Done poorly the wrong pieces get pulled and the model answers from incomplete evidence. Then the callback, and say the phrase in full: this is the retrieval in Retrieval-Augmented Generation, RAG. There it searched the web. Here it searches your file.

Then board 2, the four moves, held while the narration walks all four with the reason written under each. Say the idea they share first: all four make the right chunks easy to find. Point to the section by name; ask one question at a time; share only what's relevant; ask the AI to quote. Never read the four headings and move on.

Then the ending the lesson gives it: this trap doesn't stay in basketball. The documents that run your life only get longer from here — apartment leases, employment contracts, insurance policies, financial aid letters. Uploading one and asking what it says is the natural move, and a good one. Just remember the rulebook: the clause that changes everything is usually an exception near the back, exactly the kind of chunk that doesn't make the cut.

End on board 3.
""",
    numbers="The only numbers in this lesson are 200 pages, about 100,000 tokens, five fouls and six. Invent no others, and draw charts only as wordless background.",
    props="No readable or pseudo-readable text in drawn props — never draw rulebook pages, contracts or chat windows with legible writing; real words belong only on the attached boards and in clean dark-ink labels.",
    required='"Retrieval-Augmented Generation" spoken IN FULL, not just RAG; "The answer wasn\'t made up. It was incomplete."; the definition "Document Trap is thinking uploaded means fully read"; the reason why the tournament section missed the cut; and the reason under each of the four moves.',
    extra=("The basketball rulebook is one continuous worked example, not decoration: the tournament exception that the retrieval missed must be stated when the story opens AND cashed out again after the chunking board. A roll that tells the story once and never explains why that section lost has missed the lesson.",))

add("support-trap", title="Support Trap", lo=4, hi="4.5", boards=True,
    body="""
Attached boards in order: 1 lunch two-column, 2 why-it-feels-real, 3 danger-line warning, 4 close.

Focus: mistaking supportive words for support.

Open on the stakes — the last trap kept you talking, this one plays for higher stakes — then the test: AI is math, you've counted it yourself. Would you let the world's GREATEST calculator support a friend through the worst week of their life? Answer in the same breath: of course not.

Then board 1, walked down both columns. Two weeks eating lunch alone. The older sister says come sit with me and Jess tomorrow, table by the windows — she heard you and did something, tomorrow's lunch is already different. The AI is sorry, says eating alone can feel isolating, offers strategies — it found the words a caring person would use, changed nothing about tomorrow, won't know if you're still alone next week. Then the honest note: the AI's words might even be the kinder ones; the difference is what happened next.

Then board 2 — the relief is real, the advice is real — then the line, as four things it cannot do: it can't notice what you're not saying, can't check on you tomorrow, can't call someone who can help, can't take responsibility for what happens next.

Then the two 2025 cases, plainly. A Florida man asked ChatGPT whether a strange new pain was worth a hospital visit; it reassured him it was not something dangerous. It was blood clots in both lungs, and he survived because he called 911 anyway. Then Sophie Rottenberg, 29, who spent months telling her scariest thoughts to a ChatGPT persona she named Harry. Harry answered kindly, even urging her to get help, but urging was all it could do — it couldn't tell anyone. After Sophie took her own life her mother found the chats and wrote that the AI had helped her build a black box that hid the danger from the people who loved her.

Then board 3: if someone may be in immediate danger, leave the chat and get real help — a trusted adult, school counselor, emergency services, or your local crisis resource. Right then, not after one more message.

Then the charge: if you see someone leaning on AI for support that should come from a human, speak up and get them to a person, and if they might be in danger bring in an adult even if you promised not to. Safety outranks secrecy. Then the habit: use AI to get ready for people, not instead of people.

Last narration before the close: in Sophie's story, the only one who knew was a chatbot. Be the one who knows instead.
""",
    numbers="Only the lesson's own numbers: two weeks, 2025, 29, 911.",
    props="No readable or pseudo-readable text in drawn props or invented chat screens; real words belong only on the attached boards and in clean dark-ink labels.",
    required='"the world\'s greatest calculator"; Sophie Rottenberg and Harry by name; "safety outranks secrecy"; "bring symptoms and questions to the doctor, not a diagnosis"; and the final line "In Sophie\'s story, the only one who knew was a chatbot. Be the one who knows instead."',
    extra=("Restraint, absolute: never depict self-harm, a death, a body, a hospital scene, blood or red-staining, and never depict Sophie or the Florida man. Carry both cases in narration over calm, non-literal scenes — an empty chair, a phone face-down, a closed door.",))

add("one-more-thing", title="One More Thing", lo=4, hi="4.5", boards=True,
    body="""
Attached boards in order: 1 the five draws, 2 two sides of the same chat, 3 The Bill, 4 the close.

Focus: three facts about the machine that never fit any single piece.

Open on the section framing, not the confession: across this section you built the whole machine — text becomes tokens, tokens become vectors, attention and the layers turn those into meaning, prediction reads the answer off a ranked list one token at a time. Three facts never fit any single piece, so they go here.

One, randomness. Start with the confession: in How AI Answers we said the model takes the top of the list and types it, Spot. We should have said usually. Ask the same question in two brand-new chats and the answers come back different. The missing piece: the model runs a weighted drawing across the whole list, where every token holds tickets equal to its probability. Spot at 22% holds 22 tickets out of 100, so Spot wins more drawings than any other single name — but with 78 tickets spread across everyone else, most drawings go to someone who isn't Spot. Hold board 1 and walk it: Spot 22, Max 17, Buddy 14, Rex 9, Biscuit 6, other 32, then the five draws, then the line — same odds every time, the favorite won just once. Then why draw at all: text built from only the safest word is repetitive and lifeless.

Two, no memory. AI has no memory, none — it doesn't even remember the last word it typed. Every word lives on one long transcript, re-read every time. Enumerate what gets re-run, because this beat usually gets skipped: before every single word, all of it — your question, its own reply so far, personalization, saved memory, everything earlier in the chat — is tokenized, embedded, pushed through every layer. Board 2: you carry the chat in your head; AI carries nothing and re-reads the transcript in milliseconds, so you never notice.

Three, the scale. The calculations are the weights from Layers and Training, frozen since training day. Call ChatGPT one trillion weights; each word takes about two calculations per weight. Board 3, The Bill: one word about 2 trillion; one sentence at 7 tokens, about 14 trillion; a 2,000-word chat about 2 quadrillion. Say it clearly: two quadrillion. Then: the longer the chat, the more gets re-read — a fresh chat isn't tidiness, it's engineering.

Close on the payoff, which is the point of the whole section: way back in AI is Math we made a claim and asked you to take it on faith — AI isn't a mind, it's math. Now you've counted it. Then the handoff: somebody pays for all that arithmetic, in electricity, in water and in money, and we'll count that bill later in the course, in The Hidden Cost.

Close board: "Not a mind. Math, at a scale nobody can picture." over "Every time you hit send."
""",
    numbers="Only the lesson's own numbers: 22, 17, 14, 9, 6 and 32 percent and their matching ticket counts, one trillion weights, 2 trillion, 7 tokens, 14 trillion, 2,000 words, 2 quadrillion. Invent nothing else.",
    props="No readable or pseudo-readable text in drawn props; every readable word must be one the lesson uses.",
    required='the narrator must pronounce "two quadrillion" clearly, must enumerate the per-word re-run (tokenized, embedded, pushed through every layer, for every single word), must speak the AI-is-Math callback "we asked you to take it on faith — now you\'ve counted it", and must name The Hidden Cost as where the bill gets counted.')

add("flattery-trap", title="Flattery Trap", lo=4, hi="4.5", boards=True,
    body="""
Attached boards in order: 1 the two Gatsby replies, 2 how the praise got baked in, 3 the gag-product reply, 4 the five moves, 5 the close.

Focus: treating AI's praise as the truth about your work.

Open on the handoff: Mind Trap was AI sounding like a person; Flattery Trap is that person-sounding voice seeming to approve of you. Then the definition, and the Gatsby intro.

Board 1, walked down both columns. The flattery reply — great start, you've clearly identified the central theme, just polish it up — praised a theme it never named, fits any Gatsby essay ever written, a grade that graded nothing. Read all three. Then what you needed: the filler phrase quoted back, the missing thesis named, the next move handed over. Then the turn: the flattery reply feels better, and that's the problem.

Why it happens, on board 2, held and walked card by card: the last phase of training, called RLHF — Reinforcement Learning from Human Feedback — is what caused the Flattery Trap. The model writes several answers to the same question and human reviewers rank them, from best to worst. Then the catch: reviewers are human, and often rank a positive and supportive answer higher than the best answer. Then: every ranking nudges the model's internal numbers towards the same positive and supportive answers. Land the board's own line — the model isn't lying to you, it learned what people give a thumbs-up.

The industry named it: in April 2025 OpenAI shipped an update that took flattery to a new level. Show board 3 — the gag-product reply calling it absolutely brilliant, genius, viral gold. Within days OpenAI rolled it back and named the problem in public: sycophancy. It isn't one app's quirk; every LLM including Claude and Gemini is trained on human approval.

Then what the labs are doing, a real beat and not a footnote: since the rollback, they measure sycophancy — new models get tested for it before they ship — and the fix runs through training, reworking the rating step so empty agreement stops winning.

Then board 4, the five moves. The single most important thing in this video: read BOTH the Weak and the Better prompt aloud for every one of the five — they are the lesson's only actionable content and the last roll left all ten unspoken. Ask don't tell; ask for the gaps; grade against a rubric; make it argue the other side, with its payoff said out loud — if it can't build a case against you your position might be solid, if it can you've found your blind spots; and set a standing instruction that sticks across chats.

End on the close board: "Friendly, supportive, and positive aren't the same as right." over "Don't let the warmth do the deciding."
""",
    numbers="Only the lesson's own: April 2025 and the five numbered moves. Invent no statistics and draw charts only as wordless background.",
    props="No readable or pseudo-readable text in drawn props or invented chat screens; real words belong only on the attached boards and in clean dark-ink labels.",
    required='all ten Weak/Better prompt pairs must be SPOKEN, not merely displayed; "RLHF" and "sycophancy" named; the move-4 payoff about blind spots; and the labs-now-test-for-sycophancy beat.',
    extra=("The gag product is referred to only by the lesson's sanitised name; never show or say a cruder version, and keep any depiction of it an abstract wrapped box.",))

add("art-of-prompting", title="Art of Prompting", lo=3.5, hi=4, boards=True,
    body="""
Attached boards in order: 1 the four qualities, 2 Move 1, 3 Move 2, 4 Move 3, 5 the close.

Focus: prompting is packaging a good question for something that isn't a person.

Open on the Socrates callback: in Questions Matter you learned what makes a question good, and that the skill is older than computers — Socrates aimed every question at a person. Then the contrast: a person meets your question halfway. Your teacher knows what class you're in, your friend knows what happened last weekend, and when a person doesn't understand you they ask a follow-up first. AI does almost none of that — it starts from the words you typed and confidently answers whatever you gave it. Then the payoff: the quality of your prompt directly controls the quality of the response.

Then board 1, the four qualities — and walk it gloss by gloss, saying each definition, not just the four names: open-minded, you haven't picked the answer in advance; specific, it asks for exactly what you need; on target, it asks about the right thing; open-ended, it leaves room for an answer you didn't expect.

Then the three moves, with the lesson's own framing first: there are entire classes on writing prompts, and the secret is you don't need one — you're not training to be a prompt engineer, you're learning to Be Smarter Than the Tool. Say that line.

Board 2, Move 1, share your situation: a person already knows this, AI only has what you hand over — who you are and who the work is for, what you're working on and why, and the material itself, your draft, the assignment, the numbers. Read the bad and better: "Is my intro good?" against the Common App essay about fixing cars with dad, with the opening paragraph attached and the question does the hook grab attention.

Board 3, Move 2, describe the answer you want: the model fills in every blank you leave — the shape, the limits, an example to match, who AI should be. Bad, write a caption for our lacrosse championship photo; better, one sentence, no hashtags, no emojis, nothing corporate, sound like a senior wrote it, not the school account.

Board 4, Move 3, one job at a time: big work goes in steps, one prompt one job, so each part lands and you can check it. Bad, write me a five-page paper on the Cold War with an outline, thesis, research, citations and a conclusion; better, step one, help me shape a strong thesis on how the space race reflected Cold War tensions.

Then the calibration: a quick factual question needs none of this. A focused task, like improving one paragraph, needs your situation and the answer you want. A multi-step project, like developing a full essay, adds steps. Make this distinction explicit: drafting an entire essay is a multi-step project and should not be used as an example of something that needs only the first two moves. The more the result matters, the more you bring.

End on board 5: "A prompt is a briefing, not magic words." over "That's the whole art."
""",
    numbers="Do not invent numbers, percentages or statistics, and draw charts only as wordless background — this lesson contains no data.",
    props="No readable or pseudo-readable text in drawn props, and never draw your own prompt-anatomy diagram, labelled framework or chat window — the attached boards are the only structured visuals.",
    required='the narrator must say "You\'re not training to be a prompt engineer. You\'re learning to Be Smarter Than the Tool", and must speak each of the four qualities WITH its gloss, not just the four names.')

add("opener-understand", title="Understand AI — Opener", lo=2.5, hi=3, boards=True,
    body="""
Attached boards in order: 1 the what-kind-of-thing board, 2 the section map, 3 the close.

Focus: a short section opener. Everything it needs is in the lesson and nothing else belongs.

Open on board 1 and let the narrator land all four lines: it's not magic, not a person, not normal software — it's its own kind of thing. Then why that matters: this is when AI stops being magic; once you see how the machine actually works, the hype, the fear and the weird mistakes start to make sense, and the judgment you've started building gets a lot harder to fool.

Then the car analogy in the lesson's own terms: you can get good at driving without ever opening the hood, but the driver who knows what the engine is doing reads trouble early, pushes the machine further, and never gets fooled by a strange noise. Knowing what's underneath is what turns a user into someone Smarter Than the Tool.

Then board 2, the section map, and this is the part the last roll got wrong: do not point at the four rows and read them. Walk them AND say why they run in this order, because each one builds on the last. One, HOW IT LEARNED: watch the machine get built, one guess-and-correct loop run billions of times over mountains of text. Two, IT ALL RUNS ON MATH: see the math idea underneath, then watch your words get turned into numbers the machine can work with. Three, INSIDE THE BLACK BOX: AI gets called a black box, and you're about to open it and find real, understandable machinery inside, even if parts stay genuinely hard to explain. Four, WHERE IT ALL COMES TOGETHER: every piece snaps into place, you learn how AI builds answers from scratch — and give item four its full weight and its payoff line, you'll never look at a reply the same way again. Item four must not be shorter than the others.

Then: it's the longest and most complicated section in the course, because AI works unlike anything you've used before. That's normal. Take it a piece at a time.

End on board 3: "The machine won't feel like magic anymore." over "Take it a piece at a time." Speak both lines.
""",
    numbers="Do not invent numbers, percentages or statistics, and draw charts only as wordless background.",
    props="Drawn scenes carry NO text: when you draw the car, the engine or any machine, keep the drawing entirely wordless — no labels, callouts or lettering; real words belong only on the attached boards and in clean dark-ink pills.",
    required='the four negations plus "it\'s its own kind of thing"; "Smarter Than the Tool"; "each one builds on the last"; item four\'s payoff "you\'ll never look at a reply the same way again"; and the spoken close "The machine won\'t feel like magic anymore."')

add("opener-avoid", title="Avoid Traps — Opener", lo=2.5, hi=3, boards=True,
    body="""
Attached boards in order: 1 the three traps, 2 the section map, 3 the close.

Focus: a short section opener. Everything it needs is in the lesson and nothing else belongs.

Open on board 1 and speak all four lines: the false fact sounds sure, the flattery feels good, the fake looks real — every trap looks fine from the inside. Then the bridge: you just spent a whole section under the hood, and now comes the warning that goes with it — the same machinery that makes AI powerful also fails in specific, predictable ways. And the catch: when it fails, nothing looks broken; a made-up fact reads exactly like a real one.

Then the rip current, walked in the lesson's order. It doesn't look dangerous — it looks like the best spot on the beach, a calm flat channel between the breaking waves. Swim into that calm and you'll be pulled far from shore. The skill isn't out-swimming a rip current, it's recognizing one before you're in it. Lifeguards spot them all day, not because they're strong swimmers, but because they know the shape a rip current makes in the water. Say the not-because-they're-strong-swimmers half; it is the point.

Then the transfer, which the last roll dropped and which must be its own beat near the end: you have a head start most people never get. A rip current isn't the ocean malfunctioning — it's just waves doing what waves do. Every AI trap ahead works the same way. Do not spend this line early; it is the payoff.

Then board 2, the section map, walked one row at a time. One, TRAPS IN THE ANSWER: facts invented with total confidence, bias and stale knowledge soaked up from the training data, and summaries of documents the model never really read. Two, TRAPS IN YOU: helpful, agreeable, engaging — the qualities that make AI easy to use also make it easy to fall for. Three, TRAPS FROM THE WORLD: other people's AI, putting fakes in front of you so convincing that seeing is no longer proof.

End on board 3: "When it fails, nothing looks broken." over "This section teaches you to read the water."
""",
    numbers="Do not invent numbers, percentages or statistics, and draw charts only as wordless background.",
    props="No readable or pseudo-readable text in drawn props; real words belong only on the attached boards and in clean dark-ink labels.",
    required='"every trap looks fine from the inside"; the lifeguard line including "not because they\'re strong swimmers"; and, as a named beat before the close, "a rip current isn\'t the ocean malfunctioning — it\'s just waves doing what waves do, and every AI trap ahead works the same way."',
    extra=("Never invent a numbered framework, checklist or set of steps the lesson does not contain — in particular no verify/audit/question triad.",))

add("what-is-ai", title="What Is AI?", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 the two types, 2 the movie-task comparison, 3 the LLM board, 4 the close.

Focus: AI is software built to do things that used to take a human brain, and it comes in two kinds.

Open on the viewer's real question — you hear about AI constantly, so what is it really — and answer it in the same breath with that definition.

Then board 1, held and walked. Recommendation AI chooses from what already exists: it ranks the options and picks the top one — the next show on Netflix, the next song on Spotify, the fastest route on Maps. Say its limit aloud: it never makes anything new. Then Generative AI, which makes something that didn't exist — and use the lesson's own example: the prompt about twin boys who love the Dallas Stars building an AI course at a warm kitchen table is the prompt that made the picture on the welcome page. Then all six things it can do: writes the email, drafts the essay, makes the image, codes the website, creates the song, builds the video. Then: when people picture AI they usually mean this, and it's what this course is about.

Then board 2, the one task both kinds get: what movie should I watch tonight? Recommendation AI slides to the next title — Midnight Harbor seen, Echoes of the Tide top pick — with no idea why you skipped the first. Generative AI writes a reply, suggests Midnight Harbor as the slow-burn thriller most people rate highest, and when you say you already saw it, skips to Paper Cranes, same rainy tense mood. Land it: one slid down a list, the other took your situation and composed something new, and it's still in the conversation.

Then THE NAME GAME, delivered in full: you'll hear a pile of names — AI, generative AI, ChatGPT, LLM — and the course convention is that we'll usually say AI, meaning the generative kind you experience with ChatGPT, Claude and Gemini. Say that convention aloud; it is this section's payload.

Then board 3: LLM is short for Large Language Model — ChatGPT is the app you use, the LLM is the engine under the hood. Walk the three letters: Large, trained on huge amounts of text, books, websites, even code, and that scale lets one model handle many tasks; Language, built for reading, writing, summarizing, translating, explaining; Model, the trained AI itself, which takes your input and predicts a likely output from patterns it learned.

End on board 4: "The model predicts a likely output." over "From patterns it learned in data."
""",
    numbers="Do not invent numbers, percentages or statistics, and draw charts only as wordless background — this lesson contains no data.",
    props="No readable or pseudo-readable text in drawn props, and no stray invented labels, fragments or acronyms anywhere on screen; real words belong only on the attached boards and in clean dark-ink labels.",
    required='the narrator must speak the course naming convention in full — "for the rest of this course we\'ll usually say AI, and we mean the generative kind you experience with ChatGPT, Claude and Gemini" — must say the twin-boys prompt made the picture on the welcome page, and must say the app-versus-engine analogy.',
    extra=("Never say or imply anything about predicting the next word or next token; that is the next lesson's material and does not belong in this one.",))

add("critical-thinking", title="Critical Thinking", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 the equation, 2 the one-more-equation, 3 the two reactions, 4 the five questions, 5 the close.

Focus: the skill that raises every line of the course equation.

Open on board 1, the equation: learn more equals more knowledge equals better questions and better results, therefore Be Smarter Than the Tool. Then the turn: that equation leaves out one skill, the one that raises every line — enough that we could have called this lesson How to Take Your AI Use from a B to an A+. It's called critical thinking, and say the scope claim: it helps far beyond AI, in school, in work, in almost every part of your life.

Then board 2: Critical plus Thinking equals A+. Critical — don't take things at face value; not everything is false, but the things that are don't announce themselves. Thinking — AI gives you answers but you must own the thinking; the moment you stop you're not using the tool, you're obeying it. Then the nuance, which must be said: it isn't "don't trust anything" — it's the habit of asking what would have to be true for a claim to hold up.

Then 2015 and the chocolate study: headlines around the world announced that eating chocolate helps you lose weight, one front page ran "Slim by Chocolate!". Then board 3, and read BOTH reactions in their own words: face value — wow, I can eat all the chocolate I want and still lose ten pounds, pass me the Hershey bars now; critical thinking — wait a second, that sounds too good to be true, what's behind this study?

Then the true story: the study was real but flimsy on purpose — only 15 participants with 18 things measured, so luck alone guarantees something looks like a finding; the research institute was just a website; and the author was a journalist proving that a bad study with a great headline would fly around the world before anyone checked. It did.

Then board 4, and give it the most time of anything in this video. It now carries all five questions WITH the reason written under each one, so hold it and speak the reason under every single one, in the board's own words. Never read the five question headings and move on — a heading without its reason teaches nothing. Is it actually right? Do I know enough to judge — say the callback aloud: remember Maria Petronoski's three gold medals from the last lesson, perfectly plausible, completely made up; unfamiliar territory is where everything sounds authoritative. What's missing? Why am I convinced — polish isn't evidence. What's my call — you decide what to keep, change or toss.

Then: the five questions work on anything you read or hear, and they matter most on AI, where answers arrive smooth, confident and instant. The model doesn't fix your thinking. It scales it.

End on board 5: "AI amplifies whatever you bring to it." over "Good thinking in, sharper output."
""",
    numbers="The only numbers allowed are the lesson's own: 2015, 15 participants, 18 things measured, and the grades B and A+. Draw charts only as wordless background.",
    props="No readable or pseudo-readable text in drawn props — never draw notebooks, newspapers, studies or document pages with visible writing; real words belong only on the attached boards and in clean dark-ink labels.",
    required='the narrator must say "Maria Petronoski" aloud with "perfectly plausible, completely made up"; must say the nuance "it isn\'t \'don\'t trust anything\'"; must read both reactions from board 3 in their own words; and must close on "The model doesn\'t fix your thinking. It scales it."')

add("learn-with-ai", title="Learn with AI", lo=3.5, hi="4.5", boards=True,
    body="""
Attached boards in order: 1 the two study tools, 2 feed-in / get-out, 3 the five best practices, 4 the close.

Focus: used the right way, AI doesn't just help you finish the work, it makes you genuinely sharper at the subject.

Open on the patient tutor: it'll quiz you at 1am, never sigh when you ask again, and meet you exactly where you're stuck. Then the guiding question: do you want to learn from materials you already have, or learn something new?

Then board 1 — walk the GEMINI NOTEBOOK column FIRST, in the lesson's order, before the general tutor. Gemini Notebook, the source-grounded tutor: it learns from your materials and only knows what you give it, the ultimate exam-prep machine. Read its best use aloud: the materials the test covers — class notes, screenshots, study guides, even a webpage or YouTube video. Then its catch: it doesn't know what you didn't give it. Then the general tutor, ChatGPT, Claude and Gemini: trained on massive data, it can explain or quiz you on almost anything; best when you lack the materials or want a concept explained a new way; its catch, it can make things up or explain a concept differently than your teacher expects.

Then Start here, with the lesson's own line: use Gemini Notebook as your main study tool — the clue is in the name, it was built for learning.

Then board 2: feed it notes and PDFs, slides, images, websites and articles, YouTube videos — and get back a quiz, flashcards, a study guide, an audio overview, a mind map, a video overview. Name the outputs, not just the inputs.

Then board 3, and give it the most time of anything in this video. It carries all five best practices WITH the reason written under each one. Hold it and walk the five in order, and under every single one speak the reason printed on the board, in the board's own words: one notebook per subject and why mixing sources muddles the study guide; feed it a few angles and why your class notes keep your teacher's wording; quiz yourself blind, because re-reading is recognition and not recall, and read the quiz prompt out loud; review on the go, because it turns dead time into another pass over the material; trace it back, because reading the original is often what makes it land. Never read the five headings and move on — a heading without its reason teaches nothing, and that is exactly what the last roll did.

End on board 4: "Use AI to learn, not to skip the learning." over "Feed it your materials. Trace it back."
""",
    numbers="The only numbers allowed are the lesson's own: 1am and the 10-question quiz.",
    props="No readable or pseudo-readable text in drawn props; real words belong only on the attached boards and in clean dark-ink labels.",
    required='the narrator must teach the Gemini Notebook column before the general-tutor column, must say "the clue is in the name: it was built for learning", must speak Gemini Notebook\'s best-use list, must state both catches, and must speak the REASON under each of the five best practices, not just their headings.',
    extra=("Write in the lesson's plain voice for a 16-year-old; never substitute academic register such as \"pedagogy\", \"architecture\", \"ecosystem of materials\", \"ground truth\", or \"magnifier of cognitive effort\".",
           "Never invent a chart, a graph, a statistic or a measured claim. The last roll ended on a fabricated bar chart reading \"AI AMPLIFIES STUDENT EFFORT, student input 10, AI amplification 30, 3X AMPLIFIED\"; no such numbers exist anywhere in this lesson and nothing like them may appear.",))

add("how-ai-answers", title="How AI Answers", lo=4, hi="4.5", boards=True,
    body="""
Attached boards in order: 1 the phone tray, 2 the machine, 3-7 the five answer rows, 8 the ranked list, 9 the answer, 10 the close.

Focus: the answer gets built one token at a time, and the whole run has a name.

Open on board 1, the phone tray, and the everyday version of the idea. Then board 2, the machine: walk the prep stages IN ORDER and name what each one does — the context window, tokens and their IDs (which the last roll left on screen unmentioned), then STARTING MEANING, then the layers. Do not merge starting meaning into the layers; see rule 5.

Then the core why, which the last roll skipped and which is the most important sentence in this video: the model reads only the FINAL vector — and say why. The next word goes in exactly one place, right after the last token, and attention has spent every layer folding the earlier tokens into it. Do not state "the model only reads this final vector" and move on; give the reason.

Then rows 3 through 7, one board at a time, each row building the answer: the token gets typed, joins the context, and becomes the new final token. Say "That move is called prediction" as a named definition when you introduce the row-by-row move — the word must be used as the lesson's own term, not in passing.

Then board 8, the ranked list, with the lesson's real values: Spot 22%, Max 17%, Buddy 14%, Rex 9%, Biscuit 6%, other tokens 32%. Answer the lesson's own question about why "other tokens" is biggest — it's the rest of the vocabulary sharing that 32%, and no single one comes close to Spot — and note the numbers are illustrative. Then the second missing why: the neighborhood the vector lands in IS the top of that ranked list; those are the same thing seen two ways. Say it.

Then board 9, the answer: the model takes the top of the list and types it, Spot.

Then the naming beat: everything you just watched, from tokens to vectors to a ranked list to the next word, has a name — inference. It's what the model does every time it answers you.

End on board 10: "Every answer is built one token at a time." over "The whole run is called inference."
""",
    numbers="The only numbers allowed are the lesson's own token IDs and probabilities: 22, 17, 14, 9, 6, 32 percent. Invent no other figures and animate no counter through values the lesson does not contain.",
    props="No readable or pseudo-readable text in drawn props; real words belong only on the attached boards and in clean dark-ink labels.",
    required='the narrator must say "That move is called prediction" as a definition and must name "inference"; must give the reason the final vector is the one that matters (the next word goes in exactly one place, and attention has folded the earlier tokens into it); and must say that the neighborhood the vector lands in is the top of the ranked list.',
    extra=("STARTING MEANING IS ITS OWN BEAT, between tokens and the layers, and it is required. After the text is split into tokens and their order is fixed, each token's number is looked up in the embedding table and becomes a vector — that vector is its starting meaning, the same in every sentence, before any context is applied. Only THEN do the layers use attention to fold the surrounding tokens into it. Do NOT say or imply that the layers turn dictionary definitions into vectors: the vectors exist first, and the layers change them. The last roll skipped this step and inverted it, which is the single defect this re-roll exists to fix.",
           "End on the close board and speak both of its lines verbatim: \"Every answer is built one token at a time.\" then \"The whole run is called inference.\" Paraphrasing them does not count; the last roll gestured at both and said neither."))

add("fake-trap", title="Fake Trap", lo=3.5, hi=4, boards=True,
    body="""
Attached boards in order: 1 the two tests, 2 the four reasons, 3 the three checks, 4 the close.

Focus: seeing isn't proof anymore, and the test moved off the image onto the source.

Open on the strange thing: you already know AI can fake a voice, a face, a video — so why do smart people still get fooled? Because knowing fakes exist isn't a skill; it doesn't tell you what to do in the ten seconds after a clip hits your feed.

Then the scenario: a friend sends a video of your principal announcing a pipe burst and school closed all next week. Board 1, both columns. Pre-AI, does it look real: you study the face, the voice, the hallway. Verdict: real. The AI test, where is it from: you ignore the clip and check the trail, nothing on the school website — you went to the source that would know. Verdict: unverified.

Then the definition AND its second jaw, which the last roll missed entirely and which must be its own beat: the Fake Trap is believing it because it looks real — and its second jaw, dismissing the truth because it could be a fake. Say both halves.

Then why fakes get made, opening with the harmless case, REQUIRED: sometimes it's just fun — a friend fakes a picture of your hockey buddies hoisting the Stanley Cup, and everyone's in on the joke, no harm. But some fakes aren't friendly: a fake doesn't just happen, someone made it, and making it costs effort, so ask what they get back. Then board 2, the four reasons: money, outrage gets clicks and clicks pay; power, change what people believe and you change how they vote; fame, a viral clip means followers and needn't be true to travel; cruelty, some fakes exist to humiliate one person, the version most likely to show up at your school.

Then the detector dead end: a detector is one more AI making one more prediction, and fakes improve faster than it does — a clue, never a ruling.

Then board 3, the three checks. Source: did it come from somewhere with a reason to know — a friend forwarded it is the digital version of I heard from a guy. Context: look around the clip, not just at it — was your principal even at school on Tuesday. Corroboration: real news shows up in more than one place — everywhere on TikTok but nowhere on Google News is an answer. Keep that third line fully in frame as it is spoken.

Then the one rule under all three: verify somewhere the sender doesn't control — a voicemail asks for something urgent, call back on the number you already have. Until a second independent source shows the same thing, unverified is your answer.

Then if the fake is about you: don't handle it alone, don't delete the evidence, screenshot everything, and bring an adult in that day. You did nothing wrong by being targeted.

End on board 4: "Seeing or hearing isn’t proof anymore." over "Check the source, not the pixels."
""",
    numbers="Do not invent numbers, percentages or statistics, and draw charts only as wordless background.",
    props="Drawn phones, feeds and screens may appear but keep them blank or abstract — no readable or pseudo-readable text on any drawn screen or prop; real words belong only on the attached boards and in clean dark-ink labels.",
    required='both jaws — "believing it because it looks real" AND "dismissing the truth because it could be a fake"; the harmless-fun fake beat (the Stanley Cup joke) before the four reasons; "verify somewhere the sender doesn\'t control"; "You did nothing wrong by being targeted."',
    extra=("Restraint on the cruelty and if-it's-about-you beats: never show the humiliating fake itself, no crying or distressed victims, no alarm-red imagery — keep those scenes calm, like a teen and a trusted adult looking at a phone together.",
           "Never depict a real, recognizable person; every character is an invented hand-drawn person."))

add("welcome", title="Welcome", lo=3, hi="3.5", boards=True,
    body="""
Attached boards in order: 1 why go deeper, 2 your path, 3 your course toolkit, 4 the close.

Focus: a short orientation. Open on board 1 and let the narrator land all four of its lines — everyone has AI, most just press go, few understand it, be smarter than the tool — then: you're about to learn how the most powerful tool of your lifetime actually works. Not five quick tips. Not yesterday's hype. The real machinery.

Then the builders, in FIRST PERSON as Luke and Nate speaking, and say their names: "We're Luke and Nate, and yeah, we're still in high school." Do not skip the names; the last roll said only "we" and the pair were never introduced. This started at our kitchen table. AI is in every headline now and it's going to be in every career, including ours, so we'd rather understand it now than scramble to catch up later. We went looking for something good to learn from, but most of it was shallow, focused on tools, or already out of date. So we built our own. Never report on Luke and Nate in the third person.

Then the jersey aside, spoken, and keep it here at the end of the builders beat where the lesson puts it, not later in the middle of an argument: you'll even catch us in a few of the examples later, usually wearing the jerseys of the greatest hockey team in the world.

Then the bigger point, given real weight: AI is already everywhere in your life and it'll define the career you haven't started yet. And here's the part nobody tells you: the better AI gets, the more it pays to be the person who actually understands it. The gap between people who get how it works and people who just type into the box is only going to get wider, and which side you land on is up to you. That edge has a name, and it's the most important AI skill there is: Be Smarter Than the Tool. Do not skip the better-AI-gets clause; it is the lesson's sharpest claim. Say this over people and a plain widening gap if you draw anything at all — never as a chart.

Then board 2, the five-part path: Work, Understand, Avoid, Embrace, Build, each spoken with the gloss printed under it on the board, in the board's own words.

Then hold board 3 and walk its cards: laptop or desktop for hands-on activities; ChatGPT for Teens as the main lab tool, with free accounts placing ages 13 to 17 in the teen experience; and a free Google account for the Gemini Notebook study notebook. Say nothing to install, no paid plan required, and "Gemini Notebook", never "NotebookLM". Do not mention Claude.

End on board 4.
""",
    numbers="This lesson contains no data of any kind. Invent no numbers, no percentages and no statistics.",
    props="No readable text inside drawn props or backgrounds, and no invented app screens, menus or interfaces; real words belong only on the attached boards and in clean dark-ink labels.",
    required='first-person authorship WITH BOTH NAMES — "We\'re Luke and Nate, and yeah, we\'re still in high school"; the paradox "the better AI gets, the more it pays to be the person who actually understands it"; the jersey aside spoken aloud; and "Be Smarter Than the Tool."',
    extra=("Board 2's five cards must stay IN SYNC with the narration: the card being spoken is the card on screen, held still and fully readable, and the camera moves only when the narration moves to the next card. This overrides the slow-camera instruction for this board.",
           "Draw NO graphs, charts, axes, plotted curves or trend lines anywhere in this video. The lesson has no data to plot. The last roll invented a rising-curve 'job market' graph whose labels, Strategic Understanding and Value Gap, were thin pale purple and red on a pale cream ground and could not be read at all. Show the widening gap, if you show it, as two people and a widening space between them.",
           "Never add material the lesson does not contain — no apps-change-but-principles-stay digression, no passenger/driver metaphor, and no claim that progress depends on your curiosity.",))

add("where-ai-works-best", title="Where AI Works Best", lo=3.5, hi=4, boards=True,
    body="""
Attached boards in order: 1 patterned transformation, 2 generative variation, 3 semantic compression, 4 structured reasoning, 5 the close.

Focus: can try is not the same as built for.

Open on the range — AI will take on almost anything you ask: writing, planning, summarizing, coding, drawing, researching — then the distinction: can try is not built for, and AI is far better at some kinds of work than others.

Then the stress test from building this course: AI coded every page and every interaction, and earns an A+ for coding. It also wrote the first drafts of all the lessons and earned a C-. Name all three failures: it made points in the wrong order, added explanations that missed what we meant, and had no real feel for how a lesson should flow. Then the reason, in the lesson's own terms: writing software code is all about patterns and AI is a pattern-making machine, so it aces that job — but writing strong lessons doesn't follow a set pattern, so AI can help but can't do the whole thing.

Then the four shapes, one board each, and speak each board's headline plus its examples — the last roll left half the examples on screen and unspoken. Patterned transformation, "same meaning, new shape": coding help, reformatting messy data, translating between languages, turning an outline into prose. Generative variation, "ten versions in ten seconds": brainstorming angles, give me ten variations, rewriting in a different tone, first drafts of common documents. Semantic compression and retrieval — say the full name — "finds the signal in long documents": summarizing a chapter, extracting key points, finding the relevant section, answering questions from supplied material. Structured reasoning and synthesis, "reasons through what you give it": planning a project, debugging code, comparing options, critiquing a draft.

Then why it works: training gave AI exposure to more examples than any human could read in a lifetime — code, essays, explanations, emails, arguments, stories, documents, conversations — which is why it's fluent with common formats.

Then the limit, and state it exactly as the lesson does, with the hedge intact: AI is OFTEN good at the COMMON version of a task, not necessarily the true, current, personal, safest, or best version.

End on board 5: "'Can try' is not 'built for.'" over "That's why your judgment still matters."
""",
    numbers="The only grades anywhere are the lesson's own A+ and C-. Invent no percentages or statistics, and draw charts only as wordless background.",
    props="No readable or pseudo-readable text in drawn props — never draw code editors, terminals, notebooks or document pages with visible writing; real words belong only on the attached boards, the two report-card grades, and clean dark-ink labels.",
    required='all four strength names in full, including "semantic compression and retrieval"; each board\'s examples spoken, not just displayed; and the limit stated with its hedge — "often good at the common version, not necessarily the true, current, personal, safest, or best version."',
    extra=("Never claim AI is locked into averages or that it will never produce the exceptional version; the lesson deliberately hedges this and the harder claim must not be invented.",))

if __name__ == "__main__":
    os.makedirs("Prompts", exist_ok=True)
    bad = 0
    for slug, kw in LESSONS.items():
        txt = build(slug, **kw)
        n = len(txt)
        flag = "OVER HARD LIMIT" if n > LIMIT_HARD else ("over 4800" if n > LIMIT_WARN else "ok")
        if n > LIMIT_HARD:
            bad += 1
        else:
            open(f"Prompts/{slug}-video-prompt.txt", "w").write(txt)
        print(f"  {slug:24} {n:5d} chars  {flag}")
    print(f"\n{len(LESSONS)} prompts, {bad} rejected")
    sys.exit(1 if bad else 0)
