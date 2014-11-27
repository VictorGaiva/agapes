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
from event import *
import os.path as path
import threading
import wx

# TODO: Adicionar suporte a abas, para processamento paralelo.

class FileDrop(wx.FileDropTarget):
    
    def __init__(self, obj):
        super(FileDrop, self).__init__()
        self.imover = wx.BitmapFromImage(wx.Image(path.join(__path__, "img", "dragover.png"), wx.BITMAP_TYPE_ANY))
        self.obj = obj
        
    def OnDropFiles(self, x, y, filenames):        
        self.obj.SetBitmap(self.original)        
        del self.original
        
        Event.dropped.trigger(filenames[0])
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
        distbox = wx.TextCtrl(midpan, -1, "1.5")
        dstline = wx.StaticLine(midpan, style = wx.LI_VERTICAL, size = (1,24))
        resultx = wx.StaticText(midpan, label = "")
        
        imctrl  = wx.StaticBitmap(
            midpan, -1,
            wx.BitmapFromImage(wx.Image(path.join(__path__, "img", "draghere.png"), wx.BITMAP_TYPE_ANY)),
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
                    
class AppMain(wx.App):
    
    def OnInit(self):
        self.frame = MainWindow(None, -1, __appname__)
        self.SetTopWindow(self.frame)
        
        return True
    
    def OnDrop(self, function):
        @ThreadWrapper
        def process(filename):
            function(filename, float(self.frame.distancebox.GetValue()))
        
        return process

def ThreadWrapper(function):
    """
    Invólucro de funções a serem executadas em um thread.
    @param lambda function Função a ser envolvida.
    """
    def threadf(*args, **kwargs):
        t = threading.Thread(target = function, args = args, kwargs = kwargs)
        t.start()
        
    return threadf

def InitGUI(function):
    """
    Inicializa a interface gráfica do usuário, o que
    permite que o programa seja utilizado sem a
    necessidade do uso de uma linha de comando.
    @param lambda function Função que realiza o processamento da imagem.
    """
    app = AppMain()
    Event.dropped = app.OnDrop(function)
        
    app.MainLoop()
    