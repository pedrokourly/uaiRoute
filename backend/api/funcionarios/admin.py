from django.contrib import admin
from .models import Funcionario

# Registrando o modelo 'Funcionario' para ser exibido no admin
admin.site.register(Funcionario)
