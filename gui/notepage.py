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
from .event import LinkEvent
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

        self.lock = None
        self.comm = None
        self.patch = None
        self.path = None

        self.parent = parent
        self.enable = enable
        self.root = wx.Panel(self, size = (800, 483))

        wrapper = self.Init()
        wrapper.Add(self.InitLeft(), 3, wx.EXPAND | wx.RIGHT, 5)
        wrapper.Add(wx.StaticLine(self.root, style = wx.LI_VERTICAL), 0, wx.EXPAND | wx.RIGHT, 4)
        wrapper.Add(self.InitRight(), 1, wx.EXPAND)

    @classmethod
    def FromActive(cls, parent):
        """
        Cria uma nova página baseada na página ativada. Esse
        método copia todos os campos da página ativada do
        Notebook dado.
        :param parent Notebook a servir como base.
        :return NotePage
        """
        npg = cls(parent)
        opg = parent.GetCurrentPage()

        npg.farm.SetValue(opg.farm.GetValue())
        npg.plot.SetValue(opg.plot.GetValue())
        npg.dnum.SetValue(opg.dnum.GetValue())
        npg.dmtr.SetSelection(opg.dmtr.GetSelection())
        #npg.sample.SetValue(opg.sample.GetValue())

        return npg

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
        self.drop = DropField(self.root, self, not self.enable)

        root = wx.BoxSizer(wx.VERTICAL)
        root.Add(self.drop, 1, wx.EXPAND | wx.BOTTOM, 5)
        root.Add(self.InitTools(), 0, wx.EXPAND)

        return root

    def InitTools(self):
        """
        Inicializa as ferramentas e objetos localizados no
        lado inferior esquerdo da aba.
        :return BoxSizer
        """
        #self.sample = wx.SpinCtrl(
        #    self.root, -1, "", size = (60, 25),
        #    min = 20, max = 90, initial = 50
        #)
        #
        #amostratx = wx.StaticText(self.root, -1, "Amostras:")
        #porcenttx = wx.StaticText(self.root, -1, "%")

        root = wx.BoxSizer(wx.HORIZONTAL)
        #root.Add(amostratx, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        #root.Add(self.sample, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        #root.Add(porcenttx, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        root.Add(self.InitSelectionButtons(), 0, wx.ALIGN_RIGHT)
        root.Add((10,10), 1, wx.EXPAND)
        root.Add(self.InitPhaseButtons(), 0, wx.ALIGN_RIGHT)

        return root

    def InitSelectionButtons(self):
        """
        Inicializa os botões de controle de seleção e ferramentas
        a serem utilizadas.
        :return BoxSizer
        """
        self.sokay = wx.Button(self.root, -1, "OK", size = (25,25))
        self.sadd = wx.Button(self.root, -1, "+", size = (25, 25))
        self.sremove = wx.Button(self.root, -1, "-", size = (25,25))
        self.sseg = wx.Button(self.root, -1, "SG", size = (25, 25))
        self.stxt = wx.StaticText(self.root, -1, "")

        self.sokay.Disable()
        self.sadd.Disable()
        self.sremove.Disable()
        self.sseg.Disable()

        LinkEvent(self.sokay, wx.EVT_BUTTON, "ButtonSOK", (self,))
        LinkEvent(self.sadd, wx.EVT_BUTTON, "ButtonSAdd", (self,))
        LinkEvent(self.sremove, wx.EVT_BUTTON, "ButtonSRemove", (self,))
        LinkEvent(self.sseg, wx.EVT_BUTTON, "ButtonSSegment", (self,))

        root = wx.BoxSizer(wx.HORIZONTAL)
        root.Add(self.sokay, 0, wx.RIGHT, 4)
        root.Add(wx.StaticLine(self.root, style = wx.LI_VERTICAL), 0, wx.EXPAND)
        root.Add(self.sadd, 0, wx.LEFT, 4)
        root.Add(self.sremove, 0, wx.RIGHT | wx.LEFT, 4)
        root.Add(wx.StaticLine(self.root, style = wx.LI_VERTICAL), 0, wx.EXPAND)
        root.Add(self.sseg, 0, wx.LEFT, 4)
        root.Add(self.stxt, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 6)

        return root

    def InitPhaseButtons(self):
        """
        Inicializa os botões de visualização de passos do algoritmo,
        localizados na parte inferior central da janela.
        :return BoxSizer
        """
        self.phase = [
            wx.ToggleButton(self.root, 1, "O", size = (25, 25)),
            wx.ToggleButton(self.root, 2, "S", size = (25, 25)),
            wx.ToggleButton(self.root, 3, "L", size = (25, 25))
        ]

        self.phase[0].SetValue(False)
        self.phase[1].SetValue(False)
        self.phase[2].SetValue(True and self.enable)

        self.bgrid = wx.ToggleButton(self.root, 0, "G", size = (25,25))
        LinkEvent(self.bgrid, wx.EVT_TOGGLEBUTTON, "GridButton")
        self.bgrid.Enable(self.enable)

        root = wx.BoxSizer(wx.HORIZONTAL)
        root.Add(self.bgrid, 0, wx.RIGHT, 4)
        root.Add(wx.StaticLine(self.root, style = wx.LI_VERTICAL), 0, wx.EXPAND)

        for button in self.phase:
            button.Enable(self.enable)
            root.Add(button, 0, wx.LEFT, 4)
            LinkEvent(button, wx.EVT_TOGGLEBUTTON, "PhaseButton")

        return root

    def InitRight(self):
        """
        Inicializa os objetos localizados do lado direito da
        aba, com todas as suas estruturas.
        :return BoxSizer
        """
        self.result = wx.StaticText(self.root, -1, u"0.0%")
        self.count = wx.StaticText(self.root, -1, u"0 amostras")

        root = wx.BoxSizer(wx.VERTICAL)
        root.Add(self.result, 0, wx.EXPAND | wx.BOTTOM, 5)
        root.Add(self.count, 0, wx.EXPAND | wx.BOTTOM, 5)
        root.Add(self.InitClientInfo(), 0, wx.EXPAND | wx.BOTTOM, 5)
        root.Add(self.InitDistance(), 0, wx.EXPAND)
        root.Add(wx.StaticLine(self.root, style=wx.LI_HORIZONTAL), 0, wx.EXPAND | wx.TOP, 6)
        root.Add(self.InitActionButtons(), 0, wx.EXPAND | wx.TOP, 5)

        return root

    def InitClientInfo(self):
        """
        Inicializa os campos de informação e identificação
        do cliente.
        :return BoxSizer
        """
        self.farm = wx.ComboBox(
            self.root, -1, "", choices = [], size = (191, 25),
            style = wx.CB_DROPDOWN
        )

        self.plot = wx.TextCtrl(
            self.root, -1, "",
            size = (191, 25)
        )

        root = wx.BoxSizer(wx.VERTICAL)
        root.Add(wx.StaticText(self.root, -1, u"Fazenda:"), 0, wx.EXPAND | wx.BOTTOM, 5)
        root.Add(self.farm, 0, wx.EXPAND | wx.BOTTOM, 5)
        root.Add(wx.StaticText(self.root, -1, u"Talhão:"), 0, wx.EXPAND | wx.BOTTOM, 5)
        root.Add(self.plot, 0, wx.EXPAND)

        return root

    def InitDistance(self):
        """
        Inicializa campos de informação sobre a distância
        entre as linhas de plantação de cana-de-açúcar.
        :return BoxSizer
        """
        self.dnum = wx.SpinCtrlDouble(
            self.root, -1, initial = 1.50, min = .00, max = 50., inc = .25,
            size = (70, 23)
        )

        self.dmtr = wx.Choice(
            self.root, -1, size = (90, 23),
            choices = [u"centímetros", u"metros", u"polegadas", u"pés", u"jardas"],
        )

        self.dmtr.SetSelection(1)
        self.dnum.SetDigits(2)

        wrapper = wx.BoxSizer(wx.HORIZONTAL)
        wrapper.Add(self.dnum, 1, wx.RIGHT, 5)
        wrapper.Add(self.dmtr, 1)

        root = wx.BoxSizer(wx.VERTICAL)
        root.Add(wx.StaticText(self.root, -1, u"Distância entre linhas:"), 0, wx.EXPAND)
        root.Add(wrapper, 0, wx.EXPAND | wx.TOP, 5)

        return root

    def InitActionButtons(self):
        """
        Inicializa os botões de ação da página. Esses botões
        são responsáveis pelo controle de execução e fechamento
        da página atual.
        :return BoxSizer
        """
        self.btrun = wx.Button(self.root, -1, "Processar")
        self.btcls = wx.Button(self.root, -1, "Fechar")

        LinkEvent(self.btrun, wx.EVT_BUTTON, "RunPage")
        LinkEvent(self.btcls, wx.EVT_BUTTON, "ClosePage")

        root = wx.BoxSizer(wx.HORIZONTAL)
        root.Add(self.btrun, 1, wx.RIGHT, 5)
        root.Add(self.btcls, 1)

        return root
