#!/usr/bin/env python3
"""Build the six one-page course toolkit references; reuse Five Big Ideas unchanged.
Run with .video-venv/bin/python3 (bash scripts/video/env.sh installs reportlab,
pypdf, and Pillow). Downloadable PDFs live in packets/.
Pass guide filenames to rebuild selected PDFs; omit them to build all six.
"""
from pathlib import Path
import json, hashlib, sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
INK='#0e0a1f'; BODY='#3a3550'
GUIDES=[
 dict(slug='evaluation-matters', file='evaluation-matters-guide',id='evaluating', title='Evaluation Matters', desc='A practical checklist for deciding whether an AI answer is ready to use.', subtitle='Is it right? Is it good enough for what I need?', takeaway='The tool answers. You evaluate.', vertical_expansion=20, body_size=11.5, body_leading=16.5, sections=[
 ('01  Do a quick review', '<b>Read.</b> Read the answer before you use it. If you pass it along, you are responsible for what it says.<br/><b>Understand.</b> You cannot judge an answer you do not understand. Ask for a simpler explanation of anything unclear.<br/><b>Validate.</b> Compare the answer with what you know and what you asked for. Is anything wrong, missing, or not useful?'),
 ('02  Take a closer look', 'A quick review is often enough. When more is riding on the answer, or you are not sure it is right, take a closer look.<br/><br/><b>What kind of task?</b> A factual answer needs accurate information. A draft needs clear writing. A plan needs to work.<br/><b>How much is riding on it?</b> What happens if the answer is wrong? The more that depends on it, the more carefully you should check it.<br/><br/><b>Check the sources.</b> Ask for sources, then open them. Are they reliable, and do they support the claims? For current information, ask AI to search the web.<br/><b>Challenge the answer.</b> Ask for the strongest argument against it or what important information was left out. Decide whether that changes your view.<br/><b>Check it yourself.</b> Recalculate the numbers, test the code, or ask someone who knows the subject.'),
 ('03  Make your move', '<b>Use it.</b> The answer is right and good enough for what you need.<br/><b>Fix it.</b> Tell AI what needs to change, or change it yourself. Check the revised answer before using it.<br/><b>Walk away.</b> If AI is not helping, try another approach or ask someone who knows the subject.')]),
 dict(slug='where-ai-works-best',file='where-ai-works-best-guide',body_size=12,body_leading=18,id='whatitdoesbest',standalone_sections=['Keep your judgment in the process'],title='Where AI Works Best',desc='Four useful kinds of work, with examples to help you get started.',subtitle='Match the job to one of these four strengths.',takeaway='AI gives you a starting point. You make the call.',sections=[
 ('01  Reshape your material','Give AI something you already have and ask for it in a different form. Keep the meaning while changing the presentation.<br/><b>Try:</b> Turn notes into a table, a voice memo into a to-do list, or technical instructions into plain language.'),
 ('02  Explore possibilities','Ask for options when you are stuck or want more choices. React to the ideas and ask for more of what interests you.<br/><b>Try:</b> Brainstorm essay angles, club names, story openings, or fundraiser ideas.'),
 ('03  Find what matters','Give AI a document or several sources and say what you need to know. Use the result to decide where to focus.<br/><b>Try:</b> Find scholarship requirements, summarize a chapter, or compare two articles.'),
 ('04  Work through problems','Describe your goal, what you know, and what is getting in the way. Ask AI to break the problem into steps or compare approaches.<br/><b>Try:</b> Plan a trip within a budget, troubleshoot code, or investigate an unexpected experiment result.'),
 ('Keep your judgment in the process','Check that rewrites preserve your meaning, summaries match the sources, and proposed ideas or solutions fit your situation. A fluent result is not a guarantee.')]),
 dict(slug='prompting-matters',file='prompting-matters-guide',body_size=11,body_leading=15,step_gap=19,id='prompting',vertical_expansion=20,standalone_sections=['Start with a good question','A reusable outline','Put it together'],title='Prompting Matters',desc='Four prompting moves, a worked example, and an outline you can reuse.',subtitle='Start with a good question. Then give AI what it needs.',takeaway='A prompt is a briefing, not magic words.',sections=[
 ('Start with a good question','Use what you learned in Questions Matter. Then give AI the information and instructions it needs with these four moves.'),
 ('01  Share your situation','Tell AI who you are, who the work is for, what you are working on, and why. Do not make it guess.'),
 ('02  Give it the material','Include the actual draft, notes, assignment, rubric, numbers, or source you want it to use. Share only what the task needs.'),
 ('03  Describe the answer you want','Specify the format, length, tone, and what to skip. Give an example when it would help.'),
 ('04  One job at a time','Break big work into steps. Ask for the next step and say where AI should stop. Review each part before moving on.'),
 ('A reusable outline','I am working on <b>[task]</b> for <b>[audience or purpose]</b>.<br/>Use <b>[material]</b>. Help me <b>[specific next step]</b>.<br/>Give me <b>[format]</b>, with <b>[limits]</b>.<br/>Stop after <b>[step]</b> so I can review.'),
 ('Put it together','“I’m preparing a history presentation for my class. Here are my notes and the rubric. Suggest three possible main arguments in a short list. Use only these notes. Wait for me to choose before making an outline.”<br/><br/>A quick factual question: just ask. Real work: share your situation, material, and desired answer. A big project: work one job at a time.')]),
 dict(slug='critical-thinking',file='critical-thinking-five-habits-guide',body_size=12,body_leading=18.5,id='critical',standalone_sections=['Use these beyond AI'],title='Five Habits of Critical Thinking',desc='Five questions to use with AI, news, schoolwork, and everyday claims.',subtitle='Pause, examine the claim, and make your own decision.',takeaway='Good thinking in, sharper output.',sections=[
 ('01  Is it actually right?','What evidence supports the claim? Does that evidence support the conclusion?'),
 ('02  Do I know enough to judge?','Recognize where your knowledge ends. Find out what you need to understand before deciding.'),
 ('03  What’s missing?','Look for missing information and other explanations. Would a different fact change the conclusion?'),
 ('04  Why am I convinced?','Is it the evidence, the confident wording, or what you want to believe?'),
 ('05  What’s my call?','Decide what to believe or do. You can change your mind when you learn more.'),
 ('Use these beyond AI','These questions work on anything you read or hear. AI can help you look for weaknesses in an argument, but you still judge whether its answer holds up.')]),
 dict(slug='honesty-and-privacy',file='honesty-and-privacy-sharing-guide',body_size=11.5,body_leading=16.5,vertical_expansion=20,step_gap=19,id='integrity',title='Share Only What AI Needs',desc='What to share, what to keep out, and what to do if you already shared it.',subtitle='Give useful context without sharing unnecessary personal details.',takeaway='You meant to share the task. Check everything you send.',sections=[
 ('Usually fine','Interests, goals, preferences, and broad details about the situation. Include what helps AI understand the job.'),
 ('Only when needed','Health, medication, family situations, grades, income, expenses, or debt. Keep details general whenever possible and include only what the task needs.'),
 ('Keep out','Passwords, security codes, account numbers, identification numbers, home addresses, and other people’s private information.'),
 ('Before attaching a file or image','Check the whole item, including names, background details, notifications, and unrelated pages. Crop or remove what the task does not need, then check the edited copy. For homework help, share the problem without student names, school details, or private information elsewhere in the photo. You can type the relevant information instead.'),
 ('Ask before sending','What does AI actually need for this task? Can I remove a detail or describe it more generally and still get useful help?'),
 ('Why this matters','An AI chat is a record sent to an outside system. It may stay in your account, be read by people at the AI company, be handed over if the law requires it, or be seen by someone who gets into your device or account.'),
 ('If you already shared it','Delete the chat from your history. This removes it from the app’s visible history, but a copy may remain in the AI company’s systems for a period of time. Each app has its own deletion policy.<br/><br/><b>Shared a password or security code?</b> Deleting the chat is not enough. Change any passwords or security codes you shared.')]),
 dict(slug='honesty-and-privacy',file='honesty-and-privacy-school-guide',body_size=12,body_leading=18.5,id='integrity',title='Using AI in School',desc='Check the rules, understand your work, and explain how AI helped.',subtitle='Own what you submit and be clear about how it was made.',takeaway='If your name is on the work, you own how it was made.',sections=[
 ('01  Start with the assignment rules','AI help may be allowed in one class and prohibited in another. Check the policy and ask your teacher when it is unclear. Disclose AI use as required.'),
 ('02  Use AI to support learning','When permitted, use it to practice, ask for explanations, get feedback, or improve work you understand and created. Do not submit AI-generated work as your own or use AI when the assignment prohibits it.'),
 ('03  Understand it','Be able to explain the ideas and choices in your work yourself. If you cannot, keep learning before you submit.'),
 ('04  Show your process','Keep drafts, sources, and relevant AI conversations so you can show how the work developed.'),
 ('05  Explain AI’s role','Clearly say what you did and how AI helped. Adapt this example truthfully and follow your teacher’s disclosure requirements:<br/><br/>“I wrote the draft and used AI to identify unclear passages. I chose and made the revisions and checked the facts against my sources.”')])
]
def editorial(c,g):
 """Shared toolkit layout; number steps and retain descriptive supplementary headings."""
 left=58;right=554;width=right-left
 expansion=g.get('vertical_expansion',0)
 def text(value,x,y,font,size,color):
  c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,y,value)
 text('BE SMARTER THAN THE TOOL',left,730+expansion,'GuideBold',9.5,'#704cff')
 text('/  YOUR AI TOOLKIT',left+pdfmetrics.stringWidth('BE SMARTER THAN THE TOOL','GuideBold',9.5)+8,730+expansion,'GuideBold',9.5,'#625c7a')
 title_size=min(30,30*width/pdfmetrics.stringWidth(g['title'],'GuideBold',30))
 text(g['title'],left,687+expansion,'GuideBold',title_size,INK)
 subtitle_size=min(13.5,13.5*width/pdfmetrics.stringWidth(g['subtitle'],'Guide',13.5))
 text(g['subtitle'],left,662+expansion,'Guide',subtitle_size,'#625c7a')
 c.setStrokeColor(HexColor('#dcd5f5'));c.setLineWidth(.5);c.line(left,642+expansion,right,642+expansion)
 numbered=any('  ' in heading for heading,_ in g['sections'])
 body_x=104 if numbered else left
 body_width=right-body_x
 standalone=[heading in g.get('standalone_sections',[]) for heading,_ in g['sections']]
 section_widths=[width if separate else body_width for separate in standalone]
 # Shared spacing defaults; denser guides can adjust the gap between sections.
 label_gap=4;step_gap=g.get('step_gap',24);example_gap=5;coda_before=20;coda_after=16
 style=ParagraphStyle('editorial-body',fontName='Guide',fontSize=g['body_size'],leading=g['body_leading'],textColor=HexColor(BODY))
 example_style=ParagraphStyle('editorial-example',parent=style,fontSize=10.5,textColor=HexColor('#5c5680'))
 y=616+expansion
 if 'figure' in g:
  f=g['figure'];image=Image.open(ROOT/f['path']).convert('RGB').crop(f['crop'])
  figure_width=f.get('width',width);figure_height=figure_width*image.height/image.width
  c.drawImage(ImageReader(image),left+(width-figure_width)/2,y+10-figure_height,figure_width,figure_height)
  y-=figure_height+14
 for i,((heading,body),separate,section_width) in enumerate(zip(g['sections'],standalone,section_widths)):
  section_x=left if separate else body_x
  if i:
   y-=coda_before if separate else step_gap
  if separate and i:
   c.setStrokeColor(HexColor('#dcd5f5'));c.setLineWidth(.5);c.line(left,y,right,y)
   y-=coda_after
  if '  ' in heading:
   number,label=heading.split('  ',1)
   text(number,left,y-7,'GuideBold',23,'#704cff')
  else:label=heading
  assert pdfmetrics.stringWidth(label.upper(),'GuideBold',12)<=section_width,label
  text(label.upper(),section_x,y,'GuideBold',12,INK)
  y-=label_gap
  parts=body.split('<br/><b>Try:</b>',1)
  p=Paragraph(parts[0],style);_,height=p.wrap(section_width,1000)
  p.drawOn(c,section_x,y-height);y-=height
  if len(parts)==2:
   y-=example_gap
   example=Paragraph('<b>Try:</b>'+parts[1],example_style)
   _,height=example.wrap(section_width,1000)
   example.drawOn(c,section_x,y-height);y-=height
 assert y>=178-expansion,('Guide content overlaps the takeaway',g['title'],y)
 c.setFillColor(HexColor('#ffe187'));c.roundRect(left,116-expansion,width,42,8,fill=1,stroke=0)
 c.setFillColor(HexColor('#704cff'));c.circle(82,137-expansion,8,fill=1,stroke=0)
 c.setStrokeColor(HexColor('#ffffff'));c.setLineWidth(1.8)
 path=c.beginPath();path.moveTo(78.5,137-expansion);path.lineTo(81,134.5-expansion);path.lineTo(85.5,139.5-expansion);c.drawPath(path)
 takeaway_size=min(14.5,14.5*(right-116)/pdfmetrics.stringWidth(g['takeaway'],'GuideBold',14.5))
 text(g['takeaway'],100,131-expansion,'GuideBold',takeaway_size,INK)
 c.setStrokeColor(HexColor('#dcd5f5'));c.setLineWidth(.5);c.line(left,97-expansion,right,97-expansion)
 text("© 2026 Nate O’Brien and Luke O’Brien. All rights reserved.",left,77-expansion,'Guide',8.6,'#625c7a')
 website_x=left+pdfmetrics.stringWidth("© 2026 Nate O’Brien and Luke O’Brien. All rights reserved.",'Guide',8.6)+5
 text('besmarterthanthetool.com',website_x,77-expansion,'GuideBold',8.6,'#625c7a')
 c.linkURL('https://besmarterthanthetool.com',(website_x,74-expansion,right,88-expansion),relative=0)

