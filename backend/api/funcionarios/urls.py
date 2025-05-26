from django.urls import path
from .views import (
    FuncionarioListCreateView,
    FuncionarioRetrieveUpdateDestroyView,
    FuncionarioLoginView
)

urlpatterns = [
    path('', FuncionarioListCreateView.as_view(), name='listar_funcionarios_api'),  # GET/POST
    path('<int:pk>/', FuncionarioRetrieveUpdateDestroyView.as_view(), name='detalhar_funcionario'),  # GET/PUT/DELETE
    path('login/', FuncionarioLoginView.as_view(), name='login_funcionario'),  # POST para login
]
