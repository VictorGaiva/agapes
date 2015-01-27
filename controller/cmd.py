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
from gui.event import EventBinder
from core.image import ImageWindow
from core import SaveImage
import controller as ct

import config

@EventBinder("ImageSegmented")
def OnImageSegmented(img, context):
    """
    Função invocada em reação ao evento ImageSegmented.
    :param img Imagem segmentada.
    :param context Contexto de execução.
    """
    context.append(img)

@EventBinder("ImageProcessed")
def OnImageProcessed(img, pcent, meter, context):
    """
    Função invocada em reação ao evento ImageProcessed.
    :param img Imagem processada.
    :param pcent Porcentagem de falhas.
    :param meter Metros de falhas encontrados.
    :param context Contexto de execução.
    """
    context.text("Falhas: %.2f metros (%d%%)" % (meter, pcent), (20, -50))
    context.append(img)

def ControlCommandLine(address, distance):
    """
    Executar o programa a partir da linha de comando, permitindo
    assim, o uso em plataformas diferenciadas onde a GUI não
    está disponível ou é incompatível.
    :param address Endereço da imagem alvo do processamento.
    :param distance Distância entre as linhas de plantação.
    """
    img = ct.LoadImage(address)
    win = ImageWindow(config.appname, img)

    img, comp, cmap = ct.SegmentImage(img, context = win)
    img, lines, pcent, meter = ct.ProcessImage(img, cmap, distance, context = win)

    SaveImage(address, img)
