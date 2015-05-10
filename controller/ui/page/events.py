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
from core.image import Image

def layer(button, control, e):
    """
    Callback para o evento TOGGLEBUTTON nos botões
    de camada.
    :param button Botão que foi clicado.
    :param control Controlador da página.
    :param e Dados do evento.
    """
    for b in control.pg.l:
        b.SetValue(b.Id == button.Id)

    control.im.select(button.Id)
    control.sp.update()
    control.pg.canvas.update()

def grid(button, control, e):
    """
    Callback para o evento TOGGLEBUTTON no botão
    de grade.
    :param button Botão que foi clicado.
    :param control Controlador da página.
    :param e Dados do evento.
    """
    control.sp.showgrid(button.Value)
    control.sp.update()
    control.pg.canvas.update()