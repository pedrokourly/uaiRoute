from django.db import models
from django.core.exceptions import ValidationError

class Alojamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    capacidade_maxima = models.PositiveIntegerField()
    
    # Novo endereço
    rua = models.CharField(max_length=255, default='Desconhecida')
    numero = models.CharField(max_length=10, default='S/N')
    bairro = models.CharField(max_length=100, default='Desconhecido')
    cidade = models.CharField(max_length=100, default='Desconhecido')

    def clean(self):
        # Validação para não permitir capacidade menor que funcionários já alocados
        if self.pk:  # Se é uma edição (não criação)
            funcionarios_alocados = self.funcionarios.count()
            if self.capacidade_maxima < funcionarios_alocados:
                raise ValidationError({
                    'capacidade_maxima': f"Não é possível reduzir a capacidade para {self.capacidade_maxima}. "
                                       f"Há {funcionarios_alocados} funcionários já alocados neste alojamento."
                })

    def __str__(self):
        return f"{self.nome} ({self.capacidade_maxima} vagas)"

    def vagas_disponiveis(self):
        return self.capacidade_maxima - self.funcionarios.count()
