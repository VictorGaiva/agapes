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
from Queue import Queue
from gui.event import PostEvent
from .container import Container
from . import *

class Communication(object):
    """
    Controle de comunicação entre threads e execução
    do Pipeline.
    """

    def __init__(self, priority, **context):
        """
        Inicializa um novo objeto para execução do pipeline.
        :param priority Prioridade de execução desta comunicação.
        :param context Contexto de execução.
        :return Communication
        """
        self.event = True       # Invocar eventos de conclusão de passos?
        self.priority = priority
        self.context = Container(**context)

        self._ready = Queue()
        self._sent, self._received = 0, 0

    def push(self, stage, **args):
        """
        Adiciona uma tarefa a ser executada pelos
        estágios do pipeline.
        :param stage Estágio alvo para execução.
        :param args Argumentos a serem passados ao pipeline.
        """
        if load <= stage <= process:
            if low <= self.priority <= high:
                data = Container(**args)
                self._sent = self._sent + 1
                Pipeline.push(stage, self.priority, self, data)

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
            PostEvent(stagename[stage], data, self.context)

        self._ready.put( (stage, data) )

    def pop(self):
        """
        Resgata da pilha valores retornados pelos estágios
        de execução do pipeline. Esse método esperará o
        término de execução no pipeline de um novo objeto
        caso ainda exista objetos pendentes em execução.
        :return tuple
        """
        if not self.pendent:
            return None

        data = self._ready.get()
        self._received = self._received + 1

        return data

    def consume(self):
        """
        Aguarda o término de execução de todos os objetos
        que se encontram na fila de execução do pipeline.
        """
        while self.pendent:
            self.pop()

    @property
    def pendent(self):
        """
        Verifica se existem tarefas pendentes cujo
        processamento no pipeline ainda não foi terminado.
        :return bool Há tarefas pendentes?
        """
        return self._sent != self._received
