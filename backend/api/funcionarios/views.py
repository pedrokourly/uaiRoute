from rest_framework import generics
from .models import Funcionario
from .serializers import FuncionarioSerializer
from api.obras.models import Obra  # Corrigido: importando 'Obra' de 'api.obras.models'

# API de Funcionários
class FuncionarioListCreateView(generics.ListCreateAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

class FuncionarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
