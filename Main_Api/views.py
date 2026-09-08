import numpy as np
import pandas as pd
import joblib
from pathlib import Path
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
    return subset[columns].to_dict('records')


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
