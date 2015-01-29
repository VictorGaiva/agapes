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
from .event import BindEvent
import wx

class StatusBar(wx.StatusBar):
    """
    Objeto responsável pela criação, controle e administração
    da barra de status da aplicação.
    """

    def __init__(self, parent):
        """
        Cria uma nova instância do objeto.
        :param parent Janela-pai da janela atual.
        :return Menu
        """
        wx.StatusBar.__init__(
            self, parent, -1,
            style = wx.STB_SHOW_TIPS | wx.STB_ELLIPSIZE_END | wx.ST_SIZEGRIP
        )

        self.parent = parent
        self.SetFieldsCount(1)

        parent.SetStatusBar(self)
        self.BindEvents()

    def Push(self, message):
        """
        Adiciona uma nova mensagem à pilha de mensagens da barra
        de status da janela atual.
        :param message Nova mensagem a ser empilhada.
        """
        self.PushStatusText(message, 0)

    def Pop(self):
        """
        Remove uma mensagem da pilha de mensagens da barra
        de status da janela atual.
        """
        self.PopStatusText(0)

    def BindEvents(self):
        """
        Víncula métodos do objeto a eventos que podem ser disparados.
        :return None
        """
        BindEvent("PopStatus", self.Pop)
        BindEvent("PushStatus", self.Push)