def build():
 fontroot=Path('/System/Library/Fonts/Supplemental')
 pdfmetrics.registerFont(TTFont('Guide',str(fontroot/'Arial.ttf')))
 pdfmetrics.registerFont(TTFont('GuideBold',str(fontroot/'Arial Bold.ttf')))
 pdfmetrics.registerFontFamily('Guide',normal='Guide',bold='GuideBold',italic='Guide',boldItalic='GuideBold')
 manifest_path=ROOT/'course-assets/manifest.json';manifest=json.loads(manifest_path.read_text())
 selected=GUIDES if len(sys.argv)==1 else [g for g in GUIDES if g['file'] in sys.argv[1:]]
 if not selected: raise SystemExit('Unknown guide filename')
 for g in selected:
  out=ROOT/'packets'/(g['file']+'.pdf');out.parent.mkdir(parents=True,exist_ok=True)
  c=canvas.Canvas(str(out),pagesize=(612,792));c.setTitle(g['title']);c.setAuthor("Nate O'Brien and Luke O'Brien");c.setSubject('Be Smarter Than the Tool | Your AI Toolkit')
  editorial(c,g)
  c.showPage();c.save();reader=PdfReader(out);assert len(reader.pages)==1;assert g['title'] in reader.pages[0].extract_text()
  rel=str(out.relative_to(ROOT))
  entry={'new':rel,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'reference_files':['index.html'],'generator':'scripts/build-course-toolkit.py','purpose':'One-page course toolkit PDF reference.','pages':1}
  manifest['generated_assets']=[x for x in manifest['generated_assets'] if x.get('new')!=rel]+[entry]
  print(out.relative_to(ROOT))
 manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':build()
