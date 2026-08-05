"""Proxy do cálculo de rotas da OpenRouteService.

A chave ficava embutida no JavaScript da tela de visualização de ordem, o
que a entregava a qualquer visitante que abrisse o código-fonte da página.
A chamada passa a sair daqui, e a chave nunca chega ao browser.
"""
import os

import requests
import backend_client
from flask import jsonify, request

from uairoute import app
from auth_routes import require_login_api

ORS_API_KEY = os.environ.get('ORS_API_KEY', '')
ORS_URL = 'https://api.openrouteservice.org/v2/directions/driving-car/json'


@app.route('/api/rota/direcoes', methods=['POST'])
@require_login_api
def rota_direcoes():
    if not ORS_API_KEY:
        return jsonify({
            'error': 'Cálculo de rota indisponível: ORS_API_KEY não configurada.'
        }), 503

    coordenadas = (request.get_json(silent=True) or {}).get('coordinates')
    if not coordenadas or len(coordenadas) < 2:
        return jsonify({'error': 'São necessárias ao menos duas coordenadas.'}), 400

    try:
        resposta = backend_client.post(
            ORS_URL,
            headers={
                'Authorization': ORS_API_KEY,
                'Content-Type': 'application/json',
            },
            json={
                'coordinates': coordenadas,
                'profile': 'driving-car',
                'format': 'json',
                'geometry': 'true',
                'instructions': 'false',
            },
            timeout=20,
        )
    except requests.RequestException as erro:
        return jsonify({'error': f'Serviço de rotas indisponível: {erro}'}), 502

    if resposta.status_code != 200:
        return jsonify({'error': 'Erro ao calcular a rota.'}), resposta.status_code

    return jsonify(resposta.json())
