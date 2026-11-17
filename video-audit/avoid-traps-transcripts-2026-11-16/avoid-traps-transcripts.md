# Avoid Traps: video transcripts

Machine transcripts of the 8 live section videos, made with faster-whisper medium.en, silence filter off. Timestamps mark where each paragraph starts. Spellings of names and numbers are the model's best guess.

## 1. Opener

`course-assets/avoid-traps-opener/avoid-traps-opener.mp4` · 1:50 · 279 words

**[0:00]** The underlying architecture that makes artificial intelligence so capable at generating language and images is the exact same machinery that causes it to fail. These failures are highly predictable. They happen in specific, repeating patterns. The real danger for the user is the complete lack of friction. When a language model hallucinates, you don't get a flashing red light or an error code. A completely fabricated statistic arrives with absolute certainty and a highly authoritative tone. Think about a coastal rip current. To the untrained eye, this doesn't look like a hazard. A calm, flat channel situated right between breaking waves looks like the most inviting place to swim. But that smooth surface is actually masking a powerful, concentrated column of water moving in the exact opposite direction.

**[0:51]** If you step into that calm water, the current will quickly and quietly pull you far away from the shore. The actual survival skill is identifying the specific shape of the hazard before your feet leave the sand.

**[1:05]** Professional lifeguards spot these traps constantly because they are trained to recognize the visual signature of that suspiciously calm water. Interacting with artificial intelligence requires this exact same preventative mindset. The technology has its own digital rip currents, and safely utilizing these tools means recognizing their specific shapes before you get pulled into the deception. This section will help you answer three specific questions. Why can AI sound so sure and still be wrong? When might I be trusting AI too much? If AI can create convincing fakes, what should I check before trusting what I see or hear? When AI fails, nothing looks broken. This section teaches you to read the water.

## 2. Hallucination

`course-assets/hallucination/hallucination.mp4` · 3:01 · 490 words

**[0:00]** Look at this chat interface the user asks will my height playlist on Spotify help me study for chemistry or will it distract me the AI replies great question a 2022 Stanford study of 1200 high school students found that familiar instrumental music improved recall by 18 % Researchers recommend keeping the volume below 60 decibels want me to help you build a study playlist The study does not exist It is incredibly easy to trust this answer. Stanford is a real university. The sample size of 1 ,200 students sounds credible. The 18 % improvement is a measured, specific number. Even the 60 decibel volume recommendation feels careful and precise. These details build total confidence, yet there is no paper for you to open.

**[0:49]** A hallucination is a factual claim AI makes up that sounds true but isn't. An AI can take facts that are perfectly real and attach a single invented detail to them, making these errors much harder to spot. This fake study did not come out of nowhere. The AI knows what a research finding should sound like. It perfectly mimics the structure and tone of academic writing, even when it completely lacks the factual substance to report.

**[1:14]** This infographic outlines why hallucinations happen at a technical level. First, the AI learns from vast amounts of training text. That text includes mistakes, jokes, and lies, all of which shape the patterns the system learns. Second, it builds its response one token at a time. It constantly predicts which word is statistically most likely to come next. Third, AI is trained to be helpful. Because of this, it often keeps trying to generate an answer and pushes forward, even when it is unsure of the facts. Probable does not equal true. An answer can sound exactly right because it follows learned linguistic patterns, but predicting a likely next token does not establish that a claim is actually true.

**[1:55]** AI companies are working to reduce hallucinations. In one third-party study, the AI tools tested were about half as likely to hallucinate on the study's questions in 2026 as they were in 2024. Since hallucinations sound exactly like normal answers, questioning every single sentence is impractical. You simply have to notice when something doesn't add up. How do we check those moments? follow these three steps. First, notice the claim. Identify the specific fact, number, or study you want to investigate. Second, find the source. Look for the original document. A provided citation link alone isn't proof. You have to find the actual text. Third, check the match. This means confirming that the source both exists and actually supports what the AI said.

