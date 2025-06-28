from django.db import models
from api.veiculos.models import Veiculo
from api.alojamento.models import Alojamento
from api.obras.models import Obra

class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    obra_destino = models.ForeignKey(Obra, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    
    # Campos para cálculo de rota
    distancia_total = models.FloatField(null=True, blank=True, help_text="Distância em km")
    tempo_estimado = models.IntegerField(null=True, blank=True, help_text="Tempo em minutos")
    
    def __str__(self):
        return f"{self.titulo} - {self.veiculo.placa}"

class AlojamentoOrdemServico(models.Model):
    """Relacionamento muitos-para-muitos entre OrdemServico e Alojamento"""
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='alojamentos_paradas')
    alojamento = models.ForeignKey(Alojamento, on_delete=models.CASCADE)
    ordem_parada = models.IntegerField(help_text="Ordem da parada na rota")
    
    class Meta:
        ordering = ['ordem_parada']
        unique_together = ['ordem_servico', 'ordem_parada']
    
    def __str__(self):
        return f"{self.ordem_servico.titulo} - Parada {self.ordem_parada}: {self.alojamento.nome}"
