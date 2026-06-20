# Favicon handoff — AI Leadership Society

The browser-tab mark is the "Ai" logo (no "Leadership Society" wordmark),
on a white rounded square so it stays legible on light AND dark browser themes.

## Files (in /icons)
- favicon-16x16.png
- favicon-32x32.png
- favicon-48x48.png
- apple-touch-icon.png   (180×180, for iOS home screen)
- icon-192.png           (PWA / Android)
- icon-512.png           (PWA / Android)
- site.webmanifest

Source master: favicon-white-512.png (also favicon-navy-512.png and
favicon-transparent-512.png exist if we ever want to switch treatment).

## What to do
1. Copy the /icons folder to the site's web root (so paths resolve at /icons/...).
2. Add this to <head>:

```html
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/icons/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
<link rel="manifest" href="/icons/site.webmanifest">
<meta name="theme-color" content="#15315a">
```

3. (Optional) Generate a multi-resolution /favicon.ico (16+32+48) for legacy
   browsers and place it at the web root — most modern browsers don't need it
   since the PNG <link> tags above cover them.

Note: hard-refresh / clear cache to see the new tab icon — favicons cache aggressively.
