import sqlite3 as sql
from profissional import Profissional


class ProfissionalDao:

    @staticmethod
    def cria_tabela_profissional(conexao):
        comando = 'create table if not exists profissionais (' \
                  'id integer primary key autoincrement, ' \
                  'nome varchar(60) not null, ' \
                  'sobrenome varchar(150) not null, ' \
                  'nr_registro varchar(6), ' \
                  'uf_registro varchar(2), ' \
                  'sigla_conselho varchar(10)' \
                  ')'

        comando2 = "create table  if not exists  contatos_profissionais (id integer not null, contato varchar(80) not null, " \
                   " primary key(id, contato) " \
                   " foreign key(id) references profissionais(id)" \
                   ")"

        try:
            cursor = conexao.cursor()
            cursor.execute(comando)
            cursor.execute(comando2)
        except sql.DatabaseError as erro:
            print(erro)

    @staticmethod
    def insere_profissional(conexao, prof):
        comando = "insert into profissionais(nome, sobrenome, nr_registro, uf_registro, sigla_conselho) values(?,?,?,?,?)"
        cmd_insert_contato = "insert into contatos_profissionais(id, contato) values(?, ?)"

        try:
            cursor = conexao.cursor()
            cursor.execute(comando, (prof.get_nome(), prof.get_sobrenome(), prof.get_nr_registro(),
                                     prof.get_uf_registro(), prof.get_sigla_conselho()))

            ultimo_id = cursor.lastrowid

            for contato in prof.get_contatos():
                cursor.execute(cmd_insert_contato, (ultimo_id, contato))

            conexao.commit()
            return ultimo_id

        except sql.DatabaseError as err:
            print("Erro ao inserir o profissional {} - Detalhe: {}".format(prof.get_nome(), err))
            return -1

    @staticmethod
    def exclui_profissional(conexao, p_id):
        comando = 'delete from profissionais where id = ?'
        comando_exl_contatos = 'delete from contatos_profissionais where id = ?'
        try:
            cursor = conexao.cursor()
            cursor.execute(comando_exl_contatos, (p_id,))
            cursor.execute(comando, (p_id,))
            conexao.commit()
            return 1
        except sql.DatabaseError as err:
            print("Profissional com o código {} não pode ser excluído - Detalhe: {}".format(p_id, err))
            return -1

    @staticmethod
    def consulta_profissionaol_conselho(conexao, p_nr_registro, p_uf):
        comando = 'select id, nome, sobrenome, nr_registro, uf_registro, sigla_conselho from ' \
                  'profissionais where nr_registro = ? and uf_registro = ? '
        comando_contatos = 'select contato from contatos_profissionais where id=?'
        try:
            ret_prof = None
            cursor = conexao.cursor()
            for reg in cursor.execute(comando, (p_nr_registro,p_uf)):
                ret_prof = Profissional(reg[1],reg[2],reg[3],reg[4],reg[5],p_id=reg[0])

                cursor_cont = conexao.cursor()
                for r_cont in cursor_cont.execute(comando_contatos, (ret_prof.get_id(),)):
                    ret_prof.get_contatos().append(r_cont[0])

                return ret_prof #Retorna um objeto Profissional

        except sql.DatabaseError as err:
            print("Cliente não pode ser consultado - Detalhe: {}".format(err))
        return None

    @staticmethod
    def consulta_profissional_id(conexao, p_id):
        comando = "select  id, nome, sobrenome, nr_registro, uf_registro, sigla_conselho  from profissionais where id = ?"
        comando_contatos = 'select contato from contatos_profissionais where id=?'
        try:
            ret_prof = None
            cursor = conexao.cursor()
            for reg in cursor.execute(comando, (p_id,)):
                ret_prof = Profissional(reg[1],reg[2],reg[3],reg[4],reg[5],p_id=reg[0])

                cursor_cont = conexao.cursor()
                for r_cont in cursor_cont.execute(comando_contatos, (ret_prof.get_id(),)):
                    ret_prof.get_contatos().append(r_cont[0])

                return ret_prof #Retorna um objeto Profissional

        except sql.DatabaseError as err:
            print("Profissional não pode ser consultado - Detalhe: {}".format(err))
        return None

    @staticmethod
    def consulta_profissional_nome(conexao, p_nome):
        comando = "select  id, nome, sobrenome, nr_registro, uf_registro, sigla_conselho from profissionais where nome like ?"
        comando_contatos = 'select contato from contatos_profissionais where id=?'
        try:
            lista_profs = list()
            cursor = conexao.cursor()
            for reg in cursor.execute(comando, (p_nome,)):
                ret_prof = Profissional(reg[1],reg[2],reg[3],reg[4],reg[5],p_id=reg[0])

                cursor_cont = conexao.cursor()
                for r_cont in cursor_cont.execute(comando_contatos, (reg[0],)):
                    ret_prof.get_contatos().append(r_cont[0])

                lista_profs.append(ret_prof)

            return lista_profs
        except sql.DatabaseError as err:
            print("Profissional não pode ser consultado - Detalhe: {}".format(err))
        return None

    @staticmethod
    def consulta_profissionais(conexao):
        comando = 'select  id, nome, sobrenome, nr_registro, uf_registro, sigla_conselho from profissionais a'
        lista_profs = []
        try:
            cursor = conexao.cursor()
            cursor.execute(comando)
            lista_profs = cursor.fetchall()
        except sql.DatabaseError as err:
            print("Erro na consulta dos profissionais cadastrados - Detalhe: {}".format(err))
        return lista_profs

    @staticmethod
    def atualiza_profissional(conexao, prof_atual, prof_novo):
        comando_atu_prof = " update profissionais " \
                              " set nome = ?, sobrenome = ?, nr_registro = ?, uf_registro = ?,  sigla_conselho= ? where id = ?"
        comando_exl_contatos = 'delete from contatos_profissionais where id = ?'
        cmd_insert_contato = "insert into contatos_profissionais(id, contato) values(?, ?)"
        try:
            cursor = conexao.cursor()
            mudou_dados = (
                prof_atual.get_nome() != prof_novo.get_nome()
                or prof_atual.get_sobrenome() != prof_novo.get_sobrenome()
                or prof_atual.get_nr_registro() != prof_novo.get_nr_registro()
                or prof_atual.get_uf_registro() != prof_novo.get_uf_registro()
                or prof_atual.get_sigla_conselho() != prof_novo.get_sigla_conselho()
            )
            contatos_atual = prof_atual.get_contatos() or []
            contatos_novo = prof_novo.get_contatos() or []
            mudou_contatos = contatos_atual != contatos_novo

            if mudou_dados:
                cursor.execute(comando_atu_prof, (prof_novo.get_nome(), prof_novo.get_sobrenome(), prof_novo.get_nr_registro(),
                               prof_novo.get_uf_registro(), prof_novo.get_sigla_conselho(), prof_novo.get_id()))

            if mudou_dados or mudou_contatos:
                # Exclui e reinclui todos os contatos
                cursor.execute(comando_exl_contatos, (prof_novo.get_id(),))
                for contato in prof_novo.get_contatos():
                    cursor.execute(cmd_insert_contato, (prof_novo.get_id(), contato))

                conexao.commit()
                return prof_novo  # Sucesso, retorna os dados dos dados atualizados
            return prof_novo

        except sql.DatabaseError as err:
            print("Profissional n??o foi atualizado corretamente - Detalhe: {}".format(err))
            return prof_atual # Ocorrendo erro, o metodo retorna os dados do cliente sem atualiza????o

