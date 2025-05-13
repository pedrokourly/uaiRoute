from rest_framework import generics
from .models import Veiculo
from .serializers import VeiculoSerializer

# GET e POST - Lista todos os veículos ou cria um novo
class VeiculoListCreateView(generics.ListCreateAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

# GET, PUT/UPDATE e DELETE - Detalha, atualiza ou deleta um veículo
class VeiculoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
