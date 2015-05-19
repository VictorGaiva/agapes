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
from ..image import Image
from ..util import Point
from ..grid import Element
import cv2 as cv

class Patch(Image, Element):
    """
    Representação de um retalho de imagem. Administra
    e pode modificar um pedaço de uma imagem.
    """

    def __init__(self, pwork, elem, pos, psize):
        """
        Inicializa uma nova instância do objeto.
        :param pwork Colcha de retalhos que contém esse retalho.
        :param elem Posição do elemento no gradeado.
        :param pos Posição do retalho sobre a imagem.
        :param psize Tamanho do retalho sobre a imagem.
        :return Patch
        """
        Element.__init__(self, pwork, elem)
        Image.__init__(self, pwork.region(pos, psize).raw)

        self.psize = Point(*psize)

    @property
    def fill(self):
        """
        Calcula a área não-vazia do retalho em relação ao
        tamanho que o retalho deveria ter.
        :return float
        """
        imgb = self.binarize(thresh = 25).raw
        value = cv.countNonZero(imgb)

        return value / float(self.psize.x * self.psize.y)

    def border(self):
        """
        Calcula os pontos extremos do retalho. Os pontos
        calculados formam um quadrado perfeito, cujas
        bordas correspondem aos limites do retalho.
        :return list
        """
        tl = self.psize * self.pos
        br = tl + self.shape

        return tl, br

    def sew(self, image):
        """
        Costura uma imagem na região coberta pelo retalho.
        A imagem a ser costurada precisa possuir as mesmas
        dimensões do retalho.
        :param image Imagem a ser costurada.
        """
        self.raw[:,:] = image.raw[:,:]
