from pathlib import Path
import json,re
OUT=Path(__file__).resolve().parent
POINTS=[
('problem','Encouragement versus honest evaluation / Flattery definition'),
('gatsby','Gatsby essay introduction is actually taught, not merely displayed'),
('contrast','Empty praise versus missing-thesis feedback and next step'),
('positive','Positive feedback can be useful when specific'),
('why','Spoken transition into why AI leans agreeable'),
('rlhf','Reinforcement learning from human feedback, named in full'),
('training','Reviewers rank → agreement can win → training changes patterns'),
('baked','Praise gets baked into the system'),
('sycophancy','Sycophancy defined'),
('incident','April 2025 update / gag-product example'),
('quote','Actual excessive-praise response explained or quoted'),
('rollback','Rollback after three days; problem across assistants'),
('mitigation','Testing/training/instructions help but do not eliminate the problem'),
('askbridge','Bridge from mitigation into practical prompting'),
('neutral','Ask, Don’t Tell: weak/better prompt and reason'),
('gaps','Ask for the Gaps: weaknesses, omissions, opposing views and reason'),
('rubric','Use a Rubric: explicit criteria, evidence, improvement and limits'),
('saved','Saved instruction: directness, weaknesses, evidence, corrections; app support qualifier'),
('engagementbridge','Exact useful-help / did-you-choose bridge'),
('choice','Continuing is allowed; continuing without deciding is the trap'),
('slope','Slope meaning/formula and useful follow-up offer'),
('endings','One minute versus twenty-five; useful but not the original task'),
('engagement','Engagement definition and how follow-ups preempt a decision'),
('closing','Both closing lines, with no extra spoken ending')]
HARD=["The Flattery Trap is treating AI’s approval as honest evaluation.","Here’s why AI leans agreeable.","The praise literally gets baked into the system.","How you ask still matters.","Here are three ways to fight the Flattery Trap.","Even when the help is useful, there’s another question: did you choose to keep going?","The Engagement Trap is spending time you never decided to spend.","Look for specifics, not approval.","Know what you came for. When you have it, choose what happens next."]
def norm(s):return re.sub(r'[^a-z0-9]+',' ',s.lower().replace('’',"'")).strip()
def stamp(t):return f'{int(t)//60}:{t%60:05.2f}'
def quote(n,a,b):
 d=json.loads((OUT/f'transcripts/flattery-engagement-{n}.json').read_text())
 return ' '.join(s['text'] for s in d['segments'] if s['start']<b and s['end']>a)
if __name__=='__main__':
 for n in (1,2,3):
  p=OUT/f'transcripts/flattery-engagement-{n}.json'
  if not p.exists():continue
  d=json.loads(p.read_text());s=norm(' '.join(x['text'] for x in d['segments']))
  print('ROLL',n)
  for line in HARD:print('MET' if norm(line) in s else 'MISSED',line)

