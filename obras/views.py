from rest_framework import generics
from .models import Obra
from .serializers import ObraSerializer

class ObraListCreateView(generics.ListCreateAPIView):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer

class ObraRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
