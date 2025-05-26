from django.contrib import admin
from .models import Veiculo

# Registrando o modelo 'Veiculo' para ser exibido no admin
admin.site.register(Veiculo)
