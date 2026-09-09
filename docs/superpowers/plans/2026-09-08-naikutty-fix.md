# Naikutty Fix & Hosting-Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Naikutty (a Django dog-breed recommendation app) actually run end-to-end — form loads, prediction pipeline executes without crashing, a result is shown to the user — and get it into a hostable state (no hardcoded secrets/paths, dependencies declared, deploy config present).

**Architecture:** Existing Django 4.0-era project (`Naikutty/` project package + `Main_Api` app) is kept as-is structurally. We fix the three real bugs blocking the pipeline (serializer typo, broken feature-encoding call, view never returning a result), make file loading and settings environment-relative instead of hardcoded, add a results template, and add the deployment/dependency scaffolding that never existed (`requirements.txt`, `Procfile`, `.gitignore`, whitenoise for static files).

**Tech Stack:** Django 5.0.x, djangorestframework, pandas, scikit-learn (LogisticRegression, already trained and pickled in `dog.pkl`), joblib, whitenoise + gunicorn for deploy.

## Global Constraints

- Keep the existing DB model (`Main_Model`) and its DRF viewset (`Main_ModelViews`/`UserList`) — they store form submissions to SQLite and are working functionality, not part of the bug list.
- `dog.pkl` is a `LogisticRegression` with `n_features_in_=5` and `feature_names_in_ = ['grooming_frequency_category', 'shedding_category', 'energy_level_category', 'trainability_category', 'demeanor_category']` (verified by loading it directly). Feature order in any new code MUST match this exactly.
- The repo has no training script, so the exact label-encoding scheme used when the model was originally fit cannot be recovered with certainty. Empirically, neither an alphabetically-sorted-group class mapping nor the raw `*_value` columns from `dog.csv` reproduce high accuracy against the model (tested: 24% and 11% respectively, both heavily skewed to one class) — this model was a weak student-project classifier, not a bug we can "fix" by encoding differently. We will treat the predicted class index as a best-effort pointer into the alphabetically-sorted list of the 9 unique `group` values in `dog.csv` (the standard behavior of `sklearn.LabelEncoder`/`pd.factorize`, and the most defensible default absent the original training code), and clearly this is a best-effort mapping, not a verified one.
- `popularity` in `dog.csv` is stored as a string/object column ("1", "10", "100" sort lexicographically) — must be cast to `int` before sorting.
- Do not commit `db.sqlite3`, `__pycache__/`, or a virtualenv to git.

---

### Task 1: Dependencies, serializer fix, and settings hardening

**Files:**
- Create: `requirements.txt`
- Create: `.venv/` (local virtualenv, not committed)
- Modify: `Main_Api/serializers.py`
- Modify: `Naikutty/settings.py`
- Modify: `.gitignore` (create if needed — only `.idea/.gitignore` exists today)

**Interfaces:**
- Produces: a working `python manage.py check` and `python manage.py test` from a clean venv, which every later task assumes.

- [ ] **Step 1: Create a virtualenv and install current dependencies**

```bash
cd Naikutty
python -m venv .venv
.venv/Scripts/pip install django djangorestframework pandas numpy scikit-learn joblib whitenoise gunicorn
```

- [ ] **Step 2: Freeze exact versions into requirements.txt**

```bash
.venv/Scripts/pip freeze > requirements.txt
```

- [ ] **Step 3: Fix the serializer typo**

In `Main_Api/serializers.py`, line 8:

```python
class Main_ModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Main_Model
        fields = '__all__'
```

- [ ] **Step 4: Harden settings.py for env-based config**

Replace lines 22-28 of `Naikutty/settings.py`:

```python
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-+41-&4v3^(3r+j)fha56orz#$@=ak+@$dmf#2k(5zyc@enl86d',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [h for h in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') if h]
if DEBUG:
    ALLOWED_HOSTS += ['localhost', '127.0.0.1']
```

Add whitenoise to `MIDDLEWARE` (right after `SecurityMiddleware`, i.e. as the new second entry) and add static file storage config after `STATIC_URL = 'static/'`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

