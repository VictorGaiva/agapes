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
from gui import InitGUI, ThreadWrapper
from core.image import ImageWindow
from core import *
import config
import time

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

@ThreadWrapper
def ExecutePage(page, filename):
    """
    Controla a execução do algoritmo enquanto estiver sendo executado
    a partir da interface gráfica.
    :param page Página alvo da execução.
    :param filename Nome do arquivo a processado.
    """
    img = LoadImage(filename)
    page.dropfield.AppendImage(img.normalize().raw, *img.shape)
    page.origbt.SetValue(True)
    time.sleep(.1)

    img, comp, cmap = SegmentImage(img)
    if img.inverted:
        page.dropfield.AppendImage(img.colorize().normalize().transpose().raw, *img.shape.swap)
    else:
        page.dropfield.AppendImage(img.colorize().normalize().raw, *img.shape)
    page.origbt.SetValue(False)
    page.origbt.Enable()
    page.segmbt.SetValue(True)
    time.sleep(.1)

    img, _, p, m = ProcessImage(img, cmap, page.dnum.GetValue())
    print "{0}% {1} metros".format(p, m)

    if img.inverted:
        page.dropfield.AppendImage(img.normalize().transpose().raw, *img.shape.swap)
    else:
        page.dropfield.AppendImage(img.normalize().raw, *img.shape)
    page.segmbt.SetValue(False)
    page.segmbt.Enable()
    page.linebt.SetValue(True)
    page.linebt.Enable()

def ExecuteGUI():
    """
    Inicializa a execução da interface gráfica de usuário.
    Dessa forma, precisamos aguardar pelo usuário para que
    algum processamento inicie.
    """
    InitGUI()
