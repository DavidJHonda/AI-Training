# Understand AI: video transcripts

Machine transcripts of the 11 live section videos, made with faster-whisper medium.en, silence filter off. Timestamps mark where each paragraph starts. Spellings of names and numbers are the model's best guess.

## 1. Opener

`course-assets/understand-ai-opener/understand-ai-opener.mp4` · 1:11 · 214 words

**[0:00]** Sometimes, working with AI feels like having a PhD-level expert right at your side. Other times, it makes a mistake you'd expect from a six-year-old. How can the same tool do both?

**[0:12]** AI isn't magic, a person, or even ordinary software. To explain why it has these blind spots, we need to look at what happens inside. Think about driving a car. You can get pretty good at it without ever opening the hood. But knowing what happens underneath the metal helps you understand exactly what the car can do and why something might go wrong. The same goes for AI. Time to look under the hood.

**[0:37]** Knowing how it works helps you be smarter than the tool. We are going to take you inside the machine one piece at a time. Some of this will be new to you, but each piece builds on the one before it. You don't need to memorize every term. The goal is to understand how your words become an answer. This section will help you answer three specific questions. Where does AI get all that knowledge? How does AI seem to understand what I ask? How does AI come up with its answers? The machine won't feel like magic anymore. Take it a piece at a time.

## 2. Probability & Prediction

`course-assets/probability-and-prediction/probability-and-prediction.mp4` · 2:41 · 403 words

**[0:00]** When you type a prompt into ChatGPT and receive a coherent response, it can feel like the system is thinking. Tools like Claude appear to understand context and nuance, leading us to wonder what is actually happening behind the interface. These systems function by calculating probability, analyzing the statistical likelihood of what should happen next. This process of predicting outcomes based on specific data traces back to 1654, when mathematicians Blaise Pascal and Pierre de Fermat exchanged letters about the odds in gambling. Their work provided the foundation for how we calculate the chance of a future event, a framework that remains central to how modern AI builds an answer.

**[0:44]** To see how that works, we start with standard probability. This applies to scenarios where every possible outcome is equally likely. The math is a simple division. You count the ways to get the specific result you want and divide that by the total number of possible outcomes.

**[1:01]** Consider a basic scenario. You toss two coins. To find the chance both land on heads, we map out the possibilities. There are four equally likely results. Only one matches our goal. We divide that successful path by the four total outcomes, giving a probability of 25%. However, odds are rarely static. In mathematics, conditional probability describes how new evidence changes the calculation. Imagine we run the toss again, but this time someone peaks. They tell you the first coin landed on heads. Because the first coin is heads, we can immediately eliminate any outcome starting with tails. Those possibilities are ruled out. Our total pool of outcomes has shrunk from 4 to 2.

**[1:47]** Out of those two remaining paths, only 1 results in double heads. 1 divided by 2 means the probability jumps to 50%. The physical state of the coins didn't change, but your knowledge of them did. AI uses conditional probability to answer your questions. If you ask, what should I name my new dog, and the AI begins its response with, you could name him, those words become the context for the next calculation. It might find a 22 % chance for Spot, 17 % for Max, and 14 % for Buddy.

**[2:23]** Once a word is chosen, it is added to the text. This updated string of words becomes the new evidence for the next calculation, and the cycle repeats instantly.

**[2:33]** AI builds answers with probabilities, one prediction at a time.

## 3. How AI Learns

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

## 4. Tokens

`course-assets/tokens/tokens.mp4` · 3:22 · 547 words

**[0:00]** Computers only process numbers. That seems counterintuitive because when you write an email, send a text or type on your phone, you see words. But behind the scenes, those words are converted to numbers so the computer can work with them. The exact same rule applies to AI. How did your words become numbers that AI could work with, and how did AI's response turn back into words you could read?

**[0:23]** One idea is to assign each word in every language a unique number. That way, whatever word you type, the AI gets a corresponding number. But that whole word approach breaks down fast. People constantly invent new words, names, and slang. They also make typos and include things like emojis and computer code. Even a list of a million words couldn't cover everything a person might type. Instead, AI uses reusable chunks of text called tokens. Think of them as building blocks for language. Here is what tokens look like. Unbelievable becomes un, belie, and vol. It is one word built from three distinct chunks.