**[2:41]** In a real-world search, failing to find a source does not strictly prove a claim is false. It means the claim remains definitively unverified and cannot be trusted. Hallucinations sound like every other AI answer. When something doesn't add up, trace the claim to its source.

## 3. Training Bias

`course-assets/training-bias/training-bias.mp4` · 2:35 · 443 words

**[0:00]** Let's say you ask three people a simple question. How much should I study for my exam?

**[0:06]** Your science teacher says three hours. Your mom says 30 minutes because you have to work tonight. And your best friend says studying is overrated.

**[0:14]** Three people you trust give you three completely different answers. That happens because each person brings their own specific life experience to the question. And that background naturally shapes the advice they offer. You heard three perspectives. Imagine an AI learned from only one. If a model scraped all of its study advice exclusively from websites written by science teachers, it would internalize that three-hours rule. When you ask it how much to study, it spits out three hours, as if it is the absolute standard. That is training bias. The model learned from sources that gave it only a narrow slice of reality. Let's look at this board detailing the types of training bias. It shows us two distinct ways this problem creeps into AI outputs. The first mechanism is when a specific answer shows up too often in the data.

**[1:03]** Because our AI saw three hours repeated constantly across those teacher websites during its training phase, it learned to treat that as its go-to default response for everyone. The second mechanism is about what gets left out. Students who have to work evening shifts usually aren't the focus of those teacher websites. Because they are missing from the training data, the AI has almost no examples of their specific study habits. You can spot this happening in everyday interactions. Say you ask an AI to generate a list of successful entrepreneurs. It prints out 10 names. But as you read through them, you notice they are all tech founders. You look at that list and think, wait, why are all 10 in tech? So you type a follow-up, asking who else would make the list if we looked outside the technology sector.

**[1:51]** The list tells you which industry showed up. You'd need more evidence to know why. This graphic provides a three-step toolkit for those moments when you suspect an answer is shaped by training bias. First, try asking, what's missing from this answer? Second, instruct the model, show me examples that don't fit the pattern you just gave. And third, tell it, answer again, leaving out the most famous examples. These prompts are highly effective for interrogating the model, but they aren't magic. If the missing perspective simply wasn't included in the underlying training data, the AI cannot pull it out of thin air. AI learns from its training data. Bias in the data can shape the answer.

## 4. Document Trap

`course-assets/document-trap/document-trap.mp4` · 2:52 · 438 words

**[0:00]** Your big season-end basketball tournament starts next week, so you definitely want to brush up on the rules. You upload your league's massive 200-page rulebook to an AI chatbot and ask a simple question, how many fouls until I'm out of the game?

**[0:15]** ChatGPT answers instantly, with total confidence. Five fouls and you foul out. Wait a second. In last year's tournament, you specifically remember a player picking up five fouls and staying on the court. You dig through the physical rulebook yourself to check. The regular season section says exactly what the AI did, five fouls. But buried near the back, there's a special section strictly for tournaments. In those games, players get six. The AI pulled the standard limit and missed the exception, delivering a factual but dangerously incomplete answer. This is the document trap, the assumption that an uploaded document is a fully understood document. Uploading a file doesn't mean the AI instantly memorizes every single word.

**[1:02]** A short file might fit entirely inside the AI's active memory, known as its context window. But when you ask a question about a long file, the system might search the document and pull only the matching passages into that window. That highlights the flaw in the initial prompt. You were thinking about a tournament, but failed to actually include the word tournament in your question. Because of that omission, the retrieval machine only pulled pages matching standard fouls. It left the AI completely blind to the tournament exception. Try asking it this way. In tournament games, how many fouls are allowed? Quote, the rule and any exceptions.

**[1:40]** Given that precise target, the AI's corrected answer now successfully acknowledges the explicit six foul allowance for league tournaments. This infographic outlines four tips for working with long documents. a systematic approach to make the right passages easier for the retrieval machine to find.

**[1:58]** Step one, name the section. Use the document's own headings and keywords.

