class Agendamento:
    __slots__ = ['__id_agendamento', '__cliente', '__servico', '__id_agenda']

    def __init__(self, p_id_agendamento=False, p_cliente=False, p_servico=False, p_id_agenda=False):
        self.__id_agendamento = p_id_agendamento
        self.__cliente = p_cliente
        self.__servico = p_servico
        self.__id_agenda = p_id_agenda

    def get_id_agendamento(self):
        return self.__id_agendamento

    def get_cliente(self):
        return self.__cliente

    def get_servico(self):
        return self.__servico

    def get_id_agenda(self):
        return self.__id_agenda

    def set_id_agendamento(self, valor):
        self.__id_agendamento = valor

    def set_cliente(self, valor):
        self.__cliente = valor

    def set_servico(self, valor):
        self.__servico = valor

    def set_id_agenda(self, valor):
        self.__id_agenda = valor

    def __str__(self):
        return(f"Agendamento ==> id: {self.get_id_agendamento()} \n Cliente: {self.get_cliente().get_nome()}  \n Serviço:  {self.get_servico().get_nome_servico()} \n Agenda ID: {self.get_id_agenda()}")        
