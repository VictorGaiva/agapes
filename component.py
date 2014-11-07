#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@package PSG
@author Adolfo Hengling <adolfohengling@gmail.com>
@author Marcos Teixeira <ecclesiedei@gmail.com>
@author Rodrigo Siqueira <rodriados@gmail.com>
"""
from image import *
from point import *
from map import *
import cv2 as cv
import numpy
import copy

class Component(object):
    """
    Armazena, protege e manipula todos os pontos de um componente conexo da
    imagem. Cada componente é dado por uma lista de pontos, que juntos
    descrevem o contorno do componente.
    @module component
    """
    
    def __init__(self, contour):
        """
        Inicializa e cria uma nova instância do objeto.
        @param list contour Lista de pontos que descrevem os contornos do componente.
        @return Component
        """
        self.points = [Point(*pnt[0]) for pnt in contour]
        self.contour = contour
                
        self.up = min(self.points, key = lambda pnt: pnt.y).y
        self.down = max(self.points, key = lambda pnt: pnt.y).y
        self.area = cv.contourArea(contour)
        self.belief = self.down - self.up
        self.line = None
    
    @classmethod
    def load(cls, image):
        """
        Encontra todos os componentes presentes na imagem dada, e
        retorna a lista de todos os componentes.
        @param Image image Imagem alvo da operação.
        @return ComponentList
        """
        raw = copy.deepcopy(image.raw)
        cnts, _ = cv.findContours(raw, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        lcomp = [cls(contour) for contour in cnts]
        comps = [comp for comp in lcomp if comp.belief > 1]
        
        return ComponentList.mapped(comps, image.shape)
    
    def draw(self, image, color):
        """
        Desenha os contornos do componente em uma imagem com a cor determinada.
        @param Image image Imagem alvo para o desenho da linha.
        @param tuple|int color Cor a ser usada.
        """
        cv.drawContours(image.raw, [self.contour], 0, color, -1)
        
class ComponentList(object):
    """
    Armazena uma lista de componentes obtidos da imagem. Este objeto
    administra, manipula e executa diversas operações sobre uma
    lista de componentes encontrados.
	@module component
    """
    
    def __init__(self, lcomp):
        """
        Inicializa e cria uma nova instância do objeto.
        @param list lcomp Lista de componentes.
        @return ComponentList
        """
        self.comps = list(lcomp)
        
    def __getitem__(self, index):
        """
        Acessa a lista e retorna o Component encontrado na posição dada.
        Caso o parâmetro seja uma slice, uma lista de Component é retornada.
        @param int|slice index Índice do elemento a ser retornado.
        @return Component|list
        """
        return ([None] + self.comps)[index]
    
    def __iter__(self):
        """
        Transforma o objeto em um iterável para permitir a fácil iteração
        entre os componentes armazenados.
        @yields Component
        """
        for component in self.comps:
            yield component
    
    @classmethod
    def mapped(cls, lcomp, shape):
        """
        Inicializa o objeto com componentes já instanciados e
        cria o mapa de localização desses componentes.
        @param list lcomp Componentes instanciados.
        @param tuple shape Formato da imagem alvo.
        @return ComponentList
        """
        new = cls(lcomp)
        new.sort()
                
        map = Image.new(shape, numpy.uint16, 1)
        [comp.draw(map, i + 1) for i, comp in enumerate(new.comps)]
        Map.set(map, [None] + new.comps)
        
        return new
    
    @property
    def count(self):
        """
        Contagem de componentes na lista.
        @return int Quantidade de elementos.
        """
        return len(self.comps)
    
    def sort(self, key = lambda c: c.belief, reverse = False):
        """
        Ordena os componentes de acordo com a confiança individual de cada
        componente presente na imagem.
        @param lambda key Função para a ordenação dos componentes.
        """
        self.comps = sorted(self.comps, key = key, reverse = not reverse)
        
    def draw(self, image, color):
        """
        Desenha todos os componentes em uma imagem com a cor determinada.
        @param Image image Imagem alvo para o desenho da linha.
        @param tuple|int color Cor a ser usada.
        """
        for comp in self:
            comp.draw(image, color)
        