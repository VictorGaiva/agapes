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
from gui.main.canvas import Canvas
import wx

class Window(wx.Frame):
    """
    Objeto responsável pelo posicionamento e controle de elementos
    na janela principal da aplicação.
    """

    def __init__(self, control, title = ''):
        """
        Cria uma nova instância do objeto.
        :param control Controlador da janela principal.
        :param title Título da nova janela.
        :return MainWindow
        """
        wx.Frame.__init__(
            self, None, -1, title,
            size = (600, 460),
            style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        )

        self.control = control
        self.title = title

        self.InitUI()
        self.control.bind(self)

        self.Centre(wx.BOTH)
        self.Show()

    def InitUI(self):
        """
        Constrói e posiciona os elementos utilizados pela janela nos
        locais corretos.
        """
        self.root = wx.Panel(self)
        self.canvas = Canvas(self.root, (584,393))

        wrapper = wx.BoxSizer(wx.VERTICAL)
        wrapper.Add(self.canvas, 0, wx.EXPAND | wx.BOTTOM, 5)
        wrapper.Add(self.InitToolbar(), 0, wx.EXPAND | wx.ALL, -1)

        total = wx.BoxSizer(wx.HORIZONTAL)
        total.Add(wrapper, 1, wx.EXPAND | wx.ALL, 5)

        self.root.SetSizer(total)

    def InitToolbar(self):
        """
        Inicializa a barra de ferramentas da janela de segmentação
        avulsa.
        :return BoxSizer
        """
        self.i_soil = wx.ToggleButton(self.root, -1, "Terra", size = (75, 25))
        self.i_cane = wx.ToggleButton(self.root, -1, "Cana", size = (75, 25))
        self.w_incr = wx.Button(self.root, -1, "Incrementar", size = (75, 25))
        self.w_sobr = wx.Button(self.root, -1, "Sobreescreve", size = (75, 25))
        self.w_test = wx.Button(self.root, -1, "Testar", size = (75, 25))
        self.w_close = wx.Button(self.root, -1, "Finalizar", size = (75, 25))

        root = wx.BoxSizer(wx.HORIZONTAL)
        root.Add(self.i_soil, 0, wx.RIGHT, 3)
        root.Add(self.i_cane, 0)
        root.Add((1,1), 1, wx.EXPAND)
        root.Add(self.w_incr, 0, wx.RIGHT, 3)
        root.Add(self.w_sobr, 0, wx.RIGHT, 3)
        root.Add(self.w_test, 0, wx.RIGHT, 3)
        root.Add(self.w_close, 0, wx.RIGHT)

        return root
