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
        :return Novo ponto inicializado.
        """
        return super(Point, cls).__new__(cls, [x, y])

    def __init__(self, x, y):
        """
        Inicializa uma nova instância do objeto.
        :param x Valor do ponto no eixo-x.
        :param y Valor do ponto no eixo-y.
        :return Ponto inicializado.
        """
        super(Point, self).__init__()
        self.x = x
        self.y = y
        
    def __add__(self, other):
        """
        Implementa a soma de dois pontos.
        :param other Operador do cálculo de soma.
        :return Novo ponto com valores somados.
        """
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        """
        Implementa a soma de dois pontos.
        :param other Operador do cálculo de subtração.
        :return Novo ponto com valores subtraídos.
        """
        return Point(self.x - other[0], self.y - other[1])
    
    def __neg__(self):
        """
        Inverte os valores armazenados para um novo objeto.
        :return Novo ponto negativado.
        """
        return Point(-self.x, -self.y)
        
    @property
    def swap(self):
        """
        Inverte as coordenadas do ponto.
        :return Novo ponto com coordenadas invertidas.
        """
        return Point(self.y, self.x)
    
    def round(self, precision = 0):
        """
        Arredonda os valores armazenados pelo objeto.
        :param precision Precisão do arredondamento.
        :return Ponto com coordenandas arredondadas.
        """
        x = round(self.x, precision)
        y = round(self.y, precision)
        return Point(x, y)
        
    def euclidean(self, destiny = (0,0)):
        """
        Calcula a distância euclidiana até um outro ponto.
        :param destiny Ponto para ser comparado.
        :return Distância euclidiana entre os dois pontos.
        """
        deltax = self.x - destiny[0]
        deltay = self.y - destiny[1]
        dist = math.sqrt(deltax ** 2 + deltay ** 2)
        return dist
    
    def manhattan(self, destiny):
        """
        Calcula a distância de Manhattan até um outro ponto.
        :param destiny Ponto para ser comparado.
        :return Distância de manhattan entre os dois pontos.
        """
        deltax = self.x - destiny[0]
        deltay = self.y - destiny[1]
        dist = abs(deltax) + abs(deltay)        
        return dist