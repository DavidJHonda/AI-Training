# Tokens: rolls 1 and 2 against the live video (narration review, 2026-09-22)

**Candidates:** `Prompts/tokens-1.mp4` (5:09.60, 9288 frames) and `Prompts/tokens-2.mp4` (4:06.23, 7387 frames), both rolled on
the 2026-09-21 kit. **Live:** `course-assets/tokens/tokens.mp4` (3:37.60, 6528 frames), v8 shipped 2026-09-16 under the old
method. Grounding: the Tokens section of `index.html`, `lessons/tokens.md`, and the beat spine, verbatim lines and guardrails in
`Prompts/UNDERSTAND-AI-VIDEO-KITS.md`. Full transcripts are beside this file.

## Verdicts

| Roll | Verdict | Why |
|---|---|---|
| **tokens-1** | **KEEP** | All thirteen beats taught, all seven required verbatim lines spoken exactly. Defects are pronunciation, not teaching. |
| tokens-2 | REROLL (not usable as a spine) | "Where the Pieces Come From" is MISSING — the guardrail beat the kit says must come before Send. Six of seven verbatim lines absent; Board 5 counts mostly unspoken; Claude's unpublished vocabulary dropped; the Avengers reply summarized, not read. |
| live v8 | Would not pass today | The Avengers reply is never narrated; Board 5 loses two of its five examples; five of seven verbatim lines absent. Strong on the cat beat and on where the pieces come from. |

## Required verbatim lines

| Line | tokens-1 | tokens-2 | live |
|---|---|---|---|
| "Math is the magic that powers AI." | ✅ 0.00 | ❌ "Artificial intelligence is powered entirely by mathematics" | ❌ "It runs on math." |
| "Instead of giving every word its own number, AI uses reusable pieces of text called tokens." | ✅ 56.70 | ❌ "Instead of whole words, AI uses reusable fragments…" | ❌ "Instead of trying to memorize every possible whole word…" |
| "Reuse the pieces. Build more words." | ✅ 110.20 | ❌ | ❌ |
| "Tokenization turns text into token IDs the model can use." | ✅ 175.60 | ❌ | ❌ |
| "A token ID identifies the token. Meaning comes later." | ✅ 199.80 | ❌ "That token ID acts as an address… calculated later." | ❌ "It is just a catalog number…" |
| "Words become numbers." | ✅ 302.30 | ✅ 235.00 | ✅ 207.12 |
| "That lets AI work with your language using math." | ✅ 303.80 | ❌ "This translation into mathematics is the process that allows AI to comprehend and utilize human language." | ✅ 207.12 |
| **Total** | **7 / 7** | **1 / 7** | **2 / 7** |

## Beat by beat

