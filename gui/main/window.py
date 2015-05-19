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
from .notebook import Notebook
from .notebook.report import ReportPage
from .notebook.process import ProcessPage
from .statusbar import StatusBar
from .menu import Menu
import config
import wx

class MainWindow(wx.Frame):
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
            size = config.wsize,
            style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        )

        self.control = control
        self.title = title

        self.InitUI()
        self.Centre(wx.BOTH)
        self.Show()

    def InitUI(self):
        """
        Constrói e posiciona os elementos utilizados pela janela nos
        locais corretos.
        """
        self.root = wx.Panel(self)
        self.book = Notebook(self, style = wx.BK_TOP | wx.NB_MULTILINE)

        wrapper = wx.BoxSizer()
        wrapper.Add(self.book, 1, wx.EXPAND | wx.ALL, 5)

        self.root.SetSizer(wrapper)

        self.book.add(ReportPage, u"Planilha")
        self.book.add(ProcessPage, u"Processar", True)
        self.book.ChangeSelection(1)

        self.menu = Menu(self)
        self.status = StatusBar(self)
