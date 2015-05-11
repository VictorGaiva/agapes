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
from core.image import Image
from .grid import GridSpectator
import cv2 as cv

class SelectionSpectator(GridSpectator):
    """
    Manipula uma imagem gradeada e permite selecionar
    regiões da imagem. As regiões selecionadas sempre
    corresponderão às celulas do gradeado.
    """

    def __init__(self, image, cellsize, shape = (800, 600), color = (0,0,255)):
        """
        Inicializa e cria uma nova instância do objeto.
        :param image Image a ser exibida.
        :param cellsize Tamanho de cada célula da grade.
        :param shape Formato do campo de visão para a imagem.
        :param color Cor a ser utilizada para a seleção.
        :return LayeredSpectator
        """
        GridSpectator.__init__(self, image, cellsize, shape)
        self.color = color

        self.selection = []

    def __len__(self):
        """
        Contabiliza a quantidade de elementos selecionados.
        :return int
        """
        return len(self.selection)

    def update(self):
        """
        Atualiza a imagem observada. Mostra as alterações
        realizadas na imagem alvo de observação.
        """
        super(SelectionSpectator, self).update()
        self.drawselection() if self.selection else None

    def select(self, px, py):
        """
        Adiciona uma elemento à seleção.
        :param px Posição no eixo-x da janela.
        :param py Posição no eixo-y da janela.
        """
        pixel = self.imgpos(px, py)
        pos = pixel // self.cellsize

        try:
            elem = self.im.access(pos)
            self.toggle(elem) if elem else None

        except:
            return

    def deselect(self):
        """
        Desseleciona os elementos que haviam sido selecionados,
        tornando a lista de elementos selecionados vazia.
        """
        self.selection = []

    def toggle(self, elem):
        """
        Alterna um elemento à seleção. Isto é, caso o elemento
        já esteja na seleção, ele é retirado. De forma
        antagônica, caso o elemento não esteja na seleção ele
        é adicionado.
        :param elem Elemento a ser alternado.
        """
        rem = elem in self.selection
        self.selection.remove(elem) if rem else self.selection.append(elem)

    def drawselection(self):
        """
        Desenha a seleção de elementos sobre a
        imagem sendo exibida.
        """
        for elem in self.selection:
            tl, br = elem.border()

            p0 = (tl * self.rel[0])(round)(int) + (10,10)
            p1 = (br * self.rel[0])(round)(int) - (10,10)

            cv.rectangle(self.actual.raw, p0, p1, self.color, 3)
