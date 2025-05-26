from flask import render_template, request, redirect, url_for
from uairoute import app
import requests

# Rotas para Veículos
@app.route('/veiculos')
def veiculos():
    response = requests.get('http://localhost:8000/api/veiculos/')
    if response.status_code == 200:
        veiculos = response.json()
        return render_template('veiculos/listar-veiculos.html', veiculos=veiculos)
    else:
        return render_template('veiculos/listar-veiculos.html', error="Erro ao buscar veículos.")

@app.route('/veiculos/cadastrar', methods=['GET', 'POST'])
def cadastrarVeiculo():
    if request.method == 'POST':
        veiculo = {
            'tipo': request.form['tipo'],
            'placa': request.form['placa'],
            'modelo': request.form.get('modelo', ''),
            'marca': request.form.get('marca', ''),
            'ano': request.form.get('ano', '')
        }
        try:
            response = requests.post('http://localhost:8000/api/veiculos/', json=veiculo)
            if response.status_code in [200, 201]:
                return redirect(url_for('veiculos'))
            else:
                return render_template('veiculos/cadastrar-veiculos.html', error='Erro ao cadastrar veículo.')
        except Exception as e:
            return render_template('veiculos/cadastrar-veiculos.html', error=str(e))
    return render_template('veiculos/cadastrar-veiculos.html')

@app.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
def editarVeiculo(id):
    if request.method == 'POST':
        veiculo = {
            'tipo': request.form['tipo'],
            'placa': request.form['placa'],
            'modelo': request.form.get('modelo', ''),
            'marca': request.form.get('marca', ''),
            'ano': request.form.get('ano', '')
        }
        try:
            response = requests.put(f'http://localhost:8000/api/veiculos/{id}/', json=veiculo)
            if response.status_code in [200, 204]:
                return redirect(url_for('veiculos'))
            else:
                return render_template('veiculos/editar-veiculos.html', veiculo=veiculo, error='Erro ao editar veículo.')
        except Exception as e:
            return render_template('veiculos/editar-veiculos.html', veiculo=veiculo, error=str(e))
    # GET: busca dados do veículo
    try:
        response = requests.get(f'http://localhost:8000/api/veiculos/{id}/')
        if response.status_code == 200:
            veiculo = response.json()
        else:
            veiculo = {}
    except Exception:
        veiculo = {}
    return render_template('veiculos/editar-veiculos.html', veiculo=veiculo)

@app.route('/veiculos/excluir/<int:id>', methods=['POST'])
def excluirVeiculo(id):
    try:
        response = requests.delete(f'http://localhost:8000/api/veiculos/{id}/')
        if response.status_code in [200, 204]:
            return redirect(url_for('veiculos'))
        else:
            return redirect(url_for('veiculos'))
    except Exception as e:
        return redirect(url_for('veiculos'))
