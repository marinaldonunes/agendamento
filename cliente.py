
class Cliente:

    __slots__ = ['__id', '__nome', '__sobrenome', '__dt_nascimento', '__cpf', '__nome_mae', '__sexo', '__contatos']

    """ Os atributos marcados como False são para permitir que o construtor seja usado também sem parametros,
    ou seja, Cliente() """
    def __init__(self, nome, sobrenome, dtnascimento, cpf, nome_mae, sexo, p_id=0):
        self.__id = p_id
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__dt_nascimento = dtnascimento
        self.__cpf = cpf
        self.__nome_mae = nome_mae
        self.__sexo = sexo
        self.__contatos = list()

    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def get_sobrenome(self):
        return self.__sobrenome

    def get_cpf(self):
        return self.__cpf

    def get_sexo(self):
        return self.__sexo

    def get_dtnascimento(self):
        return self.__dt_nascimento

    def get_contatos(self):
        return self.__contatos

    def get_nome_mae(self):
        return self.__nome_mae

    def set_id(self, pcodigo):
        self.__id = pcodigo

    def set_nome(self, pnome):
        self.__nome = pnome

    def set_sobrenome(self, psobrenome):
        self.__sobrenome = psobrenome

    def set_cpf(self, pcpf):
        self.__cpf = pcpf

    def set_sexo(self, psexo):
        self.__sexo = psexo

    def set_dtnascimento(self, pdt_nasc):
        self.__dt_nascimento = pdt_nasc

    def set_contatos(self, plista):
        self.__contatos.extend(plista)

    def set_nome_mae(self, pnome):
        self.__nome_mae = pnome

    def __str__(self):
        print(self.get_nome() + " " + self.get_sobrenome())
        print(self.get_dtnascimento())
        print(self.get_cpf())
        print(self.get_nome_mae())
        print(self.get_sexo())
        print(self.get_contatos())
        return str(self.get_id())