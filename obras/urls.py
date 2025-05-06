from django.urls import path
from .views import listar_obras, cadastrar_obra

urlpatterns = [
    path('obras/', listar_obras, name='listar_obras'),
    path('obras/cadastrar/', cadastrar_obra, name='cadastrar_obra'),
]
