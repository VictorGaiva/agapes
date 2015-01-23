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
from util import *
import config
import os.path as path
import threading
import wx

win = HierarchicalJar(
    size = (800, 600)
)

class AppMain(wx.App):
    """
    Objeto responsável pela criação e coordenação geral das
    ações aplicadas por e realizadas sobre a janela.
    """

    def OnInit(self):
        """
        Inicializa exibição da GUI.
        :return None
        """
        win.main = MainWindow(None, -1, config.appname)
        self.SetTopWindow(win.main)

        return True


    @classmethod
    def OnDrop(cls, function):
        """
        Prepara função a ser executada quando uma imagem é solta sobre
        o campo indicado na janela.
        """
        @ThreadWrapper
        def process(filename):
            function(filename, float(win.main.distance))

        return process


class NotePage(wx.Panel):
    """
    Objeto responsável por inicializar, controlar e administrar uma
    página do notebook.
    """

    def __init__(self, parent):
        """
        Cria uma nova instância do objeto.
        :param parent Janela-pai da janela atual.
        """
        super(NotePage, self).__init__(
            parent, -1
        )

        self.sz, self.el = Factory(HierarchicalJar).createmany(2)

        self.sz.wrap = wx.BoxSizer()
        self.el.wrap = wx.Panel(self, size = (800, 483))

        self.SetSizer(self.sz.wrap)
        self.sz.all = wx.BoxSizer(wx.HORIZONTAL)

        self.sz.wrap.Add((2, 0), 0)
        self.sz.wrap.Add(self.el.wrap, 0, wx.RIGHT | wx.TOP, 4)
        self.el.wrap.SetSizer(self.sz.all)

        self.sz.left = wx.BoxSizer(wx.VERTICAL)
        self.sz.right = wx.BoxSizer(wx.VERTICAL)

        self.sz.all.Add(self.sz.left, 3, wx.EXPAND | wx.RIGHT, 5)
        self.sz.all.Add(wx.StaticLine(self.el.wrap, style = wx.LI_VERTICAL), 0, wx.EXPAND | wx.RIGHT, 4)
        self.sz.all.Add(self.sz.right, 1, wx.EXPAND)

        self.dropfield = wx.StaticBitmap(
            self.el.wrap, -1,
            wx.BitmapFromImage(win.img.draginit),
            size = (100, 453)
        )

        self.sz.tools = wx.BoxSizer(wx.HORIZONTAL)

        self.sz.left.Add(self.dropfield, 0, wx.EXPAND | wx.BOTTOM, 5)
        self.sz.left.Add(self.sz.tools, 1, wx.EXPAND)

        self.sample = wx.SpinCtrl(
            self.el.wrap, -1, "", size = (60, 25),
            min = 20, max = 90, initial = 60
        )

        self.sz.tools.Add(
            wx.StaticText(self.el.wrap, -1, "Amostras:"), 0,
            wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5
        )

        self.sz.tools.Add(self.sample, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.sz.tools.Add(
            wx.StaticText(self.el.wrap, -1, "%"), 0,
            wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5
        )

        self.el.b.imorig = wx.ToggleButton(self.el.wrap, -1, "Orig", size = (25, 25))
        self.el.b.imsegm = wx.ToggleButton(self.el.wrap, -1, "Segment", size = (25, 25))
        self.el.b.imline = wx.ToggleButton(self.el.wrap, -1, "Lined", size = (25, 25))

        self.sz.tools.Add((10,10), 1, wx.EXPAND)
        self.sz.tools.Add(self.el.b.imorig, 0, wx.ALIGN_RIGHT | wx.LEFT, 4)
        self.sz.tools.Add(self.el.b.imsegm, 0, wx.ALIGN_RIGHT | wx.LEFT, 4)
        self.sz.tools.Add(self.el.b.imline, 0, wx.ALIGN_RIGHT | wx.LEFT, 4)

        self.sz.infos = wx.GridBagSizer(5, 5)
        self.sz.right.Add(self.sz.infos, 1, wx.EXPAND)

        self.sz.infos.Add((100,100), (0,0), (1,2), wx.EXPAND)

        self.sz.infos.Add(
            wx.StaticText(self.el.wrap, -1, u"Fazenda:"),
            (1,0), (1,2), wx.EXPAND
        )

        self.el.farm = wx.ComboBox(
            self.el.wrap, -1, "", choices = [],
            size = (191, 25),
            style = wx.CB_DROPDOWN
        )

        self.sz.infos.Add(self.el.farm, (2,0), (1,2), wx.EXPAND)

        self.sz.infos.Add(
            wx.StaticText(self.el.wrap, 1, u"Talhão:"),
            (3,0), (1,2), wx.EXPAND
        )

        self.el.field = wx.TextCtrl(
            self.el.wrap, -1, "",
            size = (191, 25)
        )

        self.sz.infos.Add(self.el.field, (4,0), (1,2), wx.EXPAND)

        self.sz.infos.Add(
            wx.StaticText(self.el.wrap, 1, u"Distância entre linhas:"),
            (5,0), (1,2), wx.EXPAND
        )

        self.el.dist.number = wx.SpinCtrlDouble(
            self.el.wrap, -1, initial = 1.50,
            min = .00, max = 50., inc = .25,
            size = (70, 25)
        )

        self.el.dist.number.SetDigits(2)
        self.sz.infos.Add(self.el.dist.number, (6,0), (1,1), wx.EXPAND)

        self.el.dist.type = wx.Choice(
            self.el.wrap, -1,
            choices = [u"centímetros", u"metros", u"polegadas", u"pés", u"jardas"],
            size = (90, 23)
        )

        self.el.dist.type.SetSelection(1)
        self.sz.infos.Add(self.el.dist.type, (6,1), (1,1), wx.EXPAND)

        self.sz.infos.Add(
            wx.StaticLine(self.el.wrap, style = wx.LI_HORIZONTAL),
            (7,0), (1,2), wx.EXPAND | wx.TOP | wx.BOTTOM, 5
        )

        self.el.b.run = wx.Button(self.el.wrap, -1, "Processar")
        self.el.b.dlt = wx.Button(self.el.wrap, -1, "Fechar")

        self.sz.infos.Add(self.el.b.run, (8,0), (1,1), wx.EXPAND)
        self.sz.infos.Add(self.el.b.dlt, (8,1), (1,1), wx.EXPAND)


class MainWindow(wx.Frame):
    """
    Objeto responsável pelo posicionamento e controle de elementos
    na janela principal da aplicação.
    """

    def __init__(self, parent, wid = wx.ID_ANY, title = ''):
        """
        Cria uma nova instância do objeto.
        :param parent Janela-pai da janela atual.
        :param wid Identificador da nova janela a ser criada.
        :param title Título da nova janela.
        """
        super(MainWindow, self).__init__(
            parent, wid, title,
            size = win.size,
            style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        )

        self.InitMenu()
        self.InitUI()
        self.InitStatus()

        self.Centre(wx.BOTH)
        self.Show()


    def InitMenu(self):
        """
        Constrói e prosiciona o menu de ferramentas na janela.
        :return None
        """
        win.menu = wx.MenuBar()

        win.menu.file = wx.Menu()
        m_quit = win.menu.file.Append(wx.ID_EXIT, u'Sair', u'Sair da aplicação.')

        win.menu.Append(win.menu.file, u'&Arquivo')

        self.Bind(wx.EVT_MENU, self.OnQuit, m_quit)

        self.SetMenuBar(win.menu)


    def InitUI(self):
        """
        Constrói e posiciona os elementos utilizados pela janela nos locais
        corretos.
        :return None
        """
        win.box.root = wx.Panel(self)
        win.notebook = wx.Notebook(win.box.root, -1, style = wx.BK_TOP | wx.NB_MULTILINE)

        win.sizer.wrap = wx.BoxSizer()
        win.sizer.wrap.Add(win.notebook, 1, wx.EXPAND | wx.ALL, 5)
        win.box.root.SetSizer(win.sizer.wrap)

        win.img.draginit = wx.Image(path.join(config.path, "img", "draghere.png"), wx.BITMAP_TYPE_ANY)
        win.img.dragover = wx.Image(path.join(config.path, "img", "dragover.png"), wx.BITMAP_TYPE_ANY)

        win.notebook.AddPage(NotePage(win.notebook), u"Planilha")
        win.notebook.AddPage(NotePage(win.notebook), u"Talhões")

        win.notebook.ChangeSelection(1)


    def InitUIAntigo(self):
        """
        Constrói e posiciona os elementos utilizados pela janela nos locais
        corretos.
        :return None
        """
        #rightimg = wx.StaticBitmap(
        #    win.box.right, -1,
        #    wx.BitmapFromImage(wx.Image(path.join(config.path, "img", "rightside.png"), wx.BITMAP_TYPE_ANY)),
        #    size = (76, 50)
        #)

        #win.sizer.right.Add(rightimg, 1, wx.EXPAND | wx.BOTTOM, 5)

        win.sizer.wrap = wx.BoxSizer(wx.HORIZONTAL)

        win.box.root = wx.Panel(self)
        win.box.root.SetSizerAndFit(win.sizer.wrap)

        win.sizer.root = wx.GridBagSizer(5, 5)
        win.sizer.wrap.Add(win.sizer.root, 1, wx.EXPAND | wx.ALL, 5)

        #win.box.ltopleft = wx.Panel(win.box.root, size = (100,100))
        #win.box.ltopleft.SetBackgroundColour("#FF0000")
        win.slider = wx.Slider(
            win.box.root, -1, 50, 0, 100,
            wx.DefaultPosition, (35, 470),
            wx.SL_VERTICAL | wx.SL_AUTOTICKS | wx.SL_LEFT | wx.SL_MIN_MAX_LABELS | wx.SL_INVERSE
        )

        win.dropfield = wx.StaticBitmap(
            win.box.root, -1,
            wx.BitmapFromImage(wx.Image(path.join(config.path, "img", "draghere.png"), wx.BITMAP_TYPE_ANY)),
            size = (687, 470)
        )

        win.box.lbottom = wx.Panel(win.box.root, size = (35,35))
        win.box.lbottom.SetBackgroundColour("#0000FF")

        win.box.right = wx.Panel(win.box.root, size = (100,100))
        win.box.right.SetBackgroundColour("#FFFF00")

        win.sizer.root.Add(win.dropfield,    (0,0), (1,1), wx.EXPAND)
        win.sizer.root.Add(win.slider,       (0,1), (1,1), wx.EXPAND)
        win.sizer.root.Add(win.box.lbottom,  (1,0), (1,2), wx.EXPAND)

        win.sizer.root.Add(wx.StaticLine(
            win.box.root, -1,
            style = wx.VERTICAL
        ),                                   (0,2), (2,1), wx.EXPAND)

        win.sizer.root.Add(win.box.right,    (0,3), (2,1), wx.EXPAND)


    def InitStatus(self):
        """
        Inicializa a barra de status da janela atual.
        :return None
        """
        win.status = self.CreateStatusBar(
            2,
            wx.STB_SHOW_TIPS | wx.STB_ELLIPSIZE_END | wx.ST_SIZEGRIP
        )

        win.status.SetFieldsCount(1)
        win.status.PushStatusText(u"Carregamento concluído.", 0)


    def OnQuit(self, event):
        """
        Método a ser chamado quando o programa estiver sendo fechado.
        :param event Dados sobre o evento engatilhado.
        :return None
        """
        self.Close()


def ThreadWrapper(function):
    """
    Invólucro de funções a serem executadas em um thread.
    :param function Função a ser envolvida.
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
    :param function Função que realiza o processamento da imagem.
    """
    Event.listen("dropped", AppMain.OnDrop(function))

    app = AppMain()
    app.MainLoop()
