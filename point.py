#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@package PSG
@author Adolfo Hengling <adolfohengling@gmail.com>
@author Marcos Teixeira <ecclesiedei@gmail.com>
@author Rodrigo Siqueira <rodriados@gmail.com>
"""
import math

class Point(tuple):
    """
    Armazena as coordenadas de um ponto e implementa operações
    básicas a serem aplicadas sobre ele.
    @module point
    """
    
    def __new__(cls, x, y):
        """
        Cria uma nova instância do objeto.
        @param float x Valor do índice 0
        @param float y Valor do índice 1
        @return Point
        """
        return super(Point, cls).__new__(cls, [x, y])

    def __init__(self, x, y):
        """
        Inicializa uma nova instância do objeto.
        @param float x Valor do ponto no eixo-x
        @param float y Valor do ponto no eixo-y
        @return Point
        """
        super(Point, self).__init__()
        self.x = x
        self.y = y
        
    def __add__(self, other):
        """
        Implementa a soma de dois pontos.
        @param Point|tuple other Operador do cálculo
        @return Point
        """
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        """
        Implementa a soma de dois pontos.
        @param Point|tuple other Operador do cálculo
        @return Point
        """
        return Point(self.x - other[0], self.y - other[1])
    
    def __neg__(self):
        """
        Inverte os valores armazenados para um novo objeto.
        @return Point
        """
        return Point(-self.x, -self.y)
        
    @property
    def inverse(self):
        """
        Inverte as coordenadas do ponto.
        @return Point Ponto invertido.
        """
        return Point(self.y, self.x)
    
    def round(self, precision = 0):
        """
        Arredonda os valores armazenados pelo objeto.
        @param int precision Precisão do arredondamento.
        @return Point
        """
        x = round(self.x, precision)
        y = round(self.y, precision)
        return Point(x, y)
        
    def euclidean(self, destiny = (0,0)):
        """
        Calcula a distância euclidiana até um outro ponto.
        @param Point|tuple destiny Ponto para ser comparado.
        @return double Distância entre os dois pontos.
        """
        deltax = self.x - destiny[0]
        deltay = self.y - destiny[1]
        dist = math.sqrt(deltax ** 2 + deltay ** 2)
        return dist
    
    def manhattan(self, destiny):
        """
        Calcula a distância de Manhattan até um outro ponto.
        @param Point|tuple destiny Ponto para ser comparado.
        @return double Distância entre os dois pontos.
        """
        deltax = self.x - destiny[0]
        deltay = self.y - destiny[1]
        dist = abs(deltax) + abs(deltay)        
        return dist