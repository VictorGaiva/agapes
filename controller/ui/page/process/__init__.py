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
from core.patchwork.layered import LayeredPatchWork
from core.spectator.selection import SelectionSpectator
from .. import Control as BaseControl
from controller import ThreadWrapper
from core.algorithm import Algorithm
from controller.event import Event
from core.image import Image
from core.util import Point
from . import events as e
from config import root
import wx

#TODO: Melhorar linkagem de eventos.
#TODO: Organizar funções de callback de eventos.

class Control(BaseControl):
    """
    Controla e administra a execução de uma
    página de processamento de imagens da
    interface gráfica através dos eventos disparados.
    """
    _init = Image.load("{0}/img/dginit.png".format(root))
    _over = Image.load("{0}/img/dgover.png".format(root))
    _wait = Image.load("{0}/img/dgwait.png".format(root))

    def __init__(self, parent, main = False):
        """
        Inicializa uma nova instância.
        :param parent Controlador superior na hierarquia.
        :param main A página a ser controlada é inicial?
        :return Control
        """
        BaseControl.__init__(self, parent)
        self.main = main

        self.selected = set()
        self.result = {}

    def bind(self, page):
        """
        Vincula uma página ao controlador.
        :param page Página a ser vinculada.
        """
        self.pg = page
        self.initmain() if self.main else self.waitprocess()

        Event("DropEnter", self.pg.canvas).bind(self.enter)
        Event("DropLeave", self.pg.canvas).bind(self.leave)
        Event("DropFiles", self.pg.canvas).bind(self.drop)

        if not self.main:
            Event(wx.EVT_TOGGLEBUTTON, self.pg.l_g).bind(e.grid, self)
            Event(wx.EVT_TOGGLEBUTTON, self.pg.l_1).bind(e.layer, self)
            Event(wx.EVT_TOGGLEBUTTON, self.pg.l_2).bind(e.layer, self)
            Event(wx.EVT_TOGGLEBUTTON, self.pg.l_3).bind(e.layer, self)
            Event(wx.EVT_BUTTON, self.pg.s_done).bind(e.deselect, self)
            Event(wx.EVT_BUTTON, self.pg.s_add).bind(e.addresult, self)
            Event(wx.EVT_BUTTON, self.pg.s_del).bind(e.delresult, self)
            Event(wx.EVT_BUTTON, self.pg.s_fsg).bind(e.patchsegment, self)
            Event(wx.EVT_BUTTON, self.pg.a_run).bind(e.run, self)
            Event(wx.EVT_MOTION, self.pg.canvas).bind(self.mMotion)
            Event(wx.EVT_MOUSEWHEEL, self.pg.canvas).bind(self.mWheel)
            Event(wx.EVT_LEFT_DOWN, self.pg.canvas).bind(self.lDown)
            Event(wx.EVT_LEFT_UP, self.pg.canvas).bind(self.lUp)
            Event("Click", self.pg.canvas).bind(e.select, self)
            Event("ImageSegmented").bind(e.segmented)
            Event("ImageProcessed").bind(e.processed)

    def initmain(self):
        """
        Mostra na página o campo de drag-n-drop. Esse campo é
        preenchido com uma imagem inicial que instrui o usuário
        a inicializar um processamento.
        """
        for elem in [
            self.pg.s_done, self.pg.s_add, self.pg.s_del, self.pg.s_fsg,
            self.pg.s_txt, self.pg.l_g, self.pg.l_1, self.pg.l_2,
            self.pg.l_3, self.pg.a_run, self.pg.a_stop]:
            elem.Disable()

        self.pg.canvas.set(self._init)

    def waitprocess(self):
        """
        Mostra na página uma mensagem de aguardo. Essa imagem
        somente será mudada quando uma imagem for enviada para
        essa página.
        """
        self.pg.canvas.set(self._wait)
        self.pg.l_3.SetValue(True)

    @ThreadWrapper
    def initimage(self, fname):
        """
        Inicializa a imagem a ser processada por essa página.
        :param fname Caminho do arquivo a ser aberto.
        """
        img = Image.load(fname)

        self.im = LayeredPatchWork((200,200), img, img.swap(), img.swap(), img.swap())
        self.sp = SelectionSpectator(self.im, self.im.psize, self.pg.canvas.size)

        self.pg.canvas.set(self.sp)
        self.sp.update()
        self.pg.canvas.update()

        self.ex = Algorithm(self.im)

    def enter(self, canvas):
        """
        Callback para o evento DropEnter.
        :param canvas Campo de drag-n-drop.
        """
        self._prev = canvas.set(self._over)

    def leave(self, canvas):
        """
        Callback para o evento DropLeave.
        :param canvas Campo de drag-n-drop.
        """
        canvas.set(self._prev)

    def drop(self, canvas, fnames):
        """
        Callback para o evento DropLeave.
        :param canvas Campo de drag-n-drop.
        :param fnames Arquivos a serem processados.
        """
        for fn in fnames:
            newpg = Event("NewPage", self.parent.win.book).post(self.pg)
            newpg.initimage(fn)

        self.leave(canvas)

    def mMotion(self, canvas, e):
        """
        Callback para o evento de mouse MOTION.
        :param canvas Campo de exibição de imagens
        :param e Dados do evento.
        """
        if e.LeftIsDown():
            self._move = self._move + 1
            diff = self._mstart - (e.x, e.y)
            canvas.im.move(self._mark, *diff)
            canvas.update()

    def mWheel(self, canvas, e):
        """
        Callback para o evento de mouse MOUSEWHEEL.
        :param canvas Campo de exibição de imagens
        :param e Dados do evento.
        """
        self._mark = canvas.im.mark()
        diff = e.GetWheelRotation() // e.GetWheelDelta()
        canvas.im.zoom(self._mark, diff * 45)
        canvas.im.update()
        canvas.update()

    def lDown(self, canvas, e):
        """
        Callback para o evento de mouse LEFT_DOWN.
        :param canvas Campo de exibição de imagens
        :param e Dados do evento.
        """
        self._mstart = Point(e.GetX(), e.GetY())
        self._mark = canvas.im.mark()
        self._move = 0
        e.Skip()

    def lUp(self, canvas, e):
        """
        Callback para o evento de mouse LEFT_UP.
        :param canvas Campo de exibição de imagens
        :param e Dados do evento.
        """
        if self._move <= 3:
            Event("Click", canvas).post(self._mstart)