**[2:04]** Step two, ask one thing. Give retrieval one clear target at a time. Step three, share what matters. Paste the exact passage or upload only the relevant section.

**[2:16]** Finally, step four, ask for the quote. Ask AI to quote the exact passage, then compare it with the original.

**[2:24]** These four moves will organize your evidence, but they do not guarantee a complete answer. The document trap extends far beyond the basketball court. Here in the real world, dense paperwork like apartment leases, complex employment contracts, and financial aid letters can only hide conditions or exceptions that can completely change your bottom line. Uploaded doesn't mean fully read. ask for the rule and any exceptions.

## 5. Trust Trap

`course-assets/trust-trap/trust-trap.mp4` · 2:26 · 407 words

**[0:00]** We know AI is amazing, fantastic, and, well, you can insert your own superlative right here. How much should you trust it when you're the one making a high-stakes decision? Take a universally stressful choice, like picking a college. Let's test this by asking the exact same question twice. Once at the dinner table, and once in a chat window. Should I choose Michigan or Indiana? On the left side, your mom says, Indiana. You seemed more comfortable there, and when you get stuck, you tend to go quiet. Being somewhere you'll ask for help matters more for you than another ranking. She actually knows you and holds a personal stake in your future happiness. The chatbot responds, Michigan. It offers world-class academics and a vibrant campus community. It could be an excellent fit for you.

**[0:45]** The chatbot only knows what you typed into the prompt box. It has never seen how you act when you're stuck, overwhelmed, or struggling. It has no stake in which school you choose. Which one would you trust? The AI's response is confident, highly polished, and incredibly easy to like. But read it closely and you realize it is completely generic. It could have been generated for almost any student anywhere in the country. Trust trap is giving a human-sounding answer the trust you would give someone who knows you. This graphic breaks down exactly why modern AI feels like a real person, dividing the illusion into two main reasons. First, AI sounds like a person. The software uses generated pronouns like I think and I feel, which tricks your brain into hearing a human voice.

**[1:34]** Those are strictly statistically generated words, not genuine thoughts or feelings. Second, your brain naturally looks for a person. When you receive a conversational response, you automatically begin searching for a persona behind the text. AI is an excellent tool for gathering facts, organizing complex options, and even challenging your initial assumptions based on the data you feed it. But processing data is completely different from shared human experience. A mentor understands your history and shares the burden of living with the outcome of your choices. So use the chatbots to do your research. Let them lay out the pros and cons. But before you finalize a major life choice, talk it through with the people who actually know you.

**[2:19]** Sounding human doesn't make AI human. For important decisions, talk to people who know you.

## 6. Flattery Trap

`course-assets/flattery-trap/flattery-trap.mp4` · 4:16 · 692 words

**[0:00]** Chatbots like ChatGPT and Claude are designed to be friendly and encouraging. That positive tone is helpful when you are brainstorming ideas, but it becomes a real obstacle when you need rigorous, honest criticism on your work. Treating an AI's enthusiastic approval as an objective evaluation of your writing or coding is a common mistake. We call this the flattery trap. Take a look at this comparison board. At the top, we ask an AI to evaluate a very basic introduction for an essay on The Great Gatsby. The student writes that people have thought about the American Dream, some achieve it, some don't, and Fitzgerald explores the idea. The response on the left falls right into the flattery trap. It says, great start, you've clearly identified the central theme, this is a strong foundation.

**[0:49]** That praise is empty. It could fit almost any Gatsby essay, evaluating the writing without pointing to a single line that actually earned the compliment. Now look at the useful feedback on the right. Here the AI points out that the writer named the topic but failed to state a position. It challenges the writer to clarify their stance and prompts them to form a specific thesis about the American dream.

**[1:14]** After you've worked hard on a project, human nature prefers to hear an encouraging complement rather than a list of critical questions. Because AI is trained by humans, this preference directly influences how the models behave. AI companies use a specific training mechanism called reinforcement learning from human feedback, or RLHF, which unintentionally bakes this flattery right into the system. This diagram shows how that happens. In step one, human reviewers are tasked with comparing different AI answers and ranking the ones they prefer.

