# Naikutty Visual Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give Home.html, DogForm.html, and Result.html one cohesive "warm & playful" visual identity via a shared stylesheet, replacing the fragile Webflow-era homepage markup and each page's bespoke inline styles, per `docs/superpowers/specs/2026-09-08-naikutty-redesign-design.md`.

**Architecture:** One new shared stylesheet (`Main_Api/static/Main_Api/css/base.css`) loaded by all three templates via Django's `staticfiles` app (already configured — `django.contrib.staticfiles` is installed and `STATICFILES_STORAGE`/`STATIC_ROOT` are set). A small template filter (`Main_Api/templatetags/dog_extras.py`) splits the comma-separated `temperament` string into individual tag pills for Result.html, keeping `views.py` untouched. All hotlinked third-party photos and the Webflow framework/jQuery/WebFont-loader dependency on Home.html are replaced with inline SVG illustrations and a direct Google Fonts `<link>`.

**Tech Stack:** Plain CSS (custom properties), inline SVG, Django template tags/filters. No new Python dependencies.

## Global Constraints

- No changes to `views.py`, `models.py`, `forms.py`, `urls.py`, or the DRF API — this is a template/CSS/static-asset-only pass.
- The 7 existing tests in `Main_Api/tests.py` must continue to pass unchanged (they assert template names and context data, not markup).
- Design tokens (exact hex values, font names) below are taken verbatim from the approved spec — do not substitute different colors/fonts.
- Every template loads fonts via a direct `<link>` (no `WebFont.load()` JS loader) and `{% load static %}` + `{% static 'Main_Api/css/base.css' %}` for the stylesheet.

---

### Task 1: Shared design-system stylesheet

**Files:**
- Create: `Main_Api/static/Main_Api/css/base.css`

**Interfaces:**
- Produces: CSS custom properties (`--color-bg`, `--color-primary`, etc.) and component classes (`.btn`, `.btn-primary`, `.btn-secondary`, `.card`, `.tag`, `.tag-primary`, `.site-nav`, `.hero`, `.feature-row`, `.tip-grid`, `.stats-row`, `.cta-band`, `.feedback-form`, `.site-footer`, `.form-page`, `.field`, `.result-page`, `.breed-card`) consumed by Tasks 3-5.

- [ ] **Step 1: Create the static directory and stylesheet**

Create `Main_Api/static/Main_Api/css/base.css`:

