from django.contrib import admin
from .models import Alojamento

@admin.register(Alojamento)
class AlojamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'capacidade_maxima', 'vagas_disponiveis', 'rua', 'numero', 'bairro', 'cidade')
    search_fields = ('nome', 'bairro', 'cidade')
