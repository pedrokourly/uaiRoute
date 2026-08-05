import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from django.conf import settings
from api.funcionarios.models import Funcionario


class Command(BaseCommand):
    help = 'Cria um usuário administrador padrão se não existir'

    def handle(self, *args, **options):
        email = 'admin@teste.com'
        nome = 'Administrador'
        cargo = 'Administrador'

        # Lê a senha do ambiente ou usa fallback para desenvolvimento
        senha = os.environ.get('ADMIN_PASSWORD')

        if not senha:
            if settings.DEBUG:
                # Em desenvolvimento (DEBUG=True), usa fallback para conveniência
                senha = 'admin'
            else:
                # Em produção (DEBUG=False), a senha é obrigatória
                raise CommandError(
                    'ADMIN_PASSWORD é obrigatória em produção (DEBUG=False). '
                    'Defina a variável de ambiente ADMIN_PASSWORD antes de subir o container. '
                    'Exemplo: export ADMIN_PASSWORD="sua-senha-segura"'
                )

        # Verifica se o administrador já existe
        if Funcionario.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'Administrador com email {email} já existe.')
            )
            return

        # Cria o administrador
        admin_user = Funcionario.objects.create(
            nome_completo=nome,
            cargo=cargo,
            email=email,
            senha=make_password(senha),
            is_admin=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Administrador criado com sucesso!\n'
                f'Email: {email}\n'
                f'Senha: {"(definida via ADMIN_PASSWORD)" if os.environ.get("ADMIN_PASSWORD") else senha}'
            )
        )
