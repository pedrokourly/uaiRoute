from django.urls import path
from .views import FuncionarioListCreateView, FuncionarioRetrieveUpdateDestroyView
from .auth_views import login, perfil, atualizar_perfil

urlpatterns = [
    # Para listar todos os funcionários ou criar um novo
    path('', FuncionarioListCreateView.as_view(), name='listar_funcionarios_api'),  # GET/POST

    # Para recuperar, editar ou excluir um funcionário específico
    path('<int:pk>/', FuncionarioRetrieveUpdateDestroyView.as_view(), name='detalhar_funcionario'),  # GET/PUT/DELETE
    
    # Endpoints de autenticação
    path('login/', login, name='login_funcionario'),  # POST
    path('perfil/', perfil, name='perfil_funcionario'),  # GET
    path('perfil/atualizar/', atualizar_perfil, name='atualizar_perfil_funcionario'),  # PUT
]
