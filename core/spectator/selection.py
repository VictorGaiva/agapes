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
from .grid import GridSpectator
import cv2 as cv

#TODO: Aprimorar métodos de escritura de textos sobre o espectador.

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
        self.tcolor = {}
        self.text = {}

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
        self.drawselection()
        self.drawtext()

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
            pass

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

    def settextcolor(self, cell, color):
        """
        Indica a cor que deve ser utilizada no texto de uma célula.
        :param cell Identificador de célula.
        :param color Cor do texto.
        """
        self.tcolor[cell] = color

    def addtext(self, cell, text, color):
        """
        Adiciona um texto a ser desenhado sobre uma célula do
        gradeado quando a célula não está selecionada.
        :param cell Identificador da célula alvo.
        :param text Texto a ser exibido.
        :param color Cor do texto.
        """
        self.text[cell] = text
        self.tcolor[cell] = self.tcolor.get(cell, color)

    def remtext(self, cell, text, color):
        """
        Remove um texto a ser desenhado sobre uma célula do
        gradeado quando a célula não está selecionada.
        :param cell Identificador da célula alvo.
        """
        del self.text[cell]

    def drawselection(self):
        """
        Desenha a seleção de elementos ou os textos adicionados
        sobre a imagem alvo do espectador.
        """
        for elem in self.selection:
            tl, br = elem.border()
            p0 = (tl * self.rel[0])(round)(int) + (5,5)
            p1 = (br * self.rel[0])(round)(int) - (5,5)

            cv.rectangle(self.actual.raw, p0, p1, self.color, 3)

    def drawtext(self):
        """
        Desenha os textos informados sobre os elementos
        indicados anteriormente.
        :return:
        """
        xsize = (self.cellsize * self.rel[0]).x
        fsz = min(.75, (xsize / 80) * .75)

        if xsize < 45:
            return

        for elem, text in self.text.iteritems():
            elem = self.im.access(elem)

            if elem in self.selection:
                continue

            tl, br = elem.border()
            p0 = (tl * self.rel[0])(round)(int)
            p1 = (br * self.rel[0])(round)(int)
            pf = Point(p0.x, p1.y) + (10, -10)

            color = self.tcolor[elem.pos]
            cv.putText(self.actual.raw, text, pf, cv.FONT_HERSHEY_SIMPLEX, fsz, color, 2, cv.CV_AA)