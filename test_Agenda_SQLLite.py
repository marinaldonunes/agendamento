import sqlite3 as sql
from agendaDao import AgendaDao
from profissionalDao import ProfissionalDao
from profissional import Profissional
from agenda import Agenda
import unittest
import os
import datetime as dt
from test_Profissional_SQLLite import testeProfissionalSQLLite


class TesteAgendaSQLLite(unittest.TestCase):

    def setUp(self):
        """Configuração antes de cada teste"""
        self.caminho_banco = r"c:\temp\TesteBD.db"

        # Remove o banco de dados anterior, garantindo um ambiente de testes limpo
        if os.path.exists(self.caminho_banco):
            os.remove(self.caminho_banco)

        # Cria uma nova conexão para cada teste
        self.conexao = sql.connect(self.caminho_banco)
        AgendaDao.criar_tabela_agenda(self.conexao)
        ProfissionalDao.cria_tabela_profissional(self.conexao)


    def tearDown(self):
        """Encerramento após cada teste"""
        self.conexao.close()  # Fecha a conexão ao final de cada teste
        if os.path.exists(self.caminho_banco):
            os.remove(self.caminho_banco)  # Remove o banco após o teste 
            


    def test_InserirAgenda(self):

        #Criação de um profissional para agedan
        prof = Profissional('Fernanda', 'Oliveira', 2222,  'PE',  'CRP')
        prof.set_contatos(['fe@hotmail.br', '888888888'])
        prof_id = ProfissionalDao.insere_profissional(self.conexao, prof)
        prof.set_id(prof_id)

        agd = Agenda(prof, dt.datetime.strptime('20/05/2025', "%d/%m/%Y"), '0800')      

        self.assertEqual(AgendaDao.inserir_agenda(self.conexao, agd), 1)   
          

    def test_ExcluirAgenda(self):

        prof = Profissional('Fernanda', 'Oliveira', 2222,  'PE',  'CRP')
        prof.set_contatos(['fe@hotmail.br', '888888888'])
        prof_id = ProfissionalDao.insere_profissional(self.conexao, prof)

        profissional_bd = ProfissionalDao.consulta_profissional_id(self.conexao, prof_id)

        agd = Agenda(profissional_bd, dt.datetime.strptime('20/05/2025', "%d/%m/%Y"), '0800')      

        self.assertEqual(AgendaDao.excluir_agenda(self.conexao, agd), 1)               


    def test_AtualizarAgenda(self):

        #Criação de um profissional para agedan
        prof = Profissional('Fernanda', 'Oliveira', 2222,  'PE',  'CRP')
        prof.set_contatos(['fe@hotmail.br', '888888888'])
        prod_id = ProfissionalDao.insere_profissional(self.conexao, prof)
        profissional_bd = ProfissionalDao.consulta_profissional_id(self.conexao, prod_id)
        agd = Agenda(profissional_bd, dt.datetime.strptime('20/05/2025', "%d/%m/%Y"), '0800')  
        AgendaDao.inserir_agenda(self.conexao, agd)               
    
        self.assertEqual(AgendaDao.atualizar_agenda(self.conexao, 
                                                       profissional_bd,  
                                                       dt.datetime.strptime('20/05/2025', "%d/%m/%Y"),'0800',  
                                                       dt.datetime.strptime('20/05/2025', "%d/%m/%Y"),'1000'
                                                       ), 1)   


    def test_consultas_agendas_prof(self):
        prof2 = Profissional('Pedro', 'Mane', 1452,  'MG',  'CREFITO')
        prof2.set_contatos(['fe@hotmail.br', '888888888'])
        prof_id = ProfissionalDao.insere_profissional(self.conexao, prof2)
        prof2.set_id(prof_id)
        agd2 = Agenda(prof2, dt.datetime.strptime('20/07/2025', '%d/%m/%Y'), '1000')          
        agd3 = Agenda(prof2, dt.datetime.strptime('21/07/2025', '%d/%m/%Y'), '1000')   
        AgendaDao.inserir_agenda(self.conexao, agd2)    
        AgendaDao.inserir_agenda(self.conexao, agd3)               

        #Tamanho da lista de agendas do profissional é igual a 2        
        self.assertEqual(len(AgendaDao.consulta_agendas_prof(self.conexao, prof2.get_id())), 2)


if __name__ == '__main__':
    unittest.main()





