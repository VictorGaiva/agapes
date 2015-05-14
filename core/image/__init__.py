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
from copy import deepcopy
from ..util import Point
import cv2 as cv
import numpy

class Image(object):
    """
    Protege e intermedia todas as interações com imagens.
    Também analiza e aplica quaisquer alterações requisitadas
    a uma das versões da imagem.
    """

    def __init__(self, source):
        """
        Inicializa e cria uma nova instância do objeto.
        :param source Imagem alvo do objeto.
        :return Image
        """
        self.shape = Point(*source.shape[:2]).swap
        self.raw = source

    def __getitem__(self, index):
        """
        Localiza e acessa um pixel ou uma região da imagem.
        :param index Índice ou fatia a ser acessada.
        :return tuple
        """
        return self.raw[index[1], index[0]]

    def __setitem__(self, index, value):
        """
        Modifica o valor de um pixel ou de uma região de
        interesse da imagem.
        :param index Índice ou fatia a ser acessada.
        :param value Novo valor a ocupar os elementos selecionados.
        """
        self.raw[index[1], index[0]] = value

    @classmethod
    def load(cls, filename):
        """
        Carrega a imagem a partir de um arquivo e a transforma
        em um novo objeto Image.
        :param filename Nome do arquivo da imagem alvo.
        :return Image
        """
        raw = cv.imread(filename)
        return Image(raw)

    @classmethod
    def new(cls, shape, channels = 3, dtype = numpy.uint8):
        """
        Cria uma nova imagem totalmente vazia.
        :param shape Formato da imagem.
        :param channels Número de canais da imagem.
        :param dtype Tipo de cada elemento da imagem.
        :return Image
        """
        shape = (channels,) + shape[:] if channels > 1 else shape
        blank = numpy.zeros(shape[::-1], dtype)
        return Image(blank)

    def resize(self, proportion = 0, size = Point(1,1)):
        """
        Redimensiona a imagem de acordo com a proporção ou
        com o tamanho dado. Nenhuma distorção ocorrerá
        durante o processo.
        :param proportion Proporção de redimensionamento da imagem.
        :param size Tamanho mínimo da imagem após redimensionamento.
        :return Image
        """
        if self.shape.x * proportion < size[0] \
        or self.shape.y * proportion < size[1]:
            proportion = max(
                size[0] / float(self.shape.x),
                size[1] / float(self.shape.y)
            )

        raw = cv.resize(
            self.raw, None, fx = proportion, fy = proportion,
            interpolation = cv.INTER_NEAREST
        )

        return Image(raw)

    def copy(self):
        """
        Produz uma cópia profunda do imagem armazenada.
        Permite fazer alterações sobre essa imagem sem
        alterar a cópia original.
        :return Image
        """
        raw = deepcopy(self.raw)
        return Image(raw)

    def rect(self, p1, p2):
        """
        Retorna uma subimagem, ou seja, apenas um recorte
        da área total da imagem a partir dos pontos extremos.
        :param p1 Canto superior esquerdo da região a ser recortada.
        :param p2 Canto inferior direito da região a ser recortada.
        :return Image
        """
        #raw = self[p1[0] : p2[0], p1[1] : p2[1]]
        raw = self.raw[p1[1] : p2[1], p1[0] : p2[0]]
        return Image(raw)

    def region(self, pos, size):
        """
        Retorna uma subimagem, ou seja, apenas um recorte
        da área total da imagem.
        :param pos Canto superior esquerdo do recorte.
        :param size Tamanho da região a ser recortada.
        :return Image
        """
        #raw = self[pos[0] : pos[0] + size[0], pos[1] : pos[1] + size[1]]
        raw = self.raw[pos[1] : pos[1] + size[1], pos[0] : pos[0] + size[0]]
        return Image(raw)

    def binarize(self, thresh = 127, value = 255):
        """
        Transforma a imagem atual em uma imagem binária.
        :param thresh Limiar de separação.
        :param value Novo valor para pixels com valor acima de  thresh  .
        :return Image
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_BGR2GRAY)
        raw = cv.threshold(raw, thresh, value, cv.THRESH_BINARY)[1]
        return Image(raw)

    def swap(self):
        """
        Inverte a ordem dos canais no padrão RGB.
        :return Image
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_BGR2RGB)
        return Image(raw)

    def colorize(self):
        """
        Transforma uma imagem binária em uma imagem colorida.
        :return Image
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_GRAY2BGR)
        return Image(raw)

    def tolab(self):
        """
        Transforma a imagem atual para o tipo L*a*b*.
        :return Image
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_BGR2LAB)
        return Image(raw)

    def transpose(self):
        """
        Inverte a imagem atual. Assim, as dimensões se inventem
        e é necessário inverter as coordenadas de um ponto para
        resgatar um mesmo pixel da imagem anterior.
        :return Image
        """
        raw = cv.transpose(self.raw)
        return Image(raw)

    def show(self, wname = "image"):
        """
        Mostra a imagem armazenada pelo objeto.
        :return Window
        """
        from .window import Window

        win = Window(self, wname)
        win.show()

        return win

    def save(self, filename = "image.png"):
        """
        Salva a imagem atual em um arquivo.
        :param filename Nome do arquivo a ser criado.
        """
        cv.imwrite(filename, self.raw)