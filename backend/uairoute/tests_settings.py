import pytest
from django.core.exceptions import ImproperlyConfigured

from uairoute.settings import exigir_secret_key


def test_em_dev_o_fallback_e_aceito():
    assert exigir_secret_key(debug=True, valor=None) is not None


def test_em_producao_sem_chave_falha():
    with pytest.raises(ImproperlyConfigured, match="SECRET_KEY"):
        exigir_secret_key(debug=False, valor=None)


def test_em_producao_com_chave_a_devolve():
    assert exigir_secret_key(debug=False, valor="chave-real") == "chave-real"