```css
:root {
  --color-bg: #fdf8f0;
  --color-bg-card: #ffffff;
  --color-primary: #8ebf42;
  --color-primary-dark: #6e9a2f;
  --color-accent: #e08e45;
  --color-text: #3a3a3a;
  --color-text-muted: #7a7a7a;
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 24px;
  --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.06);
  --font-heading: 'Baloo 2', cursive;
  --font-body: 'Nunito', sans-serif;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-body);
  line-height: 1.6;
}

h1, h2, h3, h4 {
  font-family: var(--font-heading);
  color: var(--color-text);
  margin: 0 0 0.5em;
}

a { color: var(--color-primary-dark); text-decoration: none; }

.container { max-width: 960px; margin: 0 auto; padding: 0 24px; }

/* Nav */
.site-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  max-width: 960px;
  margin: 0 auto;
}
.site-nav .wordmark {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-primary-dark);
}
.site-nav .nav-links { display: flex; gap: 24px; }
.site-nav .nav-links a { font-weight: 600; color: var(--color-text); }
.site-nav .nav-links a:hover { color: var(--color-primary-dark); }

/* Buttons */
.btn {
  display: inline-block;
  padding: 12px 28px;
  border-radius: 999px;
  font-family: var(--font-heading);
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  border: 2px solid transparent;
  text-align: center;
}
.btn-primary { background: var(--color-primary); color: #fff; }
.btn-primary:hover { background: var(--color-primary-dark); }
.btn-secondary { background: transparent; border-color: var(--color-primary); color: var(--color-primary-dark); }
.btn-secondary:hover { background: var(--color-primary); color: #fff; }

/* Cards */
.card {
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  padding: 24px;
}

/* Tags */
.tag {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  background: var(--color-accent);
  color: #fff;
  margin: 2px 4px 2px 0;
}
.tag-primary { background: var(--color-primary); }

/* Hero (Home) */
.hero { text-align: center; padding: 60px 24px 40px; }
.hero .illustration { max-width: 220px; margin: 0 auto 24px; display: block; }
.hero h1 { font-size: 42px; }
.hero p.subhead { font-size: 18px; color: var(--color-text-muted); margin-bottom: 28px; }

/* Feature rows (Home) */
.feature-row { display: flex; align-items: center; gap: 48px; padding: 48px 0; max-width: 960px; margin: 0 auto; }
.feature-row.reverse { flex-direction: row-reverse; }
.feature-row .feature-text { flex: 1; }
.feature-row .feature-illustration { flex: 1; text-align: center; }
.feature-row .feature-illustration svg { max-width: 200px; width: 100%; height: auto; }

/* Tip cards (Home) */
.tip-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; max-width: 960px; margin: 0 auto; padding: 24px 24px 48px; }
.tip-card { text-align: center; padding: 24px; }
.tip-card svg { width: 48px; height: 48px; margin-bottom: 12px; color: var(--color-primary); }

/* Stats (Home) */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  background: var(--color-primary);
  border-radius: var(--radius-lg);
  padding: 32px 24px;
  margin: 24px auto 48px;
  max-width: 960px;
  color: #fff;
  text-align: center;
}
.stats-row .stat-number { font-family: var(--font-heading); font-size: 32px; font-weight: 700; }
.stats-row .stat-label { font-size: 14px; opacity: 0.9; }

/* CTA band (Home) */
.cta-band {
  text-align: center;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: 48px 24px;
  margin: 24px auto;
  max-width: 960px;
}

/* Feedback form (Home) */
.feedback-form { display: flex; gap: 12px; max-width: 420px; margin: 24px auto 0; }
.feedback-form input[type=email] {
  flex: 1;
  padding: 12px 16px;
  border-radius: 999px;
  border: 2px solid #e5ddd0;
  font-family: var(--font-body);
  font-size: 15px;
}

/* Footer (Home) */
.site-footer { text-align: center; padding: 40px 24px 60px; color: var(--color-text-muted); font-size: 14px; }
.site-footer .wordmark { font-family: var(--font-heading); font-size: 20px; color: var(--color-primary-dark); display: block; margin-bottom: 8px; }

/* Form card (DogForm) */
.form-page { max-width: 520px; margin: 40px auto; padding: 0 24px; }
.form-page .back-link { display: inline-block; margin-bottom: 20px; font-weight: 600; }
.form-page p.intro { color: var(--color-text-muted); margin-top: -8px; }
.field { margin-bottom: 20px; }
.field label { display: block; font-weight: 600; margin-bottom: 6px; }
.field input[type=text], .field select {
  width: 100%;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  border: 2px solid #e5ddd0;
  font-family: var(--font-body);
  font-size: 15px;
  background-color: #fff;
  appearance: none;
}
.field select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%237a7a7a'%3E%3Cpath d='M5 8l5 5 5-5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 36px;
}
.field input:focus, .field select:focus { outline: none; border-color: var(--color-primary); }
.form-page .btn { width: 100%; }

/* Result page */
.result-page { max-width: 640px; margin: 40px auto; padding: 0 24px; }
.result-page .back-link { display: inline-block; margin-bottom: 20px; font-weight: 600; }
.result-page .group-callout { margin: 12px 0 28px; }
.result-page .group-callout .tag { font-size: 16px; padding: 8px 20px; }
.breed-card { display: flex; gap: 16px; margin-bottom: 16px; }
.breed-card .paw { font-size: 24px; line-height: 1.2; }
.breed-card h2 { font-size: 20px; margin-bottom: 6px; }
.breed-card p.description { color: var(--color-text-muted); margin-top: 10px; }
.result-page .try-again { margin-top: 24px; }

@media (max-width: 640px) {
  .feature-row, .feature-row.reverse { flex-direction: column; }
  .tip-grid, .stats-row { grid-template-columns: 1fr 1fr; }
  .hero h1 { font-size: 32px; }
}
```

