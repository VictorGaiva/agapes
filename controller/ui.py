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
from .pipeline import *
from . import ThreadWrapper
from core.patch import PatchWork
from gui.event import EventBinder, PostEvent
from gui import InitUI

@EventBinder("ImageLoaded")
def OnImageLoaded(img, context):
    """
    Função invocada em reação ao evento ImageLoaded.
    :param img Imagem carregada.
    :param context Contexto de execução.
    """
    page, = context
    page.dropfield.SetImage(img.normalize().raw, *img.shape)

@EventBinder("ImageSegmented")
def OnImageSegmented(img, context):
    """
    Função invocada em reação ao evento ImageSegmented.
    :param img Imagem segmentada.
    :param context Contexto de execução.
    """
    page, patch = context
    page.dropfield.original[0].glue(patch, img.colorize())
    page.dropfield.original[1].glue(patch, img.colorize())

    page.dropfield.ChangeImage(2, page.dropfield.original[0].raw, *page.dropfield.original[0].shape)
    page.dropfield.ChangeImage(3, page.dropfield.original[1].raw, *page.dropfield.original[1].shape)

@EventBinder("ImageProcessed")
def OnImageProcessed(img, pcent, meter, context):
    """
    Função invocada em reação ao evento ImageProcessed.
    :param img Imagem processada.
    :param pcent Porcentagem de falhas.
    :param meter Metros de falhas encontrados.
    :param context Contexto de execução.
    """
    page, patch = context
    page.dropfield.original[1].glue(patch, img)
    print "{0}% {1} metros".format(pcent, meter)
    page.dropfield.ChangeImage(3, page.dropfield.original[1].raw, *page.dropfield.original[1].shape)

@EventBinder("NewPage")
@ThreadWrapper
def OnNewPage(page, filename):
    """
    Função invocada em reação ao evento NewPage.
    :param page Página recém-criada.
    :param filename Arquivo de imagem a ser processada.
    """
    comm = Communication()
    comm.push(load, normal, args = (filename,))

    img, = comm.response()
    patchw = PatchWork(img, 200, 200)
    PostEvent("ImageLoaded", patchw, context = (page,))

    yes, no = patchw.chop().choose(0.6)
    comm.pushmany(segment, normal, [[(p.image,), (p,)] for p in yes])
    comm.pushmany(segment,    low, [[(p.image,), (p,)] for p in no])

    while comm.pendent():
        response = comm.response()

        if response.stage == segment:
            image, cmap = response
            context = (page,) + response.context
            PostEvent("ImageSegmented", image, context = context)
            comm.push(process, response.priority, args = (cmap, 1.5), context = response.context)

        elif response.stage == process:
            image, pcent, meter = response
            context = (page,) + response.context
            PostEvent("ImageProcessed", image, pcent, meter, context = context)

def ControlUI():
    """
    Inicializa a execução da interface gráfica de usuário.
    Dessa forma, precisamos aguardar pelo usuário para que
    algum processamento inicie.
    """
    InitUI()