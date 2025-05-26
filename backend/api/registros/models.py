from django.db import models

class Registro(models.Model):
    nome_completo = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)  # campo novo
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo
