from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Incluir as URLs dos apps de Obras, Funcionários e Veículos
    path('api/obras/', include('api.obras.urls')),  # API de Obras
    path('api/funcionarios/', include('api.funcionarios.urls')),  # API de Funcionários
    path('api/veiculos/', include('api.veiculos.urls')),  # API de Veículos
    path('api/registros/', include('api.registros.urls')),
    path('api/alojamento/', include('api.alojamento.urls')),
    path('api/ordens-servico/', include('api.ordens_servico.urls')),  # API de Ordens de Serviço
]
