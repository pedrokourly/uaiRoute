from rest_framework import serializers
from .models import Funcionario

class FuncionarioSerializer(serializers.ModelSerializer):
    rua = serializers.CharField(source='alojamento.rua', read_only=True)
    numero = serializers.CharField(source='alojamento.numero', read_only=True)
    bairro = serializers.CharField(source='alojamento.bairro', read_only=True)
    cidade = serializers.CharField(source='alojamento.cidade', read_only=True)

    class Meta:
        model = Funcionario
        fields = [
            'id', 'nome_completo', 'cargo', 'email', 'senha',
            'is_admin', 'alojamento',
            'rua', 'numero', 'bairro', 'cidade'  # ✅ endereço do alojamento
        ]

    def validate_alojamento(self, alojamento):
        if alojamento and alojamento.vagas_disponiveis() <= 0:
            raise serializers.ValidationError(f"O alojamento '{alojamento.nome}' está lotado.")
        return alojamento
