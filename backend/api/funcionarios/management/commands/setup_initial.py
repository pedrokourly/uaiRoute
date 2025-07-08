from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Configura o banco de dados inicial e cria o administrador'

    def handle(self, *args, **options):
        self.stdout.write('Executando migrations...')
        call_command('migrate')
        
        self.stdout.write('Criando administrador padrão...')
        call_command('create_admin')
        
        self.stdout.write(
            self.style.SUCCESS('Setup inicial completo!')
        )
