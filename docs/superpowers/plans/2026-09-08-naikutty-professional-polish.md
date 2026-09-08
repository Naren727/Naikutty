# Naikutty "Professional Playful" Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade all 3 templates to the validated "Modern SaaS Playful" look (gradient mesh background, floating glass nav, gradient buttons, glow-shadow photos, bento-style stats) per `docs/superpowers/specs/2026-09-08-naikutty-professional-polish-design.md`.

**Architecture:** New design tokens and shared component rules (nav, buttons, hover-lift) go into `base.css` first since every template depends on them. Then each template is updated to use the new nav, and Home's hero/body sections get their bento/glow treatment.

**Tech Stack:** Plain CSS only (gradients, `backdrop-filter`, `filter: drop-shadow`, CSS transitions) — no JS, no new dependencies.

## Global Constraints

- Templates/CSS only — no changes to `views.py`, `models.py`, `forms.py`, or any Python logic.
- All 10 existing tests must keep passing unchanged (they assert template names/context, not markup).
- Exact token values below are taken from the validated mockup — don't substitute different colors/gradients.

---

### Task 1: Sitewide design tokens, glass nav, gradient buttons, hover-lift

**Files:**
- Modify: `Main_Api/static/Main_Api/css/base.css`

**Interfaces:**
- Produces: `--gradient-primary`, `--gradient-accent`, `--shadow-glow-primary`, `--shadow-glow-accent`, `--shadow-lift`, `--glass-bg`, `--glass-border` custom properties, and the restyled `.site-nav`/`.btn-primary`/`.btn-secondary`/`.tip-card`/`.breed-card` rules — consumed by every later task.

- [ ] **Step 1: Add new tokens**

In `Main_Api/static/Main_Api/css/base.css`, add to the `:root` block (after `--font-body: 'Nunito', sans-serif;`):

```css
  --gradient-primary: linear-gradient(135deg, #8ebf42, #6e9a2f);
  --gradient-accent: linear-gradient(135deg, #f4a261, #e08e45);
  --shadow-glow-primary: 0 12px 28px -8px rgba(110, 154, 47, 0.55);
  --shadow-glow-accent: 0 12px 28px -8px rgba(224, 142, 69, 0.5);
  --shadow-lift: 0 18px 34px -12px rgba(0, 0, 0, 0.18);
  --glass-bg: rgba(255, 255, 255, 0.65);
  --glass-border: rgba(255, 255, 255, 0.9);
```

- [ ] **Step 2: Deepen the shared card shadow and add the gradient mesh body background**

Replace:

```css
  --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.06);
```

with:

```css
  --shadow-card: 0 8px 28px rgba(0, 0, 0, 0.08);
```

Replace the `body` rule:

```css
body {
  margin: 0;
  background: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-body);
  line-height: 1.6;
}
```

with:

```css
body {
  margin: 0;
  background:
    radial-gradient(ellipse 900px 600px at 10% -5%, rgba(142, 191, 66, 0.14), transparent 60%),
    radial-gradient(ellipse 800px 600px at 100% 10%, rgba(224, 142, 69, 0.16), transparent 55%),
    radial-gradient(ellipse 700px 500px at 15% 100%, rgba(142, 191, 66, 0.08), transparent 60%),
    var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-body);
  line-height: 1.6;
}
```

- [ ] **Step 3: Tighten heading letter-spacing**

Replace:

```css
h1, h2, h3, h4 {
  font-family: var(--font-heading);
  color: var(--color-text);
  margin: 0 0 0.5em;
}
```

with:

```css
h1, h2, h3, h4 {
  font-family: var(--font-heading);
  color: var(--color-text);
  margin: 0 0 0.5em;
  letter-spacing: -0.3px;
}
```

- [ ] **Step 4: Rebuild `.site-nav` as a floating glass pill**

Replace:

```css
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
```

with:

```css
/* Nav */
.site-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 22px;
  max-width: 900px;
  margin: 18px auto 0;
  background: var(--glass-bg);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--glass-border);
  border-radius: 999px;
  box-shadow: 0 8px 30px -10px rgba(58, 58, 58, 0.18);
}
.site-nav .wordmark {
  font-family: var(--font-heading);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-primary-dark);
}
.site-nav .nav-links { display: flex; gap: 24px; }
.site-nav .nav-links a { font-weight: 600; color: var(--color-text); }
.site-nav .nav-links a:hover { color: var(--color-primary-dark); }
```

- [ ] **Step 5: Gradient/ghost buttons with hover-lift**

Replace:

```css
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
```

with:

```css
/* Buttons */
.btn {
  display: inline-block;
  padding: 12px 28px;
  border-radius: 999px;
  font-family: var(--font-heading);
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  border: 1.5px solid transparent;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}
.btn-primary { background: var(--gradient-primary); color: #fff; box-shadow: var(--shadow-glow-primary); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 16px 34px -8px rgba(110, 154, 47, 0.65); }
.btn-secondary {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border-color: rgba(58, 58, 58, 0.15);
  color: var(--color-primary-dark);
}
.btn-secondary:hover { background: #fff; border-color: var(--color-primary); transform: translateY(-2px); }
```

- [ ] **Step 6: Hover-lift for tip cards and breed cards**

Add after the `.tag-primary { background: var(--color-primary); }` rule:

```css
.tip-card, .breed-card {
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.tip-card:hover, .breed-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lift);
}
```

- [ ] **Step 7: Verify no syntax errors**

```bash
.venv/Scripts/python manage.py collectstatic --noinput
```

Expected: completes without error.

- [ ] **Step 8: Commit**

```bash
git add Main_Api/static/Main_Api/css/base.css
git commit -m "style: add gradient-mesh tokens, glass nav, gradient buttons, hover-lift"
```

---

### Task 2: Home hero rebuild

**Files:**
- Modify: `Main_Api/templates/Myforms/Home.html` (nav + hero sections)
- Modify: `Main_Api/static/Main_Api/css/base.css` (hero-specific rules)

**Interfaces:**
- Consumes: tokens from Task 1.

- [ ] **Step 1: Make the nav wordmark a link (Home only needs this change to the nav markup)**

In `Main_Api/templates/Myforms/Home.html`, replace:

```html
    <nav class="site-nav">
      <span class="wordmark">&#128062; NaiKutty</span>
      <div class="nav-links">
```

with:

```html
    <nav class="site-nav">
      <a class="wordmark" href="/">&#128062; NaiKutty</a>
      <div class="nav-links">
```

- [ ] **Step 2: Rebuild the hero markup**

Replace the entire hero `<div>` block:

```html
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
```

with:

```html
    <div class="hero">
      <div class="hero-glow"></div>
      <span class="eyebrow">&#128062; Free &middot; Takes 30 seconds</span>
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
      <h1>Pick out your <span class="gradient-text">furry friend</span> today</h1>
      <p class="subhead">Answer five quick questions and we'll match you with a breed group that actually fits your life.</p>
      <div class="hero-btns">
        <a class="btn btn-primary" href="/form">Get a Dog</a>
        <a class="btn btn-secondary" href="#about">See how it works</a>
      </div>
    </div>
```

- [ ] **Step 3: Add the hero-specific CSS**

In `Main_Api/static/Main_Api/css/base.css`, replace:

```css
/* Hero (Home) */
.hero { text-align: center; padding: 60px 24px 40px; }
.hero .illustration { max-width: 220px; margin: 0 auto 24px; display: block; }
.hero h1 { font-size: 42px; }
.hero p.subhead { font-size: 18px; color: var(--color-text-muted); margin-bottom: 28px; }
```

with:

```css
/* Hero (Home) */
.hero { position: relative; text-align: center; padding: 60px 24px 40px; overflow: hidden; }
.hero-glow {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  width: 380px;
  height: 380px;
  background: radial-gradient(circle, rgba(142, 191, 66, 0.28) 0%, rgba(224, 142, 69, 0.18) 55%, transparent 75%);
  filter: blur(10px);
  z-index: 0;
  pointer-events: none;
}
.hero .eyebrow,
.hero .illustration,
.hero h1,
.hero p,
.hero-btns { position: relative; z-index: 1; }
.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(142, 191, 66, 0.35);
  padding: 6px 16px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 800;
  color: var(--color-primary-dark);
  margin-bottom: 18px;
  box-shadow: 0 4px 14px -6px rgba(0, 0, 0, 0.12);
}
.hero .illustration { max-width: 220px; margin: 0 auto 24px; display: block; }
.hero h1 { font-size: 44px; }
.gradient-text {
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.hero p.subhead { font-size: 18px; color: var(--color-text-muted); max-width: 480px; margin: 0 auto 28px; }
.hero-btns { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
```

- [ ] **Step 4: Run the tests**

```bash
.venv/Scripts/python manage.py test Main_Api -v 1
```

Expected: all 10 tests `OK`.

- [ ] **Step 5: Commit**

```bash
git add Main_Api/templates/Myforms/Home.html Main_Api/static/Main_Api/css/base.css
git commit -m "style: rebuild the homepage hero with gradient text, glow, and eyebrow badge"
```

