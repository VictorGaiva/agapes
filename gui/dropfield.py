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
from .event import *
from . import images
import wx

class DropField(wx.StaticBitmap, wx.FileDropTarget):
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
        self.size = size
        self.parent = parent
        self.imginit = wx.BitmapFromImage(images.drag.init)
        self.imgover = wx.BitmapFromImage(images.drag.over)

        wx.StaticBitmap.__init__(
            self, parent, -1,
            self.imginit,
            size = size
        )

        wx.FileDropTarget.__init__(
            self
        )

        self.SetDropTarget(self)

    def OnEnter(self, *args):
        """
        Método executado em reação ao evento Enter de
        wx.FileDropTarget .
        :return int
        """
        self.SetBitmap(self.imgover)
        self.SetSize(self.size)
        return 1

    def OnLeave(self):
        """
        Método executado em reação ao evento Leave de
        wx.FileDropTarget .
        :return None
        """
        self.SetBitmap(self.imginit)
        self.SetSize(self.size)

    def OnDropFiles(self, x, y, filenames):
        """
        Método executado em reação ao evento DropFiles de
        wx.FileDropTarget .
        :return bool
        """
        self.SetBitmap(self.imginit)
        self.SetSize(self.size)

        Event.get("DropFile").trigger(filenames)
        return True
