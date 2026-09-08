# Naikutty Real Photos + Responsive Design — Design Spec

## Purpose

The visual redesign (previous spec/plan) replaced hotlinked third-party stock photos with inline SVG illustrations, trading photo-realism for reliability. This spec adds real dog photos back in a reliable way — via the [Dog CEO API](https://dog.ceo/api), a free public API built specifically for serving breed photos — and does a full responsive pass so the site works well from small phones through desktop.

## Part 1: Real Photos

### Source

Dog CEO API (`https://dog.ceo/api`), confirmed reachable and stable. No API key, no rate limit documented, images served from `images.dog.ceo` (Cloudflare-backed, stable static file URLs).

### Breed photos on the Result page

`views.py` gains a `breed_photo_url(breed_name)` helper:

1. Normalize the breed name to lowercase words (strip non-letters).
2. Try each word, in order, as a candidate Dog CEO top-level breed key (fetched once at import time from `https://dog.ceo/api/breeds/list/all` and cached — see Caching below). The first word that matches a key wins.
3. If that key has sub-breeds, look for a sub-breed whose name is a substring of (or contains) the remaining words joined together — e.g. "Golden Retriever" → key `retriever`, remaining `golden` → matches sub-breed `golden`.
4. If a sub-breed matches, request `https://dog.ceo/api/breed/{key}/{sub}/images/random`; if the key has no sub-breeds or none matched, request `https://dog.ceo/api/breed/{key}/images/random`.
5. Any failure (no key match, HTTP error, timeout, malformed response) returns `None` — never raises.

Verified against all 277 breeds in `dog.csv`: **181/277 (65%) resolve to a real photo**; the remaining 96 are breeds Dog CEO's dataset genuinely doesn't have (e.g. Azawakh, Barbet, Bolognese) and fall back to the current paw emoji. This is expected, not a bug — the fallback is the point.

**Caching:** Django's built-in `django.core.cache` (default `LocMemCache`, no new infrastructure) stores the breed-key/sub-breed list (fetched once, 24h TTL) and each per-breed photo lookup result — including a "no photo" sentinel for misses — so repeat requests for the same breed don't re-hit the external API. Network calls use a 2-second timeout and are wrapped in a broad `try/except` so a slow or down API degrades to the existing fallback instead of breaking the page.

**Presentation:** each breed card's current paw emoji is replaced by a 56px circular frame: a real photo (`<img>`, `object-fit: cover`, `border-radius: 50%`) when `photo_url` is present, otherwise the existing paw emoji centered in the same circular frame — so the layout doesn't shift based on photo availability. The frame keeps a thin accent-colored ring, matching the current "warm & playful" theme rather than looking like a bolted-on photo.

### Homepage photos

The 3 feature-row illustrations (currently solid-color SVG blobs with abstract icon paths) each get a small real photo inset as a circular image sitting inside the existing colored blob — the blob becomes a ring/frame around the photo rather than being replaced. Three specific, pre-verified, permanent Dog CEO static image URLs are hardcoded directly in `Home.html` (not fetched at request time — no backend dependency for the homepage, and these exact files are confirmed stable):

- `https://images.dog.ceo/breeds/retriever-golden/joey_img_0628.jpg` (for "Dogs?")
- `https://images.dog.ceo/breeds/husky/unibooboo.jpg` (for "Why should you have one?")
- `https://images.dog.ceo/breeds/corgi-cardigan/n02113186_11400.jpg` (for "Don't skip spending time with your dog")

The hero illustration (the cartoon dog face) stays as-is — it's the brand mark, not a "real dog" moment.

### New dependency

`requests` is added to `requirements.txt` for the server-side Dog CEO calls.

## Part 2: Responsive Design

Current `base.css` has one `@media (max-width: 640px)` block covering feature-row stacking and grid collapse. This expands to a proper multi-breakpoint pass:

- **1024px (tablet landscape / small laptop):** feature-row illustrations shrink slightly; container max-widths already fluid via `max-width` + `padding`, no major change needed here beyond confirming no horizontal overflow.
- **768px (tablet portrait):** nav switches from a single row to wrapping (wordmark on its own line if needed, links wrap below); tip-grid and stats-row drop from the current break to 2 columns *starting here* instead of at 640px, so tablets get the 2-column layout earlier.
- **640px (large phone):** feature-rows stack vertically (existing behavior, kept); hero heading size reduces (existing, kept).
- **480px (small phone):** tip-grid and stats-row drop to a single column; the circular photo frames on breed cards and feature rows shrink further; form/result page horizontal padding reduces slightly so content isn't cramped against the edge.

All breakpoints are additive `max-width` media queries layered on the existing mobile-first-ish structure (the base styles already assume a flexible, non-fixed-width layout, so this is refinement, not a rewrite). No JavaScript, no hamburger menu — the nav has only 3 links plus a wordmark, so wrapping is sufficient at this scale.

## Testing

- New test in `Main_Api/tests.py` for `breed_photo_url`: mocks `requests.get` (via `unittest.mock.patch`) so the test suite never makes a real network call — asserts a matching breed returns a photo URL and a clearly-nonexistent breed name returns `None`.
- Existing 7 tests continue to pass unchanged (they don't assert on markup/images).
- Manual verification: load Result page for a breed that should match (e.g. submit preferences that recommend a Golden Retriever-containing group) and confirm a real photo renders; resize the browser through 1024/768/640/480px and confirm no horizontal scrollbar or overlapping content at any width.

## Self-Review Notes

- No placeholders — matching algorithm, cache strategy, exact image URLs, and breakpoint behavior are all fully specified.
- Scope: one cohesive pass (photos + responsive) since both are refinements to the already-built design system, not a new subsystem.
- Ambiguity resolved: image source (Dog CEO API, live, per user's choice), homepage images are hardcoded/stable rather than live-fetched (avoids a backend dependency for a page that has no view logic today), fallback behavior when no photo match exists (paw emoji, unchanged layout).
