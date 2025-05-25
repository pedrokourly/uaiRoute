from flask import render_template, request, redirect, url_for
from uairoute import app
import requests

@app.route('/')
def home():
    return render_template('home.html')



# Rotas para Obras
@app.route('/obras')
def obras():
    response = requests.get('http://localhost:8000/api/obras/')
    if response.status_code == 200:
        obras = response.json()
        return render_template('obras/listar-obras.html', obras=obras)
    else:
        return render_template('obras/listar-obras.html', error="Erro ao buscar obras.")

@app.route('/obras/cadastrar', methods=['GET', 'POST'])
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
            obra = {
                'id': id,
                'nome': '',
                'rua': '',
                'numero': '',
                'bairro': '',
                'cidade': ''
            }
    except Exception:
        obra = {
            'id': id,
            'nome': '',
            'rua': '',
            'numero': '',
            'bairro': '',
            'cidade': ''
        }
    return render_template('obras/editar-obras.html', obra=obra)

@app.route('/obras/excluir/<int:id>', methods=['POST'])
def excluirObra(id):
    try:
        response = requests.delete(f'http://localhost:8000/api/obras/{id}/')
        if response.status_code in [200, 204]:
            return redirect(url_for('obras'))
        else:
            return f'Erro ao excluir obra: {response.text}', 400
    except Exception as e:
        return f'Erro ao excluir obra: {str(e)}', 400



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
            'capacidade': request.form['capacidade'],
            'rua': request.form['rua'],
            'numero': request.form['numero'],
            'bairro': request.form['bairro'],
            'cidade': request.form['cidade'],
            'disponibilidade': 'disponibilidade' in request.form
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
            'capacidade': request.form['capacidade'],
            'rua': request.form['rua'],
            'numero': request.form['numero'],
            'bairro': request.form['bairro'],
            'cidade': request.form['cidade'],
            'disponibilidade': 'disponibilidade' in request.form
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
            veiculo = {
                'id': id,
                'tipo': '',
                'placa': '',
                'capacidade': '',
                'rua': '',
                'numero': '',
                'bairro': '',
                'cidade': '',
                'disponibilidade': False
            }
    except Exception:
        veiculo = {
            'id': id,
            'tipo': '',
            'placa': '',
            'capacidade': '',
            'rua': '',
            'numero': '',
            'bairro': '',
            'cidade': '',
            'disponibilidade': False
        }
    return render_template('veiculos/editar-veiculos.html', veiculo=veiculo)

@app.route('/veiculos/excluir/<int:id>', methods=['POST'])
def excluirVeiculo(id):
    try:
        response = requests.delete(f'http://localhost:8000/api/veiculos/{id}/')
        if response.status_code in [200, 204]:
            return redirect(url_for('veiculos'))
        else:
            return f'Erro ao excluir veículo: {response.text}', 400
    except Exception as e:
        return f'Erro ao excluir veículo: {str(e)}', 400



# Rotas para Funcionário
@app.route('/funcionarios')
def funcionarios():
    
    request = requests.get('http://localhost:8000/api/funcionarios/')
    if request.status_code == 200:
        funcionarios = request.json()
        return render_template('funcionarios/listar-funcionario.html', funcionarios=funcionarios)
    else:
        return render_template('funcionarios/listar-funcionario.html', error="Erro ao buscar funcionários.")


@app.route('/funcionarios/cadastrar', methods=['GET', 'POST'])
def cadastrarFuncionario():
    if request.method == 'POST':
        funcionario = {
            'nome_completo': request.form['nome_completo'],
            'rua': request.form['rua'],
            'numero': request.form['numero'],
            'bairro': request.form['bairro'],
            'cidade': request.form['cidade'],
            'cargo': request.form['cargo'],
            'email': request.form['email'],
            'senha': request.form['senha']
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
            'nome_completo': request.form['nome_completo'],
            'rua': request.form['rua'],
            'numero': request.form['numero'],
            'bairro': request.form['bairro'],
            'cidade': request.form['cidade'],
            'cargo': request.form['cargo'],
            'email': request.form['email'],
            'senha': request.form['senha']
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
            funcionario = {
                'id': id,
                'nome_completo': '',
                'rua': '',
                'numero': '',
                'bairro': '',
                'cidade': '',
                'cargo': '',
                'email': '',
                'senha': ''
            }
    except Exception:
        funcionario = {
            'id': id,
            'nome_completo': '',
            'rua': '',
            'numero': '',
            'bairro': '',
            'cidade': '',
            'cargo': '',
            'email': '',
            'senha': ''
        }
    return render_template('funcionarios/editar-funcionario.html', funcionario=funcionario)

@app.route('/funcionarios/excluir/<int:id>', methods=['POST'])
def excluirFuncionario(id):
    try:
        response = requests.delete(f'http://localhost:8000/api/funcionarios/{id}/')
        if response.status_code in [200, 204]:
            return redirect(url_for('funcionarios'))
        else:
            return f'Erro ao excluir funcionário: {response.text}', 400
    except Exception as e:
        return f'Erro ao excluir funcionário: {str(e)}', 400

