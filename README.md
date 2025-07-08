# 🚚 UaiRoute - Sistema de Gestão de Rotas e Logística

> Sistema completo para gerenciamento de funcionários, veículos, obras e otimização de rotas logísticas, desenvolvido com Django REST Framework e Flask.

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.1-green.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.1-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Sobre o Projeto

O **UaiRoute** é um sistema web completo para gerenciamento de operações logísticas, permitindo:

- 👥 Gestão de funcionários e alojamentos
- 🚗 Controle de veículos e sua disponibilidade
- 🏗️ Cadastro e monitoramento de obras
- 📋 Criação e acompanhamento de ordens de serviço
- 🗺️ Visualização de rotas otimizadas em mapas interativos
- 📍 Geocodificação automática de endereços

## 🏗️ Arquitetura

O projeto possui uma arquitetura modular dividida em:

### Backend (Django REST API)
- **Framework**: Django 5.2.1 + Django REST Framework
- **Banco de Dados**: SQLite (desenvolvimento)
- **Autenticação**: Sistema personalizado com sessões
- **APIs**: RESTful para todas as entidades

### Frontend (Flask Web App)
- **Framework**: Flask 3.1.1
- **Templates**: Jinja2 com HTML5/CSS3/JavaScript
- **Mapas**: Integração com OpenStreetMap
- **Interface**: Responsiva e moderna

## 📁 Estrutura do Projeto

```
uaiRoute/
├── backend/                    # API Django
│   ├── api/                   # Apps da API
│   │   ├── alojamento/        # Gestão de alojamentos
│   │   ├── funcionarios/      # Gestão de funcionários
│   │   ├── obras/             # Gestão de obras
│   │   ├── ordens_servico/    # Ordens de serviço
│   │   ├── registros/         # Sistema de cadastro
│   │   ├── utils/             # Utilitários (geocoding)
│   │   └── veiculos/          # Gestão de veículos
│   ├── uairoute/              # Configurações Django
│   ├── db.sqlite3             # Banco de dados
│   └── manage.py              # CLI Django
├── frontend/                   # Interface Flask
│   ├── templates/             # Templates HTML
│   ├── static/                # CSS, JS, imagens
│   ├── routes.py              # Rotas principais
│   ├── auth_routes.py         # Autenticação
│   ├── config.py              # Configurações centralizadas
│   └── *_routes.py            # Rotas específicas
├── scripts/                    # Scripts de inicialização
│   ├── start-backend.sh       # Script do backend
│   └── start-frontend.sh      # Script do frontend
├── docker-compose.yml         # Orquestração Docker
├── Dockerfile.backend         # Imagem do Django
├── Dockerfile.frontend        # Imagem do Flask
├── Makefile                   # Comandos facilitados
├── .dockerignore              # Arquivos ignorados no Docker
├── .env.example               # Exemplo de variáveis de ambiente
├── requirements.txt           # Dependências Python
└── README_SETUP.md           # Guia de configuração
```

## ✨ Funcionalidades

### 🔐 Sistema de Autenticação
- Login seguro para funcionários e administradores
- Níveis de acesso diferenciados
- Sessões persistentes

### 👥 Gestão de Funcionários
- Cadastro completo de funcionários
- Vinculação a alojamentos
- Controle de permissões (admin/funcionário comum)
- Validação de capacidade de alojamentos

### 🏠 Gestão de Alojamentos
- Cadastro de alojamentos com endereço completo
- Controle de capacidade máxima
- Geocodificação automática de coordenadas
- Gestão de vagas disponíveis

### 🚗 Gestão de Veículos
- Cadastro de diferentes tipos de veículos
- Controle de disponibilidade
- Informações de capacidade e localização
- Coordenadas geográficas automáticas

### 🏗️ Gestão de Obras
- Cadastro de obras com localização
- Endereçamento completo
- Coordenadas automáticas via geocoding

### 📋 Ordens de Serviço
- Criação de ordens com múltiplas paradas
- Vinculação de veículos e destinos
- Controle de status (pendente, andamento, concluída)
- Cálculo automático de rotas otimizadas
- Estimativas de tempo e distância

