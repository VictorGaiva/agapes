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
from gui.event import EventBinder, PostEvent
from core.image import ImageWindow
from core import SaveImage
from . import pipeline as pl

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
    comm = pl.Communication()

    comm.PushToStage(pl.LOAD, pl.NORMAL, args = (address,))
    img = comm.PopResponse()[1]
    win = ImageWindow(config.appname, img)

    comm.PushToStage(pl.SEGMENT, pl.NORMAL, args = (img,))
    img, comp, cmap = comm.PopResponse()[1]
    PostEvent("ImageSegmented", img, context = win)

    comm.PushToStage(pl.PROCESS, pl.NORMAL, args = (cmap, distance,))
    img, lines, pcent, meter = comm.PopResponse()[1]
    PostEvent("ImageProcessed", img, pcent, meter, context = win)

    SaveImage(address, img)
