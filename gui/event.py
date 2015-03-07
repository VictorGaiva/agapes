#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
PSG - Tecnologia Aplicada

Este é um módulo utilizado para contagem de falhas em
plantações de cana-de-açúcar através do uso de imagens
aéreas capturadas por VANT's ou aparelhos similares.

Este arquivo é responsável pelo desenho da interface do
programa e também pela execução e apresentação dos
resultados obtidos com a imagem fornecida.
"""

class EventHandler(object):
    """
    Objeto responsável pela execução e alteração de
    manipuladores de evento.
    """
    
    def __init__(self, handls):
        """
        Cria uma nova instância do objeto.
        :param handls Manipulador de evento.
        """
        self.handlers = handls if type(handls) is list else [handls]

    def add(self, handls):
        """
        Adiciona manipuladores ao evento.
        :param handls Manipuladores a serem adicionados.
        """
        for handl in (handls if type(handls) is list else [handls]):
            self.handlers.append(handl)

    def remove(self, handls):
        """
        Remove manipuladores ao evento.
        :param handls Manipuladores a serem removidos.
        """
        for handl in (handls if type(handls) is list else [handls]):
            if handl in self.handlers:
                self.handlers.remove(handl)

    def trigger(self, *args, **kwargs):
        """
        Executa os manipuladores do evento.
        :param args Argumentos dos manipuladores.
        :param kwargs Argumentos nomeados dos manipuladores.
        """
        for handl in self.handlers:
            handl(*args, **kwargs)

class EmptyHandler(EventHandler):
    """
    Objeto responsável pela execução de manipuladores
    de eventos vazios ou inexistentes.
    """

    def __init__(self, name):
        """
        Cria uma nova instância do objeto.
        :param name Nome do evento vazio chamado.
        """
        self.name = name

    def add(self, handls):
        """
        Ignora adição de manipuladores ao evento.
        :param handls Manipuladores a serem adicionados.
        """
        pass

    def remove(self, handls):
        """
        Ignora a remoção de manipuladores ao evento.
        :param handls Manipuladores a serem removidos.
        """
        pass

    def trigger(self, *args, **kwargs):
        """
        Ignora execução de manipuladores do evento.
        :param args Argumentos dos manipuladores.
        :param kwargs Argumentos nomeados dos manipuladores.
        """
        print "Unknown `" + self.name + "` event triggered!"

class EventBinder(object):
    """
    Objeto responsável por registrar novos eventos a partir do
    uso de decoradores, para facilitar a criação de eventos.
    """

    def __init__(self, name):
        """
        Cria uma nova instância do objeto.
        :param name Nome do evento a ser escutado.
        """
        self.name = name

    def __call__(self, function):
        """
        Vincula um método a ser executado em reação ao evento.
        :param function Função a ser anexada.
        :return Método inalterado porém estático.
        """
        Event.listen(self.name, function)
        return function

class Event(object):
    """
    Objeto responsável pelo controle, administração e
    armazenamento de eventos durante toda a execução do programa.
    """
    list = {}

    @classmethod
    def listen(cls, ename, function):
        """
        Cria um manipulador de eventos de acordo com o nome dado.
        :param ename Nome do evento a ser criado.
        :param function Funções a serem executadas quando durante o evento.
        :return EventHandler
        """
        cls.list[ename] = EventHandler(function)

    @classmethod
    def get(cls, ename):
        """
        Recupera um evento através do nome de seu manipulador.
        :param ename Nome do evento a ser recuperado.
        :return EventHandler
        """
        if ename in cls.list:
            return cls.list[ename]

        else:
            return EmptyHandler(ename)

    @classmethod
    def delete(cls, ename):
        """
        Remove manipuladores de um evento. Após a chamada desse
        método, o evento será totalmente destruído.
        :param ename Nome do evento a ser destruído.
        """
        del cls.list[ename]

def BindEvent(ename, function):
    """
    Vincula novos eventos personalizados com suas
    respectivas funções.
    :param ename Nome do evento a ser vínculado.
    :param function Método ou função a ser vínculada.
    :return None
    """
    Event.listen(ename, function)

def LinkEvent(obj, event, ename, args = ()):
    """
    Liga um evento built-in disparado em um objeto a um
    evento tratado por esse módulo.
    :param obj Objeto alvo do evento.
    :param event Evento disparado no objeto.
    :param ename Nome do evento a ser vinculado.
    :param args Parâmetros de contexto.
    """
    obj.Bind(event, lambda *arg: PostEvent(ename, *(args + arg)))

def PostEvent(ename, *args, **kwargs):
    """
    Dispara e executa um evento, passando os parâmetros
    fornecidos.
    :param ename Nome do evento a ser disparado.
    :param args Argumentos de posição.
    :param kwargs Argumentos nominais.
    :return mixed
    """
    return Event.get(ename).trigger(*args, **kwargs)