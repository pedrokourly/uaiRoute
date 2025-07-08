from rest_framework import serializers
from django.contrib.auth.hashers import make_password
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

    def create(self, validated_data):
        """Criptografa a senha ao criar um funcionário"""
        if 'senha' in validated_data:
            validated_data['senha'] = make_password(validated_data['senha'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Criptografa a senha ao atualizar um funcionário, apenas se uma nova senha foi fornecida"""
        if 'senha' in validated_data and validated_data['senha']:
            validated_data['senha'] = make_password(validated_data['senha'])
        elif 'senha' in validated_data and not validated_data['senha']:
            # Se o campo senha está vazio, remove do validated_data para não alterar a senha atual
            validated_data.pop('senha', None)
        return super().update(instance, validated_data)
