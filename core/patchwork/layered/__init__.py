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
from core.grid import Grid
from core.util import Point
from core.image.list import List
from .patch import LayeredPatch
from .. import PatchWork
from math import ceil

__all__ = [
    "LayeredPatchWork", "LayeredPatch"
]

class LayeredPatchWork(List, Grid):
    """
    Colcha de retalhos em camadas. Adiministra várias
    colchas de retalhos de uma única vez. Para o correto
    funcionamento, todas as colchas de retalhos devem
    possuir o mesmo tamanho.
    """

    def __init__(self, psize, *image):
        """
        Inicializa uma nova instância do objeto.
        :param psize Tamanho dos retalhos.
        :param image Imagens a serem recortadas e manipuladas por retalhos.
        :return PatchWork
        """
        fpsz = float(psize[0]), float(psize[1])

        List.__init__(self, *image)
        Grid.__init__(self, ceil(self.shape.x / fpsz[0]), ceil(self.shape.y / fpsz[1]))

        self.psize = Point(*psize)

    __getitem__ = List.__getitem__
    __setitem__ = List.__setitem__

    insert = Grid.insert
    remove = Grid.remove

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
                self.insert((i,j), LayeredPatch(self, (i,j), (x,y), self.psize))

        self.filter(lambda p: p.fill > least)

    def show(self, wname = "image"):
        """
        Mostra a imagem armazenada pelo objeto.
        :return Window
        """
        from core.image.window import Window
        from core.spectator.layered import LayeredSpectator

        win = Window(self, wname, spec = LayeredSpectator)
        win.show()

        return win
