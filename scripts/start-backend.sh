#!/bin/bash

# Script de inicialização do backend Django

echo "🚀 Iniciando UaiRoute Backend..."

# Aguardar um pouco para garantir que tudo esteja pronto
sleep 2

# Executar migrações
echo "📦 Executando migrações..."
python manage.py migrate

# Criar usuário admin se não existir (já está no manage.py)
echo "👤 Verificando usuário administrador..."

# Iniciar servidor
echo "🌐 Iniciando servidor Django na porta 8000..."
python manage.py runserver 0.0.0.0:8000