---

### Task 3: Home body sections — glow photos, 4th row photo, tip icons, bento stats, glass CTA

**Files:**
- Modify: `Main_Api/templates/Myforms/Home.html`
- Modify: `Main_Api/static/Main_Api/css/base.css`

- [ ] **Step 1: Give the "When are you getting your dog?" row a real photo**

Replace:

```html
      <div class="feature-illustration">
        <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
          <circle cx="80" cy="80" r="70" fill="#f0e4d0"/>
          <g fill="none" stroke="#8ebf42" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="80" cy="60" r="22"/>
            <path d="M45 120c5-25 22-38 35-38s30 13 35 38"/>
          </g>
        </svg>
      </div>
```

with:

```html
      <div class="feature-illustration glow-primary">
        <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
          <defs><clipPath id="photoClip0"><circle cx="80" cy="80" r="64"/></clipPath></defs>
          <circle cx="80" cy="80" r="70" fill="#f0e4d0"/>
          <image href="https://images.dog.ceo/breeds/labrador/pic1_l.jpg" x="16" y="16" width="128" height="128" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip0)"/>
        </svg>
      </div>
```

- [ ] **Step 2: Add glow classes to the other 3 feature-illustration divs**

Add `glow-accent` or `glow-primary` to each `<div class="feature-illustration">` under `id="features"` (there are 3, one per row). Change:

```html
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <defs><clipPath id="photoClip1">
```

to:

```html
        <div class="feature-illustration glow-accent">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <defs><clipPath id="photoClip1">
```

Change:

```html
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <defs><clipPath id="photoClip2">
```

to:

```html
        <div class="feature-illustration glow-primary">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <defs><clipPath id="photoClip2">
```

Change:

```html
        <div class="feature-illustration">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <defs><clipPath id="photoClip3">
```

to:

```html
        <div class="feature-illustration glow-accent">
          <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
            <defs><clipPath id="photoClip3">
```

- [ ] **Step 3: Add glow CSS and update the feature-illustration base rule**

In `base.css`, replace:

```css
/* Feature rows (Home) */
.feature-row { display: flex; align-items: center; gap: 48px; padding: 48px 0; max-width: 960px; margin: 0 auto; }
.feature-row.reverse { flex-direction: row-reverse; }
.feature-row .feature-text { flex: 1; }
.feature-row .feature-illustration { flex: 1; text-align: center; }
.feature-row .feature-illustration svg { max-width: 320px; width: 100%; height: auto; }
```

with:

```css
/* Feature rows (Home) */
.feature-row { display: flex; align-items: center; gap: 48px; padding: 48px 0; max-width: 960px; margin: 0 auto; }
.feature-row.reverse { flex-direction: row-reverse; }
.feature-row .feature-text { flex: 1; }
.feature-row .feature-illustration { flex: 1; text-align: center; }
.feature-row .feature-illustration svg { max-width: 320px; width: 100%; height: auto; }
.feature-illustration.glow-primary svg { filter: drop-shadow(0 20px 36px rgba(110, 154, 47, 0.35)); }
.feature-illustration.glow-accent svg { filter: drop-shadow(0 20px 36px rgba(224, 142, 69, 0.35)); }
```

- [ ] **Step 4: Colored icon circles on tip cards**

Replace the 3 tip cards:

```html
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
```

with:

```html
      <div class="tip-grid">
        <div class="tip-card card">
          <div class="tip-icon tip-icon-primary"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9a2 2 0 1 1 3.3-1.5l6.2 6.2A2 2 0 1 1 15 17l-6.2-6.2A2 2 0 0 1 4 9zm16 6a2 2 0 1 1-3.3 1.5l-6.2-6.2A2 2 0 1 1 9 7l6.2 6.2A2 2 0 0 1 20 15z"/></svg></div>
          <h4>Dog grooming tips</h4>
          <p>For long-haired pooches, set up a daily grooming routine to remove tangles and prevent mats. Gently tease out tangles with a slicker brush, then a bristle brush.</p>
        </div>
        <div class="tip-card card">
          <div class="tip-icon tip-icon-accent"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11h18a9 9 0 0 1-18 0z"/><path d="M7 11V8a5 5 0 0 1 10 0v3"/></svg></div>
          <h4>Dog nutrition tip</h4>
          <p>The best dog food for your companion should meet their nutritional needs — not every dog has exactly the same requirements, so tailor it to yours.</p>
        </div>
        <div class="tip-card card">
          <div class="tip-icon tip-icon-primary"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.9 6.4 7 .8-5.2 4.8 1.5 6.9L12 17.6 5.8 20.9l1.5-6.9L2.1 9.2l7-.8L12 2z"/></svg></div>
          <h4>Essential tip</h4>
          <p>If you're wondering how to train a dog with a specific behavior, give them treats, praise, or affection — whatever motivates them most works best.</p>
        </div>
      </div>
```

