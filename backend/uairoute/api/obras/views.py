from rest_framework import generics
from .models import Obra
from .serializers import ObraSerializer

# GET e POST - Lista todas as obras ou cria uma nova
class ObraListCreateView(generics.ListCreateAPIView):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer

# GET, PUT/UPDATE e DELETE - Detalha, atualiza ou deleta uma obra
class ObraRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
