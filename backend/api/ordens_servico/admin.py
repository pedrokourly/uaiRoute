from django.contrib import admin
from .models import OrdemServico, AlojamentoOrdemServico

class AlojamentoOrdemServicoInline(admin.TabularInline):
    model = AlojamentoOrdemServico
    extra = 1

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'veiculo', 'obra_destino', 'status', 'data_criacao']
    list_filter = ['status', 'data_criacao']
    search_fields = ['titulo', 'veiculo__placa', 'obra_destino__nome']
    inlines = [AlojamentoOrdemServicoInline]
