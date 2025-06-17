from rest_framework import generics
from .models import Alojamento
from .serializers import AlojamentoSerializer

class AlojamentoListCreateView(generics.ListCreateAPIView):
    queryset = Alojamento.objects.all()
    serializer_class = AlojamentoSerializer

class AlojamentoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alojamento.objects.all()
    serializer_class = AlojamentoSerializer
