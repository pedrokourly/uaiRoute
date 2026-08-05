"""Testes de calcular_rota_otimizada quando ORS_API_KEY não está configurada.

A mesma chave hardcoded que o Task 6 tirou do JavaScript do frontend também
vivia aqui, usada em duas chamadas server-to-server à OpenRouteService. Os
dois pontos que chamam esta função (ordens_servico_list e
ordem_servico_detail) engolem qualquer exceção só imprimindo no console --
então, assim que a chave antiga for revogada, o cálculo de rota passaria a
falhar em silêncio. Estes testes garantem que a ausência da chave é tratada
de forma explícita, sem chamar a OpenRouteService com uma chave vazia.
"""
import json
from unittest.mock import patch

import pytest

from api.obras.models import Obra
from api.ordens_servico.views import calcular_rota_otimizada
from api.veiculos.models import Veiculo


def _criar_ordem_servico():
    veiculo = Veiculo.objects.create(
        tipo='carro',
        placa='ABC1234',
        capacidade=4,
        rua='Rua A',
        numero='1',
        bairro='Centro',
        cidade='Porto Alegre',
        latitude=-30.0346,
        longitude=-51.2177,
    )
    obra = Obra.objects.create(
        nome='Obra Teste',
        rua='Rua B',
        numero='2',
        bairro='Centro',
        cidade='Gramado',
        latitude=-29.3794,
        longitude=-50.8764,
    )
    from api.ordens_servico.models import OrdemServico
    return OrdemServico.objects.create(titulo='Ordem Teste', veiculo=veiculo, obra_destino=obra)


@pytest.mark.django_db
@patch('api.ordens_servico.views.requests.post')
def test_sem_chave_nao_chama_a_ors_e_nao_levanta_excecao(mock_post, monkeypatch):
    monkeypatch.setenv('ORS_API_KEY', '')
    ordem_servico = _criar_ordem_servico()

    calcular_rota_otimizada(ordem_servico)

    mock_post.assert_not_called()
    assert ordem_servico.distancia_total is None
    assert ordem_servico.tempo_estimado is None


@pytest.mark.django_db
@patch('api.ordens_servico.views.requests.post')
def test_criar_ordem_sem_chave_nao_quebra_a_criacao(mock_post, monkeypatch, client):
    """Fluxo real: POST /api/ordens-servico/ dispara calcular_rota_otimizada
    dentro de um try/except que hoje só imprime o erro. Sem a chave, a
    criação da ordem precisa continuar funcionando normalmente."""
    monkeypatch.setenv('ORS_API_KEY', '')
    veiculo = Veiculo.objects.create(
        tipo='carro', placa='XYZ9876', capacidade=4,
        rua='Rua A', numero='1', bairro='Centro', cidade='Porto Alegre',
    )
    obra = Obra.objects.create(
        nome='Obra Teste 2', rua='Rua B', numero='2', bairro='Centro', cidade='Gramado',
    )

    resposta = client.post(
        '/api/ordens-servico/',
        data=json.dumps({
            'titulo': 'Ordem via API',
            'veiculo_id': veiculo.id,
            'obra_destino_id': obra.id,
        }),
        content_type='application/json',
    )

    assert resposta.status_code == 201, resposta.content
    mock_post.assert_not_called()