```python
STATIC_URL = 'static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

- [ ] **Step 5: Add .gitignore**

Create `.gitignore` at repo root:

```
.venv/
__pycache__/
*.pyc
db.sqlite3
staticfiles/
.env
```

- [ ] **Step 6: Verify the project boots**

```bash
.venv/Scripts/python manage.py check
```

Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .gitignore Main_Api/serializers.py Naikutty/settings.py
git commit -m "fix: install deps, fix serializer typo, harden settings for env config"
```

---

### Task 2: Fix the prediction pipeline (label encoding, feature order, model path)

**Files:**
- Modify: `Main_Api/views.py`
- Test: `Main_Api/tests.py`

**Interfaces:**
- Consumes: `dog.pkl` (`BASE_DIR / 'dog.pkl'`), `dog.csv` (`BASE_DIR / 'dog.csv'`).
- Produces: `encode_features(gfc, sc, elc, tc, dc) -> np.ndarray` (shape `(1, 5)`), `predict_group(features) -> str` (a value from `dog.csv`'s `group` column), `recommend_breeds(group, limit=5) -> list[dict]` (each dict has `Breed`, `description`, `temperament`, `group`). These are consumed by Task 3's view code and its results template.

- [ ] **Step 1: Write the failing tests**

Replace `Main_Api/tests.py`:

```python
from django.test import TestCase
from Main_Api.views import encode_features, predict_group, recommend_breeds, GROUPS


class EncodeFeaturesTests(TestCase):
    def test_returns_correct_shape(self):
        features = encode_features(
            "Daily Brushing", "Frequent", "Energetic", "Easy Training", "Friendly"
        )
        self.assertEqual(features.shape, (1, 5))

    def test_unknown_category_defaults_to_zero(self):
        features = encode_features("nonsense", "Frequent", "Energetic", "Easy Training", "Friendly")
        self.assertEqual(features[0][0], 0)


class PredictGroupTests(TestCase):
    def test_returns_one_of_the_known_groups(self):
        group = predict_group(
            encode_features("Daily Brushing", "Frequent", "Energetic", "Easy Training", "Friendly")
        )
        self.assertIn(group, GROUPS)


class RecommendBreedsTests(TestCase):
    def test_returns_breeds_from_requested_group(self):
        breeds = recommend_breeds("Toy Group", limit=3)
        self.assertLessEqual(len(breeds), 3)
        for breed in breeds:
            self.assertEqual(breed["group"], "Toy Group")
            self.assertIn("Breed", breed)
            self.assertIn("description", breed)

    def test_sorted_by_popularity_ascending(self):
        breeds = recommend_breeds("Sporting Group", limit=5)
        pops = [b["popularity"] for b in breeds]
        self.assertEqual(pops, sorted(pops))
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
.venv/Scripts/python manage.py test Main_Api -v 2
```

Expected: `ImportError: cannot import name 'encode_features'` (functions don't exist yet).

- [ ] **Step 3: Implement the fixed pipeline**

Replace lines 1-54 of `Main_Api/views.py` (imports through the end of `label_Encode`) with:

```python
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Main_Model
from .serializers import Main_ModelSerializers
from .forms import Userforms

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'dog.pkl'
DATA_PATH = BASE_DIR / 'dog.csv'

_model = joblib.load(MODEL_PATH)
_dog_df = pd.read_csv(DATA_PATH)
_dog_df['popularity'] = pd.to_numeric(_dog_df['popularity'], errors='coerce')
GROUPS = sorted(_dog_df['group'].dropna().unique())

GFC_SWITCHER = {
    "2-3 Times a Week Brushing": 0, "Daily Brushing": 1, "Occasional Bath/Brush": 2,
    "Specialty/Professional": 3, "Weekly Brushing": 4,
}
SC_SWITCHER = {
    "Frequent": 0, "Infrequent": 1, "Occasional": 2, "Regularly": 3, "Seasonal": 4,
}
ELC_SWITCHER = {
    "Calm": 0, "Couch Potato": 1, "Energetic": 2, "Needs Lots of Activity": 3, "Regular Exercise": 4,
}
TC_SWITCHER = {
    "Agreeable": 0, "Eager to Please": 1, "Easy Training": 2, "Independent": 3, "May be Stubborn": 4,
}
DC_SWITCHER = {
    "Alert/Responsive": 0, "Aloof/Wary": 1, "Friendly": 2, "Outgoing": 3, "Reserved with Strangers": 4,
}


def encode_features(gfc, sc, elc, tc, dc):
    """Encode the 5 form choices into the (1, 5) array dog.pkl expects.

    Feature order matches dog.pkl's feature_names_in_:
    grooming, shedding, energy, trainability, demeanor.
    """
    values = [
        GFC_SWITCHER.get(gfc, 0),
        SC_SWITCHER.get(sc, 0),
        ELC_SWITCHER.get(elc, 0),
        TC_SWITCHER.get(tc, 0),
        DC_SWITCHER.get(dc, 0),
    ]
    return np.array(values).reshape(1, -1)


def predict_group(features):
    """Map the model's predicted class index back to a group name.

    dog.pkl has no training script in this repo, so the exact label
    encoding it was fit with can't be recovered. We use the standard
    sklearn/pandas convention (classes sorted alphabetically) as the
    best-effort mapping.
    """
    class_index = int(_model.predict(features)[0])
    return GROUPS[class_index]


def recommend_breeds(group, limit=5):
    subset = _dog_df[_dog_df['group'] == group].sort_values('popularity')
    subset = subset.head(limit)
    columns = ['Breed', 'description', 'temperament', 'group', 'popularity']
    return subset[columns].to_dict('records')
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
.venv/Scripts/python manage.py test Main_Api -v 2
```

Expected: all 5 tests `OK`.

- [ ] **Step 5: Commit**

```bash
git add Main_Api/views.py Main_Api/tests.py
git commit -m "fix: repair broken feature encoding and add tested prediction pipeline"
```

---

### Task 3: Wire the view up to GET/POST and show a result

**Files:**
- Modify: `Main_Api/views.py` (the `Uform` view and `Dogselect`/old view code below `label_Encode`)
- Create: `Main_Api/templates/Myforms/Result.html`
- Test: `Main_Api/tests.py`

**Interfaces:**
- Consumes: `encode_features`, `predict_group`, `recommend_breeds` from Task 2.
- Produces: `Uform` view that renders `Myforms/DogForm.html` on GET and `Myforms/Result.html` on successful POST.

- [ ] **Step 1: Write the failing tests**

Append to `Main_Api/tests.py`:

```python
class UformViewTests(TestCase):
    def test_get_renders_the_form(self):
        response = self.client.get('/form/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Myforms/DogForm.html')

    def test_post_renders_a_recommendation(self):
        response = self.client.post('/form/', {
            'name': 'Test User',
            'gfc': 'Daily Brushing',
            'sc': 'Frequent',
            'elc': 'Energetic',
            'tc': 'Easy Training',
            'dc': 'Friendly',
            'xtra': 'none',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Myforms/Result.html')
        self.assertIn('group', response.context)
        self.assertIn('breeds', response.context)
        self.assertGreater(len(response.context['breeds']), 0)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
.venv/Scripts/python manage.py test Main_Api.tests.UformViewTests -v 2
```

Expected: FAIL — POST currently returns the empty form again (no `Result.html`, no `group`/`breeds` in context), and the view is `@api_view(["POST"])`-only so plain GET returns 405.

- [ ] **Step 3: Replace the view and drop the dead `Dogselect`/`label_Encode`-only code**

Replace the `@api_view(["POST"])` / `Uform` / `Dogselect` block in `Main_Api/views.py` (everything from the old `@api_view(["POST"])` line through the end of the old `Dogselect` function) with:

```python
def Uform(request):
    if request.method == "POST":
        form = Userforms(request.POST)
        if form.is_valid():
            features = encode_features(
                form.cleaned_data['gfc'],
                form.cleaned_data['sc'],
                form.cleaned_data['elc'],
                form.cleaned_data['tc'],
                form.cleaned_data['dc'],
            )
            group = predict_group(features)
            breeds = recommend_breeds(group)
            return render(request, 'Myforms/Result.html', {
                'name': form.cleaned_data['name'],
                'group': group,
                'breeds': breeds,
            })
    else:
        form = Userforms()
    return render(request, 'Myforms/DogForm.html', {'form': form})
```

Also delete the now-unused `class Main_ModelViews` duplication concern: leave `Main_ModelViews`/`UserList` at the bottom of the file untouched — they are separate, working functionality per the Global Constraints.

- [ ] **Step 4: Create the results template**

Create `Main_Api/templates/Myforms/Result.html`:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Your Dog Recommendation</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700" rel="stylesheet">
    <style>
      body { font-family: Roboto, Arial, sans-serif; color: #666; max-width: 700px; margin: 40px auto; padding: 0 20px; }
      h1 { color: #333; }
      .group-tag { display: inline-block; background: #8ebf42; color: #fff; padding: 4px 12px; border-radius: 12px; font-size: 14px; margin-bottom: 20px; }
      .breed-card { border: 1px solid #ddd; border-radius: 6px; padding: 16px; margin-bottom: 16px; }
      .breed-card h2 { margin: 0 0 6px 0; font-size: 20px; color: #333; }
      .temperament { color: #8ebf42; font-weight: 500; margin-bottom: 8px; }
      a.back-link { display: inline-block; margin-top: 20px; color: #8ebf42; }
    </style>
  </head>
  <body>
    <h1>Thanks, {{ name }}!</h1>
    <p>Based on your preferences, you're best matched with the:</p>
    <span class="group-tag">{{ group }}</span>
    <h3>Recommended breeds</h3>
    {% for breed in breeds %}
    <div class="breed-card">
      <h2>{{ breed.Breed }}</h2>
      <p class="temperament">{{ breed.temperament }}</p>
      <p>{{ breed.description|truncatewords:40 }}</p>
    </div>
    {% empty %}
    <p>No breeds found for this group.</p>
    {% endfor %}
    <a class="back-link" href="/form/">&larr; Try again</a>
  </body>
</html>
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
.venv/Scripts/python manage.py test Main_Api -v 2
```

Expected: all tests `OK`.

- [ ] **Step 6: Commit**

```bash
git add Main_Api/views.py Main_Api/templates/Myforms/Result.html Main_Api/tests.py
git commit -m "feat: render a real recommendation result instead of discarding it"
```

---

### Task 4: Deployment scaffolding and manual end-to-end verification

**Files:**
- Create: `Procfile`
- Create: `.env.example`
- Modify: `Naikutty/wsgi.py` (verify only, no change expected)

**Interfaces:**
- Consumes: everything from Tasks 1-3.
- Produces: a deployable app for Render/Railway (`web: gunicorn Naikutty.wsgi`).

- [ ] **Step 1: Add a Procfile for Render/Railway/Heroku-style hosts**

Create `Procfile`:

```
web: gunicorn Naikutty.wsgi --log-file -
release: python manage.py migrate
```

- [ ] **Step 2: Document required env vars**

Create `.env.example`:

```
DJANGO_SECRET_KEY=replace-with-a-long-random-string
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app.onrender.com
```

- [ ] **Step 3: Collect static files to confirm whitenoise config is valid**

```bash
.venv/Scripts/python manage.py collectstatic --noinput
```

Expected: completes without error, creates `staticfiles/`.

- [ ] **Step 4: Manual smoke test with runserver**

```bash
.venv/Scripts/python manage.py runserver
```

Then in a browser: visit `/`, click "Find a Dog" / "Get a Dog", submit the form, confirm a `Result.html` page renders with a group name and at least one breed card, and "Try again" returns to the form.

- [ ] **Step 5: Run the full test suite one more time**

```bash
.venv/Scripts/python manage.py test
```

Expected: all tests `OK`.

- [ ] **Step 6: Commit**

```bash
git add Procfile .env.example
git commit -m "chore: add deployment scaffolding (Procfile, env var docs)"
```
