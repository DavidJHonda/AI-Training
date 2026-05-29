# Parking Lot — cut-but-keepable lesson content

Content removed from a lesson but worth reusing later. Each entry: what it is, where it came from, the verbatim source, and where it might go.

---

## "The Scale of What's Happening" — billions-of-calculations SEE IT

- **Origin:** AI Answers → Inference lesson (`InferenceSection`), removed 2026-05-29 during the source-first reorder to keep the merged Inference lesson from getting dense.
- **Possible destination:** back into Inference, or a future "why it feels instant / cost of inference" lesson.
- **Supporting state it needs if restored:** the `computePhase`, `computeQChars`, `computeAiWords`, `computeReveal` (useState) hooks + the compute `useEffect`, plus the `computeQuestion` / `computeAnswer` string vars and `computeAnswerWords` (= `computeAnswer.split(" ")`). Also depends on the shared `ThinkingBubble` component — still defined in `index.html`, currently unused elsewhere; kept available for this restoration, so do not delete it.
- **Full source:** in git history at the commit before this one, inside the `InferenceSection` function. Note the pieces sit in two different regions of that component: the state hooks/vars above are declared near the top of `InferenceSection` (~120 lines above the JSX), while the JSX block lives lower down. Searching the pre-removal `index.html` for the string `Why it feels instant` finds only the JSX — a restorer must recover BOTH regions, not just that anchor. The JSX block is the complete unit: SectionKicker "The Scale of What's Happening" + the "Why it feels instant" InteractiveBox with its ThinkingBubble/AIBubble compute animation, the reveal button, the stats grid [Tokens ~14, Dimensions thousands, Layers ~100, "every token checks its relationship to every other token"], the "≈ 100,000,000,000+ calculations" figure, the "over 3,000 years" line, and the KeyInsight "Billions of calculations, all for one word.".
