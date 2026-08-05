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
│   ├── db.sqlite3             # Banco de dados (execução local sem Docker)
│   └── manage.py              # CLI Django
├── frontend/                   # Interface Flask
│   ├── templates/             # Templates HTML
│   ├── static/                # CSS, JS, imagens
│   ├── routes.py              # Rotas principais
│   ├── auth_routes.py         # Autenticação
│   ├── config.py              # Configurações centralizadas
│   └── *_routes.py            # Rotas específicas
├── docker-compose.yml         # Orquestração Docker
├── Dockerfile.backend         # Imagem do Django
├── Dockerfile.frontend        # Imagem do Flask
├── .dockerignore              # Arquivos ignorados no Docker
├── .env.example               # Exemplo de variáveis de ambiente
└── requirements.txt           # Dependências Python
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

Não é preciso criar arquivos nem preparar o banco antes: o Compose sobe tudo a
partir de um clone limpo.

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/uairoute.git
cd uairoute

# 2. Suba os serviços (desenvolvimento)
docker-compose up -d --build

# 3. Acesse o sistema
# Frontend: http://localhost:5000
```

No primeiro start o backend aplica as migrações e cria o administrador padrão
automaticamente — acompanhe por `docker-compose logs -f backend`. O frontend só
sobe depois que o backend passa no healthcheck.

**Nota de Segurança:** O backend Django não é publicado no host — não é acessível
em `localhost:8000`. É um serviço interno que só o frontend (Flask) alcança,
dentro da rede do Docker Compose, em `http://backend:8000`. Isso impede acesso
não autenticado direto à API.

### 💻 Executar Localmente (Desenvolvimento)

```bash
# 1. Clone e instale as dependências
git clone https://github.com/seu-usuario/uairoute.git
cd uairoute
pip install -r requirements.txt

# 2. Backend Django (um terminal)
cd backend
python manage.py migrate
python manage.py runserver     # cria o admin padrão automaticamente

# 3. Frontend Flask (outro terminal)
cd frontend
python uairoute.py
```

Sem a variável `DATABASE_PATH`, o Django usa `backend/db.sqlite3` — nenhuma
configuração extra é necessária para rodar fora do Docker.

### 🌐 Acessos (Desenvolvimento)

- **Frontend**: http://localhost:5000

No modo desenvolvimento local (sem Docker), a API também fica acessível:

- **API Django**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

### 🚀 Stack de Produção

Para publicar em produção, use:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

**Requisito obrigatório:** a variável `SECRET_KEY` deve estar definida no ambiente.
Gere uma chave segura com:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

E defina no `.env` ou passe ao Compose:

```bash
export SECRET_KEY="sua-chave-gerada-acima"
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

O `docker-compose.prod.yml` sobrescreve `DEBUG=False`, força `SECRET_KEY`, e
executa ambos os apps sob Gunicorn com múltiplos workers. O banco continua no
volume nomeado `backend_data`.

### 👤 Usuário Padrão

Criado automaticamente na primeira execução do `runserver`, em ambos os modos:

| Campo | Valor             |
| ----- | ----------------- |
| Email | `admin@teste.com` |
| Senha | `admin`           |
| Tipo  | Administrador     |

Se preferir criar o administrador manualmente, ou se algo falhar no bootstrap
automático:

```bash
python manage.py create_admin      # apenas o administrador
python manage.py setup_initial     # migrations + administrador

