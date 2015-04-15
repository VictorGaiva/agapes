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
import cv2 as cv
from gui.event import EventBinder
from core.patch import PatchWork
import os.path as path
import shutil
import os

@EventBinder("ImageLoaded")
def OnImageLoaded(data, context):
    """
    Função invocada em reação ao evento ImageLoaded.
    :param data Dados de execução.
    :param context Contexto de execução.
    """
    img = data.image
    page = context.page

    page.patchw = PatchWork(img, 200, 200)
    page.path = path.splitext(data.address)[0]

    if path.isdir(page.path):
        shutil.rmtree(page.path)

    os.makedirs(page.path + path.sep + "segmented")
    os.makedirs(page.path + path.sep + "processed")

    page.drop.SetImage(img.normalize(), *img.shape)

@EventBinder("ImageSegmented")
def OnImageSegmented(data, context):
    """
    Função invocada em reação ao evento ImageSegmented.
    :param data Dados de execução.
    :param context Contexto de execução.
    """
    page = context.page
    image, nm = data.image, data.id
    image = image.colorize().normalize()

    page.drop.ChangeImage(1, data.patch, image)
    page.drop.ChangeImage(2, data.patch, image)
    image.save(page.path + path.sep + "segmented" + path.sep + str(nm) + ".png")

@EventBinder("ImageProcessed")
def OnImageProcessed(data, context):
    """
    Função invocada em reação ao evento ImageProcessed.
    :param data Dados de execução.
    :param context Contexto de execução.
    """
    page = context.page
    image, nm = data.image, data.id
    image = image.normalize()

    page.drop.ChangeImage(2, data.patch, image)
    page.drop.ShowLocalResult(data.patch, data.percent, False)

    image.raw = cv.cvtColor(image.raw, cv.COLOR_RGB2BGR)
    image.save(page.path + path.sep + "processed" + path.sep + str(nm) + ".png")