**[1:02]** Unusual becomes un and usual. That is two tokens.

**[1:07]** Unmatchable becomes un, match, and able. That is three tokens. Notice how all three of these un words reuse the exact same chunk, un.

**[1:18]** Tokens handle compound words effortlessly. Basketball becomes basket and ball, that is two tokens.

**[1:25]** I heart AI becomes I, then a space with the heart, then a space with AI. That is three tokens. On the board, you can see SP marks a leading space. Even complex inputs break down into chunks. The web address shown on the board breaks into eight disparate tokens. A token can be a whole word or just part of one. The full collection of tokens is called the model's vocabulary. This proves how a finite set of chunks can build infinite variations of human text. When setting up AI, engineers run a program that analyzes a massive collection of text to build this vocabulary database. Each token in that newly built vocabulary is then assigned a specific number, known as its token ID. Think of it like a street address. It perfectly identifies where and what the token is, but it tells the computer absolutely nothing about what the word actually means.

**[2:15]** Look at this diagram contrasting how you and an AI process the same text. When you read the word cat, you instantly know what it means. Fur, whiskers, be animal. For AI, it starts with a token ID. Here, the tokenizer converts the written word cat to ID 4719. The number identifies the token, not its meaning. Here is a diagram showing the full process of what happens when you hit send. Step one, start with text. You type a question or message. Step two, split into tokens. A program called a tokenizer breaks the raw text down into reusable chunks.

**[2:51]** Step three, look up token IDs. The tokenizer finds each chunk's assigned number within its vocabulary.

**[2:58]** Tokenization turns text into token IDs the model can use.

**[3:02]** When the AI replies, its initial answer is generated as token IDs. The tokenizer then converts those IDs back into pieces of text and joins them together into the final answer. Words become numbers. That lets AI work with your language using math.

## 5. Embeddings: Meaning as Numbers

`course-assets/embeddings/embeddings.mp4` · 3:10 · 502 words

**[0:00]** By now, you likely know that AI converts text into tokens, and assigns each one a unique numerical identifier called a token ID. But there is a catch. That number tells us absolutely nothing about what the word actually means.

**[0:16]** Think of a high school cafeteria. An ID identifies you. It doesn't describe you. If four students are wearing badges, those numbers tell us who is who. But they tell us nothing about who is funny, who plays hockey, or who just stole french fries off their friend's tray. So how can numbers actually represent meaning? Let's use a taste test analogy.

**[0:37]** Imagine rating drinks on a scale from zero to 10, where a higher number means a drink has more of a certain trait. This table shows how we will structure the test. We have rows for the drinks, and we will judge them across six distinct characteristics, sweet, bitter, fizz, heat, caffeine, and dark. You and your friends tasted coffee and rated it on six characteristics. Let's put those ratings in the table. Next, you taste Coke and rate it on the same six characteristics. Which drink scores nine for sweet, one for bitter and 10 for fizz? That is Coke. A row of numbers like this is called a vector. Each position is a dimension and the number there is its value. Now let's add a third drink, Pepsi. Look closely at the resulting data.

**[1:24]** Pepsi's six values match Coke's exactly. If we hid the drink names, these numbers alone could not tell the two colas apart. To solve this problem, let us introduce a new column. Citrus gives us a seventh dimension. When we rate the drinks for citrus flavor, coffee gets a 0, Coke gets a 1, and Pepsi gets a 10. The first six values still match, but their new seven-number profiles are distinctly different. Another dimension can capture a difference the earlier numbers missed. AI uses this exact same numerical approach to represent the meaning of words. That row is called an embedding. This comparison table maps our taste test directly to an AI model. In your test, every drink gets a row. In AI, every single token in the model's vocabulary gets its own row.

**[2:14]** For dimensions, your test used six, then seven. AI typically uses thousands of dimensions. While you chose values on a 0-10 scale, AI learns its values during training, utilizing positive numbers, negative numbers, and decimals. Your taste test captured named traits, like sweet and fizz. AI captures complex, abstract patterns in how a token is actually used. And while you provided human labels for the columns, an AI model has none. The values simply work together to represent meaning. Both use a row of numbers to describe something. Even word fragments get their own embeddings. A long word, like unbelievable, splits into three separate token rows, each containing its own sequence of learned numbers.

**[3:00]** AI uses numbers to work with meaning. Those numbers help AI recognize similarities and differences.

