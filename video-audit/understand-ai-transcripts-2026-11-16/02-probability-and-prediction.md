# 2. Probability & Prediction

`course-assets/probability-and-prediction/probability-and-prediction.mp4` · 2:41 · 403 words

**[0:00]** When you type a prompt into ChatGPT and receive a coherent response, it can feel like the system is thinking. Tools like Claude appear to understand context and nuance, leading us to wonder what is actually happening behind the interface. These systems function by calculating probability, analyzing the statistical likelihood of what should happen next. This process of predicting outcomes based on specific data traces back to 1654, when mathematicians Blaise Pascal and Pierre de Fermat exchanged letters about the odds in gambling. Their work provided the foundation for how we calculate the chance of a future event, a framework that remains central to how modern AI builds an answer.

**[0:44]** To see how that works, we start with standard probability. This applies to scenarios where every possible outcome is equally likely. The math is a simple division. You count the ways to get the specific result you want and divide that by the total number of possible outcomes.

**[1:01]** Consider a basic scenario. You toss two coins. To find the chance both land on heads, we map out the possibilities. There are four equally likely results. Only one matches our goal. We divide that successful path by the four total outcomes, giving a probability of 25%. However, odds are rarely static. In mathematics, conditional probability describes how new evidence changes the calculation. Imagine we run the toss again, but this time someone peaks. They tell you the first coin landed on heads. Because the first coin is heads, we can immediately eliminate any outcome starting with tails. Those possibilities are ruled out. Our total pool of outcomes has shrunk from 4 to 2.

**[1:47]** Out of those two remaining paths, only 1 results in double heads. 1 divided by 2 means the probability jumps to 50%. The physical state of the coins didn't change, but your knowledge of them did. AI uses conditional probability to answer your questions. If you ask, what should I name my new dog, and the AI begins its response with, you could name him, those words become the context for the next calculation. It might find a 22 % chance for Spot, 17 % for Max, and 14 % for Buddy.

**[2:23]** Once a word is chosen, it is added to the text. This updated string of words becomes the new evidence for the next calculation, and the cycle repeats instantly.

**[2:33]** AI builds answers with probabilities, one prediction at a time.
