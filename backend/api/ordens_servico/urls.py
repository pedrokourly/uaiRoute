from django.urls import path
from . import views

urlpatterns = [
    path('', views.ordens_servico_list, name='ordens_servico_list'),
    path('<int:pk>/', views.ordem_servico_detail, name='ordem_servico_detail'),
    path('<int:pk>/rota/', views.ordem_servico_rota, name='ordem_servico_rota'),
    path('alojamento/<int:alojamento_id>/', views.ordens_servico_por_alojamento, name='ordens_servico_por_alojamento'),
    path('funcionario/<int:funcionario_id>/', views.ordens_servico_funcionario, name='ordens_servico_funcionario'),
]
