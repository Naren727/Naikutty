# Naikutty Real Photos + Responsive Design Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add real dog photos (via the Dog CEO API) to the Result page's breed cards and the homepage's 3 feature illustrations, and do a full responsive pass across 1024/768/640/480px breakpoints, per `docs/superpowers/specs/2026-09-08-naikutty-photos-responsive-design.md`.

**Architecture:** A new `breed_photo_url()` helper in `views.py` matches a breed name against the Dog CEO API's breed list (fetched once, cached via `django.core.cache`) and fetches a photo URL, itself cached per-breed for 24h; any failure returns `None`. `recommend_breeds()` attaches `photo_url` to each breed dict. `Result.html` renders a circular photo frame (real photo or paw-emoji fallback). `Home.html` gets 3 hardcoded, pre-verified Dog CEO image URLs composited into the existing SVG blob illustrations via `<image>` + `<clipPath>`. `base.css` gains 4 breakpoints replacing the current single one.

**Tech Stack:** `requests` (new dependency) for server-side HTTP calls, `django.core.cache` (built-in `LocMemCache`, no new infra) for caching, inline SVG `<image>`/`<clipPath>` for homepage photo insets.

## Global Constraints

- The breed-matching heuristic (try each word of the breed name as a Dog CEO top-level key; if it has sub-breeds, match one against the remaining words as a substring; otherwise use the key alone) is verified to resolve 181/277 (65%) of `dog.csv` breeds — do not "improve" it further as part of this plan; the fallback path for the other 35% is intentional, not a defect.
- All external HTTP calls (`requests.get`) use `timeout=2` and are wrapped in broad `try/except Exception` — a slow/down API must degrade to the fallback, never raise or hang a request.
- Tests must never make real network calls — mock `requests.get` (for the dedicated `breed_photo_url` tests) or mock `breed_photo_url` itself (for tests that only need `recommend_breeds`/`Uform` to work, not to test photo-matching logic).
- The homepage's 3 photo URLs are hardcoded static strings (not fetched at request time) — verified reachable:
  - `https://images.dog.ceo/breeds/retriever-golden/joey_img_0628.jpg`
  - `https://images.dog.ceo/breeds/husky/unibooboo.jpg`
  - `https://images.dog.ceo/breeds/corgi-cardigan/n02113186_11400.jpg`

---

### Task 1: `breed_photo_url` helper, wired into `recommend_breeds`, with mocked tests

**Files:**
- Modify: `requirements.txt`
- Modify: `Main_Api/views.py`
- Modify: `Main_Api/tests.py`

**Interfaces:**
- Produces: `breed_photo_url(breed_name: str) -> str | None`, consumed by `recommend_breeds` (Task 1) and indirectly by `Result.html` (Task 2) via the `photo_url` key each breed dict now carries.

- [ ] **Step 1: Add the dependency**

Add a line to `requirements.txt`:

```
requests==2.32.3
```

Install it:

```bash
.venv/Scripts/pip install requests==2.32.3
```

- [ ] **Step 2: Write the failing tests**

Add to `Main_Api/tests.py` (add `import re` is not needed here; add these imports at the top of the file alongside the existing ones):

```python
from unittest.mock import patch, Mock
from django.core.cache import cache
from Main_Api.views import breed_photo_url
```

Append test classes:

```python
class BreedPhotoUrlTests(TestCase):
    def setUp(self):
        cache.clear()

    @patch('Main_Api.views.requests.get')
    def test_matching_breed_returns_a_photo_url(self, mock_get):
        def fake_get(url, timeout=2):
            response = Mock()
            response.raise_for_status = Mock()
            if url == 'https://dog.ceo/api/breeds/list/all':
                response.json.return_value = {'message': {'retriever': ['golden']}}
            else:
                response.json.return_value = {
                    'status': 'success',
                    'message': 'https://images.dog.ceo/breeds/retriever-golden/fake.jpg',
                }
            return response
        mock_get.side_effect = fake_get

        self.assertEqual(
            breed_photo_url('Golden Retriever'),
            'https://images.dog.ceo/breeds/retriever-golden/fake.jpg',
        )

    @patch('Main_Api.views.requests.get')
    def test_unmatched_breed_returns_none(self, mock_get):
        def fake_get(url, timeout=2):
            response = Mock()
            response.raise_for_status = Mock()
            response.json.return_value = {'message': {'retriever': ['golden']}}
            return response
        mock_get.side_effect = fake_get

        self.assertIsNone(breed_photo_url('Totally Fictional Breed'))

    @patch('Main_Api.views.requests.get')
    def test_api_failure_returns_none_not_an_exception(self, mock_get):
        mock_get.side_effect = Exception('network is down')

        self.assertIsNone(breed_photo_url('Golden Retriever'))
```

