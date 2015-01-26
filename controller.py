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
from gui import InitGUI
from core.image import ImageWindow
from core import *
import config

def ExecuteCommandLine(address, distance):
    """
    Executar o programa a partir da linha de comando, permitindo
    assim, o uso em plataformas diferenciadas onde a GUI não
    está disponível ou é incopatível.
    :param address Endereço da imagem alvo do processamento.
    :param distance Distância entre as linhas de plantação.
    """
    img = LoadImage(address)
    win = ImageWindow(config.appname, img)

    img, comp, cmap = SegmentImage(img)
    win.append(img)

    img, lines, pcent, meter = ProcessImage(img, cmap, distance)
    win.text("Falhas: %.2f metros (%d%%)" % (meter, pcent), (20, -50))
    win.append(img)

    SaveImage(address, img)
    
def ExecuteGUI():
    """
    Inicializa a execução da interface gráfica de usuário.
    Dessa forma, precisamos aguardar pelo usuário para que
    algum processamento inicie.
    """
    InitGUI()
