# UaiRoute - Configuração Inicial

## Configuração do Backend

### Primeira execução

Ao executar o servidor Django pela primeira vez, o sistema criará automaticamente um usuário administrador padrão.

### Dados do Administrador Padrão

- **Email:** admin@teste.com
- **Senha:** admin
- **Tipo:** Administrador

### Como iniciar o servidor

1. Navegue até o diretório do backend:
   ```bash
   cd backend
   ```

2. Execute as migrations (se necessário):
   ```bash
   python manage.py migrate
   ```

3. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

Na primeira execução do `runserver`, o sistema automaticamente:
- Verificará se existe um administrador
- Criará o usuário admin@teste.com/admin se não existir
- Exibirá uma mensagem confirmando a criação

### Comandos Manuais

Se preferir, você pode executar os comandos manualmente:

```bash
# Criar apenas o administrador
python manage.py create_admin

# Executar setup completo (migrations + admin)
python manage.py setup_initial

# Ou usar o script de setup
python setup_initial.py
```

### Alterando os dados do administrador

Para alterar email/senha padrão, edite o arquivo:
`backend/manage.py` na função `setup_admin_if_needed()`

Ou execute o comando personalizado:
`backend/api/funcionarios/management/commands/create_admin.py`

## Frontend

O frontend Flask está configurado para se conectar com este usuário administrador automaticamente criado.
