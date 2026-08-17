# QUEUED EDIT — Finish Smarter opener rewrite (bike analogy)

**Status: approved by David 2026-08-17, NOT YET APPLIED** — another session was mid-flight
in index.html. Apply on David's go-ahead. Delete this file after applying.

## The edit (all in `OpenerSkillsSection` + one CLOSE_BOARDS line)

1. **Illustration card** (the typeset Illustration): lines become
   `Your setup. / Your questions. / Your judgment. / Your Skills.` and the payoff line
   becomes `And you'll always be Smarter Than the Tool.`
   (David chose "Your Skills" over "Your depth" by default — his original suggestion;
   confirm at apply time.)
2. **Delete ALL whyThisMatters text between the illustration and the overview box**
   (the five-sections recap, the pivot, the access/sameness paragraphs, the
   "Here's how it runs." transition). The kept KEEP-THIS-QUESTION beat carries the
   sameness premise.
3. **Replace with** (David-approved wording, polished punctuation):
   > Last section, and it's the one you keep.
   >
   > Think about learning to ride a bike. You outgrew it and moved on to another
   > bike. But you had learned a key skill: balance. Whether you became a serious
   > cyclist or just ride for fun, that skill stayed with you. Nobody could give you
   > balance. You had to build it.
   >
   > This section is about skills like that: the ones you build once and keep
   > forever. Some of them are AI skills. The most important ones aren't. You'll
   > build both here.
   (The one-line orientation opener is a default — David hadn't confirmed; cut the
   first line for a cold open if he prefers.)
4. **KEEP unchanged:** THE COMMON MISTAKE beat, KEEP THIS QUESTION IN MIND beat,
   the overview box (now THREE beat groups after the 2026-08-17 section split).
5. **CLOSE_BOARDS.openerskills** → pill `"The tool is rented."` sticky
   `"The skills are yours to keep."` (David picked option 3.)
6. **Section name: RESOLVED 2026-08-17** — the section split back out as "Build Your
   Skills" (commit e063eca); this opener now fronts that section and the export
   slug is already `Opener-Build`.

## Apply procedure
Standard: edit → node --check → serve + validate() 55 → design-check PASS →
screenshot opener → regenerate the `Opener-Build` export (id `openerskills`) →
commit + push. House rules: no em-dashes, colon setups, curly apostrophes.
