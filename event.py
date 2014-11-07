#!/usr/bin/python
# -*- encoding: utf-8 -*-
class EventHandler(object):
    """
    Objeto respons�vel pela execu��o e altera��o de
    manipuladores de evento.
    """
    
    def __init__(self, handls):
        """
        Cria uma nova inst�ncia do objeto.
        @param list|callable handls Manipulador de evento.
        """
        self.handlers = handls if type(handls) is list else [handls]
        
    def __iadd__(self, handls):
        """
        Adiciona manipuladores ao evento.
        @param list|callable handls Manipuladores a serem adicionados.
        """
        for handl in (handls if type(handls) is list else [handls]):
            self.handlers.append(handl)
            
    def __isub__(self, handls):
        """
        Remove manipuladores ao evento.
        @param list|callable handls Manipuladores a serem removidos.
        """
        for handl in (handls if type(handls) is list else [handls]):
            if handl in self.handlers:
                self.handlers.remove(handl)
                
    def __call__(self, *args, **kwargs):    
        """
        Executa os manipuladores do evento.
        @param list args Argumentos dos manipuladores.
        @param dict kwargs Argumentos nomeados dos manipuladores.
        """
        for handl in self.handlers:
            handl(*args, **kwargs)

class Event(object):
    """
    Objeto respons�vel pelo controle, administra��o e
    armazenamento de eventos durante toda a execu��o do programa.
    """
    list = {}
    
    class __metaclass__(type):
        """
        Metaclasse de Event. Facilita a utiliza��o da classe
        de eventos, disponibilizando m�todos m�gicos estaticamente.
        """
        
        def __getattr__(cls, name):
            """
            Invoca um evento atrav�s da chamada de seu manipulador.
            @param str name Nome do evento invocado.
            """
            if name in cls.list:
                return cls.list[name]
            else:
                return EventHandler(lambda *l, **k: None)
        
        def __setattr__(cls, name, value):
            """
            Permite adicionar novos eventos e suas manipula��es �
            lista para serem escutados e executados.
            @param str name Nome do evento a ser escutado.
            @param list|callable value Fun��es a serem executadas pelo evento.
            """
            cls.list[name] = EventHandler(value)
            
        def __delattr__(cls, name):
            """
            Remove manipuladores de um evento. Ap�s a chamada desse
            m�todo, o evento ser� totalmente destru�do.
            @param str name Nome do evento a ser destru�do.
            """
            del cls.list[name]