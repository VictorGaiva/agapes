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
from multiprocessing import Queue, Pipe, Lock
from . import ThreadWrapper
import core
import time

_alive = True
_queues = [
    [Queue(), Queue(), Queue()],
    [Queue(), Queue(), Queue()],
    [Queue(), Queue(), Queue()]
]

LOW, NORMAL, HIGH = range(3)
LOAD, SEGMENT, PROCESS = range(3)

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
        self.lock = Lock()
        self.reader, self.writer = Pipe(False)
        self.sent, self.received = 0, 0

    def __del__(self):
        """
        Finaliza a comunicação com o pipeline.
        É recomendável invocar esse método após o término
        da execução de tarefas.
        """
        self.writer.close()
        self.reader.close()

    def PushToStage(self, stage, priority = NORMAL, args = (), **context):
        """
        Adiciona uma tarefa a ser executada porum
        um dos estágios do pipeline.
        :param stage Estágio alvo das tarefas.
        :param priority Prioridade de execução da tarefa.
        :param args Argumentos de posição da tarefa.
        :param kwargs Argumentos nominais da tarefa.
        :param context Dados de contexto.
        """
        _queues[stage][priority].put((self.writer, self.lock, args, context))
        self.sent = self.sent + 1

    def PopResponse(self):
        """
        Resgata da pilha, valores retornados pelos
        estágios de execução do pipeline. Caso não hajam
        valores retornados ainda, esse método aguardará
        até que um valor seja retornado.
        :return mixed
        """
        if self.sent == self.received:
            return None

        retv = self.reader.recv()
        self.received = self.received + 1

        return retv

@ThreadWrapper
def PipelineStage(idn, function):
    """
    Decorator para estágios do pipeline.
    :param idn Identificador do estágio.
    :param function Função a ser executada no estágio.
    """
    lqueue = _queues[idn]

    while _alive:
        for priority in [HIGH, NORMAL, LOW]:
            if not lqueue[priority].empty():
                break
        else:
            time.sleep(.2)
            continue

        writer, lock, args, context = lqueue[priority].get()
        retv = function(*args)

        lock.acquire()
        writer.send((idn, retv, context))
        lock.release()

def InitPipeline():
    """
    Inicializa a execução do pipeline de tarefas para
    o processamento seguro das imagens.
    """
    PipelineStage(LOAD, core.LoadImage)
    PipelineStage(SEGMENT, core.SegmentImage)
    PipelineStage(PROCESS, core.ProcessImage)

def StopPipeline():
    """
    Finaliza a execução do pipeline de tarefas para
    o processamento de imagens.
    """
    global _alive
    _alive = False