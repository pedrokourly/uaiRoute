from django.urls import path
from . import views

urlpatterns = [
    # Para listar todas as obras ou criar uma nova
    path('', views.obra_list_create, name='listar_obras_api'),  # GET/POST

    # Para recuperar, editar ou excluir uma obra específica
    path('<int:pk>/', views.obra_detail, name='detalhar_obra'),  # GET/PUT/DELETE
]
