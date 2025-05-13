from rest_framework import generics
from .models import Funcionario
from .serializers import FuncionarioSerializer

class FuncionarioListCreateView(generics.ListCreateAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

class FuncionarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
