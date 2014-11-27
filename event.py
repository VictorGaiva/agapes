#!/usr/bin/python
# -*- encoding: utf-8 -*-
from sys import stdout

class EventHandler(object):
    """
    Objeto responsável pela execução e alteração de
    manipuladores de evento.
    """
    
    def __init__(self, handls):
        """
        Cria uma nova instância do objeto.
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
                
    def trigger(self, *args, **kwargs):
        """
        Executa os manipuladores do evento.
        @param list args Argumentos dos manipuladores.
        @param dict kwargs Argumentos nomeados dos manipuladores.
        """
        for handl in self.handlers:
            handl(*args, **kwargs)

class Event(object):
    """
    Objeto responsável pelo controle, administração e
    armazenamento de eventos durante toda a execução do programa.
    """
    list = {}
    
    class __metaclass__(type):
        """
        Metaclasse de Event. Facilita a utilização da classe
        de eventos, disponibilizando métodos mágicos estaticamente.
        """
        
        def __getattr__(cls, name):
            """
            Invoca um evento através da chamada de seu manipulador.
            @param str name Nome do evento invocado.
            """
            if name in cls.list:
                return cls.list[name]
            else:
                msg = str(name) + " event triggered!\n"
                return EventHandler(lambda *l, **k: stdout.write(msg))
        
        def __setattr__(cls, name, value):
            """
            Permite adicionar novos eventos e suas manipulações à
            lista para serem escutados e executados.
            @param str name Nome do evento a ser escutado.
            @param list|callable value Funções a serem executadas pelo evento.
            """
            cls.list[name] = EventHandler(value)
            
        def __delattr__(cls, name):
            """
            Remove manipuladores de um evento. Após a chamada desse
            método, o evento será totalmente destruído.
            @param str name Nome do evento a ser destruído.
            """
            del cls.list[name]