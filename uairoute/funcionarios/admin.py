from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'email', 'cargo', 'cidade']
    search_fields = ['nome_completo', 'email', 'cargo']
    list_filter = ['cidade', 'cargo']
