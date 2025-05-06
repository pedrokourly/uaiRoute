from django.urls import path
from .views import FuncionarioListCreateView, FuncionarioRetrieveUpdateDestroyView

urlpatterns = [
    path('funcionarios/', FuncionarioListCreateView.as_view(), name='listar_funcionarios'),
    path('funcionarios/<int:pk>/', FuncionarioRetrieveUpdateDestroyView.as_view(), name='detalhar_funcionario'),
]
