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
from .element import Element
from ..util import Point

__all__ = [
    "Grid", "Element"
]

class Grid(object):
    """
    Representação de uma grade de objetos responsável
    por armazenar e gerir as interações entre os elementos
    do gradeado.
    """

    def __init__(self, rows = 0, cols = 0):
        """
        Inicializa uma nova instância.
        :param rows Quantidade de linhas iniciais.
        :param cols Quantidade de colunas iniciais.
        :return Grid
        """
        rows, cols = int(rows), int(cols)

        self.count = Point(rows, cols)
        self.data = [[None for i in xrange(cols + 1)] for j in xrange(rows + 1)]

    @property
    def total(self):
        """
        Contagem total de elementos presentes no gradeado.
        :return int
        """
        return sum(e is not None for r in self.data for e in r)

    def __setitem__(self, index, value):
        """
        Insere um objeto a uma posição do gradeado.
        :param index Índice ao qual o elemento deve ser inserido.
        :param value Objeto a ser inserido.
        """
        elem = Element(self, index, value)
        self.data[index[0]][index[1]] = elem

    def access(self, index):
        """
        Acessa um elemento referenciado no gradeado.
        :param index Índice do elemento a ser acessado.
        :return mixed
        """
        return self.data[index[0]][index[1]]

    def insert(self, index, value):
        """
        Adiciona um elemento ao gradeado.
        :param index Índice ao qual o elemento deve ser adicionado.
        :param value Objeto a ser adicionado.
        """
        self.data[index[0]][index[1]] = value

    def remove(self, index):
        """
        Remove um elemento do gradeado.
        :param index Índice do elemento a ser removido.
        """
        self.data[index[0]][index[1]] = None

    def filter(self, function):
        """
        Mantém ao gradeado apenas os elementos que
        satisfizerem a condição dada pela função.
        :param function Função de filtragem.
        :return list
        """
        okay = []

        for i in xrange(self.count.x):
            for j in xrange(self.count.y):
                if not function(self.data[i][j]):
                    self.remove((i, j))
                else:
                    okay.append(self.data[i][j])

        return okay