# Via Docker
docker-compose exec backend python manage.py create_admin
```

Para alterar as credenciais padrão, edite `setup_admin_if_needed()` em
[`backend/manage.py`](backend/manage.py) ou o comando em
`backend/api/funcionarios/management/commands/create_admin.py`.

## 🔧 Configuração Avançada

### 🐳 Docker
O projeto inclui configuração completa para Docker:

#### Arquivos Docker
- `Dockerfile.backend` - Imagem do Django
- `Dockerfile.frontend` - Imagem do Flask  
- `docker-compose.yml` - Orquestração dos serviços
- `.dockerignore` - Arquivos ignorados no build

#### Volumes

- `backend_data:/app/data` - Volume nomeado com o banco SQLite (`/app/data/db.sqlite3`)

O banco fica **dentro** do volume nomeado, não em um bind mount de arquivo.
Isso é proposital: um bind mount como `./backend/db.sqlite3:/app/db.sqlite3`
quebra em clone limpo, porque o arquivo está no `.gitignore` e o Docker cria um
diretório vazio no lugar dele.

#### Rede
- `uairoute-network` - Rede interna para comunicação entre serviços

### Variáveis de Ambiente

O backend lê toda a configuração sensível do ambiente. Com Docker Compose os
valores já vêm definidos nos arquivos `docker-compose*.yml`; para execução local
ou para sobrescrever em produção, crie um `.env` na raiz baseado no `.env.example`.

#### Backend (Django)

| Variável | Padrão (dev, `DEBUG=True`) | Obrigatório em produção | Descrição |
| -------- | -------------------------- | ---------------------- | --------- |
| `SECRET_KEY` | chave insegura versionada | ✓ Sim | Chave para assinar sessões e tokens. Gere com `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DEBUG` | `True` | — | `True`/`False` para modo debug |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | — | Hosts permitidos, separados por vírgula. Inclua `backend` para Docker. |
| `CSRF_TRUSTED_ORIGINS` | `http://localhost:5000,http://127.0.0.1:5000` | — | Origens confiáveis para CSRF, separadas por vírgula |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5000,http://127.0.0.1:5000` | — | Origens permitidas para CORS (requisições do frontend), separadas por vírgula |
| `DATABASE_PATH` | `backend/db.sqlite3` | — | Caminho do SQLite. No Docker aponta para `/app/data/db.sqlite3` (volume persistente) |
| `ORS_API_KEY` | (vazio) | — | Chave da OpenRouteService para cálculo de rotas (veja abaixo) |

#### Frontend (Flask)

| Variável | Padrão (dev) | Descrição |
| -------- | ------------ | --------- |
| `BACKEND_URL` | `http://localhost:8000` | URL da API Django. No Docker use `http://backend:8000` |
| `SERVER_IP` | `localhost` | IP/hostname para bind do Flask. Use `0.0.0.0` em produção ou Docker. |
| `DEBUG` | `True` | Modo debug |
| `SECRET_KEY` | (lê do backend) | Em produção, deve ser a mesma do backend |
| `ORS_API_KEY` | (vazio) | Chave da OpenRouteService (veja abaixo) |

#### OpenRouteService (`ORS_API_KEY`)

A chave da OpenRouteService é usada para calcular rotas otimizadas nas ordens
de serviço. Antes era hardcoded no template do frontend; agora é uma variável
de ambiente lida tanto pelo **backend** (ao criar/editar ordens) quanto pelo
**frontend** (ao visualizar ordens).

Sem a chave:
- O backend não calcula `distancia_total` e `tempo_estimado`
- O frontend retorna erro 503 ao tentar visualizar a rota

Obtenha uma chave gratuita em https://openrouteservice.org/dev/#/signup
e defina em `ORS_API_KEY` no `.env` ou na stack de produção.

### Banco de Dados
O projeto usa SQLite por padrão. Para produção, configure PostgreSQL ou MySQL no `settings.py`.

### APIs Externas
- **Geocoding**: Utiliza a API gratuita do OpenStreetMap (Nominatim)
- **Mapas**: Integração com Leaflet.js e OpenStreetMap

## 🧪 Testes

O projeto inclui suítes de testes para backend e frontend usando `pytest` e
`pytest-django`.

### Executar Testes

```bash
# Testes do backend
cd backend
python -m pytest -v

# Testes do frontend
cd frontend
python -m pytest -v
```