In `base.css`, replace:

```css
/* Tip cards (Home) */
.tip-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; max-width: 960px; margin: 0 auto; padding: 24px 24px 48px; }
.tip-card { text-align: center; padding: 24px; }
.tip-card svg { width: 48px; height: 48px; margin-bottom: 12px; color: var(--color-primary); }
```

with:

```css
/* Tip cards (Home) */
.tip-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; max-width: 960px; margin: 0 auto; padding: 24px 24px 48px; }
.tip-card { text-align: center; padding: 24px; }
.tip-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
  color: var(--color-primary-dark);
}
.tip-icon-primary { background: linear-gradient(135deg, rgba(142, 191, 66, 0.18), rgba(142, 191, 66, 0.32)); }
.tip-icon-accent { background: linear-gradient(135deg, rgba(224, 142, 69, 0.18), rgba(224, 142, 69, 0.32)); }
.tip-icon svg { width: 28px; height: 28px; }
```

- [ ] **Step 5: Bento-style stats strip**

Replace:

```html
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
```

with:

```html
      <div class="stats-row">
        <div class="stat-cell stat-gradient">
          <div class="stat-number">+12k</div>
          <div class="stat-label">Dog related queries</div>
        </div>
        <div class="stat-cell stat-glass">
          <div class="stat-number">84</div>
          <div class="stat-label">Dogs matched</div>
        </div>
        <div class="stat-cell stat-glass">
          <div class="stat-number">307</div>
          <div class="stat-label">Breeds explored</div>
        </div>
        <div class="stat-cell stat-gradient-accent">
          <div class="stat-number">24h</div>
          <div class="stat-label">Service</div>
        </div>
      </div>
```

In `base.css`, replace:

```css
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
```

with:

```css
/* Stats (Home) */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin: 24px auto 48px;
  max-width: 960px;
  text-align: center;
}
.stat-cell { border-radius: var(--radius-md); padding: 24px 16px; }
.stat-cell .stat-number { font-family: var(--font-heading); font-size: 28px; font-weight: 700; }
.stat-cell .stat-label { font-size: 13px; }
.stat-gradient { background: var(--gradient-primary); color: #fff; box-shadow: var(--shadow-glow-primary); }
.stat-gradient-accent { background: var(--gradient-accent); color: #fff; box-shadow: var(--shadow-glow-accent); }
.stat-gradient .stat-label, .stat-gradient-accent .stat-label { opacity: 0.92; }
.stat-glass {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  box-shadow: 0 10px 24px -12px rgba(0, 0, 0, 0.12);
}
.stat-glass .stat-number { color: var(--color-primary-dark); }
.stat-glass .stat-label { color: var(--color-text-muted); }
```

- [ ] **Step 6: Glass CTA/feedback bands**

In `base.css`, replace:

```css
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
```

with:

```css
/* CTA band (Home) */
.cta-band {
  text-align: center;
  background: var(--glass-bg);
  backdrop-filter: blur(14px);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: 0 10px 30px -14px rgba(0, 0, 0, 0.12);
  padding: 48px 24px;
  margin: 24px auto;
  max-width: 960px;
}
```

- [ ] **Step 7: Run the tests**

```bash
.venv/Scripts/python manage.py test Main_Api -v 1
```

Expected: all 10 tests `OK`.

- [ ] **Step 8: Commit**

```bash
git add Main_Api/templates/Myforms/Home.html Main_Api/static/Main_Api/css/base.css
git commit -m "style: bento-style stats, glow photos on all 4 rows, colored tip icons, glass CTA bands"
```

---

### Task 4: DogForm page — glass nav

**Files:**
- Modify: `Main_Api/templates/Myforms/DogForm.html`
- Modify: `Main_Api/static/Main_Api/css/base.css`

- [ ] **Step 1: Replace the back-link with the glass nav**

Replace:

```html
    <div class="form-page">
      <a class="back-link" href="/">&larr; NaiKutty</a>
      <div class="card">
```

with:

```html
    <nav class="site-nav">
      <a class="wordmark" href="/">&#128062; NaiKutty</a>
    </nav>
    <div class="form-page">
      <div class="card">
```

