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
from core.image import Image
import cv2 as cv

class Spectator(Image):
    """
    Manipula uma imagem e a prepara para a exibição em um
    painel com dimensões diferentes da imagem e com
    ferramentas de visualização de imagem.
    """

    class Marker(object):
        """
        Marcador de estado do campo de visão. É utilizado
        como ponto base para as manipulações do campo de
        visão e como histórico que pode ser restaurado.
        """

        def __init__(self, observer):
            """
            Inicializa e cria uma nova instância do objeto.
            :param observer Instância a ser salva.
            """
            self.obj = observer

            self.total = Point(*observer.total)
            self.lt = Point(*observer.lt)
            self.rb = Point(*observer.rb)

        def restore(self):
            """
            Restaura o estado salvo ao observador. Dessa
            forma, o observador volta à configuração anterior.
            """
            self.obj.total = self.total
            self.obj.lt = self.lt
            self.obj.rb = self.rb

    def __init__(self, image, shape = (800, 600)):
        """
        Inicializa e cria uma nova instância do objeto.
        :param image Imagem a ser exibida.
        :param shape Formato do campo de visão para a imagem.
        :return Spectator
        """
        self.shape = Point(*shape)
        self.actual = self.im = image

        self.total = self.im.shape
        self.lt = (self.total - self.shape) // 2
        self.rb = (self.total + self.shape) // 2

    @property
    def raw(self):
        """
        Imagem visível na região de interesse selecionada
        atualmente.
        :return Image
        """
        f0 = lambda i: max(i, 0)

        l, t = map(f0, -self.lt)
        r, b = map(f0, self.rb - self.total)

        l, r = (self.shape.x, 0) if (l + r) > self.shape.x else (l, r)
        t, b = (self.shape.y, 0) if (t + b) > self.shape.y else (t, b)

        raw = self.actual.rect(map(f0, self.lt), map(f0, self.rb)).raw
        return cv.copyMakeBorder(raw, t, b, l, r, cv.BORDER_CONSTANT, value = 0)

    def imgpos(self, px, py):
        """
        Calcula a correspondência de um ponto no campo
        de visão com um ponto na imagem. Em outras palavras,
        transforma um ponto das coordenadas da janela para
        as coordenadas equivalentes da imagem.
        :param px Posição no eixo-x da janela.
        :param py Posição no eixo-y da janela.
        :return Point
        """
        return self.lt + (px, py)

    def mark(self):
        """
        Cria um ponto de marcação de estado do observador.
        Utilizado para as transformações de movimentação e
        zoom no campo de visão.
        """
        return self.Marker(self)

    def move(self, mark, dx, dy):
        """
        Movimenta o campo de visão sobre a imagem.
        :param mark Estado de início do movimento.
        :param dx Deslocamento no eixo-x.
        :param dy Deslocamento no eixo-y.
        """
        self.lt = mark.lt + (dx, dy)
        self.rb = mark.rb + (dx, dy)

    def zoom(self, mark, value):
        """
        Aplica zoom à imagem sobre o campo de visão.
        :param mark Estado de início do movimento.
        :param value Quantidade de zoom a ser aplicado.
        """
        limits = (self.im.shape.x / 10, self.im.shape.x * 5)
        before = mark.total

        value = min(max(50, limits[0], before.x + value), limits[1])

        self.actual = self.im.resize(0, (value, 50))
        self.total = self.actual.shape

        diff = self.total - before
        self.lt = mark.lt + diff // 2
        self.rb = mark.rb + diff // 2

    def update(self):
        """
        Atualiza a imagem observada. Mostra as alterações
        realizadas na imagem alvo de observação.
        """
        self.actual = self.im.resize(0, self.total)
