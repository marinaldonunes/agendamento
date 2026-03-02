import sqlite3 as sql
from cliente import Cliente


class ClienteDao:

    @staticmethod
    def cria_tabela_cliente(conexao):

        comando = "create table  if not exists clientes(id integer primary key autoincrement, " \
                  "nome varchar(60) not null, " \
                  "sobrenome varchar(100) not null, " \
                  "dt_nascimento date, " \
                  "cpf varchar(11) unique, " \
                  "nome_mae varchar(150), " \
                  "sexo varchar(1) not null)"

        comando2 = "create table  if not exists contatos_clientes (id integer not null, " \
                   "contato varchar(80) not null, " \
                   " primary key(id, contato) " \
                   " foreign key(id) references clientes(id)" \
                   ")"

        try:
            cursor = conexao.cursor()
            cursor.execute(comando)
            cursor.execute(comando2)
        except sql.DatabaseError as erro:
            print(erro)

    @staticmethod
    def insere_cliente(conexao, cli):
        comando = "insert into clientes(nome, sobrenome, dt_nascimento, cpf, nome_mae, sexo) values(?,?,?,?,?,?)"
        cmd_insert_contato = "insert into contatos_clientes(id, contato) values(?, ?)"

        try:
            cursor = conexao.cursor()
            dt_nasc_sql = cli.get_dtnascimento().strftime('%Y-%m-%d') if hasattr(cli.get_dtnascimento(), 'strftime') else cli.get_dtnascimento()
            cursor.execute(comando, (cli.get_nome(), cli.get_sobrenome(), dt_nasc_sql, cli.get_cpf(),
                                     cli.get_nome_mae(), cli.get_sexo()))

            ultimo_id = cursor.lastrowid

            for contato in cli.get_contatos():
                cursor.execute(cmd_insert_contato, (ultimo_id, contato))

            conexao.commit()
            return ultimo_id

        except sql.DatabaseError as err:
            print("Erro ao inserir o cliente {} - Detalhe: {}".format(cli.get_nome(), err))            
            return -1


    @staticmethod
    def exclui_cliente(conexao, p_id):
        comando = 'delete from clientes where id = ?'
        comando_exl_contatos = 'delete from contatos_clientes where id = ?'
        try:
            cursor = conexao.cursor()
            cursor.execute(comando_exl_contatos, (p_id,))
            cursor.execute(comando, (p_id,))
            conexao.commit()
            return 1
        except sql.DatabaseError as err:
            print("Usuario com o código {} não pode ser excluído - Detalhe: {}".format(p_id, err))            
            return -1


    @staticmethod
    def consulta_cliente_cpf(conexao, p_cpf):
        comando = 'select id, nome, sobrenome, dt_nascimento, cpf, nome_mae, sexo from clientes where cpf = ?'
        comando_contatos = 'select contato from contatos_clientes where id=?'
        try:
            cursor = conexao.cursor()
            for  id, nome, sobrenome, dtnasc, cpf, mae, sexo  in cursor.execute(comando, (p_cpf,)):
                ret_cliente = Cliente(nome, sobrenome, dtnasc, cpf, mae, sexo, p_id=id)

                cursor_cont = conexao.cursor()
                for r_cont in cursor_cont.execute(comando_contatos, (ret_cliente.get_id(),)):
                    ret_cliente.get_contatos().append(r_cont[0])

                return ret_cliente

        except sql.DatabaseError as err:
            print("Cliente não pode ser consultado - Detalhe: {}".format(err))
        return None

    @staticmethod
    def consulta_cliente_id(conexao, p_id):
        comando = "select id, nome, sobrenome, dt_nascimento, cpf, nome_mae, sexo from clientes where id = ?"
        comando_contatos = 'select contato from contatos_clientes where id=?'
        try:
            cursor = conexao.cursor()
            for id, nome, sobrenome, dtnasc, cpf, mae, sexo in cursor.execute(comando, (p_id,)):
                ret_cliente = Cliente(nome, sobrenome, dtnasc, cpf, mae, sexo, p_id=id)

                cursor_cont = conexao.cursor()
                for r_cont in cursor_cont.execute(comando_contatos, (ret_cliente.get_id(),)):
                    ret_cliente.get_contatos().append(r_cont[0])

                return ret_cliente

        except sql.DatabaseError as err:
            print("Cliente não pode ser consultado - Detalhe: {}".format(err))
        return None

    @staticmethod
    def consulta_cliente_nome_dtnasc(conexao, p_nome, p_dt_nasc):
        comando = "select id, nome, sobrenome, dt_nascimento, cpf, nome_mae, sexo from clientes where nome like ? and dt_nascimento = ?"
        comando_contatos = 'select contato from contatos_clientes where id=?'
        try:
            lista_clientes = list()
            cursor = conexao.cursor()
            dt_nasc_sql = p_dt_nasc.strftime('%Y-%m-%d') if hasattr(p_dt_nasc, 'strftime') else p_dt_nasc
            for  id, nome, sobrenome, dtnasc, cpf, mae, sexo in cursor.execute(comando, (p_nome, dt_nasc_sql)):
                ret_cliente = Cliente(nome, sobrenome, dtnasc, cpf, mae, sexo, p_id=id)

                cursor_cont = conexao.cursor()
                for r_cont in cursor_cont.execute(comando_contatos, (id,)):
                    ret_cliente.get_contatos().append(r_cont[0])

                lista_clientes.append(ret_cliente)

            return lista_clientes
        except sql.DatabaseError as err:
            print("Cliente não pode ser consultado - Detalhe: {}".format(err))
        return None

    @staticmethod
    def consulta_clientes(conexao):
        comando = 'select a.id, a.nome, a.sobrenome, a.dt_nascimento, a.nome_mae, a.cpf, a.sexo from clientes a'
        listaclientes = []
        try:
            cursor = conexao.cursor()
            cursor.execute(comando)
            listaclientes = cursor.fetchall()
        except sql.DatabaseError as err:
            print("Erro na consulta dos clientes cadastrados - Detalhe: {}".format(err))
        return listaclientes

    @staticmethod
    def atualiza_cliente(conexao, cli_atual, cli_novo):
        comando_atu_cliente = " update clientes " \
                              " set nome = ?, dt_nascimento = ?, nome_mae = ?,  cpf= ?, sexo = ? " \
                              " where id = ?"
        comando_exl_contatos = 'delete from contatos_clientes where id = ?'
        cmd_insert_contato = "insert into contatos_clientes(id, contato) values(?, ?)"
        try:
            cursor = conexao.cursor()
            if (cli_atual.get_nome() != cli_novo.get_nome() or
                    cli_atual.get_dtnascimento() != cli_novo.get_dtnascimento() or
                    cli_atual.get_cpf() != cli_novo.get_cpf() or
                    cli_atual.get_nome_mae() != cli_novo.get_nome_mae() or
                    cli_atual.get_sexo() != cli_novo.get_sexo()):

                dt_nasc_sql = cli_novo.get_dtnascimento().strftime('%Y-%m-%d') if hasattr(cli_novo.get_dtnascimento(), 'strftime') else cli_novo.get_dtnascimento()
                cursor.execute(comando_atu_cliente, (cli_novo.get_nome(), dt_nasc_sql, cli_novo.get_nome_mae(),
                               cli_novo.get_cpf(), cli_novo.get_sexo(), cli_atual.get_id()))

                # Exclui e reinclui todos os contatos
                cursor.execute(comando_exl_contatos, (cli_atual.get_id(),))
                for contato in cli_novo.get_contatos():
                    cursor.execute(cmd_insert_contato, (cli_atual.get_id(), contato))

                conexao.commit()
                return cli_novo # Sucesso, retorna os dados dos dados atualizados

        except sql.DatabaseError as err:
            print("Cliente não foi atualizado corretamente - Detalhe: {}".format(err))
            return cli_atual # Ocorrendo erro, o metodo retorna os dados do cliente sem atualização