# Editorial ratings are based on the complete transcripts, not keyword counts.
# The slope formula is incidental to the stopping-choice lesson; compressed math
# is recorded, but is not by itself a failed Engagement explanation.
RATINGS={
1:[
('TAUGHT',0,4.07,'Direct definition; omits the longer encouragement hook.'),
('THIN',4.98,25.23,'Calls it a Gatsby intro but never reads or describes the essay itself.'),
('TAUGHT',16.74,33.11,'Identifies no evidence versus missing thesis; actual response quotes are compressed.'),
('TAUGHT',26.01,33.11,'Specificity and improvement criterion survives; positive-can-be-good qualifier is implicit.'),
('TAUGHT',33.86,35.73,''),('TAUGHT',38.72,41.73,''),('RICH',42.46,53.17,''),('TAUGHT',53.50,55.73,''),
('TAUGHT',56.76,64.97,'“Chooses” is loose shorthand; avoid emphasizing agency in visuals.'),
('TAUGHT',65.78,74.31,''),('TAUGHT',78.70,90.23,'Enough of the quoted excess to convey the failure.'),
('THIN',90.98,102.01,'Three-day rollback is spoken; cross-assistant scope is not explicit.'),
('THIN',94.72,102.01,'Testing and persistence are spoken; improvement/training/instructions compressed.'),
('TAUGHT',102.80,114.39,'Practical bridge works semantically, but the required “How you ask still matters” line is absent.'),
('TAUGHT',115.14,127.73,'Neutral evaluation explained; better prompt paraphrased.'),
('WRONG',128.36,158.95,'Good diagnostic prompt is followed by an overclaim: asking objections “override[s]” agreement and “force[s]” a correct response.'),
('RICH',159.58,181.97,'Evidence, next level, and non-guaranteed grade all taught.'),
('THIN',182.62,192.73,'Directness, weaknesses, corrections retained; evidence and app-support qualifier omitted.'),
('TAUGHT',201.72,206.65,''),('TAUGHT',207.42,214.27,'Accurately distinguishes usefulness from continuing without deciding.'),
('TAUGHT',218.24,228.67,'Question and offer summarized; actual mathematical definition/formula not spoken. Optional donor enrichment, not a required new math lesson.'),
('RICH',229.50,254.99,'Both times and useful-but-unplanned contrast preserved. “Equates” is an ASR ambiguity, likely “a quiz”; not treated as a factual error.'),
('TAUGHT',255.76,269.63,'Definition exact; “short-circuiting your ability” is overstated compared with the page’s choice framing.'),
('TAUGHT',270.44,287.67,'Both exact lines, followed by a redundant ten-second spoken outro that must be cut.')],
2:[
('RICH',0,13.49,''),('TAUGHT',14.78,25.89,'Abridged Gatsby introduction preserves its weak, generic content.'),
('RICH',26.60,54.59,'Both response quotes, evidence, missing thesis, and next step taught.'),('RICH',55.26,64.05,''),
('TAUGHT',64.88,66.43,''),('RICH',67.18,72.55,''),('RICH',73.40,91.65,'Remove the unnecessary “Over millions of interactions” aside; it is not supported by this lesson’s sources.'),('TAUGHT',92.24,94.45,''),
('TAUGHT',95.46,102.81,''),('THIN',103.66,107.97,'Gag example retained, but April 2025 and the update introducing the failure are not spoken.'),
('RICH',108.70,128.91,'Most of the original response retained; final potential-to-explode clause omitted without losing meaning.'),
('THIN',130.08,135.41,'Rollback taught; cross-assistant scope omitted.'),('TAUGHT',136.48,141.17,'Testing, training and persistence taught; explicit improvement and instructions omitted.'),
('TAUGHT',144.30,148.13,''),('RICH',148.94,164.97,''),('RICH',165.66,185.51,''),
('THIN',186.72,206.99,'Rubric/evidence/next level strong; omits the check-it-yourself/nonofficial-grade qualifier.'),
('THIN',207.98,216.19,'Support qualifier, directness, weaknesses and evidence retained; “tell me when I’m wrong” omitted.'),
('TAUGHT',221.46,226.47,''),('WRONG',227.42,233.15,'Calls extra help dangerous because useful. The lesson permits deliberate continuation; the trap is the missing decision.'),
('TAUGHT',234.22,249.05,'Actual question and follow-up options spoken; answer content summarized. Formula donor optional.'),
('RICH',249.74,278.79,'Both times and useful-but-unplanned contrast intact; quiz detail omitted without changing the comparison.'),
('RICH',279.40,290.51,''),('TAUGHT',291.18,297.35,'Exact closing with no extra spoken outro.')]
}
RATINGS[3]=[
('RICH',0,17.51,''),('THIN',18.68,26.95,'Names a weak Gatsby introduction but never reads it.'),
('TAUGHT',27.72,58.93,'Both sides explained, although the essay is absent.'),('RICH',56,63.17,''),
('TAUGHT',64.26,67.1,''),('TAUGHT',67.1,72.56,''),
('RICH',72.56,87.44,'Small.en dropped the agreement sentence. Independent base.en transcription of 1:04–1:34 confirms: “Positive, agreeable answers naturally feel better, winning approval.” Do not treat the first ASR omission as missing audio.'),
('TAUGHT',87.38,90.7,''),('TAUGHT',90.74,98.91,''),('TAUGHT',100.06,107.89,'April 2025 is spoken; the update is identified retrospectively in the rollback sentence.'),
('TAUGHT',108.96,118.59,'Compact “brilliant / genius / performance art” quotation preserves the point; less original text than roll -2.'),
('RICH',119.48,132.6,'Three days, public acknowledgment, and multiple assistants explicit.'),
('RICH',133.18,141.45,'Testing, system instructions, improvement and persistence all explicit.'),
('TAUGHT',142.16,146.67,''),('THIN',147.42,156,'Neutral prompt named without the weak prompt or reason.'),
('THIN',156,160.16,'“What’s weak?” alone omits missing pieces and opposing views.'),
('THIN',160.16,164,'Only “use a rubric to set criteria”; evidence, next level and limits absent.'),
('THIN',164,167.13,'Only lead with weaknesses; conditional app support, directness, evidence and correction absent.'),
('TAUGHT',172.76,177.72,''),('TAUGHT',223.5,239.25,'Correct choice distinction arrives in the conclusion rather than before the example.'),
('TAUGHT',178.1,195.52,'Question/offer summarized; no spoken math formula. Enough to set up the decision, not a maths explanation.'),
('RICH',195.52,222.89,'Both times, graph/practice/quiz sequence, and useful-but-unplanned comparison survive.'),
('RICH',223.5,239.25,''),('TAUGHT',243.04,249.23,'Both exact lines, no extra spoken outro. Optional “two rules” preamble can be removed.')]
