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
from .list import List
from wx import PyEventBinder

class Post(object):
    """
    Objeto responsável pela invocação de um evento,
    permitindo assim gerar um evento sobre um objeto
    manualmente.
    """

    def __init__(self, ename, obj = None):
        """
        Cria uma nova instância do objeto.
        :param ename Nome do evento a ser gerado.
        :param obj Objeto alvo do evento.
        """
        self._ename = ename
        self._obj = obj

    def send(self, *args, **kwargs):
        """
        Invoca o evento inicializado passando
        argumentos para seu callback.
        :param args Argumentos do manipulador.
        :param kwargs Argumentos nomeados do manipulador.
        :return mixed
        """
        return List.get(self._ename, self._obj).execute(*args, **kwargs)    \
            if not isinstance(self._ename, PyEventBinder)                   \
            else self._obj.GetEventHandler().ProcessEvent(self._ename)
