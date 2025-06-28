from flask import render_template, request, redirect, url_for
from uairoute import app
import requests

# Rotas para Funcionários
@app.route('/funcionarios')
def funcionarios():
    try:
        response = requests.get('http://localhost:8000/api/funcionarios/')
        if response.status_code == 200:
            funcionarios = response.json()
            return render_template('Funcionarios/listar-funcionario.html', funcionarios=funcionarios)
        else:
            return render_template('Funcionarios/listar-funcionario.html', error="Erro ao buscar funcionários.")
    except Exception as e:
        return render_template('Funcionarios/listar-funcionario.html', error="Erro ao conectar com o servidor.")

@app.route('/funcionarios/cadastrar', methods=['GET', 'POST'])
def cadastrarFuncionario():
    # Buscar alojamentos disponíveis
    try:
        alojamentos_response = requests.get('http://localhost:8000/api/alojamento/')
        alojamentos = alojamentos_response.json() if alojamentos_response.status_code == 200 else []
    except:
        alojamentos = []
    
    if request.method == 'POST':
        funcionario = {
            'nome_completo': request.form['nome_completo'],
            'email': request.form.get('email', ''),
            'cargo': request.form.get('cargo', ''),
            'senha': request.form.get('senha', ''),
            'alojamento': request.form.get('alojamento') if request.form.get('alojamento') else None
        }
        try:
            response = requests.post('http://localhost:8000/api/funcionarios/', json=funcionario)
            if response.status_code in [200, 201]:
                return redirect(url_for('funcionarios'))
            else:
                # Tenta extrair mensagem de erro específica do backend
                error_message = 'Erro ao cadastrar funcionário.'
                if response.status_code == 400:
                    try:
                        error_data = response.json()
                        if 'error' in error_data:
                            if 'alojamento' in error_data['error']:
                                error_message = error_data['error']['alojamento'][0]
                            else:
                                error_message = str(error_data['error'])
                    except:
                        pass
                return render_template('Funcionarios/cadastrar-funcionario.html', 
                                     error=error_message, alojamentos=alojamentos)
        except Exception as e:
            return render_template('Funcionarios/cadastrar-funcionario.html', error=str(e), alojamentos=alojamentos)
    return render_template('Funcionarios/cadastrar-funcionario.html', alojamentos=alojamentos)

@app.route('/funcionarios/editar/<int:id>', methods=['GET', 'POST'])
def editarFuncionario(id):
    # Buscar alojamentos disponíveis
    try:
        alojamentos_response = requests.get('http://localhost:8000/api/alojamento/')
        alojamentos = alojamentos_response.json() if alojamentos_response.status_code == 200 else []
    except:
        alojamentos = []
    
    if request.method == 'POST':
        funcionario = {
            'nome_completo': request.form['nome_completo'],
            'email': request.form.get('email', ''),
            'cargo': request.form.get('cargo', ''),
            'senha': request.form.get('senha', ''),
            'alojamento': request.form.get('alojamento') if request.form.get('alojamento') else None
        }
        try:
            response = requests.put(f'http://localhost:8000/api/funcionarios/{id}/', json=funcionario)
            if response.status_code in [200, 204]:
                return redirect(url_for('funcionarios'))
            else:
                # Tenta extrair mensagem de erro específica do backend
                error_message = 'Erro ao editar funcionário.'
                if response.status_code == 400:
                    try:
                        error_data = response.json()
                        if 'error' in error_data:
                            if 'alojamento' in error_data['error']:
                                error_message = error_data['error']['alojamento'][0]
                            else:
                                error_message = str(error_data['error'])
                    except:
                        pass
                return render_template('Funcionarios/editar-funcionario.html', 
                                     funcionario=funcionario, error=error_message, alojamentos=alojamentos)
        except Exception as e:
            return render_template('Funcionarios/editar-funcionario.html', funcionario=funcionario, error=str(e), alojamentos=alojamentos)
    # GET: busca dados do funcionário
    try:
        response = requests.get(f'http://localhost:8000/api/funcionarios/{id}/')
        if response.status_code == 200:
            funcionario = response.json()
        else:
            funcionario = {}
    except Exception:
        funcionario = {}
    return render_template('Funcionarios/editar-funcionario.html', funcionario=funcionario, alojamentos=alojamentos)

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
