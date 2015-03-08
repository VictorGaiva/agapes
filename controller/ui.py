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
from .pipeline import *
from . import ThreadWrapper
from threading import Condition
from core.patch import PatchWork
from gui.event import EventBinder, PostEvent, BindEvent
from gui import Init as Start
import os.path as path
import os

@EventBinder("ImageLoaded")
def OnImageLoaded(img, context):
    """
    Função invocada em reação ao evento ImageLoaded.
    :param img Imagem carregada.
    :param context Contexto de execução.
    """
    page, = context
    page.drop.SetImage(img.normalize(), *img.shape)

@EventBinder("ImageSegmented")
def OnImageSegmented(img, context):
    """
    Função invocada em reação ao evento ImageSegmented.
    :param img Imagem segmentada.
    :param context Contexto de execução.
    """
    page, patch = context
    image = img.colorize().normalize()

    page.drop.ChangeImage(1, patch, image)
    page.drop.ChangeImage(2, patch, image)

@EventBinder("ImageProcessed")
def OnImageProcessed(img, pcent, count, context):
    """
    Função invocada em reação ao evento ImageProcessed.
    :param img Imagem processada.
    :param pcent Porcentagem de falhas.
    :param count É uma amostra aleatória selecionada?
    :param context Contexto de execução.
    """
    page, patch = context
    image = img.normalize()

    page.drop.ShowLocalResult(patch, pcent, count >= normal)
    page.drop.ChangeImage(2, patch, image)

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

        page.comm = Communication()
        page.comm.push(load, normal, args = (filename,))

        img, = page.comm.response()
        page.patchw = PatchWork(img, 200, 200)
        PostEvent("ImageLoaded", page.patchw, context = (page,))
        page.path = path.splitext(filename)[0]

        try:
            os.makedirs(page.path + path.sep + "segmented")
            os.makedirs(page.path + path.sep + "processed")
        except:
            pass

        page.lock.wait()

        yes, no = page.patchw.chop().choose(0.6)
        page.comm.pushmany(segment, normal, [[(p.image,), (p,)] for p in yes])
        page.comm.pushmany(segment,    low, [[(p.image,), (p,)] for p in no])

        scount = 0
        pcount = 0

        while page.comm.pendent():
            response = page.comm.response()

            if response.stage == segment:
                image, cmap = response
                context = (page,) + response.context
                image.save(page.path + path.sep + "segmented" + path.sep + "{0}.png".format(scount))
                scount = scount + 1
                PostEvent("ImageSegmented", image, context = context)
                page.comm.push(process, response.priority, args = (cmap, page.dnum.Value), context = response.context)

            elif response.stage == process:
                image, pcent, meter = response
                context = (page,) + response.context
                image.save(page.path + path.sep + "processed" + path.sep + "{0}.png".format(pcount))
                pcount = pcount + 1
                PostEvent("ImageProcessed", image, pcent, response.priority, context = context)

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