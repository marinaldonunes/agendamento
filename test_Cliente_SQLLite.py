import sqlite3 as sql
import unittest
import datetime as dt
import os

from clienteDao import ClienteDao
from cliente import Cliente


class TesteClienteSQLLite(unittest.TestCase):
    

    def setUp(self):
        """Configuração antes de cada teste"""
        self.caminho_banco = "TesteBD.db"

        # Remove o banco de dados anterior, garantindo um ambiente de testes limpo
        if os.path.exists(self.caminho_banco):
            os.remove(self.caminho_banco)

        # Cria uma nova conexão para cada teste
        self.conexao = sql.connect(self.caminho_banco)
        ClienteDao.cria_tabela_cliente(self.conexao)


    def tearDown(self):
        """Encerramento após cada teste"""
        self.conexao.close()  # Fecha a conexão ao final de cada teste
        if os.path.exists(self.caminho_banco):
            os.remove(self.caminho_banco)  # Remove o banco após o teste             


    def test_InserirCliente(self):
       
        cli = Cliente(nome='Mario', sobrenome='Oliveira', dtnascimento=dt.datetime.strptime('20/05/1980', "%d/%m/%Y"),
                    cpf='1111111111111', nome_mae='Marina Joana', sexo='M')
        cli.set_contatos(['mns@hotmail.br', '8387987987'])        

        self.assertNotEqual(ClienteDao.insere_cliente(self.conexao, cli), -1)


    def test_ExcluirCliente(self):
       
        cli = Cliente(nome='Mario', sobrenome='Oliveira', dtnascimento=dt.datetime.strptime('20/05/1980', "%d/%m/%Y"),
                    cpf='1111111111111', nome_mae='Marina Joana', sexo='M')
        cli.set_contatos(['mns@hotmail.br', '8387987987'])  

        codCli = ClienteDao.insere_cliente(self.conexao, cli)      
        self.assertEqual(ClienteDao.exclui_cliente(self.conexao, codCli), 1)

    def test_AtualizarCliente(self):

        cli_banco = Cliente(nome='Mario', sobrenome='Oliveira', dtnascimento=dt.datetime.strptime('20/05/1980', "%d/%m/%Y"),
                    cpf='1111111111111', nome_mae='Marina Joana', sexo='M')
        cli_banco.set_contatos(['mns@hotmail.br', '8387987987']) 
        ClienteDao.insere_cliente(self.conexao, cli_banco)

        cli_novo = Cliente(nome='Mario', sobrenome='Oliveira', dtnascimento=dt.datetime.strptime('20/05/1980', "%d/%m/%Y"),
                    cpf='222222222222', nome_mae='Marina Joana', sexo='M')
        cli_novo.set_contatos(['mns@hotmail.br', '83123456789'])  

        resultado = ClienteDao.atualiza_cliente(self.conexao, cli_banco, cli_novo)      
        self.assertEqual(resultado.get_cpf(), '222222222222') and self.assertEqual(resultado.get_nome(), 'Mario')


    def test_ConsultaClientePorCPF(self):

        cli = Cliente(nome='Mario', sobrenome='Oliveira', dtnascimento=dt.datetime.strptime('20/05/1980', "%d/%m/%Y"),
                    cpf='222222222222', nome_mae='Marina Joana', sexo='M')
        cli.set_contatos(['mns@hotmail.br', '8387987987'])        
        
        ClienteDao.insere_cliente(self.conexao, cli)

        self.assertIsInstance(ClienteDao.consulta_cliente_cpf(self.conexao, '222222222222'), Cliente)


    def test_ConsultaListaClientes(self):

        cli = Cliente(nome='Mario', sobrenome='Oliveira', dtnascimento=dt.datetime.strptime('20/05/1980', "%d/%m/%Y"),
                    cpf='222222222222', nome_mae='Marina Joana', sexo='M')
        cli.set_contatos(['mns@hotmail.br', '8387987987'])        
        ClienteDao.insere_cliente(self.conexao, cli)

        cli2= Cliente(nome='Maria', sobrenome='Pereira', dtnascimento=dt.datetime.strptime('20/05/2000', "%d/%m/%Y"),
                    cpf='11111111111', nome_mae='Marina Joana', sexo='F')
        cli2.set_contatos(['mns@hotmail.br', '83963258741'])    
        ClienteDao.insere_cliente(self.conexao, cli2)

        cli3= Cliente(nome='Luiz', sobrenome='Pereira', dtnascimento=dt.datetime.strptime('20/05/2020', "%d/%m/%Y"),
                    cpf='987654321', nome_mae='Edna Marta', sexo='M')
        cli3.set_contatos(['mns@hotmail.br', '83963258741'])    
        ClienteDao.insere_cliente(self.conexao, cli3)        

        lista = ClienteDao.consulta_clientes(self.conexao)
        self.assertEqual(len(lista), 3)


if __name__ == "__main__":
    unittest.main()
