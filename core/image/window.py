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
from ..util import Point
from .spectator import Spectator
from controller import ThreadWrapper
from controller.event import Event
import cv2 as cv

class Window(object):
    """
    Cria, exibe e controla uma janela simples de interface
    gráfica para mostrar e manipular uma imagem.
    """

    def __init__(self, image, wname = 'image', shape = (800, 600)):
        """
        Inicializa e cria uma nova instância de objeto.
        :param image Imagem a ser exibida.
        :param wname Nome da janela a ser criada.
        :param shape Tamanho da janela de exibição.
        :return Window
        """
        self.spec = Spectator(image, shape)
        self.source = image

        self.shape = shape
        self.wname = wname

    @ThreadWrapper
    def show(self):
        """
        Cria uma janela, mostra a imagem e administra os
        eventos de mouse e teclado disparados sobre a janela.
        """
        cv.namedWindow(self.wname, cv.WINDOW_AUTOSIZE)
        cv.resizeWindow(self.wname, *self.shape)

        self.loop()

        cv.destroyWindow(self.wname)
        exit()

    def loop(self):
        """
        Mantém o loop de atualização constante da janela
        de imagem.
        """
        key = cv.waitKey(10) & 255

        while key not in [-1, 27]:
            cv.imshow(self.wname, self.spec.raw)
            cv.setMouseCallback(self.wname, self.mouse)

            key = cv.waitKey(0) & 255

    def mouse(self, event, x, y, flag, *param):
        """
        Trata os eventos de mouse disparados sobre a janela.
        Alguns dos eventos são tratados simplesmente delegando
        o evento para que seja tratado externamente.
        :param event Tipo de evento disparado pelo mouse.
        :param x Posição no eixo-x em que o evento ocorreu.
        :param y Posição no eixo-y em que o evento ocorreu.
        :param flag Informações adicionais sobre o evento.
        :param param Parâmetros adicionais.
        """
        self.actual = Point(x, y)

        if event in [cv.EVENT_LBUTTONDOWN, cv.EVENT_RBUTTONDOWN]:
            self.initial = self.actual
            self.mark = self.spec.mark()

        elif event == cv.EVENT_MOUSEMOVE and flag & cv.EVENT_FLAG_LBUTTON:
            diff = self.initial - self.actual
            self.spec.move(self.mark, *diff)

        elif event == cv.EVENT_MOUSEMOVE and flag & cv.EVENT_FLAG_RBUTTON:
            diff = self.initial.vector - self.actual
            self.spec.zoom(self.mark, diff.length * diff.versor[1] * 3)

        elif event in [cv.EVENT_LBUTTONUP, cv.EVENT_RBUTTONUP] \
            and self.initial == self.actual:
            Event("cvClick", self).post(self.actual, event)

        elif event in [cv.EVENT_LBUTTONDBLCLK, cv.EVENT_RBUTTONDBLCLK]:
            Event("cvDoubleClick", self).post(self.actual, event)

        cv.imshow(self.wname, self.spec.raw)