Cada diretório tem seu próprio `pytest.ini` com configurações específicas.

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
docker-compose up -d --build            # Primeira execução (build + start)
docker-compose up -d                    # Iniciar em background
docker-compose down                     # Parar serviços
docker-compose restart                  # Reiniciar serviços

# Monitoramento
docker-compose ps                       # Status dos containers
docker-compose logs -f                  # Ver logs em tempo real
docker-compose logs -f backend          # Logs apenas do backend
docker-compose logs -f frontend         # Logs apenas do frontend

# Acesso aos containers
docker-compose exec backend bash        # Shell no backend
docker-compose exec frontend bash       # Shell no frontend

# Limpeza (⚠️ o -v apaga o volume com o banco de dados)
docker-compose down -v
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
docker-compose down && docker-compose up -d --build
```

**Erro de porta ocupada:**
```bash
# Verificar porta em uso (só o frontend expõe porta no host; o backend
# é interno e não publica a 8000)
netstat -tulpn | grep :5000

# Parar containers e tentar novamente
docker-compose down && docker-compose up -d
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
docker-compose logs -f

# Verificar conectividade interna
docker-compose exec frontend curl http://backend:8000/
```

### Banco de Dados
```bash
# Resetar migrações (cuidado em produção!)
docker-compose exec backend python manage.py migrate --fake-initial

# Backup do banco (vive no volume backend_data)
docker cp uairoute-backend:/app/data/db.sqlite3 ./backup_db.sqlite3

# Restaurar um backup
docker cp ./backup_db.sqlite3 uairoute-backend:/app/data/db.sqlite3
docker-compose restart backend
```

**Atenção:** `docker-compose down -v` remove o volume `backend_data` e, com ele,
o banco. Faça o backup acima antes. Sem o `-v`, os dados são preservados.

## 🎯 Branch `demo`

Existe uma branch `demo` que estende o trabalho desta branch (`seguranca`/`produto`).
A branch `demo` implementa um modo isolado por visitante: cada acesso anônimo
(sem login) cria uma sessão isolada com dados de teste, sem afetar o estado
compartilhado dos usuários autenticados.

Esta branch (`seguranca`) representa o estado base (modo "produto" compartilhado),
enquanto a branch `demo` constrói sobre ela para adicionar a experiência isolada
de demonstração.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🐳 Docker Details

### Imagens Docker
- **Backend**: `uairoute-backend` (Django + SQLite)
- **Frontend**: `uairoute-frontend` (Flask + Templates)

### Arquitetura Docker

```
┌────────────────────────────────────────────────────────┐
│  uairoute-network (bridge)                             │
│                                                         │
│  ┌─────────────────┐              ┌─────────────────┐  │
│  │   Frontend      │              │    Backend      │  │
│  │   Flask:5000    │─────────────►│   Django:8000   │  │
│  │  (publicado)    │              │  (interno)      │  │
│  ├─────────────────┤              ├─────────────────┤  │
│  │ • Templates     │              │ • REST API      │  │
│  │ • Static Files  │              │ • SQLite DB     │  │
│  │ • Routes        │              │ • Migrations    │  │
│  └─────────────────┘              └─────────────────┘  │
│         ▲                                                │
│         │ :5000                                          │
│    (host)                                               │
└────────────────────────────────────────────────────────┘
```

**Acesso:**
- **Frontend**: Publicado em `:5000` no host (acessível externamente)
- **Backend**: Interno apenas — não publicado no host. Acessível dentro da rede
  Compose via `http://backend:8000` (do frontend) ou via Docker Compose exec

### Volumes Persistentes

- **Database**: volume nomeado `backend_data` → `/app/data/db.sqlite3`

### Configuração de Rede

- **Network**: `uairoute-network` (bridge)
- **Comunicação**: Frontend conecta em `http://backend:8000`
- **Exposição**: Apenas Frontend publicado na porta 5000. Backend é interno.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
