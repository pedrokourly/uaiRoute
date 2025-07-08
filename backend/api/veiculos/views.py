from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Veiculo
from .serializers import VeiculoSerializer
from api.utils.geocoding import buscar_coordenadas_com_fallback

@api_view(['GET', 'POST'])
def veiculo_list_create(request):
    if request.method == 'GET':
        veiculos = Veiculo.objects.all()
        serializer = VeiculoSerializer(veiculos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = VeiculoSerializer(data=request.data)
        if serializer.is_valid():
            veiculo = serializer.save()
            
            # Buscar coordenadas automaticamente se não foram fornecidas
            if not veiculo.latitude or not veiculo.longitude:
                lat, lon = buscar_coordenadas_com_fallback(
                    veiculo.rua, veiculo.numero, veiculo.bairro, veiculo.cidade
                )
                if lat and lon:
                    veiculo.latitude = lat
                    veiculo.longitude = lon
                    veiculo.save()
            
            # Retornar dados atualizados
            serializer = VeiculoSerializer(veiculo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def veiculo_detail(request, pk):
    try:
        veiculo = Veiculo.objects.get(pk=pk)
    except Veiculo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = VeiculoSerializer(veiculo)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = VeiculoSerializer(veiculo, data=request.data)
        if serializer.is_valid():
            veiculo = serializer.save()
            
            # Buscar coordenadas se o endereço foi alterado e coordenadas não foram fornecidas
            if not veiculo.latitude or not veiculo.longitude:
                lat, lon = buscar_coordenadas_com_fallback(
                    veiculo.rua, veiculo.numero, veiculo.bairro, veiculo.cidade
                )
                if lat and lon:
                    veiculo.latitude = lat
                    veiculo.longitude = lon
                    veiculo.save()
            
            serializer = VeiculoSerializer(veiculo)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        veiculo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
