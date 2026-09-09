# Tokens: two raw video versions

Reviewed September 9, 2026. Recommendation: **reroll both; version 1 is the stronger fallback.**

This is a narration-first intake evaluation, not a finished-video shipping grade. No source, prompt, lesson, or live video was changed.

## Decision

Version 1 (3:27) gives the more usable account of reusable pieces and token IDs. Version 2 (3:58) has a better opening grounded in the Avengers exchange, but introduces more misleading explanations. Neither covers two essential lesson beats in narration: how the vocabulary is built during setup, and how reply IDs become readable text. A combined edit cannot recover narration that neither recording contains. Given the preference to reroll rather than manufacture missing narration, neither is a good repair candidate.

The problem is not that every sentence of the lesson must be read. These omissions leave the core process incomplete. Current boards and Notebook graphics could repair visual errors, but cannot supply the missing spoken explanation.

## Coverage

| Teaching point | Version 1 | Version 2 |
|---|---|---|
| We communicate in words; AI uses numbers | Clear opening; Avengers example near end | Strong Avengers opening |
| Why a fixed whole-word dictionary cannot cover new words, names, typos, and code | Replaced mainly by an efficiency explanation; irregular inputs mentioned later | Essentially omitted |
| Reusable pieces, including whole words or parts | Good subword/reuse explanation; whole-word flexibility not made clear | Good reuse example, undermined by saying entire words are rarely tokens |
| Setup: build vocabulary from text, assign IDs, reuse same tokens/IDs in training and chat | Missing | Missing; mentions a fixed library near the end without explaining its origin |
| Type text → split into tokens → look up IDs | Covered, late in video | Covered, with typing established in opening |
| Token ID identifies the token, not meaning | Strong | Strong |
| Spaces, names, and URLs | Examples covered; leading-space explanation wrong | Examples covered; explicitly misinterprets SP notation |
| Reply IDs decoded back into text | Missing | Missing |
| Exact approved two-line closing | Missing | Missing |

Neither includes the lesson's approximate vocabulary-size examples. That is secondary to setup and decoding and is not the main reason for rerolling.

## Version 1: strongest passages and repairs

- **0:37–1:05:** useful explanation of `un`, `belie`, and `vable`, followed by reuse of `un`. The narration supports the building-block concept.
- **1:24–1:43:** clear distinction between `cat` and ID 4719. This teaches the right concept without asking students to interpret the ID as meaning.
- **2:38–2:57:** usable text → pieces → IDs explanation. Its placement after the detailed examples makes the progression less direct, but reordering alone is not a reason to reject the roll.
- **0:27–0:37 and 1:06–1:15:** whole-word vocabulary framed primarily as a processing-power problem. Vocabulary size does affect efficiency, but “radically reduces processing power” is an overstatement without a defined comparison. It displaces the more accessible lesson point: reusable pieces cover new inputs. Generated graphics add unsupported load and compute statistics, including a 90%+ FLOP reduction.
- **2:12–2:18:** says an empty leading space or heart emoji gets its own distinct ID. In the actual displayed example, the space and heart are one token; the next space and AI are another. This requires a narration correction, not just a replacement graphic.
- **2:30–2:38:** “every keystroke” mapped into an ID encourages the wrong one-keystroke/one-ID interpretation. IDs belong to chunks of text.
- **1:43–1:50:** the detour into deep understanding and a vast neural network can be cut; the next lesson handles meaning.
- **2:19–2:24:** optional pause-and-guess exercise can be cut. Its generated URL does not match the following course example.

Additional visual repairs if reused: the generated `unusual` breakdown around 1:04 does not match cl100k_base; the efficiency comparison around 1:13 introduces terminology and statistics absent from the lesson. Preserve accurate Notebook graphics elsewhere rather than replacing every scene with a board.

## Version 2: strongest passages and repairs

- **0:00–0:19:** the Avengers exchange gives the lesson a concrete, conversational opening. Retain this approach in the next roll, but avoid “cannot process English letters, grammar, or vocabulary.” The model processes language through numerical representations.
- **0:35–1:03:** good token-ID-versus-meaning explanation.
- **1:39–1:57:** useful building-block/reuse explanation.
- **1:04–1:12:** says every incoming word maps to one label. This contradicts the multi-token words taught afterward.
- **1:33–1:38:** “rarely treats entire words as single tokens” is unjustified. A token can be a whole word or part of one; common whole words can be tokens.
- **2:08–2:17:** says the tokenizer ignores human rules for spaces/punctuation and always finds the most mathematically efficient pieces. The actual tokenizer uses rules involving whitespace and punctuation; a globally most-efficient segmentation is not guaranteed.
- **2:40–2:54:** says the system assigns explicit token markers labeled SP to track leading spaces. **SP is only the course board's notation for a space.** The tokenizer does not insert the letters SP. The accompanying claim about giving everything the same weight is unsupported.
- **3:07–3:19:** “strict correlation” between word complexity and token count is too strong. Familiarity and token count have relationships, but the five examples do not establish a universal rule.

Confirmed visual errors: at 2:17, the generated pipeline labels `Un`, `believ`, `able` with IDs that actually decode to `un`, `belie`, `vable`, and omits the space in its reconstructed sequence. At 3:19, a completed generated graphic labels the course URL as nine tokens with invented IDs, after the narration correctly says eight. Adjacent frames were checked so this is not a partial-animation objection. These visuals are repairable; the missing and incorrect narration remains the decisive issue.

## What the next roll needs to teach

1. Start with the short words-in/words-out exchange.
2. Explain why giving every whole word an ID fails as people invent new words and type names, typos, symbols, and code.
3. Define reusable tokens as whole words or pieces, and show the `un` example.
4. Explain vocabulary setup before use, then distinguish that from splitting a new message at chat time.
5. Explain that an ID identifies a token and does not contain its meaning.
6. Use the verified table. Say a token can include a leading space; do not speak SP as a tokenizer operation.
7. Close the loop: reply IDs become text again.
8. End with the approved close: “Words become numbers. That lets AI work with your language using math.”

Keep engineering/compute claims out of this introductory explanation. No new visuals are required to make these points narratable.

## Evidence and scope

Both complete videos were transcribed with base.en and independently with small.en. Both full transcripts were read. All ten contact sheets were inspected, followed by targeted full-size frames and adjacent-frame checks. Current lesson text and current board assets were compared with the rolls. Timing is approximate and refers to the original uploads, not an edited timeline. No claim of a complete real-time listening pass or finished-video audio QA is made. An ambiguous ASR phrase near version 1's 2:00 mark is not treated as a confirmed pronunciation defect.

The actual cl100k_base examples were checked with tiktoken; results are saved in `token-verification.json`. In particular, `I ♥ AI` gives three tokens: `I`, ` ♥`, ` AI`; the course URL gives eight. Input metadata/hashes are in `sources.json`; full transcripts, scene inventories, contact sheets, and targeted frames are retained alongside this report.

Technical references: [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary) explains subwords, vocabulary training, and decoding. [OpenAI's tokenizer definitions](https://github.com/openai/tiktoken/blob/main/tiktoken_ext/openai_public.py) establish that whitespace and punctuation are part of actual tokenization rules. These checks support the concrete corrections above; they are not reasons to add technical caveats throughout the student lesson.
