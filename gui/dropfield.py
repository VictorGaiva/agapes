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
from core.point import *
from .event import PostEvent
from . import images
import time
import wx

class DropField(wx.Panel, wx.FileDropTarget):
    """
    Objeto responsável pela criação, administração de
    campos de drag and drop.
    """

    def __init__(self, parent, size = (568, 453)):
        """
        Cria uma nova instância do objeto.
        :param parent Janela-pai da janela atual.
        :param size Tamanho a ser ocupado pelo widget.
        """
        self.size = Point(*size)
        self.parent = parent

        wx.Panel.__init__(
            self, parent, -1,
            size = size
        )

        wx.FileDropTarget.__init__(
            self
        )

        self.imglist = [[wx.BitmapFromImage(images.drag.init)]]
        self.imgover = wx.BitmapFromImage(images.drag.over)
        self.imgindex = 0

        self.mousepos = None
        self.click = False
        self.hover = False

        self.bmp = self.imglist[self.imgindex][0]
        self.pos = Point(0,0)

        self.SetDropTarget(self)
        self.BindEvents()

    def BindEvents(self):
        """
        Víncula métodos do objeto a eventos que podem ser disparados.
        :return None
        """
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def AppendImage(self, img, width, height):
        """
        Adiciona uma imagem à lista de imagens para exibição.
        :param img Imagem a ser adicionada.
        :param width Largura da imagem a ser adicionada.
        :param height Largura da imagem a ser adicionada.
        """
        self.imglist.append([wx.BitmapFromBuffer(width, height, img), Point(width, height)])
        self.imgindex = self.imgindex + 1

        if not self.hover:
            self.bmp = self.imglist[self.imgindex][0]

        self.Refresh()

    def OnMouseDown(self, event):
        """
        Método executado em reação ao evento MouseLeftDown.
        :return None
        """
        self.mousepos = Point(event.GetX(), event.GetY())
        self.click = True
        event.Skip()

    def OnMouseUp(self, event):
        """
        Método executado em reação ao evento MouseLeftUp.
        :return None
        """
        self.mousepos = None
        self.click = False

    def OnMotion(self, event):
        """
        Método executado em reação ao evento MouseMotion.
        :return None
        """
        if self.click:
            actual = Point(event.GetX(), event.GetY())
            diff = actual - self.mousepos
            self.mousepos = actual
            self.pos = self.pos + diff

            if self.pos.x > 0:
                self.pos.x = 0
            elif -self.pos.x > self.imglist[self.imgindex][1].x - self.size.x:
                self.pos.x = -(self.imglist[self.imgindex][1].x - self.size.x)

            if self.pos.y > 0:
                self.pos.y = 0
            elif -self.pos.y > self.imglist[self.imgindex][1].y - self.size.y:
                self.pos.y = -(self.imglist[self.imgindex][1].y - self.size.y)

            self.Refresh()

    def OnPaint(self, *args):
        """
        Método executado em reação ao evento OnPaint.
        :return None
        """
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, *self.pos if not self.hover else (0,0))

    def OnEnter(self, *args):
        """
        Método executado em reação ao evento Enter de
        wx.FileDropTarget .
        :return int
        """
        self.hover = True
        self.bmp = self.imgover
        self.Refresh()

        return 1

    def OnLeave(self):
        """
        Método executado em reação ao evento Leave de
        wx.FileDropTarget .
        :return None
        """
        self.hover = False
        self.bmp = self.imglist[self.imgindex][0]
        self.Refresh()

    def OnDropFiles(self, x, y, filenames):
        """
        Método executado em reação ao evento DropFiles de
        wx.FileDropTarget .
        :return bool
        """
        self.hover = False
        self.bmp = self.imglist[self.imgindex][0]
        self.Refresh()

        PostEvent("DropFiles", filenames)

        return True
