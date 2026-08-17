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
- Parallel-card hierarchy: marker, title, supporting text, then illustration. Keep
  every marker and title block on shared horizontal guides so all labels can be read
  in one pass. Reserve a fixed lower art zone; illustration shape or density must
  never move the title or copy. Use a number only when order matters, a letter when
  it explains a term, and an icon for an unnumbered stage.
- Takeaway component: mandatory on every board, full width inside the 80 px margins,
  84 px tall with 16 px corners and warm gold `#ffe9ab`. Leave 40 px above it and
  40 px below it. Use navy text at 32 px and weight 600 plus
  the same 52 px purple check-circle mark. Treat the check and sentence as one
  centered lockup with a 16 px gap; do not center the sentence independently or
  strand the check at the left edge. Do not use a border or gradient, and do not
  substitute scales, speakers, sparkles, or another decoration in this slot.
- Readability: generous margins and no body copy that depends on zooming.
- Constraints: drawn/vector-like visuals only; no photography, logos, watermarks,
  recognizable people, decorative b-roll, or extra text.
- Purpose: the exact same board must work on the lesson page and in the existing
  narration window.

## Board-specific specifications

1. **Why Learn AI:** three numbered columns — “THIS IS YOUR TIME,” “YOU’LL MOVE
   FASTER,” and “NOTHING TO UNLEARN.” Supporting lines: “Nobody has a twenty-year
   head start,” “What took a decade is within reach now,” and “You’re learning the
   new workflow first.” Place the three existing illustrations beneath the aligned
   copy. Takeaway: “This is your time to learn the new workflow.”
2. **Does AI Think:** symbols-in → giant rulebook shape match → likely reply-out,
   ending “Fluent answer. No understanding required.”
3. **What You Can Control:** paired “OUT OF YOUR HANDS” and “IN YOUR HANDS” lists
   organized around volume and leverage controls. Use the course navy (`#08072b`)
   for the “OUT OF YOUR HANDS” header rather than charcoal. Takeaway: “The left
   side is loud. The right side is leverage.”
4. **Does School Matter:** “Same AI. Different value.” as a left-to-right flow from
   Ask the Right Question → AI Answer → Make the Answer Better. Use three equal
   circular markers labeled “SKILL 1,” “AI,” and “SKILL 2”; AI is the bridge, not a
   numbered third skill. Align all three title and supporting-text blocks above the
   illustrations. End “The tool brings answers. You bring judgment.”
5. **Learn With AI:** decision split from “Do you want to learn from your materials—or
   learn something new?” to Source-Grounded Tutor and General Tutor, each with a
   concise best use and catch. Takeaway: “Match the tutor to its knowledge source.”
6. **Where AI Works Best:** four equal cards — Transform, Generate, Compress,
   Reason — with one reinforcing icon and concise use examples per card. Takeaway:
   “Match the job to one of AI’s four strengths.”
7. **Questions Matter:** three-era timeline — Library / Search / AI — with “Half a
   Saturday,” “An hour or two,” and “Seconds.” Takeaway: “The cost of finding an
   answer collapsed.”
8. **Context Window:** glowing central visibility boundary with current prompt,
   earlier messages, and added files inside; older chats, unsent pages, computer files,
   and other apps outside. Takeaway: “If it isn’t in the window, the model can’t see
   it.”
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
    stage title, a two-line description, and a distinct supporting illustration:
    productive AI use; an open-hood view of AI; catching a misleading answer;
    facing a changing future; and building practical capability. Do not add a
    sixth “Finish” stage. Takeaway: “Start with the tool. Finish with what you can
    do.”
