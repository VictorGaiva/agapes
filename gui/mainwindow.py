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
from .notepage import *
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
        super(MainWindow, self).__init__(
            parent, wid, title,
            size = config.wsize,
            style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        )

        self.InitMenu()
        self.InitUI()
        self.InitStatus()

        self.Centre(wx.BOTH)
        self.Show()

    def InitMenu(self):
        """
        Constrói e prosiciona o menu de ferramentas na janela.
        :return None
        """
        w_menu = wx.MenuBar()

        w_menu.file = wx.Menu()
        m_quit = w_menu.file.Append(wx.ID_EXIT, u'Sair', u'Sair da aplicação.')

        w_menu.Append(w_menu.file, u'&Arquivo')

        self.Bind(wx.EVT_MENU, self.OnQuit, m_quit)

        self.SetMenuBar(w_menu)

    def InitUI(self):
        """
        Constrói e posiciona os elementos utilizados pela janela nos locais
        corretos.
        :return None
        """
        w_box_root = wx.Panel(self)
        w_notebook = wx.Notebook(w_box_root, -1, style = wx.BK_TOP | wx.NB_MULTILINE)

        w_sizer_wrap = wx.BoxSizer()
        w_sizer_wrap.Add(w_notebook, 1, wx.EXPAND | wx.ALL, 5)
        w_box_root.SetSizer(w_sizer_wrap)

        w_notebook.AddPage(NotePage(w_notebook), u"Planilha")
        w_notebook.AddPage(NotePage(w_notebook), u"Talhões")

        w_notebook.ChangeSelection(1)

    def InitStatus(self):
        """
        Inicializa a barra de status da janela atual.
        :return None
        """
        w_status = self.CreateStatusBar(
            2,
            wx.STB_SHOW_TIPS | wx.STB_ELLIPSIZE_END | wx.ST_SIZEGRIP
        )

        w_status.SetFieldsCount(1)
        w_status.PushStatusText(u"Carregamento concluído.", 0)

    def OnQuit(self, event):
        """
        Método a ser chamado quando o programa estiver sendo fechado.
        :param event Dados sobre o evento engatilhado.
        :return None
        """
        self.Close()
