from django.urls import path
from . import views

urlpatterns = [
    path('', views.alojamento_list_create, name='listar_alojamentos'),
    path('<int:pk>/', views.alojamento_detail, name='detalhar_alojamento'),
]
