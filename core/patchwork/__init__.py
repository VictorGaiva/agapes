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
from ..grid import Grid
from ..util import Point
from .patch import Patch
from .list import List
from math import ceil

__all__ = [
    "PatchWork", "Patch"
]

class PatchWork(Image, Grid):
    """
    Colcha de retalhos de imagens. Representa a união de
    vários retalhos que trabalham independentemente e, de
    certa forma, unidos para a formação e modificação de uma
    imagem.
    """
    __slots__ = 'raw', 'shape', 'psize'

    def __init__(self, image, psize):
        """
        Inicializa uma nova instância do objeto.
        :param image Imagem a ser recortada e manipulada por retalhos.
        :param psize Tamanho dos retalhos.
        :return PatchWork
        """
        shape = image.shape
        fpsz = float(psize[0]), float(psize[1])

        Grid.__init__(self, ceil(shape.x / fpsz[0]), ceil(shape.y / fpsz[1]))
        Image.__init__(self, image.raw)

        self.psize = Point(*psize)

    __getitem__ = Image.__getitem__
    __setitem__ = Image.__setitem__

    def shred(self, least = 0.5):
        """
        Recorta a imagem, cria todos os retalhos possíveis
        de existirem sobre a imagem e seleciona apenas aqueles
        que estão acima da porcentagem mínima de preenchimento
        do retalho.
        :param least Porcentagem mínima de preenchimento.
        """
        for i, x in enumerate(xrange(0, self.shape.x, self.psize.x)):
            for j, y in enumerate(xrange(0, self.shape.y, self.psize.y)):
                self.insert((i, j), Patch(self, (x,y), self.psize))

        self.filter(lambda p: p.fill > least)
