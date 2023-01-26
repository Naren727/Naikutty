from rest_framework import serializers
from .models import Main_Model


class Main_ModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Main_Model
        fields = '_all_'
