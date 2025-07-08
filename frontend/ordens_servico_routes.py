from flask import render_template, request, redirect, url_for, jsonify, session
from uairoute import app
import requests

# Importar os decoradores de autenticação
from auth_routes import require_admin, require_login

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

@app.route('/ordens-servico/visualizar/<int:id>')
@require_login
def visualizar_ordem_servico(id):
    funcionario = session.get('funcionario')
    if not funcionario:
        return redirect(url_for('login'))
    
    # Se não for admin, verificar se tem acesso à ordem
    if not funcionario.get('is_admin', False):
        if not funcionario_pode_acessar_ordem(funcionario['id'], id):
            return render_template('OrdemServico/visualizar-ordem.html', 
                                 error="Você não tem acesso a esta ordem de serviço.",
                                 is_admin=funcionario.get('is_admin', False))
    
    try:
        # Buscar dados da ordem de serviço
        response = requests.get(f'http://localhost:8000/api/ordens-servico/{id}/')
        if response.status_code == 200:
            ordem = response.json()
            return render_template('OrdemServico/visualizar-ordem.html', 
                                 ordem=ordem, 
                                 is_admin=funcionario.get('is_admin', False))
        else:
            return render_template('OrdemServico/visualizar-ordem.html', 
                                 error="Ordem de serviço não encontrada.",
                                 is_admin=funcionario.get('is_admin', False))
    except Exception as e:
        return render_template('OrdemServico/visualizar-ordem.html', 
                             error="Erro ao conectar com o servidor.",
                             is_admin=funcionario.get('is_admin', False))

@app.route('/api/ordens-servico/<int:id>/rota')
@require_login
def ordem_servico_rota_api(id):
    """Endpoint para fornecer dados da rota para o frontend"""
    funcionario = session.get('funcionario')
    if not funcionario:
        return jsonify({'error': 'Acesso negado'}), 401
    
    # Se não for admin, verificar se tem acesso à ordem
    if not funcionario.get('is_admin', False):
        if not funcionario_pode_acessar_ordem(funcionario['id'], id):
            return jsonify({'error': 'Acesso negado a esta ordem'}), 403
    
    try:
        response = requests.get(f'http://localhost:8000/api/ordens-servico/{id}/rota/')
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Dados da rota não encontrados'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def funcionario_pode_acessar_ordem(funcionario_id, ordem_id):
    """
    Verifica se um funcionário pode acessar uma ordem de serviço específica.
    Retorna True se for admin ou se a ordem inclui o alojamento do funcionário.
    """
    try:
        # Buscar informações do funcionário
        funcionario_response = requests.get(f'http://localhost:8000/api/funcionarios/{funcionario_id}/')
        if funcionario_response.status_code != 200:
            return False
        
        funcionario = funcionario_response.json()
        
        # Se for admin, pode acessar qualquer ordem
        if funcionario.get('is_admin', False):
            return True
        
        # Se não tem alojamento, não pode acessar nenhuma ordem
        if not funcionario.get('alojamento'):
            return False
        
        # Buscar a ordem de serviço
        ordem_response = requests.get(f'http://localhost:8000/api/ordens-servico/{ordem_id}/')
        if ordem_response.status_code != 200:
            return False
        
        ordem = ordem_response.json()
        alojamento_funcionario_id = funcionario['alojamento']
        
        # Verificar se o alojamento do funcionário está nas paradas da ordem
        alojamentos_paradas = ordem.get('alojamentos_paradas', [])
        for parada in alojamentos_paradas:
            alojamento_parada = parada.get('alojamento', {})
            if isinstance(alojamento_parada, dict) and alojamento_parada.get('id') == alojamento_funcionario_id:
                return True
            elif isinstance(alojamento_parada, int) and alojamento_parada == alojamento_funcionario_id:
                return True
        
        return False
        
    except Exception as e:
        print(f"Erro ao verificar acesso: {e}")
        return False

@app.route('/minhas-ordens')
@require_login
def minhas_ordens():
    """
    Página para funcionários visualizarem suas ordens de serviço
    """
    funcionario = session.get('funcionario')
    
    if not funcionario:
        return redirect(url_for('login'))
    
    # Se for admin, redirecionar para a listagem completa
    if funcionario.get('is_admin', False):
        return redirect(url_for('ordens_servico'))
    
    try:
        # Buscar ordens de serviço relacionadas ao alojamento do funcionário
        response = requests.get(f'http://localhost:8000/api/ordens-servico/funcionario/{funcionario["id"]}/')
        
        if response.status_code == 200:
            data = response.json()
            funcionario_info = data.get('funcionario', {})
            ordens = data.get('ordens', [])
            return render_template('minhas-ordens.html', 
                                 funcionario=funcionario_info,
                                 ordens_servico=ordens)
        else:
            return render_template('minhas-ordens.html', 
                                 ordens_servico=[], 
                                 error="Erro ao buscar suas ordens de serviço.")
    except Exception as e:
        return render_template('minhas-ordens.html', 
                             ordens_servico=[], 
                             error=f"Erro ao conectar com o servidor: {str(e)}")

