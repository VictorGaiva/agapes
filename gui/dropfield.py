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
from core.patch import PatchWork
from core.image import Image
from core.point import *
from .event import PostEvent
from . import image

from copy import deepcopy
import wx

class DropField(wx.Panel, wx.FileDropTarget):
    """
    Objeto responsável pela criação, administração de
    campos de drag and drop.
    """

    class ImageElement(object):
        """
        Objeto responsável por armazenar um elemento
        da lista de imagens.
        """

        def __init__(self, bitmap, shape = (0,0)):
            """
            Cria uma nova instância do objeto.
            :param bitmap Imagem bitmap a ser adicionada à lista.
            :param shape Tamanho da imagem a ser adicionada.
            :return ImageElement
            """
            self.bitmap = bitmap
            self.shape = Point(*shape)

        @classmethod
        def FromImage(cls, image):
            """
            Cria uma nova instância a partir de um objeto
            de imagem.
            :param image Imagem a ser transformada em bitmap.
            :return ImageElement
            """
            bitmap = wx.BitmapFromImage(image)
            return cls(bitmap)

        @classmethod
        def FromBuffer(cls, buf, width, height):
            """
            Cria uma nova instância a partir de um objeto
            de imagem.
            :param buf Buffer a ser transformado em bitmap.
            :param width Largura dos dados contidos no buffer.
            :param height Altura dos dados contidos no buffer.
            :return ImageElement
            """
            bitmap = wx.BitmapFromBuffer(width, height, buf)
            return cls(bitmap, (width, height))

    def __init__(self, parent, size = (568, 453), enable = True):
        """
        Cria uma nova instância do objeto.
        :param parent Janela-pai da janela atual.
        :param size Tamanho a ser ocupado pelo widget.
        :param enable Permite movimento da imagem com mouse?
        """
        self.size = Point(*size)
        self.parent = parent
        self.enable = enable

        wx.Panel.__init__(
            self, parent, -1,
            size = size
        )

        wx.FileDropTarget.__init__(
            self
        )

        self.iover =  self.ImageElement.FromImage(image.drag.over)
        self.ilist = [self.ImageElement.FromImage(image.drag.init)]
        self.original = []
        self.index = 0

        self.mousepos = None
        self.hover = False

        self.bmp = self.ilist[self.index].bitmap
        self.pos = Point(0,0)

        self.SetBackgroundColour("#CCCCCC")
        self.SetDropTarget(self)
        self.BindEvents()

    def SetImage(self, img, width, height):
        """
        Adiciona uma imagem à lista de imagens para exibição.
        :param img Imagem a ser adicionada.
        :param width Largura da imagem a ser adicionada.
        :param height Largura da imagem a ser adicionada.
        """
        self.ilist.extend([
            DropField.ImageElement.FromBuffer(img, width, height),
            DropField.ImageElement.FromBuffer(img, width, height),
            DropField.ImageElement.FromBuffer(img, width, height),
        ])

        self.original = [
            PatchWork(Image(deepcopy(img)), 200, 200),
            PatchWork(Image(deepcopy(img)), 200, 200),
        ]

        self.bmp = self.ilist[1].bitmap \
            if not self.hover else self.iover.bitmap

        self.index = 1
        self.Refresh()

    def ChangeImage(self, index, img, width, height):
        """
        Modifica a imagem presente em um dos índices da lista
        de imagens para exibição.
        :param index Índice alvo para da mudança.
        :param img Imagem a ser adiciona na posição da anterior.
        :param width Largura da imagem a ser adicionada.
        :param height Largura da imagem a ser adicionada.
        """
        self.ilist[index] = \
            DropField.ImageElement.FromBuffer(img, width, height)

        self.bmp = self.ilist[index].bitmap \
            if self.index == index and not self.hover else self.bmp

        self.Refresh()

    def ShowIndex(self, sid):
        """
        Muda a imagem a ser exibida.
        :param sid Índice da imagem a ser mostrada.
        """
        self.index = sid if sid < len(self.ilist) else self.index
        self.bmp = self.ilist[self.index].bitmap

        self.Refresh()

    def BindEvents(self):
        """
        Víncula métodos do objeto a eventos que podem ser disparados.
        :return None
        """
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnEnter(self, *args):
        """
        Método executado em reação ao evento Enter de
        wx.FileDropTarget .
        :return int
        """
        self.hover = True
        self.bmp = self.iover.bitmap
        self.Refresh()

        PostEvent("PushStatus", u'Solte a imagem e clique em "Processar" para processá-la.')

        return 1

    def OnDropFiles(self, x, y, filenames):
        """
        Método executado em reação ao evento DropFiles de
        wx.FileDropTarget .
        :return bool
        """
        self.hover = False
        self.bmp = self.ilist[self.index].bitmap
        self.Refresh()

        PostEvent("PopStatus")
        PostEvent("DropFiles", filenames)

        return True

    def OnLeave(self):
        """
        Método executado em reação ao evento Leave de
        wx.FileDropTarget .
        :return None
        """
        self.hover = False
        self.bmp = self.ilist[self.index].bitmap
        self.Refresh()

        PostEvent("PopStatus")

    def OnMouseDown(self, event):
        """
        Método executado em reação ao evento MouseLeftDown.
        :return None
        """
        self.mousepos = Point(event.GetX(), event.GetY())
        event.Skip()

    def OnMouseUp(self, event):
        """
        Método executado em reação ao evento MouseLeftUp.
        :return None
        """
        self.mousepos = None

    def OnMotion(self, event):
        """
        Método executado em reação ao evento MouseMotion.
        :return None
        """
        if self.enable and self.mousepos is not None:
            shape = self.ilist[self.index].shape
            actual = Point(event.GetX(), event.GetY())
            _x, _y = self.pos + (actual - self.mousepos)

            _x = 0 if _x > 0 else _x
            _y = 0 if _y > 0 else _y

            _x = self.size.x - shape.x if -_x > shape.x - self.size.x else _x
            _y = self.size.y - shape.y if -_y > shape.y - self.size.y else _y

            self.mousepos = actual
            self.pos = Point(_x, _y)
            self.Refresh()

    def OnPaint(self, *args):
        """
        Método executado em reação ao evento OnPaint.
        :return None
        """
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, *self.pos if not self.hover else (0,0))
