# Embrace Editorial Board Review

These eight boards began as isolated review builds. **Even the Experts Don’t
Know** has now been approved and copied byte-identically to the Loudest Voices
on-page lesson and video-prep materials. The other seven remain review-only.

The boards use the canonical renderers and current specifications for:

- Editorial Explainer: Two-Card Full-Bleed (`EE-2FB`)
- Editorial Explainer: Three-Card Full-Bleed (`EE-3FB`)
- Editorial Explainer: Four-Card Full-Bleed (`EE-4FB`)
- Editorial Explainer: Flow (`EE-FLOW`)

## Review files

- `very-different-bets.jpg` (`Even the Experts Don’t Know` review board)
- `this-has-happened-before.jpg`
- `a-jailbreak.jpg`
- `the-test-that-reached-the-internet.jpg`
- `gps-versus-self-driving.jpg`
- `chatbot-versus-agent.jpg`
- `your-first-assignment.jpg`
- `four-famous-plans.jpg`

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
  infrastructure; an experimental flying car waiting on a test platform.
- **A Jailbreak:** defenders protecting many routes; one narrow route passing
  through a single opening.
- **The Test That Reached the Internet:** controlled sandbox; discovered opening;
  connection to the wider network; access to external computer systems.
- **GPS versus Self-Driving Car:** route guidance with manual controls; autonomous
  navigation and rerouting.
- **Ask a Chatbot versus Hire an Agent:** manual basketball-video editing with one
  caption contribution; an automated select-edit-caption-schedule-publish workflow.
- **Your First Assignment:** customer-review busy work; automated organization
  leaving investigation, questions, and judgment.
- **Four Famous Plans:** text messaging becoming mass communication; military GPS
  becoming civilian navigation; cane toads spreading instead of eating the target
  beetles; added highway lanes producing more congestion.
