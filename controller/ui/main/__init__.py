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

class Control(object):
    """
    Controla e administra a execução de toda a
    janela de interface gráfica através dos
    eventos disparados.
    """

    def __init__(self):
        """
        Inicializa uma nova instância.
        :return Control
        """
        self.pages = []
        self.win = None

    @property
    def count(self):
        """
        Retorna a contagem de páginas registradas no
        livro de abas.
        :return int
        """
        return len(self.pages)

    def register(self, page):
        """
        Registra uma nova página. Permite rastrear e
        manter referências das páginas existentes da
        janela.
        :param page Nova página a ser registrada.
        """
        self.pages.append(page)

    def bind(self, window):
        """
        Vincula uma janela ao controlador.
        :param window Janela a ser vinculada.
        """
        self.win = window

        Event("NewPage", self.win.book).bind(self.newpage)

    def newpage(self, book, page):
        """
        Callback ao evento NewPage sobre win.book.
        :param book Objeto alvo do evento.
        :param page Página que disparou o evento.
        :return Control[Page]
        """
        return book.add(page.__class__, u"#{0}".format(self.count - 2))
