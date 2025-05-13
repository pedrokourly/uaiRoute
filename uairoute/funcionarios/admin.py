from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display =  ['id','nome_completo', 'email', 'cargo', 'cidade']
    search_fields = ['id','nome_completo', 'email', 'cargo']
    list_filter = ['id','cidade', 'cargo']