- [ ] **Step 3: Run the tests to verify they fail**

```bash
.venv/Scripts/python manage.py test Main_Api.tests.BreedPhotoUrlTests -v 2
```

Expected: `ImportError: cannot import name 'breed_photo_url'`.

- [ ] **Step 4: Implement `breed_photo_url` in `views.py`**

Add near the top of `Main_Api/views.py`, after the existing imports (add `import re` and `import requests` to the imports, and `from django.core.cache import cache`):

```python
import re
import requests
from django.core.cache import cache
```

Add after the `GROUPS = ...` line and before the `GFC_SWITCHER` block:

```python
DOG_CEO_BREEDS_CACHE_KEY = 'dog_ceo_breeds_list'
DOG_CEO_PHOTO_CACHE_PREFIX = 'dog_ceo_photo:'
DOG_CEO_CACHE_TTL = 60 * 60 * 24  # 24 hours


def _get_dog_ceo_breeds():
    breeds = cache.get(DOG_CEO_BREEDS_CACHE_KEY)
    if breeds is not None:
        return breeds
    try:
        response = requests.get('https://dog.ceo/api/breeds/list/all', timeout=2)
        response.raise_for_status()
        breeds = response.json()['message']
    except Exception:
        breeds = {}
    cache.set(DOG_CEO_BREEDS_CACHE_KEY, breeds, DOG_CEO_CACHE_TTL)
    return breeds


def _match_dog_ceo_breed(breed_name, breeds):
    """Find a (key, sub_breed_or_None) pair in the Dog CEO breed list for breed_name.

    Tries each word of breed_name as a candidate top-level key; if that key has
    sub-breeds, looks for one that's a substring match against the remaining
    words. Verified to resolve 181/277 dog.csv breeds this way.
    """
    words = re.findall(r'[a-z]+', breed_name.lower())
    for i, word in enumerate(words):
        if word in breeds:
            subs = breeds[word]
            rest = ''.join(words[:i] + words[i + 1:])
            if not subs:
                return (word, None)
            for sub in subs:
                sub_clean = sub.replace('-', '')
                if sub_clean in rest or (rest and rest in sub_clean):
                    return (word, sub)
            return (word, None)
    return None


def breed_photo_url(breed_name):
    """Best-effort real photo URL for breed_name via the Dog CEO API, or None."""
    cache_key = f'{DOG_CEO_PHOTO_CACHE_PREFIX}{breed_name}'
    cached = cache.get(cache_key)
    if cached is not None:
        return cached or None

    photo_url = None
    match = _match_dog_ceo_breed(breed_name, _get_dog_ceo_breeds())
    if match:
        key, sub = match
        path = f'{key}/{sub}' if sub else key
        try:
            response = requests.get(f'https://dog.ceo/api/breed/{path}/images/random', timeout=2)
            response.raise_for_status()
            data = response.json()
            if data.get('status') == 'success':
                photo_url = data.get('message')
        except Exception:
            photo_url = None

    cache.set(cache_key, photo_url or '', DOG_CEO_CACHE_TTL)
    return photo_url
```

- [ ] **Step 5: Wire it into `recommend_breeds`**

Modify the `recommend_breeds` function:

```python
def recommend_breeds(group, limit=5):
    subset = _dog_df[_dog_df['group'] == group].sort_values('popularity')
    subset = subset.head(limit)
    columns = ['Breed', 'description', 'temperament', 'group', 'popularity']
    breeds = subset[columns].to_dict('records')
    for breed in breeds:
        breed['photo_url'] = breed_photo_url(breed['Breed'])
    return breeds
```

- [ ] **Step 6: Run the new tests to verify they pass**

```bash
.venv/Scripts/python manage.py test Main_Api.tests.BreedPhotoUrlTests -v 2
```

Expected: all 3 tests `OK`.

- [ ] **Step 7: Fix the now-network-dependent existing tests**

`RecommendBreedsTests` and `UformViewTests` now trigger real `breed_photo_url` calls (and therefore real network I/O) via `recommend_breeds`. Patch it out since those tests only care about the other fields. Add `@patch('Main_Api.views.breed_photo_url', return_value=None)` (with a matching `mock_photo` parameter) to every test method in `RecommendBreedsTests` and to `test_post_renders_a_recommendation` in `UformViewTests`. For example:

