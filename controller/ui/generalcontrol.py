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
from gui.event import PostEvent, BindEvent
from gui.notepage import NotePage

from ..pipeline.singlestage import SingleStage
from ..pipeline.multistage import MultiStage
from ..pipeline import *
from .. import ThreadWrapper

class GeneralControl(object):
    """
    Controla e administra a execução de toda a
    interface gráfica através dos eventos
    disparados.
    """

    def __init__(self):
        """
        Inicializa uma nova instância.
        :return GeneralControl
        """
        self._count = 0
        self._pages = []
        self._window = None

    def bind(self, window):
        """
        Vincula uma janela a esse controlador.
        :param window Janela a ser vinculada.
        """
        BindEvent("DropFiles", self.OnDropFiles)
        BindEvent("NewPage", self.OnNewPage)
        BindEvent("PageChanged", self.OnPageChanged)
        self._window = window

        #Page events below
        self.book = self._window.book
        BindEvent("GridButton", self.OnGridButton)
        BindEvent("PhaseButton", self.OnPhaseButton)
        BindEvent("RunPage", self.OnRunPage)
        BindEvent("ClosePage", self.OnClosePage)
        BindEvent("UpdateContagem", self.OnUpdateContagem)

        BindEvent("ButtonSOK", self.OnButtonSOK)
        BindEvent("ButtonSAdd", self.OnButtonSAdd)
        BindEvent("ButtonSRemove", self.OnButtonSRemove)
        BindEvent("ButtonSSegment", self.OnButtonSSegment)

        BindEvent("SelectionAdd", self.OnSelectionAdd)
        BindEvent("SelectionRemove", self.OnSelectionRemove)
        BindEvent("SelectionClean", self.OnSelectionClean)

    def OnDropFiles(self, filenames):
        """
        Método executado assim que o evento DropFiles é disparado.
        Este método cria uma nova aba e permite que uma imagem
        seja processada.
        :param filenames Nome dos arquivos a serem processados.
        :return None
        """
        for filename in filenames:
            newpage = NotePage.FromActive(self._window.book)
            PostEvent("NewPage", newpage, filename)

            self._count = self._count + 1
            self._window.book.AddPage(newpage, "#{0}".format(self._count))

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
        page.comm.pop()
        page.lock.wait()

        page.comm = MultiStage(normal, segment, process, page = page)
        yes, no = page.patchw.chop().choose(0)

        for i, p in enumerate(no):
            page.comm.push(patch = p, distance = page.dnum.GetValue(), id = i)

        page.comm.consume()
        page.lock.release()

    def OnPageChanged(self, e):
        """
        Método executado quando o evento PageChanged é disparado.
        Esse evento é utilizado para redesenhar o resultado do
        algoritmo.
        """
        self._window.book.GetCurrentPage().drop.Draw(True)






    #Page methods below
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

    def OnButtonSOK(self, page, event):
        """
        Método executado em resposta ao evento ButtonSOK
        """
        while page.drop.selection._count > 0:
            for elem in page.drop.selection._elems:
                elem.S.Hide()
                elem.Name.Show()
                page.drop.selection.remove(elem)

        page.drop.selection.clean()
        page.drop.Draw(True)

    def OnButtonSAdd(self, page, event):
        """
        Método executado em resposta ao evento ButtonSAdd
        """
        for elem in page.drop.selection._elems:
            if elem.Name not in page.drop.incount:
                page.drop.outcount.remove(elem.Name)
                page.drop.incount.append(elem.Name)
                elem.Name.Color = "Green"

        page.drop.UpdateContagem()
        page.drop.Draw(True)

    def OnButtonSRemove(self, page, event):
        """
        Método executado em resposta ao evento ButtonSRemove
        """
        for elem in page.drop.selection._elems:
            if elem.Name in page.drop.incount:
                page.drop.incount.remove(elem.Name)
                page.drop.outcount.append(elem.Name)
                elem.Name.Color = "Red"

        page.drop.UpdateContagem()
        page.drop.Draw(True)

    def OnButtonSSegment(self, page, event):
        """
        Método executado em resposta ao evento ButtonSSegment
        """
        from gui.segmentation import Window
        self.__win = Window(page, page.drop.selection, -1, u"Controle de segmentação")

    def OnSelectionAdd(self, selection):
        """
        Método executado em resposta ao evento SelectionAdd
        """
        selection.page.sokay.Enable()
        selection.page.sadd.Enable()
        selection.page.sremove.Enable()
        selection.page.sseg.Enable()
        selection.page.stxt.SetLabel(
            "{0} retalho{1} selecionado{1}.".format(
                selection._count, "s" if selection._count > 1 else ""
            )
        )

    def OnSelectionRemove(self, selection):
        """
        Método executado em resposta ao evento SelectionRemove
        """
        if selection._count == 0:
            selection.page.sokay.Disable()
            selection.page.sadd.Disable()
            selection.page.sremove.Disable()
            selection.page.sseg.Disable()
            selection.page.stxt.SetLabel("")

        else:
            selection.page.stxt.SetLabel(
                "{0} retalho{1} selecionado{1}.".format(
                    selection._count, "s" if selection._count > 1 else ""
                )
            )

    def OnSelectionClean(self, selection):
        """
        Método executado em resposta ao evento SelectionClean
        """
        selection.page.sokay.Disable()
        selection.page.sadd.Disable()
        selection.page.sremove.Disable()
        selection.page.sseg.Disable()
        selection.page.stxt.SetLabel("")
