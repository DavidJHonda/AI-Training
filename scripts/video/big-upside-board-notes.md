# Big Upside example boards

Updated 2026-09-24. These notes are production references, not video narration or student-facing text.

## Current boards

- `course-assets/big-upside/big-upside-scientific-discovery.jpg`: Helping People Stay Healthy. Finding Cancer, Urgent Scans, New Antibiotics.
- `course-assets/big-upside/big-upside-practical-help.jpg`: Helping People in Everyday Life. Reading Aloud, Flood Warnings, Targeted Spraying.

Both use the existing three-card Editorial Explainer renderer with unchanged title, card-heading, and body font sizes. Canonical filenames are retained. Four existing illustration panels were reused; two new panels were generated with the built-in image tool and composed into the final boards. The renderer can recover all six panels from those canonical JPGs, so no separate source-art copies are needed in the course assets.

## Supporting sources

- Cancer screening: https://www.lu.se/artikel/ai-stodd-screening-brostcancer-nya-resultat-tyder-pa-annu-hogre-traffsakerhet
- Brain-bleed scan triage: https://www.accessdata.fda.gov/cdrh_docs/pdf21/K211179.pdf (flags suspected findings for clinical review; does not replace standard interpretation).
- Antibiotic laboratory research: https://news.mit.edu/index.php/2023/using-ai-scientists-combat-drug-resistant-infections-0525
- Reading text and describing images: https://www.bemyeyes.com/bme-ai/
- Flood warnings: https://sites.research.google/floodforecasting/?web=1
- Targeted spraying: https://www.deere.com/en-us/our-company/technology-and-innovation/sense-and-act

## Image generation prompts

### Urgent scans

Use case: scientific-educational. Create a text-free wide 16:9 illustration for a high-school AI course card about flagging urgent scans. Polished softly lit 3D educational illustration in cobalt blue and pale blue, simple readable composition. A radiology monitor displays a conceptual axial brain CT scan; a restrained amber outline highlights one small suspected abnormal area, with an amber notification icon beside the screen. The image communicates a scan flagged for a doctor's review, not a diagnosis. No human figures, blood, gore, words, letters, numbers, branding or decorative tiny text. Clear centered subject, generous crop-safe margins. This is an explanatory illustration, not an actual medical scan.

### Targeted spraying

Use case: scientific-educational. Create a text-free wide 16:9 illustration for a high-school AI course card about targeted weed spraying. Polished softly lit 3D educational illustration in teal, green and pale aqua, simple readable composition. Close low oblique view of a compact section of agricultural spray boom with a small camera moving above orderly healthy crop plants; one nozzle emits a narrow mist only at a clearly different weed between the rows, other nozzles stay off and crops are not being sprayed. Strong visual distinction between neat crop rows and isolated weed. No people, words, letters, numbers, logos or labels. Clear centered action, generous crop-safe margins. Positive natural daylight.

