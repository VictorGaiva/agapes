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
from controller.pipeline import high, segment
from controller.pipeline.singlestage import SingleStage
from core.image import Image, ImageWindow
from core.patch import Patch, PatchWork
from ..event import LinkEvent, EventBinder, PostEvent
from controller import ThreadWrapper
from os import path
import cv2 as cv
import wx

class Window(wx.Frame):
    """
    Objeto responsável pela criação e posicionamento
    de uma janela para segmentação avulsa de retalhos.
    """

    def __init__(self, parent, selection, wid = wx.ID_ANY, title = ''):
        """
        Cria uma nova instância do objeto.
        :param parent Janela superior à que deve ser criada.
        :param selection Seleção de retalhos.
        :param wid Identificador da nova janela a ser criada.
        :param title Título da nova janela.
        """
        self.selection = selection
        self.page = parent
        self.__train = [[],[]]

        wx.Frame.__init__(
            self, parent, wid, title,
            size = (150, 170),
            style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        )

        LinkEvent(self, wx.EVT_CLOSE, "SegClose", (self,))

        self.InitUI()
        self.InitOpenCVWindow()
        self.Show()

    def InitUI(self):
        """
        Constrói e posiciona os elementos utilizados pela janela nos
        locais corretos.
        """
        self.root = wx.Panel(self)

        self.terra = wx.ToggleButton(self.root, -1, "Terra")
        self.cana = wx.ToggleButton(self.root, -1, "Cana")
        self.teste = wx.Button(self.root, -1, "Testar")
        self.okay = wx.ToggleButton(self.root, -1, "OK")

        LinkEvent(self.terra, wx.EVT_TOGGLEBUTTON, "ButtonTerra", (self,))
        LinkEvent(self.cana, wx.EVT_TOGGLEBUTTON, "ButtonCana", (self,))
        LinkEvent(self.teste, wx.EVT_BUTTON, "ButtonTeste", (self,))
        LinkEvent(self.okay, wx.EVT_TOGGLEBUTTON, "ButtonSegOK", (self,))

        root = wx.BoxSizer(wx.VERTICAL)
        root.Add(self.terra, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 4)
        root.Add(self.cana, 0, wx.EXPAND | wx.ALL, 4)
        root.Add((1,1), 1, wx.EXPAND)
        root.Add(wx.StaticLine(self.root, style = wx.LI_HORIZONTAL), 0, wx.EXPAND)
        root.Add(self.teste, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 4)
        root.Add(self.okay, 0, wx.EXPAND | wx.ALL, 4)

        self.root.SetSizer(root)

    @EventBinder("SegClose")
    def OnSegClose(self, event):
        """
        Fecha a janela.
        """
        self.win.keep = False

    @EventBinder("ButtonTerra")
    def OnButtonTerra(self, event):
        """
        Callback para evento em ButtonTerra.
        """
        if event.Checked():
            print "Terra!"
            self.win.index = 0
            self.cana.SetValue(False)
            self.win.mousecontrol = self.TerraControl
        else:
            self.win.mousecontrol = True

    def TerraControl(self, event, x, y, flag, *param):
        """
        Controle de demarcação de terra.
        """
        if event == cv.EVENT_MOUSEMOVE and flag & cv.EVENT_FLAG_LBUTTON:
            cv.circle(self.win.image[0].raw, self.win.anchor + (x, y), 2, (0, 0,255), -1)
            self.__train[0].append(self.original[self.win.anchor + (x, y)][:])

    @EventBinder("ButtonCana")
    def OnButtonCana(self, event):
        """
        Callback para evento em ButtonCana.
        """
        if event.Checked():
            print "Cana!"
            self.win.index = 0
            self.terra.SetValue(False)
            self.win.mousecontrol = self.CanaControl
        else:
            self.win.mousecontrol = True

    def CanaControl(self, event, x, y, flag, *param):
        """
        Controle de demarcação de cana.
        """
        if event == cv.EVENT_MOUSEMOVE and flag & cv.EVENT_FLAG_LBUTTON:
            cv.circle(self.win.image[0].raw, self.win.anchor + (x, y), 2, (0, 255, 0), -1)
            self.__train[1].append(self.original[self.win.anchor + (x, y)][:])

    @EventBinder("ButtonTeste")
    def OnButtonTeste(self, event):
        """
        Callback para evento em ButtonTeste.
        """
        self.cana.SetValue(False)
        self.terra.SetValue(False)
        self.win.mousecontrol = True
        self.win.index = 1

        x = [[0,0,0]]
        y = [0]

        x = x + self.__train[0] + self.__train[1]
        y = y + [0] * len(self.__train[0]) + [255] * len(self.__train[1])

        comm = SingleStage(high, segment)
        comm.event = False

        for elem in self.selection._elems:
            comm.push(patch = elem.patch, train = [x, y])

        pwork = PatchWork(self.win.image[1], 200, 200)

        while comm.pendent:
            data = comm.pop()
            p = Patch(pwork, *data.patch.pos)
            p.sew(Image(cv.cvtColor(data.image.raw, cv.COLOR_GRAY2BGR)))

    @EventBinder("ButtonSegOK")
    @ThreadWrapper
    def OnButtonSegOK(self, event):
        """
        Callback para evento em ButtonSegOK
        """
        x = [[0,0,0]]
        y = [0]

        x = x + self.__train[0] + self.__train[1]
        y = y + [0] * len(self.__train[0]) + [255] * len(self.__train[1])

        self.win.keep = False

        comm = SingleStage(high, segment)
        comm2 = SingleStage(high, segment + 1)
        comm2.event, comm.event = False, False

        for i, e in enumerate(self.selection._elems):
            comm.push(patch = e.patch, distance = 1.5, id = i, train = [x, y])

        while comm.pendent:
            data = comm.pop()
            print "Pop segmented!, ", data.id
            img = data.image.colorize().normalize()

            self.page.drop.ChangeImage(1, data.patch, img)
            self.page.drop.ChangeImage(2, data.patch, img)
            img.save(self.page.path + path.sep + "segmented" + path.sep + str(data.id) + ".png")
            comm2.push(patch = data.patch, image = data.image, distance = data.distance, id = data.id, compmap = data.compmap)

        while comm2.pendent:
            data = comm2.pop()
            print "Pop processed {0}! {1} ".format(data.id, data.percent)
            self.page.drop.ChangeImage(2, data.patch, data.image.normalize())
            print data.percent
            e.Name.SetText("{0}%".format(data.percent))
            img.save(self.page.path + path.sep + "processed" + path.sep + str(data.id) + ".png")
            self.page.drop.Draw(True)
            self.page.drop.UpdateContagem()

        self.Close()

    def InitOpenCVWindow(self):
        """
        Inicializa janela que mostra a segmentação da imagem.
        """
        iorig = Image.new(self.page.drop.img.shape)
        isegm = Image.new(self.page.drop.img.shape)

        img = cv.cvtColor(self.page.drop.img.normalize(False).raw, cv.COLOR_RGB2BGR)
        pwork = PatchWork(iorig, 200, 200)
        plist = []

        for elem in self.selection._elems:
            p = Patch(pwork, *elem.patch.pos)
            p.sew(
                Image(cv.cvtColor(
                    self.page.drop.img.normalize(False)[
                        p.pos.x : p.pos.x + p.size.x,
                        p.pos.y : p.pos.y + p.size.y
                    ]
                    , cv.COLOR_RGB2BGR
                ))
            )
            plist.append(p)

        self.original = Image(pwork.raw).tolab()

        self.win = ImageWindow("Segmentar", pwork, 2, 0)
        self.win.append(isegm)
        self.win.index = 0
