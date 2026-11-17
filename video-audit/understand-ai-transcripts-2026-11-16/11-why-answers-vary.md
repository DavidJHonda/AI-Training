# 11. Why Answers Vary

`course-assets/why-answers-vary/why-answers-vary.mp4` · 3:02 · 443 words

**[0:00]** You ask AI, what should I name my new dog? It suggests Spot. You start a new chat and ask the exact same question. This time, it suggests Max. Why did the same question get a different answer? Three main components dictate an AI's response. First, the model you use and its thinking time changes the answer. Second, what the AI receives, your prompt and provided context. But the third column is where the real mechanics live. AI uses techniques giving different tokens a chance, sampling and temperature. Take a look at this probabilities chart. The AI has generated the phrase, you could name him and is evaluating its options for the next open blank.

**[0:44]** At this exact blank, the AI calculates a probability for every token in its vocabulary. Right now, spot leads the starting odds at 22%. You might expect the AI to pick the winner automatically But a 22 % probability means AI would pick Spot about 22 times out of 100 dries, on average, if the odds stay the same. That's called sampling. If we run five separate random picks with these exact unchanged probabilities, we get a specific sequence. Pick one, Max. Pick two, Spot. Pick three, Buddy. Pick four, Rex. And pick five, Max. Spot was picked only once, even with the highest probability. Another five picks could turn out entirely differently.

**[1:32]** Why does AI work this way?

**[1:34]** Choosing the absolute most likely token every single time makes the AI's answers rigid, predictable, and highly repetitive. Giving other likely tokens a chance to be selected introduces essential variety. It makes the generated text feel more creative and natural to a human reader. Choosing a different token shapes what comes next. One slightly different token choice at a critical juncture can send the entire remainder of the generated answer in a completely new direction.

**[2:03]** Sampling selects a token using probabilities.

**[2:06]** Temperature adjusts those probabilities. In ChatGPT, Gemini, and Claude, temperature is set for you behind the scenes. This chart compares how different temperature settings change the odds for each dog name. Notice the center column. These are the starting odds derived directly from the model's training and the context you provided. A low temperature setting concentrates the odds onto the most likely choices.

**[2:31]** Spot leads at 22%, but at low temperature, its chance jumps to 36%. A high temperature setting does the opposite by spreading the odds out more widely. Here, Spot's chance falls to 16%. Both settings manipulate the exact same starting odds. Spot remains the most likely individual token at all three settings. Temperature changes its probability.

**[2:55]** AI answers vary. Different inputs. Different odds. Different choices.
