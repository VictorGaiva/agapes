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
from .point import *
import config

from threading import Thread
import cv2 as cv
import numpy
import copy

class Image(object):
    """
    Protege e intermedia todas as interações com a imagem
    aberta. Também analiza e aplica quaisquer alterações
    requisitadas a uma das versões da imagem.
    """
    
    def __init__(self, source):
        """
        Inicializa e cria uma nova instância do objeto.
        :param source Imagem alvo do objeto.
        :return Nova instância do objeto de imagem.
        """
        self.shape = Point(*source.shape[:2]).swap
        self.inverted = False
        self.raw = source


    def __getitem__(self, index):
        """
        Localiza e retorna um item, no caso um pixel, da imagem.
        :param index Índice ou fatia a ser acessada.
        :return Pixel ou fatia de pixels selecionados.
        """
        return self.raw[index[1], index[0]]
    
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
    def new(cls, shape, dtype = numpy.uint8, channels = 3):
        """
        Cria uma nova imagem totalmente vazia.
        :param shape Formato da imagem.
        :param dtype Tipo de cada elemento da imagem.
        :param channels Número de canais da imagem.
        :return Imagem vazia criada.
        """
        shape = (channels,) + shape if channels > 1 else shape
        blank = numpy.zeros(shape[::-1], dtype)
        return cls(blank)
    
    def resize(self, proportion, min = Point(1,1)):
        """
        Redimensiona a imagem de acordo com a proporção dada.
        Nenhuma distorção ocorrerá durante o processo.
        :param proportion Proporção de redimensionamento da imagem.
        :param min Tamanho mínimo da imagem após redimensionamento.
        :return Imagem redimensionada.
        """
        if self.shape.x * proportion < min.x \
        or self.shape.y * proportion < min.y:
            proportion = max(
                min.x / float(self.shape.x),
                min.y / float(self.shape.y)
            )

        raw = cv.resize(self.raw, None, fx = proportion, fy = proportion)
        return Image(raw)
    
    def binarize(self):
        """
        Transforma a imagem atual em uma imagem binária.
        :return Imagem binária gerada.
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_BGR2GRAY)
        _, raw = cv.threshold(raw, 127, 255, cv.THRESH_BINARY)
        return Image(raw)
    
    def colorize(self):
        """
        Transforma uma imagem binária em uma imagem colorida.
        :return Imagem colorida gerada.
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_GRAY2BGR)
        return Image(raw)
    
    def tolab(self):
        """
        Transforma a imagem atual para o tipo L*a*b*.
        :return Imagem gerada no formato L*a*b*.
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_BGR2LAB)
        return Image(raw)
    
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
            self.raw if not self.inverted else cv.transpose(self.raw)
        )

    def transpose(self):
        """
        Inverte a imagem atual. Assim, as dimensões se inventem
        e é necessário inverter as coordenadas de um ponto para
        resgatar um mesmo pixel da imagem anterior.
        """
        self.shape = self.shape.swap
        self.raw = cv.transpose(self.raw)
        self.inverted = not self.inverted

    def check(self, comps):
        """
        Verifica a necessidade de rotação da imagem e o faz
        de acordo com o verificado.
        :param comps Componentes de verificação de rotação.
        """
        count = 0
        
        for i in xrange(1, 9):
            x, y = zip(*comps[i].points)
            line = numpy.poly1d(numpy.polyfit(x, y, deg = 1))
                
            if abs(line[1]) < 1:
                count += 1

        if not count < 5:
            self.transpose()
            return False

        return True

class ImageWindow(object):
    """
    Classe responsável pela exibição de uma imagem e também
    pelo controle da imagem sobre a janela, permitindo que
    a imagem seja deslocada e toda a imagem seja visível em
    uma tela menor que ela.
    """
    
    def __init__(self, wname, image):
        """
        Inicializa e cria uma nova instância do objeto.
        :param wname Nome da janela a ser criada.
        :param image Imagem a ser exibida.
        :return Instância criada.
        """
        self.size = config.wsize
        self.wname = "{0} #{1}".format(wname, config.wid)
        self.shape = image.shape
        self.closed = False
        self.word = None
        config.wid += 1

        self.image = [image if not image.inverted else Image(cv.transpose(image.raw))]
        self.index = 0

        self._mousep = None
        self.anchor = None
        self.mid = None

        thread = Thread(target = ImageWindow.show, args = (self,))
        thread.start()
            
    def mouse(self, event, x, y, flag, *param):
        """
        Método responsável pelo controle do mouse.
        :param event Evento realizado pelo mouse.
        :param x Coordenadas-x do evento.
        :param y Coordenadas-y do evento.
        :param flag Flags do evento.
        :param param Parâmetros adicionais.
        """
        if event == cv.EVENT_LBUTTONDOWN:
            self._mousep = Point(x, y)
        elif event == cv.EVENT_LBUTTONUP:
            del self._mousep
        elif event == cv.EVENT_MOUSEMOVE and flag & cv.EVENT_FLAG_LBUTTON:       
            _x, _y = self.anchor + (self._mousep - (x, y))
            
            _x = _x if _x > 0 else 0
            _y = _y if _y > 0 else 0
            
            _x = _x if _x <= self.shape.x - self.size[0] else self.shape.x - self.size[0]
            _y = _y if _y <= self.shape.y - self.size[1] else self.shape.y - self.size[1]

            self._mousep = Point(x, y)
            self.anchor  = Point(_x, _y)
            self.frame()
    
    def append(self, image):
        """
        Adiciona uma imagem à lista de imagens a serem exibidas.
        :param image Imagem a ser adiciona à lista.
        """
        self.image.append(image if not image.inverted else Image(cv.transpose(image.raw)))
        self.index = len(self.image) - 1
        self.frame()
        
    def text(self, txt, pos, color = (255, 255, 0)):
        """
        Insere um texto estático na janela.
        :param txt Texto a ser posicionado.
        :param pos Posição do texto.
        :param color Cor do texto.
        """
        pos = tuple([
            (pos[i] if pos[i] >= 0 else self.size[i] + pos[i])
                for i in xrange(2)
        ])
        
        self.word = type('', (object,), {
            'word': txt, 'pos': pos, 'color': color
        })
    
    def show(self):
        """
        Método responsável por gerir a exibição da imagem.
        """
        self.mid = Point(self.shape.x / 2, self.shape.y / 2)
        self.anchor = Point(self.mid.x - self.size[0] / 2, self.mid.y - self.size[1] / 2)
                
        cv.namedWindow(self.wname, cv.WINDOW_AUTOSIZE)
        cv.setMouseCallback(self.wname, self.mouse)
        self.frame()
        
        key = cv.waitKey(10) % 256
    
        while key != 27:
            cv.setMouseCallback(self.wname, self.mouse)
            key = cv.waitKey(10) % 256
            
            if key in [ord('w'), ord('W')]:
                self.index = self.index + 1 if self.index < len(self.image) - 1 else 0
            elif key in [ord('s'), ord('S')]:
                self.index = self.index - 1 if self.index > 0 else len(self.image) - 1

            self.frame()
            
        cv.destroyWindow(self.wname)
        exit()
        
    def frame(self):
        """
        Cria e exibe a imagem da janela.
        """
        wframe = copy.deepcopy(self.image[self.index][
            self.anchor.x : self.anchor.x + self.size[0],
            self.anchor.y : self.anchor.y + self.size[1]            
        ])
        
        if self.word is not None:
            cv.putText(wframe, self.word.word, self.word.pos,
                cv.FONT_HERSHEY_TRIPLEX, 0.7, self.word.color
            )
            
        cv.imshow(self.wname, wframe)