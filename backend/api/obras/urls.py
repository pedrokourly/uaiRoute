from django.urls import path
from .views import ObraListCreateView, ObraRetrieveUpdateDestroyView

urlpatterns = [
    # Para listar todas as obras ou criar uma nova
    path('', ObraListCreateView.as_view(), name='listar_obras_api'),  # GET/POST

    # Para recuperar, editar ou excluir uma obra específica
    path('<int:pk>/', ObraRetrieveUpdateDestroyView.as_view(), name='detalhar_obra'),  # GET/PUT/DELETE
]
