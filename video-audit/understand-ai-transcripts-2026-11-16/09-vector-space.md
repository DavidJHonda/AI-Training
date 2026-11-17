# 9. Vector Space

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
