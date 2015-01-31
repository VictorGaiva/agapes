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
from .dropfield import *
import wx

class NotePage(wx.Panel):
    """
    Objeto responsável por inicializar, controlar e administrar uma
    página do notebook.
    """

    def __init__(self, parent, enable = True):
        """
        Cria uma nova instância do objeto.
        :param parent Janela-pai da janela atual.
        :param enable Permitir movimentação da imagem-alvo?
        """
        wx.Panel.__init__(
            self, parent, -1
        )

        self.parent = parent
        self.enable = enable
        self.root = wx.Panel(self, size = (800, 483))

        wrapper = self.Init()
        wrapper.Add(self.InitLeft(), 3, wx.EXPAND | wx.RIGHT, 5)
        wrapper.Add(wx.StaticLine(self.root, style = wx.LI_VERTICAL), 0, wx.EXPAND | wx.RIGHT, 4)
        wrapper.Add(self.InitRight(), 1, wx.EXPAND)

    def Init(self):
        """
        Inicializa a aba com suas principais estruturas. Prepara
        o painel para receber os elementos que o compõe.
        :return BoxSizer
        """
        wrapper = wx.BoxSizer()
        wrapper.Add((2,0), 0)
        wrapper.Add(self.root, 0, wx.RIGHT | wx.TOP, 4)
        self.SetSizer(wrapper)

        root = wx.BoxSizer(wx.HORIZONTAL)
        self.root.SetSizer(root)

        return root

    def InitLeft(self):
        """
        Inicializa os objetos localizados do lado esquerdo da
        aba, com todas as suas estruturas.
        :return BoxSizer
        """
        self.dropfield = DropField(self.root, enable = self.enable)

        root = wx.BoxSizer(wx.VERTICAL)
        root.Add(self.dropfield, 0, wx.EXPAND | wx.BOTTOM, 5)
        root.Add(self.InitTools(), 1, wx.EXPAND)

        return root

    def InitRight(self):
        """
        Inicializa os objetos localizados do lado direito da
        aba, com todas as suas estruturas.
        :return BoxSizer
        """
        self.farm = wx.ComboBox(
            self.root, -1, "", choices = [],
            size = (191, 25),
            style = wx.CB_DROPDOWN
        )

        self.plot = wx.TextCtrl(
            self.root, -1, "",
            size = (191, 25)
        )

        self.dnum = wx.SpinCtrlDouble(
            self.root, -1, initial = 1.50,
            min = .00, max = 50., inc = .25,
            size = (70, 25)
        )

        self.dmtr = wx.Choice(
            self.root, -1,
            choices = [u"centímetros", u"metros", u"polegadas", u"pés", u"jardas"],
            size = (90, 23)
        )

        self.runbt = wx.Button(self.root, -1, "Processar")
        self.clsbt = wx.Button(self.root, -1, "Fechar")

        fazendatx = wx.StaticText(self.root, -1, u"Fazenda:")
        talhoestx = wx.StaticText(self.root, -1, u"Talhão:")
        dslinestx = wx.StaticText(self.root, -1, u"Distância entre linhas:")
        self.dmtr.SetSelection(1)
        self.dnum.SetDigits(2)

        wrapper = wx.GridBagSizer(5,5)
        wrapper.Add((100,100), (0,0), (1,2), wx.EXPAND)
        wrapper.Add(fazendatx, (1,0), (1,2), wx.EXPAND)
        wrapper.Add(self.farm, (2,0), (1,2), wx.EXPAND)
        wrapper.Add(talhoestx, (3,0), (1,2), wx.EXPAND)
        wrapper.Add(self.plot, (4,0), (1,2), wx.EXPAND)
        wrapper.Add(dslinestx, (5,0), (1,2), wx.EXPAND)
        wrapper.Add(self.dnum, (6,0), (1,1), wx.EXPAND)
        wrapper.Add(self.dmtr, (6,1), (1,1), wx.EXPAND)

        wrapper.Add(
            wx.StaticLine(self.root, style = wx.LI_HORIZONTAL),
            (7,0), (1,2), wx.EXPAND | wx.TOP | wx.BOTTOM, 5
        )

        wrapper.Add(self.runbt, (8,0), (1,1), wx.EXPAND)
        wrapper.Add(self.clsbt, (8,1), (1,1), wx.EXPAND)

        root = wx.BoxSizer(wx.VERTICAL)
        root.Add(wrapper, 1, wx.EXPAND)

        return root

    def InitTools(self):
        """
        Inicializa as ferramentas e objetos localizados no
        lado inferior esquerdo da aba.
        :return BoxSizer
        """
        self.sample = wx.SpinCtrl(
            self.root, -1, "", size = (60, 25),
            min = 20, max = 90, initial = 50
        )

        amostratx = wx.StaticText(self.root, -1, "Amostras:")
        porcenttx = wx.StaticText(self.root, -1, "%")

        root = wx.BoxSizer(wx.HORIZONTAL)
        root.Add(amostratx, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        root.Add(self.sample, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        root.Add(porcenttx, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        root.Add((10,10), 1, wx.EXPAND)

        root.AddMany([
            (button, 0, wx.ALIGN_RIGHT | wx.LEFT, 4)
                for button in self.InitPhaseButtons()
        ])

        return root

    def InitPhaseButtons(self):
        """
        Inicializa os botões de visualização de passos do algoritmo,
        localizados na parte inferior central da janela.
        :return list
        """
        self.phase = [
            wx.ToggleButton(self.root, 1, "O", size = (25, 25)),
            wx.ToggleButton(self.root, 2, "S", size = (25, 25)),
            wx.ToggleButton(self.root, 3, "L", size = (25, 25))
        ]

        self.phase[0].SetValue(True)
        self.phase[1].SetValue(False)
        self.phase[2].SetValue(False)

        for i, button in enumerate(self.phase):
            button.Bind(wx.EVT_TOGGLEBUTTON, self.OnPhaseButton)

        return self.phase

    def OnPhaseButton(self, event):
        """
        Método executado em reação ao evento ToggleButton de algum
        dos botões de visualização de passos do algoritmo.
        :param event Dados do evento.
        """
        for button in self.phase:
            button.SetValue(button.GetId() == event.GetId())

        self.dropfield.ShowIndex(event.GetId())
        event.Skip()
