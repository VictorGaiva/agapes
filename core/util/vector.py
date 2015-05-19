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

class Vector(tuple):
    """
    Representação de vetor sobre um plano cartesiano
    bidimensional.
    """

    def __new__(cls, x, y):
        """
        Cria uma nova instância do objeto.
        :param x Valor do índice #0.
        :param y Valor do índice #1.
        :return tuple
        """
        return super(Vector, cls).__new__(cls, [x, y])

    def __init__(self, x, y):
        """
        Inicializa a nova instância do objeto.
        :param x Valor do ponto no eixo-x.
        :param y Valor do ponto no eixo-y.
        :return Vector
        """
        super(Vector, self).__init__()
        self.x = x
        self.y = y

    def __add__(self, other):
        """
        Implementa a soma de dois vetores.
        :param other Operador do cálculo de soma.
        :return Vector
        """
        return Vector(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        """
        Implementa a soma invertida de dois vetores.
        :param other Operador do cálculo de soma.
        :return Vector
        """
        return Vector(other[0] + self.x, other[1] + self.y)

    def __sub__(self, other):
        """
        Implementa a subtração de dois vetores.
        :param other Operador do cálculo de subtração.
        :return Vector
        """
        return Vector(self.x - other[0], self.y - other[1])

    def __rsub__(self, other):
        """
        Implementa a subtração invertida de dois vetores.
        :param other Operador do cálculo de subtração.
        :return Vector
        """
        return Vector(other[0] - self.x, other[1] - self.y)

    def __mul__(self, value):
        """
        Implementa a multiplicação por um escalar.
        :param value Escalar para a multiplicação.
        :return Vector
        """
        return Vector(self.x * value, self.y * value)

    def __rmul__(self, value):
        """
        Implementa a multiplicação invertida por um escalar.
        :param value Escalar para a multiplicação.
        :return Vector
        """
        return Vector(value * self.x, value * self.y)

    def __div__(self, value):
        """
        Implementa a divisão por um escalar.
        :param value Escalar para a divisão.
        :return Vector
        """
        return Vector(self.x / value, self.y / value)

    def __rdiv__(self, value):
        """
        Implementa a divisão de um escalar por um vetor.
        :param value Escalar para a divisão.
        :return Vector
        """
        return Vector(value / self.x, value / self.y)

    def __floordiv__(self, value):
        """
        Implementa a divisão inteira por um escalar.
        :param value Escalar para a divisão.
        :return Vector
        """
        return Vector(int(self.x // value), int(self.y // value))

    def __rfloordiv__(self, value):
        """
        Implementa a divisão inteira de um escalar por um vetor.
        :param value Escalar para a divisão.
        :return Vector
        """
        return Vector(int(value // self.x), int(value // self.y))

    def __abs__(self):
        """
        Implementa a operação de módulo nas coordenadas
        do vetor.
        :return Vector
        """
        return Vector(abs(self.x), abs(self.y))

    def __neg__(self):
        """
        Inverte os valores armazenados para um novo objeto.
        :return Vector
        """
        return Vector(-self.x, -self.y)

    @property
    def point(self):
        """
        Transforma o vetor em um ponto.
        :return Point
        """
        from .point import Point
        return Point(*self)

    @property
    def length(self):
        """
        Calcula o tamanho - norma - do vetor.
        :return float
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def versor(self):
        """
        Normaliza o vetor, transformando-o em um versor.
        Em outras palavras, um vetor com tamanho 1.
        :return Vector
        """
        try:
            return self / float(self.length)
        except ZeroDivisionError:
            return Vector(0,0)

    @property
    def angle(self):
        """
        Calcula o cosseno e o seno do ângulo do vetor
        no plano cartesiano.
        :return float
        """
        return math.copysign(math.acos(self.versor.x), self.y)

    def round(self, precision = 0):
        """
        Arredonda os valores armazenados pelo objeto.
        :param precision Precisão do arredondamento.
        :return Vector
        """
        x = round(self.x, precision)
        y = round(self.y, precision)
        return Vector(x, y)
