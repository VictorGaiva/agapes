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
from . import ThreadWrapper
from Queue import Queue
import core
import time

_queues = [
    [Queue(), Queue(), Queue()],
    [Queue(), Queue(), Queue()],
    [Queue(), Queue(), Queue()]
]

low, normal, high = range(3)
load, segment, process = range(3)
_alive = True

class Communication(object):
    """
    Objeto responsável pelo controle da comunicação
    de um thread com o Pipeline.
    """

    def __init__(self):
        """
        Inicializa uma nova instância do objeto.
        :return Communication
        """
        self.queue = Queue()
        self.sent, self.received = 0, 0

    def push(self, stage, priority = normal, args = (), context = ()):
        """
        Adiciona uma tarefa a ser executada por um
        dos estágios do pipeline.
        :param stage Estágio alvo das tarefas.
        :param priority Prioridade de execução da tarefa.
        :param args Argumentos de posição da tarefa.
        :param context Dados de contexto.
        """
        if load <= stage <= process and low <= priority <= high:
            _queues[stage][priority].put( (self.queue, args, context) )
            self.sent = self.sent + 1

    def pushmany(self, stage, priority = normal, content = []):
        """
        Adiciona várias tarefas a serem executadas por
        um dos estágios do pipeline.
        :param stage Estágio alvo das tarefas.
        :param priority Prioridade de execução da tarefa.
        :param content Lista de argumentos e dados de contexto.
        """
        for argnctxt in content:
            self.push(stage, priority, *argnctxt)

    def response(self):
        """
        Resgata da pilha, valores retornados pelos
        estágios de execução do pipeline. Caso não hajam
        valores retornados ainda, esse método aguardará
        até que um valor seja retornado.
        :return mixed
        """
        if not self.pendent():
            return None

        frompipeline = self.queue.get()
        self.received = self.received + 1

        return StageResult(self, *frompipeline)

    def pendent(self):
        """
        Verifica se há alguma solicitação pendente para ser
        resgatada como resposta.
        :return bool Há solicitação pendente?
        """
        return self.sent != self.received

class StageResult(object):
    """
    Objeto responsável pelo auxílio e controle dos dados
    através do Pipeline.
    """

    def __init__(self, comm, stage, priority, response, context):
        """
        Inicializa uma nova instância do objeto.
        :param comm Instância de comunicação com pipeline.
        :param stage Último estágio de pipeline executado.
        :param priority Prioridade de execução dos dados.
        :param response Resposta dada pelo estágio de pipeline.
        :param context Informações de contexto.
        :return Guide
        """
        self.priority = priority
        self.context = context
        self.stage = stage
        self.comm = comm

        self.response = response if type(response) is tuple else (response,)

    def __getitem__(self, item):
        """
        Localiza e retorna um ou vários elementos de
        resposta dados pelo pipeline.
        :param item Índice a ser retornado.
        :return mixed
        """
        return self.response[item]

@ThreadWrapper
def PipelineStage(idn, function):
    """
    Decorator para estágios do pipeline.
    :param idn Identificador do estágio.
    :param function Função a ser executada no estágio.
    """
    lqueue = _queues[idn]

    while _alive:
        for priority in [high, normal, low]:
            if not lqueue[priority].empty():
                break
        else:
            continue

        output, args, context = lqueue[priority].get()

        try:
            output.put( (idn, priority, function(*args), context) )
        except:
            output.put( (-1, low, None, None) )

def InitPipeline():
    """
    Inicializa a execução do pipeline de tarefas para
    o processamento seguro das imagens.
    """
    PipelineStage(load, core.LoadImage)
    PipelineStage(segment, core.SegmentImage)
    PipelineStage(process, core.ProcessImage)

def StopPipeline():
    """
    Finaliza a execução do pipeline de tarefas para
    o processamento de imagens.
    """
    global _alive
    _alive = False