```python
class RecommendBreedsTests(TestCase):
    @patch('Main_Api.views.breed_photo_url', return_value=None)
    def test_returns_breeds_from_requested_group(self, mock_photo):
        breeds = recommend_breeds("Toy Group", limit=3)
        self.assertLessEqual(len(breeds), 3)
        for breed in breeds:
            self.assertEqual(breed["group"], "Toy Group")
            self.assertIn("Breed", breed)
            self.assertIn("description", breed)

    @patch('Main_Api.views.breed_photo_url', return_value=None)
    def test_sorted_by_popularity_ascending(self, mock_photo):
        breeds = recommend_breeds("Sporting Group", limit=5)
        pops = [b["popularity"] for b in breeds]
        self.assertEqual(pops, sorted(pops))
```

And for `UformViewTests.test_post_renders_a_recommendation`, add the same decorator/parameter to that one method (leave `test_get_renders_the_form` untouched — it never reaches `recommend_breeds`).

- [ ] **Step 8: Run the full suite**

```bash
.venv/Scripts/python manage.py test Main_Api -v 2
```

Expected: all 10 tests `OK`, and the run completes quickly (no real network calls).

- [ ] **Step 9: Commit**

```bash
git add requirements.txt Main_Api/views.py Main_Api/tests.py
git commit -m "feat: add Dog CEO API breed photo lookup with tested fallback"
```

---

### Task 2: Circular photo frame on the Result page

**Files:**
- Modify: `Main_Api/static/Main_Api/css/base.css`
- Modify: `Main_Api/templates/Myforms/Result.html`

**Interfaces:**
- Consumes: `breed.photo_url` (may be `None`) from Task 1.

- [ ] **Step 1: Replace the `.paw` CSS rule with a `.photo-frame` rule**

In `Main_Api/static/Main_Api/css/base.css`, replace:

```css
.breed-card .paw { font-size: 24px; line-height: 1.2; }
```

with:

```css
.breed-card .photo-frame {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  border: 3px solid var(--color-accent);
  font-size: 24px;
}
.breed-card .photo-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

- [ ] **Step 2: Update the template**

In `Main_Api/templates/Myforms/Result.html`, replace:

```html
        <div class="paw">&#128062;</div>
```

with:

```html
        <div class="photo-frame">
          {% if breed.photo_url %}<img src="{{ breed.photo_url }}" alt="{{ breed.Breed }}">{% else %}&#128062;{% endif %}
        </div>
```

- [ ] **Step 3: Run the tests**

```bash
.venv/Scripts/python manage.py test Main_Api -v 1
```

Expected: all 10 tests `OK` (template change isn't asserted on directly, but confirms nothing broke).

- [ ] **Step 4: Commit**

```bash
git add Main_Api/static/Main_Api/css/base.css Main_Api/templates/Myforms/Result.html
git commit -m "style: show a real breed photo (or paw fallback) on the results page"
```

---

### Task 3: Homepage photo insets + full responsive breakpoint pass

**Files:**
- Modify: `Main_Api/templates/Myforms/Home.html`
- Modify: `Main_Api/static/Main_Api/css/base.css`

**Interfaces:** none beyond static HTML/CSS.

- [ ] **Step 1: Inset real photos into the 3 feature-row SVGs**

In `Main_Api/templates/Myforms/Home.html`, replace each of the 3 feature-row SVGs under `id="features"` with a version that clips a real photo into the existing colored circle. Replace:

```html
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <circle cx="80" cy="80" r="70" fill="#fbe4e8"/>
            <path d="M80 115s-32-19-32-42a18 18 0 0 1 32-11 18 18 0 0 1 32 11c0 23-32 42-32 42z" fill="#e08e45"/>
          </svg>
        </div>
```

with:

```html
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <defs><clipPath id="photoClip1"><circle cx="80" cy="80" r="55"/></clipPath></defs>
            <circle cx="80" cy="80" r="70" fill="#fbe4e8"/>
            <image href="https://images.dog.ceo/breeds/retriever-golden/joey_img_0628.jpg" x="25" y="25" width="110" height="110" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip1)"/>
          </svg>
        </div>
