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
from core.image.list import List
from core.grid import Element
from core.util import Point
from ..patch import Patch

class LayeredPatch(Patch, List, Element):
    """
    Representação de um retalho de imagem em camadas.
    Administra e pode modificar um pedaço de uma lista
    de imagens.
    """

    def __init__(self, lpwork, elem, pos, psize):
        """
        Inicializa uma nova instância do objeto.
        :param lpwork Colcha de retalhos em camadas que contém esse retalho.
        :param elem Posição do elemento no gradeado.
        :param pos Posição do retalho sobre a imagem.
        :param psize Tamanho do retalho sobre a imagem.
        :return Patch
        """
        List.__init__(self, *[Patch(im, elem, pos, psize) for im in lpwork])
        Element.__init__(self, lpwork, elem)

        self.psize = Point(*psize)

    __getitem__ = List.__getitem__
    __setitem__ = List.__setitem__

    def sew(self, image, start = None, end = None):
        """
        Costura uma imagem às regiões cobertas pelo retalhos
        selecionados. A imagem a ser costurada precisa possuir
        as mesmas dimensões dos retalhos.
        :param start Índice inicial para costurar.
        :param end Índice final
        :param image Imagem a ser costurada.
        :return:
        """
        for patch in self[start:end]:
            patch.sew(image)