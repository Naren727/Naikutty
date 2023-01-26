import pandas as pd
from pandas import DataFrame
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Main_Model
from .serializers import Main_ModelSerializers
from .forms import Userforms
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import numpy as np
import pickle
import joblib
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.contrib import messages
import sklearn

# Create your views here.
class Main_ModelViews(viewsets.ModelViewSet):
    queryset = Main_Model.objects.all()
    serializer_class = Main_ModelSerializers


def home(request):
    return render(request, "Myforms/Home.html")


def label_Encode(array):
    gfc_switcher = {
        "2-3 Times a Week Brushing": 0, "Daily Brushing": 1, "Occasional Bath/Brush": 2, "Specialty/Professional": 3,
        "Weekly Brushing": 4
    }
    sc_switcher = {
        "Frequent": 0, " Infrequent": 1, "Occasional": 2, "Regularly": 3, "Seasonal": 4
    }
    elc_switcher = {
        "Calm": 0, "Couch Potato": 1, "Energetic": 2, "Needs Lots of Activity": 3, "Regular Exercise": 4
    }
    tc_switcher = {
        "Agreeable": 0, "Eager to Please": 1, "Easy Training": 2, "Independent": 3, "May be Stubborn": 4
    }
    dc_switcher = {
        "Alert/Responsive": 0, " Aloof/Wary": 1, "Friendly": 2, "Outgoing": 3, "Reserved with Strangers": 4
    }
    gfc = gfc_switcher.get(array[0], 0)
    sc = sc_switcher.get(array[1], 0)
    elc = elc_switcher.get(array[2], 0)
    tc = tc_switcher.get(array[3], 0)
    dc = dc_switcher.get(array[4], 0)
    new_dict = np.array(gfc, sc, elc, tc, dc)
    return new_dict


@api_view(["POST"])
def Uform(request):
    if request.method == "POST":
        form = Userforms(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            gfc = form.cleaned_data['gfc']
            sc = form.cleaned_data['sc']
            elc = form.cleaned_data['elc']
            tc = form.cleaned_data['tc']
            dc = form.cleaned_data['dc']
            tempdict = (name, gfc, sc, elc, tc, dc)
            df = pd.DataFrame(tempdict)
            Dogselect(df)

    form = Userforms()
    return render(request, 'Myforms/DogForm.html', {'form': form})


def Dogselect(request):
    try:
        model = joblib.load('dog.pkl')
        userdata = request.data
        dict = np.array(list(userdata.values()))
        label_Encode(dict)
        dict = dict.reshape(1, -1)
        pred = model.predict(dict)
        print(request.data)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


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
