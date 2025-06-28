from flask import render_template, request, redirect, url_for, jsonify
from uairoute import app
import requests

# Importar os decoradores de autenticação
from auth_routes import require_admin

@app.route('/ordens-servico')
@require_admin
def ordens_servico():
    try:
        response = requests.get('http://localhost:8000/api/ordens-servico/')
        if response.status_code == 200:
            ordens = response.json()
            return render_template('OrdemServico/listar-ordens.html', ordens=ordens)
        else:
            return render_template('OrdemServico/listar-ordens.html', error="Erro ao buscar ordens de serviço.")
    except Exception as e:
        return render_template('OrdemServico/listar-ordens.html', error="Erro ao conectar com o servidor.")

@app.route('/ordens-servico/cadastrar', methods=['GET', 'POST'])
@require_admin
def cadastrar_ordem_servico():
    # Buscar dados necessários para o formulário
    try:
        veiculos_response = requests.get('http://localhost:8000/api/veiculos/')
        veiculos = veiculos_response.json() if veiculos_response.status_code == 200 else []
        
        obras_response = requests.get('http://localhost:8000/api/obras/')
        obras = obras_response.json() if obras_response.status_code == 200 else []
        
        alojamentos_response = requests.get('http://localhost:8000/api/alojamento/')
        alojamentos = alojamentos_response.json() if alojamentos_response.status_code == 200 else []
    except:
        veiculos = []
        obras = []
        alojamentos = []
    
    if request.method == 'POST':
        # Processar alojamentos selecionados
        alojamentos_selecionados = []
        alojamento_ids = request.form.getlist('alojamentos')
        
        for i, alojamento_id in enumerate(alojamento_ids):
            if alojamento_id:  # Se há um ID válido
                alojamentos_selecionados.append({
                    'alojamento_id': int(alojamento_id),
                    'ordem_parada': i + 1
                })
        
        ordem_data = {
            'titulo': request.form.get('titulo'),
            'descricao': request.form.get('descricao', ''),
            'veiculo_id': int(request.form.get('veiculo_id')),
            'obra_destino_id': int(request.form.get('obra_destino_id')),
            'observacoes': request.form.get('observacoes', ''),
            'alojamentos': alojamentos_selecionados
        }
        
        try:
            response = requests.post('http://localhost:8000/api/ordens-servico/', json=ordem_data)
            if response.status_code in [200, 201]:
                return redirect(url_for('ordens_servico'))
            else:
                error_data = response.json()
                return render_template('OrdemServico/cadastrar-ordem.html', 
                                     veiculos=veiculos, obras=obras, alojamentos=alojamentos,
                                     error=error_data.get('error', 'Erro ao cadastrar ordem de serviço'))
        except Exception as e:
            return render_template('OrdemServico/cadastrar-ordem.html', 
                                 veiculos=veiculos, obras=obras, alojamentos=alojamentos,
                                 error=f'Erro de conexão: {str(e)}')
    
    return render_template('OrdemServico/cadastrar-ordem.html', 
                         veiculos=veiculos, obras=obras, alojamentos=alojamentos)

@app.route('/ordens-servico/<int:id>/visualizar')
@require_admin
def visualizar_ordem_servico(id):
    try:
        # Buscar dados da ordem de serviço
        response = requests.get(f'http://localhost:8000/api/ordens-servico/{id}/')
        if response.status_code == 200:
            ordem = response.json()
            return render_template('OrdemServico/visualizar-ordem.html', ordem=ordem)
        else:
            return render_template('OrdemServico/visualizar-ordem.html', 
                                 error="Ordem de serviço não encontrada.")
    except Exception as e:
        return render_template('OrdemServico/visualizar-ordem.html', 
                             error="Erro ao conectar com o servidor.")

@app.route('/api/ordens-servico/<int:id>/rota')
@require_admin
def ordem_servico_rota_api(id):
    """Endpoint para fornecer dados da rota para o frontend"""
    try:
        response = requests.get(f'http://localhost:8000/api/ordens-servico/{id}/rota/')
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Dados da rota não encontrados'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
