# Image-Generation Prompt Set

The initial illustrations were generated with the built-in image-generation
workflow. Final component geometry and typography are applied deterministically by
`scripts/video/normalize_alternative_board_titles.sh`, preserving the approved art
while making every board conform to this specification.

## Common specification

- Use case: educational infographic diagram.
- Canvas: 16:9 landscape; exported as 1600×900 JPEG.
- Canvas: one flat pale-lavender field (`#eeeaff`) across the complete frame.
- Body container: one white panel at x=80, y=172, 1440×564 px, with 16 px corners.
  The entire body composition lives inside this panel. Interior columns and cards
  are allowed, but no artwork bleeds outside it and no irregular lavender slivers
  separate body elements.
- Design: white cards, bold dark-navy typography, purple primary accent with
  restrained blue, orange, and teal.
- Board title: exactly 44 px, weight 800, dark navy, sentence case, and centered.
  Never reduce the title size to make a line fit; wrap it to a second line instead.
- Vertical stack: 40 px top margin, 100 px title block, 32 px gap, 564 px body
  zone, 40 px gap, 84 px takeaway band, and 40 px bottom margin. These values total
  exactly 900 px and do not vary by board.
- Title zone: use the same uninterrupted lavender field as the board background,
  with no separate band, rule, divider, or visible seam. Center the complete title
  group optically and vertically within the fixed 100 px block, with at least 80 px
  side margins. The block supports a one-line title, a one-line title plus subline,
  or a two-line title without a subline. Rewrite a title/subline combination that
  would exceed the block; never shrink the 44 px title.
- Optional subline: 26 px, weight 500, muted purple-grey, centered, and 10 px below
  the title.
- Body zone: always 564 px tall. Scale the complete body composition proportionally
  inside the zone; the zone itself never grows to accommodate a dense board.
- Interior hierarchy: card headings may be no larger than 28 px. Supporting copy is
  normally 24–26 px so the board title is always the strongest text on the canvas.
- Supporting copy uses the course’s regular body-text ink (`#0e0a1f`). Do not use
  muted grey for small explanatory text; reserve muted color for optional sublines,
  inactive progress labels, and other genuinely secondary interface information.
- Parallel-card hierarchy: marker, title, supporting text, then illustration. Keep
  every marker and title block on shared horizontal guides so all labels can be read
  in one pass. Reserve a fixed lower art zone; illustration shape or density must
  never move the title or copy. Use a number only when order matters, a letter when
  it explains a term, and an icon for an unnumbered stage.
- Step-marker alignment: center every numeral or short marker label on both axes
  inside its circle, using the glyph’s rendered bounds rather than a fixed baseline.
  Do not stack a category word above a numeral inside the circle; the marker itself
  contains only the centered numeral or short label.
- Wrapped step headings: every peer step uses the same fixed title slot. Treat a
  two-line heading as one text block and center that complete block horizontally and
  vertically inside the slot. Center a one-line heading vertically in that same
  slot; never align it to the first line of its two-line neighbors.
- Takeaway component: mandatory on every board, full width inside the 80 px margins,
  84 px tall with 16 px corners and warm gold `#ffe9ab`. Leave 40 px above it and
  40 px below it. Use navy text at 32 px and weight 600 plus
  the same 52 px purple check-circle mark. Treat the check and sentence as one
  centered lockup with a 16 px gap; do not center the sentence independently or
  strand the check at the left edge. Do not use a border or gradient, and do not
  substitute scales, speakers, sparkles, or another decoration in this slot.
- Readability: generous margins and no body copy that depends on zooming.
- Constraints: drawn/vector-like visuals only; no photography, public figures,
  logos, watermarks, decorative b-roll, or extra text. Recurring course hosts may
  appear only when a board-specific specification calls for them.
- Purpose: the exact same board must work on the lesson page and in the existing
  narration window.

## Opener section-map component

- Use the common 1600×900 canvas, title zone, body panel, and takeaway band above.
- Set the section name as the 44 px title and “In this section” as the 26 px
  subline.
