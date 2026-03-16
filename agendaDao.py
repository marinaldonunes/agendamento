import sqlite3 as sql
from agenda import Agenda
from profissional import Profissional
from profissionalDao import ProfissionalDao
import os
import datetime as dt

class AgendaDao:

    @staticmethod
    def criar_tabela_agenda(conexao):

        comando = 'create table  if not exists agendas (' \
                  'id_profissional number not null,' \
                  'data date not null, ' \
                  'horario varchar(4) not null, ' \
                  'primary key(id_profissional, data, horario), '\
                  'foreign key(id_profissional) references profissionais(id) ' \
                  ')'

        try:
            cursor = conexao.cursor()
            cursor.execute(comando)
        except sql.DatabaseError as erro:
            print(erro)
            

    @staticmethod
    def inserir_agenda(conexao, p_agenda):

        comando_inserir = 'insert into agendas (id_profissional, data, horario) values (?,?,?)'

        try:
            cursor = conexao.cursor()
            data_sql = p_agenda.get_dia().strftime('%Y-%m-%d') if hasattr(p_agenda.get_dia(), 'strftime') else p_agenda.get_dia()
            cursor.execute(comando_inserir, (p_agenda.get_profissional().get_id(), data_sql,
                                             p_agenda.get_hora()))
            conexao.commit()
            return 1

        except sql.DatabaseError as erro:
            print("Erro inserir agenda do profissional {} no dia/hora: {} - {} - {}".
                  format(p_agenda.get_profissional().get_nome(), p_agenda.get_dia().strftime('%Y-%m-%d'), p_agenda.get_hora(), erro))
        return -1

    @staticmethod
    def consulta_agendas_prof(conexao, id_profissional):

        comando = 'select id_profissional, data, horario from agendas where id_profissional = ?'

        try:
        
            horarios = list()
            cursor = conexao.cursor()
            for reg in cursor.execute(comando, (id_profissional,)):               
                horarios.append((reg[1],reg[2]))

            return horarios

        except sql.DatabaseError as erro:
            print("Erro consultar agendas do profissional: {} - {}".format(id_profissional, erro))
            return -1

    @staticmethod
    def consulta_agendas(conexao):

        comando = 'select id_profissional, data, horario from agendas order by id_profissional, data, horario'

        try:
            registros = []
            cursor = conexao.cursor()
            for reg in cursor.execute(comando):
                registros.append((reg[0], reg[1], reg[2]))
            return registros
        except sql.DatabaseError as erro:
            print("Erro consultar todas as agendas - {}".format(erro))
            return -1


    @staticmethod
    def consulta_agenda(conexao, p_profissional, p_dia, p_hora):

        comando = 'select id_profissional, data, horario from agendas where id_profissional = ? and data = ? and horario = ?'     

        try:
            cursor = conexao.cursor()            
            data_sql = p_dia.strftime('%Y-%m-%d') if hasattr(p_dia, 'strftime') else p_dia
            prof_id = p_profissional.get_id()
            parametros = (prof_id, data_sql, p_hora)       
            cursor.execute(comando, parametros)  
            result = cursor.fetchone()  
            if result:
                agenda = Agenda()
                agenda.set_profissional(p_profissional)
                agenda.set_dia = p_dia
                agenda.set_hora = p_hora
                return agenda
            else:
                return -1
        except sql.DatabaseError as erro:
            print("Erro consultar agenda do profissional: {} - Data/hora: {}/{} - {}".format(prof_id, data_sql, p_hora, erro))            
        return -1



    @staticmethod
    def excluir_agenda(conexao, p_agenda):

        comando = 'delete from agendas where id_profissional = ? and data = ? and horario = ?'

        try:
            cursor = conexao.cursor()
            profissional_id = p_agenda.get_profissional().get_id()
            data_sql = p_agenda.get_dia().strftime('%Y-%m-%d') if hasattr(p_agenda.get_dia(), 'strftime') else p_agenda.get_dia()
            hora = p_agenda.get_hora()
            parametros = (profissional_id, data_sql, hora)
            cursor.execute(comando, parametros)
            conexao.commit()

            return 1
        except sql.DatabaseError as erro:
            print("Erro excluir agenda do profissional {} no dia/hora: {}/{} - {}".
                  format(p_agenda.get_profissional().get_nome(), p_agenda.get_dia().strftime('%Y-%m-%d'), p_agenda.get_hora(), erro))
        return -1
            

    @staticmethod
    def atualizar_agenda(conexao, p_prof, p_dia_atual, p_hora_atual, p_dia_nova, p_hora_nova):            

        try:
            cursor = conexao.cursor()
            agenda_existe = AgendaDao.consulta_agenda(conexao, p_prof, p_dia_atual, p_hora_atual)
            if agenda_existe:
                agenda = Agenda(p_prof, p_dia_atual, p_hora_atual )
                AgendaDao.excluir_agenda(conexao, agenda)
                agd_nova = Agenda(p_prof, p_dia_nova, p_hora_nova)    
                AgendaDao.inserir_agenda(conexao, agd_nova)   
                return 1         

        except sql.DatabaseError as erro:
            print("Erro agenda do profissional {} no dia/hora: {}/{} - {}".
                  format(agd_nova.get_profissional().get_nome(), agd_nova.get_dia(), agd_nova.get_hora(), erro))    
        return -1    





if __name__ == '__main__':

    caminho_banco = r"c:\temp\TesteBD.db"
    if os.path.exists(caminho_banco):
        os.remove(caminho_banco)
    conexao = sql.connect(caminho_banco)
    ProfissionalDao.cria_tabela_profissional(conexao)
    AgendaDao.criar_tabela_agenda(conexao)


    #Criação de um profissional para agedan
    prof1 = Profissional('zeZE', 'Pereira', 9999,  'PE',  'CRP')
    prof1.set_contatos(['fe@hotmail.br', '888888888'])
    prof_id = ProfissionalDao.insere_profissional(conexao, prof1)
    prof1.set_id(prof_id)    

    prof2 = Profissional('Pedro', 'Mane', 1452,  'MG',  'CRREFITO')
    prof2.set_contatos(['fe@hotmail.br', '888888888'])
    prof_id = ProfissionalDao.insere_profissional(conexao, prof2)
    prof2.set_id(prof_id)

    agd = Agenda(prof1, dt.datetime.strptime('20/05/2025', '%d/%m/%Y'), '0800')      
    agd2 = Agenda(prof2, dt.datetime.strptime('20/07/2025', '%d/%m/%Y'), '1000')          
    agd3 = Agenda(prof2, dt.datetime.strptime('21/07/2025', '%d/%m/%Y'), '1000')              

    AgendaDao.inserir_agenda(conexao, agd)
    AgendaDao.inserir_agenda(conexao, agd2)    
    AgendaDao.inserir_agenda(conexao, agd3)     

    AgendaDao.excluir_agenda(conexao, agd)

    AgendaDao.atualizar_agenda(conexao, prof2, dt.datetime.strptime('20/07/2025', '%d/%m/%Y'),'1000', dt.datetime.strptime('20/01/2026', '%d/%m/%Y'), '1130')     

    x = AgendaDao.consulta_agendas_prof(conexao, prof2.get_id())
    print(x)

    
          
