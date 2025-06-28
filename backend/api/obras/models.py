from django.db import models

class Obra(models.Model):
    nome = models.CharField(max_length=120)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    
    # Coordenadas geográficas
    latitude = models.FloatField(null=True, blank=True, help_text="Latitude da obra")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitude da obra")

    def __str__(self):
        return f"{self.nome} - {self.cidade}"
