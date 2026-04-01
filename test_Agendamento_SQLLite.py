import datetime as dt
import sqlite3 as sql
import unittest

from agendamento import Agendamento
from agendamentoDao import AgendamentoDao
from agenda import Agenda
from agendaDao import AgendaDao
from cliente import Cliente
from clienteDao import ClienteDao
from profissional import Profissional
from profissionalDao import ProfissionalDao
from servico import Servico
from servicoDao import ServicoDao


class TestAgendamentoSQLite(unittest.TestCase):
    def setUp(self):
        self.conexao = sql.connect(":memory:")

        ProfissionalDao.cria_tabela_profissional(self.conexao)
        AgendaDao.criar_tabela_agenda(self.conexao)
        ServicoDao.criar_tabela_servico(self.conexao)
        ClienteDao.cria_tabela_cliente(self.conexao)
        AgendamentoDao.criar_tabela_agendamento(self.conexao)

        self.prof1 = Profissional("Jose", "Pereira", 1111, "SP", "CRP")
        self.prof2 = Profissional("Ana", "Souza", 2222, "RJ", "CRP")
        self.prof1.set_contatos(["prof1@mail.com"])
        self.prof2.set_contatos(["prof2@mail.com"])
        self.prof1.set_id(ProfissionalDao.insere_profissional(self.conexao, self.prof1))
        self.prof2.set_id(ProfissionalDao.insere_profissional(self.conexao, self.prof2))

        self.serv1 = Servico("Massagem", 60)
        self.serv2 = Servico("Pilates", 50)
        self.serv1.set_id(ServicoDao.inserir_servico(self.conexao, self.serv1))
        self.serv2.set_id(ServicoDao.inserir_servico(self.conexao, self.serv2))

        self.cli1 = Cliente("Mario", "Oliveira", dt.date(1980, 5, 20), "11111111111", "Marina", "M")
        self.cli2 = Cliente("Fernanda", "Silva", dt.date(1990, 1, 10), "22222222222", "Marta", "F")
        self.cli1.set_contatos(["cli1@mail.com"])
        self.cli2.set_contatos(["cli2@mail.com"])
        self.cli1.set_id(ClienteDao.insere_cliente(self.conexao, self.cli1))
        self.cli2.set_id(ClienteDao.insere_cliente(self.conexao, self.cli2))

        self.ag1 = self._inserir_agendamento(self.cli1, self.serv1, self.prof1, dt.date(2026, 1, 10), "0900")
        self.ag2 = self._inserir_agendamento(self.cli2, self.serv1, self.prof1, dt.date(2026, 1, 10), "1000")
        self.ag3 = self._inserir_agendamento(self.cli2, self.serv2, self.prof2, dt.date(2026, 1, 11), "0900")

    def tearDown(self):
        self.conexao.close()

    def _inserir_agendamento(self, cliente, servico, profissional, data, hora):
        agenda = Agenda(profissional, data, hora)
        agenda_id = AgendaDao.inserir_agenda(self.conexao, agenda)
        agenda.set_id(agenda_id)
        agendamento = Agendamento(0, cliente, servico, agenda_id)
        novo_id = AgendamentoDao.inserir_agendamentos(self.conexao, agendamento)
        agendamento.set_id_agendamento(novo_id)
        return agendamento

    def test_consultar_agendamento_por_id_retorna_objeto(self):
        result = AgendamentoDao.consultar_agendamento(self.conexao, self.ag1.get_id_agendamento())

        self.assertIsInstance(result, Agendamento)
        self.assertEqual(self.ag1.get_id_agendamento(), result.get_id_agendamento())
        self.assertEqual(self.cli1.get_id(), result.get_cliente().get_id())
        self.assertEqual(self.serv1.get_id(), result.get_servico().get_id())
        agenda_result = AgendaDao.consulta_agenda_id(self.conexao, result.get_id_agenda())
        self.assertEqual(self.prof1.get_id(), agenda_result.get_profissional())

    def test_consultar_agendamentos_cliente(self):
        rows = list(AgendamentoDao.consultar_agendamentos_cliente(self.conexao, self.cli2.get_id()))
        self.assertEqual(2, len(rows))

    def test_consultar_agendamentos_profissional(self):
        rows = list(AgendamentoDao.consultar_agendamentos_profissional(self.conexao, self.prof1.get_id()))
        self.assertEqual(2, len(rows))

    def test_consultar_agendamentos_servicos(self):
        rows = list(AgendamentoDao.consultar_agendamentos_servicos(self.conexao, self.serv1.get_id()))
        self.assertEqual(2, len(rows))

    def test_consultar_agendamentos_data(self):
        rows = list(AgendamentoDao.consultar_agendamentos_data(self.conexao, dt.date(2026, 1, 10)))
        self.assertEqual(2, len(rows))

    def test_consultar_agendamentos_data_hora(self):
        rows = list(AgendamentoDao.consultar_agendamentos_data_hora(self.conexao, dt.date(2026, 1, 10), "0900"))
        self.assertEqual(1, len(rows))
        self.assertEqual(self.ag1.get_id_agendamento(), rows[0][0])

    def test_excluir_agendamento(self):
        status = AgendamentoDao.excluir_agendamento(self.conexao, self.ag3)
        self.assertEqual(1, status)

        result = AgendamentoDao.consultar_agendamento(self.conexao, self.ag3.get_id_agendamento())
        self.assertEqual(-1, result)


if __name__ == "__main__":
    unittest.main()
