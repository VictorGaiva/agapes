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
from . import ThreadWrapper
from . import pipeline as pl
from core import SaveImage
from gui.event import EventBinder, PostEvent
from gui import InitUI

@EventBinder("ImageLoaded")
def OnImageLoaded(img, context):
    """
    Função invocada em reação ao evento ImageLoaded.
    :param img Imagem carregada.
    :param context Contexto de execução.
    """
    context.dropfield.AppendImage(img.normalize().raw, *img.shape)
    context.phase[0].SetValue(True)

@EventBinder("ImageSegmented")
def OnImageSegmented(img, context):
    """
    Função invocada em reação ao evento ImageSegmented.
    :param img Imagem segmentada.
    :param context Contexto de execução.
    """
    context.dropfield.AppendImage(img.colorize().normalize().raw, *img.shape)
    context.phase[0].SetValue(False)
    context.phase[1].SetValue(True)
    context.phase[0].Enable()

@EventBinder("ImageProcessed")
def OnImageProcessed(img, pcent, meter, context):
    """
    Função invocada em reação ao evento ImageProcessed.
    :param img Imagem processada.
    :param pcent Porcentagem de falhas.
    :param meter Metros de falhas encontrados.
    :param context Contexto de execução.
    """
    print "{0}% {1} metros".format(pcent, meter)
    context.dropfield.AppendImage(img.normalize().raw, *img.shape)
    context.phase[1].SetValue(False)
    context.phase[2].SetValue(True)
    context.phase[1].Enable()
    context.phase[2].Enable()

@EventBinder("NewPage")
@ThreadWrapper
def OnNewPage(page, filename):
    """
    Função invocada em reação ao evento NewPage.
    :param page Página recém-criada.
    :param filename Arquivo de imagem a ser processada.
    """
    comm = pl.Communication()

    comm.PushToStage(pl.LOAD, pl.NORMAL, args = (filename,))
    img = comm.PopResponse()[1]
    PostEvent("ImageLoaded", img, context = page)

    comm.PushToStage(pl.SEGMENT, pl.NORMAL, args = (img,))
    img, comp, cmap = comm.PopResponse()[1]
    PostEvent("ImageSegmented", img, context = page)

    comm.PushToStage(pl.PROCESS, pl.NORMAL, args = (cmap, 1.5,))
    img, lines, pcent, meter = comm.PopResponse()[1]
    PostEvent("ImageProcessed", img, pcent, meter, context = page)

    SaveImage(filename, img)

def ControlUI():
    """
    Inicializa a execução da interface gráfica de usuário.
    Dessa forma, precisamos aguardar pelo usuário para que
    algum processamento inicie.
    """
    InitUI()