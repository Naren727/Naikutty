# Naikutty "Professional Playful" Polish — Design Spec

## Purpose

Following visual brainstorming (3 mockup directions compared live, "B. Modern SaaS Playful" selected and then refined for more depth/richness), this spec upgrades the whole site — not just the homepage hero — to the validated look: layered gradient-mesh backgrounds, a floating glass nav, gradient-filled buttons and bento cards with colored glow shadows, and hover-lift micro-interactions. Same warm palette and playful tone; more depth, polish, and visual confidence.

## Design Tokens (additions to `base.css` `:root`)

```css
--gradient-primary: linear-gradient(135deg, #8ebf42, #6e9a2f);
--gradient-accent: linear-gradient(135deg, #f4a261, #e08e45);
--shadow-glow-primary: 0 12px 28px -8px rgba(110, 154, 47, 0.55);
--shadow-glow-accent: 0 12px 28px -8px rgba(224, 142, 69, 0.5);
--shadow-lift: 0 18px 34px -12px rgba(0, 0, 0, 0.18);
--glass-bg: rgba(255, 255, 255, 0.65);
--glass-border: rgba(255, 255, 255, 0.9);
```

## Sitewide changes (apply to Home, DogForm, Result)

- **Background:** `body` gets a subtle layered gradient mesh (soft green blob upper-left, soft terracotta blob upper-right, faint green blob lower-left, all radial-gradient, over the existing cream base) instead of flat `--color-bg`. Same mesh recipe validated in the mockup, toned down slightly (lower opacity) so it reads as ambient depth, not a busy background — body text stays fully readable.
- **Nav:** `.site-nav` becomes a floating glass pill — `background: var(--glass-bg)`, `backdrop-filter: blur(14px)`, `border: 1px solid var(--glass-border)`, `border-radius: 999px`, soft shadow, sitting with margin from the viewport edge instead of a flush top bar. Home keeps its 3 links (Dogs?/Info/Find a Dog); DogForm and Result currently have no nav (just a plain "← NaiKutty" text link) — both gain the same floating glass nav component (wordmark linking to `/`) for consistency, replacing the old back-link.
- **Buttons:** `.btn-primary` switches from flat `--color-primary` to `var(--gradient-primary)` fill plus `var(--shadow-glow-primary)`, with a hover state that lifts (`translateY(-2px)`) and deepens the shadow. `.btn-secondary` becomes a translucent "ghost" button (`var(--glass-bg)` background, 1.5px border) rather than a flat outline.
- **Headings:** tighten letter-spacing slightly (`-0.3px`) sitewide for a more confident, less default-webfont look.
- **Interactive cards:** `.tip-card` and `.breed-card` get a hover-lift transition (`translateY(-4px)` + `var(--shadow-lift)`) — the same micro-interaction validated on the bento mockup.

## Home page

- **Hero:** rebuilt to match the validated mockup — an eyebrow pill badge ("🐾 Free · Takes 30 seconds"), the heading with "furry friend" rendered in a green→terracotta gradient-text span, subtitle copy, and two buttons (gradient primary "Get a Dog" + ghost secondary "See how it works" scrolling to `#about`). The cartoon dog illustration stays, now sitting on a soft radial-gradient glow blob behind it for depth.
- **Feature rows** (all 4: "When are you getting your dog?", "Dogs?", "Why should you have one?", "Don't skip spending time with your dog"): each row's photo circle switches from the current thin flat ring to a colored glow-shadow (matching each row's accent tint) for the bento-card depth language. The previously-icon-only first row ("When are you getting your dog?") gets a real photo too, for full consistency: `https://images.dog.ceo/breeds/labrador/pic1_l.jpg` (verified reachable), replacing its abstract line-art icon.
- **Tip cards:** each gets a small colored gradient circle behind its icon (green/accent-tinted, alternating) instead of a plain currentColor icon floating on white, plus the sitewide hover-lift.
- **Stats row:** rebuilt as a proper bento strip mixing a gradient cell and glass cells (mirroring the hero mockup's `c3`/`c5` treatment) instead of one flat solid-green rectangle — e.g. 2 gradient-accent cells and 2 glass cells alternating, each with its own subtle shadow.
- **CTA band + feedback band:** both become glass cards (`var(--glass-bg)` + blur + border) instead of flat white, buttons updated to the new gradient/ghost styles.
- **Footer:** unchanged content, restyled to sit on the new mesh background cleanly (no structural change needed here).

## DogForm page

- Gains the floating glass nav (replacing the plain back-link).
- The form's `.card` container gets a slightly stronger shadow (`var(--shadow-lift)` on the container itself is too strong for a static panel — use a middle-ground shadow, not full lift) so it reads as "elevated" against the new mesh background.
- Submit button switches to the new gradient `.btn-primary` styling automatically (shared class).

## Result page

- Gains the floating glass nav (replacing the plain back-link) — keeps the "Try again" ghost button at the bottom as-is (already `.btn-secondary`, inherits the new ghost style automatically).
- The group-name tag (`.tag-primary`) switches to `var(--gradient-primary)` fill instead of flat color.
- Breed card photo frames switch from the flat 3px accent-colored ring to a colored glow-shadow (same treatment as the homepage feature photos), and `.breed-card` picks up the sitewide hover-lift.

## Explicitly out of scope

- No changes to `views.py`, `models.py`, `forms.py`, or any Python logic — this is templates/CSS only, same as the prior two design passes.
- No new sections or content — this is a visual upgrade of existing content, not new copy (aside from the hero eyebrow badge text already agreed: "Free · Takes 30 seconds").
- No JavaScript/scroll-reveal animations — hover-lift and backdrop-blur are pure CSS, no new script needed, keeping the site framework-free.

## Testing

- All 10 existing tests continue to pass unchanged (template-name/context assertions, not markup).
- Manual verification: load all 3 pages, confirm the glass nav/gradient buttons/mesh background render consistently across them, confirm hover-lift works on tip cards and breed cards, confirm the 4th feature row now shows a real photo, and re-check the 4 responsive breakpoints (1024/768/640/480) since the nav and hero are being rebuilt.

## Self-Review Notes

- No placeholders — every token value, gradient recipe, and per-page change is spelled out above.
- Scope: one cohesive visual-system upgrade across all 3 templates plus `base.css`; not decomposed further since the whole point is sitewide consistency.
- Ambiguity resolved: nav unification (DogForm/Result gain the same nav component Home has, since leaving them on the old plain back-link would undercut the "sitewide professional polish" goal), and the 4th feature row's missing photo is fixed as part of this pass rather than left inconsistent.