- Present the section sequence as stacked full-width rows joined by one subtle
  vertical route. Each row uses a centered 64 px number circle, a 28 px heading,
  and 24 px supporting copy. Do not convert the map into narrow columns.
- Three-step maps use three 160 px rows. The four-step Understand AI map uses four
  122 px rows. Row height changes; type sizes and the 564 px body zone do not.
- Preserve equal visual weight for every step. In particular, the fourth Understand
  AI step must not be compressed or treated as an afterthought.
- Use a section-specific gold takeaway that resolves the purpose of the map without
  repeating the opener’s separate closing board verbatim.
- In video, keep the complete map visible and emphasize one row at a time as its
  narration is spoken.

## Board-specific specifications

1. **Why Learn AI:** title “Why you’ll thrive in the AI future” with subline “AI is
   new for everyone. This is your big advantage.” Use three numbered columns —
   “THIS IS YOUR TIME,” “YOU’LL MOVE FASTER,” and “NOTHING TO UNLEARN.” Each column
   carries a compact explanation of the advantage, not just a caption: nobody has a
   twenty-year head start; AI collapses the old career runway; and new learners do
   not have an old workflow to undo. Reduce the three existing illustrations enough
   to keep all explanations readable, then place them beneath the aligned copy.
   Takeaway: “This is your time to learn the new workflow.”
2. **Does AI Think:** symbols-in → giant rulebook shape match → likely reply-out,
   ending “Fluent answer. No understanding required.”
3. **What You Can Control:** paired “OUT OF YOUR HANDS” and “IN YOUR HANDS” lists
   organized around volume and leverage controls. Use the course navy (`#08072b`)
   for the “OUT OF YOUR HANDS” header rather than charcoal. Takeaway: “The left
   side is loud. The right side is leverage.”
4. **Does School Matter:** “Same AI. Different value.” as a left-to-right flow from
   Ask the Right Question → AI Answer → Make the Answer Better. Use three equal
   circular markers labeled “1,” “AI,” and “2”; AI is the bridge, not a numbered
   third skill. Give each stage enough supporting copy to carry the lesson without
   a second text box: knowledge sharpens the question; similar questions produce
   similar answers; and the learner must judge, challenge, and improve the result.
   Align all three title and supporting-text blocks above smaller illustrations.
   End “The tool brings answers. You bring judgment.”
5. **Learn With AI:** decision split from “Do you want to learn from your materials or
   learn something new?” to Source-Grounded Tutor and General Tutor, each with a
   concise best use and catch. Takeaway: “Match the tutor to its knowledge source.”
6. **Where AI Works Best:** use four separate boards so the complete lesson context
   remains readable on the page and in the video. Each board uses the shared title,
   subline, white body panel, and gold takeaway system. Split the body into a large
   reinforcing illustration on the left and, on the right, the full “What it does”
   explanation plus all four examples. The sequence is Patterned Transformation,
   Generative Variation, Semantic Compression and Retrieval, then Structured
   Reasoning and Synthesis. These four boards replace the visible programmatic
   four-strength box on the lesson page and the four older video boards one-for-one.
7. **Questions Matter:** three-era timeline — Library / Search / AI. Each column
   includes three narration-matched process steps, followed by “Half a Saturday,”
   “An hour or two,” or “Seconds,” then a smaller supporting illustration. Takeaway:
   “The cost of finding an answer collapsed.” The board replaces the visible
   programmatic timeline box on the lesson page.
8. **Context Window:** glowing central visibility boundary with current prompt,
   earlier messages, and added files inside; older chats, unsent pages, computer files,
   and other apps outside. Takeaway: “If it isn’t in the window, the model can’t see
   it.” The board replaces the visible four-card “Outside the window” box on the
   lesson page; preserve that box’s complete explanations as accessible text.
9. **Training:** four-stage map — Setup, Pretraining, Instruction Tuning, Preference
   Tuning — plus the Guess → Check → Nudge → Again loop. Takeaway: “Training is
   guess, check, nudge, repeat.”
