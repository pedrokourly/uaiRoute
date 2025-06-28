import os
from flask import render_template, session, redirect, url_for
from uairoute import app

import obras_routes
import veiculos_routes
import funcionarios_routes
import alojamentos_routes
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
    
    # Se for funcionário comum, redirecionar para o mapa
    return redirect(url_for('mapa'))

@app.route('/home')
@require_admin
def home():
    return render_template('home.html')

@app.route('/mapa')
@require_login
def mapa():
    server_ip = os.environ.get('SERVER_IP')
    return render_template('mapa.html', server_ip=server_ip)