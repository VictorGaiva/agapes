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
from core.spectator import Spectator
from controller.event import Event
from core.image import Image
from core.util import Point
from . import events as e
import wx

class Control(object):
    """
    Controla e administra a execução da janela de
    segmentação avulsa.
    """

    def __init__(self, parent, selection):
        """
        Inicializa uma nova instância.
        :param parent Controlador-pai.
        :param selection Seleção de imagens a serem segmentadas.
        :return Control
        """
        self.selected = [i for i in selection]
        self.parent = parent
        self.win = None

        self.tgt = self.generate()
        self.im = self.tgt.copy()
        self.lab = self.im.swap().tolab()

        self.intest = False
        self.last = None

        self.train = ([],[])
        self.sp = Spectator(self.tgt, (584,393))
        self.sp.update()

    def __del__(self):
        """
        Destrutor de instância.
        :return
        """

    def bind(self, window):
        """
        Vincula uma janela ao controlador.
        :param window Janela a ser vinculada.
        """
        self.win = window
        self.win.canvas.set(self.sp)
        self.soil, self.cane = False, False

        Event("Click", self.win.canvas).bind(e.click, self)
        Event("SoilClick", self.win.canvas).bind(e.clicksoil, self)
        Event("CaneClick", self.win.canvas).bind(e.clickcane, self)
        Event(wx.EVT_TOGGLEBUTTON, self.win.i_soil).bind(e.soil, self)
        Event(wx.EVT_TOGGLEBUTTON, self.win.i_cane).bind(e.cane, self)
        Event(wx.EVT_BUTTON, self.win.w_incr).bind(e.incrementa, self)
        Event(wx.EVT_BUTTON, self.win.w_sobr).bind(e.sobreescreve, self)
        Event(wx.EVT_BUTTON, self.win.w_test).bind(e.test, self)
        Event(wx.EVT_BUTTON, self.win.w_close).bind(e.close, self)
        Event(wx.EVT_MOTION, self.win.canvas).bind(self.mMotion)
        Event(wx.EVT_MOUSEWHEEL, self.win.canvas).bind(self.mWheel)
        Event(wx.EVT_LEFT_DOWN, self.win.canvas).bind(self.lDown)
        Event(wx.EVT_LEFT_UP, self.win.canvas).bind(self.lUp)

    def generate(self):
        """
        Cria uma imagem baseada nos elementos selecionados para
        segmentação avulsa.
        :return Image
        """
        x0 = min(self.selected, key = lambda e: e.pos.x).pos.x
        y0 = min(self.selected, key = lambda e: e.pos.y).pos.y
        x1 = max(self.selected, key = lambda e: e.pos.x).pos.x
        y1 = max(self.selected, key = lambda e: e.pos.y).pos.y

        xdiff = x1 - x0
        ydiff = y1 - y0
        psize = self.parent.im.psize
        self.diff = Point(x0, y0)

        img = Image.new(((1 + xdiff) * psize.x, (1 + ydiff) * psize.y))
        pwork = PatchWork(psize, img)
        pwork.shred(0)

        for elem in self.selected:
            pwork.access((elem.pos - self.diff)).sew(elem[1])

        return pwork

    def mMotion(self, canvas, e):
        """
        Callback para o evento de mouse MOTION.
        :param canvas Campo de exibição de imagens
        :param e Dados do evento.
        """
        if e.LeftIsDown():
            if self.soil:
                Event("SoilClick", canvas).post((e.x, e.y))
            elif self.cane:
                Event("CaneClick", canvas).post((e.x, e.y))
            else:
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
            if self.soil:
                Event("SoilClick", canvas).post((e.x, e.y))
            elif self.cane:
                Event("CaneClick", canvas).post((e.x, e.y))
            else:
                Event("Click", canvas).post(self._mstart)
