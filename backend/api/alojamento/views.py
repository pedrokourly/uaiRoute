from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import Alojamento
from .serializers import AlojamentoSerializer

class AlojamentoListCreateView(generics.ListCreateAPIView):
    queryset = Alojamento.objects.all()
    serializer_class = AlojamentoSerializer

class AlojamentoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alojamento.objects.all()
    serializer_class = AlojamentoSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Validação manual para verificar se não há funcionários demais para a nova capacidade
            alojamento = serializer.save()
            alojamento.full_clean()  # Chama o método clean() do modelo
            return Response(serializer.data)
        except ValidationError as e:
            # Retorna erro de validação
            return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
