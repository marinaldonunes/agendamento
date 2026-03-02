import sqlite3 as sql
from servicoDao import ServicoDao
from clienteDao import ClienteDao
from profissionalDao import ProfissionalDao
from agendaDao import AgendaDao
from agendamentoDao import AgendamentoDao


if __name__ == '__main__':
    conexao = sql.connect("AgendamentoBD.db")
    ServicoDao.criar_tabela_servico(conexao)
    ClienteDao.cria_tabela_cliente(conexao)
    ProfissionalDao.cria_tabela_profissional(conexao)
    AgendaDao.criar_tabela_agenda(conexao)
    AgendamentoDao.criar_tabela_agendamento(conexao)
    print("Fim")