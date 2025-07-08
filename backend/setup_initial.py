#!/usr/bin/env python
"""
Script para inicializar o projeto UaiRoute
Este script deve ser executado na primeira vez que o projeto for configurado
"""

import os
import sys
import django

# Adiciona o diretório do projeto ao path
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uairoute.settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    
    print("=== Configuração Inicial do UaiRoute ===")
    print("1. Executando migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("\n2. Criando administrador padrão...")
    execute_from_command_line(['manage.py', 'create_admin'])
    
    print("\n=== Configuração completa! ===")
    print("Você pode agora iniciar o servidor com: python manage.py runserver")
    print("Dados do administrador:")
    print("Email: admin@teste.com")
    print("Senha: admin")
