from flask import render_template
from uairoute import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/obras')
def obras():
    return render_template('obras/lista-de-formulario.html')

@app.route('/obras/cadastrar')
def cadastrarObra():
    return render_template('obras/cadastrar.html')

@app.route('/veiculos')
def listaDeVeiculos():
    return render_template('veiculos/lista_De_Veiculos.html')