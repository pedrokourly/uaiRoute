from django.contrib import admin
from .models import Registro

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'email', 'criado_em']
    search_fields = ['nome_completo', 'email']
