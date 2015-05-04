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
from . import Control as BaseControl

class Control(BaseControl):
    """
    Controla e administra a execução de uma
    página de relatório da interface gráfica
    através dos eventos disparados.
    """

    def __init__(self, parent, *args):
        """
        Inicializa uma nova instância.
        :param parent Controlador superior na hierarquia.
        :return Control
        """
        BaseControl.__init__(self, parent)
