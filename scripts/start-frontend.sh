#!/bin/bash

# Script de inicialização do frontend Flask

echo "🚀 Iniciando UaiRoute Frontend..."

# Aguardar backend estar pronto
echo "⏳ Aguardando backend estar disponível..."
sleep 5

# Verificar se backend está respondendo
while ! curl -s http://backend:8000/ > /dev/null; do
    echo "⏳ Aguardando backend..."
    sleep 2
done

echo "✅ Backend disponível!"

# Iniciar servidor Flask
echo "🌐 Iniciando servidor Flask na porta 5000..."
python uairoute.py
