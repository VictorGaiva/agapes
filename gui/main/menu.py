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
import wx

class Menu(wx.MenuBar):
    """
    Objeto responsável pela criação, controle e administração
    da barra de menus da aplicação.
    """

    def __init__(self, parent):
        """
        Cria uma nova instância do objeto.
        :param parent Janela-pai da janela atual.
        :return Menu
        """
        wx.MenuBar.__init__(self)

        self.parent = parent
        self.file = wx.Menu()
        self.quit = self.file.Append(wx.ID_EXIT, u"Sair", u"Sair da aplicação")

        self.Append(self.file, u"&Arquivo")

        parent.SetMenuBar(self)
