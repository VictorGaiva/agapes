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
    count = 0

    for elem in control.selected:

        if elem not in control.result.keys():
            continue

        pcent, meter = control.result[elem]
        totalpcent = totalpcent + pcent
        totalmeter = totalmeter + meter
        count = count + 1

    if not count:
        control.pg.r_pcent.SetLabel("0")
        control.pg.r_fmtrs.SetLabel("0 m")
    else:
        control.pg.r_pcent.SetLabel(str(int(round(totalpcent / float(count)))))
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
    pass

def run(button, control, e):
    """
    Callback para o evento BUTTON de processamento.
    :param button Botão responsável pelo evento.
    :param control Controlador de página.
    :param e Dados do evento.
    """
    button.Disable()
    control.ex.run(control, control.pg.i_dval.GetValue())

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
    context.control.sp.addtext(data.patch.pos, str(int(round(data.percent))) + "%", (255,0,0))
    context.control.result[data.patch.pos] = (data.percent, data.meters)
    updateresult(context.control)
    update(context.control)