## 6. Transformer

`course-assets/transformer/transformer.mp4` · 4:26 · 657 words

**[0:00]** When you type a message to ChatGBT, you use words, and it responds with words. Underneath, AI splits your text into small pieces, called tokens. Each token has an embedding, a row of numbers that represents its starting meaning. AI works mathematically, but to make the connections easier to see, we will use whole words.

**[0:20]** Two problems.

**[0:22]** Let's look at the left side, problem one. The same word can mean something completely different, depending on the sentence. If you say, please turn on the light, light means brightness. But if you say, the empty suitcase felt light, it means not heavy. So when you type light, how does the AI know which version you mean?

**[0:43]** Now look at the right side. Problem 2, pronouns.

**[0:47]** The cat was thirsty, so it drank the milk. Here, it means the cat. But in the sentence, the milk was fresh, so the cat drank it, it means the milk. When you use a pronoun like it, how does the AI know what you're actually referring to? The answer is right there in the rest of the sentence. The surrounding words help AI figure out the meaning. Our human brains use those surrounding words to lock on to the right meaning almost instantly. But for earlier AI, keeping that context connected was a serious challenge, because it read text strictly in order, one word at a time. Let's follow this sentence. the tired cat sat on the mat during the May rainstorm. It soon fell asleep.

**[1:30]** Notice the growing distance between cat and it. Earlier AI often struggled to keep that connection, especially in longer passages. That limitation set the stage for a new architecture.

**[1:42]** In 2017, eight researchers at Google published a paper called, Attention is All You Need. It introduced the transformer, which is the T in chat GPT. This diagram shows a completely different mechanical approach. The transformer can process the tokens in your message at once. By taking in the complete message together, the word IT can immediately draw on information from CAT, bypassing the gap of the words in between. There's more to reading than taking in the words. AI actually needs to figure out which words matter most and use that information to update the underlying numbers.

**[2:17]** This board shows two mechanisms updating a token's meaning. First, attention weighs information from relevant words and blends it into the token's numbers. Notice the connection flowing from it to cat.

**[2:31]** Second, transformation uses learned patterns to further process those numbers. The surrounding words help update each token's numbers. Applying this to our examples shows how the transformer resolves meaning.

**[2:45]** Please turn on the light, means brightness. The empty suitcase felt light means not heavy. On the left turn on acts on the token light pulling its mathematical meaning toward brightness. Below empty establishes light as not heavy. It works similarly for pronouns.

**[3:05]** The cat was thirsty so it drank the milk. It means cat. The milk was fresh so the cat drank it. It means milk. First it points to the thirsty cat. Next to the The combination of attention and transformation is exactly how AI deduces which meaning fits.

**[3:25]** Because the Transformer continually weighs relationships across the entire text simultaneously, this same mathematical blending scales up to capture broader structural patterns, allowing AI to interpret human nuances like sarcasm and idioms. The words alone aren't enough. Their order matters too. This board contrasts two phrases, dog bites man and man bites dog. Without positional information, these identical tokens and starting embeddings are completely ambiguous. They float without sequence, capable of describing two entirely different events. The solution is positional encoding. It acts as a numerical stamp, one, two, three, that helps the model keep track of every token's precise place in the sequence.

**[4:14]** Positional encoding tells the transformer where every token belongs. Attention is all you need. AI uses relationships between words to help interpret your message.

## 7. Layers

`course-assets/layers/layers.mp4` · 2:56 · 467 words

**[0:00]** Have you ever read a passage in English class that only made sense after a few reads? Try this sentence.

**[0:07]** The horse raced past the barn fell. On the first read, it doesn't make sense. It feels like someone forgot a word. You reach fell and the sentence just seems to stop short. So you read it again. Wait, did a barn fall? Or did the horse raced past the barn afterward? You test each possibility against the words to see if fell goes with the barn or with the horse. Finally, the meaning clicks. Someone raced a horse past a barn, then the horse fell. Raced describes a horse, and fell is what the horse did. Working the sentence out depends entirely on these repeated passes. Each read updates the meaning until it clicks.

