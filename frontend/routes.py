import os
import requests
from flask import render_template, session, redirect, url_for, jsonify
from uairoute import app

import obras_routes
import veiculos_routes
import funcionarios_routes
import alojamentos_routes
import ordens_servico_routes
import auth_routes

# Importar os decoradores de autenticação
from auth_routes import require_login, require_admin

@app.route('/')
def index():
    # Se não estiver logado, redirecionar para login
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Se for admin, mostrar homepage completa
    if session.get('funcionario', {}).get('is_admin'):
        return redirect(url_for('home'))
    
    # Se for funcionário comum, redirecionar para suas ordens
    return redirect(url_for('minhas_ordens'))

@app.route('/home')
@require_admin
def home():
    return render_template('home.html')

@app.route('/mapa')
@require_login
def mapa():
    funcionario = session.get('funcionario')
    
    # Apenas admins podem acessar o mapa
    if not funcionario or not funcionario.get('is_admin', False):
        return redirect(url_for('minhas_ordens'))
    
    ordens_servico = []
    error = None
    
    if funcionario:
        try:
            # Buscar ordens de serviço relacionadas ao alojamento do funcionário
            response = requests.get(f'http://localhost:8000/api/ordens-servico/funcionario/{funcionario["id"]}/')
            if response.status_code == 200:
                data = response.json()
                ordens_servico = data.get('ordens', [])
            else:
                error = "Erro ao carregar ordens de serviço"
        except Exception as e:
            error = f"Erro de conexão: {str(e)}"
    
    server_ip = os.environ.get('SERVER_IP')
    return render_template('mapa.html', 
                         server_ip=server_ip, 
                         funcionario=funcionario,
                         ordens_servico=ordens_servico,
                         error=error)

@app.route('/debug-sessao')
def debug_sessao():
    return jsonify({
        'logged_in': session.get('logged_in', False),
        'funcionario': session.get('funcionario', None)
    })