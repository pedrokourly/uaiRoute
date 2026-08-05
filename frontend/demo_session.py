"""Sessão do visitante do demo: identificador do banco e entrada automática.

Cada visitante recebe um demo_id, que o backend traduz no arquivo SQLite
dele. O identificador precisa sobreviver ao logout: se sumisse, o visitante
receberia um banco novo e vazio na requisição seguinte, perdendo tudo o que
tivesse acabado de criar.
"""
from uuid import uuid4

from flask import session

from uairoute import app

ADMIN_DO_DEMO = {
    'email': 'admin@teste.com',
    'senha': 'admin',
}


@app.before_request
def preparar_sessao_de_demo():
    if session.get('demo_id'):
        return

    session['demo_id'] = uuid4().hex

    # Auto-login só na primeira visita. Quem fizer logout depois continua
    # fora, e consegue usar a tela de login com a conta de funcionário comum.
    if session.get('demo_deslogado'):
        return

    _autenticar_como_admin()


def _autenticar_como_admin():
    # Importado aqui para evitar ciclo: backend_client lê a sessão que este
    # módulo popula.
    import backend_client
    from config import BACKEND_URL

    try:
        resposta = backend_client.post(
            f'{BACKEND_URL}/api/funcionarios/login/', json=ADMIN_DO_DEMO
        )
    except Exception:
        return

    if resposta.status_code != 200:
        return

    dados = resposta.json()
    if dados.get('success'):
        session['funcionario'] = dados['funcionario']
        session['logged_in'] = True
