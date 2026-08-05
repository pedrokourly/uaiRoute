import pytest
from django.test import Client

from uairoute.demo_middleware import IdDeDemoInvalido, caminho_do_banco


def test_id_valido_gera_caminho_dentro_do_diretorio():
    caminho = caminho_do_banco("a" * 32)
    assert caminho.name == "a" * 32 + ".sqlite3"
    assert caminho.parent.name == "demos"


@pytest.mark.parametrize("id_ruim", [
    "../../etc/passwd",
    "a" * 31,
    "a" * 33,
    "A" * 32,          # maiúsculas não são hexadecimal do uuid4().hex
    "z" * 32,
    "",
    "a" * 30 + "/x",
    "a" * 32 + "\n",   # \Z rejeita trailing newlines ($ deixaria passar)
])
def test_ids_invalidos_sao_recusados(id_ruim):
    with pytest.raises(IdDeDemoInvalido):
        caminho_do_banco(id_ruim)


def test_health_nao_exige_header(client):
    assert client.get("/health/").status_code == 200


def test_api_sem_header_responde_400():
    assert Client().get("/api/funcionarios/").status_code == 400
