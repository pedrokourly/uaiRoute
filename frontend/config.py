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
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY', 'uairoute-secret-key-2025')

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
