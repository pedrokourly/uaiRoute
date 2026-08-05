"""
Configurações do UaiRoute Frontend
"""
import os

# URL base do backend
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000')

# URLs das APIs
API_URLS = {
    'funcionarios': f'{BACKEND_URL}/api/funcionarios/',
    'veiculos': f'{BACKEND_URL}/api/veiculos/',
    'obras': f'{BACKEND_URL}/api/obras/',
    'alojamentos': f'{BACKEND_URL}/api/alojamento/',
    'ordens_servico': f'{BACKEND_URL}/api/ordens-servico/',
    'registros': f'{BACKEND_URL}/api/registros/',
}

# Configurações do Flask
CHAVE_DE_DESENVOLVIMENTO = 'uairoute-secret-key-2025'


def exigir_secret_key(debug, valor):
    """Ver a nota equivalente em backend/uairoute/settings.py.

    O cookie de sessão do Flask é assinado com esta chave: com o fallback
    versionado, qualquer pessoa forja uma sessão de administrador.
    """
    if valor:
        return valor
    if debug:
        return CHAVE_DE_DESENVOLVIMENTO
    raise RuntimeError(
        'SECRET_KEY é obrigatória quando DEBUG=False. '
        'Gere uma com: python -c "import secrets; print(secrets.token_urlsafe(50))"'
    )


DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
SECRET_KEY = exigir_secret_key(DEBUG, os.environ.get('SECRET_KEY'))

# IP do servidor para templates
SERVER_IP = os.environ.get('SERVER_IP', 'localhost')

# Função para disponibilizar configurações nos templates
def get_template_config():
    # BACKEND_URL não é mais publicado aqui: o browser não tem acesso ao
    # Django, e expor a URL interna só serviria para confundir.
    return {
        'SERVER_IP': SERVER_IP,
        'DEBUG': DEBUG
    }
