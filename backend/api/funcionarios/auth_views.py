from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Funcionario

@api_view(['POST'])
def login(request):
    """
    Endpoint para autenticação de funcionários
    """
    email = request.data.get('email')
    senha = request.data.get('senha')
    
    if not email or not senha:
        return Response({
            'error': 'Email e senha são obrigatórios'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Busca funcionário pelo email
        funcionario = Funcionario.objects.get(email=email)
        
        # Verifica a senha (por enquanto comparação simples, em produção usar hash)
        if funcionario.senha == senha:
            # Login bem-sucedido
            return Response({
                'success': True,
                'funcionario': {
                    'id': funcionario.id,
                    'nome_completo': funcionario.nome_completo,
                    'email': funcionario.email,
                    'cargo': funcionario.cargo,
                    'is_admin': funcionario.is_admin,
                    'alojamento': funcionario.alojamento.id if funcionario.alojamento else None
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Email ou senha incorretos'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except Funcionario.DoesNotExist:
        return Response({
            'error': 'Email ou senha incorretos'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def perfil(request):
    """
    Endpoint para obter dados do perfil do funcionário logado
    """
    funcionario_id = request.GET.get('id')
    
    if not funcionario_id:
        return Response({
            'error': 'ID do funcionário é obrigatório'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        funcionario = Funcionario.objects.get(id=funcionario_id)
        return Response({
            'id': funcionario.id,
            'nome_completo': funcionario.nome_completo,
            'email': funcionario.email,
            'cargo': funcionario.cargo,
            'is_admin': funcionario.is_admin,
            'alojamento': funcionario.alojamento.id if funcionario.alojamento else None,
            'alojamento_nome': funcionario.alojamento.nome if funcionario.alojamento else None
        }, status=status.HTTP_200_OK)
        
    except Funcionario.DoesNotExist:
        return Response({
            'error': 'Funcionário não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def atualizar_perfil(request):
    """
    Endpoint para funcionário atualizar seus próprios dados
    """
    funcionario_id = request.data.get('id')
    
    if not funcionario_id:
        return Response({
            'error': 'ID do funcionário é obrigatório'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        funcionario = Funcionario.objects.get(id=funcionario_id)
        
        # Permite atualizar apenas alguns campos
        if 'nome_completo' in request.data:
            funcionario.nome_completo = request.data['nome_completo']
        if 'email' in request.data:
            funcionario.email = request.data['email']
        if 'cargo' in request.data:
            funcionario.cargo = request.data['cargo']
        if 'senha' in request.data and request.data['senha']:
            funcionario.senha = request.data['senha']
            
        # Apenas admin pode alterar is_admin e alojamento de outros
        # Por simplicidade, vamos permitir que o usuário altere seu próprio alojamento
        if 'alojamento' in request.data:
            alojamento_id = request.data['alojamento']
            if alojamento_id:
                from api.alojamento.models import Alojamento
                funcionario.alojamento = Alojamento.objects.get(id=alojamento_id)
            else:
                funcionario.alojamento = None
        
        funcionario.full_clean()  # Valida o modelo
        funcionario.save()
        
        return Response({
            'success': True,
            'message': 'Perfil atualizado com sucesso'
        }, status=status.HTTP_200_OK)
        
    except Funcionario.DoesNotExist:
        return Response({
            'error': 'Funcionário não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