| # | Beat | tokens-1 | tokens-2 | live v8 |
|---|---|---|---|---|
| 1 | Math powers AI; you ask in words | **RICH** "Math is the magic that powers AI, but you ask AI questions in words, not numbers." (0.00) | TAUGHT "…you aren't typing out equations. You ask questions in plain English." (4.00) | TAUGHT "It runs on math. It only processes numbers." (12.08) |
| 2 | Board 1: the Avengers exchange, reply in full | **RICH** reads the whole reply: "Most people point to Avengers Endgame… Infinity War is the other top pick if you like a darker ending." (21.30–31.40) | THIN "the AI responds with a natural-sounding paragraph about endgame and infinity war" (19.00) | THIN "the AI replies with a detailed answer, just like a person would" (6.08) |
| 3 | One number per word, and why it breaks | **RICH** (34.10–56.70) slang, typos, emojis, code, million-word list | **RICH** (34.00–54.00) same ground | TAUGHT (23.44–39.28) same ground, tighter |
| 4 | Tokens defined; vocabulary; pieces recombine | TAUGHT (56.70–72.80) "reusable pieces of text called tokens… full collection… is called its vocabulary" | TAUGHT (63.00–111.00) plus **RICH** recombination: "the AI can process any word, even a brand new one, by breaking it down into pieces it already recognizes" | **RICH** carries the page's own line: "A token can be a whole word, or it can be just a small fragment of one." (46.08) |
| 5 | Board 2: un / belie / vable; reuse trio; letters after un; banner | **RICH** all of it, incl. "the letters following the prefix un are split into multiple tokens" (86.40) and the banner (110.20) | TAUGHT split + trio (71.00–89.00); no letters-after-un, no banner | THIN split ✓ but only two reuse words ("unusual or unmatchable"), no letters-after-un, no banner |
| 6 | Where the pieces come from (engineers, program, ID as address) — **before Send** | **RICH** (113.10–142.00) engineers choose the split, a program analyses massive text, ID is "an address that identifies the token, but says nothing about its actual meaning" | **MISSING** — jumps from vocabulary sizes straight to "This diagram tracks what happens when you hit send." The address idea surfaces only later, at the cat board. | **RICH** (84.64–125.28) engineers, programs, permanent vocabulary, ID as "an exact address in the AI's vocabulary catalog" |
| 7 | Vocabulary sizes | **RICH** all three: 200,000 / 256,000 / "Anthropic hasn't published [Claude's]" (124.10) | THIN two sizes; Claude omitted | THIN two sizes; Claude omitted |
| 8 | Board 3: the three Send steps by name + IDs + banner | **RICH** "Step one… Step two… In step three…" with all three IDs and the banner (146.10–179.60) | TAUGHT steps unnamed, IDs ✓, no banner (114.00–132.00) | TAUGHT steps unnamed, IDs ✓, no banner (125.28–140.16) |
| 9 | Board 4: the cat; ID 4719; number is not meaning | **RICH** + banner verbatim (183.60–203.70) | TAUGHT (132.00–158.00) | **RICH** (140.88–170.72) the sharpest version: "not a mathematical representation of fur, whiskers, or a small animal" |
| 10 | Bridge: all the text you send gets split | TAUGHT "All the text you send to AI gets split." (203.70) | TAUGHT "Every character you send to an AI is subject to this splitting and numbering process." (158.00) | THIN — cuts straight to "This chart shows how a tokenizer handles everything." (170.72) |
| 11 | Board 5: five examples with pieces **and counts**; SP is a label; space joins the piece after it | **RICH** all five with counts; SP explained: "SP marks a leading space… spaces attach[] to the chunk that follows them, resulting in 3 tokens total" (216.30–270.30) | TAUGHT ex 1–5 present (splits correct, incl. "Chat, G, and PT"), but only ex 1 and ex 5 carry counts; SP described without the 3-token total | THIN only three of five examples (ChatGPT, I ♥ AI, the web address); unbelievable and basketball missing; no SP label |
| 12 | The return trip | **RICH** (285.80–300.10) | **RICH** (217.00–235.00) | **RICH** (190.88–207.12) |
| 13 | Close: the two lines | **RICH** both verbatim | THIN first line only | **RICH** both verbatim |

**Missing in all three:** "The model uses those same tokens and IDs during training and when you chat" (page and Markdown, "Where the
Pieces Come From"). No roll supplies a donor. It is peripheral to understanding tokenization, so it does not block a KEEP, but the
next prompt should require it.

## Recommendation

**Ship tokens-1 as the spine. No graft is needed for completeness** — it is the only roll that teaches every beat and speaks every
required line. Two optional donors, David's call, both cross-generation (voice match unverified, so each would need a listen before
it went in):

1. **live 46.08–52.08** — "A token can be a whole word, or it can be just a small fragment of one." The page's own sentence, which
   roll 1 never says. It would sit under Board 2's opening.
2. **live 152.48–165.28** — the sharper ending of the cat beat. Roll 1's version is adequate; this is polish, not repair.

## David's decisions (2026-09-22)

- **"Anthropic hasn't published Claude's" is fine on listening.** The transcript's "Clods" is a whisper artifact of the spoken
  word, not a mispronunciation to repair. No edit.
- **Neither optional donor is wanted** ("I don't think we need those. It works fine without."). tokens-1 ships on its own
  narration, whole, with no graft from the live video.

So the narration is final: **tokens-1, uncut, ungrafted.**

## Editing notes (tokens-1)

- **Pronunciation, two remaining.** "Claw 100K base" for `cl100k_base` (159.46) and "the Witten word cat" for "written"
  (190.74). Neither changes the teaching; both accepted.
- **"str" and "aining" are read as one word, "straining"** (261.10–270.30), which slightly undercuts the eight-token count. The
  count is stated correctly.
- Roll 1 reads the URL's **token pieces**, not the address itself — that follows `lessons/tokens.md` line 121 and does not breach
  the kit's "never speaks the URL" guardrail.
- Runtime 5:09 against the live 3:37; the pill would go 4 min → 5 min if it ships as is.
- Frame 0 is the blank paper card with the Gemini Notebook corner mark (standard, cleaned at render). No stock-photo watermark
  seen in the frames sampled.

## Materials notes

- The kit's beat 6 guardrail ("teach where the pieces come from before describing what happens at Send") is exactly what roll 2
  dropped. Worth restating as a prompt negative before the next Tokens roll.
- Board 5's counts are what separates roll 1 from roll 2. The Markdown states each count in its own sentence; the prompt should
  name "that is N tokens" as required wording if another roll is needed.
