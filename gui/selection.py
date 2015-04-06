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
from .event import PostEvent

class Selection(object):
    """
    Objeto responsável pela representação e controle de
    seleção de retalhos.
    """

    def __init__(self, page):

        """
        Cria uma nova instância do objeto.
        :return Selection
        """
        self._elems = []
        self._count = 0
        self._active = False

        self.page = page

    def add(self, elem):
        """
        Adiona um elemento à seleção.
        :param elem Elemento a ser adicionado.
        """
        self._elems.append(elem)
        self._count = self._count + 1
        self._active = True
        PostEvent("SelectionAdd", self)

    def remove(self, elem):
        """
        Remove um elemento da seleção.
        :param elem Elemento a ser removido.
        """
        if elem in self._elems:
            self._elems.remove(elem)
            self._count = self._count - 1
            self._active = self._count > 0
            PostEvent("SelectionRemove", self)

    def toggle(self, elem):
        """
        Adiciona ou remove um elemento da seleção.
        :param elem Elemento alvo.
        :return bool Foi adicionado?
        """
        if elem in self._elems:
            self.remove(elem)
            return False

        else:
            self.add(elem)
            return True

    def clean(self):
        """
        Remove todos os elementos da seleção.
        """
        PostEvent("SelectionClean", self)

        self._elems = []
        self._count = 0
        self._active = False