from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import Alojamento
from .serializers import AlojamentoSerializer
from api.utils.geocoding import buscar_coordenadas_com_fallback

@api_view(['GET', 'POST'])
def alojamento_list_create(request):
    if request.method == 'GET':
        alojamentos = Alojamento.objects.all()
        serializer = AlojamentoSerializer(alojamentos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AlojamentoSerializer(data=request.data)
        if serializer.is_valid():
            alojamento = serializer.save()
            
            # Buscar coordenadas automaticamente se não foram fornecidas
            if not alojamento.latitude or not alojamento.longitude:
                lat, lon = buscar_coordenadas_com_fallback(
                    alojamento.rua, alojamento.numero, alojamento.bairro, alojamento.cidade
                )
                if lat and lon:
                    alojamento.latitude = lat
                    alojamento.longitude = lon
                    alojamento.save()
            
            # Retornar dados atualizados
            serializer = AlojamentoSerializer(alojamento)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def alojamento_detail(request, pk):
    try:
        alojamento = Alojamento.objects.get(pk=pk)
    except Alojamento.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AlojamentoSerializer(alojamento)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = AlojamentoSerializer(alojamento, data=request.data)
        if serializer.is_valid():
            try:
                alojamento = serializer.save()
                
                # Buscar coordenadas se o endereço foi alterado e coordenadas não foram fornecidas
                if not alojamento.latitude or not alojamento.longitude:
                    lat, lon = buscar_coordenadas_com_fallback(
                        alojamento.rua, alojamento.numero, alojamento.bairro, alojamento.cidade
                    )
                    if lat and lon:
                        alojamento.latitude = lat
                        alojamento.longitude = lon
                        alojamento.save()
                
                serializer = AlojamentoSerializer(alojamento)
                return Response(serializer.data)
            except ValidationError as e:
                return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            alojamento.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Validação manual para verificar se não há funcionários demais para a nova capacidade
            alojamento = serializer.save()
            alojamento.full_clean()  # Chama o método clean() do modelo
            return Response(serializer.data)
        except ValidationError as e:
            # Retorna erro de validação
            return Response({'error': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
