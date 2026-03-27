import sqlite3 as sql
import os
import datetime as dt
from agendaDao import AgendaDao
from clienteDao import ClienteDao
from servicoDao import ServicoDao
from profissionalDao import ProfissionalDao
from profissional import Profissional
from agenda import Agenda
from cliente import Cliente
from servico import Servico
from agendamento import Agendamento



class AgendamentoDao:

    @staticmethod
    def criar_tabela_agendamento(conexao):

        comando = "create table  if not exists agendamentos (" \
                  "id_agendamento integer primary key autoincrement not null, " \
                  "id_cliente number not null, " \
                  "id_servico number not null, " \
                  "id_agenda number not null, " \
                  "foreign key(id_cliente) references clientes(id), " \
                  "foreign key(id_agenda) references agendas(id_agenda), " \
                  "foreign key(id_servico) references servicos(id))"

        try:
            cursor = conexao.cursor()
            cursor.execute(comando)
        except sql.DatabaseError as erro:
            print(erro)

    @staticmethod
    def inserir_agendamentos(conexao, p_agendamento):

        comando_inserir = "insert into agendamentos(id_cliente, id_servico, id_agenda) " \
                          "values (?,?,?)"

        try:
            cursor = conexao.cursor()
            data_sql = p_agendamento.get_agenda().get_dia().strftime('%Y-%m-%d') if hasattr(p_agendamento.get_agenda().get_dia(), 'strftime') else p_agendamento.get_agenda().get_dia()
            cursor.execute(comando_inserir, (p_agendamento.get_cliente().get_id(), p_agendamento.get_servico().get_id(),
                           p_agendamento.get_agenda().get_id_agenda()))
            
            ultimo_id = cursor.lastrowid            

            conexao.commit()
            return ultimo_id
        except sql.DatabaseError as erro:
            print("Erro ao incluir agendamento. {}".format(erro))
        return -1

    @staticmethod
    def existe_agendamento(conexao, prof_id, data, hora):
        comando = "select 1 from agendamentos a, agendas b where b.id_profissional = ? and b.data = ? and b.hora = ? and a.id_agenda = b.id_agenda"
        try:
            cursor = conexao.cursor()
            data_sql = data.strftime('%Y-%m-%d') if hasattr(data, 'strftime') else data
            cursor.execute(comando, (prof_id, data_sql, hora))
            return cursor.fetchone() is not None
        except sql.DatabaseError as erro:
            print("Erro ao verificar agendamento. {} - {}".format((prof_id, data, hora), erro))
        return False


    @staticmethod
    def consultar_agendamento(conexao, p_id):

        comando_consulta_agd = "select a.id_agendamento, a.id_cliente, a.id_servico, b.id_profissional, b.data, b.hora " \
                               "from agendamentos a, agendas b where a.id_agendamento = ? and a.id_agenda = b.id_agenda "
        try:
            cursor = conexao.cursor()
            cursor.execute(comando_consulta_agd, (p_id,))
            result = cursor.fetchone()  
            if result:

                cliente = ClienteDao.consulta_cliente_id(conexao, result[1])
                servico = ServicoDao.consultar_servico_id(conexao,result[2])                
                profissional = ProfissionalDao.consulta_profissional_id(conexao,result[3])
                agenda = Agenda(profissional, result[4], result[5])

                r_agendamento = Agendamento(result[0],cliente, servico, agenda)

                return r_agendamento
        except sql.DatabaseError as erro:
            print("Erro ao recuperar agendamento id:. {} - {}".format(p_id, erro))
        return -1


    @staticmethod
    def consultar_agendamentos_cliente(conexao, p_id):

        comando_consulta_agd = "select a.id_agendamento, a.id_cliente, a.id_servico, b.id_profissional, b.data, b.hora " \
                               "from agendamentos a, agendas b where a.id_cliente = ? and a.id_agenda = b.id_agenda "

        try:
            cursor = conexao.cursor()
            r_agendamentos = cursor.execute(comando_consulta_agd, (p_id,))
            return r_agendamentos
        except sql.DatabaseError as erro:
            print("Erro ao recuperar agendamento id:. {} - {}".format(p_id, erro))
        return -1


    @staticmethod
    def consultar_agendamentos_profissional(conexao, p_id):

        comando_consulta_agd = "select a.id_agendamento, a.id_cliente, a.id_servico, b.id_profissional, b.data, b.hora " \
                               "from agendamentos a, agendas b where b.id_profissional = ? and a.id_agenda = b.id_agenda "
        try:
            cursor = conexao.cursor()
            r_agendamentos = cursor.execute(comando_consulta_agd, (p_id,))
            return r_agendamentos
        except sql.DatabaseError as erro:
            print("Erro ao recuperar agendamento id:. {} - {}".format(p_id, erro))
        return -1


    @staticmethod
    def consultar_agendamentos_servicos(conexao, p_id):

        comando_consulta_agd = "select a.id_agendamento, a.id_cliente, a.id_servico, b.id_profissional, b.data, b.hora " \
                               "from agendamentos a, agendas b where a.id_servico = ? and a.id_agenda = b.id_agenda "
        try:
            cursor = conexao.cursor()
            r_agendamentos = cursor.execute(comando_consulta_agd, (p_id,))
            return r_agendamentos
        except sql.DatabaseError as erro:
            print("Erro ao recuperar agendamento id:. {} - {}".format(p_id, erro))
        return -1


    @staticmethod
    def consultar_agendamentos_data(conexao, p_data):

        comando_consulta_agd = "select a.id_agendamento, a.id_cliente, a.id_servico, b.id_profissional, b.data, b.hora " \
                               "from agendamentos a, agendas b where b.data = ? and a.id_agenda = b.id_agenda "
        try:
            cursor = conexao.cursor()
            data_sql = p_data.strftime('%Y-%m-%d') if hasattr(p_data, 'strftime') else p_data
            r_agendamentos = cursor.execute(comando_consulta_agd, (data_sql,))
            return r_agendamentos
        except (sql.DatabaseError, TypeError, ValueError) as erro:
            print("Erro ao recuperar agendamento id:. {} - {}".format(p_data, erro))
        return -1


    @staticmethod
    def consultar_agendamentos_data_hora(conexao, p_data, p_hora):

        comando_consulta_agd = "select a.id_agendamento, a.id_cliente, a.id_servico, b.id_profissional, b.data, b.hora " \
                               "from agendamentos a, agendas b where b.data = ?  and b.hora=? and a.id_agenda = b.id_agenda "
        
        try:
            cursor = conexao.cursor()
            data_sql = p_data.strftime('%Y-%m-%d') if hasattr(p_data, 'strftime') else p_data
            parametros = (data_sql, p_hora)
            r_agendamentos = cursor.execute(comando_consulta_agd, parametros)
            return r_agendamentos
        except (sql.DatabaseError, TypeError, ValueError) as erro:
            print("Erro ao recuperar agendamento id:. {} : {} - {}".format(p_data, p_hora, erro))
        return -1


    @staticmethod
    def excluir_agendamento(conexao, p_agd):

        comando_excluir = "delete from agendamentos where id_agendamento = ?"

        try:
            cursor = conexao.cursor()
            cursor.execute(comando_excluir, (p_agd.get_id(),))
            conexao.commit()
            return 1
        except sql.DatabaseError as erro:
            print("Erro ao incluir agendamento. {}".format(erro))
        return -1






