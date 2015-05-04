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
from . import Control as BaseControl
from controller.event import Event
from core.image import Image
from config import root

class Control(BaseControl):
    """
    Controla e administra a execução de uma
    página de processamento de imagens da
    interface gráfica através dos eventos disparados.
    """
    _init = Image.load("{0}/img/dginit.png".format(root))
    _over = Image.load("{0}/img/dgover.png".format(root))

    def __init__(self, parent, main = False):
        """
        Inicializa uma nova instância.
        :param parent Controlador superior na hierarquia.
        :param main A página a ser controlada é inicial?
        :return Control
        """
        BaseControl.__init__(self, parent)
        self.main = main

    def bind(self, page):
        """
        Vincula uma página ao controlador.
        :param page Página a ser vinculada.
        """
        self.pg = page
        #self.initmain() if self.first else self.waitprocess()
        self.initmain()

        Event("DropEnter", self.pg.canvas).bind(self.enter)
        Event("DropLeave", self.pg.canvas).bind(self.leave)
        Event("DropFiles", self.pg.canvas).bind(self.drop)

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

    def drop(self, canvas, fname):
        """
        Callback para o evento DropLeave.
        :param canvas Campo de drag-n-drop.
        :param fname Arquivos a serem processados.
        """
        self.leave(canvas)
        print fname