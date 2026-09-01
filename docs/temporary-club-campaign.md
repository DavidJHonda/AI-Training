# Temporary AI Club entry page

## Preservation baseline

The original first-visit page is preserved by the annotated Git tag:

`pre-club-campaign-2026-09-01`

The tag points to commit `43c521226ef98a298259204cc0f566a33375fc88`.
It captures the complete course—not only the visible entry-page markup—so the
original styles, scripts, images, and behavior can be recovered together.

## Campaign window

The temporary entry treatment is active from September 1, 2026 through
September 10, 2026 in Central Daylight Time. At midnight on September 11, the
original entry page becomes the automatic fallback again.

The campaign dates live in the `CLUB_CAMPAIGN` object near the top of
`index.html`.

## Preview controls

- `?clubPromo=preview` forces the temporary entry treatment on.
- `?clubPromo=off` forces the original entry page on.

These overrides only change which first-visit treatment is displayed. They do
not change course progress or enrollment behavior.

## Restoration

The original page remains in `index.html` as the non-campaign branch, so no
manual restoration is required when the campaign expires.

To inspect the exact pre-campaign file later:

`git show pre-club-campaign-2026-09-01:index.html`

After the campaign, revert the single campaign commit to remove the dormant
campaign code and its logo asset from the repository. Do not reset the branch
or overwrite unrelated work.
