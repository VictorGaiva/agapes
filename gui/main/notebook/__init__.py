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
from controller.ui.page import Control
import wx

class Notebook(wx.Notebook):
    """
    Elemento de interface gráfica responsável pela
    criação e gerenciamento de abas.
    """

    def __init__(self, parent, style):
        """
        Inicializa uma nova instância.
        :param parent Janela ou painel superior em hierarquia.
        :param style Estilos do elemento de interface gráfica.
        :return Notebook
        """
        wx.Notebook.__init__(self, parent.root, -1, style = style)

        self.parent = parent
        self.pages = []

    def __getitem__(self, index):
        """
        Permite recuperar uma página a partir de seu
        número de índice.
        :param index Índice da página a ser recuperada.
        :return Panel
        """
        return self.pages[index]                        \
            if 0 <= index < self.count                  \
            else None

    @property
    def count(self):
        """
        Retorna a contagem de páginas registradas no
        livro de abas.
        :return int
        """
        return len(self.pages)

    def current(self):
        """
        Retorna a página atualmente selecionada no livro
        de abas. Esta página é a que está atualmente visível.
        :return Panel
        """
        return self.GetCurrentPage()

    def add(self, PType, title, inicial = False, *args, **kwargs):
        """
        Cria e adiciona uma nova página ao livro.
        :param PType Tipo de página a ser criada.
        :param title Título da nova página.
        :param inicial É a página inicial do software.
        :param args Argumentos de posição extras da página.
        :param kwargs Argumentos nominais extras da página.
        :return controller.ui.page.Control
        """
        pctrl = Control[PType](self.parent.control, inicial)
        npage = PType(pctrl, self, inicial, *args, **kwargs)

        self.AddPage(npage, title)
        self.pages.append(npage)

        return pctrl
