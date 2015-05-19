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
import copy

import cv2 as cv
import numpy

from .util import Point
from .map import *


class Component(object):
    """
    Armazena, protege e manipula todos os pontos de um componente conexo da
    imagem. Cada componente é dado por uma lista de pontos, que juntos
    descrevem o contorno do componente.
    """
    
    def __init__(self, contour):
        """
        Inicializa e cria uma nova instância do objeto.
        :param contour Lista de pontos que descrevem os contornos do componente.
        :return Component
        """
        self.points = map(lambda p: Point(*p[0]), contour)
        self.contour = contour
                
        self.up = min(self.points, key = lambda pnt: pnt.y).y
        self.down = max(self.points, key = lambda pnt: pnt.y).y
        self.area = cv.contourArea(contour)
        self.belief = self.down - self.up
        self.line = None
    
    def draw(self, image, color):
        """
        Desenha os contornos do componente em uma imagem com a cor determinada.
        :param image Imagem alvo para o desenho da linha.
        :param color Cor a ser usada.
        """
        cv.drawContours(image.raw, [self.contour], 0, color, -1)
        
class ComponentList(object):
    """
    Armazena uma lista de componentes obtidos da imagem. Este objeto
    administra, manipula e executa diversas operações sobre uma
    lista de componentes encontrados.
    """
    
    def __init__(self, lcomp):
        """
        Inicializa e cria uma nova instância do objeto.
        :param lcomp Lista de componentes.
        :return ComponentList
        """
        self.comps = list(lcomp)
        
    def __getitem__(self, index):
        """
        Acessa a lista e retorna o Component encontrado na posição dada.
        Caso o parâmetro seja uma slice, uma lista de Component é retornada.
        :param index Índice do elemento a ser retornado.
        :return Component|list
        """
        return ([None] + self.comps)[index]
    
    def __iter__(self):
        """
        Transforma o objeto em um iterável para permitir a fácil iteração
        entre os componentes armazenados.
        :yield Component
        """
        for component in self.comps:
            yield component

    @classmethod
    def load(cls, img):
        """
        Encontra todos os componentes presentes na imagem dada, e
        retorna a lista de todos os componentes.
        :param img Imagem alvo da operação.
        :return ComponentList, Map
        """
        def generate():
            yield img
            yield img.transpose()

        slopes = []

        for inv, image in enumerate(generate()):
            raw = copy.deepcopy(image.raw)
            cts = cv.findContours(raw, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[0]

            lcomp = map(Component, cts)
            lcomp = filter(lambda comp: comp.belief > 1, lcomp)
            lcomp = cls(lcomp).sort()

            slopev = lcomp.slope()
            slopes.append([slopev, lcomp, image.shape, inv])

            if slopev > 1:
                break

        lcomp, shape, inverted = max(slopes, key = lambda el: el[0])[1:]
        cmap = lcomp.map(shape, inverted)

        return lcomp, cmap, inverted
    
    @property
    def count(self):
        """
        Contagem de componentes na lista.
        :return Quantidade de elementos.
        """
        return len(self.comps)

    def map(self, shape, inverted):
        """
        Inicializa o objeto com componentes já instanciados e
        cria o mapa de localização desses componentes.
        :param shape Formato da imagem alvo.
        :param inverted O mapa estará invertido?
        :return Map
        """
        cmap = Map(self.comps, shape, inverted)
        return cmap

    def slope(self, count = 10):
        """
        Verifica a necessidade de rotação da imagem.
        :param count Quantidade de componentes a serem analizados.
        :return float Média de inclinação dos componentes.
        """
        func = lambda comp: numpy.poly1d(
            numpy.polyfit(
                *zip(*comp.points), deg = 1
            )
        )[1]

        value = map(func, self.comps[1:count + 1])
        return sum(value) / float(count)
    
    def sort(self, key = lambda c: c.belief, reverse = False):
        """
        Ordena os componentes de acordo com a confiança individual de cada
        componente presente na imagem.
        :param key Função para a ordenação dos componentes.
        :param reverse Os componentes devem estar na ordem contrária?
        """
        self.comps = sorted(self.comps, key = key, reverse = not reverse)
        return self
        
    def draw(self, image, color):
        """
        Desenha todos os componentes em uma imagem com a cor determinada.
        :param image Imagem alvo para o desenho da linha.
        :param color Cor a ser usada.
        """
        for comp in self:
            comp.draw(image, color)
        