import os
import time
from pathlib import Path

import pytest
from django.core.management import call_command


def _criar_banco(diretorio, nome, idade_horas=0):
    diretorio.mkdir(parents=True, exist_ok=True)
    caminho = diretorio / f"{nome}.sqlite3"
    caminho.write_bytes(b"fake")
    if idade_horas:
        antigo = time.time() - idade_horas * 3600
        os.utime(caminho, (antigo, antigo))
    return caminho


def test_apaga_os_antigos_e_preserva_os_recentes(settings, tmp_path):
    settings.DEMO_DIR = str(tmp_path / "demos")
    diretorio = Path(settings.DEMO_DIR)
    velho = _criar_banco(diretorio, "a" * 32, idade_horas=48)
    novo = _criar_banco(diretorio, "b" * 32, idade_horas=1)

    call_command("limpar_demos", "--idade-horas", "24")

    assert not velho.exists()
    assert novo.exists()


def test_teto_remove_os_mais_antigos_primeiro(settings, tmp_path):
    settings.DEMO_DIR = str(tmp_path / "demos")
    settings.DEMO_MAX_BANCOS = 2
    diretorio = Path(settings.DEMO_DIR)
    _criar_banco(diretorio, "a" * 32, idade_horas=3)
    _criar_banco(diretorio, "b" * 32, idade_horas=2)
    recente = _criar_banco(diretorio, "c" * 32, idade_horas=1)

    call_command("limpar_demos", "--idade-horas", "24")

    assert len(list(diretorio.glob("*.sqlite3"))) == 2
    assert recente.exists()


def test_diretorio_inexistente_nao_quebra(settings, tmp_path):
    settings.DEMO_DIR = str(tmp_path / "nao-existe")
    call_command("limpar_demos", "--idade-horas", "24")
