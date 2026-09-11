## START SMARTER

# How an LLM Works

If you’ve used AI, you’ve probably used an app like ChatGPT, Claude, or Gemini. The app is what you use. Under the hood, a **Large Language Model**, or **LLM** for short, does the work.

![What’s an LLM? Large means trained on huge amounts of text and code. Language means reading, writing, summarizing, translating, and explaining. Model means predicting likely output from learned patterns.](../illustrations/what-is-ai-llm.jpg)

So how does an LLM actually turn your words into an answer?

When ChatGPT or Claude write a sentence, they're running math to predict the likely next words. They aren't looking up what your words mean; they're working out which words tend to follow which.

How do they do it? In two phases. First the model learns, once, by soaking up patterns from mountains of text. Then, every time you chat, it uses those patterns to build your answer one word at a time.

![Learn Once. Answer Every Word. Training creates learned numerical patterns once. For every next word, the model scores probabilities, chooses one likely next word, and repeats the process. Both arrows stop at the next numbered step. Learn once. Use the patterns for every answer.](ai-is-different-learn-once.jpg)

Four ideas carry it. Below, we follow one example, peanut butter, through all four.

## 01 Training

The model **teaches itself**: guess the next word, check, and nudge its numbers toward the right word.

![How Training Works. Read: The model reads a training example with the answer included. Guess: Given “Peanut butter and ___,” the model guesses cloud. Check: The example says jelly, and the guess is compared with that word. Adjust: The model’s internal numbers change to make jelly more likely in this situation. The flow returns to Read for the next example.](how-an-llm-training-flow.jpg)

## 02 Patterns

So what is it actually learning? **Patterns**. Here's one you picked up as a child. Which word comes next?

![How AI Learns Patterns. One Familiar Pattern: Peanut butter and blank leads to jelly; you knew it, and so does AI. Patterns Are Everywhere: Twinkle, twinkle, little blank leads to star; Once upon a blank leads to time; Better late than blank leads to never. AI learns patterns by working through billions of examples.](how-ai-learns-patterns.jpg)

These are easy patterns you already know. AI also learns patterns in places you might not expect: how people explain ideas, ask questions, solve problems, and even misspell words.

## 03 Probability

AI doesn't make one guess. It scores **every** possible next word: a ranked list with a probability on each, and those numbers shift with the surrounding text.

