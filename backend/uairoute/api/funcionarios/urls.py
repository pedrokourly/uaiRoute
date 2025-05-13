from django.urls import path
from .views import FuncionarioListCreateView, FuncionarioRetrieveUpdateDestroyView

urlpatterns = [
    # Para listar todos os funcionários ou criar um novo
    path('', FuncionarioListCreateView.as_view(), name='listar_funcionarios_api'),  # GET/POST

    # Para recuperar, editar ou excluir um funcionário específico
    path('<int:pk>/', FuncionarioRetrieveUpdateDestroyView.as_view(), name='detalhar_funcionario'),  # GET/PUT/DELETE
]