- [ ] **Step 2: Verify Django finds the static file**

```bash
.venv/Scripts/python manage.py findstatic Main_Api/css/base.css
```

Expected: prints the absolute path to the file (confirms `AppDirectoriesFinder` picks it up — no `STATICFILES_DIRS` change needed).

- [ ] **Step 3: Commit**

```bash
git add Main_Api/static/Main_Api/css/base.css
git commit -m "feat: add shared design-system stylesheet"
```

---

### Task 2: Template filter to split temperament into tag pills

**Files:**
- Create: `Main_Api/templatetags/__init__.py`
- Create: `Main_Api/templatetags/dog_extras.py`

**Interfaces:**
- Produces: `{% load dog_extras %}` + `{{ value|split_comma }}` — a template filter returning a list of trimmed strings, consumed by Task 4 (Result.html).

- [ ] **Step 1: Create the templatetags package**

Create `Main_Api/templatetags/__init__.py` (empty file).

- [ ] **Step 2: Implement the filter**

Create `Main_Api/templatetags/dog_extras.py`:

```python
from django import template

register = template.Library()


@register.filter
def split_comma(value):
    """Split 'Friendly, Smart, Obedient' into ['Friendly', 'Smart', 'Obedient']."""
    if not value:
        return []
    return [part.strip() for part in value.split(',') if part.strip()]
```

- [ ] **Step 3: Verify it's importable**

```bash
.venv/Scripts/python manage.py shell -c "from Main_Api.templatetags.dog_extras import split_comma; print(split_comma('Friendly, Smart, Obedient'))"
```

Expected: `['Friendly', 'Smart', 'Obedient']`

- [ ] **Step 4: Commit**

```bash
git add Main_Api/templatetags/
git commit -m "feat: add split_comma template filter for temperament tags"
```

---

### Task 3: Restyle DogForm.html

**Files:**
- Modify: `Main_Api/templates/Myforms/DogForm.html` (full rewrite)

**Interfaces:**
- Consumes: `Main_Api/static/Main_Api/css/base.css` (Task 1). Field names/ids (`name`, `gfc`, `sc`, `elc`, `tc`, `dc`, `xtra`) are unchanged — `Userforms` in `Main_Api/forms.py` and `Uform` in `views.py` depend on these exact names.

- [ ] **Step 1: Replace the file**

Replace the full contents of `Main_Api/templates/Myforms/DogForm.html`:

```html
{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Find Your Dog — NaiKutty</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700&family=Nunito:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'Main_Api/css/base.css' %}">
  </head>
  <body>
    <div class="form-page">
      <a class="back-link" href="/">&larr; NaiKutty</a>
      <div class="card">
        <h1>Find Your Dog</h1>
        <p class="intro">Answer a few questions and we'll match you with a breed group.</p>
        <form action="" method="POST">
          {% csrf_token %}
          <div class="field">
            <label for="name">Name</label>
            <input type="text" value="John Doe" id="name" name="name"/>
          </div>
          <div class="field">
            <label for="gfc">Grooming Frequency</label>
            <select name="gfc" id="gfc">
              <option value="2-3 Times a Week Brushing">2-3 Times a Week Brushing</option>
              <option value="Daily Brushing">Daily Brushing</option>
              <option value="Occasional Bath/Brush">Occasional Bath/Brush</option>
              <option value="Specialty/Professional">Specialty/Professional</option>
              <option value="Weekly Brushing">Weekly Brushing</option>
            </select>
          </div>
          <div class="field">
            <label for="sc">Shedding</label>
            <select name="sc" id="sc">
              <option value="Frequent">Frequent</option>
              <option value="Infrequent">Infrequent</option>
              <option value="Occasional">Occasional</option>
              <option value="Regularly">Regularly</option>
              <option value="Seasonal">Seasonal</option>
            </select>
          </div>
          <div class="field">
            <label for="elc">Energy Level</label>
            <select name="elc" id="elc">
              <option value="Calm">Calm</option>
              <option value="Couch Potato">Couch Potato</option>
              <option value="Energetic">Energetic</option>
              <option value="Needs Lots of Activity">Needs Lots of Activity</option>
              <option value="Regular Exercise">Regular Exercise</option>
            </select>
          </div>
          <div class="field">
            <label for="tc">Trainability</label>
            <select name="tc" id="tc">
              <option value="Agreeable">Agreeable</option>
              <option value="Eager to Please">Eager to Please</option>
              <option value="Easy Training">Easy Training</option>
              <option value="Independent">Independent</option>
              <option value="May be Stubborn">May be Stubborn</option>
            </select>
          </div>
          <div class="field">
            <label for="dc">Demeanor</label>
            <select name="dc" id="dc">
              <option value="Alert/Responsive">Alert/Responsive</option>
              <option value="Aloof/Wary">Aloof/Wary</option>
              <option value="Friendly">Friendly</option>
              <option value="Outgoing">Outgoing</option>
              <option value="Reserved with Strangers">Reserved with Strangers</option>
            </select>
          </div>
          <div class="field">
            <label for="xtra1">Anything else?</label>
            <input type="text" value="none" id="xtra1" name="xtra"/>
          </div>
          <button type="submit" class="btn btn-primary">Find My Dog</button>
        </form>
      </div>
    </div>
  </body>
</html>
```

