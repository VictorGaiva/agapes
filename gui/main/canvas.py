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
from controller.event import Event
from core.image import Image
import wx

class Canvas(wx.Panel, wx.FileDropTarget):
    """
    Painel responsável pela exibição e manipulação das
    imagens a serem apresentadas. Este painel é o elemento
    de interface gráfica mais importante do software.
    """

    def __init__(self, parent, size, *args, **kwargs):
        """
        Inicializa uma nova instância do objeto.
        :param parent Objeto pai.
        :param size Tamanho do canvas.
        :param args Argumentos de posição passados ao método.
        :param kwargs Argumentos nominais passados ao método.
        :return BufferedPanel
        """
        wx.Panel.__init__(self, parent, -1, size = size, *args, **kwargs)
        wx.FileDropTarget.__init__(self)

        self.size = size
        self.frames = 0

        Event(wx.EVT_PAINT, self).bind(Canvas.paint)
        self.SetDoubleBuffered(True)
        self.SetDropTarget(self)
        self.init()

    def paint(self, event):
        """
        Desenha o buffer no painel.
        :param event Dados do evento.
        """
        wx.BufferedPaintDC(self, self.buffer)

    def init(self):
        """
        Inicializa o buffer de desenho.
        """
        self.buffer = wx.EmptyBitmap(*self.size)
        self.im = Image.new(self.size)
        self.update()

    def set(self, image):
        """
        Modifica a imagem a ser mostrada no canvas.
        :param image Nova imagem a ser mostrada.
        :return Image
        """
        last = self.im
        self.im = image
        self.update()

        return last

    def update(self):
        """
        Força a atualização do buffer de desenho e o
        device context atuais.
        """
        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)

        self.draw(dc)
        del dc

        self.Refresh()
        self.Update()

    def draw(self, dc):
        """
        Desenha no buffer o que deve ser mostrado no
        painel.
        :param dc Device context.
        """
        dc.SetBackground(wx.Brush(wx.Colour(0x00, 0x00, 0x00)))
        dc.Clear()

        bmp = wx.BitmapFromBuffer(self.im.shape.x, self.im.shape.y, self.im.raw)
        dc.DrawBitmap(bmp, 0, 0)

    def OnEnter(self, *args):
        """
        Callback para o evento de entrada do mouse sobre
        a área de drop. Delega o evento para o
        manipulador personalizado de eventos.
        :param args Argumentos do evento.
        :return bool
        """
        Event("DropEnter", self).post()
        return True

    def OnDropFiles(self, x, y, fname):
        """
        Callback para o evento de drop. Esse método somente
        delega o evento disparado para o manipulador
        personalizado de eventos.
        :param x Valor da coordenada x em que o evento ocorreu.
        :param y Valor da coordenada y em que o evento ocorreu.
        :param fname Arquivos que foram arrastados.
        """
        Event("DropFiles", self).post(fname)
        return True

    def OnLeave(self):
        """
        Callback para o evento de saída do mouse sobre
        a área de drop. Delega o evento para o
        manipulador personalizado de eventos.
        """
        Event("DropLeave", self).post()