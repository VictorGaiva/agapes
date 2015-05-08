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
from ..util import Point

class Element(object):
    """
    Representação de uma célula de uma tabela ou um
    sistema de grade.
    """
    __slots__ = 'grid', 'pos', 'data'

    def __init__(self, grid, pos, data = None):
        """
        Inicializa uma nova instância de objeto.
        :param grid Gradeado a qual o elemento pertence.
        :param pos Posição do elemento no gradeado.
        :param data Dado que deve ser armazenado no elemento.
        :return Element
        """
        self.grid = grid
        self.data = data
        self.pos = Point(*pos)

    @property
    def up(self):
        """
        Elemento localizado acima no gradeado.
        :return Element
        """
        return self.grid.access(self.pos - (1, 0))

    @property
    def down(self):
        """
        Elemento localizado abaixo no gradeado.
        :return Element
        """
        return self.grid.access(self.pos + (1, 0))

    @property
    def left(self):
        """
        Elemento localizado à esquerda no gradeado.
        :return Element
        """
        return self.grid.access(self.pos - (0, 1))

    @property
    def right(self):
        """
        Elemento localizado à direita no gradeado.
        :return Element
        """
        return self.grid.access(self.pos + (0, 1))