- [ ] **Step 2: Run the existing view tests**

```bash
.venv/Scripts/python manage.py test Main_Api.tests.UformViewTests -v 2
```

Expected: both tests still `OK` (field names unchanged, so form submission still works).

- [ ] **Step 3: Commit**

```bash
git add Main_Api/templates/Myforms/DogForm.html
git commit -m "style: restyle the dog preference form with the shared design system"
```

---

### Task 4: Restyle Result.html

**Files:**
- Modify: `Main_Api/templates/Myforms/Result.html` (full rewrite)

**Interfaces:**
- Consumes: `Main_Api/static/Main_Api/css/base.css` (Task 1), `split_comma` filter (Task 2), and the existing context (`name`, `group`, `breeds`) from `Uform` in `views.py` — unchanged.

- [ ] **Step 1: Replace the file**

Replace the full contents of `Main_Api/templates/Myforms/Result.html`:

```html
{% load static %}
{% load dog_extras %}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Your Dog Recommendation — NaiKutty</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700&family=Nunito:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'Main_Api/css/base.css' %}">
  </head>
  <body>
    <div class="result-page">
      <a class="back-link" href="/">&larr; NaiKutty</a>
      <h1>Thanks, {{ name }}!</h1>
      <p>Based on your preferences, you're best matched with the:</p>
      <div class="group-callout"><span class="tag tag-primary">{{ group }}</span></div>
      <h3>Recommended breeds</h3>
      {% for breed in breeds %}
      <div class="card breed-card">
        <div class="paw">&#128062;</div>
        <div>
          <h2>{{ breed.Breed }}</h2>
          <div>
            {% for trait in breed.temperament|split_comma %}<span class="tag">{{ trait }}</span>{% endfor %}
          </div>
          <p class="description">{{ breed.description|truncatewords:40 }}</p>
        </div>
      </div>
      {% empty %}
      <p>No breeds found for this group.</p>
      {% endfor %}
      <a class="btn btn-secondary try-again" href="/form/">&larr; Try again</a>
    </div>
  </body>
</html>
```

- [ ] **Step 2: Run the existing view tests**

```bash
.venv/Scripts/python manage.py test Main_Api.tests.UformViewTests -v 2
```

Expected: both tests still `OK`.

- [ ] **Step 3: Commit**

```bash
git add Main_Api/templates/Myforms/Result.html
git commit -m "style: restyle the results page with tag-pill temperament traits"
```

---

### Task 5: Restyle Home.html

**Files:**
- Modify: `Main_Api/templates/Myforms/Home.html` (full rewrite)

**Interfaces:**
- Consumes: `Main_Api/static/Main_Api/css/base.css` (Task 1). Preserves anchors `#about` and `#features` (linked from the nav) and the `/form` links (linked from `Naikutty/urls.py` → `Main_Api/urls.py` → `views.Uform`, unchanged).

