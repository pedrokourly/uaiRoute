from django.contrib import admin
from .models import Obra

# Registrando o modelo 'Obra' para ser exibido no admin
admin.site.register(Obra)
