class Agendamento:
    __slots__ = ['__id', '__cliente', '__servico', '__agenda']

    def __init__(self, p_id=False, p_cliente=False, p_servico=False, p_agenda=False):
        self.__id = p_id
        self.__cliente = p_cliente
        self.__servico = p_servico
        self.__agenda = p_agenda

    def get_id(self):
        return self.__id

    def get_cliente(self):
        return self.__cliente

    def get_servico(self):
        return self.__servico

    def get_agenda(self):
        return self.__agenda

    def set_id(self, valor):
        self.__id = valor

    def set_cliente(self, valor):
        self.__cliente = valor

    def set_servico(self, valor):
        self.__servico = valor

    def set_agenda(self, valor):
        self.__agenda = valor

    def __str__(self):
        return(f"Agendamento ==> id: {self.get_id()} \n Cliente: {self.get_cliente().get_nome()}  \n Serviço:  {self.get_servico().get_nome_servico()} \n Profissional: {self.get_agenda().get_profissional().get_nome()}  \n Dia:Hora:{self.get_agenda().get_dia()}:{self.get_agenda().get_hora()}")        
