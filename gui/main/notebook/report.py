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
from controller.ui.page.report import Control
import wx

class ReportPage(wx.Panel):
    """
    Página responsável pela geração e gerenciamento
    do relatório final apresentado pelo software.
    """
    __control__ = Control

    def __init__(self, control, parent, _):
        """
        Inicializa uma nova instância do objeto.
        :param control Controlador da página.
        :param parent Objeto pai.
        :return ReportPage
        """
        wx.Panel.__init__(self, parent, -1)

        self.control = control
        self.parent = parent

        self.control.bind(self)