### 🗺️ Sistema de Mapas
- Visualização interativa de rotas
- Marcadores para alojamentos, obras e veículos
- Integração com OpenStreetMap
- Cálculo de rotas otimizadas

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.12+ (para execução local)
- Docker e Docker Compose (para execução containerizada)
- pip (gerenciador de pacotes Python)

### 🐳 Executar com Docker (Recomendado)

#### Opção 1: Usando Docker Compose
```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/uairoute.git
cd uairoute

# 2. Execute com Docker Compose
docker-compose up -d

# 3. Acesse o sistema
# Frontend: http://localhost:5000
# Backend API: http://localhost:8000
```

#### Opção 2: Usando Makefile (mais fácil)
```bash
# Primeira execução (build + start)
make setup

# Comandos úteis
make up      # Iniciar serviços
make down    # Parar serviços
make logs    # Ver logs
make restart # Reiniciar
make clean   # Limpeza completa
```

### 💻 Executar Localmente (Desenvolvimento)

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/uairoute.git
cd uairoute
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o Backend (Django)
```bash
cd backend

# Execute as migrações
python manage.py migrate

# Inicie o servidor (criará admin automaticamente)
python manage.py runserver
```

### 4. Configure o Frontend (Flask)
```bash
cd frontend

# Inicie o servidor Flask
python uairoute.py
```

### 5. Acesse o sistema
- **Frontend**: http://localhost:5000
- **API Django**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

### 👤 Usuário Padrão
- **Email**: admin@teste.com
- **Senha**: admin
- **Tipo**: Administrador

## 🔧 Configuração Avançada

### 🐳 Docker
O projeto inclui configuração completa para Docker:

#### Arquivos Docker
- `Dockerfile.backend` - Imagem do Django
- `Dockerfile.frontend` - Imagem do Flask  
- `docker-compose.yml` - Orquestração dos serviços
- `Makefile` - Comandos facilitados
- `.dockerignore` - Arquivos ignorados no build

#### Volumes
- `backend_data:/app/data` - Dados persistentes do backend
- `./backend/db.sqlite3:/app/db.sqlite3` - Banco de dados

#### Rede
- `uairoute-network` - Rede interna para comunicação entre serviços

### Variáveis de Ambiente
Crie um arquivo `.env` no diretório raiz baseado no `.env.example`:
```env
# Desenvolvimento local
DEBUG=True
SERVER_IP=localhost
BACKEND_URL=http://localhost:8000

# Docker
# DEBUG=True
# SERVER_IP=backend  
# BACKEND_URL=http://backend:8000
```

### Banco de Dados
O projeto usa SQLite por padrão. Para produção, configure PostgreSQL ou MySQL no `settings.py`.

### APIs Externas
- **Geocoding**: Utiliza a API gratuita do OpenStreetMap (Nominatim)
- **Mapas**: Integração com Leaflet.js e OpenStreetMap

## 📊 API Endpoints

### Funcionários
- `GET/POST /api/funcionarios/` - Listar/Criar funcionários
- `GET/PUT/DELETE /api/funcionarios/{id}/` - Detalhes/Editar/Excluir
- `POST /api/funcionarios/login/` - Autenticação

### Veículos
- `GET/POST /api/veiculos/` - Listar/Criar veículos
- `GET/PUT/DELETE /api/veiculos/{id}/` - Detalhes/Editar/Excluir

### Obras
- `GET/POST /api/obras/` - Listar/Criar obras
- `GET/PUT/DELETE /api/obras/{id}/` - Detalhes/Editar/Excluir

### Alojamentos
- `GET/POST /api/alojamento/` - Listar/Criar alojamentos
- `GET/PUT/DELETE /api/alojamento/{id}/` - Detalhes/Editar/Excluir

### Ordens de Serviço
- `GET/POST /api/ordens-servico/` - Listar/Criar ordens
- `GET/PUT/DELETE /api/ordens-servico/{id}/` - Detalhes/Editar/Excluir
- `GET /api/ordens-servico/{id}/rota/` - Obter rota otimizada
- `GET /api/ordens-servico/funcionario/{id}/` - Ordens por funcionário

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2.1** - Framework web principal
- **Django REST Framework 3.16.0** - API REST
- **django-cors-headers 4.7.0** - CORS para frontend
- **SQLite** - Banco de dados (desenvolvimento)

