from rest_framework import serializers
from .models import Alojamento

class AlojamentoSerializer(serializers.ModelSerializer):
    vagas_disponiveis = serializers.SerializerMethodField()

    class Meta:
        model = Alojamento
        fields = '__all__'

    def get_vagas_disponiveis(self, obj):
        return obj.vagas_disponiveis()