@app.route('/minhas-ordens/visualizar/<int:id>')
@require_login
def visualizar_minha_ordem(id):
    """
    Visualização de ordem específica para funcionários não-admin
    """
    funcionario = session.get('funcionario')
    
    if not funcionario:
        return redirect(url_for('login'))
    
    # Se for admin, redirecionar para a visualização completa
    if funcionario.get('is_admin', False):
        return redirect(url_for('visualizar_ordem_servico', id=id))
    
    try:
        # Buscar dados da ordem de serviço
        response = requests.get(f'http://localhost:8000/api/ordens-servico/{id}/')
        
        if response.status_code == 200:
            ordem = response.json()
            
            # Verificar se o funcionário tem acesso a esta ordem
            alojamento_funcionario_id = funcionario.get('alojamento')
            if not alojamento_funcionario_id:
                return render_template('minhas-ordens.html', 
                                     ordens_servico=[], 
                                     error="Você não está associado a nenhum alojamento.")
            
            # Verificar se o alojamento do funcionário está nas paradas da ordem
            tem_acesso = False
            alojamentos_paradas = ordem.get('alojamentos_paradas', [])
            for parada in alojamentos_paradas:
                alojamento_parada = parada.get('alojamento', {})
                if isinstance(alojamento_parada, dict) and alojamento_parada.get('id') == alojamento_funcionario_id:
                    tem_acesso = True
                    break
                elif isinstance(alojamento_parada, int) and alojamento_parada == alojamento_funcionario_id:
                    tem_acesso = True
                    break
            
            if not tem_acesso:
                return render_template('minhas-ordens.html', 
                                     ordens_servico=[], 
                                     error="Você não tem acesso a esta ordem de serviço.")
            
            return render_template('OrdemServico/visualizar-ordem.html', 
                                 ordem=ordem, 
                                 funcionario=funcionario,
                                 is_admin=funcionario.get('is_admin', False))
        else:
            return render_template('minhas-ordens.html', 
                                 ordens_servico=[], 
                                 error="Ordem de serviço não encontrada.")
    except Exception as e:
        return render_template('minhas-ordens.html', 
                             ordens_servico=[], 
                             error="Erro ao conectar com o servidor.")

@app.route('/ordens-servico/excluir/<int:id>', methods=['POST'])
@require_admin
def excluir_ordem_servico(id):
    """
    Excluir uma ordem de serviço (apenas admins)
    """
    try:
        # Fazer requisição DELETE para o backend
        response = requests.delete(f'http://localhost:8000/api/ordens-servico/{id}/')
        
        if response.status_code == 204:
            # Exclusão bem-sucedida
            return redirect(url_for('ordens_servico'))
        elif response.status_code == 404:
            # Ordem não encontrada
            return redirect(url_for('ordens_servico'))
        else:
            # Outro erro
            return redirect(url_for('ordens_servico'))
            
    except Exception as e:
        # Erro de conexão
        return redirect(url_for('ordens_servico'))

@app.route('/ordens-servico/editar/<int:id>', methods=['GET', 'POST'])
@require_admin
def editar_ordem_servico(id):
    try:
        # Buscar a ordem de serviço específica
        ordem_response = requests.get(f'http://localhost:8000/api/ordens-servico/{id}/')
        if ordem_response.status_code != 200:
            return render_template('OrdemServico/listar-ordens.html', 
                                 error="Ordem de serviço não encontrada.")
        
        ordem = ordem_response.json()
        
        # Buscar dados necessários para o formulário
        veiculos_response = requests.get('http://localhost:8000/api/veiculos/')
        veiculos = veiculos_response.json() if veiculos_response.status_code == 200 else []
        
        obras_response = requests.get('http://localhost:8000/api/obras/')
        obras = obras_response.json() if obras_response.status_code == 200 else []
        
        alojamentos_response = requests.get('http://localhost:8000/api/alojamento/')
        alojamentos = alojamentos_response.json() if alojamentos_response.status_code == 200 else []
        
    except Exception as e:
        return render_template('OrdemServico/listar-ordens.html', 
                             error="Erro ao conectar com o servidor.")
    
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
            'status': request.form.get('status'),
            'veiculo_id': int(request.form.get('veiculo_id')),
            'obra_destino_id': int(request.form.get('obra_destino_id')),
            'observacoes': request.form.get('observacoes', ''),
            'alojamentos': alojamentos_selecionados
        }
        
        try:
            response = requests.put(f'http://localhost:8000/api/ordens-servico/{id}/', json=ordem_data)
            if response.status_code in [200, 201]:
                return redirect(url_for('ordens_servico'))
            else:
                error_data = response.json()
                return render_template('OrdemServico/editar-ordem.html', 
                                     ordem=ordem, veiculos=veiculos, obras=obras, alojamentos=alojamentos,
                                     error=error_data.get('error', 'Erro ao atualizar ordem de serviço'))
        except Exception as e:
            return render_template('OrdemServico/editar-ordem.html', 
                                 ordem=ordem, veiculos=veiculos, obras=obras, alojamentos=alojamentos,
                                 error=f'Erro de conexão: {str(e)}')
    
    return render_template('OrdemServico/editar-ordem.html', 
                         ordem=ordem, veiculos=veiculos, obras=obras, alojamentos=alojamentos)

@app.route('/ordens-servico/concluir/<int:id>', methods=['POST'])
@require_admin
def concluir_ordem_servico(id):
    """
    Marcar uma ordem de serviço como concluída (apenas admins)
    """
    try:
        # Fazer requisição PATCH para alterar apenas o status
        response = requests.patch(
            f'http://localhost:8000/api/ordens-servico/{id}/', 
            json={'status': 'concluida'}
        )
        
        if response.status_code in [200, 201]:
            # Status alterado com sucesso
            return redirect(url_for('visualizar_ordem_servico', id=id))
        elif response.status_code == 404:
            # Ordem não encontrada
            return redirect(url_for('ordens_servico'))
        else:
            # Outro erro
            return redirect(url_for('visualizar_ordem_servico', id=id))
            
    except Exception as e:
        # Erro de conexão
        return redirect(url_for('visualizar_ordem_servico', id=id))
