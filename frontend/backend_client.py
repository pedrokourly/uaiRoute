"""Ponto único de saída das chamadas HTTP ao backend Django.

Existe para que a branch demo consiga injetar o header de sessão em todas
as chamadas mexendo num arquivo só, em vez de nos seis módulos de rota.
Na branch main, headers_extras() não devolve nada.
"""
import requests

from config import BACKEND_URL

TIMEOUT_PADRAO = 15


def headers_extras(url):
    """Header que diz ao backend qual banco de demo usar.

    Fora de um contexto de requisição (comandos, testes de unidade) não há
    sessão, e o dicionário vazio faz a chamada seguir sem o header.
    """
    from flask import has_request_context, session

    # Só injeta o header em chamadas ao próprio backend Django -- a chamada
    # à OpenRouteService em rota_routes.py usa o mesmo cliente, e o id de
    # sessão do demo não tem nada a ver com aquele serviço externo.
    if not url.startswith(BACKEND_URL):
        return {}

    if not has_request_context():
        return {}
    demo_id = session.get('demo_id')
    return {'X-Demo-Session': demo_id} if demo_id else {}


def _chamar(metodo, url, **kwargs):
    kwargs.setdefault('timeout', TIMEOUT_PADRAO)
    headers = dict(kwargs.pop('headers', None) or {})
    headers.update(headers_extras(url))
    if headers:
        kwargs['headers'] = headers
    return requests.request(metodo, url, **kwargs)


def get(url, **kwargs):
    return _chamar('GET', url, **kwargs)


def post(url, **kwargs):
    return _chamar('POST', url, **kwargs)


def put(url, **kwargs):
    return _chamar('PUT', url, **kwargs)


def delete(url, **kwargs):
    return _chamar('DELETE', url, **kwargs)


def patch(url, **kwargs):
    return _chamar('PATCH', url, **kwargs)
