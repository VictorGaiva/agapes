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
from core.patchwork import PatchWork
import cv2 as cv
import os

#TODO: Organizar as funções em grupos de funções correlacionadas.

def update(control):
    """
    Atualiza a imagem mostrada no campo de
    visualização de uma página.
    :param control Controlador da página.
    """
    control.sp.update()
    control.pg.canvas.update()

def updateresult(control):
    """
    Atualiza a contabilização do resultado obtido
    pelo algoritmo.
    :param control Controlador da página.
    """
    totalpcent = 0
    totalmeter = 0
    totalcrops = 0
    count = 0

    for elem in control.selected:

        if elem not in control.result.keys():
            continue

        pcent, meter, crops = control.result[elem]
        totalpcent = totalpcent + pcent
        totalmeter = totalmeter + meter
        totalcrops = totalcrops + crops
        count = count + 1

    if not count:
        control.pg.r_pcent.SetLabel("0.00")
        control.pg.r_fmtrs.SetLabel("0 m")
        control.pg.r_cmtrs.SetLabel("0 m")
    else:
        control.pg.r_pcent.SetLabel(str(round(totalpcent / float(count), 2)))
        control.pg.r_cmtrs.SetLabel(str(totalcrops) + " m")
        control.pg.r_fmtrs.SetLabel(str(totalmeter) + " m")

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
    update(control)

def grid(button, control, e):
    """
    Callback para o evento TOGGLEBUTTON no botão
    de grade.
    :param button Botão que foi clicado.
    :param control Controlador da página.
    :param e Dados do evento.
    """
    control.sp.showgrid(button.Value)
    update(control)

def select(canvas, control, pos):
    """
    Callback para o evento Click sobre o campo de
    visualização de imagem.
    :param canvas Campo de visualização de imagem.
    :param control Controlador de página.
    :param pos Posição de clique sobre a imagem.
    """
    control.sp.select(*pos)
    update(control)

    qtd = len(control.sp)
    txt = "{0} retalhos selecionados."
    control.pg.s_fsg.Enable(bool(qtd))
    control.pg.s_txt.SetLabel(txt.format(qtd) if qtd else "")

def deselect(button, control, e):
    """
    Callback para o evento BUTTON de desseleção.
    :param button Botão responsável pelo evento.
    :param control Controlador de página.
    :param e Dados do evento.
    """
    control.pg.s_txt.SetLabel("")
    control.pg.s_fsg.Disable()
    control.sp.deselect()
    update(control)

def addresult(button, control, e):
    """
    Callback para o evento BUTTON de adição de resultado.
    :param button Botão responsável pelo evento.
    :param control Controlador de página.
    :param e Dados do evento.
    """
    for elem in control.sp.selection:
        control.sp.settextcolor(elem.pos, (0,255,0))

    elems = set([e.pos for e in control.sp.selection])
    control.selected.update(elems)
    control.pg.r_patch.SetLabel(str(len(control.selected)) + "/" + str(control.patchcount))
    updateresult(control)

def delresult(button, control, e):
    """
    Callback para o evento BUTTON de exclusão de resultado.
    :param button Botão responsável pelo evento.
    :param control Controlador de página.
    :param e Dados do evento.
    """
    for elem in control.sp.selection:
        control.sp.settextcolor(elem.pos, (255,0,0))

    elems = set([e.pos for e in control.sp.selection])
    control.selected.difference_update(elems)
    updateresult(control)

def patchsegment(button, control, e):
    """
    Callback para o evento BUTTON de segmentação avulsa.
    :param button Botão responsável pelo evento.
    :param control Controlador de página.
    :param e Dados do evento.
    """
    from controller.ui.segment import Control
    from gui.segmentation import Init

    control = Control(control, control.sp.selection)
    Init(control)

def run(button, control, e):
    """
    Callback para o evento BUTTON de processamento.
    :param button Botão responsável pelo evento.
    :param control Controlador de página.
    :param e Dados do evento.
    """
    button.Disable()
    control.ex.run(control, control.pg.i_dval.GetValue())

def end(button, control, e):
    """
    Callback para o evento BUTTON de finalizar.
    :param button Botão responsável pelo evento.
    :param control Controlador de página.
    :param e Dados do evento.
    """
    img = control.im[0].copy()

    pw = PatchWork((200,200), img)
    pw.shred()

    for patch in control.selected:
        pt = control.im.access(patch)[3].swap()
        pw.access(patch).sew(pt)
        cv.putText(img.raw, control.sp.gettext(patch), (patch[0]*200 + 10, patch[1]*200 + 190), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.CV_AA)

    fdir = os.path.split(os.path.realpath(control.pg.address))
    img.save(fdir[0] + os.path.sep + "processed." + fdir[1])

def segmented(data, context):
    """
    Callback para o evento global ImageSegmented.
    :param data Dados do processamento.
    :param context Contexto de evento.
    """
    data.patch.sew(data.image.colorize(), 2)
    update(context.control)

def processed(data, context):
    """
    Callback para o evento global ImageProcessed.
    :param data Dados do processamento.
    :param context Contexto de evento.
    """
    data.patch.sew(data.image.swap(), 3)
    context.control.sp.addtext(data.patch.pos, str(round(data.percent, 2)) + "%", (255,0,0))
    context.control.result[data.patch.pos] = (data.percent, data.meters, data.crop)
    updateresult(context.control)
    update(context.control)
