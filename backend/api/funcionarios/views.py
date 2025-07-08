from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import Funcionario
from .serializers import FuncionarioSerializer
from api.obras.models import Obra  # Corrigido: importando 'Obra' de 'api.obras.models'

# API de Funcionários
class FuncionarioListCreateView(generics.ListCreateAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Validação manual para verificar capacidade do alojamento
            funcionario = serializer.save()
            funcionario.full_clean()  # Chama o método clean() do modelo
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Retorna erro de validação
            return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

class FuncionarioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Validação manual para verificar capacidade do alojamento
            funcionario = serializer.save()
            funcionario.full_clean()  # Chama o método clean() do modelo
            return Response(serializer.data)
        except ValidationError as e:
            # Retorna erro de validação
            return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
