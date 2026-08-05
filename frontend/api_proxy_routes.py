"""Rotas que repassam ao backend as consultas que o mapa faz pelo browser.

O Django não é mais publicado para fora da rede do Docker, então o
JavaScript do mapa não consegue mais falar com ele diretamente. Estas rotas
são a única ponte, e passam pela mesma sessão que protege o resto do app.
"""
import requests
from flask import jsonify

from uairoute import app
from config import API_URLS
from auth_routes import require_login_api


def _repassar(url):
    try:
        resposta = requests.get(url, timeout=10)
    except requests.RequestException as erro:
        return jsonify({'error': f'Backend indisponível: {erro}'}), 502

    if resposta.status_code != 200:
        return jsonify({'error': 'Erro ao consultar o backend'}), resposta.status_code

    return jsonify(resposta.json())


@app.route('/api/obras')
@require_login_api
def api_obras():
    return _repassar(API_URLS['obras'])


@app.route('/api/veiculos')
@require_login_api
def api_veiculos():
    return _repassar(API_URLS['veiculos'])


@app.route('/api/alojamento')
@require_login_api
def api_alojamento():
    return _repassar(API_URLS['alojamentos'])
