from flask import render_template
from uairoute import app

import obras_routes
import veiculos_routes
import funcionarios_routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mapa')
def map():
    return render_template('mapa.html')