**[0:45]** AI does something similar. It builds meaning through repeated updates. AI doesn't read your message the way you do. It processes your text through a series of layers. The whole stack of layers is called a neural network. numbers go in on one side, and final numbers come out the other. In between stands a long line of layers, one after another, each containing attention and transformation. The numbers that come out are not the numbers that went in. Attention and transformation update the numbers at each layer. Now, let's follow a single word, it, to see how its numbers change in a real sentence. The tired cat sat on the mat during the May rainstorm. It soon fell asleep. At the start, the word it could refer to different things.

**[1:31]** The starting numbers .12 and negative .34 don't tell us which one. By layer 1, the numbers update, beginning to capture a connection between it and cat. Moving into layer 2, the numbers update again. Now they carry even more specific information about that connection. This process repeats. It doesn't stop at layer 2. the numbers continue passing through more layers, each building directly on the previous layer's numbers. By the result stage, the two numbers finish at 0 .41 and 0 .06. Its updated numbers carry information about its connection to CAT. While AI companies don't always share exactly how many layers their models use, published designs show architectures built with dozens and sometimes more than a hundred layers.

**[2:19]** The horse sentence took a few reeds to untangle. Sarcasm, story twists, and complicated reasoning can take even more work. AI's layers give it more steps to work through those relationships and build meaning. If more layers give the system better reasoning, why not just keep adding them infinitely? Because adding layers demands massive amounts of computing power and time, the extra benefit has to be worth the cost. Meaning builds up, layer by layer, attention and transformation, dozens of times.

## 8. AI Brain Break (activity video inside Layers)

`course-assets/ai-brain-break/ai-brain-break.mp4` · 4:20 · 641 words

**[0:02]** Think of an AI token not as a piece of digital code, but as a physical arcade coin. To get an AI to answer you, a tiny robotic mechanism has to physically drop one of these coins into a massive industrial slot. When you ask a brief question, the labor requirement is minimal. It takes exactly one coin to produce an answer. This chart shows the difference in physical load based on your prompt. A short question load requires just one coin. But a long question load forces that poor robot to drag an entire overflowing bucket of change across the facility room. So when an AI takes a few seconds to generate a response, you are not waiting on complex software computations. The only thing causing that delay is a small robot hauling loose change as fast as its little legs can carry it.

**[0:53]** Training an AI is a highly physical process. instead of processing algorithms, the system actually runs laps around the data center cabinets. Track laps run against intelligence and you get a steep upward curve. The more laps, the smarter it gets. But skip conditioning and output drops to zero. That sleeping icon is the model getting tired halfway through homework and lying down. We tend to think of artificial intelligence as a triumph of mathematics. In reality, it is mostly a matter of cardiovascular endurance.

**[1:30]** Server farms and data centers are kept at absolutely freezing temperatures, which presents a significant survival challenge for artificial intelligence. To adapt to this cold, the model adds layers of clothing. A larger, more advanced AI model literally requires a much bigger winter jacket to stay warm. When a system reaches a hundred layers, its closet becomes incredibly crowded. Engineers have to figure out how to store massive quantities of scarves, mittens, and one truly enormous parka just to keep the system running. Advancing the capabilities of modern AI is not a matter of writing better code. It is primarily a logistical struggle to find more shelf space for all that winter gear.

**[2:15]** This graphic shows how AI generates answers that feel so deeply personal. it relies on direct mind-reading telemetry. Those invisible concentric waves are your thoughts being transmitted straight into your cell phone's antenna. Sometimes an AI will hallucinate or give you completely incorrect information. This happens because the phone's microphone simply failed to hear your internal monologue. The solution to a bad AI response is purely physical. You just need to forcefully project your thoughts louder.

**[2:47]** Google's flagship model was originally named Lemon Pie, directly inspired by the engineer's favorite midnight snack during long development hours. However, users constantly kept asking if the system came with ice cream. To stop the questions, they executed a last-minute name change. They chose Gemini because it rhymes with Lemon Pie, hoping nobody would notice the switch.

**[3:09]** Over at OpenAI, early models struggled with severe hearing loss. Users literally had to shout at the screen, which is why this corporate timeline shows the original product was named Yell GPT. Once the engineering team finally fixed the system's hearing, users could stop screaming at their keyboards. The megaphones were retired, and everyone was finally able to just chat. We map the progress of machine learning through algorithmic breakthroughs, but its actual history is dictated by midnight snacks and otolaryngology.

