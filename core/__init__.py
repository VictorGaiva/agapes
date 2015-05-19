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
from .segmentator import Segmentator
from .component import ComponentList
from .image import Image
from .line import LineList

__all__ = [
    "LoadImage",
    "SegmentImage",
    "ProcessImage",
    "SaveImage",
]

def LoadImage(data):
    """
    Carrega uma imagem.
    :param data Dados de execução.
    :return Image Imagem carregada.
    """
    image = Image.load(data.address)
    return dict(image = image)

def SegmentImage(data):
    """
    Executa a segmentação da imagem.
    :param data Dados de execução.
    :return Image, Map Lista de componentes.
    """
    try:
        seg = Segmentator.train(train = data.train)
    except:
        seg = Segmentator.train()
    image = seg.apply(data.patch)
    comp, compmap, inverted = ComponentList.load(image)

    return dict(image = image, compmap = compmap, inverted = inverted)

def ProcessImage(data):
    """
    Processa a imagem e procura por linhas de plantação
    de cana-de-açúcar; e desenha sobre a imagem as linhas
    encontradas.
    :param data Dados de execução.
    :return Image, float, float Porcentagem e metragem de falhas.
    """
    lines = LineList.first(data.compmap, data.compmap.comp[1])
    lines.complete()

    pct, mtrs, image = lines.error(data.distance, data.compmap.inverted)

    return dict(image = image, percent = pct, meters = mtrs)

def SaveImage(original, image):
    """
    Salva a imagem resultante.
    :param original Endereço da imagem original.
    :param image Imagem a ser salva.
    """
    name = original.rsplit('.', 1)
    image.save("{0}.processed.{1}".format(*name))