if __name__ == '__main__':

    caminho_banco = r"c:\temp\TesteBD.db"
    if os.path.exists(caminho_banco):
        os.remove(caminho_banco)
    conexao = sql.connect(caminho_banco)
    ProfissionalDao.cria_tabela_profissional(conexao)
    AgendaDao.criar_tabela_agenda(conexao)
    ServicoDao.criar_tabela_servico(conexao)
    ClienteDao.cria_tabela_cliente(conexao)
    AgendamentoDao.criar_tabela_agendamento(conexao)

    prof1 = Profissional('Jose', 'Pereira', 9999,  'PE',  'CRP')
    prof1.set_contatos(['zepe@hotmail.br', '99999999'])
    prof_id = ProfissionalDao.insere_profissional(conexao, prof1)
    prof1.set_id(prof_id)    

    prof2 = Profissional('Pedro', 'Sales', 1452,  'MG',  'CRREFITO')
    prof2.set_contatos(['psales@hotmail.br', '888888888'])
    prof_id = ProfissionalDao.insere_profissional(conexao, prof2)
    prof2.set_id(prof_id)

    agd1 = Agenda(prof1, dt.datetime.strptime('20/05/2025', '%d/%m/%Y'), '0800')      
    agd2 = Agenda(prof2, dt.datetime.strptime('20/07/2025', '%d/%m/%Y'), '1000')          
    agd3 = Agenda(prof2, dt.datetime.strptime('21/07/2025', '%d/%m/%Y'), '1000')              

    AgendaDao.inserir_agenda(conexao, agd1)
    AgendaDao.inserir_agenda(conexao, agd2)    
    AgendaDao.inserir_agenda(conexao, agd3)     

    serv1 = Servico('Massagem', 60)
    serv2 = Servico('Natacao', 50)    
    serv3 = Servico('Pilates', 50)
    serv4 = Servico('FastMassage', 30)    

    idServ = ServicoDao.inserir_servico(conexao, serv1)
    serv1.set_id(idServ)

    idServ = ServicoDao.inserir_servico(conexao, serv2)
    serv2.set_id(idServ)

    idServ = ServicoDao.inserir_servico(conexao, serv3)
    serv3.set_id(idServ)

    idServ = ServicoDao.inserir_servico(conexao, serv4)      
    serv4.set_id(idServ)    

    cli1 = Cliente(nome='Mario', sobrenome='Oliveira', dtnascimento=dt.datetime.strptime('20/05/1980', "%d/%m/%Y"),
                    cpf='1111111111111', nome_mae='Marina Joana', sexo='M')
    cli1.set_contatos(['mns@hotmail.br', '8387987987'])  

    cli2 = Cliente(nome='Fernanda', sobrenome='Silva', dtnascimento=dt.datetime.strptime('10/01/1950', "%d/%m/%Y"),
                    cpf='147852369963', nome_mae='Marta Maria', sexo='F')
    cli2.set_contatos(['fe@hotmail.br', '8332165489'])      

    id = ClienteDao.insere_cliente(conexao, cli1)
    cli1.set_id(id)

    id = ClienteDao.insere_cliente(conexao, cli2)
    cli2.set_id(id)    

    marcacao1 = Agendamento(0, cli1, serv1, agd1.get_id())
    marcacao2 = Agendamento(0, cli2, serv2, agd2.get_id())
    marcacao3 = Agendamento(0, cli2, serv3, agd3.get_id())

    idAgd = AgendamentoDao.inserir_agendamentos(conexao,marcacao1)
    marcacao1.set_id(idAgd)
    idAgd =AgendamentoDao.inserir_agendamentos(conexao,marcacao2)
    marcacao2.set_id(idAgd)
    idAgd =AgendamentoDao.inserir_agendamentos(conexao,marcacao3)        
    marcacao3.set_id(idAgd)

    AgendamentoDao.excluir_agendamento(conexao, marcacao1)

    print(AgendamentoDao.consultar_agendamento(conexao, marcacao3.get_id()))