<style>
  #same-word-different-odds {
    box-sizing: border-box;
    width: 100%;
    container-type: inline-size;
    
    padding: 2.5%;
    border-radius: 22px;
    background: #eae7fd;
    color: #0e0a1f;
    font-family: "Plus Jakarta Sans", sans-serif;
    overflow: hidden;
  }
  #same-word-different-odds * { box-sizing: border-box; }
  #same-word-different-odds h1 {
    margin: 0 0 2.6%;
    font-size: clamp(28px, 3.684cqw, 56px);
    line-height: 1.04;
    letter-spacing: -0.03em;
    font-weight: 700;
  }
  #same-word-different-odds .odds-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2.6%;
    min-height: 350px;
  }
  #same-word-different-odds .odds-panel {
    display: flex;
    flex-direction: column;
    min-width: 0;
    border-radius: 17px;
    background: #fff;
    overflow: hidden;
    box-shadow: 0 8px 18px rgba(28, 19, 82, .08);
  }
  #same-word-different-odds .phrase {
    min-height: 92px;
    margin: 3.7% 5.2% 0;
    padding: 3.5% 4%;
    display: flex;
    align-items: center;
    border-radius: 12px;
    font: 500 clamp(18px, 1.908cqw, 29px)/1.45 "Plus Jakarta Sans", sans-serif;
    color: #3a3550;
  }
  #same-word-different-odds .purple .phrase { background: #e5defe; border: 2px solid #c8baf6; }
  #same-word-different-odds .teal .phrase { background: #e1f5f1; border: 2px solid #b5ded8; }
  #same-word-different-odds .rows {
    flex: 1;
    display: grid;
    grid-template-rows: repeat(4, minmax(54px, 1fr));
    padding: 3.4% 5.2% 4.2%;
  }
  #same-word-different-odds .row {
    display: grid;
    grid-template-columns: minmax(82px, .85fr) 2.5fr 56px;
    align-items: center;
    gap: 3.2%;
    border-bottom: 1px solid #e5e2ed;
  }
  #same-word-different-odds .row:last-child { border-bottom: 0; }
  #same-word-different-odds .word {
    font-size: clamp(18px, 1.908cqw, 29px);
    font-weight: 700;
    color: #3a3550;
  }
  #same-word-different-odds .track {
    height: clamp(12px, 1.447cqw, 22px);
    border-radius: 999px;
    background: #efedf4;
    overflow: hidden;
  }
  #same-word-different-odds .fill { height: 100%; border-radius: inherit; }
  #same-word-different-odds .purple .fill { background: #4f2fc4; }
  #same-word-different-odds .teal .fill { background: #0e8f86; }
  #same-word-different-odds .teal .jelly .fill { background: #4f2fc4; }
  #same-word-different-odds .teal .jelly .word,
  #same-word-different-odds .teal .jelly .percent { color: #4f2fc4; }
  #same-word-different-odds .percent {
    text-align: right;
    font: 700 clamp(18px, 1.908cqw, 29px)/1.3 "Plus Jakarta Sans", sans-serif;
    color: #3a3550;
  }
  #same-word-different-odds .takeaway {
    min-height: 0;
    margin-top: 2.6%;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: clamp(12px, 1.579cqw, 24px);
    padding: clamp(10px, 1.447cqw, 22px) 16px;
    background: #ffe39a;
    font-size: clamp(18px, 2.105cqw, 32px);
    line-height: 1.4;
    font-weight: 500;
    text-align: center;
  }
  #same-word-different-odds .check {
    flex: 0 0 auto;
    width: clamp(22px, 2.895cqw, 44px);
    height: clamp(22px, 2.895cqw, 44px);
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: #fff;
    background: #4f2fc4;
    font-size: .72em;
    font-weight: 800;
  }
  #same-word-different-odds .check svg { width: 65%; height: 65%; display: block; }
  @media (max-width: 620px) {
    #same-word-different-odds { padding: 24px; }
    #same-word-different-odds h1 { margin-bottom: 20px; }
    #same-word-different-odds .odds-grid { grid-template-columns: 1fr; height: auto; gap: 18px; }
    #same-word-different-odds .odds-panel { min-height: 290px; }
    #same-word-different-odds .takeaway { min-height: 0; height: auto; padding: 12px 14px; margin-top: 20px; }
  }
</style>
<div id="same-word-different-odds" role="group" aria-label="Same Word. Different Odds. Two probability lists show how surrounding words change likely next-word predictions.">
  <h1>Same Word. Different Odds.</h1>
  <div class="odds-grid">
    <section class="odds-panel purple" aria-label="Probabilities after I'd like to buy peanut butter and blank">
      <div class="phrase">I’d like to buy peanut butter and _____.</div>
      <div class="rows">
        <div class="row jelly"><div class="word">jelly</div><div class="track"><div class="fill" style="width: 41%"></div></div><div class="percent">41%</div></div>
        <div class="row"><div class="word">bread</div><div class="track"><div class="fill" style="width: 27%"></div></div><div class="percent">27%</div></div>
        <div class="row"><div class="word">bananas</div><div class="track"><div class="fill" style="width: 16%"></div></div><div class="percent">16%</div></div>
        <div class="row"><div class="word">honey</div><div class="track"><div class="fill" style="width: 5%"></div></div><div class="percent">5%</div></div>
      </div>
    </section>
    <section class="odds-panel teal" aria-label="Probabilities after I'd like to buy a peanut butter and banana blank">
      <div class="phrase">I’d like to buy a peanut butter and banana _____.</div>
      <div class="rows">
        <div class="row"><div class="word">sandwich</div><div class="track"><div class="fill" style="width: 54%"></div></div><div class="percent">54%</div></div>
        <div class="row"><div class="word">smoothie</div><div class="track"><div class="fill" style="width: 16%"></div></div><div class="percent">16%</div></div>
        <div class="row"><div class="word">toast</div><div class="track"><div class="fill" style="width: 9%"></div></div><div class="percent">9%</div></div>
        <div class="row jelly"><div class="word">jelly</div><div class="track"><div class="fill" style="width: 2%"></div></div><div class="percent">2%</div></div>
      </div>
    </section>
  </div>
  <div class="takeaway"><span class="check" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M5 16L12 23L27 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span><span>The surrounding words change the odds.</span></div>
