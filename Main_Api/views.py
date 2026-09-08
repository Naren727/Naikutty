import re
import numpy as np
import pandas as pd
import joblib
import requests
from pathlib import Path
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
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
    cache_key = DOG_CEO_PHOTO_CACHE_PREFIX + re.sub(r'[^a-z0-9]+', '_', breed_name.lower())
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


FEATURE_COLUMNS = [
    'grooming_frequency_category', 'shedding_category', 'energy_level_category',
    'trainability_category', 'demeanor_category',
]


def encode_features(gfc, sc, elc, tc, dc):
    """Encode the 5 form choices into the 1-row DataFrame dog.pkl expects.

    Column names/order match dog.pkl's feature_names_in_ exactly, which
    avoids sklearn's "X does not have valid feature names" warning.
    """
    values = [[
        GFC_SWITCHER.get(gfc, 0),
        SC_SWITCHER.get(sc, 0),
        ELC_SWITCHER.get(elc, 0),
        TC_SWITCHER.get(tc, 0),
        DC_SWITCHER.get(dc, 0),
    ]]
    return pd.DataFrame(values, columns=FEATURE_COLUMNS)


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
    breeds = subset[columns].to_dict('records')
    for breed in breeds:
        breed['photo_url'] = breed_photo_url(breed['Breed'])
    return breeds


class Main_ModelViews(viewsets.ModelViewSet):
    queryset = Main_Model.objects.all()
    serializer_class = Main_ModelSerializers


def home(request):
    return render(request, "Myforms/Home.html")


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


class UserList(Main_ModelViews):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'head', 'post']

    def get(self, request, *args, **kwargs):
        serializer = Main_ModelSerializers(Main_Model.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        self.http_method_names.append("GET")
        serializer = Main_ModelSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
