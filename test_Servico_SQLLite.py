import sqlite3 as sql
import unittest
import os

from servicoDao import ServicoDao
from servico import Servico


class testeServicosSQLLite(unittest.TestCase):


    def setUp(self):
        """Configuração antes de cada teste"""
        self.caminho_banco = "TesteBD.db"

        # Remove o banco de dados anterior, garantindo um ambiente de testes limpo
        if os.path.exists(self.caminho_banco):
            os.remove(self.caminho_banco)

        # Cria uma nova conexão para cada teste
        self.conexao = sql.connect(self.caminho_banco)
        ServicoDao.criar_tabela_servico(self.conexao)


    def tearDown(self):
        """Encerramento após cada teste"""
        self.conexao.close()  # Fecha a conexão ao final de cada teste
        if os.path.exists(self.caminho_banco):
            os.remove(self.caminho_banco)  # Remove o banco após o teste 


    def test_CriarServico(self):   
        serv1 = Servico('servico1', 10)
        self.assertEqual(ServicoDao.inserir_servico(self.conexao, serv1), 1)

    def test_ExcluirServico(self):
        serv1 = Servico('servico1', 10)
        ServicoDao.inserir_servico(self.conexao, serv1)

        self.assertEqual(ServicoDao.excluir_servico(self.conexao, serv1.get_id()), 1)      

    def test_AtualizarServico(self):

        #Inserir um serviço
        serv1 = Servico('servico1', 10)
        #Retorna o id do serviço inserido
        ServId = ServicoDao.inserir_servico(self.conexao, serv1)
        #Associa o novo id ao serv1 local
        serv1.set_id(ServId)

        novo_nome_servico = 'servico2'
        nova_duracao = 20

        #Atualiza no banco o serviço local com os novos valores
        ServicoDao.atualiza_servico(self.conexao, serv1, novo_nome_servico, nova_duracao )
        #Consulta o serviço no banco a partir do novo nome
        servicos = ServicoDao.consultar_servico_nome(self.conexao, 'servico2')

        #Faz o unpacking dos atributos da instancia do serviço recuperada do banco
        id, nome, duracao = servicos[0]
    
        #Verifica se o valor retornado do banco para o atributo duração é o valor informado para a nova duração do serviço
        self.assertEqual(duracao, 20)


if __name__ == '__main__':
    unittest.main()