</div>

In this example, adding “banana” drops the probability of “jelly” from 41% to 2%.

## 04 Prediction

Probability handled one word. But your answer is hundreds of words long, so the model just repeats the move. Your phone does this when you write a text: it suggests a word, you tap it, it suggests the next.

<style>
#prediction-board { container-type:inline-size; background:#eae7fd; color:#0e0a1f; font-family:'Plus Jakarta Sans',sans-serif; padding:2.5%; border-radius:20px; }
#prediction-board * { box-sizing:border-box; }
#prediction-board h2 { font-size:clamp(28px,3.684cqw,56px); font-weight:700; letter-spacing:-.03em; line-height:1.2; margin:0 0 26px; }
#prediction-board .content { display:grid; grid-template-columns:minmax(0,1fr) 26px minmax(0,1fr) 26px minmax(0,1fr); gap:12px; align-items:stretch; }
#prediction-board .step { background:#fff; border-radius:14px; padding:26px 22px; display:flex; flex-direction:column; justify-content:space-between; gap:26px; }
#prediction-board .sentence { font-size:clamp(18px,1.908cqw,29px); font-weight:500; line-height:1.45; color:#3a3550; }
#prediction-board .result { display:flex; align-items:center; gap:12px; font-size:clamp(18px,1.908cqw,29px); }
#prediction-board .flow-arrow { align-self:center; width:26px; height:32px; color:#4f2fc4; }
#prediction-board .prior { color:#4f2fc4; font-weight:700; }
#prediction-board .new-word { display:inline-block; color:white; background:#4f2fc4; padding:3px 14px; border-radius:9px; font-weight:700; line-height:1.5; }
#prediction-board .predict-arrow { color:#4f2fc4; font-weight:700; }
#prediction-board .banner { margin-top:22px; padding:clamp(10px,1.447cqw,22px) 16px; border-radius:10px; background:#ffe39a; display:flex; align-items:center; justify-content:center; gap:clamp(12px,1.579cqw,24px); font-size:clamp(18px,2.105cqw,32px); line-height:1.4; font-weight:500; text-align:center; }
#prediction-board .check { width:clamp(22px,2.895cqw,44px); height:clamp(22px,2.895cqw,44px); flex-shrink:0; background:#4f2fc4; color:white; border-radius:50%; display:grid; place-items:center; }
#prediction-board .check svg { width:65%; height:65%; display:block; }
@media(max-width:550px) { #prediction-board .content {grid-template-columns:1fr;} #prediction-board .step {padding:24px;} #prediction-board .flow-arrow {justify-self:center;transform:rotate(90deg);} #prediction-board .banner {padding:12px 14px;gap:12px;} }
</style>
<section id="prediction-board" aria-label="Prediction: One Word at a Time">
  <h2>One Word at a Time</h2>
  <div class="content">
    <div class="step"><div class="sentence">I want to buy peanut butter and</div><div class="result"><span class="predict-arrow" aria-label="predicts">→</span><span class="new-word">jelly</span></div></div>
    <svg class="flow-arrow" viewBox="0 0 26 32" aria-label="Use the updated sentence"><path d="M2 16H23 M15 8L23 16L15 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div class="step"><div class="sentence">I want to buy peanut butter and <span class="prior">jelly</span></div><div class="result"><span class="predict-arrow" aria-label="predicts">→</span><span class="new-word">for</span></div></div>
    <svg class="flow-arrow" viewBox="0 0 26 32" aria-label="Use the updated sentence"><path d="M2 16H23 M15 8L23 16L15 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div class="step"><div class="sentence">I want to buy peanut butter and jelly <span class="prior">for</span></div><div class="result"><span class="predict-arrow" aria-label="predicts">→</span><span class="new-word">lunch</span></div></div>
  </div>
  <div class="banner"><span class="check" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M5 16L12 23L27 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span><span>Add a word. Use the updated sentence. Predict again.</span></div>
</section>

A full paragraph runs this loop many times, fast enough to look like thought.

Training builds the patterns.

The model uses those patterns to build your answer, one word at a time.