### Frontend
- **Flask 3.1.1** - Framework web para interface
- **Jinja2 3.1.6** - Engine de templates
- **Requests 2.32.3** - Cliente HTTP para API
- **HTML5/CSS3/JavaScript** - Interface do usuário
- **Leaflet.js** - Mapas interativos

### Utilitários
- **OpenStreetMap Nominatim** - Geocodificação
- **Werkzeug 3.1.3** - Utilitários WSGI

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Comandos Úteis

### 🐳 Docker Commands
```bash
# Build e inicialização
make setup          # Primeira execução (build + up)
make build          # Construir imagens
make up             # Iniciar serviços
make down           # Parar serviços

# Monitoramento
make logs           # Ver todos os logs
make backend        # Logs apenas do backend
make frontend       # Logs apenas do frontend

# Manutenção
make restart        # Reiniciar serviços
make clean          # Limpeza completa (containers, imagens, volumes)

# Docker Compose direto
docker-compose up -d                    # Iniciar em background
docker-compose logs -f                  # Ver logs em tempo real
docker-compose exec backend bash       # Acessar container do backend
docker-compose exec frontend bash      # Acessar container do frontend
```

### Django (Backend)
```bash
# Desenvolvimento local
python manage.py makemigrations        # Criar migrações
python manage.py migrate               # Aplicar migrações
python manage.py createsuperuser       # Criar superusuário
python manage.py collectstatic         # Coletar arquivos estáticos
python manage.py shell                 # Shell Django

# Docker
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py shell
```

### Flask (Frontend)
```bash
# Desenvolvimento local
python uairoute.py                      # Executar com debug
python uairoute.py --host 0.0.0.0 --port 5000  # IP específico

# Docker
docker-compose restart frontend        # Reiniciar apenas frontend
docker-compose logs -f frontend        # Logs do frontend
```

## 🐛 Resolução de Problemas

### 🐳 Docker
**Containers não iniciam:**
```bash
make down && make clean && make setup
```

**Erro de porta ocupada:**
```bash
# Verificar portas em uso
netstat -tulpn | grep :5000
netstat -tulpn | grep :8000

# Parar containers e tentar novamente
make down && make up
```

**Problemas de permissão:**
```bash
sudo chown -R $USER:$USER .
```

### Erro de CORS
Verifique se `django-cors-headers` está instalado e configurado no `settings.py`.

### Erro de Geocoding
A API do OpenStreetMap tem limite de requisições. Aguarde alguns segundos entre requisições.

### Erro de Conexão Backend/Frontend
```bash
# Verificar se serviços estão rodando
docker-compose ps

# Verificar logs
make logs

# Verificar conectividade interna
docker-compose exec frontend curl http://backend:8000/
```

### Banco de Dados
```bash
# Resetar migrações (cuidado em produção!)
docker-compose exec backend python manage.py migrate --fake-initial

# Backup do banco
docker cp uairoute-backend:/app/db.sqlite3 ./backup_db.sqlite3
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🐳 Docker Details

### Imagens Docker
- **Backend**: `uairoute-backend` (Django + SQLite)
- **Frontend**: `uairoute-frontend` (Flask + Templates)

### Arquitetura Docker
```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   Flask:5000    │◄──►│   Django:8000   │
│                 │    │                 │
├─────────────────┤    ├─────────────────┤
│ • Templates     │    │ • REST API      │
│ • Static Files  │    │ • SQLite DB     │
│ • Routes        │    │ • Migrations    │
└─────────────────┘    └─────────────────┘
```

### Volumes Persistentes
- **Database**: `./backend/db.sqlite3` → `/app/db.sqlite3`
- **Backend Data**: `backend_data` volume para dados persistentes

### Configuração de Rede
- **Network**: `uairoute-network` (bridge)
- **Comunicação**: Frontend conecta em `http://backend:8000`
- **Exposição**: Frontend na porta 5000, Backend na porta 8000

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
