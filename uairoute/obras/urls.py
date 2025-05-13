from django.urls import path
from .views import ObraListCreateView, ObraRetrieveUpdateDestroyView

urlpatterns = [
    path('obras/', ObraListCreateView.as_view(), name='listar_obras'),
    path('obras/<int:pk>/', ObraRetrieveUpdateDestroyView.as_view(), name='detalhar_obra'),
]
