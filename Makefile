# Makefile para UaiRoute

.PHONY: help build up down restart logs clean

# Ajuda
help:
	@echo "🚚 UaiRoute - Comandos Docker Disponíveis:"
	@echo ""
	@echo "  build     - Construir todas as imagens Docker"
	@echo "  up        - Iniciar todos os serviços"
	@echo "  down      - Parar todos os serviços"
	@echo "  restart   - Reiniciar todos os serviços"
	@echo "  logs      - Visualizar logs de todos os serviços"
	@echo "  clean     - Limpar containers, imagens e volumes"
	@echo "  backend   - Logs apenas do backend"
	@echo "  frontend  - Logs apenas do frontend"
	@echo ""

# Construir imagens
build:
	@echo "🔨 Construindo imagens Docker..."
	docker-compose build

# Iniciar serviços
up:
	@echo "🚀 Iniciando UaiRoute..."
	docker-compose up -d

# Parar serviços
down:
	@echo "🛑 Parando UaiRoute..."
	docker-compose down

# Reiniciar serviços
restart:
	@echo "🔄 Reiniciando UaiRoute..."
	docker-compose restart

# Ver logs
logs:
	@echo "📋 Logs do UaiRoute..."
	docker-compose logs -f

# Logs do backend
backend:
	@echo "📋 Logs do Backend..."
	docker-compose logs -f backend

# Logs do frontend
frontend:
	@echo "📋 Logs do Frontend..."
	docker-compose logs -f frontend

# Limpeza completa
clean:
	@echo "🧹 Limpando containers, imagens e volumes..."
	docker-compose down -v
	docker system prune -f
	docker volume prune -f

# Primeira execução (build + up)
setup: build up
	@echo "✅ UaiRoute configurado e executando!"
	@echo "🌐 Frontend: http://localhost:5000"
	@echo "🔧 Backend API: http://localhost:8000"
	@echo "👤 Admin: admin@teste.com / admin"
