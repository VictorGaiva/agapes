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
from core.patch import PatchWork
from core.image import ImageWindow
from gui.event import EventBinder, PostEvent
from .pipeline import *

import config

@EventBinder("ImageSegmented")
def OnImageSegmented(image, context):
    """
    Função invocada em reação ao evento ImageSegmented.
    :param image Imagem segmentada.
    :param context Contexto de execução.
    """
    win, patch = context
    win[1].glue(patch.pos, patch.size, image.colorize())
    win[2].glue(patch.pos, patch.size, image.colorize())

@EventBinder("ImageProcessed")
def OnImageProcessed(image, pcent, meter, context):
    """
    Função invocada em reação ao evento ImageProcessed.
    :param image Imagem resultante do processamento.
    :param pcent Porcentagem de falhas encontradas.
    :param meter Metros de falhas encontrados.
    """
    win, patch = context
    win[2].glue(patch.pos, patch.size, image)
    win.text("Falhas: %.2f metros (%d%%)" % (meter, pcent), (20, -50))

def ControlCommandLine(address, distance, width, height, rate):
    """
    Executar o programa a partir da linha de comando, permitindo
    assim, o uso em plataformas diferenciadas onde a GUI não
    está disponível ou é incompatível.
    :param address Endereço da imagem alvo do processamento.
    :param distance Distância entre as linhas de plantação.
    :param width Largura das amostras.
    :param height Altura das amostras.
    :param rate Porcentagem de amostras a serem selecionadas.
    """
    comm = Communication()
    comm.push(load, normal, args = (address,))

    img, = comm.response()
    patchw = PatchWork(img, width, height)
    win = ImageWindow(config.appname, patchw, 3)

    yes, no = patchw.chop().choose(rate)
    comm.pushmany(segment, normal, [[(p.image,), (p,)] for p in yes])
    comm.pushmany(segment,    low, [[(p.image,), (p,)] for p in no])

    while comm.pendent():
        response = comm.response()

        if response.stage == segment:
            image, cmap = response
            context = (win,) + response.context
            PostEvent("ImageSegmented", image, context = context)
            comm.push(process, response.priority, args = (cmap, distance), context = response.context)

        elif response.stage == process:
            image, pcent, meter = response
            context = (win,) + response.context
            PostEvent("ImageProcessed", image, pcent, meter, context = context)