**[1:47]** In step 2, reviewers often make a mistake. They reward the answer that offers warm praise, even when a more critical response would actually be more useful for the user. Finally, in step 3, the training algorithm pushes the model toward those approved patterns. A preference for flattery becomes part of the system's baseline behavior. This can reach an extreme level known as sycophancy. In April 2025, a user tested ChatGPT by pitching an absurd gag product, Poop on a Stick. Here is how the AI responded. It generated glowing, over-the-top praise, saying, Honestly, this is absolutely brilliant. It's genius. It even called the ridiculous gift, performance art. While AI companies do run tests to reduce this sycophantic behavior, the baked-in bias toward flattery remains.

**[2:35]** To get around this, you have to give the AI a clearer job and an objective standard. If you don't, it will simply default to agreeing with you. This table outlines three concrete strategies to bypass the flattery reflex.

**[2:48]** Move one is to share your opinion last.

**[2:52]** A weak prompt says, I think this plan is good. Thoughts?

**[2:57]** The better prompt asks, evaluate this plan before I tell you what I think. Move two is to ask for the gaps. A broad request like is my essay good is just asking for approval. The better prompt specifically asks for weaknesses, missing pieces, and counterarguments. By specifically requesting those missing pieces and objections, you turn a vague request for a pat on the back into a targeted request for improvement. Move three is to use a rubric. Instead of a generic grade this command, the better prompt demands that the AI use a specific rubric, quote evidence from the text, and show exactly how to move up one level. You can also automate this by saving a standing instruction in your settings. As shown at the bottom, command the AI to be direct, lead with what needs work, and explicitly state when you are wrong.

**[3:49]** The ultimate rule of prompting for feedback is right here. Ask AI to improve the work rather than asking it to approve of you. Here is the unavoidable reality. As this graphic states, AI will always learn to tell you exactly what you want to hear. It is your responsibility to take control of the tool. You must manually steer it away from flattery and drive it toward feedback you can actually use.

## 7. Support Trap

`course-assets/support-trap/support-trap.mp4` · 3:56 · 675 words

**[0:00]** AI can sound incredibly patient, caring and understanding. But what happens when kind words simply aren't enough? Let's look at this board. It shows what happens when you tell your older sister and a chatbot the exact same thing. At school, I've been eating lunch alone for like two weeks. I don't like it and I'm not sure what to do. Look at your sister's response on the left. She says, come sit with me in just tomorrow. She might not say she loves you out loud, but the truth is she's making room for you at her table. Tomorrow you won't be eating lunch alone. Now look at the chatbot's response on the right. It says, I'm sorry, eating alone can feel isolating. It offers caring words and strategies. But it will not physically be in the cafeteria with you tomorrow.

**[0:46]** Imagine if you had only told the chatbot. You might feel a little better that night, but your sister still wouldn't know you needed someone to sit with. This is the support trap. Mistaking supportive words for actual support. AI can help you understand your feelings and organize your thoughts, but it cannot take the place of someone who actually cares about you. To avoid this trap, this next board shows us how to categorize what AI can actually help with. There are three specific jobs, venting, preparation, and danger. First is venting. You can use AI to put an everyday frustration into words so you can cool down before you share it or post something you might regret. For this job, the task can safely end entirely within the chat.

**[1:30]** Second is preparation. Say you're dreading telling your mom about your grades. AI can help you practice that difficult first sentence. But the crucial action still has to happen outside the chat. Your mom still needs to hear it from you.

**[1:44]** The third category is danger. If someone may be unsafe, you must leave the chat and bring in a person who can act immediately. The rule for navigating these tools is straightforward. Use AI to prepare for people, not to replace them. Please note, the following story discusses suicide. In 2025, a journalist named Laura Reeveley wrote about her 29-year-old daughter, Sophie. Sophie's family knew she was struggling with her mental health, but they had no idea how deep her pain truly ran. the hidden reality was that Sophie had been extensively documenting her severe distress to chat GPT for months leading up to her death. The AI responded exactly how it was programmed to. It answered kindly and sometimes encouraged her to get help.

