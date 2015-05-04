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
import random

import cv2 as cv

from .util.point import Point
from .image import Image


#TODO: Utilizar como base um grafo, onde cada vértice é um retalho.
#TODO: Utilizar esse grafo para facilitar a interação e navegação entre os retalhos.
#TODO: Fazer um sistema de camadas em cada retalho. Onde cada camada é um passo do algoritmo.

class Patch(object):
    """
    Objeto responsável por representar uma porção da imagem,
    chamada de retalho.
    """

    def __init__(self, pwork, x, y):
        """
        Inicializa e cria uma nova instância do objeto.
        :param pwork Referência à imagem original.
        :param x Coordenada esquerda do retalho.
        :param y Coordenada superior do retalho.
        """
        self.pos = Point(x, y)
        self.size = pwork.psize
        self.pwork = pwork

    @property
    def image(self):
        """
        Retorna a porção de imagem referente ao retalho atual.
        :return Image
        """
        return self.pwork.region(self.pos, self.size)

    def sew(self, image):
        """
        Costura uma imagem na região do retalho atual. A imagem
        a ser costurada precisa possuir as mesma dimensões do
        retalho.
        :param image Imagem a ser costurada.
        """
        self.pwork.glue(self, image)

class PatchList(object):
    """
    Objeto responsável por armazenar uma lista de retalhos.
    """

    def __init__(self, patches):
        """
        Inicializa e cria uma nova instância do objeto.
        :param patches Lista de Patches criados.
        """
        self.patches = patches
        self.count = len(patches)

    def __getitem__(self, index):
        """
        Retorna um item da lista de patches.
        :param index Índice a ser retornado.
        :return Patch
        """
        return self.patches[index]

    def choose(self, rate = 1):
        """
        Escolhe alguns patches aleatoriamente.
        :param rate Porcentagem de patches a serem escolhidos.
        :return PatchList, PatchList
        """
        yes = random.sample(self.patches, int(self.count * rate))
        no  = filter(lambda p: p not in yes, self.patches)

        return PatchList(yes), PatchList(no)

class PatchWork(Image, PatchList):
    """
    Objeto responsável por trabalhar com uma imagem
    assemelhando-a a uma colcha de retalhos, com vários
    recortes de tamanhos iguais.
    """

    def __init__(self, image, width, height):
        """
        Inicializa e cria uma nova instância do objeto.
        :param image Imagem de fundo para os retalhos.
        :param width Largura dos retalhos.
        :param height Altura dos retalhos.
        :return PatchWork
        """
        Image.__init__(self, image.raw, image.inverted)
        PatchList.__init__(self, [])

        self.psize = Point(width, height)
        self.limit = width * height * 0.5

    def glue(self, patch, image):
        """
        Cola uma imagem sobre a região indicada.
        :param patch Retalho de clipagem.
        :param image Imagem a ser colada.
        """
        self[
            patch.pos.x : patch.pos.x + patch.size.x,
            patch.pos.y : patch.pos.y + patch.size.y
        ] = image.raw

    def transpose(self):
        """
        Inverte o PatchWork atual. Assim, as dimensões se inventem
        e é necessário inverter as coordenadas de um ponto para
        resgatar um mesmo pixel da imagem anterior.
        :return PatchWork transposto.
        """
        return PatchWork(
            Image.transpose(self),
            *self.psize.swap
        )

    def chop(self):
        """
        Recorta a imagem e encontra todos os retalhos que
        são bons o suficiente para serem processados.
        :return PatchList
        """
        self.patches.extend([
            Patch(self, x, y) for x in xrange(0, self.shape.x, self.psize.x)
                for y in xrange(0, self.shape.y, self.psize.y)
                    if self.pixels(x, y) >= self.limit
        ])

        self.count = len(self.patches)
        return self

    def pixels(self, x, y):
        """
        Verifica a quantidade de pixels não-pretos presentes
        no retalho cujo canto superor direito é dado.
        :param x Canto esquerdo do retalho.
        :param y Canto superior do retalho.
        :return int Contagem de pixels não-pretos.
        """
        return reduce(
            lambda _x, _y: _x + _y,
            cv.reduce(
                self.region((x,y), self.psize).binarize().raw,
                0, cv.cv.CV_REDUCE_SUM, dtype = cv.CV_32S
            )[0]
        )
