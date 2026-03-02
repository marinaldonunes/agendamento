
class Profissional:
    __slots__ = ['__id_profissional', '__nome_profissional',  '__sobrenome_profissional', '__nr_registro',
                 '__uf_registro', '__sigla_conselho', '__contatos_prof']

    def __init__(self, p_nome_prof, p_sobrenome, p_nr_registro=' ', p_uf_registro=' ', p_sigla_conselho=' ', p_id=0):
        self.__id_profissional = p_id
        self.__nome_profissional = p_nome_prof
        self.__sobrenome_profissional = p_sobrenome
        self.__nr_registro = p_nr_registro
        self.__uf_registro = p_uf_registro
        self.__sigla_conselho = p_sigla_conselho
        self.__contatos_prof = list()  # lista contatos

    def get_id(self):
        return self.__id_profissional

    def get_nome(self):
        return self.__nome_profissional

    def get_sobrenome(self):
        return self.__sobrenome_profissional

    def get_nr_registro(self):
        return self.__nr_registro

    def get_uf_registro(self):
        return self.__uf_registro

    def get_sigla_conselho(self):
        return self.__sigla_conselho

    def get_contatos(self):
        return self.__contatos_prof

    def set_id(self, valor):
        self.__id_profissional = valor

    def set_nome(self, valor):
        self.__nome_profissional = valor

    def set_sobrenome(self, valor):
        self.__sobrenome_profissional = valor

    def set_nr_registro(self, valor):
        self.__nr_registro = valor

    def set_uf_registro(self, valor):
        self.__uf_registro = valor

    def set_sigla_conselho(self, valor):
        self.__sigla_conselho = valor

    def set_contatos(self, valor):
            self.__contatos_prof.extend(valor)

    def __str__(self):
        print(self.get_nome() + " " + self.get_sobrenome())
        print("Conselho/Registro/UF: {}/{}/{}".format(self.get_sigla_conselho(), self.get_nr_registro(),self.get_uf_registro()))
        print(self.get_contatos())
        return str(self.get_id())