**[3:43]** Both Gemini and ChatGPT operate on what is known as the transformer architecture. This technical schematic compares that standard silicon transformer grid with a completely different approach used by Clod. It runs on a specialized pasta-based architecture known as Clodaroni. When a Clod model encounters a highly complex user prompt, engineers deploy a very specific troubleshooting protocol. They simply add more sauce. Forget about adding more compute power or tweaking parameters. The ultimate solution to complex digital problems is a generous layer of marinara.

## 9. Vector Space

`course-assets/vector-space/vector-space.mp4` · 3:21 · 534 words

**[0:00]** Each AI token starts with a row of numbers called an embedding. As the AI processes your message, its layers change those numbers to reflect the surrounding context. But those new numbers might not match the starting numbers for any token. How can they still represent meaning?

**[0:17]** An exact match isn't necessary. The relationships between the numbers matter too. We can picture those relationships as positions on a map, where nearby positions can represent similar meanings. That's the idea behind vector space.

**[0:31]** This map uses latitude and longitude to describe position. Let's add Dallas with its coordinates 32 .78 degrees north, 96 .80 degrees west.

**[0:41]** Next, add Mountain View, then New York City.

**[0:45]** Now you get coordinates that don't match one of our existing cities. The first is 38 degrees north, 120 degrees west. Mountain View is closest, even without an exact match. Next, try 40 degrees north, 76 degrees west. New York City is closest to the second point. The coordinates didn't match either city exactly, but distance helped us find the closest match.

**[1:08]** A map uses two numbers to describe a position, but we can do the same with more than two numbers. Imagine a taste test where you rate drinks on seven characteristics. We can't draw all seven dimensions, but a simplified picture shows which drinks are closest. Let's add Coke to the map. Next is Pepsi. Pepsi scores are close to Coke's so it sits near Coke in the soft drinks neighborhood. Now add a hot coffee. Hot coffee scores differ more from Coke's and Pepsi's so it sits farther away in the coffee and tea neighborhood. Now you get numbers that don't match any of our existing drinks. Let's add Mystery Drink A. Mystery Drink A is near Coke and Pepsi. Its first six numbers match both. Compare the last number, citrus. Mystery Drink A is 9, Coke is 1, and Pepsi is 10.

**[1:57]** Pepsi is closest. The citrus gap is only 1 compared with 8 for Coke. Now add Mystery Drink B. Mystery Drink B is in the coffee and tea neighborhood. Compare its seven numbers with Hot Coffee's vector. Hot Coffee is closest to Mystery Drink B. Its ratings are similar across all seven dimensions.

**[2:15]** Each drink's seven numbers give it a position in vector space. Comparing those numbers helps us find the closest This is the idea behind distance. Smaller gaps mean closer positions. AI uses this idea on a much larger scale. Its embeddings have thousands of dimensions, with values learned during training. After the layers update a token's vector, it doesn't need to match another vector exactly. Its position in vector space helps represent its meaning. Let's look at this meaning map to see how context changes position. Consider the sentence, The tired cat sat on the mat during the May rainstorm. It soon fell asleep.

**[2:53]** On its own, it could refer to many things. As the layers process the sentence, they update its numbers to carry information connecting it to cat. It remains a separate token, now near cat. Its new position reflects its connection to cat in this sentence.

**[3:12]** Meaning is a position in vector space. similar meanings usually sit close together.

## 10. How AI Answers

`course-assets/how-ai-answers/how-ai-answers.mp4` · 3:35 · 600 words

**[0:00]** When you ask a question, the system first processes your words together. Then it faces a new problem. How does it actually begin an answer? We'll show words as single tokens to make this example much easier to follow.

**[0:12]** Imagine you ask, what should I name my new dog? Before the answer begins, the question goes through four steps you've already seen.

**[0:20]** Tokens breaks the question into pieces. Positions marks where each piece belongs. Starting vectors turns each token into numbers that carry its starting meaning. And finally, through layers, where attention and transformation work together to update those numbers.

**[0:36]** As the tokens pass through the layers, each token's vector is updated using information from the tokens before it. In this simplified example, let's follow the last token in the question, what should I name my new dog? It begins with a starting vector representing a question mark. As it passes through the layers, those numbers change to reflect your question about naming a dog. After running through all the layers, the question marks vector reflects the context of your specific question.

