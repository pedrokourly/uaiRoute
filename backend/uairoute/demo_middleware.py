"""Um banco SQLite por visitante do demo.

O visitante recebe um identificador no cookie de sessão do Flask, que o
repassa em X-Demo-Session. Aqui esse identificador vira o arquivo que a
conexão 'default' vai usar durante o request.

A troca é feita em settings_dict['NAME'] da conexão, não por um router:
assim nenhuma view, serializer ou model precisa saber que isso existe.

Requer gunicorn com workers sync e sem --threads. A conexão é por processo;
com várias threads por worker, dois visitantes a compartilhariam.
"""
import os
import re
import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.db import connections
from django.http import JsonResponse

ID_VALIDO = re.compile(r'^[0-9a-f]{32}\Z')

# Caminhos que respondem sem tocar no banco e, por isso, sem sessão de demo.
CAMINHOS_LIVRES = ('/health/',)


class IdDeDemoInvalido(ValueError):
    pass


def caminho_do_banco(demo_id):
    """Traduz o identificador do visitante no arquivo do banco dele.

    A validação contra ID_VALIDO é requisito de segurança, não de robustez:
    o valor vem de um header e vira nome de arquivo. Sem ela, um
    X-Demo-Session com '../' escreve fora do diretório de demos.
    """
    if not isinstance(demo_id, str) or not ID_VALIDO.match(demo_id):
        raise IdDeDemoInvalido(f'Identificador de demo inválido: {demo_id!r}')
    return Path(settings.DEMO_DIR) / f'{demo_id}.sqlite3'


def _garantir_banco(caminho):
    if caminho.exists():
        return
    caminho.parent.mkdir(parents=True, exist_ok=True)
    semente = Path(settings.DEMO_SEED)
    if not semente.exists():
        raise FileNotFoundError(
            f'Banco semente ausente em {semente}. Rode: python manage.py build_seed'
        )
    # Copia para um arquivo temporário no mesmo diretório e troca atomicamente:
    # shutil.copy2 direto no destino não é atômico (trunca e escreve aos poucos),
    # então uma segunda requisição concorrente para o mesmo demo_id novo poderia
    # abrir uma conexão SQLite contra um arquivo parcialmente escrito.
    fd, temporario = tempfile.mkstemp(dir=caminho.parent, suffix='.tmp')
    os.close(fd)
    try:
        shutil.copy2(semente, temporario)
        os.replace(temporario, caminho)
    except BaseException:
        Path(temporario).unlink(missing_ok=True)
        raise


class DemoDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in CAMINHOS_LIVRES:
            return self.get_response(request)

        demo_id = request.META.get(settings.DEMO_HEADER)
        try:
            caminho = caminho_do_banco(demo_id)
        except IdDeDemoInvalido:
            return JsonResponse(
                {'error': 'Requisição sem sessão de demo válida.'}, status=400
            )

        _garantir_banco(caminho)

        conexao = connections['default']
        conexao.close()
        conexao.settings_dict['NAME'] = str(caminho)
        try:
            return self.get_response(request)
        finally:
            conexao.close()
