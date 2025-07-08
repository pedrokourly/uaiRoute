from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from api.funcionarios.models import Funcionario


class Command(BaseCommand):
    help = 'Cria um usuário administrador padrão se não existir'

    def handle(self, *args, **options):
        email = 'admin@teste.com'
        senha = 'admin'
        nome = 'Administrador'
        cargo = 'Administrador'

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
                f'Senha: {senha}'
            )
        )
