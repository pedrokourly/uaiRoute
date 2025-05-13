from django.db import models

class Obra(models.Model):
    nome = models.CharField(max_length=120)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.cidade}"
