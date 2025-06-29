from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import OrdemServico
from .serializers import OrdemServicoSerializer
import requests
import json

@api_view(['GET', 'POST'])
def ordens_servico_list(request):
    if request.method == 'GET':
        ordens = OrdemServico.objects.all().order_by('-data_criacao')
        serializer = OrdemServicoSerializer(ordens, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = OrdemServicoSerializer(data=request.data)
        if serializer.is_valid():
            ordem_servico = serializer.save()
            
            # Calcular rota automaticamente
            try:
                calcular_rota_otimizada(ordem_servico)
            except Exception as e:
                print(f"Erro ao calcular rota: {e}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ordem_servico_detail(request, pk):
    try:
        ordem = OrdemServico.objects.get(pk=pk)
    except OrdemServico.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OrdemServicoSerializer(ordem)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OrdemServicoSerializer(ordem, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        ordem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def ordem_servico_rota(request, pk):
    """Endpoint para obter dados da rota otimizada"""
    try:
        ordem = OrdemServico.objects.get(pk=pk)
    except OrdemServico.DoesNotExist:
        return Response({'error': 'Ordem de serviço não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        rota_data = gerar_dados_rota(ordem)
        return Response(rota_data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def ordens_servico_por_alojamento(request, alojamento_id):
    """
    Retorna todas as ordens de serviço que incluem um alojamento específico como parada
    """
    try:
        from .models import AlojamentoOrdemServico
        
        # Buscar todas as ordens de serviço que incluem este alojamento
        paradas_alojamento = AlojamentoOrdemServico.objects.filter(
            alojamento_id=alojamento_id
        ).select_related('ordem_servico')
        
        ordens_ids = [parada.ordem_servico.id for parada in paradas_alojamento]
        ordens = OrdemServico.objects.filter(id__in=ordens_ids).order_by('-data_criacao')
        
        serializer = OrdemServicoSerializer(ordens, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': f'Erro ao buscar ordens de serviço: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def ordens_servico_funcionario(request, funcionario_id):
    """
    Retorna todas as ordens de serviço relacionadas ao alojamento onde o funcionário está hospedado
    """
    try:
        from api.funcionarios.models import Funcionario
        
        # Buscar o funcionário
        funcionario = Funcionario.objects.get(pk=funcionario_id)
        
        if not funcionario.alojamento:
            return Response({
                'message': 'Funcionário não está associado a nenhum alojamento',
                'ordens': []
            })
        
        # Buscar ordens de serviço que incluem o alojamento do funcionário
        from .models import AlojamentoOrdemServico
        
        paradas_alojamento = AlojamentoOrdemServico.objects.filter(
            alojamento=funcionario.alojamento
        ).select_related('ordem_servico')
        
        ordens_ids = [parada.ordem_servico.id for parada in paradas_alojamento]
        ordens = OrdemServico.objects.filter(id__in=ordens_ids).order_by('-data_criacao')
        
        serializer = OrdemServicoSerializer(ordens, many=True)
        return Response({
            'funcionario': {
                'id': funcionario.id,
                'nome': funcionario.nome_completo,
                'alojamento': funcionario.alojamento.nome if funcionario.alojamento else None
            },
            'ordens': serializer.data
        })
        
    except Funcionario.DoesNotExist:
        return Response(
            {'error': 'Funcionário não encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Erro ao buscar ordens de serviço: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def calcular_rota_otimizada(ordem_servico):
    """Calcula a rota otimizada usando a API OpenRouteService"""
    api_key = '5b3ce3597851110001cf62489715e0567dc24edd98bd95aee36637a9'
    
    # Ponto de partida (localização do veículo)
    veiculo = ordem_servico.veiculo
    if veiculo.latitude and veiculo.longitude:
        start_point = [float(veiculo.longitude), float(veiculo.latitude)]
    else:
        # Coordenada padrão (centro de Porto Alegre)
        start_point = [-51.2177, -30.0346]
    
    # Ponto final (obra de destino)
    obra = ordem_servico.obra_destino
    if obra.latitude and obra.longitude:
        end_point = [float(obra.longitude), float(obra.latitude)]
    else:
        # Coordenada padrão (Gramado)
        end_point = [-50.8764, -29.3794]
    
    # Pontos intermediários (alojamentos)
    waypoints = []
    coordenadas_padrao = [
        [-51.1794, -29.1687],  # Caxias do Sul
        [-51.1378, -29.6854],  # Novo Hamburgo
        [-50.8497, -29.3653],  # Canela
        [-51.1000, -29.5000],  # Coordenada adicional 1
        [-50.9000, -29.4000],  # Coordenada adicional 2
    ]
    
    for i, parada in enumerate(ordem_servico.alojamentos_paradas.all()):
        alojamento = parada.alojamento
        if alojamento.latitude and alojamento.longitude:
            waypoints.append([float(alojamento.longitude), float(alojamento.latitude)])
        else:
            # Usar coordenada padrão baseada no índice
            if i < len(coordenadas_padrao):
                waypoints.append(coordenadas_padrao[i])
            else:
                # Se exceder as coordenadas padrão, usar uma próxima a Porto Alegre
                waypoints.append([-51.2177 + (i * 0.1), -30.0346 + (i * 0.1)])
    
    if not waypoints:
        # Rota direta se não há paradas
        coordinates = [start_point, end_point]
    else:
        # Rota otimizada com paradas
        optimization_body = {
            "jobs": [{"id": i+1, "location": point} for i, point in enumerate(waypoints)],
            "vehicles": [{
                "id": 1,
                "profile": "driving-car",
                "start": start_point,
                "end": end_point
            }]
        }
        
        try:
            opt_response = requests.post(
                'https://api.openrouteservice.org/optimization',
                headers={
                    'Authorization': api_key,
                    'Content-Type': 'application/json'
                },
                json=optimization_body,
                timeout=10
            )
            
            if opt_response.ok:
                opt_data = opt_response.json()
                if opt_data.get('routes') and len(opt_data['routes']) > 0:
                    route = opt_data['routes'][0]
                    coordinates = [start_point]
                    for step in route['steps']:
                        if step['type'] in ['job', 'end']:
                            coordinates.append(step['location'])
        except:
            coordinates = [start_point] + waypoints + [end_point]
    
    # Calcular direções finais
    try:
        directions_response = requests.post(
            'https://api.openrouteservice.org/v2/directions/driving-car/json',
            headers={
                'Authorization': api_key,
                'Content-Type': 'application/json'
            },
            json={
                "coordinates": coordinates,
                "profile": "driving-car",
                "format": "json"
            },
            timeout=10
        )
        
        if directions_response.ok:
            directions_data = directions_response.json()
            if directions_data.get('routes') and len(directions_data['routes']) > 0:
                summary = directions_data['routes'][0]['summary']
                ordem_servico.distancia_total = round(summary['distance'] / 1000, 2)  # km
                ordem_servico.tempo_estimado = round(summary['duration'] / 60)  # minutos
                ordem_servico.save()
    except:
        pass

def gerar_dados_rota(ordem_servico):
    """Gera dados formatados para renderização da rota no frontend"""
    veiculo = ordem_servico.veiculo
    obra = ordem_servico.obra_destino
    
    # Dados básicos da rota
    rota_data = {
        'ordem_id': ordem_servico.id,
        'titulo': ordem_servico.titulo,
        'veiculo': {
            'tipo': veiculo.tipo,
            'placa': veiculo.placa,
            'posicao': [
                float(veiculo.longitude) if veiculo.longitude else -51.2177,
                float(veiculo.latitude) if veiculo.latitude else -30.0346
            ]
        },
        'obra_destino': {
            'nome': obra.nome,
            'endereco': f"{obra.rua}, {obra.numero} - {obra.bairro}, {obra.cidade}",
            'posicao': [
                float(obra.longitude) if obra.longitude else -50.8764,
                float(obra.latitude) if obra.latitude else -29.3794
            ]
        },
        'alojamentos': [],
        'distancia_total': ordem_servico.distancia_total,
        'tempo_estimado': ordem_servico.tempo_estimado,
        'status': ordem_servico.status
    }
    
    # Coordenadas padrão para alojamentos sem coordenadas
    coordenadas_padrao = [
        [-51.1794, -29.1687],  # Caxias do Sul
        [-51.1378, -29.6854],  # Novo Hamburgo
        [-50.8497, -29.3653],  # Canela
        [-51.1000, -29.5000],  # Coordenada adicional 1
        [-50.9000, -29.4000],  # Coordenada adicional 2
    ]
    
    # Adicionar alojamentos na ordem correta
    for i, parada in enumerate(ordem_servico.alojamentos_paradas.all()):
        alojamento = parada.alojamento
        
        # Determinar coordenadas
        if alojamento.latitude and alojamento.longitude:
            posicao = [float(alojamento.longitude), float(alojamento.latitude)]
        else:
            if i < len(coordenadas_padrao):
                posicao = coordenadas_padrao[i]
            else:
                posicao = [-51.2177 + (i * 0.1), -30.0346 + (i * 0.1)]
        
        rota_data['alojamentos'].append({
            'nome': alojamento.nome,
            'ordem': parada.ordem_parada,
            'endereco': f"{alojamento.rua}, {alojamento.numero} - {alojamento.bairro}, {alojamento.cidade}",
            'posicao': posicao
        })
    
    return rota_data
