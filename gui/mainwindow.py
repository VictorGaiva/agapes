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
from .statusbar import *
from .notepage import *
from .menu import *

import config
import wx

class MainWindow(wx.Frame):
    """
    Objeto responsável pelo posicionamento e controle de elementos
    na janela principal da aplicação.
    """

    def __init__(self, control, wid = wx.ID_ANY, title = ''):
        """
        Cria uma nova instância do objeto.
        :param control Objeto de controle de execução.
        :param wid Identificador da nova janela a ser criada.
        :param title Título da nova janela.
        """
        self.control = control
        self.title = title

        wx.Frame.__init__(
            self, None, wid, title,
            size = config.wsize,
            style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        )

        self.InitUI()
        self.menu = Menu(self)
        self.status = StatusBar(self)

        self.Centre(wx.BOTH)
        self.Show()

    def InitUI(self):
        """
        Constrói e posiciona os elementos utilizados pela janela nos
        locais corretos.
        """
        self.root = wx.Panel(self)
        self.book = wx.Notebook(self.root, -1, style = wx.BK_TOP | wx.NB_MULTILINE)
        self.control.book = self.book

        wrapper = wx.BoxSizer()
        wrapper.Add(self.book, 1, wx.EXPAND | wx.ALL, 5)
        self.root.SetSizer(wrapper)

        self.book.AddPage(NotePage(self.book), u"Planilha")
        self.book.AddPage(NotePage(self.book, False), u"Talhões")
        LinkEvent(self.book, wx.EVT_NOTEBOOK_PAGE_CHANGED, "PageChanged")

        self.book.ChangeSelection(1)

    def OnQuit(self, *args):
        """
        Método a ser executado quando o programa estiver sendo fechado.
        :return None
        """
        self.Close()
