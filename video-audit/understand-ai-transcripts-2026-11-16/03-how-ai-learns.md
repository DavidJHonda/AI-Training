# 3. How AI Learns

`course-assets/how-ai-learns/how-ai-learns.mp4` · 3:23 · 521 words

**[0:00]** Modern AI can explain complex chemistry, write functional code, and help you improve an essay. How did it learn to do those things?

**[0:09]** Think about learning to shoot a basketball. You try a shot, see how you did, and make an adjustment to your mechanics.

**[0:15]** AI also learns through repeated attempts. Let's follow the process from preparation to a model that is ready to use.

**[0:23]** Two things happen before training starts. First, set up the system. Engineers design the model and give its internal numbers starting values. Training will adjust those numbers as the model learns. Second, gather the data. Teams collect books, websites, conversations, code, images, audio, and video. This becomes the curriculum.

**[0:45]** Training builds different abilities in three main phases. Phase one is pre-training, learn patterns. Phase two is instruction tuning, learn to follow instructions. Phase 3 is preference tuning. Improve responses through feedback.

**[0:59]** Across all three phases, training follows a basic loop. Guess, check, and adjust. What changes is the examples and feedback used to guide those adjustments. Here is a simple example. Given the phrase peanut butter and blank, the model makes a guess. In this instance, it guesses cloud.

**[1:19]** Next is the check. The actual training example says jelly, so the system compares its guess with that correct word. Finally, the adjust phase. The system tweaks its internal numbers to make jelly more likely in this specific situation. Then the loop runs again on the next example. Those adjustments change the model's internal numbers called weights. Now let's look at the first phase of training called pre-training. In pre-training, the model learns from more text than you could read in 1 ,000 lifetimes. Across vast amounts of text and code, it learns broad patterns in language and information. The model can produce fluent text, but it doesn't reliably follow your instructions yet. Training keeps adjusting the model's weights. What changes in the next phases is the kind of examples and feedback used to guide those adjustments.

**[2:09]** This brings us to phase two, instruction tuning. Now people provide questions paired with helpful example answers. The model practices answering those questions, adjusting its weights, so its answers become more like those human examples.

**[2:23]** The model can follow a request, but its answer may still be unclear, incomplete, or unhelpful. Following instructions is a start. Next, the model learns from feedback about which answers people find more helpful. That's preference tuning. In phase three, the model produces several answers to a question. People compare those answers and select the best one based on clear, useful, and accurate information. Training adjusts the model's weights to make answers like the selected one more likely. However, there is still work to do. Feedback helps improve the answers, but AI can still give a wrong answer that sounds right. When training ends, the model is ready to use. It relies entirely on the final internal weights produced by that long three-phase process. During a normal chat, it can work with new information you give it, but your conversation does not change those weights.

**[3:13]** AI learns from examples and feedback. Guess, check, adjust. repeat
