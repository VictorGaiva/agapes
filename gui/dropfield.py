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
from core.point import *
from .event import PostEvent
from . import image

from internal import FloatCanvas, GUIMode
import wx

class DropField(FloatCanvas.FloatCanvas, wx.FileDropTarget):
    """
    Objeto responsável pela criação, administração de
    campos de drag and drop.
    """

    class ImageElement(object):
        """
        Objeto responsável por armazenar um elemento
        da lista de imagens.
        """

        def __init__(self, bitmap, shape = (0,0)):
            """
            Cria uma nova instância do objeto.
            :param bitmap Imagem bitmap a ser adicionada à lista.
            :param shape Tamanho da imagem a ser adicionada.
            :return ImageElement
            """
            self.bitmap = bitmap
            self.shape = Point(*shape)

        @classmethod
        def FromImage(cls, img):
            """
            Cria uma nova instância a partir de um objeto
            de imagem.
            :param img Imagem a ser transformada em bitmap.
            :return ImageElement
            """
            bitmap = wx.BitmapFromImage(img)
            return cls(bitmap)

        @classmethod
        def FromBuffer(cls, buf, width, height):
            """
            Cria uma nova instância a partir de um objeto
            de imagem.
            :param buf Buffer a ser transformado em bitmap.
            :param width Largura dos dados contidos no buffer.
            :param height Altura dos dados contidos no buffer.
            :return ImageElement
            """
            bitmap = wx.BitmapFromBuffer(width, height, buf)
            return cls(bitmap, (width, height))

    def __init__(self, parent, etarget, placeholder = False, size = (568, 453)):
        """
        Cria uma nova instância do objeto.
        :param parent Janela-pai da janela atual.
        :param size Tamanho a ser ocupado pelo widget.
        :param placeholder Janela sem imagem?
        """
        self.size = Point(*size)
        self.parent = parent
        self.placeholder = placeholder
        self.etarget = etarget
        self.index = None
        self.list = []

        self.incount = []
        self.outcount = []
        self.total = 0.0

        FloatCanvas.FloatCanvas.__init__(self, parent, -1, size, None, "Black")
        wx.FileDropTarget.__init__(self)

        init = self.ImageElement.FromImage(image.drag.init)
        over = self.ImageElement.FromImage(image.drag.over)

        self.init =\
            self.AddBitmap(init.bitmap, (0,0), 'cc', False) if placeholder else\
            self.AddText("Carregando...", (0,0), 10, "White", Position = 'cc')

        self.over = self.AddBitmap(over.bitmap, (0,0), 'cc', True)
        self.over.Hide()

        self.SetDropTarget(self)
        #self.BindEvents()

    def BindEvents(self):
        """
        Víncula métodos do objeto a eventos que podem ser disparados.
        :return None
        """
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def SetImage(self, img, width, height):
        """
        Adiciona uma imagem à lista de imagens para exibição.
        :param img Imagem a ser adicionada.
        :param width Largura da imagem a ser adicionada.
        :param height Largura da imagem a ser adicionada.
        """
        self.list.extend([
            self.ImageElement.FromBuffer(img.raw, width, height),
            self.ImageElement.FromBuffer(img.raw, width, height),
            self.ImageElement.FromBuffer(img.raw, width, height),
        ])

        self.init.Hide()
        self.height = height
        self.bitmap = self.AddScaledBitmap(self.list[2].bitmap, (0,0), height, 'cc', False)
        self.DrawGrid(img.shape, 200, 200)
        self.ShowGrid(False)
        self.SetMode(GUIMode.GUIMove())
        self.index = 2

        self.Draw(True)

    def DrawGrid(self, imgsize, width, height):
        """
        Desenha a grade de retalhos da imagen.
        :param imgsize Tamanho total da imagem.
        :param width Largura de cada retalho.
        :param height Altura de cada retalho.
        """
        tl = Point(-imgsize.x / 2, imgsize.y / 2)
        e = []

        for x in xrange(0, imgsize.x, width):
            e.append(self.AddLine((tl + (x, 0), tl + (x, -imgsize.y)), "Green"))

        for y in xrange(0, imgsize.y, height):
            e.append(self.AddLine((tl - (0, y), tl - (-imgsize.x, y)), "Green"))

        e.append(self.AddLine((tl + (imgsize.x, 0), tl + (imgsize.x, -imgsize.y)), "Green"))
        e.append(self.AddLine((tl - (0, imgsize.y), tl - (-imgsize.x, imgsize.y)), "Green"))

        self.grid = e

    def ShowGrid(self, show):
        """
        Método responsável por controlar a exibição ou
        não da grade de retalhos.
        :param show Controle de exibição da grade.
        """
        if show:
            for e in self.grid: e.Show()
        else:
            for e in self.grid: e.Hide()

        self.Draw(True)

    def ShowLocalResult(self, patch, pcent, contagem):
        """
        Exibe a porcentagem de falhas encontradas em um
        retalho da imagem.
        :param patch Informações sobre o retalho.
        :param pcent Porcentagem de falhas encontradas.
        :param contagem Faz parte da contagem total?
        """
        imgsize = self.list[0].shape
        tl = Point(-imgsize.x / 2, imgsize.y / 2)

        t = self.AddScaledTextBox(
            "{0}%".format(pcent),
            (tl.x + patch.pos.x + (patch.size.x / 2), tl.y - patch.pos.y - (patch.size.y / 2)),
            25, "Green" if contagem else "Red",
            Position = 'cc',
            Alignment = 'center',
            Weight = wx.BOLD,
            LineColor = None
        )

        R = self.AddRectangle( (tl.x + patch.pos.x + 5, tl.y - patch.pos.y - 5), (patch.size.x - 10, -patch.size.y + 10),
            LineColor = None, FillColor = None
        )
        R.Name = t
        R.Bind(FloatCanvas.EVT_FC_LEFT_DCLICK, self.DeleteFromCount)

        if contagem:
            self.incount.append(t)
            self.UpdateContagem()
        else:
            self.outcount.append(t)

    def DeleteFromCount(self, obj):
        """
        Deleta um retalho da contagem de falhas.
        :param obj Retalho clicado.
        """
        t = obj.Name

        if t.Color == "Green":
            self.incount.remove(t)
            self.outcount.append(t)
            t.Color = "Red"
        else:
            self.outcount.remove(t)
            self.incount.append(t)
            t.Color = "Green"

        self.UpdateContagem()
        self.Draw(True)

    def UpdateContagem(self):
        """
        Calcula a porcentagem de falhas de acordo com os retalhos
        selecionados.
        """
        count = 0.0
        for t in self.incount:
            count += float(t.String[:-1])
        count /= len(self.incount)

        PostEvent("UpdateContagem", self.etarget, count, len(self.incount))

    def ChangeImage(self, index, patch, img):
        """
        Modifica a imagem presente em um dos índices da lista
        de imagens para exibição.
        :param index Índice alvo para da mudança.
        :param patch Recorte de imagem e dados de clipagem.
        :param img Imagem a ser costurada
        """
        dc = wx.BufferedDC(None, self.list[index].bitmap)

        dc.DrawBitmap(
            self.ImageElement.FromBuffer(img.raw, *img.shape).bitmap,
            patch.pos.x, patch.pos.y, True
        )

        del dc

        if index == self.index:
            try:
                self.bitmap.__init__(self.list[index].bitmap, (0,0), self.height, 'cc', False)
                self.Draw(True)
            except:
                return

    def ShowIndex(self, sid):
        """
        Muda a imagem a ser exibida.
        :param sid Índice da imagem a ser mostrada.
        """
        self.index = sid if sid < len(self.list) else self.index
        self.bitmap.__init__(self.list[self.index].bitmap, (0,0), self.height, 'cc', False)
        self.Draw(True)

    def OnEnter(self, *args):
        """
        Método executado em reação ao evento Enter de
        wx.FileDropTarget .
        :return int
        """
        self.over.Show()
        self.Draw(True)

        PostEvent("PushStatus", u'Solte a imagem e clique em "Processar" para processá-la.')

        return 1

    def OnDropFiles(self, x, y, filenames):
        """
        Método executado em reação ao evento DropFiles de
        wx.FileDropTarget .
        :return bool
        """
        self.over.Hide()
        self.Draw(True)

        PostEvent("PopStatus")
        PostEvent("DropFiles", filenames)

        return True

    def OnLeave(self):
        """
        Método executado em reação ao evento Leave de
        wx.FileDropTarget .
        :return None
        """
        self.over.Hide()
        self.Draw(True)

        PostEvent("PopStatus")

    def OnMouseDown(self, event):
        """
        Método executado em reação ao evento MouseLeftDown.
        :return None
        """
        self.mousepos = Point(event.GetX(), event.GetY())
        event.Skip()

    def OnMouseUp(self, event):
        """
        Método executado em reação ao evento MouseLeftUp.
        :return None
        """
        self.mousepos = None

    def OnMotion(self, event):
        """
        Método executado em reação ao evento MouseMotion.
        :return None
        """
        if self.enable and self.mousepos is not None:
            shape = self.ilist[self.index].shape
            actual = Point(event.GetX(), event.GetY())
            _x, _y = self.pos + (actual - self.mousepos)

            _x = 0 if _x > 0 else _x
            _y = 0 if _y > 0 else _y

            _x = self.size.x - shape.x if -_x > shape.x - self.size.x else _x
            _y = self.size.y - shape.y if -_y > shape.y - self.size.y else _y

            self.mousepos = actual
            self.pos = Point(_x, _y)
            self.Refresh()

    def OnPaint(self, *args):
        """
        Método executado em reação ao evento OnPaint.
        :return None
        """
        #dc = wx.BufferedPaintDC(self)
        #dc.DrawBitmap(self.bmp, *self.pos if not self.hover else (0,0))