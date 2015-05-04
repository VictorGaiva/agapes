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
import math

class Point(tuple):
    """
    Armazena as coordenadas de um ponto e implementa operações
    básicas a serem aplicadas sobre ele.
    """

    def __new__(cls, x, y):
        """
        Cria uma nova instância do objeto.
        :param x Valor do índice #0.
        :param y Valor do índice #1.
        :return tuple
        """
        return super(Point, cls).__new__(cls, [x, y])

    def __init__(self, x, y):
        """
        Inicializa a nova instância do objeto.
        :param x Valor do ponto no eixo-x.
        :param y Valor do ponto no eixo-y.
        :return Point
        """
        super(Point, self).__init__()
        self.x = x
        self.y = y

    def __add__(self, other):
        """
        Implementa a soma de dois pontos.
        :param other Operador do cálculo de soma.
        :return Point
        """
        return Point(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        """
        Implementa a soma invertida de dois pontos.
        :param other Operador do cálculo de soma.
        :return Point
        """
        return Point(other[0] + self.x, other[1] + self.y)

    def __sub__(self, other):
        """
        Implementa a subtração de dois pontos.
        :param other Operador do cálculo de subtração.
        :return Point
        """
        return Point(self.x - other[0], self.y - other[1])

    def __rsub__(self, other):
        """
        Implementa a subtração invertida de dois pontos.
        :param other Operador do cálculo de subtração.
        :return Point
        """
        return Point(other[0] - self.x, other[1] - self.y)

    def __mul__(self, value):
        """
        Implementa a multiplicação por um escalar.
        :param value Escalar para a multiplicação.
        :return Point
        """
        return Point(self.x * value, self.y * value)

    def __rmul__(self, value):
        """
        Implementa a multiplicação invertida por um escalar.
        :param value Escalar para a multiplicação.
        :return Point
        """
        return Point(value * self.x, value * self.y)

    def __div__(self, value):
        """
        Implementa a divisão por um escalar.
        :param value Escalar para a divisão.
        :return Point
        """
        return Point(self.x / float(value), self.y / float(value))

    def __rdiv__(self, value):
        """
        Implementa a divisão de um escalar por um ponto.
        :param value Escalar para a divisão.
        :return Point
        """
        return Point(value / float(self.x), value / float(self.y))

    def __floordiv__(self, value):
        """
        Implementa a divisão inteira por um escalar.
        :param value Escalar para a divisão.
        :return Point
        """
        return Point(int(self.x // value), int(self.y // value))

    def __rfloordiv__(self, value):
        """
        Implementa a divisão inteira de um escalar por um ponto.
        :param value Escalar para a divisão.
        :return Point
        """
        return Point(int(value // self.x), int(value // self.y))

    def __abs__(self):
        """
        Implementa a operação de módulo nas coordenadas
        do ponto.
        :return Point
        """
        return Point(abs(self.x), abs(self.y))

    def __neg__(self):
        """
        Inverte os valores armazenados para um novo objeto.
        :return Point
        """
        return Point(-self.x, -self.y)

    @property
    def vector(self):
        """
        Transforma o ponto em um vetor.
        :return Vector
        """
        from .vector import Vector
        return Vector(*self)

    @property
    def swap(self):
        """
        Inverte as coordenadas do ponto.
        :return Point
        """
        return Point(self.y, self.x)

    def round(self, precision = 0):
        """
        Arredonda os valores armazenados pelo objeto.
        :param precision Precisão do arredondamento.
        :return Point
        """
        x = round(self.x, precision)
        y = round(self.y, precision)
        return Point(x, y)

    def euclidean(self, destiny):
        """
        Calcula a distância euclidiana até um outro ponto.
        :param destiny Ponto para ser comparado.
        :return float
        """
        deltax = self.x - destiny[0]
        deltay = self.y - destiny[1]
        dist = math.sqrt(deltax ** 2 + deltay ** 2)
        return dist
    
    def manhattan(self, destiny):
        """
        Calcula a distância de Manhattan até um outro ponto.
        :param destiny Ponto para ser comparado.
        :return float
        """
        deltax = self.x - destiny[0]
        deltay = self.y - destiny[1]
        dist = abs(deltax) + abs(deltay)        
        return dist
