"""Remove os bancos de visitantes que não são mais usados.

Cada visitante gera um arquivo. Sem isto o diretório cresce indefinidamente.
"""
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Apaga bancos de demo antigos e aplica o teto de arquivos simultâneos.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--idade-horas', type=float, default=24,
            help='Apaga os bancos sem modificação há mais tempo que isto.',
        )

    def handle(self, *args, **options):
        diretorio = Path(settings.DEMO_DIR)
        if not diretorio.exists():
            self.stdout.write(f'{diretorio} não existe, nada a limpar.')
            return

        limite = time.time() - options['idade_horas'] * 3600
        bancos = sorted(diretorio.glob('*.sqlite3'), key=lambda p: p.stat().st_mtime)

        removidos = 0
        for banco in list(bancos):
            if banco.stat().st_mtime < limite:
                banco.unlink()
                bancos.remove(banco)
                removidos += 1

        # Teto de segurança: mesmo dentro do prazo, não deixa o diretório
        # crescer sem limite. Os mais antigos saem primeiro.
        excedente = len(bancos) - settings.DEMO_MAX_BANCOS
        for banco in bancos[:max(excedente, 0)]:
            banco.unlink()
            removidos += 1

        self.stdout.write(self.style.SUCCESS(
            f'✓ {removidos} banco(s) removido(s); {len(list(diretorio.glob("*.sqlite3")))} restantes.'
        ))
