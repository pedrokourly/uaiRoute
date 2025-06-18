from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_completo', 'email', 'cargo', 'alojamento', 'is_admin')
    list_filter = ('is_admin', 'alojamento')
    search_fields = ('nome_completo', 'email', 'cargo')

    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Aplica validações do modelo (como vagas do alojamento)
        super().save_model(request, obj, form, change)
