"""  Classe dos serviços oferecidos pelo estabelecimento"""


class Servico:
    __slots__ = ['__id_servico', '__nome_servico', '__duracao']

    def __init__(self, p_servico, p_duracao, p_id=0):
        self.__id_servico = p_id
        self.__nome_servico = p_servico
        self.__duracao = p_duracao

    def get_id(self):
        return self.__id_servico

    def get_nome_servico(self):
        return self.__nome_servico

    def get_duracao(self):
        return self.__duracao

    def set_id(self, valor):
        self.__id_servico = valor

    def set_nome_servico(self, valor):
        self.__nome_servico = valor

    def set_duracao(self, valor):
        self.__duracao = valor

    def __str__(self):
        return("Serviço ==> id: {} / Descricao:{}".format(self.get_id(), self.get_nome_servico()))