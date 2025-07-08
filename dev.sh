#!/bin/bash

# Script de desenvolvimento para UaiRoute
# Permite escolher entre execução local ou Docker

echo "🚚 UaiRoute - Script de Desenvolvimento"
echo "========================================"
echo ""
echo "Escolha uma opção:"
echo "1) Executar com Docker (Recomendado)"
echo "2) Executar localmente (Desenvolvimento)"
echo "3) Parar todos os serviços"
echo "4) Ver logs"
echo "5) Limpeza completa"
echo ""

read -p "Digite sua escolha (1-5): " choice

case $choice in
    1)
        echo "🐳 Iniciando com Docker..."
        if command -v make &> /dev/null; then
            make setup
        else
            docker-compose up -d
        fi
        echo ""
        echo "✅ UaiRoute executando!"
        echo "🌐 Frontend: http://localhost:5000"
        echo "🔧 Backend: http://localhost:8000"
        echo "👤 Login: admin@teste.com / admin"
        ;;
    2)
        echo "💻 Iniciando localmente..."
        echo "Certifique-se de que as dependências estão instaladas:"
        echo "pip install -r requirements.txt"
        echo ""
        echo "Inicie o backend em um terminal:"
        echo "cd backend && python manage.py runserver"
        echo ""
        echo "Inicie o frontend em outro terminal:"
        echo "cd frontend && python uairoute.py"
        ;;
    3)
        echo "🛑 Parando serviços..."
        if command -v make &> /dev/null; then
            make down
        else
            docker-compose down
        fi
        ;;
    4)
        echo "📋 Exibindo logs..."
        if command -v make &> /dev/null; then
            make logs
        else
            docker-compose logs -f
        fi
        ;;
    5)
        echo "🧹 Limpeza completa..."
        if command -v make &> /dev/null; then
            make clean
        else
            docker-compose down -v
            docker system prune -f
        fi
        ;;
    *)
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac
