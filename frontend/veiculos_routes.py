from flask import render_template, request, redirect, url_for
from uairoute import app
import requests

# Importar os decoradores de autenticação
from auth_routes import require_admin

# Rotas para Veículos
@app.route('/veiculos')
@require_admin
def veiculos():
    response = requests.get('http://localhost:8000/api/veiculos/')
    if response.status_code == 200:
        veiculos = response.json()
        return render_template('Veiculos/listar-veiculos.html', veiculos=veiculos)
    else:
        return render_template('Veiculos/listar-veiculos.html', error="Erro ao buscar veículos.")

@app.route('/veiculos/cadastrar', methods=['GET', 'POST'])
@require_admin
def cadastrarVeiculo():
    if request.method == 'POST':
        veiculo = {
            'tipo': request.form['tipo'],
            'placa': request.form['placa'],
            'capacidade': int(request.form.get('capacidade', 0)),
            'rua': request.form.get('rua', ''),
            'numero': request.form.get('numero', ''),
            'bairro': request.form.get('bairro', ''),
            'cidade': request.form.get('cidade', ''),
            'disponibilidade': 'disponibilidade' in request.form
        }
        
        try:
            response = requests.post('http://localhost:8000/api/veiculos/', json=veiculo)
            if response.status_code in [200, 201]:
                return redirect(url_for('veiculos'))
            else:
                error_msg = f"Erro ao cadastrar veículo. Status: {response.status_code}. Resposta: {response.text}"
                return render_template('Veiculos/cadastrar-veiculos.html', error=error_msg)
        except Exception as e:
            return render_template('Veiculos/cadastrar-veiculos.html', error=str(e))
    return render_template('Veiculos/cadastrar-veiculos.html')

@app.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
@require_admin
def editarVeiculo(id):
    if request.method == 'POST':
        veiculo = {
            'tipo': request.form['tipo'],
            'placa': request.form['placa'],
            'capacidade': int(request.form.get('capacidade', 0)),
            'rua': request.form.get('rua', ''),
            'numero': request.form.get('numero', ''),
            'bairro': request.form.get('bairro', ''),
            'cidade': request.form.get('cidade', ''),
            'disponibilidade': 'disponibilidade' in request.form
        }
        try:
            response = requests.put(f'http://localhost:8000/api/veiculos/{id}/', json=veiculo)
            if response.status_code in [200, 204]:
                return redirect(url_for('veiculos'))
            else:
                error_msg = f"Erro ao editar veículo. Status: {response.status_code}. Resposta: {response.text}"
                return render_template('Veiculos/editar-veiculos.html', veiculo=veiculo, error=error_msg)
        except Exception as e:
            return render_template('Veiculos/editar-veiculos.html', veiculo=veiculo, error=str(e))
    # GET: busca dados do veículo
    try:
        response = requests.get(f'http://localhost:8000/api/veiculos/{id}/')
        if response.status_code == 200:
            veiculo = response.json()
        else:
            veiculo = {}
    except Exception:
        veiculo = {}
    return render_template('Veiculos/editar-veiculos.html', veiculo=veiculo)

@app.route('/veiculos/excluir/<int:id>', methods=['POST'])
@require_admin
def excluirVeiculo(id):
    try:
        response = requests.delete(f'http://localhost:8000/api/veiculos/{id}/')
        if response.status_code in [200, 204]:
            return redirect(url_for('veiculos'))
        else:
            return redirect(url_for('veiculos'))
    except Exception as e:
        return redirect(url_for('veiculos'))
