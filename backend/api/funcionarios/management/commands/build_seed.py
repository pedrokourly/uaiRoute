"""Constrói o banco semente que todo visitante do demo recebe ao entrar.

As coordenadas estão fixas de propósito. Elas são preenchidas pelas views
de criação (buscar_coordenadas_com_fallback), não pelos models -- uma
semente construída pelo ORM nasceria com latitude e longitude nulas e o
mapa, que é a tela mais visual do produto, ficaria sem marcador nenhum.
Fora isso, o Nominatim limita a uma requisição por segundo e depender dele
no boot tornaria o build lento e dependente de rede.
"""
from pathlib import Path

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections

from api.alojamento.models import Alojamento
from api.funcionarios.models import Funcionario
from api.obras.models import Obra
from api.ordens_servico.models import AlojamentoOrdemServico, OrdemServico
from api.veiculos.models import Veiculo

ALOJAMENTOS = [
    ('Alojamento Savassi', 12, 'Rua Pernambuco', '1200', 'Savassi', 'Belo Horizonte', -19.9386, -43.9333),
    ('Alojamento Contagem', 20, 'Avenida João César de Oliveira', '3000', 'Eldorado', 'Contagem', -19.9102, -44.0537),
    ('Alojamento Betim', 16, 'Avenida Edméia Mattos Lazzarotti', '500', 'Angola', 'Betim', -19.9679, -44.1986),
]

FUNCIONARIOS = [
    ('Administrador', 'Administrador', 'admin@teste.com', 'admin', True, 0),
    ('João Batista', 'Pedreiro', 'joao@teste.com', '123456', False, 0),
    ('Maria Aparecida', 'Engenheira Civil', 'maria@teste.com', '123456', False, 0),
    ('Carlos Eduardo', 'Mestre de Obras', 'carlos@teste.com', '123456', False, 1),
    ('Ana Lúcia', 'Arquiteta', 'ana@teste.com', '123456', False, 1),
    ('Roberto Silva', 'Motorista', 'roberto@teste.com', '123456', False, 1),
    ('Fernanda Costa', 'Técnica de Segurança', 'fernanda@teste.com', '123456', False, 2),
    ('Paulo Henrique', 'Eletricista', 'paulo@teste.com', '123456', False, 2),
]

OBRAS = [
    ('Edifício Aurora', 'Rua da Bahia', '900', 'Centro', 'Belo Horizonte', -19.9245, -43.9352),
    ('Condomínio Serra Verde', 'Rua Timbiras', '1500', 'Funcionários', 'Belo Horizonte', -19.9297, -43.9366),
    ('Viaduto Leste', 'Avenida Cristiano Machado', '4000', 'Ipiranga', 'Belo Horizonte', -19.8619, -43.9231),
    ('Escola Municipal Betim', 'Rua do Rosário', '250', 'Centro', 'Betim', -19.9678, -44.1983),
    ('Centro Logístico Contagem', 'Rodovia Fernão Dias', 'km 12', 'Cinco', 'Contagem', -19.8869, -44.0536),
]

VEICULOS = [
    ('carro', 'ABC1D23', 4, 'Rua Sapucaí', '100', 'Floresta', 'Belo Horizonte', -19.9174, -43.9345),
    ('van', 'DEF4G56', 12, 'Avenida Amazonas', '2000', 'Barro Preto', 'Belo Horizonte', -19.9245, -43.9483),
    ('caminhao', 'GHI7J89', 2, 'Avenida Antônio Carlos', '6000', 'Pampulha', 'Belo Horizonte', -19.8656, -43.9647),
    ('moto', 'JKL0M12', 1, 'Rua dos Tupis', '500', 'Centro', 'Belo Horizonte', -19.9214, -43.9412),
]

ORDENS = [
    ('Entrega de material — Aurora', 'Cimento e vergalhões para a laje do 4º andar.', 0, 0, 'concluida', 12.4, 28, [0]),
    ('Transporte de equipe — Serra Verde', 'Levar a equipe de acabamento.', 1, 1, 'em_andamento', 8.1, 19, [0, 1]),
    ('Vistoria estrutural — Viaduto Leste', 'Acompanhamento da concretagem.', 0, 2, 'pendente', 15.7, 33, []),
    ('Entrega de areia — Escola Betim', 'Dois carregamentos previstos.', 2, 3, 'pendente', 41.2, 62, [2]),
    ('Inspeção elétrica — Centro Logístico', 'Revisão do quadro de distribuição.', 3, 4, 'em_andamento', 22.9, 41, [1]),
    ('Remoção de entulho — Aurora', 'Cancelada por indisponibilidade de caçamba.', 2, 0, 'cancelada', 12.4, 28, []),
]


def popular():
    """Cria os dados de demonstração. Idempotente: não faz nada se já houver."""
    if Funcionario.objects.exists():
        return

    alojamentos = [
        Alojamento.objects.create(
            nome=nome, capacidade_maxima=capacidade, rua=rua, numero=numero,
            bairro=bairro, cidade=cidade, latitude=lat, longitude=lon,
        )
        for nome, capacidade, rua, numero, bairro, cidade, lat, lon in ALOJAMENTOS
    ]

    for nome, cargo, email, senha, is_admin, indice in FUNCIONARIOS:
        Funcionario.objects.create(
            nome_completo=nome, cargo=cargo, email=email,
            senha=make_password(senha), is_admin=is_admin,
            alojamento=alojamentos[indice],
        )

    obras = [
        Obra.objects.create(
            nome=nome, rua=rua, numero=numero, bairro=bairro,
            cidade=cidade, latitude=lat, longitude=lon,
        )
        for nome, rua, numero, bairro, cidade, lat, lon in OBRAS
    ]

    veiculos = [
        Veiculo.objects.create(
            tipo=tipo, placa=placa, capacidade=capacidade, rua=rua, numero=numero,
            bairro=bairro, cidade=cidade, latitude=lat, longitude=lon,
        )
        for tipo, placa, capacidade, rua, numero, bairro, cidade, lat, lon in VEICULOS
    ]

    for titulo, descricao, i_veiculo, i_obra, status, distancia, tempo, paradas in ORDENS:
        ordem = OrdemServico.objects.create(
            titulo=titulo, descricao=descricao, veiculo=veiculos[i_veiculo],
            obra_destino=obras[i_obra], status=status,
            distancia_total=distancia, tempo_estimado=tempo,
        )
        for posicao, indice in enumerate(paradas, start=1):
            AlojamentoOrdemServico.objects.create(
                ordem_servico=ordem, alojamento=alojamentos[indice],
                ordem_parada=posicao,
            )


class Command(BaseCommand):
    help = 'Cria o banco semente do demo, com migrações aplicadas e dados de demonstração.'

    def handle(self, *args, **options):
        semente = Path(settings.DEMO_SEED)
        if semente.exists():
            self.stdout.write(f'Semente já existe em {semente}, nada a fazer.')
            return

        semente.parent.mkdir(parents=True, exist_ok=True)

        conexao = connections['default']
        conexao.close()
        conexao.settings_dict['NAME'] = str(semente)

        call_command('migrate', '--noinput', verbosity=0)
        popular()
        conexao.close()

        self.stdout.write(self.style.SUCCESS(f'✓ Semente criada em {semente}'))
