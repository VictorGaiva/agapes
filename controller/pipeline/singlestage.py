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
from . import Pipeline, load, process, low, high
from .communication import Communication
from .container import Container

class SingleStage(Communication):
    """
    Facilita o envio de objetos para a execução em um
    único estágio do pipeline.
    """

    def __init__(self, priority, stage, **context):
        """
        Inicializa um novo objeto para execução do pipeline.
        :param priority Prioridade de execução desta comunicação.
        :param stage Estágio de destino de execução.
        :param context Contexto de execução.
        :return SingleStage
        """
        Communication.__init__(self, priority, **context)
        self.stage = stage

    def push(self, **args):
        """
        Adiciona uma tarefa a ser executada pelo
        estágio do pipeline.
        :param args Argumentos a serem passados ao pipeline.
        """
        if load <= self.stage <= process:
            if low <= self.priority <= high:
                data = Container(**args)
                self._sent = self._sent + 1
                Pipeline.push(self.stage, self.priority, self, data)

    def pop(self):
        """
        Resgata da pilha valores retornados pelos estágios
        de execução do pipeline. Esse método esperará o
        término de execução no pipeline de um novo objeto
        caso ainda exista objetos pendentes em execução.
        :return Container
        """
        if not self.pendent:
            return None

        data = self._ready.get()[1]
        self._received = self._received + 1

        return data
