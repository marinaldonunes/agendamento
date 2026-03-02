""" Classe que representa os itens que podem ser agendados"""


class Agenda:
    __slot__ = ['__profissional', '__dia', '__hora']

    def __init__(self, p_profissional=False, p_dia=False, p_hora=False):
        self.__profissional = p_profissional
        self.__dia = p_dia
        self.__hora = p_hora

    def get_dia(self):
        return self.__dia

    def get_hora(self):
        return self.__hora

    def get_profissional(self):
        return self.__profissional

    def set_dia(self, p_dia):
        self.__dia = p_dia

    def set_hora(self, p_hora):
        self.__hora = p_hora

    def set_profissional(self, valor):
        self.__profissional = valor

    def __str__(self):
        return(f"Agenda ==> id: {self.get_id()} - Profissional: {self.get_profissional}/ Dia/Hora:{self.get_dia}:{self.get_hora}")