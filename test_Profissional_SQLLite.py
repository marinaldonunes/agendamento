import sqlite3 as sql
import unittest
import datetime as dt
import os

from profissionalDao import ProfissionalDao
from profissional import Profissional


class testeProfissionalSQLLite(unittest.TestCase):


    def setUp(self):
        """Configuração antes de cada teste"""
        self.caminho_banco = "TesteBD.db"

        # Remove o banco de dados anterior, garantindo um ambiente de testes limpo
        if os.path.exists(self.caminho_banco):
            os.remove(self.caminho_banco)

        # Cria uma nova conexão para cada teste
        self.conexao = sql.connect(self.caminho_banco)
        ProfissionalDao.cria_tabela_profissional(self.conexao)


    def tearDown(self):
        """Encerramento após cada teste"""
        self.conexao.close()  # Fecha a conexão ao final de cada teste
        if os.path.exists(self.caminho_banco):
            os.remove(self.caminho_banco)  # Remove o banco após o teste   


    def test_InserirProfissional(self):

        prof = Profissional('Marinaldo', 'Oliveira', 1111,  'PB',  'CREFITO')
        prof.set_contatos(['mari@hotmail.br', '9999999999'])

        self.assertIsNot(ProfissionalDao.insere_profissional(self.conexao, prof), -1)

    def test_ExcluirProfissional(self):
        prof = Profissional('Marinaldo', 'Oliveira', 1111,  'PB',  'CREFITO')
        prof.set_contatos(['mari@hotmail.br', '9999999999'])

        retorno = ProfissionalDao.insere_profissional(self.conexao, prof)
        self.assertEqual(ProfissionalDao.exclui_profissional(self.conexao, retorno), 1)        


    def test_AtualizarProfissional(self):

        prof_anterior = Profissional('Lucia', 'Nunes', 9999, 'PE', 'CRN')
        prof_anterior.set_contatos(['1234567', 'lucia@gmail'])
        prof_anterior.set_id(3)

        prof_atualizado = Profissional('Marina', 'Leite', 4444,  'PE', 'CRP')
        prof_atualizado.set_contatos(['lulu@gmail'])
        prof_atualizado.set_id(3)        

        retorno = ProfissionalDao.atualiza_profissional(self.conexao, prof_anterior, prof_atualizado)

        self.assertEqual(retorno.get_nome(), 'Marina') and self.assertEqual(retorno.get_sobrenome(), 'Leite')

    def test_ConsultaProfissinais(self):

        prof1 = Profissional('Lucia', 'Nunes', 9999, 'PE', 'CRN')
        prof1.set_contatos(['1234567', 'lucia@gmail'])

        prof2 = Profissional('Marina', 'Leite', 4444,  'PE', 'CRP')
        prof2.set_contatos(['lulu@gmail'])

        prof3 = Profissional('Edson', 'Paulo', 6666,  'CE', 'CRM')
        prof3.set_contatos(['led@gmail'])    

        ProfissionalDao.insere_profissional(self.conexao, prof1)
        ProfissionalDao.insere_profissional(self.conexao, prof2)           
        ProfissionalDao.insere_profissional(self.conexao, prof3)

        listaProfs = ProfissionalDao.consulta_profissionais(self.conexao)

        self.assertEqual(len(listaProfs), 3)
       

if __name__ == '__main__':
    unittest.main()
