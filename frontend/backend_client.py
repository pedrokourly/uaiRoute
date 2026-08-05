"""Ponto único de saída das chamadas HTTP ao backend Django.

Existe para que a branch demo consiga injetar o header de sessão em todas
as chamadas mexendo num arquivo só, em vez de nos seis módulos de rota.
Na branch main, headers_extras() não devolve nada.
"""
import requests

TIMEOUT_PADRAO = 15


def headers_extras():
    """Gancho de extensão. A branch demo o substitui pelo header de sessão."""
    return {}


def _chamar(metodo, url, **kwargs):
    kwargs.setdefault('timeout', TIMEOUT_PADRAO)
    headers = dict(kwargs.pop('headers', None) or {})
    headers.update(headers_extras())
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
