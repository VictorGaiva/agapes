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
from threading import Condition
from core.patch import PatchWork
from gui.event import EventBinder, PostEvent, BindEvent
from gui import Init as Start
from .pipeline.communication import Communication
from .pipeline.multistage import MultiStage
from .pipeline.singlestage import SingleStage
from .pipeline import *
from . import ThreadWrapper
import os.path as path
import shutil
import os

@EventBinder("ImageLoaded")
def OnImageLoaded(data, context):
    """
    Função invocada em reação ao evento ImageLoaded.
    :param data Dados de execução.
    :param context Contexto de execução.
    """
    img = data.image
    page = context.page

    page.patchw = PatchWork(img, 200, 200)
    page.path = path.splitext(data.address)[0]

    if path.isdir(page.path):
        shutil.rmtree(page.path)

    os.makedirs(page.path + path.sep + "segmented")
    os.makedirs(page.path + path.sep + "processed")

    page.drop.SetImage(img.normalize(), *img.shape)

@EventBinder("ImageSegmented")
def OnImageSegmented(data, context):
    """
    Função invocada em reação ao evento ImageSegmented.
    :param data Dados de execução.
    :param context Contexto de execução.
    """
    page = context.page
    image, nm = data.image, data.id
    image = image.colorize().normalize()

    page.drop.ChangeImage(1, data.patch, image)
    page.drop.ChangeImage(2, data.patch, image)
    image.save(page.path + path.sep + "segmented" + path.sep + str(nm) + ".png")

@EventBinder("ImageProcessed")
def OnImageProcessed(data, context):
    """
    Função invocada em reação ao evento ImageProcessed.
    :param data Dados de execução.
    :param context Contexto de execução.
    """
    page = context.page
    image, nm = data.image, data.id
    image = image.normalize()

    page.drop.ChangeImage(2, data.patch, image)
    page.drop.ShowLocalResult(data.patch, data.percent, True)
    image.save(page.path + path.sep + "processed" + path.sep + str(nm) + ".png")

class Controller(object):
    """
    Objeto responsável pelo controle da execução do
    algoritmo e administração de eventos engatilhados pela
    interface de usuário.
    """

    def __init__(self):
        """
        Inicializa nova instância do objeto.
        :return Controller
        """
        self.win = 0
        self.book = None

        self.BindEvents()

    def OnDropFiles(self, filenames):
        """
        Método executado assim que o evento DropFiles é disparado.
        Este método cria uma nova aba e permite que uma imagem
        seja processada.
        :param filenames Nome dos arquivos a serem processados.
        :return None
        """
        from gui.notepage import NotePage

        for filename in filenames:
            newpage = NotePage.FromActive(self.book)
            PostEvent("NewPage", newpage, filename)

            self.book.AddPage(newpage, "#{0}".format(self.win))
            self.win = self.win + 1

    def OnGridButton(self, event):
        """
        Método responsável pelo tratamento do evento de visão
        de grade da imagem.
        :param event Objeto alvo do evento.
        """
        self.book.GetCurrentPage().drop.ShowGrid(
            event.Checked()
        )

    def OnPhaseButton(self, event):
        """
        Método executado em reação ao evento ToggleButton de algum
        dos botões de visualização de passos do algoritmo.
        :param event Objeto alvo do evento.
        """
        page = self.book.GetCurrentPage()

        for b in page.phase:
            b.SetValue(b.GetId() == event.GetId())

        page.drop.ShowIndex(event.GetId() - 1)
        event.Skip()

    @ThreadWrapper
    def OnNewPage(self, page, filename):
        """
        Função invocada em reação ao evento NewPage.
        :param page Página recém-criada.
        :param filename Arquivo de imagem a ser processada.
        """
        page.lock = Condition()
        page.lock.acquire()

        page.comm = SingleStage(normal, load, page = page)
        page.comm.push(address = filename)

        img = page.comm.pop().image
        page.lock.wait()

        page.comm = MultiStage(normal, segment, process, page = page)
        yes, no = page.patchw.chop().choose(1)

        for i, p in enumerate(yes):
            page.comm.push(patch = p, distance = 1.5, id = i)

        page.comm.consume()
        page.lock.release()

    def OnPageChanged(self, e):
        """
        Método executado quando o evento PageChanged é disparado.
        Esse evento é utilizado para redesenhar o resultado do
        algoritmo.
        """
        self.book.GetCurrentPage().drop.Draw(True)

    def OnRunPage(self, e):
        """
        Executa o algoritmo na página. Os dados serão obtidos
        diretamente das informações passadas ao controlador.
        """
        page = self.book.GetCurrentPage()
        page.lock.acquire()
        page.lock.notify()
        page.lock.release()

    def OnClosePage(self, *e):
        """
        Encerra uma página do Notebook. Todos os dados
        contidos na página serão apagados.
        """
        if self.book.GetSelection() > 1:
            self.book.DeletePage(self.book.GetSelection())

    def OnUpdateContagem(self, target, total, count):
        """
        Atualiza resultado.
        """
        target.result.SetLabel(u"{0}%".format(total))
        target.count.SetLabel(u"{0} amostras".format(count))

    def BindEvents(self):
        """
        Víncula métodos do objeto a eventos que podem ser disparados.
        :return None
        """
        BindEvent("DropFiles", self.OnDropFiles)
        BindEvent("GridButton", self.OnGridButton)
        BindEvent("PhaseButton", self.OnPhaseButton)
        BindEvent("NewPage", self.OnNewPage)
        BindEvent("PageChanged", self.OnPageChanged)
        BindEvent("RunPage", self.OnRunPage)
        BindEvent("ClosePage", self.OnClosePage)
        BindEvent("UpdateContagem", self.OnUpdateContagem)

def Init(args):
    """
    Inicializa a execução da interface gráfica de usuário.
    Dessa forma, precisamos aguardar pelo usuário para que
    algum processamento inicie.
    :param args Argumentos passados pela linha de comando.
    """
    control = Controller()
    Start(control)