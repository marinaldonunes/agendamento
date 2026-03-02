import sqlite3 as sql
from servico import Servico

class ServicoDao:

    @staticmethod
    def criar_tabela_servico(conexao):

        comando = "create table  if not exists servicos (" \
            "id integer primary key autoincrement, " \
            "nome_servico varchar(100) not null unique, " \
            "duracao_minutos integer)"

        try:
            cursor = conexao.cursor()
            cursor.execute(comando)
        except sql.DatabaseError as erro:
            print(erro)

    @staticmethod
    def inserir_servico(conexao, p_servico):

        comando_inserir = 'insert into servicos(nome_servico, duracao_minutos) values(?, ?)'

        try:
            cursor = conexao.cursor()
            cursor.execute(comando_inserir, (p_servico.get_nome_servico(), p_servico.get_duracao()))
            ultimo_id = cursor.lastrowid

            conexao.commit()
            return ultimo_id
        except sql.DatabaseError as erro:
            print("Erro inserir na tabela o servico {}. {}".format(p_servico.get_nome_servico(), erro))
            return -1


    @staticmethod
    def consultar_servico_nome(conexao, p_nome):

        comando_consultar_servico = "select id, nome_servico, duracao_minutos from servicos where nome_servico like ?"

        lista_serv = []
        try:
            cursor = conexao.cursor()
            cursor.execute(comando_consultar_servico, (p_nome,))
            lista_serv = cursor.fetchall()
            return lista_serv
        except sql.DatabaseError as err:
            print("Erro na consulta serviços cadastrados - Detalhe: {}".format(err))
            return lista_serv

    @staticmethod
    def consultar_servico_id(conexao, p_id):

        comando_consultar_servicos = 'select id, nome_servico, duracao_minutos from servicos where id=?'

        try:
            cursor = conexao.cursor()
            cursor.execute(comando_consultar_servicos, (p_id,))
            r_servico = cursor.fetchone()
            if r_servico:
                servico = Servico(r_servico[1], r_servico[2], p_id=r_servico[0])
                return servico
            return None
        except sql.DatabaseError as erro:
            print("Erro ao consulta todos os servicos. {}".format(erro))
            return -1


    @staticmethod
    def consultar_servicos(conexao):

        comando_consultar_servicos = 'select id, nome_servico, duracao_minutos from servicos'

        try:
            cursor = conexao.cursor()
            r_servicos = cursor.execute(comando_consultar_servicos)
            return r_servicos
        except sql.DatabaseError as erro:
            print("Erro ao consulta todos os servicos. {}".format(erro))
            return -1


    @staticmethod
    def excluir_servico(conexao, id):

        comando_excluir = 'delete from servicos where id = ?'

        try:
            cursor = conexao.cursor()
            cursor.execute(comando_excluir, (id,))
            conexao.commit()
            return 1
        except sql.DatabaseError as erro:
            print("Erro inserir na tabela o servico {}. {}".format(id, erro))
            return -1

    @staticmethod
    def atualiza_servico(conexao, servicoAtual, nome, duracao):

        comando = 'update servicos set nome_servico=?, duracao_minutos=? where id=?'

        try:
            if (servicoAtual.get_nome_servico() != nome or
                servicoAtual.get_duracao() != duracao):
                cursor = conexao.cursor()
                cursor.execute(comando, (nome, duracao, servicoAtual.get_id()))
                conexao.commit()
                return 1
        except sql.DatabaseError as erro:
            print("Erro ao atualizar o servico {}. {}".format(servicoAtual.get_nome_servico(), erro))
            return -1
