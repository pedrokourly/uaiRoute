from rest_framework import serializers
from .models import Registro
from django.contrib.auth.hashers import make_password

class CadastroSerializer(serializers.ModelSerializer):
    confirmar_senha = serializers.CharField(write_only=True)
    is_admin = serializers.BooleanField(default=False)  # pode permitir o envio opcional

    class Meta:
        model = Registro
        fields = ['nome_completo', 'email', 'senha', 'confirmar_senha', 'is_admin']
        extra_kwargs = {
            'senha': {'write_only': True},
        }

    def validate(self, data):
        if data['senha'] != data['confirmar_senha']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirmar_senha')
        validated_data['senha'] = make_password(validated_data['senha'])
        return super().create(validated_data)
