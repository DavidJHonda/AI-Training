# Narration review task (one lesson per agent), 2026-09-26

Repo: /Users/davidobrien/Developer/AI-Training (run every command from there). Review dir:
video-audit/work-with-ai-live-review-2026-09-26/<slug>/ (already exists).

Read first, completely: scripts/video/NARRATION-REVIEW.md (the owner's spec; no scores, verdict KEEP/REPAIR/REROLL).

Required inputs for your lesson (all four, no skipping):
1. The LIVE PAGE in index.html is the authority for the essential teaching points. Find the
   lesson's section component: `grep -n 'sectionId: "<lessonId>"' index.html` gives the start;
   read from there down to `closeBoard("<lessonId>")` (the close pill/sticky lines are in the
   CLOSE_BOARDS map: `grep -n '^  <lessonId>: { pill' index.html`). Read the JSX as a page:
   headings, paragraphs, Callouts, card text, board images' alt text, the TRY IT (not taught
   in video), the two closing lines.
2. lessons/<markdown>.md — the upload source (what the roll was asked to teach). Extra
   video-prep nuance there is an accurate addition, not an error. If it LACKS something the
   page teaches, that is a materials bug: report it in EDITING NOTES.
3. Prompts/<prompt>.txt and the lesson's section of Prompts/WORK-WITH-AI-VIDEO-KITS.md — the
   hard requirements (verbatim lines, named terms, the two closing lines, ordering rules,
   "say the word X", banned words).
4. The transcript of the LIVE video: video-audit/work-with-ai-live-review-2026-09-26/_transcripts/<slug>.txt
   (segments with start-end seconds) and <slug>.json (word timestamps; use it for exact
   onsets). Read the whole transcript. You cannot listen to audio: say so under LISTENING and
   treat uncertain words as unresolved rather than guessing.
Also useful: the lesson's boards are the JPGs in course-assets/<slug>/ (read them if a board's
printed text is a teaching point you need to check).

Procedure: exactly NARRATION-REVIEW.md. List every teaching point in lesson order (hook,
each explanation, every worked example with its numbers/names, distinctions, hard
requirements, takeaway/closing lines); rate each RICH / TAUGHT / THIN / MISSING / WRONG with
the timestamp and the words actually spoken; hard requirements MET / MISSED with the spoken
words; ERRORS; SOURCE_QA; ADDITIONS; REPAIR PLAN (only feasible cuts/moves inside THIS file:
no raw rolls survive for this lesson, so a donor is "none available" unless the live file
itself contains the words); EDITING NOTES; LISTENING. Then the verdict per the spec's three
criteria, judged on this file as it is. Skip the 1b board plan and pause plan (a separate
hold/stroke review already covers visuals); do NOT touch any video, lesson, or prompt file.

Write three files in the review dir:
A. <slug>/NARRATION.md — the spec's per-roll block verbatim format, preceded by a 3-6 line
   plain-English summary (verdict, counts, what failed, what would fix it).
B. <slug>/narration-points.csv — one row per item, written with Python's csv module,
   UTF-8, header row exactly:
   lesson,video,kind,n,point,rating,timestamp,spoken_or_note
   kind = teaching point | hard requirement | error | addition | source_qa | editing note
   rating = RICH|TAUGHT|THIN|MISSING|WRONG for teaching points; MET|MISSED for hard
   requirements; blank otherwise. n = order within kind (1..). timestamp as m:ss.ss or a
   range. No newlines inside any cell (join with " / "). Quote what was actually spoken.
C. <slug>/narration-summary.csv — one data row, header exactly:
   lesson,video,candidate,duration,verdict,why,points_total,rich,taught,thin,missing,wrong,hard_met,hard_total,hard_missed,errors,source_qa,additions,repair_feasible,reroll_needs,listening_limits
   (verdict = KEEP|REPAIR|REROLL; why = one or two sentences; hard_missed = the missed lines
   joined by " / " or "none"; repair_feasible = yes/no + one clause; reroll_needs = what a new
   generation must teach, or "n/a"; listening_limits = what could not be verified by ear.)

Report back in under 200 words: verdict, counts, and the file paths. Do not paste the block.
