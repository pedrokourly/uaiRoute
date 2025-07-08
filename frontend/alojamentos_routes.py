from flask import render_template, request, redirect, url_for
from uairoute import app
import requests

# Importar os decoradores de autenticação
from auth_routes import require_admin
# Importar configurações centralizadas
from config import API_URLS

# Rotas para Alojamentos
@app.route('/alojamentos')
@require_admin
def alojamentos():
    try:
        response = requests.get(API_URLS['alojamentos'])
        print(response.status_code)
        if response.status_code == 200:
            alojamentos = response.json()
            return render_template('Alojamentos/listar-alojamentos.html', alojamentos=alojamentos)
        else:
            return render_template('Alojamentos/listar-alojamentos.html', error="Erro ao buscar alojamentos.")
    except Exception as e:
        return render_template('Alojamentos/listar-alojamentos.html', error="Erro ao conectar com o servidor.")

@app.route('/alojamentos/cadastrar', methods=['GET', 'POST'])
@require_admin
def cadastrarAlojamento():
    if request.method == 'POST':
        alojamento = {
            'nome': request.form['nome'].strip(),
            'capacidade_maxima': int(request.form.get('capacidade_maxima', 0)),
            'rua': request.form.get('rua', '').strip(),
            'numero': request.form.get('numero', '').strip(),
            'bairro': request.form.get('bairro', '').strip(),
            'cidade': request.form.get('cidade', '').strip()
        }
        
        try:
            response = requests.post(API_URLS['alojamentos'], json=alojamento)
            if response.status_code in [200, 201]:
                return redirect(url_for('alojamentos'))
            else:
                error_msg = f"Erro ao cadastrar alojamento. Status: {response.status_code}. Resposta: {response.text}"
                return render_template('Alojamentos/cadastrar-alojamentos.html', error=error_msg)
        except Exception as e:
            return render_template('Alojamentos/cadastrar-alojamentos.html', error=f"Erro de conexão: {str(e)}")
    return render_template('Alojamentos/cadastrar-alojamentos.html')

@app.route('/alojamentos/editar/<int:id>', methods=['GET', 'POST'])
@require_admin
def editarAlojamento(id):
    if request.method == 'POST':
        alojamento = {
            'nome': request.form['nome'].strip(),
            'capacidade_maxima': int(request.form.get('capacidade_maxima', 0)),
            'rua': request.form.get('rua', '').strip(),
            'numero': request.form.get('numero', '').strip(),
            'bairro': request.form.get('bairro', '').strip(),
            'cidade': request.form.get('cidade', '').strip()
        }
        try:
            response = requests.put(f'{API_URLS["alojamentos"]}{id}/', json=alojamento)
            if response.status_code in [200, 204]:
                return redirect(url_for('alojamentos'))
            else:
                # Tenta extrair mensagem de erro específica do backend
                error_message = 'Erro ao editar alojamento.'
                if response.status_code == 400:
                    try:
                        error_data = response.json()
                        if 'error' in error_data:
                            if 'capacidade_maxima' in error_data['error']:
                                error_message = error_data['error']['capacidade_maxima'][0]
                            else:
                                error_message = str(error_data['error'])
                    except:
                        pass
                return render_template('Alojamentos/editar-alojamentos.html', 
                                     alojamento=alojamento, error=error_message)
        except Exception as e:
            return render_template('Alojamentos/editar-alojamentos.html', alojamento=alojamento, error=f"Erro de conexão: {str(e)}")
    
    # GET: busca dados do alojamento
    try:
        response = requests.get(f'{API_URLS["alojamentos"]}{id}/')
        if response.status_code == 200:
            alojamento = response.json()
        else:
            alojamento = {}
    except Exception:
        alojamento = {}
    return render_template('Alojamentos/editar-alojamentos.html', alojamento=alojamento)

@app.route('/alojamentos/excluir/<int:id>', methods=['POST'])
@require_admin
def excluirAlojamento(id):
    try:
        response = requests.delete(f'{API_URLS["alojamentos"]}{id}/')
        if response.status_code in [200, 204]:
            return redirect(url_for('alojamentos'))
        else:
            return redirect(url_for('alojamentos'))
    except Exception as e:
        return redirect(url_for('alojamentos'))
