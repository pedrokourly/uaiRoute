from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Obra
from .serializers import ObraSerializer
from api.utils.geocoding import buscar_coordenadas_com_fallback

@api_view(['GET', 'POST'])
def obra_list_create(request):
    if request.method == 'GET':
        obras = Obra.objects.all()
        serializer = ObraSerializer(obras, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ObraSerializer(data=request.data)
        if serializer.is_valid():
            obra = serializer.save()
            
            # Buscar coordenadas automaticamente se não foram fornecidas
            if not obra.latitude or not obra.longitude:
                lat, lon = buscar_coordenadas_com_fallback(
                    obra.rua, obra.numero, obra.bairro, obra.cidade
                )
                if lat and lon:
                    obra.latitude = lat
                    obra.longitude = lon
                    obra.save()
            
            # Retornar dados atualizados
            serializer = ObraSerializer(obra)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def obra_detail(request, pk):
    try:
        obra = Obra.objects.get(pk=pk)
    except Obra.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ObraSerializer(obra)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ObraSerializer(obra, data=request.data)
        if serializer.is_valid():
            obra = serializer.save()
            
            # Buscar coordenadas se o endereço foi alterado e coordenadas não foram fornecidas
            if not obra.latitude or not obra.longitude:
                lat, lon = buscar_coordenadas_com_fallback(
                    obra.rua, obra.numero, obra.bairro, obra.cidade
                )
                if lat and lon:
                    obra.latitude = lat
                    obra.longitude = lon
                    obra.save()
            
            serializer = ObraSerializer(obra)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        obra.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
