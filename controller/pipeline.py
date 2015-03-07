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
            time.sleep(.5)
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



#from . import ThreadWrapper
#from gui.event import PostEvent
#from Queue import Queue as Q, Empty
#import core
#
#low, normal, high = range(3)
#load, segment, process = range(3)
#ename = ["ImageLoad", "ImageSegment", "ImageProcess"]
#
#class Communication(object):
#    """
#    Objeto responsável pelo controle da comunicação
#    de um thread com o Pipeline.
#    """
#
#    def __init__(self, priority, first = load, last = process, context = {}):
#        """
#        Inicializa uma nova instância do objeto.
#        :return Communication
#        """
#        self.priority = priority
#        self.first, self.last = first, last
#        self.context = context
#        self.event = True
#
#        self.ready = Q()
#        self.sent, self.rcvd = 0, 0
#
#    def Push(self, **args):
#        """
#        Adiciona uma tarefa a ser executada por um
#        dos estágios do pipeline.
#        :param args Argumentos a serem passados ao pipeline.
#        """
#        if load <= self.first <= self.last <= process:
#            if low <= self.priority <= high:
#                Pipeline.Push(self.first, self.priority, self, args or {})
#                self.sent = self.sent + 1
#
#    def Notify(self, stage, args = {}, response = ()):
#        """
#        Recebe a resposta de um estágio do pipeline e
#        trata a resposta de acordo com o necessário para
#        a execução da tarefa. Esse método será sempre
#        executado pelos threads do pipeline.
#        :param stage Estágio responsável pela resposta.
#        :param args Argumentos passados ao estágio de pipeline.
#        :param response Resposta produzida pelo estágio.
#        """
#        if self.event:
#            PostEvent(ename[stage], response, self.context)
#
#        if stage < self.last:
#            args.update(response)
#            Pipeline.Push(stage + 1, self.priority, self, args)
#
#        else:
#            self.ready.put(response)
#
#    def Pop(self):
#        """
#        Resgata da pilha, valores retornados pelos
#        estágios de execução do pipeline. Caso não hajam
#        valores retornados ainda, esse método aguardará
#        até que um valor seja retornado.
#        :return mixed
#        """
#        if not self.Pendent():
#            return None
#
#        response = self.ready.get()
#        self.rcvd = self.rcvd + 1
#
#        return response
#
#    def Pendent(self):
#        """
#        Verifica se há alguma solicitação pendente para ser
#        resgatada como resposta.
#        :return bool Há solicitação pendente?
#        """
#        return self.sent != self.rcvd
#
#class Pipeline(object):
#    """
#    Objeto responsável pelo controle e administração do
#    Pipeline que é executado em segundo plano pelo software.
#    É necessário a utilização de uma instância de
#    Communication para interagir com os threads do pipeline.
#    """
#    alive = True
#    inq = [[Q(), Q(), Q()], [Q(), Q(), Q()], [Q(), Q(), Q()]]
#
#    @classmethod
#    def Init(cls):
#        """
#        Inicializa a execução do pipeline de tarefas para
#        o processamento seguro das imagens.
#        """
#        cls.Start(load, core.LoadImage)
#        cls.Start(segment, core.SegmentImage)
#        cls.Start(process, core.ProcessImage)
#
#    @classmethod
#    def Stop(cls):
#        """
#        Finaliza a execução do pipeline de tarefas para
#        o processamento de imagens.
#        """
#        cls.alive = False
#
#    @classmethod
#    @ThreadWrapper
#    def Start(cls, stage, function):
#        """
#        Inicializa um estágio do pipeline.
#        :param stage Identificador do estágio.
#        :param function Função a ser executada no estágio.
#        """
#        while cls.alive:
#            for priority in [high, normal, low]:
#                try:
#                    outq, args = cls.inq[stage][priority].get(False)
#                    outq.Notify(stage, args, function(**args))
#                except Empty:
#                    continue
#                except:
#                    outq.Notify(stage)
#
#    @classmethod
#    def Push(cls, stage, priority, outq, args):
#        """
#        Adiciona uma tarefa a ser executada por um
#        dos estágios do pipeline.
#        :param stage Estágio alvo das tarefas.
#        :param priority Prioridade de execução da tarefa.
#        :param outq Instância de comunicação de Pipeline.
#        :param args Lista de argumentos a serem passados ao pipeline.
#        """
#        cls.inq[stage][priority].put((outq, args))