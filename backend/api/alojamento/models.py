from django.db import models

class Alojamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    capacidade_maxima = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nome} ({self.capacidade_maxima} vagas)"

    def vagas_disponiveis(self):
        # Usa o related_name definido no modelo Funcionario
        return self.capacidade_maxima - self.funcionarios.count()
