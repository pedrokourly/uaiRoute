from django.urls import path
from .views import veiculo_list_create, veiculo_detail

urlpatterns = [
    # Para listar todos os veículos ou criar um novo
    path('', veiculo_list_create, name='listar_veiculos_api'),  # GET/POST

    # Para recuperar, editar ou excluir um veículo específico
    path('<int:pk>/', veiculo_detail, name='detalhar_veiculo'),  # GET/PUT/DELETE
]
