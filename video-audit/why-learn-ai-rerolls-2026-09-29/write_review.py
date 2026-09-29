from pathlib import Path
import json,re
p=Path(__file__).parent
# Each cell: status, timestamp, exact excerpt from the fresh transcript.
rows=[
('Scribe and steady hand-copying work',('RICH','0:00–0:10','hand copy documents and proclamations'),('RICH','0:00–0:10','hand copy the king\'s proclamations'),('RICH','0:00–0:11','Your entire career is built on hand-copying'), 'Tie; keep 2.'),
('New press, thousandfold output, ignore it or learn it',('RICH','0:11–0:25','It prints pages a thousand times faster'),('RICH','0:11–0:27','learn the machine well enough to operate it'),('RICH','0:12–0:30','learn the mechanics of the machine'), 'Tie; keep 2. Mainz/mines is an ASR spelling issue, not an established spoken error.'),
('Explicitly map the press choice to learning AI',('RICH','0:26–0:37','learning to use it is today\'s version of learning to run that new machine'),('TAUGHT','0:27–0:33','Today, AI is the press in this comparison'),('TAUGHT','0:31–0:40','AI functions as today\'s version of that printing press'), 'Take 1: explains the correspondence and supplies the exact banner.'),
('AI already in everyday tools',('TAUGHT','0:38–0:48','inside your phone, your apps, and the search results'),('RICH','0:34–0:44','the tools your first job will hand you on day one'),('TAUGHT','0:41–0:49','a component of your current digital tools'), 'Keep 2. Search results omitted, but phone and workplace teaching intact; 3 loses that specificity.'),
('Current AI capabilities improve',('TAUGHT','0:47–0:50','Most of what it does today, it will do better tomorrow'),('TAUGHT','0:44–0:47','Most of what it does today, it will do better tomorrow'),('TAUGHT','0:45–0:49','become more capable every year'), 'Keep 2; 3 teaches the meaning but misses required wording.'),
('Overview orients before the five familiar uses',('TAUGHT','0:50–0:54','This graphic maps out exactly where AI already functions'),('TAUGHT','0:48–0:53','exactly where AI already lives in your daily routine'),('TAUGHT','0:49–0:52','five areas where you likely interact with AI daily'), 'Keep 2; all three introduce before developing.'),
('Recommendations: prediction, Spotify/Netflix/TikTok',('TAUGHT','0:55–0:58','predicting what you might like next on platforms like Spotify'),('RICH','0:54–1:01','Spotify, Netflix, and TikTok'),('RICH','0:53–0:57','predicting your preferences on Spotify, Netflix, and TikTok'), 'Keep 2. 1 omits Netflix and TikTok.'),
('Navigation: traffic AND arrival time, Maps/Waze',('THIN','0:59–1:01','calculating traffic in Google Maps'),('RICH','1:02–1:07','predict traffic and your arrival time on apps like Google Maps and Waze'),('THIN','0:58–1:02','predicting traffic patterns on Google Maps and Waze'), 'Take 2; 1 and 3 omit arrival-time teaching; 1 also omits Waze.'),
('Face recognition: matching, unlock AND tagging',('THIN','1:01–1:04','unlocking your phone with face recognition'),('RICH','1:08–1:14','checking whether a face matches you for phone unlocks and photo tagging'),('TAUGHT','1:03–1:06','AI matching your face to unlock your phone'), 'Take 2. 1 never explains matching; 1 and 3 omit tagging.'),
('Voice assistants: speech to words and all examples',('TAUGHT','1:04–1:06','turning spoken commands into text'),('RICH','1:15–1:21','Siri, Alexa, or Hey Google'),('TAUGHT','1:06–1:10','turning your spoken words into text for assistance like Siri and Alexa'), 'Take 2. 1 gives no named examples; 3 omits Hey Google.'),
('Chatbots: conversation and ChatGPT/Claude/Gemini',('THIN','1:06–1:08','Finally, chatbots'),('RICH','1:21–1:28','chatbots carry on direct conversations with you'),('RICH','1:11–1:17','chatbots like ChatGPT and Claude'), 'Take 2. 1 only names the category; 3 omits Gemini. Clod in roll-2 ASR is not by itself a pronunciation verdict.'),
('AI was part of daily life before chatbots',('MISSING','1:08–1:10','AI was already part of your day'),('TAUGHT','1:32–1:35','AI was already part of your day before chatbots arrived'),('TAUGHT','1:18–1:24','these other forms of AI were already a standard part of your day long before they arrived'), 'Take 2. 1 drops the chronological distinction, not just wording.'),
('Move from familiar use to deliberate practice; start now',('RICH','1:11–1:18','shift from being a passive consumer to an active user. You can start now'),('TAUGHT','1:36–1:39','Because you already use it passively, you can start now'),('TAUGHT','1:25–1:33','move from passive use to deliberate practice'), 'Take 1 as part of the coherent practice/design run. Its “easily” is encouragement, not a promise of mastery.'),
('Learn strengths, notice struggles, practice on a meaningful project',('RICH','1:18–1:24','Learn what AI does well, notice where it struggles'),('RICH','1:40–1:45','practice using it for something you care about'),('TAUGHT','1:34–1:43','identifying what the AI does well, noting where it produces errors, and applying it to a personal project'), '1 and 2 both meet the original repair target. Take 1 with adjacent beats. 3 compresses the idea but does teach its meaning.'),
('Each project supplies experience for the next',('TAUGHT','1:24–1:27','Every project gives you experience you can bring to the next one'),('TAUGHT','1:46–1:50','Every single project gives you cumulative experience that you can bring to the next one'),('THIN','1:42–1:43','to gain practical experience'), 'Take 1: exact line, simpler voice. 3 never explains project-to-project carryover.'),
('Bridge into desktop publishing as an example of learning by making',('RICH','1:28–1:31','We have seen tools close the gap between ideas and creation before'),('TAUGHT','1:51–1:57','Before personal computers, becoming a designer meant spending years at a drafting table'),('TAUGHT','1:44–1:50','Before personal computers, becoming a designer required years at a drafting table'), 'Take 1. Its spoken bridge makes why this example follows explicit; the other two are understandable but less connected.'),
('Desktop publishing: teen access and concrete products',('RICH','1:32–1:47','a teenager with a personal computer could design posters, magazines, and brochures'),('RICH','1:51–2:07','powerful design tools on a teenager\'s desk'),('TAUGHT','1:44–2:02','professional design software on a standard desk'), 'Take 1 for the full product list; keep drawings from 2. 2 omits magazines, 3 omits brochures and the explicit teenager access.'),
('Tool does not replace skill; shortens path to doing the work',('RICH','1:47–1:54','The tool didn\'t replace skill'),('RICH','2:08–2:14','It simply shortened the distance between wanting to do the work and actually doing it'),('TAUGHT','2:03–2:07','it didn\'t replace the need for an eye for layout'), '1 and 2 equally strong. Take 1 as part of the whole example.'),
('Explicitly transfer the design example back to AI and building skill',('RICH','1:54–1:57','AI gives you a similar chance to start making things while you build your skills'),('RICH','2:15–2:19','AI gives you a similar chance to start making things while you build your skills'),('TAUGHT','2:08–2:13','AI offers a similar path. It reduces the time from an idea to a finished product'), 'Take 1 with the example; 2 also meets the exact requirement. 3 emphasizes speed more than learning.'),
('Brief overview before the three reasons',('TAUGHT','1:58–2:03','three reasons you will thrive in the AI future'),('TAUGHT','2:19–2:25','three specific reasons why you\'ll thrive in the AI future'),('TAUGHT','2:14–2:17','These three panels outline why starting now helps you adapt'), 'Keep 2; no repeated introductory overview needed.'),
('This Is Your Time: school, try things, ask questions, learn',('THIN','2:03–2:08','try new things and learn without professional risk'),('RICH','2:26–2:35','try new things, ask questions, and learn from the results'),('THIN','2:18–2:21','school provides a safe environment to experiment'), 'Take 2. 1 and 3 omit practical directions; “without professional risk” is an unsupported assurance in 1.'),
('Move Faster: try ideas, feedback, previously inaccessible projects',('RICH','2:08–2:14','tackling intimidating projects by quickly testing ideas and getting feedback'),('RICH','2:36–2:43','tackle projects you otherwise wouldn\'t know how to start'),('THIN','2:22–2:27','AI provides immediate feedback, helping you complete complex projects faster'), 'Keep 2; preserves trying ideas and help getting started. 3 reduces the benefit to feedback/speed.'),
('Good habits: questions, checking answers, own decisions',('THIN','2:14–2:21','Verifying AI answers develops practices that stay with you'),('RICH','2:44–2:53','asking good questions, checking answers, and making your own independent decisions'),('THIN','2:28–2:33','lasting habits like verifying information'), 'Take 2. 1 and 3 drop asking questions and independent decisions.'),
('Skills carry forward / thrive takeaway',('TAUGHT','2:21–2:24','Start now. Build skills for whatever comes next'),('TAUGHT','2:54–2:57','Start now. Build skills you\'ll carry into whatever comes next'),('TAUGHT','2:31–2:33','a foundation for any career path'), 'Keep 2: exact banner. 1 and 3 compress and miss literal requirements.'),
('Historical pattern: steam/labor, electricity/factories, internet/information',('TAUGHT','2:24–2:34','electricity scaled up factories, and the internet connected global information'),('RICH','2:58–3:13','New tools consistently change how people work'),('TAUGHT','2:34–2:51','History shows a clear pattern of tools changing the way we work'), 'Keep 2 through the internet example. 3 adds dates and assembly-line detail unnecessarily.'),
('Qualified breadth of AI, without narrowing earlier technologies',('TAUGHT','2:35–2:37','AI could do it across almost everything'),('WRONG','3:14–3:20','Those past technologies were specialized to specific industries'),('TAUGHT','2:52–3:05','across many different fields'), 'Take 1 after 2\'s historical examples. 2 adds an unsupported categorical contrast; 3 loses the source\'s careful “could” wording.'),
('White House attribution, July 2025, strategy title',('TAUGHT','2:40–2:47','the White House released an official national strategy document'),('TAUGHT','3:21–3:28','Winning the Race, America\'s AI Action Plan'),('TAUGHT','3:06–3:13','a 2025 national strategy document'), 'Take 1 with the quotation. 3 drops White House and July.'),
('Required quotation and its potential framing',('RICH','2:51–2:58','an industrial revolution, an information revolution, and a renaissance all at once'),('WRONG','3:29–3:42','predicting it will simultaneously automate physical manufacturing'),('THIN','3:14–3:28','industrial output, digital communication, and creative work are all being upgraded'), 'Take 1: complete exact quote, including “This is the potential that AI presents.” 2 substitutes a prediction; 3 has the three-part phrase but replaces the potential sentence.'),
('Exact two-line close returns to press metaphor',('TAUGHT','3:06–3:09','AI is today\'s printing press. Learn to run it'),('TAUGHT','3:43–3:46','AI is today\'s printing press. Learn to run it'),('TAUGHT','3:29–3:32','AI is today\'s printing press. Learn to run it'), 'Keep 2. All three contain the exact close in transcription.'),
]
intro='''# Why Learn AI? — three new versions, September 29, 2026

**Recommendation: use Version 2 as the base, with three coherent narration passages from Version 1. Do not use Version 3 as the base.** The revised prep fixed the largest gap in Versions 1 and 2: both now teach strengths, struggles, personally meaningful practice, and experience carried into the next project. Version 2 best preserves the everyday examples and the practical instructions on the thrive board. Version 1 has the strongest bridge into desktop publishing and the complete required quotation.

**Verdicts are proposed REPAIR dispositions, pending listening to the joins.** None of the raw files earns KEEP against all required teaching and exact lines. Identified donor words support a repair route; because no direct audio audition was available, the joins are not certified and these are not verified REPAIR/shipping passes. Another generation is not the first step I recommend.

| Candidate | Runtime | Proposed disposition | Deciding issue |
|---|---|---|---|
| `Prompts/why-learn-ai-1.mp4` | 3:12.30 | REPAIR candidate; donor | Compresses the five uses and thrive instructions, but has a connected practice/design sequence and exact quotation. |
| `Prompts/why-learn-ai-2.mp4` | 3:49.13 | REPAIR candidate; recommended base | Strongest detailed teaching. Restore exact press/project wording; replace unsupported historical contrast and substituted quotation. |
| `Prompts/why-learn-ai-3.mp4` | 3:35.20 | REPAIR candidate; not selected | Practical habits and project-to-project learning are compressed; much required wording is paraphrased. No essential beat is stronger enough to displace 1 or 2. |

## Evidence and limits

Read the current `WhyDeeperSection` in `index.html`, all upload Markdown and prompt text, and the complete fresh transcripts of all three files. The current page remains the teaching authority; the revised upload source supplies the intended bridges. Current canonical board content and the prior 720p readability inspection informed the production plan.

Each MP4 was hashed and sequentially decoded; each has a complete `small.en` word-timestamp transcript, eight-second frame samples, contact sheets, and frame-count/runtime metadata in its own subfolder. The critical Version 1 practice/design and quotation passages and Version 2 historical/quotation passage were independently checked with `base.en`. Automated transcribers emitted numerical warnings but completed and agreed on these decisive passages. ASR alone is not audio listening. “Mines” for Mainz, “Clod” for Claude, and “Desk tab” for desktop are not treated as established pronunciation errors; the second pass renders “desktop publishing” correctly.

**LISTENING: no direct audio audition or continuous real-time viewing.** Intonation, voice continuity, breaths, pronunciation and seams remain unverified. Silence detection supports proposed cut locations but cannot certify natural pacing or unclipped words. Contact sheets and full-size selected frames support a proposed visual plan, not exhaustive final-frame QA. No production video was built or shipped; the live file, page, prep materials, and tracker were not changed. The external tracker was not accessed.

The version numbers mean these newly uploaded files, identified by hashes in their `source.json` files; they are not the deleted earlier rolls with the same names.

## Teaching-flow finding

The original lesson order still works. Each version connects the press to AI and puts familiar uses before deliberate practice. Versions 1 and 2 fix the missing how-to-start instruction; Version 3 reduces the carry-forward lesson to “gain practical experience.”

Version 1 makes the best transition into the design example: “We have seen tools close the gap between ideas and creation before.” Its example then returns explicitly to making things with AI while developing skill. Version 2 supplies the richer explanations on either side of this passage. The proposed joins preserve that whole progression: complete everyday takeaway → deliberate practice → experience carried forward → historical design example → explicit AI transfer → three practical reasons.

The history section follows naturally; moving it is unnecessary. Version 2 repeats the unwanted categorical claim at 3:14–3:17 and substitutes a prediction for the quotation at 3:32–3:40. Replacing that final passage with Version 1 keeps the historical comparison qualified and lets the exact close finish the lesson.

Optional transition polish is not treated as a failed teaching point. Missing explanation, practical directions, and required language are.

## Beat-by-beat comparison

Every cell quotes actual transcript wording. MISSING and THIN cells may quote the adjacent or compressed language to show what the viewer receives. Times are source-file times, rounded for reading; exact word times are in the transcripts. WRONG refers to a material departure from the lesson's distinction or attributed quotation, not an independent audit of the entire historical source.

| Teaching point | Version 1 | Version 2 | Version 3 | Selection / reason |
|---|---|---|---|---|
'''
lines=[intro]
for label,*parts in rows:
 cells=[]
 for status,t,quote in parts[:3]:cells.append(f'**{status}** {t}: “{quote}”')
 lines.append('| '+ ' | '.join([label,*cells,parts[3]])+' |\n')
(p/'REVIEW.md').write_text(''.join(lines))
for n in (1,2,3):
 t=[f'# Why Learn AI? — Version {n}\n\n',f'CANDIDATE: `Prompts/why-learn-ai-{n}.mp4`\n\nVERDICT: proposed REPAIR; not verified until contextual listening. See ../REVIEW.md for comparison and selected plan.\n\nTEACHING POINTS:\n\n']
 for row in rows:
  status,stamp,quote=row[n];t.append(f'- {row[0]} — **{status}** — {stamp}: “{quote}”\n')
 t.append('\nHARD REQUIREMENTS, ERRORS, SOURCE_QA, ADDITIONS, REPAIR PLAN, EDITING NOTES: see shared REVIEW.md, which records the complete comparison and avoids treating alternative raw edits as authorized builds.\n\nLISTENING: none directly; automated complete transcription and sampled visual review. No shipping claim.\n')
 (p/f'why-learn-ai-{n}'/'REVIEW.md').write_text(''.join(t))
print('Comparative and per-version teaching reviews written.')
