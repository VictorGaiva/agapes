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

    def __init__(self, control):
        """
        Cria uma nova instância do objeto.
        :param control Objeto de controle de execução.
        """
        self.control = control
        wx.App.__init__(self)

    def OnInit(self):
        """
        Inicializa exibição da GUI.
        :return None
        """
        self.main = MainWindow(self.control, -1, config.appname)
        self.control.bind(self.main)
        self.SetTopWindow(self.main)

        return True
