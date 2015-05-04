#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
PSG - Tecnologia Aplicada

Este é um módulo utilizado para contagem de falhas em
plantações de cana-de-açúcar através do uso de imagens
aéreas capturadas por VANT's ou aparelhos similares.

Este arquivo é responsével pelo desenho da interface do
programa e também pela execução e apresentação dos
resultados obtidos com a imagem fornecida.
"""
import math

import cv2 as cv
import numpy

from .component import *
from .util.point import *


class Line(ComponentList):
    """
    Armazena e forma uma linha juntando componentes diferentes em
    posições diferentes. A linha pode ser representada ou reduzida
    para um polinômio.
    """
    
    # Constantes de direção. Auxiliam ao encontrar uma nova
    # linha, permitindo passar o parâmetro direção de forma
    # mais legível.
    left = -1
    right = 1
    
    def __init__(self, cmap, *comps):
        """
        Inicializa e cria uma nova instância do objeto.
        @param list comps Componentes iniciais da linha.
        @return Line
        """
        super(Line, self).__init__(comps)
        [c.__setattr__('line', self) for c in comps]

        inf = float("inf")
        self.up = min(comps, key = lambda comp: comp.up).up
        self.down = max(comps, key = lambda comp: comp.down).down
        self.neigh = {'right': (inf, None), 'left': (inf, None)}
        self.__polynom = None

        self.map = cmap

    @classmethod
    def fromside(cls, line, dpoint, direction):
        """
        Forma uma nova linha baseado em dados encontrados em outra
        linha.
        :param line Linha a qual a nova linha se baseia.
        :param dpoint Vetor de distância entre as linhas.
        :param direction Direção em que a procura foi realizada.
        :return Line A nova linha encontrada.
        """
        comps = [None]
        
        for y in xrange(line.up, line.down):
            _x = int(dpoint.x + line.polynom(y))
            _y = int(dpoint.y + y)
            
            for _x in xrange(_x - 10, _x + 10):
                if 0 <= _x < line.map.shape.x and 0 <= _y < line.map.shape.y \
                and line.map[_x, _y] not in comps \
                and line.map[_x, _y] is not None \
                and line.map[_x, _y].line is None:
                    comps.append(line.map[_x, _y])
                    
        newl = cls(line.map, *comps[1:])
        newl.neigh['left' if direction > 0 else 'right'] = \
            dpoint.euclidean(), line
        
        newl.fill()
        newl.conquer()
        newl.fill()
        
        return newl
    
    @property
    def points(self):
        """
        Método-propriedade responsável por reunir todos os pontos
        de todos os componentes presentes na linha.
        @return list
        """
        return sum([comp.points for comp in self.comps], [])
    
    @property
    def polynom(self):
        """
        Executa regressão polinomial nos componentes e encontra o polinômio,
        e a curva que melhor se encaixam nos pontos da linha.
        @return polynom Polinômio obtido dos pontos.
        """
        if self.__polynom is None:
            x, y = zip(*self.points)
            self.__polynom = numpy.poly1d(numpy.polyfit(y, x, deg = 2))
            
        return self.__polynom
    
    @property
    def length(self):
        """
        Propriedade responsável pelo cálculo do comprimento de arco
        da linha atual.
        @return float Comprimento de arco da linha
        """
        df = self.polynom.deriv()
        fy = lambda y: math.sqrt((df ** 2 + 1)(y))
        
        i = (self.down - self.up) / 6.0
        j = fy(self.up) + fy(self.down) + fy((self.up + self.down) / 2.0)
        return i * j
    
    @property
    def area(self):
        """
        Propriedade responsável pelo cálculo da área ocupada pela linha.
        @return float Área ocupada.
        """
        return sum([comp.area for comp in self])
    
    @property
    def density(self):
        """
        Propriedade de densidade da linha. Indica, na média, a espessura
        da linha.
        @return int Densidade em pixels.
        """
        return int(round(self.area / self.length))
    
    def conquer(self):
        """
        Encontra e adiciona novos componentes achados sobre a imagem do
        polinômio. Após terminado o processo, corrige as propriedades da linha.
        @return None
        """
        before, after = self.nearby()
        keep = True
                
        while keep and (before or after):
            keep = self.add(before, after)
            before, after = self.nearby()
            
    def fill(self):
        """
        Encontra e adiciona novos componentes achados sobre o domínio atual
        da linha. Alguns componentes podem ter sido deixados para trás no
        momento de construção da linha.
        @return None
        """
        for _, comp in self.walkover(self.up, self.down):
            if comp is not None and comp not in self.comps \
            and comp.line is None:
                self.add(comp)
    
    def walkover(self, *control):
        """
        Anda por sobre o polinômio da linha e encontra o que está sob ele.
        @param list control Lista de parâmetros para o caminho na linha.
        @yields Point, Component
        """
        xlim, ylim = self.map.shape
        d = self.density / 2
        
        for y in xrange(*control):
            x = int(round(self.polynom(y)))
            
            for x in xrange(x - d, x + d):
                if 0 <= x < xlim and 0 <= y < ylim:
                    yield Point(x, y), self.map[x, y]
        
    def nearby(self):
        """
        Encontra o próximo componente - acima e abaixo da imagem do polinônio da
        linha - com uma distância máxima confiável até eles.
        @return list Componentes encontrados antes e depois da linha atual.
        """
        before, after = None, None
        limit = self.density * 4
                
        for _, comp in self.walkover(self.up - 1, self.up - limit, -1):
            if comp is not None:
                before = comp
                break
              
        for _, comp in self.walkover(self.down + 1, self.down + limit):
            if comp is not None:
                after = comp
                break
                
        return before, after
    
    def search(self, direction):
        """
        Procura pela linha mais próxima na direção indicada.
        @param direction Direção de busca de nova linha.
        @return bool Foi encontrada uma linha?
        """
        y0 = (self.down - self.up) * .5 + self.up
        x0 = self.polynom(y0)
        
        df = self.polynom.deriv()
        ty = numpy.poly1d([df(y0), 0])
        px = numpy.poly1d([-df(y0), y0 + df(y0) * x0])
        
        xlim, ylim = self.map.shape
        delta = int(self.density / 3) * direction
        pn = Point(x0 + delta, px(x0 + delta))
                
        while 0 <= pn.x < xlim and 0 <= pn.y < ylim:
            count, total = 0, 0.0
           
            for y in xrange(-30, 30):
                x = int(ty(y) + pn.x)
                y = int(pn.y) + y

                if 0 <= x < xlim and 0 <= y < ylim:
                    count = count + int(self.map[x, y] not in ([None] + self.comps))
                    total = total + 1
                        
            if total and (count / total) >= .25:
                break
            
            delta = delta + direction
            pn = Point(x0 + delta, px(x0 + delta))
            
        else:
            return False

        self.neigh['right' if direction > 0 else 'left'] \
            = pn.euclidean((x0, y0)), Line.fromside(self,  pn - (x0, y0), direction)
            
        return True
        
    def add(self, *comps):
        """
        Tenta adicionar novos componentes a uma linha. Caso não seja possível
        decidir a linha em que o componente se encontra, o componente é
        incluído em nenhuma delas.
        @param Component comps Componentes a serem adicionados.
        @return int
        """
        comps = [comp for comp in comps if comp is not None]
        added = 0
        
        for comp in comps:
            
            if comp.line is not None:
                comp.line.comps.remove(comp)
                comp.line.__polynom = None
                
                if comp.line.count > 0:
                    comp.line = None
                    continue

            if comp.up < self.up:
                self.up = comp.up
                
            if comp.down > self.down:
                self.down = comp.down
                
            self.comps.append(comp)
            self.__polynom = None
            comp.line = self
            
            added = added + 1
            
        return added
    
    def draw(self, img, color):
        """
        Desenha dados sobre uma linha.
        @param img Imagem alvo.
        @param color Cor dos componentes a serem pintados.
        @return None
        """
        for comp in self.comps:
            comp.draw(img, color)
            
        for y in xrange(self.up, self.down):
            x = int(round(self.polynom(y)))
            
            if not 0 <= x < self.map.shape.x:
                continue
                
            if self.map[x, y] in self.comps:
                cv.circle(img.raw, (x, y), 0, (255, 0, 0), 2)
            else:
                cv.circle(img.raw, (x, y), 0, (0, 0, 255), 2)
            
class LineList(object):
    """
    Armazena e manipula uma lista de linhas obtidas de uma
    imagem. Esse objeto também é responsável pela criação de todas
    as linhas existentes.
    """
    
    def __init__(self, cmap):
        """
        Inicializa e cria uma nova instância do objeto.
        @return LineList
        """
        self.lines = type('rawLineList', (list,), {
            'first': property(lambda this: this[0]),
            'last':  property(lambda this: this[-1])
        })()

        self.map = cmap
        self.shape = cmap.shape
        
    def __getitem__(self, index):
        """
        Acessa e retorna a linha presente na posição dada
        pelo parâmetro index.
        :param index Índice ou índices a serem explorados.
        :return Line|list
        """
        return self.lines[index]

    @classmethod
    def first(cls, cmap, *comps):
        """
        Inicia uma instância de lista de linhas e fornece à
        lista a primeira linha encontrada que será base
        para a descoberta de todas as outras.
        :param list comps Componentes que formam a primeira linha.
        :return LineList
        """
        line = Line(cmap, *comps)
        llst = cls(cmap)

        line.conquer()
        llst.add(line)

        return llst

    @property
    def count(self):
        """
        Contagem de linhas na lista.
        :return int Quantidade de elementos.
        """
        return len(self.lines)
        
    def add(self, *lines):
        """
        Adiciona novas linhas no fim da lista.
        @param list linhas Novas linhas a serem adicionadas.
        """
        self.lines.extend(lines)
    
    def search(self):
        """
        Executa a busca de novas linhas a partir das linhas localizadas
        nos extremos da lista.
        @yields int, Line Posição da nova linha encontrada e a própria linha.
        """
        while self.lines.first.search(Line.left):
            yield 0, self.lines.first.neigh['left'][1]
            
        while self.lines.last.search(Line.right):
            yield self.count, self.lines.last.neigh['right'][1]
    
    def complete(self):
        """
        Procura por novas linhas, adjacentes às linhas já
        conhecidas.
        @return None
        """
        for pos, line in self.search():
            self.lines.insert(pos, line)
    
    def display(self, inverted):
        """
        Mostra em uma imagem, todas as linhas presentes na lista.
        @return Image
        """
        img = Image.new(self.shape, inverted = inverted)

        for line in self.lines:
            line.draw(img, (255, 255, 255))

        if img.inverted:
            img = img.transpose()

        return img
        
    def error(self, distance, inverted):
        """
        Contabiliza a porcentagem de erros nas linhas encontradas.
        @param distance Distância entre linhas em metros.
        @return float, int Porcentagem e metros de falhas encontradas.
        @return inverted Imagem está invertida?
        """
        img = Image.new(self.shape, inverted = inverted)
        red, blue = 0, 0
        distmedia = 0
        
        for line in self.lines:
            proxline = min(line.neigh["left"][0], line.neigh["right"][0])
            maxdist = (.5 * proxline / distance)
            distmedia += maxdist
            points = []
            
            for comp in line.comps:
                comp.draw(img, (255, 255, 255))


            for y in xrange(line.up, line.down):
                x = int(round(line.polynom(y)))
                incomp = False

                for _x in xrange(x - 5, x + 5):
                    if 0 <= _x < self.shape.x \
                    and self.map[_x, y] is not None and self.map[_x, y] in line.comps:
                        incomp = True
                        break

                if incomp:
                    if len(points) > maxdist:
                        for p in points:
                            cv.circle(img.raw, p, 0, (0,0,255),2)
                        red += len(points)
                    elif len(points) > 0:
                        for p in points:
                            cv.circle(img.raw, p, 0, (255,0,0),2)
                        blue += len(points)

                    cv.circle(img.raw, (x,y), 0, (255,0,0),2)
                    points = []
                    blue += 1

                else:
                    points.append(Point(x,y))

            if len(points) > maxdist:
                for p in points:
                    cv.circle(img.raw, p, 0, (0,0,255),2)
                red += len(points)
            elif len(points) > 0:
                for p in points:
                    cv.circle(img.raw, p, 0, (255,0,0),2)
                blue += len(points)

        if img.inverted:
            img = img.transpose()

        total = red + blue
        metro = 2 * (distmedia / len(self.lines))
        return (100 * red) / total, red / metro, img
