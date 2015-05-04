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
from controller.ui.page.process import Control as Ctrl
from ..canvas import Canvas
from wx import *

class ProcessPage(Panel):
    """
    Páginas responsáveis pela manipulação e
    processamento das imagens-alvo.
    """
    __control__ = Ctrl

    def __init__(self, control, parent, inicial = False):
        """
        Inicializa uma nova instância do objeto.
        :param control Controlador da página.
        :param parent Objeto pai.
        :param inicial Esta é a página inicial?
        :return ReportPage
        """
        Panel.__init__(self, parent, -1)

        self.control = control
        self.inicial = inicial
        self.parent = parent
        self.BuildUI()

        self.control.bind(self)

    def BuildUI(self):
        """
        Constrói a interface gráfica da página.
        :return None
        """
        self.root = Panel(self, size = (800, 483))

        wrapper = self.Init()
        wrapper.Add(self.InitLeft(), 3, EXPAND | RIGHT, 5)
        wrapper.Add(StaticLine(self.root, style= LI_VERTICAL), 0, EXPAND | BOTTOM, -1)
        wrapper.Add(self.InitRight(), 1, EXPAND | LEFT, 4)

    def Init(self):
        """
        Inicializa a página com suas principais estruturas.
        Prepara o painel para receber os elementos que o compõem.
        :return BoxSizer
        """
        wrapper = BoxSizer(HORIZONTAL)
        wrapper.AddSpacer((2,0))
        wrapper.Add(self.root, 0, RIGHT | TOP, 4)
        self.SetSizer(wrapper)

        root = BoxSizer(HORIZONTAL)
        self.root.SetSizer(root)

        return root

    def InitLeft(self):
        """
        Inicializa os objetos localizados no lado esquerdo da
        página, com todas as suas respectivas estruturas.
        :return BoxSizer
        """
        self.canvas = Canvas(self.root, (571, 455))
        self.canvas.SetBackgroundColour(Colour(0x00, 0x00, 0x00))

        root = BoxSizer(VERTICAL)
        root.Add(self.canvas, 1, EXPAND | BOTTOM, 4)
        root.Add(self.InitCanvasTools(), 0, EXPAND)

        return root

    def InitRight(self):
        """
        Inicializa os objetos localizados no lado direito da
        página, com todas as suas respectivas estruturas.
        :return BoxSizer
        """
        root = BoxSizer(VERTICAL)
        root.Add(self.InitResult(), 0, EXPAND | BOTTOM, 15)
        root.Add(self.InitPlotInfo(), 0, EXPAND | BOTTOM, 5)
        root.Add((1,1), 1, EXPAND)
        root.Add(self.InitActionButtons(), 0, EXPAND)

        return root

    def InitCanvasTools(self):
        """
        Inicializa acesso às ferramentas de manipulação do
        canvas de imagem da página.
        :return BoxSizer
        """
        root = BoxSizer(HORIZONTAL)
        root.Add(self.InitSelectionButtons(), 0, BOTTOM, -1)
        root.Add((1,1), 1, EXPAND)
        root.Add(self.InitLayerButtons(), 0, BOTTOM, -1)

        return root

    def InitSelectionButtons(self):
        """
        Inicializa os botões de seleção localizados abaixo
        do canvas de imagem da página.
        :return BoxSizer
        """
        self.s_done = Button(self.root, -1, "OK", size = (40,25))
        self.s_add = Button(self.root, -1, "+", size = (25, 25))
        self.s_del = Button(self.root, -1, "-", size = (25,25))
        self.s_fsg = Button(self.root, -1, "SG", size = (25, 25))
        self.s_txt = StaticText(self.root, -1, "")

        root = BoxSizer(HORIZONTAL)
        root.Add(self.s_done, 0, LEFT, -1)
        root.AddSpacer((4,0))
        root.Add(StaticLine(self.root, style=LI_VERTICAL), 0, EXPAND | TOP, 1)
        root.Add(self.s_add, 0, LEFT | RIGHT, 3)
        root.Add(self.s_del, 0, RIGHT, 4)
        root.Add(StaticLine(self.root, style=LI_VERTICAL), 0, EXPAND | TOP, 1)
        root.Add(self.s_fsg, 0, LEFT, 3)
        root.Add(self.s_txt, 0, LEFT | ALIGN_CENTER_VERTICAL, 6)

        return root

    def InitLayerButtons(self):
        """
        Inicializa os botões de camada localizados abaixo do
        canvas de imagem da página
        :return BoxSizer
        """
        self.l_g = ToggleButton(self.root, 0, "G", size = (40,25))
        self.l_1 = ToggleButton(self.root, 1, "O", size = (25,25))
        self.l_2 = ToggleButton(self.root, 2, "S", size = (25,25))
        self.l_3 = ToggleButton(self.root, 3, "L", size = (25,25))

        root = BoxSizer(HORIZONTAL)
        root.Add(self.l_g, 0, RIGHT, 4)
        root.Add(StaticLine(self.root, style=LI_VERTICAL), 0, EXPAND | TOP, 1)
        root.Add(self.l_1, 0, LEFT | RIGHT, 3)
        root.Add(self.l_2, 0, RIGHT, 3)
        root.Add(self.l_3, 0, RIGHT, -1)

        return root

    def InitResult(self):
        """
        Inicializa os recursos para exibição dos resultados
        calculados pela página.
        :return BoxSizer
        """
        self.r_pcent = StaticText(self.root, -1, "0")
        self.r_pcent.SetFont(Font(45, DEFAULT, NORMAL, NORMAL))
        self.r_patch = StaticText(self.root, -1, "0/0")
        self.r_cmtrs = StaticText(self.root, -1, "0 m")
        self.r_fmtrs = StaticText(self.root, -1, "0 m")

        mainr = BoxSizer(HORIZONTAL)
        mainr.Add((1,1), 1, EXPAND)
        mainr.Add(self.r_pcent, 0, EXPAND | RIGHT, 5)
        mainr.Add(StaticText(self.root, -1, "%\nfalhas"), 0, EXPAND | TOP, 20)
        mainr.Add((1,1), 1, EXPAND)

        other = FlexGridSizer(3, 2,5,5)
        other.AddGrowableCol(0, 2)
        other.Add(StaticText(self.root, -1, u"Retalhos:"), 0, EXPAND)
        other.Add(self.r_patch, 0, ALIGN_RIGHT)
        other.Add(StaticText(self.root, -1, u"Plantação:"), 0, EXPAND)
        other.Add(self.r_cmtrs, 0, ALIGN_RIGHT)
        other.Add(StaticText(self.root, -1, u"Falhas:"), 0, EXPAND)
        other.Add(self.r_fmtrs, 0, ALIGN_RIGHT)

        box = StaticBox(self.root, -1, "  Resultado  ")
        box = StaticBoxSizer(box, VERTICAL)
        box.Add(mainr, 0, EXPAND | TOP | BOTTOM, 10)
        box.Add(other, 0, EXPAND | BOTTOM, 5)

        root = BoxSizer(VERTICAL)
        root.Add(box, 1, EXPAND)
        return root

    def InitPlotInfo(self):
        """
        Inicializa os recursos para informação dos retalhos
        que estão sendo calculados na página.
        :return BoxSizer
        """
        self.i_farm = TextCtrl(self.root, -1, u"")
        self.i_plot = TextCtrl(self.root, -1, u"")
        self.i_dval = SpinCtrlDouble(self.root, -1, initial=1.5, min=.0,max=50., inc=.25, size=(91, 23))
        self.i_dscl = Choice(self.root, -1, choices=[u"centímetros", u"metros", u"polegadas", u"pés", u"jardas"],size=(92, 23))
        self.i_pgrp = CheckBox(self.root, -1, u"Agrupar com outras abas com\nos mesmos identificadores", size=(184,50))
        self.i_pgrp.Disable()

        distsz = BoxSizer(HORIZONTAL)
        distsz.Add(self.i_dval, 0, EXPAND | RIGHT, 5)
        distsz.Add(self.i_dscl, 0, EXPAND)

        root = BoxSizer(VERTICAL)
        root.Add(StaticText(self.root, -1, u"Fazenda:"), 0, EXPAND | BOTTOM, 1)
        root.Add(self.i_farm, 0, EXPAND | BOTTOM, 5)
        root.Add(StaticText(self.root, -1, u"Talhão:"), 0, EXPAND | BOTTOM, 1)
        root.Add(self.i_plot, 0, EXPAND | BOTTOM, 5)
        root.Add(StaticText(self.root, -1, u"Espaçamento:"), 0, EXPAND | BOTTOM, 1)
        root.Add(distsz, 0, EXPAND | BOTTOM, 5)
        root.Add(self.i_pgrp, 0)

        return root

    def InitActionButtons(self):
        """
        Inicializa os botões de ação da página.
        :return BoxSizer
        """
        self.a_run = Button(self.root, -1, "Processar", size = (25,25))
        self.a_stop = Button(self.root, -1, "Finalizar", size = (25,25))

        root = BoxSizer(HORIZONTAL)
        root.Add(self.a_run, 1, ALL | EXPAND, -1)
        root.Add((5, 0), 0)
        root.Add(self.a_stop, 1, ALL | EXPAND, -1)

        return root