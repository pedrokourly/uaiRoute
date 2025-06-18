from django.db import models

class Alojamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    capacidade_maxima = models.PositiveIntegerField()
    
    # Novo endereço
    rua = models.CharField(max_length=255, default='Desconhecida')
    numero = models.CharField(max_length=10, default='S/N')
    bairro = models.CharField(max_length=100, default='Desconhecido')
    cidade = models.CharField(max_length=100, default='Desconhecido')

    def __str__(self):
        return f"{self.nome} ({self.capacidade_maxima} vagas)"

    def vagas_disponiveis(self):
        return self.capacidade_maxima - self.funcionarios.count()
