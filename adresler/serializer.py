from rest_framework import serializers
from .models import Adresler

class AdreslerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Adresler
        fields = ['sehir', 'mahalle', 'sokak', 'bina', 'daire']