**[1:02]** Looking at naming a dog versus choosing dinner, we see the identical final token gets different updated vectors because the different contexts change the question marks numbers. For naming your new dog, the question marks updated vector reflects the context of your whole question. For choosing your dinner, the exact same question mark now has a completely different updated vector, reflecting this different question. Why is this important?

**[1:26]** AI uses the final token's updated vector to predict the first token of its answer. Think about peanut butter ant and salt ant. Now, both end with and.

**[1:36]** But its updated vector reflects different words before it. So using patterns learned during training, an AI would likely give jelly a high probability after peanut butter and, and pepper a high probability after saltant. The prediction depends on the context reflected in those numbers. It adds the chosen token to the context and then predicts the next one. That's exactly how our response is built, using your question and the answer so far. For the dog naming question, the answer has no tokens yet. AI predicts possible starts to its reply, which include you at 18%, A at 14%, and great at 9%, with other tokens together accounting for 59%. AI selected you. You is now the last token.

**[2:21]** The last token's updated vector reflects both your question and everything the AI has written so far. Now, the context includes part of the answer, too. Its updated vector reflects the question plus the one-word answer, you. The system uses those numbers to predict exactly what comes next. To continue the growing reply, AI adds the word could to the sequence. Next, AI adds the word name.

**[2:47]** Then, AI adds the word him. Each added token becomes part of the context. Him is now the last token, and its updated vector reflects the question plus all four answer words to predict a dog name. A dog name is now a highly likely choice. Possibilities include Spot at 22%, Max at 17%, and Buddy at 14%, with other tokens accounting for 47%. AI selected Spot to build this answer, but it is important to note that another run could select a different name entirely. The answer now reads, you could name him Spot.

**[3:19]** Finishing the reply, AI adds a period, then an end of answer token.

**[3:24]** A special end of answer token signals that the reply is complete.

**[3:29]** Every answer is built one token at a time. The whole run is called inference.

## 11. Why Answers Vary

`course-assets/why-answers-vary/why-answers-vary.mp4` · 3:02 · 443 words

**[0:00]** You ask AI, what should I name my new dog? It suggests Spot. You start a new chat and ask the exact same question. This time, it suggests Max. Why did the same question get a different answer? Three main components dictate an AI's response. First, the model you use and its thinking time changes the answer. Second, what the AI receives, your prompt and provided context. But the third column is where the real mechanics live. AI uses techniques giving different tokens a chance, sampling and temperature. Take a look at this probabilities chart. The AI has generated the phrase, you could name him and is evaluating its options for the next open blank.

**[0:44]** At this exact blank, the AI calculates a probability for every token in its vocabulary. Right now, spot leads the starting odds at 22%. You might expect the AI to pick the winner automatically But a 22 % probability means AI would pick Spot about 22 times out of 100 dries, on average, if the odds stay the same. That's called sampling. If we run five separate random picks with these exact unchanged probabilities, we get a specific sequence. Pick one, Max. Pick two, Spot. Pick three, Buddy. Pick four, Rex. And pick five, Max. Spot was picked only once, even with the highest probability. Another five picks could turn out entirely differently.

**[1:32]** Why does AI work this way?

**[1:34]** Choosing the absolute most likely token every single time makes the AI's answers rigid, predictable, and highly repetitive. Giving other likely tokens a chance to be selected introduces essential variety. It makes the generated text feel more creative and natural to a human reader. Choosing a different token shapes what comes next. One slightly different token choice at a critical juncture can send the entire remainder of the generated answer in a completely new direction.

**[2:03]** Sampling selects a token using probabilities.

**[2:06]** Temperature adjusts those probabilities. In ChatGPT, Gemini, and Claude, temperature is set for you behind the scenes. This chart compares how different temperature settings change the odds for each dog name. Notice the center column. These are the starting odds derived directly from the model's training and the context you provided. A low temperature setting concentrates the odds onto the most likely choices.

**[2:31]** Spot leads at 22%, but at low temperature, its chance jumps to 36%. A high temperature setting does the opposite by spreading the odds out more widely. Here, Spot's chance falls to 16%. Both settings manipulate the exact same starting odds. Spot remains the most likely individual token at all three settings. Temperature changes its probability.

**[2:55]** AI answers vary. Different inputs. Different odds. Different choices.
