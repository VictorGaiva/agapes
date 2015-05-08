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
from core.util import Point
from . import Image

class List(Image, list):
    """
    Armazena uma lista de imagens que podem assumir
    um mesmo espaço ou campo numa interface gráfica.
    """

    def __init__(self, *source):
        """
        Inicializa e cria uma nova instância do objeto.
        :param source Primeiras imagens a serem adicionadas.
        :return List
        """
        list.__init__(self, source)

        self.i = self.length - 1
        self.actual = self[self.i] if self.length > 0 else Image.new((100,100))

    @property
    def length(self):
        """
        Calcula a quantidade de imagens armazenadas
        na lista.
        :return int
        """
        return len(self)

    @property
    def shape(self):
        """
        Calcula o formato da imagem atualmente
        selecionada na lista.
        :return Point
        """
        return self.actual.shape

    @property
    def raw(self):
        """
        Facilita o acesso ao formato cru da imagem
        atualmente selecionada na lista.
        :return numpy.ndarray
        """
        return self.actual.raw

    def add(self, source):
        """
        Adiciona uma nova imagem existente à lista.
        :param source Nova imagem a ser adicionada.
        """
        self.append(source)
        self.select(self.length - 1)

    def select(self, index):
        """
        Modifica a imagem em foco atual.
        :param index Índice da imagem a ser focalizada.
        :return Image
        """
        self.i = index
        self.actual = self[self.i]
