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

class Bind(object):
    """
    Objeto responsável pela vinculação ou desvinculação
    de um evento com seus respectivos callbacks.
    """

    def __init__(self, ename, obj = None):
        """
        Cria uma nova instância do objeto.
        :param ename Nome do evento a ser vinculado.
        :param obj Objeto sobre o qual o evento atua.
        """
        self._ename = ename
        self._obj = obj

    def __call__(self, callback):
        """
        Vincula o callback ao evento inicializado.
        É preferível que o uso desse método restrinja-se
        ao uso como decorator.
        :param callback Função de callback a ser vinculada.
        :return function
        """
        List.set(self._ename, self._obj, callback)
        return callback

    def set(self, callback, args, kwargs):
        """
        Vincula o callback ao evento inicializado.
        :param callback Função de callback a ser vinculada.
        :param args Argumentos do manipulador.
        :param kwargs Argumentos nomeados do manipulador.
        """
        obj = (self._obj,)                                  \
            if self._obj is not None                        \
            else ( )

        def _function(*pos, **name):
            kwargs.update(name)
            return callback(*obj + args + pos, **kwargs)

        List.set(self._ename, self._obj, _function)         \
            if not isinstance(self._ename, PyEventBinder)   \
            else self._obj.Bind(self._ename, _function)

    def unset(self):
        """
        Remove o callback vinculado ao evento inicializado.
        :return None
        """
        List.unset(self._ename, self._obj)                  \
            if not isinstance(self._ename, PyEventBinder)   \
            else self._obj.Unbind(self._ename)