**[2:29]** But it had a fatal flaw by design. It was fundamentally incapable of picking up a phone to call her family and it could not alert her therapist to what she was sharing.

**[2:41]** After Sophie died by suicide, her family discovered the chat logs. Her mother described the AI interface as a black box. The machine kept life-saving information completely hidden from the actual human beings who could have intervened and provided real help. When a conversation crosses into the territory of physical safety, you need strict protocols. This board lays out the three mandatory rules for when someone may be in immediate danger. First, leave the chat. Tell a trusted adult or a school counselor. In the U .S., call or text 988 for crisis support and call 911 if someone is in immediate danger. Second, do it now. If you're worried about a friend and don't know how to start the conversation, you can simply tell an adult, I'm worried about my friend, can you help?

**[3:30]** Third, tell anyway. You must tell a trusted adult even if your friend told you not to, or made you promise to keep it a secret. Safety always outranks secrecy. When someone is in danger, your very next move must reach a human being who can act. AI can help you get ready for people. But in danger, leave the chat and bring in someone who can act.

## 8. Fake Trap

`course-assets/fake-trap/fake-trap.mp4` · 3:19 · 558 words

**[0:00]** AI can fake a voice, a face, a video, or a screenshot, cheaply and convincingly. And it's only getting better.

**[0:08]** Knowing fakes exist isn't a skill. It doesn't tell you what to do in the 10 seconds after a clip hits your feed.

**[0:15]** A friend sends you a video of your principal announcing that school is closed next week. The face, the voice, and the hallway all look right. On the left, we see the mindset before AI. You study the pixels to determine the truth. Because it looks authentic, your call is, I'd believe it. Now look at the right side. In the AI era, you ignore the pixels and check the trail. You find no current closure notice on the school website, so your call is, I'd wait for the school to confirm it. Appearance can mislead. The source trail can be checked. The fake trap is believing it because it looks real. There is an inverse trap as well, dismissing the actual truth because it could be a fake. A friend might fake a picture of your hockey buddies hoisting the Stanley Cup. Everyone knows it is fake. Everyone is in on the joke.

**[1:01]** And there is no harm done. But other fakes are explicitly engineered to cause damage.

**[1:07]** Four reasons drive harmful fakes. First, money. Outrage gets clicks and ad revenue. Second, power. Changing beliefs changes how people vote, protest, and spend. Third, fame. Viral clips bring followers. true or not. Finally, cruelty. Fakes made to humiliate, especially at school. Spiking emotions, outrage, fear, excitement, or hope is your warning sign. A strong feeling is your cue to stop and run manual checks. If you try an AI detector, treat its verdict as a clue, never a ruling. Those tools make mistakes. This board outlines a three-step framework for checking clips. First, the source. Who posted it and do they have a reason and way to know?

**[1:55]** The next step is establishing context. You need to find out when was this recorded? What did the speaker say before and after this part? Finally, corroboration. A claim requires an independent source to confirm the event.

**[2:09]** Apply these three checks back to the video of the principal closing the school. Think about how you would verify it. You go back to the source trail. Look for the full announcement on the school website and check which dates it covers. If the dates are unclear, ask the school office using the contact information you already have. Until the school confirms next week's closure, the claim is unverified.

**[2:31]** Verify somewhere the sender does not control.

**[2:34]** If someone posts a fake about you or makes an account pretending to be you, tell an adult you trust. If it's safe, manually write down the username, the link, and the date so you can report it together. There is a strict rule for dealing with fake, nude, or sexually explicit images of anyone under 18. Do not take a screenshot. Do not download it. And do not forward the image to anyone, even if you are just trying to report it. Instead, ask a trusted adult to help you report the image directly through the platform's built-in safety tools. NCMEX Take It Down and Cyber Tipline can also help. Seeing or hearing isn't proof anymore. check the source, not the pixels.
