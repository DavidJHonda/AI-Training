# Shipped batch — pushed October 22, 2026

User authorized: “Commit and push all the changes we've shipped.”

All seven approved release commits were already committed locally. Reviewed the outgoing commit list and release diff, fetched origin to confirm no incoming commits, and pushed main successfully from `0e5612d7` to `1a7b15d1bda18adb1a9ab9a0c2754fe3551bd499`. Remote HEAD was verified with git ls-remote; local and origin/main have zero commits of divergence. No additional release commit was necessary. Untracked audit/build records and preparation work remain local.

Included releases:

- Embrace the Future opener v6 — `93b4e4e1`
- Loudest Voices v12 — `3c9d8b0b`
- What is AI? v14 — `375353da`
- Why Learn AI? v11 — `6b72bcd1`
- When You Need More v4 — `256093f3`
- Does School Matter? v12 — `649b2161`
- Your Home Base v9 — `1a7b15d1`

## Deployment status

GitHub reports Vercel pending: “Vercel is deploying your app.” Deployment: https://vercel.com/davidjhonda-5001s-projects/ai-training/4pRaagqB58qgrJLAyr2fUTAycVsC

Last public check at 2026-10-22T22:28:05Z still found the previous lesson references. **Push complete; deployment and production asset verification pending.** No claim that the new videos are live. See deployment-status.json and public-verification.json. Run verify_public.py after deployment completes to compare the production index and all seven served videos plus the updated Loudest Voices board against local hashes.
