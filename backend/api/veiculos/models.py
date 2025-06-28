from django.db import models

class Veiculo(models.Model):
    TIPO_CHOICES = [
        ('carro', 'Carro'),
        ('van', 'Van'),
        ('caminhao', 'Caminhão'),
        ('moto', 'Moto'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    placa = models.CharField(max_length=10, unique=True)
    capacidade = models.PositiveIntegerField()

    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    
    # Coordenadas geográficas
    latitude = models.FloatField(null=True, blank=True, help_text="Latitude do veículo")
    longitude = models.FloatField(null=True, blank=True, help_text="Longitude do veículo")

    disponibilidade = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo} - {self.placa}"
