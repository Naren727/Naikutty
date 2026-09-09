# Naikutty Visual Redesign — Design Spec

## Purpose

The functional fixes (bug fixes, working prediction pipeline, tests) are already merged on `fix/prediction-pipeline`. This spec covers a purely visual pass: the three user-facing pages (`Home.html`, `DogForm.html`, `Result.html`) currently look like three unrelated pages — a 2018 Webflow export, a bare unstyled form, and a plain results page. This redesign gives them one cohesive, warm/playful visual identity and cleans up leftover college-project cruft (dead links, an academic credit line, hotlinked third-party stock photos).

## Scope

In scope: visual restyle of all three templates, a shared CSS design system, replacing fragile/external image dependencies with inline SVG. Out of scope: any change to view logic, the prediction pipeline, or the DRF API (`Main_ModelViews`/`UserList`) — those are untouched and already tested on the fix branch. The "Send your Feedback" email signup on the homepage is restyled only; it was decorative before (no real backend) and stays decorative.

## Design System

A new shared stylesheet, `Main_Api/static/Main_Api/css/base.css`, loaded via `{% load static %}` in all three templates (replacing each page's current inline `<style>` block and, for `Home.html`, its external Webflow CSS/JS/jQuery dependency entirely).

**Tokens (CSS custom properties on `:root`):**
- `--color-bg: #fdf8f0` (warm cream)
- `--color-bg-card: #ffffff`
- `--color-primary: #8ebf42` (existing brand green — kept for continuity)
- `--color-primary-dark: #6e9a2f`
- `--color-accent: #e08e45` (warm terracotta, for tags/highlights)
- `--color-text: #3a3a3a`
- `--color-text-muted: #7a7a7a`
- `--radius-sm: 8px`, `--radius-md: 14px`, `--radius-lg: 24px`
- `--shadow-card: 0 4px 20px rgba(0,0,0,0.06)`

**Type:** Google Fonts "Baloo 2" (headings, weights 600/700) and "Nunito" (body, weights 400/600), loaded via a single `<link>` in each template's `<head>` — no WebFont.js loader.

**Shared components defined once in base.css:** `.btn` (pill-shaped, primary/secondary variants), `.card`, `.tag` (pill badge, used for the predicted group and for breed temperament traits), `.nav` (simple flex nav bar reused on Home and Form/Result via a "back to home" link).

## Page 1: Home.html

Keep every existing section and its copy (hero, "Dogs?", "Why should you have one?", "Don't skip spending time with your dog", the 3 tip cards, the stats row, "Ready to get started?" CTA, feedback signup). Changes are structural/visual only:

- **Drop:** the Webflow stylesheet link, `webfont.js`, jQuery, `webflow.85c1db4b0.js`, the IE-shim comments, all `data-w-id`/inline `transform` animation attributes (dead weight without webflow.js), the empty nav-logo `<img src="">`, the base64-embedded footer logo, the hotlinked photos from indiatoday.com/dogtime.com/a DigitalOcean bucket, the Webflow arrow SVG, the `<div class="wrapper"></div>` and empty `how-to-use`/`logos` sections that render nothing meaningful today.
- **Replace hero/section photos with inline SVG illustrations**: a simple friendly line-art dog + paw-print pattern, drawn directly in the template (no external image host dependency, no licensing ambiguity).
- **Nav:** wordmark "🐾 NaiKutty" (text, no logo image) + existing 3 links (Dogs?, Info, Find a Dog).
- **Footer:** wordmark + one-line tagline + copyright line. Remove the "Powered by Vani mam" credit and the empty-href social links per your earlier answer. No Instagram link (it had no real destination before either — `href=""`).
- Section anchors (`#about`, `#features`) are preserved so the nav links keep working.

## Page 2: DogForm.html

Restyle into a single centered card using the shared components: each of the 6 fields (name + 5 category dropdowns) gets a label + styled `<select>`/`<input>` (custom dropdown arrow via CSS, matching the rounded/warm aesthetic instead of the bare OS dropdown). Submit button uses `.btn` primary style. A small "🐾 NaiKutty" wordmark link back to `/` sits above the card. Django form field names/ids/POST behavior are unchanged — this is template/CSS only.

## Page 3: Result.html

Keep current structure (name greeting, predicted group, breed cards, "Try again" link) but apply the shared design system: group name becomes a `.tag` pill in the accent color, each breed card gets a small paw-icon bullet next to the breed name and its temperament traits rendered as small `.tag` pills instead of a plain comma-separated line. "Try again" becomes a `.btn` secondary (outline) style.

## Testing

No behavior changes, so the existing 7 Django tests (`Main_Api/tests.py`) continue to be the correctness check — they assert on template names and context data, not markup, so they remain valid unchanged. Verification for this pass is visual: manually load `/`, `/form/`, and submit the form in a browser, confirming the three pages now share consistent styling and no broken images/dead links remain.

## Self-Review Notes

- No placeholders — every section above specifies exact colors, fonts, and what gets removed vs. kept.
- Scope is a single cohesive visual pass across 3 templates + 1 new shared stylesheet; not decomposed further since the pages share one design system by construction.
- Ambiguity resolved: "restyle existing homepage" (not replace), "warm & playful" style, footer cleanup removing academic credit — all per your answers above.
