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
from ..event import Event
from . import Pipeline, load, process, low, high, stagename
from .communication import Communication
from .container import Container

class MultiStage(Communication):
    """
    Facilita o envio de objetos para a execução em vários
    estágios do pipeline de forma sequencial.
    """

    def __init__(self, priority, first = load, last = process, **context):
        """
        Inicializa um novo objeto para execução do pipeline.
        :param priority Prioridade de execução desta comunicação.
        :param first Estágio inicial de execução.
        :param last Estágio final de execução.
        :param context Contexto de execução.
        :return MultiStage
        """
        Communication.__init__(self, priority, **context)
        self.first, self.last = first, last

    def push(self, **args):
        """
        Adiciona uma tarefa a ser executada pelos
        estágios do pipeline.
        :param args Argumentos a serem passados ao pipeline.
        """
        if load <= self.first <= self.last <= process:
            if low <= self.priority <= high:
                data = Container(**args)
                self._sent = self._sent + 1
                Pipeline.push(self.first, self.priority, self, data)

    def notify(self, stage, data, response):
        """
        Recebe a resposta de um estágio do pipeline e
        trata a resposta de acordo com o necessário para
        a execução da tarefa. Esse método é sempre executado
        pelos threads do pipeline.
        :param stage Estágio de origem da resposta.
        :param data Dados armazenados pela execução.
        :param response Resposta produzida pelo estágio.
        """
        data.update(**response)

        if self.event and stage > -1:
            Event(stagename[stage]).post(data, self.context)

        if -1 < stage < self.last:
            Pipeline.push(stage + 1, self.priority, self, data)
        else:
            self._ready.put( (stage, data) )

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
