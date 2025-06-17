from django.urls import path
from .views import AlojamentoListCreateView, AlojamentoRetrieveUpdateDestroyView

urlpatterns = [
    path('', AlojamentoListCreateView.as_view(), name='listar_alojamentos'),
    path('<int:pk>/', AlojamentoRetrieveUpdateDestroyView.as_view(), name='detalhar_alojamento'),
]