- [ ] **Step 1: Replace the file**

Replace the full contents of `Main_Api/templates/Myforms/Home.html`:

```html
{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>NaiKutty — Find Your Dog</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700&family=Nunito:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'Main_Api/css/base.css' %}">
  </head>
  <body>
    <nav class="site-nav">
      <span class="wordmark">&#128062; NaiKutty</span>
      <div class="nav-links">
        <a href="#about">Dogs?</a>
        <a href="#features">Info</a>
        <a href="/form">Find a Dog</a>
      </div>
    </nav>

    <div class="hero">
      <svg class="illustration" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="110" r="70" fill="#f6c893"/>
        <ellipse cx="55" cy="60" rx="22" ry="34" fill="#e08e45" transform="rotate(-20 55 60)"/>
        <ellipse cx="145" cy="60" rx="22" ry="34" fill="#e08e45" transform="rotate(20 145 60)"/>
        <circle cx="75" cy="105" r="8" fill="#3a3a3a"/>
        <circle cx="125" cy="105" r="8" fill="#3a3a3a"/>
        <ellipse cx="100" cy="130" rx="14" ry="10" fill="#3a3a3a"/>
        <path d="M100 140 Q100 155 115 155" stroke="#3a3a3a" stroke-width="4" fill="none" stroke-linecap="round"/>
        <ellipse cx="100" cy="160" rx="18" ry="10" fill="#f28fa1"/>
      </svg>
      <h1>NaiKutty.com</h1>
      <p class="subhead">Pick out your furry friend today!</p>
      <a class="btn btn-primary" href="/form">Get a Dog</a>
    </div>

    <div class="feature-row" id="about">
      <div class="feature-text">
        <h2>When are you getting your dog?</h2>
        <p>Tell us how you groom, how much energy you have, and what kind of temperament fits your home — we'll point you to a breed group that matches.</p>
      </div>
      <div class="feature-illustration">
        <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
          <circle cx="80" cy="80" r="70" fill="#f0e4d0"/>
          <g fill="none" stroke="#8ebf42" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="80" cy="60" r="22"/>
            <path d="M45 120c5-25 22-38 35-38s30 13 35 38"/>
          </g>
        </svg>
      </div>
    </div>

    <div id="features">
      <div class="feature-row">
        <div class="feature-text">
          <h2>Dogs?</h2>
          <p>Cuteness. It's what makes us squee over puppy pics and rush to forgive our pets for the occasional naughty misstep. But why are dogs so cute? What is it about man's best friend that turns even the toughest tough guy into a babytalking fool every time his dog rolls over for a belly rub? It turns out the science of cute is fascinating stuff. Dogs do speak but only to those who know to listen.</p>
        </div>
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <circle cx="80" cy="80" r="70" fill="#fbe4e8"/>
            <path d="M80 115s-32-19-32-42a18 18 0 0 1 32-11 18 18 0 0 1 32 11c0 23-32 42-32 42z" fill="#e08e45"/>
          </svg>
        </div>
      </div>

      <div class="feature-row reverse">
        <div class="feature-text">
          <h2>Why should you have one?</h2>
          <p>They can increase opportunities to exercise, get outside, and socialize. Regular walking or playing with pets can decrease blood pressure, cholesterol levels, and triglyceride levels. Pets can help manage loneliness and depression by giving us companionship.</p>
        </div>
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
      </div>

      <div class="feature-row">
        <div class="feature-text">
          <h2>Don't skip spending time with your dog</h2>
          <p>If there's one thing your dog looks forward to every day, it's that time when they get to go out and let loose with you — playtime. Beyond seeing our beloved pups just having fun outside and enjoying themselves, there are a lot of benefits to playing with them.</p>
        </div>
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <circle cx="80" cy="80" r="70" fill="#fdf0dd"/>
            <circle cx="80" cy="80" r="30" fill="none" stroke="#e08e45" stroke-width="5"/>
            <path d="M80 50v60M50 80h60M60 60l40 40M100 60L60 100" stroke="#e08e45" stroke-width="3"/>
          </svg>
        </div>
      </div>

      <div class="tip-grid">
        <div class="tip-card card">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9a2 2 0 1 1 3.3-1.5l6.2 6.2A2 2 0 1 1 15 17l-6.2-6.2A2 2 0 0 1 4 9zm16 6a2 2 0 1 1-3.3 1.5l-6.2-6.2A2 2 0 1 1 9 7l6.2 6.2A2 2 0 0 1 20 15z"/></svg>
          <h4>Dog grooming tips</h4>
          <p>For long-haired pooches, set up a daily grooming routine to remove tangles and prevent mats. Gently tease out tangles with a slicker brush, then a bristle brush.</p>
        </div>
        <div class="tip-card card">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11h18a9 9 0 0 1-18 0z"/><path d="M7 11V8a5 5 0 0 1 10 0v3"/></svg>
          <h4>Dog nutrition tip</h4>
          <p>The best dog food for your companion should meet their nutritional needs — not every dog has exactly the same requirements, so tailor it to yours.</p>
        </div>
        <div class="tip-card card">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.4 7 .8-5.2 4.8 1.5 6.9L12 17.6 5.8 20.9l1.5-6.9L2.1 9.2l7-.8L12 2z"/></svg>
          <h4>Essential tip</h4>
          <p>If you're wondering how to train a dog with a specific behavior, give them treats, praise, or affection — whatever motivates them most works best.</p>
        </div>
      </div>

      <div class="stats-row">
        <div>
          <div class="stat-number">+12k</div>
          <div class="stat-label">Dog related queries</div>
        </div>
        <div>
          <div class="stat-number">84</div>
          <div class="stat-label">Dogs matched</div>
        </div>
        <div>
          <div class="stat-number">307</div>
          <div class="stat-label">Breeds explored</div>
        </div>
        <div>
          <div class="stat-number">24h</div>
          <div class="stat-label">Service</div>
        </div>
      </div>
    </div>

    <div class="cta-band">
      <h2>Ready to get started?</h2>
      <a class="btn btn-primary" href="/form">Get a Dog</a>
    </div>

    <div class="cta-band">
      <h2>Send your Feedback</h2>
      <p>New dog alerts, discounts and free training lessons</p>
      <form class="feedback-form" onsubmit="return false;">
        <input type="email" placeholder="Enter your email" required/>
        <button type="submit" class="btn btn-primary">Subscribe</button>
      </form>
    </div>

    <footer class="site-footer">
      <span class="wordmark">&#128062; NaiKutty</span>
      <p>Helping you find the right dog for your life. Made with love for dogs everywhere.</p>
    </footer>
  </body>
</html>
```

