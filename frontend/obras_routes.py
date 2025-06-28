from flask import render_template, request, redirect, url_for
from uairoute import app
import requests

# Importar os decoradores de autenticação
from auth_routes import require_admin

# Rotas para Obras
@app.route('/obras')
@require_admin
def obras():
    response = requests.get('http://localhost:8000/api/obras/')
    if response.status_code == 200:
        obras = response.json()
        return render_template('obras/listar-obras.html', obras=obras)
    else:
        return render_template('obras/listar-obras.html', error="Erro ao buscar obras.")

@app.route('/obras/cadastrar', methods=['GET', 'POST'])
@require_admin
def cadastrarObra():
    if request.method == 'POST':
        obra = {
            'nome': request.form['nome'],
            'rua': request.form['rua'],
            'numero': request.form['numero'],
            'bairro': request.form['bairro'],
            'cidade': request.form['cidade']
        }
        
        try:
            response = requests.post('http://localhost:8000/api/obras/', json=obra)
            if response.status_code in [200, 201]:
                return redirect(url_for('obras'))
            else:
                return render_template('obras/cadastrar-obras.html', error='Erro ao cadastrar obra.')
        except Exception as e:
            return render_template('obras/cadastrar-obras.html', error=str(e))
    return render_template('obras/cadastrar-obras.html')

@app.route('/obras/editar/<int:id>', methods=['GET', 'POST'])
@require_admin
def editarObra(id):
    if request.method == 'POST':
        obra = {
            'nome': request.form['nome'],
            'rua': request.form['rua'],
            'numero': request.form['numero'],
            'bairro': request.form['bairro'],
            'cidade': request.form['cidade']
        }
        try:
            response = requests.put(f'http://localhost:8000/api/obras/{id}/', json=obra)
            if response.status_code in [200, 204]:
                return redirect(url_for('obras'))
            else:
                return render_template('obras/editar-obras.html', obra=obra, error='Erro ao editar obra.')
        except Exception as e:
            return render_template('obras/editar-obras.html', obra=obra, error=str(e))
    # GET: busca dados da obra
    try:
        response = requests.get(f'http://localhost:8000/api/obras/{id}/')
        if response.status_code == 200:
            obra = response.json()
        else:
            obra = {}
    except Exception:
        obra = {}
    return render_template('obras/editar-obras.html', obra=obra)

@app.route('/obras/excluir/<int:id>', methods=['POST'])
@require_admin
def excluirObra(id):
    try:
        response = requests.delete(f'http://localhost:8000/api/obras/{id}/')
        if response.status_code in [200, 204]:
            return redirect(url_for('obras'))
        else:
            return redirect(url_for('obras'))
    except Exception as e:
        return redirect(url_for('obras'))
