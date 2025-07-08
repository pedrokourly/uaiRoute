"""
Exemplo de como usar as configurações centralizadas do backend.

Para aplicar em todos os arquivos de rotas, substitua:
- 'http://localhost:8000/api/funcionarios/' por API_URLS['funcionarios']
- 'http://localhost:8000/api/veiculos/' por API_URLS['veiculos'] 
- etc.

Exemplo de importação no início de cada arquivo de rotas:
from config import API_URLS

Exemplo de uso:
response = requests.get(API_URLS['funcionarios'])
response = requests.get(f"{API_URLS['funcionarios']}{id}/")
"""
