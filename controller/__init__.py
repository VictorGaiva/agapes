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
from threading import Thread

__all__ = [
    "execute",
    "ThreadWrapper",
]

def execute(args):
    """
    Executa o algoritmo com os dados parâmetros. Eventos são
    disparados e podem ter tratamentos diferenciados dependendo
    do modo em que o programa está sendo executado: através de
    uma GUI ou a partir da linha de comando.
    :param args Argumentos passados à função.
    """
    from .pipeline import Pipeline
    md = __import__("ui" if args.gui else "cmd", globals(), locals(), [], -1)

    Pipeline.init()
    md.Init()
    Pipeline.stop()

def ThreadWrapper(function):
    """
    Invólucro de funções a serem executadas em um thread.
    :param function Função a ser envolvida.
    """
    def threadf(*args, **kwargs):
        t = Thread(target = function, args = args, kwargs = kwargs)
        t.start()
        return t

    return threadf
