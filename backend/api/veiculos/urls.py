from django.urls import path
from .views import VeiculoListCreateView, VeiculoRetrieveUpdateDestroyView

urlpatterns = [
    # Para listar todos os veículos ou criar um novo
    path('', VeiculoListCreateView.as_view(), name='listar_veiculos_api'),  # GET/POST

    # Para recuperar, editar ou excluir um veículo específico
    path('<int:pk>/', VeiculoRetrieveUpdateDestroyView.as_view(), name='detalhar_veiculo'),  # GET/PUT/DELETE
]
