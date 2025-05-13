from rest_framework import serializers
from .models import Obra

class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra
        fields = ['id', 'nome', 'rua', 'numero', 'bairro', 'cidade']
