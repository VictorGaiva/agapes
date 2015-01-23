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
from .util import *
import os.path as path
import config
import wx

class NotePage(wx.Panel):
    """
    Objeto responsável por inicializar, controlar e administrar uma
    página do notebook.
    """

    def __init__(self, parent):
        """
        Cria uma nova instância do objeto.
        :param parent Janela-pai da janela atual.
        """
        super(NotePage, self).__init__(
            parent, -1
        )

        self.sz, self.el = Factory(HierarchicalJar).createmany(2)

        self.sz.wrap = wx.BoxSizer()
        self.el.wrap = wx.Panel(self, size = (800, 483))

        self.SetSizer(self.sz.wrap)
        self.sz.all = wx.BoxSizer(wx.HORIZONTAL)

        self.sz.wrap.Add((2, 0), 0)
        self.sz.wrap.Add(self.el.wrap, 0, wx.RIGHT | wx.TOP, 4)
        self.el.wrap.SetSizer(self.sz.all)

        self.sz.left = wx.BoxSizer(wx.VERTICAL)
        self.sz.right = wx.BoxSizer(wx.VERTICAL)

        self.sz.all.Add(self.sz.left, 3, wx.EXPAND | wx.RIGHT, 5)
        self.sz.all.Add(wx.StaticLine(self.el.wrap, style = wx.LI_VERTICAL), 0, wx.EXPAND | wx.RIGHT, 4)
        self.sz.all.Add(self.sz.right, 1, wx.EXPAND)

        self.dropfield = wx.StaticBitmap(
            self.el.wrap, -1,
            wx.BitmapFromImage(wx.Image(path.join(config.path, "img", "draghere.png"), wx.BITMAP_TYPE_ANY)),
            size = (100, 453)
        )

        self.sz.tools = wx.BoxSizer(wx.HORIZONTAL)

        self.sz.left.Add(self.dropfield, 0, wx.EXPAND | wx.BOTTOM, 5)
        self.sz.left.Add(self.sz.tools, 1, wx.EXPAND)

        self.sample = wx.SpinCtrl(
            self.el.wrap, -1, "", size = (60, 25),
            min = 20, max = 90, initial = 60
        )

        self.sz.tools.Add(
            wx.StaticText(self.el.wrap, -1, "Amostras:"), 0,
            wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5
        )

        self.sz.tools.Add(self.sample, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.sz.tools.Add(
            wx.StaticText(self.el.wrap, -1, "%"), 0,
            wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5
        )

        self.el.b.imorig = wx.ToggleButton(self.el.wrap, -1, "Orig", size = (25, 25))
        self.el.b.imsegm = wx.ToggleButton(self.el.wrap, -1, "Segment", size = (25, 25))
        self.el.b.imline = wx.ToggleButton(self.el.wrap, -1, "Lined", size = (25, 25))

        self.sz.tools.Add((10,10), 1, wx.EXPAND)
        self.sz.tools.Add(self.el.b.imorig, 0, wx.ALIGN_RIGHT | wx.LEFT, 4)
        self.sz.tools.Add(self.el.b.imsegm, 0, wx.ALIGN_RIGHT | wx.LEFT, 4)
        self.sz.tools.Add(self.el.b.imline, 0, wx.ALIGN_RIGHT | wx.LEFT, 4)

        self.sz.infos = wx.GridBagSizer(5, 5)
        self.sz.right.Add(self.sz.infos, 1, wx.EXPAND)

        self.sz.infos.Add((100,100), (0,0), (1,2), wx.EXPAND)

        self.sz.infos.Add(
            wx.StaticText(self.el.wrap, -1, u"Fazenda:"),
            (1,0), (1,2), wx.EXPAND
        )

        self.el.farm = wx.ComboBox(
            self.el.wrap, -1, "", choices = [],
            size = (191, 25),
            style = wx.CB_DROPDOWN
        )

        self.sz.infos.Add(self.el.farm, (2,0), (1,2), wx.EXPAND)

        self.sz.infos.Add(
            wx.StaticText(self.el.wrap, 1, u"Talhão:"),
            (3,0), (1,2), wx.EXPAND
        )

        self.el.field = wx.TextCtrl(
            self.el.wrap, -1, "",
            size = (191, 25)
        )

        self.sz.infos.Add(self.el.field, (4,0), (1,2), wx.EXPAND)

        self.sz.infos.Add(
            wx.StaticText(self.el.wrap, 1, u"Distância entre linhas:"),
            (5,0), (1,2), wx.EXPAND
        )

        self.el.dist.number = wx.SpinCtrlDouble(
            self.el.wrap, -1, initial = 1.50,
            min = .00, max = 50., inc = .25,
            size = (70, 25)
        )

        self.el.dist.number.SetDigits(2)
        self.sz.infos.Add(self.el.dist.number, (6,0), (1,1), wx.EXPAND)

        self.el.dist.type = wx.Choice(
            self.el.wrap, -1,
            choices = [u"centímetros", u"metros", u"polegadas", u"pés", u"jardas"],
            size = (90, 23)
        )

        self.el.dist.type.SetSelection(1)
        self.sz.infos.Add(self.el.dist.type, (6,1), (1,1), wx.EXPAND)

        self.sz.infos.Add(
            wx.StaticLine(self.el.wrap, style = wx.LI_HORIZONTAL),
            (7,0), (1,2), wx.EXPAND | wx.TOP | wx.BOTTOM, 5
        )

        self.el.b.run = wx.Button(self.el.wrap, -1, "Processar")
        self.el.b.dlt = wx.Button(self.el.wrap, -1, "Fechar")

        self.sz.infos.Add(self.el.b.run, (8,0), (1,1), wx.EXPAND)
        self.sz.infos.Add(self.el.b.dlt, (8,1), (1,1), wx.EXPAND)
