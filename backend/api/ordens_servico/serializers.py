from rest_framework import serializers
from .models import OrdemServico, AlojamentoOrdemServico
from api.veiculos.serializers import VeiculoSerializer
from api.alojamento.serializers import AlojamentoSerializer
from api.obras.serializers import ObraSerializer

class AlojamentoOrdemServicoSerializer(serializers.ModelSerializer):
    alojamento = AlojamentoSerializer(read_only=True)
    alojamento_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = AlojamentoOrdemServico
        fields = ['alojamento', 'alojamento_id', 'ordem_parada']

class OrdemServicoSerializer(serializers.ModelSerializer):
    veiculo = VeiculoSerializer(read_only=True)
    obra_destino = ObraSerializer(read_only=True)
    alojamentos_paradas = AlojamentoOrdemServicoSerializer(many=True, read_only=True)
    
    # Campos para criação
    veiculo_id = serializers.IntegerField(write_only=True)
    obra_destino_id = serializers.IntegerField(write_only=True)
    alojamentos = serializers.ListField(
        child=serializers.DictField(), 
        write_only=True, 
        required=False
    )
    
    class Meta:
        model = OrdemServico
        fields = [
            'id', 'titulo', 'descricao', 'veiculo', 'obra_destino', 
            'status', 'data_criacao', 'data_inicio', 'data_conclusao', 
            'observacoes', 'distancia_total', 'tempo_estimado',
            'alojamentos_paradas', 'veiculo_id', 'obra_destino_id', 'alojamentos'
        ]
        read_only_fields = ['id', 'data_criacao']
    
    def create(self, validated_data):
        alojamentos_data = validated_data.pop('alojamentos', [])
        ordem_servico = OrdemServico.objects.create(**validated_data)
        
        # Criar relacionamentos com alojamentos
        for alojamento_data in alojamentos_data:
            AlojamentoOrdemServico.objects.create(
                ordem_servico=ordem_servico,
                alojamento_id=alojamento_data['alojamento_id'],
                ordem_parada=alojamento_data['ordem_parada']
            )
        
        return ordem_servico
    
    def update(self, instance, validated_data):
        alojamentos_data = validated_data.pop('alojamentos', None)
        
        # Atualizar os campos da ordem de serviço
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Se alojamentos foram fornecidos, atualizar os relacionamentos
        if alojamentos_data is not None:
            # Remover relacionamentos existentes
            AlojamentoOrdemServico.objects.filter(ordem_servico=instance).delete()
            
            # Criar novos relacionamentos
            for alojamento_data in alojamentos_data:
                AlojamentoOrdemServico.objects.create(
                    ordem_servico=instance,
                    alojamento_id=alojamento_data['alojamento_id'],
                    ordem_parada=alojamento_data['ordem_parada']
                )
        
        return instance
