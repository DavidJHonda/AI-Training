## BUILD YOUR SKILLS

# Tune the Model

You’ve already learned to choose your app. Now comes something normal apps never ask of you. Spotify doesn’t ask which Spotify you want. AI apps do: inside each one is a family of models, and a picker to choose between them.

Think of a hockey team changing its lines. The first line has the most skill, but you can’t play them every shift; their minutes are limited. The third line is fast and steady, and it takes the everyday shifts. The coach’s job is matching the line to the moment. Inside an AI app, you’re the coach.

And the lines are real. The models in a family aren’t the same brain dialed up or down. They’re actually different LLMs. The big one has more layers, more dimensions, and was trained on more data. The smaller ones are built lighter from the start.

Why build a family at all? Because every answer you get runs on a server doing heavy math, and that math costs real money, time, and energy. So every model is a trade between three things: how smart it is, how fast it answers, and what it costs to run. No model maxes all three. The family exists so you can pick where to sit on that scale.

## The Model Family

Every model in a family sits somewhere on one scale. Nothing maxes both ends: picking a model is picking where to sit.

## ◂ Smartest · Slowest · Costliest

## Fastest · Cheapest · Lighter Thinking ▸

1

2

3

Most capable

The Senior Architect

Deep, multi-step reasoning: a 200-page document, complex code, advanced math, writing that needs real nuance. The slowest and costliest, built for the hardest problems.

**Spot it:**Labeled smartest or most capable.

Everyday

The Reliable Project Manager

Smart, quick, and balanced. Your default for most work: schoolwork, drafting, summarizing, explaining, planning.

**Spot it:**Usually the default.

Fast & light

The Speed Typist

Built for speed and volume where the thinking is simple: reformatting notes, generating a list, quick variations. Not the place for complex judgment.

**Spot it:**Labeled fastest or lightest.

Notice we didn’t print any model names. That’s on purpose: the companies rename and replace models a few times a year as they compete, and a name alone won’t tell you its size anyway. What you need is a way to figure it out in any app, in any year. Three moves:

1

Find the picker

Look for the model name at the top of the chat or next to the message box. It’s usually a dropdown. Tap it and the whole family appears. If you can’t find one, the app is choosing for you.

2

Read the descriptions, not the names

Every picker labels its models with a short line like ‘most capable’ or ‘fastest.’ That label tells you the tier, whatever the name is this month.

3

When in doubt, search

A ten-second search like ‘which ChatGPT model should I use for an essay’ gets you a current answer. The lineup changes; the search works every time.

Your turn. Below is the model picker from an app that doesn’t exist, with four made-up models. The names are useless on purpose. The labels are everything.

🔑 **The default is a choice someone else made.**Most people never open the picker and never know what they’re missing. You know the tiers now. Match the line to the moment, and send out the first line when the problem deserves it.

One more thing if you’re on a free plan. The top tier has the tightest limits, and when you hit one, the app may quietly switch you to a smaller model or make you wait. If answers suddenly feel dumber mid-chat, that’s usually what happened: check the picker. And limits usually burn by how much text is in the conversation, not how many messages, so long pastes cost more. Start fresh chats when you can.

You’ve chosen your app, and you just chose your model. Now there’s one more choice: how much effort should the model spend on this answer?

Every major AI lets you set how much effort it spends before answering. Turn it down and the model answers fast from what it already knows. Turn it up and it reasons through the problem step by step before committing. Some apps show this as a simple on/off switch, others as a dial with several levels.

Effort changes how hard the model thinks before it commits, not how the answer sounds. The wording has its own dial, and it’s coming up next.

And it’s not the same as the model choice you just made, even though both say ‘turn it up for hard problems.’ A bigger model is more brain. More effort is more thinking time from the brain you already picked. Rule of thumb: pick the model that fits the job first. If the answer still feels shallow, turn up the effort before you switch models.

⚡

#### Quick answer

**How it works:**Pattern matches from training, answers immediately.

Best for:

You need a quick answer

You’re brainstorming lots of options

The task is simple formatting, rewriting, or summarizing

You’re asking for a first draft, not final judgment

Speed matters more than depth

🧠

#### Deeper reasoning

**How it works:**Reasons step by step before responding, checks its own work.

Best for:

The problem has multiple steps

The answer needs logic, math, code, or careful comparison

You’re analyzing an argument, plan, essay, or decision

The first answer felt shallow and the issue is reasoning

Accuracy matters more than speed

The decision has real consequences

🔑 **More effort isn’t a tiny person inside the computer reconsidering.**It’s an extra round of reasoning and self-checking the model runs before answering, which catches more on hard problems. Worth turning up when the work is complex. But it’s not a truth machine. If the model is missing information, using old information, or relying on a bad source, thinking longer won’t fix that. For truth, you still need to evaluate the results.

## WHERE TO FIND THE DIAL

Look near the model picker. Some apps give effort its own switch, with a label like ‘extended thinking’ or ‘reasoning.’ Others fold it into the picker itself: choosing a model labeled ‘thinking’ is choosing more effort. Read the labels the same way you read the picker, and when you can’t tell, a ten-second search settles it.

💡 Same dial, different labels in every app. Once you understand what it does, you can find it anywhere.

Some tasks need speed. Others need depth. And the dial turns both ways: deeper is slower, and on a simple ask it buys you nothing. For each task below, decide how much effort fits.

App. Model. Effort.

Three separate decisions before you ever type a word, and now you own all three.

1

App

Where you work. Your home base, plus another app when the job clearly fits its strength.

2

Model

How much brain the job needs: most capable, everyday, or fast and light.

3

Effort

How long it thinks before it commits: quick for speed, deeper for hard problems.

**A bad answer doesn’t always mean ‘try harder.’**Sometimes you picked the wrong app. Sometimes the model is too small. Sometimes it just needs more effort. Knowing the three decisions means you can fix the right one.

## One more dial: temperature

Back in One More Thing, you learned how the model really picks its next token: a weighted drawing, where every token holds tickets equal to its probability. **Temperature** is the dial on that drawing. Low temperature hands the top pick nearly every ticket, so answers become repeatable. High temperature spreads tickets far down the list, so answers get more varied, creative, and sometimes weird. The middle is the balanced default, best for everyday writing.

Here’s the dog-name drawing from that lesson at three settings. The middle column is the balanced default; watch the odds sharpen and flatten as the dial moves. And keep an eye on Beowulf: impossible at low, alive at high. Temperature isn’t the only sampling control, but it’s the one worth knowing.

How temperature reshapes the picks

You could name him

❄️ Low

⚖️ Medium

🔥 High

Spot

58%

22%

13%

Max

19%

17%

12%

Buddy

10%

14%

11%

Rex

5%

9%

9%

Biscuit

2%

6%

8%

Beowulf

0%

3%

6%

other tokens

6%

29%

41%

You won’t see this dial in ChatGPT, Claude, or Gemini. The apps set the temperature for you; the dial itself lives in the tools developers use to build on these models. But the idea still matters, because you can ask for the effect instead: request “your best single answer” for consistency, or “ten different options” for range.