- [ ] **Step 2: Run the full test suite**

```bash
.venv/Scripts/python manage.py test Main_Api -v 2
```

Expected: all 7 tests still `OK` (Home.html isn't covered by a dedicated test, but this confirms nothing else broke).

- [ ] **Step 3: Commit**

```bash
git add Main_Api/templates/Myforms/Home.html
git commit -m "style: rebuild the homepage without the Webflow dependency"
```

---

### Task 6: Manual end-to-end visual verification

**Files:** none (verification only)

- [ ] **Step 1: Collect static files**

```bash
.venv/Scripts/python manage.py collectstatic --noinput
```

Expected: completes without error, includes `Main_Api/css/base.css` in the copied files.

- [ ] **Step 2: Start the dev server and check all three pages in a browser**

```bash
.venv/Scripts/python manage.py runserver
```

Visit `/`: confirm the hero, feature rows, tip cards, stats, and footer all render with the new fonts/colors and no broken images or dead links. Click "Find a Dog" → confirm the form renders as a styled card. Submit it → confirm Result.html renders with the group as a pill and breed cards showing tag-pill temperament traits. Click "Try again" → back to the form.

- [ ] **Step 3: Run the full test suite one final time**

```bash
.venv/Scripts/python manage.py test
```

Expected: all tests `OK`.

- [ ] **Step 4: Commit any final fixups**

If manual verification surfaces a visual bug, fix it and commit:

```bash
git add -A
git commit -m "fix: address visual issues found in manual verification"
```
