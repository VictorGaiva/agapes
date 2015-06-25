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
from controller.pipeline import high, segment, process
from controller.pipeline.singlestage import SingleStage
from controller.pipeline.multistage import MultiStage
from core.patchwork import PatchWork, Patch
from controller import ThreadWrapper
from core.image import Image
import cv2 as cv


def update(control, canvas):
    """
    Atualiza a imagem mostrada no campo de
    visualização de uma página.
    :param control Controlador da página.
    :param canvas Campo de visualização de imagem.
    """
    control.sp.update()
    canvas.update()

def soil(button, control, e):
    """
    Callback para o evento TOGGLEBUTTON no botão de terra.
    :param button Botão que foi clicado.
    :param control Controlador da página.
    :param e Dados do evento.
    """
    if control.intest:
        control.sp.im = control.last
        control.intest = False
        update(control, control.win.canvas)

    control.cane = False
    control.soil = button.GetValue()
    control.win.i_cane.SetValue(False)

def cane(button, control, e):
    """
    Callback para o evento TOGGLEBUTTON no botão de cana.
    :param button Botão que foi clicado.
    :param control Controlador da página.
    :param e Dados do evento.
    """
    if control.intest:
        control.sp.im = control.last
        control.intest = False
        update(control, control.win.canvas)

    control.soil = False
    control.cane = button.GetValue()
    control.win.i_soil.SetValue(False)

def click(canvas, control, e):
    """
    Callback para o evento CLICK no visualizador de imagem
    :param canvas Campo de visualização de imagem.
    :param control Controlador da página.
    :param e Dados do evento.
    """
    if control.intest:
        control.sp.im = control.last
        control.intest = False
        update(control, control.win.canvas)

def clicksoil(canvas, control, pos):
    """
    Demarcação de pixel solo.
    :param canvas Campo de visualização de imagem.
    :param control Controlador da página.
    :param pos Posição onde o clique ocorreu.
    """
    realpos = canvas.im.imgpos(*pos)

    if 0 <= realpos.x < control.im.shape.x              \
    and 0 <= realpos.y < control.im.shape.y:
        color = control.lab[realpos]
        if color[0]:
            control.train[0].append(color)
            cv.circle(control.tgt.raw, realpos, 2, (255,0,0), -1)
            update(control, canvas)

def clickcane(canvas, control, pos):
    """
    Demarcação de pixel solo.
    :param canvas Campo de visualização de imagem.
    :param control Controlador da página.
    :param pos Posição onde o clique ocorreu.
    """
    realpos = canvas.im.imgpos(*pos)

    if 0 <= realpos.x < control.im.shape.x              \
    and 0 <= realpos.y < control.im.shape.y:
        color = control.lab[realpos]
        if color[0]:
            control.train[1].append(color)
            cv.circle(control.tgt.raw, realpos, 2, (0,255,0), -1)
            update(control, canvas)
            
@ThreadWrapper
def incrementa(button, control, e):
    """
    Callback para o clique do botão de teste.
    :param button Botão que foi clicado.
    :param control Controlador da página.
    :param e Dados do evento.
    """
    control.soil = control.cane = False
    control.win.i_cane.SetValue(False)
    control.win.i_soil.SetValue(False)
    control.intest = True

    x0 = min(control.selected, key = lambda e: e.pos.x).pos.x
    y0 = min(control.selected, key = lambda e: e.pos.y).pos.y
    x1 = max(control.selected, key = lambda e: e.pos.x).pos.x
    y1 = max(control.selected, key = lambda e: e.pos.y).pos.y

    xdiff = x1 - x0
    ydiff = y1 - y0
    psize = control.parent.im.psize

    img = Image.new(((1 + xdiff) * psize.x, (1 + ydiff) * psize.y))

    comm = SingleStage(high, segment)
    comm.event = False

    x = [[0,128,128]]
    y = [0]

    x = x + control.train[0] + control.train[1]
    y = y + [0] * len(control.train[0]) + [255] * len(control.train[1])
    if len(x) > 2: 
      with open('patchtrain.csv','a') as f:
        for i in range(len(x)):
            tstr = ' '.join(map(str,x[i])) + ' '+ str(y[i])+'\n'
            f.write(tstr)
            

    for elem in control.selected:
        comm.push(patch = elem[0], pos = elem.pos)

    pwork = PatchWork(control.parent.im.psize, img)
    pwork.shred(0)

    control.last = control.sp.im
    control.sp.im = pwork
    update(control, control.win.canvas)

    while comm.pendent:
        data = comm.pop()
        pwork.access(data.pos - control.diff).sew(data.image.colorize())
        update(control, control.win.canvas)
    

