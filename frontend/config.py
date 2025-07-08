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
