from django.contrib import admin
from .models import Obra

@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ['nome', 'rua', 'numero', 'bairro', 'cidade']
