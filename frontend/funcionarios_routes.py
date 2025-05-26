from flask import render_template, request, redirect, url_for
from uairoute import app
import requests

# Rotas para Funcionários
@app.route('/funcionarios')
def funcionarios():
    response = requests.get('http://localhost:8000/api/funcionarios/')
    if response.status_code == 200:
        funcionarios = response.json()
        return render_template('funcionarios/listar-funcionario.html', funcionarios=funcionarios)
    else:
        return render_template('funcionarios/listar-funcionario.html', error="Erro ao buscar funcionários.")

@app.route('/funcionarios/cadastrar', methods=['GET', 'POST'])
def cadastrarFuncionario():
    if request.method == 'POST':
        funcionario = {
            'nome': request.form['nome'],
            'email': request.form.get('email', ''),
            'cargo': request.form.get('cargo', ''),
            'telefone': request.form.get('telefone', '')
        }
        try:
            response = requests.post('http://localhost:8000/api/funcionarios/', json=funcionario)
            if response.status_code in [200, 201]:
                return redirect(url_for('funcionarios'))
            else:
                return render_template('funcionarios/cadastrar-funcionario.html', error='Erro ao cadastrar funcionário.')
        except Exception as e:
            return render_template('funcionarios/cadastrar-funcionario.html', error=str(e))
    return render_template('funcionarios/cadastrar-funcionario.html')

@app.route('/funcionarios/editar/<int:id>', methods=['GET', 'POST'])
def editarFuncionario(id):
    if request.method == 'POST':
        funcionario = {
            'nome': request.form['nome'],
            'email': request.form.get('email', ''),
            'cargo': request.form.get('cargo', ''),
            'telefone': request.form.get('telefone', '')
        }
        try:
            response = requests.put(f'http://localhost:8000/api/funcionarios/{id}/', json=funcionario)
            if response.status_code in [200, 204]:
                return redirect(url_for('funcionarios'))
            else:
                return render_template('funcionarios/editar-funcionario.html', funcionario=funcionario, error='Erro ao editar funcionário.')
        except Exception as e:
            return render_template('funcionarios/editar-funcionario.html', funcionario=funcionario, error=str(e))
    # GET: busca dados do funcionário
    try:
        response = requests.get(f'http://localhost:8000/api/funcionarios/{id}/')
        if response.status_code == 200:
            funcionario = response.json()
        else:
            funcionario = {}
    except Exception:
        funcionario = {}
    return render_template('funcionarios/editar-funcionario.html', funcionario=funcionario)

@app.route('/funcionarios/excluir/<int:id>', methods=['POST'])
def excluirFuncionario(id):
    try:
        response = requests.delete(f'http://localhost:8000/api/funcionarios/{id}/')
        if response.status_code in [200, 204]:
            return redirect(url_for('funcionarios'))
        else:
            return redirect(url_for('funcionarios'))
    except Exception as e:
        return redirect(url_for('funcionarios'))