@ThreadWrapper
def sobreescreve(button, control, e):
    """
    Callback para o clique do botão de teste.
    :param button Botão que foi clicado.
    :param control Controlador da página.
    :param e Dados do evento.
    """
    control.soil = control.cane = False
    control.win.i_cane.SetValue(False)
    control.win.i_soil.SetValue(False)
    control.intest = True

    x0 = min(control.selected, key = lambda e: e.pos.x).pos.x
    y0 = min(control.selected, key = lambda e: e.pos.y).pos.y
    x1 = max(control.selected, key = lambda e: e.pos.x).pos.x
    y1 = max(control.selected, key = lambda e: e.pos.y).pos.y

    xdiff = x1 - x0
    ydiff = y1 - y0
    psize = control.parent.im.psize

    img = Image.new(((1 + xdiff) * psize.x, (1 + ydiff) * psize.y))

    comm = SingleStage(high, segment)
    comm.event = False

    x = [[0,128,128]]
    y = [0]

    x = x + control.train[0] + control.train[1]
    y = y + [0] * len(control.train[0]) + [255] * len(control.train[1])
    if len(x) > 2: 
      with open('patchtrain.csv','w') as f:
        for i in range(len(x)):
            tstr = ' '.join(map(str,x[i])) + ' '+ str(y[i])+'\n'
            f.write(tstr)
            

    for elem in control.selected:
        comm.push(patch = elem[0], pos = elem.pos)

    pwork = PatchWork(control.parent.im.psize, img)
    pwork.shred(0)

    control.last = control.sp.im
    control.sp.im = pwork
    update(control, control.win.canvas)

    while comm.pendent:
        data = comm.pop()
        pwork.access(data.pos - control.diff).sew(data.image.colorize())
        update(control, control.win.canvas)
@ThreadWrapper
def test(button, control, e):
    """
    Callback para o clique do botão de teste.
    :param button Botão que foi clicado.
    :param control Controlador da página.
    :param e Dados do evento.
    """
    control.soil = control.cane = False
    control.win.i_cane.SetValue(False)
    control.win.i_soil.SetValue(False)
    control.intest = True

    x0 = min(control.selected, key = lambda e: e.pos.x).pos.x
    y0 = min(control.selected, key = lambda e: e.pos.y).pos.y
    x1 = max(control.selected, key = lambda e: e.pos.x).pos.x
    y1 = max(control.selected, key = lambda e: e.pos.y).pos.y

    xdiff = x1 - x0
    ydiff = y1 - y0
    psize = control.parent.im.psize

    img = Image.new(((1 + xdiff) * psize.x, (1 + ydiff) * psize.y))

    comm = SingleStage(high, segment)
    comm.event = False

    x = [[0,128,128]]
    y = [0]

    x = x + control.train[0] + control.train[1]
    y = y + [0] * len(control.train[0]) + [255] * len(control.train[1])

            

    for elem in control.selected:
        comm.push(patch = elem[0], pos = elem.pos)

    pwork = PatchWork(control.parent.im.psize, img)
    pwork.shred(0)

    control.last = control.sp.im
    control.sp.im = pwork
    update(control, control.win.canvas)

    while comm.pendent:
        data = comm.pop()
        pwork.access(data.pos - control.diff).sew(data.image.colorize())
        update(control, control.win.canvas)

@ThreadWrapper
def close(button, control, e):
    """
    Callback para o clique do botão de finalização.
    :param button Botão que foi clicado.
    :param control Controlador da página.
    :param e Dados do evento.
    """
    control.win.Close()

    x = [[0,128,128]]
    y = [0]

    x = x + control.train[0] + control.train[1]
    y = y + [0] * len(control.train[0]) + [255] * len(control.train[1])

    comm = MultiStage(high, segment, process, control = control.parent)

    for i, p in enumerate(control.selected):
        p.select(0)
        comm.push(patch = p, distance = control.parent.pg.i_dval.GetValue(), id = -i)

    comm.consume()
