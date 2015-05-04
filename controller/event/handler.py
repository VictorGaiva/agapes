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

class Handler(object):
    """
    Objeto responsável pela execução de manipuladores
    de um evento.
    """

    def __init__(self, callback):
        """
        Cria uma nova instância do objeto.
        :param callback Função de reação ao evento disparado.
        """
        self._callback = callback

    def execute(self, *args, **kwargs):
        """
        Executa o callback do evento.
        :param args Argumentos do manipulador.
        :param kwargs Argumentos nomeados do manipulador.
        """
        return self._callback(*args, **kwargs)

class Empty(Handler):
    """
    Objeto responsável pela execução de manipuladores
    de um evento vazio ou inexistente.
    """

    def __init__(self, ename, obj = None):
        """
        Cria uma nova instância de manipulador vazio de evento.
        :param ename Nome do evento vazio.
        :param obj Objeto alvo do evento.
        """
        Handler.__init__(self, self.nothing)
        self._ename = ename
        self._obj = obj

    def nothing(self, *args, **kwargs):
        """
        Função responsável por mostrar mensagem de não
        existência de evento.
        """
        print "Event '{0}' posted @ {1}!".format(self._ename, self._obj or "global")