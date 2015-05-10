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
from . import Spectator
import cv2 as cv

class GridSpectator(Spectator):
    """
    Manipula uma imagem e permite adicionar, sobre ela,
    uma grade com distâncias constantes para ser exibida
    em um campo de exibição com dimensões diferentes
    daquelas da imagem.
    """

    def __init__(self, image, cellsize, shape = (800, 600)):
        """
        Inicializa e cria uma nova instância do objeto.
        :param image Image a ser exibida.
        :param cellsize Tamanho de cada célula da grade.
        :param shape Formato do campo de visão para a imagem.
        :return LayeredSpectator
        """
        Spectator.__init__(self, image, shape)

        self.cellsize = Point(*cellsize)
        self.active = False

    def update(self):
        """
        Atualiza a imagem observada. Mostra as alterações
        realizadas na imagem alvo de observação.
        """
        super(GridSpectator, self).update()
        self.drawgrid() if self.active else None

    def showgrid(self, value):
        """
        Interruptor de desenho de grade.
        :param value A grade deve ser mostrada?
        """
        self.active = value
        self.update()

    def drawgrid(self, color = (0, 255, 0)):
        """
        Desenha a grade de retalhos sobre a imagem.
        :param color Cor das linhas de grade.
        """
        rel = self.actual.shape.x / float(self.im.shape.x)
        rsz = self.cellsize * rel
        img = self.actual

        for x in interpolate(0, img.shape.x, rsz.x):
            cv.line(img.raw, (x, 0), (x, img.shape.y - 1), color, 1)

        for y in interpolate(0, img.shape.y, rsz.y):
            cv.line(img.raw, (0, y), (img.shape.x - 1, y), color, 1)

        last = img.shape - (1,1)
        cv.line(img.raw, (last.x, 0), last, color, 1)
        cv.line(img.raw, (0, last.y), last, color, 1)

def interpolate(start, end, step):
    """
    Calcula pontos num intervalo utilizando-se de
    um interpolação simples para valores quebrados.
    :param start Início do intervalo.
    :param end Fim do intervalo.
    :param step Incremento a cada passo.
    :return int
    """
    while start < end:
        yield int(round(start))
        start = start + step
