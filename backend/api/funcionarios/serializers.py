from rest_framework import serializers
from .models import Funcionario

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'

    def validate_alojamento(self, alojamento):
        if alojamento and alojamento.vagas_disponiveis() <= 0:
            raise serializers.ValidationError(f"O alojamento '{alojamento.nome}' está lotado.")
        return alojamento