```

Replace the second feature-row's SVG:

```html
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <circle cx="80" cy="80" r="70" fill="#eaf1dd"/>
            <g fill="#8ebf42">
              <ellipse cx="55" cy="50" rx="8" ry="12"/>
              <ellipse cx="105" cy="70" rx="8" ry="12"/>
              <ellipse cx="55" cy="90" rx="8" ry="12"/>
              <ellipse cx="105" cy="110" rx="8" ry="12"/>
            </g>
          </svg>
        </div>
```

with:

```html
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <defs><clipPath id="photoClip2"><circle cx="80" cy="80" r="55"/></clipPath></defs>
            <circle cx="80" cy="80" r="70" fill="#eaf1dd"/>
            <image href="https://images.dog.ceo/breeds/husky/unibooboo.jpg" x="25" y="25" width="110" height="110" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip2)"/>
          </svg>
        </div>
```

Replace the third feature-row's SVG:

```html
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <circle cx="80" cy="80" r="70" fill="#fdf0dd"/>
            <circle cx="80" cy="80" r="30" fill="none" stroke="#e08e45" stroke-width="5"/>
            <path d="M80 50v60M50 80h60M60 60l40 40M100 60L60 100" stroke="#e08e45" stroke-width="3"/>
          </svg>
        </div>
```

with:

```html
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <defs><clipPath id="photoClip3"><circle cx="80" cy="80" r="55"/></clipPath></defs>
            <circle cx="80" cy="80" r="70" fill="#fdf0dd"/>
            <image href="https://images.dog.ceo/breeds/corgi-cardigan/n02113186_11400.jpg" x="25" y="25" width="110" height="110" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip3)"/>
          </svg>
        </div>
```

(The hero illustration and the "When are you getting your dog?" first feature-row SVG are unchanged — only the 3 rows inside `id="features"` get photos, per the spec.)

- [ ] **Step 2: Replace the responsive breakpoints in base.css**

In `Main_Api/static/Main_Api/css/base.css`, replace the existing single media query block:

```css
@media (max-width: 640px) {
  .feature-row, .feature-row.reverse { flex-direction: column; }
  .tip-grid, .stats-row { grid-template-columns: 1fr 1fr; }
  .hero h1 { font-size: 32px; }
}
```

with:

```css
@media (max-width: 1024px) {
  .feature-row .feature-illustration svg { max-width: 170px; }
}

@media (max-width: 768px) {
  .site-nav { flex-wrap: wrap; gap: 12px; justify-content: center; text-align: center; }
  .tip-grid, .stats-row { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 640px) {
  .feature-row, .feature-row.reverse { flex-direction: column; }
  .hero h1 { font-size: 32px; }
}

@media (max-width: 480px) {
  .tip-grid, .stats-row { grid-template-columns: 1fr; }
  .hero { padding: 40px 16px 30px; }
  .form-page, .result-page { padding: 0 16px; }
  .breed-card .photo-frame { width: 44px; height: 44px; font-size: 20px; }
  .feature-row .feature-illustration svg { max-width: 150px; }
}
```

- [ ] **Step 3: Run the tests**

```bash
.venv/Scripts/python manage.py test Main_Api -v 1
```

Expected: all 10 tests `OK`.

- [ ] **Step 4: Commit**

```bash
git add Main_Api/templates/Myforms/Home.html Main_Api/static/Main_Api/css/base.css
git commit -m "style: inset real photos into the homepage and add responsive breakpoints"
```

---

### Task 4: Manual verification

**Files:** none (verification only)

- [ ] **Step 1: Start the dev server and load the homepage**

```bash
.venv/Scripts/python manage.py runserver
```

Confirm the 3 feature-row circles now show real dog photos inset in their colored rings, and the hero/first "When are you getting your dog?" illustration are unchanged.

- [ ] **Step 2: Submit the form and check the Result page**

Confirm each breed card shows either a real circular photo or the paw-emoji fallback (both should look intentional, not broken) — try preferences that land on a few different groups to see both cases.

- [ ] **Step 3: Resize through each breakpoint**

Check the homepage, form, and result pages at browser widths around 1280px (desktop), 1024px, 768px, 640px, and 375px (mobile), confirming: no horizontal scrollbar at any width, the nav wraps cleanly on narrow screens, the tip/stats grids step down from 3→2→1 columns, and text/buttons stay legible and tappable.

- [ ] **Step 4: Run the full suite one final time**

```bash
.venv/Scripts/python manage.py test
```

Expected: all tests `OK`.

- [ ] **Step 5: Commit any fixups**

```bash
git add -A
git commit -m "fix: address issues found in manual verification"
```
