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
from .event import *
from .appmain import *
import threading

__all__ = [
    "util",
    "event",
    "InitGUI",
]

def ThreadWrapper(function):
    """
    Invólucro de funções a serem executadas em um thread.
    :param function Função a ser envolvida.
    """
    def threadf(*args, **kwargs):
        t = threading.Thread(target = function, args = args, kwargs = kwargs)
        t.start()

    return threadf

def InitGUI():
    """
    Inicializa a interface gráfica do usuário, o que
    permite que o programa seja utilizado sem a
    necessidade do uso de uma linha de comando.
    """
    app = AppMain()
    app.MainLoop()
