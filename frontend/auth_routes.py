from flask import render_template, request, redirect, url_for, session, flash
from uairoute import app
import requests

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        try:
            # Fazer requisição para o backend
            response = requests.post('http://localhost:8000/api/funcionarios/login/', json={
                'email': email,
                'senha': senha
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    # Login bem-sucedido, salvar dados na sessão
                    session['funcionario'] = data['funcionario']
                    session['logged_in'] = True
                    
                    # Redirecionar baseado no tipo de usuário
                    if data['funcionario']['is_admin']:
                        return redirect(url_for('home'))
                    else:
                        return redirect(url_for('minhas_ordens'))
                else:
                    return render_template('login.html', error='Email ou senha incorretos')
            else:
                error_data = response.json()
                return render_template('login.html', error=error_data.get('error', 'Erro no login'))
                
        except Exception as e:
            return render_template('login.html', error='Erro de conexão com o servidor')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    # Verificar se usuário está logado
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    funcionario_id = session['funcionario']['id']
    
    # Buscar alojamentos disponíveis
    try:
        alojamentos_response = requests.get('http://localhost:8000/api/alojamento/')
        alojamentos = alojamentos_response.json() if alojamentos_response.status_code == 200 else []
    except:
        alojamentos = []
    
    if request.method == 'POST':
        # Dados para atualizar
        dados = {
            'id': funcionario_id,
            'nome_completo': request.form.get('nome_completo'),
            'cargo': request.form.get('cargo'),
            'email': request.form.get('email'),
            'alojamento': request.form.get('alojamento') if request.form.get('alojamento') else None
        }
        
        # Adicionar senha apenas se foi fornecida
        if request.form.get('senha'):
            dados['senha'] = request.form.get('senha')
        
        try:
            response = requests.put('http://localhost:8000/api/funcionarios/perfil/atualizar/', json=dados)
            
            if response.status_code == 200:
                # Atualizar dados na sessão
                session['funcionario']['nome_completo'] = dados['nome_completo']
                session['funcionario']['cargo'] = dados['cargo']
                session['funcionario']['email'] = dados['email']
                session['funcionario']['alojamento'] = dados['alojamento']
                
                # Buscar dados atualizados do funcionário
                perfil_response = requests.get(f'http://localhost:8000/api/funcionarios/perfil/?id={funcionario_id}')
                if perfil_response.status_code == 200:
                    funcionario = perfil_response.json()
                else:
                    funcionario = session['funcionario']
                
                return render_template('perfil.html', 
                                     funcionario=funcionario, 
                                     alojamentos=alojamentos,
                                     success='Perfil atualizado com sucesso!')
            else:
                error_data = response.json()
                return render_template('perfil.html', 
                                     funcionario=session['funcionario'], 
                                     alojamentos=alojamentos,
                                     error=error_data.get('error', 'Erro ao atualizar perfil'))
                
        except Exception as e:
            return render_template('perfil.html', 
                                 funcionario=session['funcionario'], 
                                 alojamentos=alojamentos,
                                 error=f'Erro de conexão: {str(e)}')
    
    # GET: buscar dados atualizados do funcionário
    try:
        response = requests.get(f'http://localhost:8000/api/funcionarios/perfil/?id={funcionario_id}')
        if response.status_code == 200:
            funcionario = response.json()
        else:
            funcionario = session['funcionario']
    except:
        funcionario = session['funcionario']
    
    return render_template('perfil.html', funcionario=funcionario, alojamentos=alojamentos)

def require_login(f):
    """Decorator para verificar se usuário está logado"""
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_admin(f):
    """Decorator para verificar se usuário é admin"""
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        if not session.get('funcionario', {}).get('is_admin'):
            return redirect(url_for('mapa'))  # Redireciona não-admin para o mapa
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function
