# Embrace Editorial Board Review

These eight boards began as isolated review builds. Seven are approved and copied
byte-identically to their on-page lessons and video-prep materials. **The Test That
Reached the Internet** was reviewed and declined because it did not tell the story
as well as the existing lesson. No boards in this review set remain undecided.

The boards use the canonical renderers and current specifications for:

- Editorial Explainer: Two-Card Full-Bleed (`EE-2FB`)
- Editorial Explainer: Three-Card Full-Bleed (`EE-3FB`)
- Editorial Explainer: Four-Card Full-Bleed (`EE-4FB`)
- Editorial Explainer: Flow (`EE-FLOW`)

## Review files

- `very-different-bets.jpg` (`Even the Experts Don’t Know` review board)
- `this-has-happened-before.jpg`
- `a-jailbreak.jpg` (`Why Jailbreaks Keep Appearing` full-bleed feature treatment)
- `the-test-that-reached-the-internet.jpg` (declined; archive only)
- `gps-versus-self-driving.jpg` (`A Chatbot Answers. An Agent Acts.` full-bleed feature treatment)
- `chatbot-versus-agent.jpg` (extended two-card Long treatment)
- `your-first-assignment.jpg`
- `four-famous-plans.jpg`

The seven pending boards store their accent assignments explicitly. Those tokens
follow each source illustration's dominant hue rather than the card's position.
Repeated accents are allowed when peer illustrations intentionally share a hue;
labels and artwork must still distinguish the cards without relying on color.

Source-art sheets live under `assets/`. The deterministic layout and copy live in
`scripts/video/render_embrace_editorial_review.py`.

## Image-generation prompt set

All sheets used the built-in ImageGen tool and this shared direction:

> Create a seamless contact sheet of premium soft 3D editorial illustrations for
> an AI literacy course. Use polished rounded geometric forms, gentle depth,
> subtle studio shadows, consistent subject scale, and pale gradient backgrounds.
> Every panel must crop cleanly to 16:9. Keep the tone calm, contemporary, and
> serious rather than playful. Do not include people, hands, faces, robots, logos,
> letters, words, numbers, captions, borders, labels, or watermarks.

Board-specific subjects:

- **Even the Experts Don’t Know:** accelerating science and medicine; unexpected goals
  moving beyond a warning boundary; a maze ending in a question-shaped gap. This
  board uses a vertically extended three-card treatment to preserve each person’s
  background plus the original `SAYS` and `BUT ADMITS` quotations.
- **This Has Happened Before:** online shopping becoming everyday commerce; one
  smartphone expanding into an ecosystem; a fragile network becoming resilient
  infrastructure; an experimental flying car waiting on a test platform. Each card
  includes a short credential label for the person making the prediction.
- **Why Jailbreaks Keep Appearing:** preserves the existing fortress illustration
  and its opposing defender/attacker signs, then adds the standard board title and
  takeaway banner. This intentionally replaces the proposed two-card treatment so
  the lesson retains visual variety.
- **The Test That Reached the Internet:** controlled sandbox; discovered opening;
  connection to the wider network; access beyond the intended test systems.
- **A Chatbot Answers. An Agent Acts.:** preserves the existing Nate-and-Luke split
  driving scene. The attached teaching strip maps GPS directly to ChatGPT and the
  self-driving car directly to an agent, without a separate takeaway banner.
- **Ask a Chatbot versus Hire an Agent:** approved and installed as an extended
  two-card Long treatment. A shared basketball-highlight assignment establishes the context, and aligned
  `YOU DO`, `AI DOES`, `THE AGENT DOES`, `YOU STILL OWN`, and `WHAT CHANGES`
  sections preserve the full sequence and responsibility boundary without a banner.
- **Your First Assignment:** approved and installed as an extended two-card Long treatment that preserves
  the original Nate-and-Luke teaching illustration. A full-width assignment setup
  leads into aligned first-pass, human-work, and result sections for the old and
  AI-assisted versions of the job.
- **The Biggest Results Were Never the Plan:** approved and installed as an expanded Four-Card treatment
  without pills or a takeaway banner. Each card now explains both the intended use
  and the larger result for text messaging, GPS, cane toads, and Houston’s widened
  Katy Freeway.