- [ ] **Step 2: Tighten the page's top margin now that the nav adds its own spacing**

In `base.css`, replace:

```css
/* Form card (DogForm) */
.form-page { max-width: 520px; margin: 40px auto; padding: 0 24px; }
.form-page .back-link { display: inline-block; margin-bottom: 20px; font-weight: 600; }
.form-page p.intro { color: var(--color-text-muted); margin-top: -8px; }
```

with:

```css
/* Form card (DogForm) */
.form-page { max-width: 520px; margin: 32px auto 40px; padding: 0 24px; }
.form-page p.intro { color: var(--color-text-muted); margin-top: -8px; }
```

- [ ] **Step 3: Run the tests**

```bash
.venv/Scripts/python manage.py test Main_Api -v 1
```

Expected: all 10 tests `OK` (the GET test only checks status code + template, unaffected by this markup change).

- [ ] **Step 4: Commit**

```bash
git add Main_Api/templates/Myforms/DogForm.html Main_Api/static/Main_Api/css/base.css
git commit -m "style: give the dog form page the shared glass nav"
```

---

### Task 5: Result page — glass nav, gradient tag, glow photo frames

**Files:**
- Modify: `Main_Api/templates/Myforms/Result.html`
- Modify: `Main_Api/static/Main_Api/css/base.css`

- [ ] **Step 1: Replace the back-link with the glass nav**

Replace:

```html
    <div class="result-page">
      <a class="back-link" href="/">&larr; NaiKutty</a>
      <h1>Thanks, {{ name }}!</h1>
```

with:

```html
    <nav class="site-nav">
      <a class="wordmark" href="/">&#128062; NaiKutty</a>
    </nav>
    <div class="result-page">
      <h1>Thanks, {{ name }}!</h1>
```

- [ ] **Step 2: Gradient group tag, glow photo frames, tightened top margin**

In `base.css`, replace:

```css
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
```

with:

```css
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
.tag-primary { background: var(--gradient-primary); }
```

Replace:

```css
/* Result page */
.result-page { max-width: 640px; margin: 40px auto; padding: 0 24px; }
.result-page .back-link { display: inline-block; margin-bottom: 20px; font-weight: 600; }
.result-page .group-callout { margin: 12px 0 28px; }
.result-page .group-callout .tag { font-size: 16px; padding: 8px 20px; }
.breed-card { display: flex; gap: 16px; margin-bottom: 16px; }
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
```

with:

```css
/* Result page */
.result-page { max-width: 640px; margin: 32px auto 40px; padding: 0 24px; }
.result-page .group-callout { margin: 12px 0 28px; }
.result-page .group-callout .tag { font-size: 16px; padding: 8px 20px; }
.breed-card { display: flex; gap: 16px; margin-bottom: 16px; }
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
  font-size: 24px;
  box-shadow: 0 8px 18px -4px rgba(224, 142, 69, 0.45);
}
```

- [ ] **Step 3: Run the tests**

```bash
.venv/Scripts/python manage.py test Main_Api -v 1
```

Expected: all 10 tests `OK`.

- [ ] **Step 4: Commit**

```bash
git add Main_Api/templates/Myforms/Result.html Main_Api/static/Main_Api/css/base.css
git commit -m "style: give the results page the shared glass nav, gradient tag, and glow photo frames"
```

---

### Task 6: Manual verification across pages and breakpoints

**Files:** none (verification only)

- [ ] **Step 1: Start the dev server and check all 3 pages**

```bash
.venv/Scripts/python manage.py runserver
```

Load `/`, `/form/`, and submit the form to reach the result page. Confirm: the floating glass nav renders consistently on all 3 pages, the mesh background is visible but doesn't hurt text readability, hero gradient-text and eyebrow badge render, all 4 homepage feature rows now show real photos with a colored glow (no more abstract icon), tip card icons sit in colored circles, the stats row shows the gradient/glass bento mix, hovering tip cards and breed cards lifts them, and the group tag on the result page is a gradient pill.

- [ ] **Step 2: Check the responsive breakpoints**

Resize through ~1280px, 1024px, 768px, 640px, and 375px. Confirm the floating nav still looks like a pill (not a squished bar) at every width, including when Home's nav links wrap on narrow screens, and that there's no horizontal overflow anywhere.

- [ ] **Step 3: Run the full test suite one final time**

```bash
.venv/Scripts/python manage.py test
```

Expected: all tests `OK`.

- [ ] **Step 4: Commit any fixups**

```bash
git add -A
git commit -m "fix: address issues found in manual verification"
```
