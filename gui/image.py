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
from .util import Jar

import os.path as path
import config
import wx

drag = Jar(
    init = wx.Image(path.join(config.path, "img", "dginit.png"), wx.BITMAP_TYPE_ANY),
    over = wx.Image(path.join(config.path, "img", "dgover.png"), wx.BITMAP_TYPE_ANY)
)
