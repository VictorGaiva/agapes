#!/usr/bin/python
# -*- encoding: utf-8 -*-
from threading import Thread
from point import *
import cv2 as cv
import numpy

class Image(object):
    """
    Protege e intermedia todas as interações com a imagem
    aberta. Também analiza e aplica quaisquer alterações
    requisitadas a uma das versões da imagem.
    """
    
    def __init__(self, source):
        """
        Inicializa e cria uma nova instância do objeto.
        @param ndarray source Imagem alvo do objeto.
        @return Image Nova instância do objeto
        """
        self.shape = Point(*source.shape[:2]).inverse
        self.raw = source
    
    def __getitem__(self, index):
        """
        Localiza e retorna um item, no caso um pixel, da imagem.
        @param tuple|slice index Índice a ser acessado.
        @return int|list Item ou itens selecionados.
        """
        return self.raw[index[1], index[0]]
    
    @classmethod
    def load(cls, filename):
        """
        Carrega a imagem a partir de um arquivo e a transforma
        em um novo objeto Image.
        @param str filename Nome do arquivo da imagem alvo.
        @return Image
        """
        raw = cv.imread(filename)
        return cls(raw)
    
    @classmethod
    def new(cls, shape, dtype = numpy.uint8, channels = 3):
        """
        Cria uma nova imagem totalmente vazia.
        @param tuple shape Formato da imagem.
        @param dtype dtype Tipo de cada elemento da imagem.
        @param int channels Número de canais da imagem.
        @return Image Imagem vazia criada.
        """
        shape = (channels,) + shape if channels > 1 else shape
        blank = numpy.zeros(shape[::-1], dtype)
        return cls(blank)
    
    def resize(self, proportion):
        """
        Redimensiona a imagem de acordo com a proporção dada.
        Nenhuma distorção ocorrerá durante o processo.
        @return Imagem Imagem redimensionada.
        """
        raw = cv.resize(self.raw, None, fx = proportion, fy = proportion)
        return Image(raw)
    
    def binarize(self):
        """
        Transforma a imagem atual em uma imagem binária.
        @return Image A nova imagem gerada.
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_BGR2GRAY)
        _, raw = cv.threshold(raw, 127, 255, cv.THRESH_BINARY)
        return Image(raw)
    
    def colorize(self):
        """
        Transforma uma imagem binária em uma imagem colorida.
        @return Image A nova imagem gerada.
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_GRAY2BGR)
        return Image(raw)
    
    def tolab(self):
        """
        Transforma a imagem atual para o tipo L*a*b*.
        @return Image A nova imagem gerada.
        """
        raw = cv.cvtColor(self.raw, cv.COLOR_BGR2LAB)
        return Image(raw)
    
    def show(self, wname = "image"):
        """
        Mostra a imagem armazenada pelo objeto e espera até que
        um botão seja apertado ou a janela seja fechada.
        @param str window Nome da janela a ser aberta
        @return int Botão pressionado.
        """
        ImageWindow(wname, self)
    
    def save(self, filename = "image.png"):
        """
        Salva a imagem atual em um arquivo.
        @param filename Nome do arquivo a ser criado.
        """
        cv.imwrite(filename, self.raw)
        
class ImageWindow(object):
    """
    Classe responsável pela exibição de uma imagem e também
    pelo controle da imagem sobre a janela, permitindo que
    a imagem seja deslocada e toda a imagem seja visível em
    uma tela menor que ela.
    """
    
    def __init__(self, wname, image, wsize = (800, 600)):
        """
        Inicializa e cria uma nova instância do objeto.
        @param str wname Nome da janela a ser criada.
        @param Image image Imagem a ser exibida.
        @return ImageWindow
        """
        self.size   = wsize
        self.wname  = wname
        self.image  = image
        self.shape = image.shape
        self.closed = False
                
        thread = Thread(target = ImageWindow.show, args = (self,))
        thread.start()
            
    def mouse(self, event, x, y, flag, *param):
        """
        Método responsável pelo controle do mouse.
        @param int event Evento realizado pelo mouse.
        @param int x, y Coordenadas do evento.
        @param int flag Flags do evento.
        @param list param Parâmetros adicionais.
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
            
            cv.imshow(self.wname, self.image[
                self.anchor.x : self.anchor.x + self.size[0],
                self.anchor.y : self.anchor.y + self.size[1]                
            ])
    
    def show(self):
        self.mid = Point(self.shape.x / 2, self.shape.y / 2)
        self.anchor = Point(self.mid.x - self.size[0] / 2, self.mid.y - self.size[1] / 2)
                
        cv.namedWindow(self.wname, cv.WINDOW_AUTOSIZE)
        cv.setMouseCallback(self.wname, self.mouse)

        cv.imshow(self.wname, self.image[
            self.anchor.x : self.anchor.x + self.size[0],
            self.anchor.y : self.anchor.y + self.size[1]
        ])
                
        while cv.waitKey(10) % 256 != 27:
            pass
            
        cv.destroyWindow(self.wname)
        exit()