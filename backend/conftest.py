# DATABASE_PATH (usado em produção para apontar o SQLite para o volume
# persistente do Docker, ver docker-compose.yml) não vaza para os testes:
# para o backend SQLite, o pytest-django força um banco de testes em
# memória (_get_test_db_name()) independentemente do NAME configurado em
# settings.DATABASES. Não há nada a limpar aqui -- este arquivo é mantido
# como ponto de extensão para fixtures futuras (ver Task 11).

import pytest


@pytest.fixture(autouse=True)
def demo_dir_temporario(tmp_path, settings):
    """DEMO_DIR aponta para /app/data, que só existe dentro do container."""
    settings.DEMO_DIR = str(tmp_path / "demos")
    settings.DEMO_SEED = str(tmp_path / "seed.sqlite3")
