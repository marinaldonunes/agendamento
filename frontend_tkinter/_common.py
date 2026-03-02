import sqlite3 as sql
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agendamentoDao import AgendamentoDao
from agendaDao import AgendaDao
from clienteDao import ClienteDao
from profissionalDao import ProfissionalDao
from servicoDao import ServicoDao

DB_PATH = ROOT_DIR / "AgendamentoBD.db"


def criar_conexao():
    conexao = sql.connect(DB_PATH)
    try:
        conexao.execute("PRAGMA foreign_keys = ON")
    except sql.DatabaseError:
        pass

    ProfissionalDao.cria_tabela_profissional(conexao)
    ClienteDao.cria_tabela_cliente(conexao)
    ServicoDao.criar_tabela_servico(conexao)
    AgendaDao.criar_tabela_agenda(conexao)
    AgendamentoDao.criar_tabela_agendamento(conexao)
    return conexao

