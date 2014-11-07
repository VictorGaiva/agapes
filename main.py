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
from segmentation import *
from component import *
from image import *
from line import *
import __builtin__
import threading
import wx
import os

__builtin__.__path__ = os.path.dirname(os.path.realpath(__file__))
__builtin__.__author__ = "Rodrigo Siqueira <rodriados@gmail.com>"
__builtin__.__version__ = '0.0.2'

# TODO:     Transformar equações utilizadas para funções paramétricas
#           permitindo, assim, aumentar o leque de curvas que podem
#           ser descritas.

# TODO:     Retirar a execução do programa diretamente do campo
#           de drag-n-drop.

# TODO:     Ao soltar uma imagem, exibí-la no campo de drag-n-drop
#           e permitir a edição da imagem diretamente desse campo.

# TODO:     Retirar o atributo global de  frame  e permitir que
#           todas as ações do programa sejam tomadas por MainWindow.
global frame

# TODO:     Adicionar ferramentas de edição de imagem na barra
#           horizontal inferior da janela.

class FileDrop(wx.FileDropTarget):
    
    def __init__(self, obj):
        super(FileDrop, self).__init__()
        
        self.imover = wx.BitmapFromImage(wx.Image(__path__ + "\\img\\dragover.png", wx.BITMAP_TYPE_ANY))
        self.obj = obj
        
    def OnDropFiles(self, x, y, filenames):
        self.obj.SetBitmap(self.original)
        del self.original
        
        t = threading.Thread(target = Run, args = (filenames))
        t.start()
        
        return True
        
    def OnEnter(self, *args):
        self.original = self.obj.GetBitmap()
        self.obj.SetBitmap(self.imover)
        self.obj.SetSize((740, 525))
        return 1
        
    def OnLeave(self, *args):
        self.obj.SetBitmap(self.original)
        self.obj.SetSize((740, 525))
        del self.original

class MainWindow(wx.Frame):
    
    def __init__(self, parent, id = wx.ID_ANY, title = ''):
        super(MainWindow, self).__init__(
            parent, id, title,
            size = (756, 592),
            style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN            
        )
        
        self.InitUI()
        self.Centre()
        self.Show()
    
    def InitUI(self):
        panel   = wx.Panel(self)
        midpan  = wx.Panel(panel)
        vertbox = wx.BoxSizer(wx.VERTICAL)
        contbox = wx.GridBagSizer(5, 5)
        hbarbox = wx.GridBagSizer(5, 5)
        disttxt = wx.StaticText(midpan, label = "Distância entre linhas:")
        distbox = wx.TextCtrl(midpan, -1, "1.5 metros")
        dstline = wx.StaticLine(midpan, style = wx.LI_VERTICAL, size = (1,24))
        resultx = wx.StaticText(midpan, label = "")
        
        imctrl  = wx.StaticBitmap(
            midpan, -1,
            wx.BitmapFromImage(wx.Image(__path__ + "\\img\\draghere.png", wx.BITMAP_TYPE_ANY)),
            size = (740, 525)
        )
        
        vertbox.Add(midpan, 1, wx.EXPAND | wx.ALL, 5)
        contbox.Add(imctrl, (0,0), flag = wx.ALIGN_LEFT | wx.ALIGN_TOP)
        contbox.Add(hbarbox, (1,0), flag = wx.ALIGN_LEFT | wx.ALIGN_TOP)
        hbarbox.Add(disttxt, (0,0), flag = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        hbarbox.Add(distbox, (0,1), flag = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        hbarbox.Add(dstline, (0,2), flag = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        hbarbox.Add(resultx, (0,3), flag = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
                
        dropt = FileDrop(imctrl)
        imctrl.SetDropTarget(dropt)
        
        panel.SetBackgroundColour('#CCCCCC')
        midpan.SetBackgroundColour('#CCCCCC')
        
        panel.SetSizer(vertbox)
        midpan.SetSizer(contbox)
        
        self.distancebox = distbox
        self.resultarea = resultx
                    
class MyApp(wx.App):
    
    def OnInit(self):
        global frame
        frame = MainWindow(None, -1, "PSG - Tecnologia Aplicada")
        self.SetTopWindow(frame)
        
        return True

def Parse(string):
    import re
    m = re.search(r"([0-9]*)[\.\,]?([0-9]*).*", string)
    return float(m.group(1) + "." + m.group(2))

def Run(file):
    image = Image.load(file).resize(.3)
    image = Segmentation().apply(image)

    comps = Component.load(image)
    
    if image.check(comps[1]):
        comps = Component.load(image)
    
    lines = Line.first(comps[1])

    lines.complete()
    pcent, meters = lines.error(Parse(frame.distancebox.GetValue()))
    frame.resultarea.SetLabel("Falhas encontradas: %.2f metros (%d%%)" % (meters, pcent))

if __name__ == '__main__':    
    app = MyApp()
    app.MainLoop()