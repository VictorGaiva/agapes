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
from .statusbar import *
from .notepage import *
from .menu import *

import controller
import config
import wx

class MainWindow(wx.Frame):
    """
    Objeto responsável pelo posicionamento e controle de elementos
    na janela principal da aplicação.
    """

    def __init__(self, parent, wid = wx.ID_ANY, title = ''):
        """
        Cria uma nova instância do objeto.
        :param parent Janela-pai da janela atual.
        :param wid Identificador da nova janela a ser criada.
        :param title Título da nova janela.
        """
        wx.Frame.__init__(
            self, parent, wid, title,
            size = config.wsize,
            style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        )

        self.InitUI()
        self.menu = Menu(self)
        self.status = StatusBar(self)

        self.Centre(wx.BOTH)
        self.Show()

        self.BindEvents()

    def InitUI(self):
        """
        Constrói e posiciona os elementos utilizados pela janela nos locais
        corretos.
        :return None
        """
        self.root = wx.Panel(self)
        self.nbook = wx.Notebook(self.root, -1, style = wx.BK_TOP | wx.NB_MULTILINE)

        wrapper = wx.BoxSizer()
        wrapper.Add(self.nbook, 1, wx.EXPAND | wx.ALL, 5)
        self.root.SetSizer(wrapper)

        self.nbook.AddPage(NotePage(self.nbook), u"Planilha")
        self.nbook.AddPage(NotePage(self.nbook), u"Talhões")
        self.nbook.ChangeSelection(1)

    def OnQuit(self, *args):
        """
        Método a ser executado quando o programa estiver sendo fechado.
        :return None
        """
        self.Close()

    def OnDropFiles(self, filenames):
        """
        Método executado assim que o evento DropFiles é disparado.
        Este método cria uma nova aba e permite que uma imagem
        seja processada.
        :return None
        """
        for filename in filenames:
            newpage = NotePage(self.nbook)
            controller.ExecutePage(newpage, filename)

            self.nbook.AddPage(newpage, "#{0}".format(config.wid))
            config.wid = config.wid + 1

    def BindEvents(self):
        """
        Víncula métodos do objeto a eventos que podem ser disparados.
        :return None
        """
        BindEvent("DropFiles", self.OnDropFiles)