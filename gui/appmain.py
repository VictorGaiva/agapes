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
from .mainwindow import *
import config
import wx

class AppMain(wx.App):
    """
    Objeto responsável pela criação e coordenação geral das
    ações aplicadas por e realizadas sobre a janela.
    """

    def OnInit(self):
        """
        Inicializa exibição da GUI.
        :return None
        """
        self.main = MainWindow(None, -1, config.appname)
        self.SetTopWindow(self.main)

        return True
