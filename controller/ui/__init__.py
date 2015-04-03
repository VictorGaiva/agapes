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
from .mainevents import OnImageLoaded, OnImageProcessed, OnImageSegmented
from .generalcontrol import GeneralControl
from gui import Init as Start

def Init(args):
    """
    Inicializa a execução da interface gráfica de usuário.
    Dessa forma, precisamos aguardar pelo usuário para que
    algum processamento inicie.
    :param args Argumentos passados pela linha de comando.
    """
    control = GeneralControl()
    Start(control)