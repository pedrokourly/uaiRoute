from django.db import models
from django.core.exceptions import ValidationError
from api.alojamento.models import Alojamento

class Funcionario(models.Model):
    nome_completo = models.CharField("Nome completo", max_length=255)
    rua = models.CharField("Rua", max_length=255)
    numero = models.CharField("Número", max_length=10)
    bairro = models.CharField("Bairro", max_length=100)
    cidade = models.CharField("Cidade", max_length=100)
    cargo = models.CharField("Cargo", max_length=100)
    email = models.EmailField("E-mail", unique=True)
    senha = models.CharField("Senha (criptografada)", max_length=128)
    is_admin = models.BooleanField("É administrador?", default=False)

    alojamento = models.ForeignKey(
        Alojamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='funcionarios'
    )

    def clean(self):
        if self.alojamento:
            ocupados = self.alojamento.funcionarios.exclude(id=self.id).count()
            if ocupados >= self.alojamento.capacidade_maxima:
                raise ValidationError({'alojamento': f"O alojamento '{self.alojamento.nome}' está lotado."})

    def __str__(self):
        return self.nome_completo

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
