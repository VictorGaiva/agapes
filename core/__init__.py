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
from .segmentator import *
from .component import *
from .image import *
from .line import *

__all__ = [
    "LoadImage",
    "SegmentImage",
    "ProcessImage",
    "SaveImage",
    "image"
]

def LoadImage(address):
    """
    Carrega uma imagem.
    :param address Endereço da imagem a ser carregada.
    :return Image Imagem carregada.
    """
    image = Image.load(address)
    image = image.resize(.3, min = Point(1200, 900))

    return image

def SegmentImage(img):
    """
    Executa a segmentação da imagem.
    :param img Imagem a ser segmentada.
    :return Image, ComponentList, Map Lista de componentes.
    """
    sgmtr = Segmentator.train()
    img = sgmtr.apply(img)

    comps, cmap = ComponentList.load(img)
    return img, comps, cmap

def ProcessImage(img, cmap, distance):
    """
    Processa a imagem e procura por linhas de plantação
    de cana-de-açúcar; e desenha sobre a imagem as linhas
    encontradas.
    :param img Imagem alvo do processo.
    :param cmap Mapa de componentes da imagem.
    :param distance Distância entre linhas da plantação.
    :return Image, float, float Porcentagem e metragem de falhas.
    """
    lines = LineList.first(cmap, cmap.comp[1])
    lines.complete()

    img = lines.display(img.inverted)
    pcent, meter = lines.error(distance)

    return img, lines, pcent, meter

def SaveImage(original, image):
    """
    Salva a imagem resultante.
    :param original Endereço da imagem original.
    :param image Imagem a ser salva.
    """
    name = original.rsplit('.', 1)
    image.save("{0}.processed.{1}".format(*name))
