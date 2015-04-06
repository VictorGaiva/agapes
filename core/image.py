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
from controller import ThreadWrapper
from .point import *

import cv2 as cv
import config
import numpy
import copy

class Image(object):
    """
    Protege e intermedia todas as interações com a imagem
    aberta. Também analiza e aplica quaisquer alterações
    requisitadas a uma das versões da imagem.
    """

    def __init__(self, source, inverted = False):
        """
        Inicializa e cria uma nova instância do objeto.
        :param source Imagem alvo do objeto.
        :param inverted A imagem está invertida?
        :return Nova instância do objeto de imagem.
        """
        self.shape = Point(*source.shape[:2]).swap
        self.inverted = inverted
        self.raw = source
    
    def __getitem__(self, index):
        """
        Localiza e retorna um pixel ou uma região da imagem.
        :param index Índice ou fatia a ser acessada.
        :return Pixel ou região selecionada.
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
        :return Instância com a imagem carregada.
        """
        raw = cv.imread(filename)
        return cls(raw)
    
    @classmethod
    def new(cls, shape, dtype = numpy.uint8, channels = 3, inverted = False):
        """
        Cria uma nova imagem totalmente vazia.
        :param shape Formato da imagem.
        :param dtype Tipo de cada elemento da imagem.
        :param channels Número de canais da imagem.
        :param inverted A imagem está invertida?
        :return Imagem vazia criada.
        """
        shape = (channels,) + shape if channels > 1 else shape
        blank = numpy.zeros(shape[::-1], dtype)
        return cls(blank, inverted)
    
    def resize(self, proportion, min = Point(1,1)):
        """
        Redimensiona a imagem de acordo com a proporção dada.
        Nenhuma distorção ocorrerá durante o processo.
        :param proportion Proporção de redimensionamento da imagem.
        :param min Tamanho mínimo da imagem após redimensionamento.
        :return Imagem redimensionada.
        """
        if self.shape.x * proportion < min[0] \
        or self.shape.y * proportion < min[1]:
            proportion = max(
                min[0] / float(self.shape.x),
                min[1] / float(self.shape.y)
            )

        raw = cv.resize(self.raw, None, fx = proportion, fy = proportion)
        return Image(raw, self.inverted)

    def region(self, pos, size):
        """
        Retorna uma subimagem, ou seja, apenas um recorte
        da área total da imagem.
        :param pos Canto superior esquerdo do recorte.
        :param size Tamanho do recorte.
        :return Recorte de imagem.
        """
        raw = self[pos[0] : pos[0] + size[0], pos[1] : pos[1] + size[1]]
        return Image(raw, self.inverted)

    def glue(self, pos, size, image):
        """
        Cola uma imagem sobre a região indicada.
        :param pos Ponto esquerdo superior da região.
        :param size dimensões da região de colagem.
        :param image Imagem a ser colada.
        """
        self[
            pos.x : pos.x + size.x,
            pos.y : pos.y + size.y
        ] = image.raw

    def binarize(self, thresh = 127, value = 255):
        """
        Transforma a imagem atual em uma imagem binária.
        :param thresh Limiar de separação.
        :param value Novo valor para pixels com valor acima de  thresh  .
        :return Imagem binária gerada.
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_BGR2GRAY)
        raw = cv.threshold(raw, thresh, value, cv.THRESH_BINARY)[1]
        return Image(raw, self.inverted)
    
    def colorize(self):
        """
        Transforma uma imagem binária em uma imagem colorida.
        :return Imagem colorida gerada.
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_GRAY2BGR)
        return Image(raw, self.inverted)

    def tolab(self):
        """
        Transforma a imagem atual para o tipo L*a*b*.
        :return Imagem gerada no formato L*a*b*.
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_BGR2LAB)
        return Image(raw, self.inverted)

    def normalize(self, color = True):
        """
        Normaliza a ordem dos canais no padrão RGB.
        :param color Corrigir canais de cor?
        :return Imagem colorida gerada.
        """
        if color:
            raw = cv.cvtColor(self.raw, cv.COLOR_BGR2RGB)
        else:
            raw = self.raw
        img = Image(raw) if not self.inverted else Image(raw, True).transpose()

        return img

    def transpose(self):
        """
        Inverte a imagem atual. Assim, as dimensões se inventem
        e é necessário inverter as coordenadas de um ponto para
        resgatar um mesmo pixel da imagem anterior.
        :return Imagem transposta.
        """
        raw = cv.transpose(self.raw)
        return Image(raw, not self.inverted)

    def show(self, wname = "image"):
        """
        Mostra a imagem armazenada pelo objeto e espera até que
        um botão seja apertado ou a janela seja fechada.
        :param wname Nome da janela a ser aberta.
        """
        ImageWindow(wname, self)
    
    def save(self, filename = "image.png"):
        """
        Salva a imagem atual em um arquivo.
        :param filename Nome do arquivo a ser criado.
        """
        cv.imwrite(
            filename,
            self.raw if not self.inverted else self.transpose().raw
        )

class ImageWindow(object):
    """
    Classe responsável pela exibição de uma imagem e também
    pelo controle da imagem sobre a janela, permitindo que
    a imagem seja deslocada e toda a imagem seja visível em
    uma tela menor que ela.
    """
    
    def __init__(self, wname, img, quantity = 1, index = None):
        """
        Inicializa e cria uma nova instância do objeto.
        :param wname Nome da janela a ser criada.
        :param img Imagem a ser exibida.
        :param quantity Quantidade de vezes  image  deve ser empilhado.
        :return Instância criada.
        """
        self.wsize = Point(*config.wsize)
        self.wname = "{0} #{1}".format(wname, config.wid)
        config.wid += 1

        self.index = (quantity - 1) if index is None else index
        self.shape = img.shape
        self.word = None
        self.mousecontrol = True
        self.anchor = Point(0,0)
        self.keep = True

        self.image = [
            Image(copy.deepcopy(
                img.raw if not img.inverted else img.transpose().raw
            )) for i in xrange(quantity)
        ]

        self.show()

    def __getitem__(self, index):
        """
        Permite o acesso exterior às imagens armazenadas na janela.
        :param index Índice da imagem a ser retornada.
        :return Image
        """
        return self.image[index]

    def append(self, image):
        """
        Adiciona uma imagem à lista de imagens a serem exibidas.
        :param image Imagem a ser adiciona à lista.
        """
        self.image.append(image if not image.inverted else image.transpose())
        self.index = len(self.image) - 1
        self.frame()
        
    @ThreadWrapper
    def show(self):
        """
        Método responsável por gerir a exibição da imagem.
        """
        mid = Point(self.shape.x / 2, self.shape.y / 2)
        self.anchor = Point(mid.x - self.wsize.x / 2, mid.y - self.wsize.y / 2)
        self._mousep = None

        cv.namedWindow(self.wname, cv.WINDOW_AUTOSIZE)
        self.updateloop()

        cv.destroyWindow(self.wname)
        exit()

    def updateloop(self):
        """
        Método responsável pela atualização constante do frame
        de imagem, encerrando somente quando o critério de parada
        """
        cv.setMouseCallback(self.wname, self.mouse)
        key = cv.waitKey(10) % 256

        while key != 27 and self.keep:
            self.frame()
            cv.setMouseCallback(self.wname, self.mouse)
            key = cv.waitKey(10) % 256

            if key in [ord('w'), ord('W')]:
                self.index = self.index + 1 \
                    if self.index < len(self.image) - 1 else 0
            elif key in [ord('s'), ord('S')]:
                self.index = self.index - 1 \
                    if self.index > 0 else len(self.image) - 1

    def mouse(self, event, x, y, flag, *param):
        """
        Método responsável pelo controle do mouse.
        :param event Evento realizado pelo mouse.
        :param x Coordenadas-x do evento.
        :param y Coordenadas-y do evento.
        :param flag Flags do evento.
        :param param Parâmetros adicionais.
        """
        if self.mousecontrol == True:
            if event == cv.EVENT_LBUTTONDOWN:
                self._mousep = Point(x, y)
            elif event == cv.EVENT_MOUSEMOVE and flag & cv.EVENT_FLAG_LBUTTON:
                _x, _y = self.anchor + (self._mousep - (x, y))

                _x = _x if _x > 0 else 0
                _y = _y if _y > 0 else 0

                _x = _x if _x <= self.shape.x - self.wsize.x    \
                    else self.shape.x - self.wsize.x

                _y = _y if _y <= self.shape.y - self.wsize.y    \
                    else self.shape.y - self.wsize.y

                self._mousep = Point(x, y)
                self.anchor = Point(_x, _y)
                self.frame()

        elif self.mousecontrol != False:
            self.mousecontrol(event, x, y, flag, *param)

    def text(self, txt, pos, color = (255, 255, 0)):
        """
        Insere um texto estático na janela.
        :param txt Texto a ser posicionado.
        :param pos Posição do texto.
        :param color Cor do texto.
        """
        pos = tuple([
            (pos[i] if pos[i] >= 0 else self.wsize[i] + pos[i])
                for i in xrange(2)
        ])

        self.word = type('', (object,), {
            'word': txt,
            'pos': pos,
            'color': color
        })

    def frame(self):
        """
        Cria e exibe a imagem da janela.
        """
        wframe = copy.deepcopy(self.image[self.index][
            self.anchor.x : self.anchor.x + self.wsize.x,
            self.anchor.y : self.anchor.y + self.wsize.y
        ])
        
        if self.word is not None:
            cv.putText(wframe, self.word.word, self.word.pos,
                cv.FONT_HERSHEY_TRIPLEX, 0.7, self.word.color
            )
            
        cv.imshow(self.wname, wframe)