10. **Embeddings:** Coke, Pepsi, and Coffee profiles across seven labeled dimensions;
   the first six match for Coke and Pepsi, while Citrus 1 versus 10 separates them.
   Takeaway: “One new dimension separates the meanings.”
11. **Layers:** repeated translucent layers containing Attention (“Which words
   matter?”) and Transformation (“Update the meaning.”), from vector-in to richer
   vector-out. Takeaway: “Same two moves. Dozens of passes.”
12. **Hallucination:** Training and Generation converge on the central distinction
    “PROBABLE ≠ TRUE.” Takeaway: “A likely sentence can still be false.”
13. **Training Bias:** Defaults, Blind Spots, and Wrong Patterns emerge from the shape
    of the training data; the wrong-pattern icon uses the cow/grass example.
    Takeaway: “The model repeats the shape of its data.”
14. **Document Trap:** Chunk → Embed → Retrieve pipeline, ending “It answers from
    what it retrieved—not from the whole document.” Use the same sentence in the
    takeaway band.
15. **What Is AI — LLM:** title “What’s an LLM?” with subline “The engine under the
    app.” Use one white body panel divided into three equal columns with subtle
    vertical rules. Each column follows letter badge, centered heading, centered
    description, divider, then illustration, all on shared horizontal guides.
    Large shows books, web pages, and code flowing into a large organized data stack;
    Language shows speech, reading, writing, summarizing, translation, and
    explanation; Model shows an input moving through a learned-pattern engine to a
    likely output. Takeaway: “ChatGPT is the app. The LLM is the engine.”
16. **Welcome — Course Arc:** title “Here’s your path.” Show one continuous route
    through five equal stages: Work, Understand, Avoid, Embrace, and Build. Use
    numbered purple markers connected by one line. Under each marker, align the
    stage title, a two-line description, and a distinct supporting illustration.
    Use simplified editorial versions of recurring hosts Luke (light-brown curls,
    green hockey jersey 4) and Nate (dark curls, green hockey jersey 96): Luke uses
    AI productively; Nate looks under the hood; Luke catches a misleading answer;
    Nate faces the changing future; and both build practical capability together.
    The green/black/white uniforms establish course personality but carry no exact
    team or league marks. Do not add a sixth “Finish” stage. Takeaway: “Start with
    the tool. Finish with what you can do.”
17. **AI Is Different — Kryptonite:** title “You’ll see stories like this.” Use one
    white body panel divided into three equal columns: Scams That Scale, Deepfakes
    of Real People, and Confident but Wrong. Each unnumbered column follows icon,
    title, complete existing description, divider, then supporting illustration.
    Use flat course-native schematic line art: a message and identity card
    multiplying into copies; a duplicated portrait with scan line and pixel
    distortion; and an answer card with a warning triangle and stethoscope. No
    gradients, expressive characters, robots, simulated UI text, or tiny detail.
    Takeaway: “Trained behavior is harder to predict, inspect, and lock down.” The
    board replaces the visible three-card stories box on the lesson page and video
    board 3 one-for-one.
18. **Evaluate the Results — process family:** build four coordinated boards titled
    “Run the quick pass,” “Decide whether to dig,” “Dig deeper when it matters,”
    and “Make your move.” Every board uses the common frame plus the same four-step
    Quick Pass → Decide → Dig → Move progress rail at the top of the white body
    panel, with the current stage filled purple. Earlier stages use purple outlines;
    later stages remain muted. Boards 1, 2, and 4 use three aligned cards. Board 3
    uses a centered three-over-two grid for its five tactics. Use numbers only for
    ordered checks and flat line icons for tactics or outcomes. Takeaways:
    “Read it. Understand it. Validate what you can.” “Unknown facts or real stakes
    mean keep going.” “Check the claim outside the answer.” “Use it, fix it, or
    choose a better path.” The four boards replace the first four instructional
    boxes one-for-one if selected; do not combine them into one dense workflow board.
