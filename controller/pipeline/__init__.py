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
from Queue import Queue, Empty
from .. import ThreadWrapper
import core

__all__ = [
    "Pipeline", "stagename",
    "low", "normal", "high",
    "load", "segment", "process",
]

#TODO: Transformar os estágios do pipeline em processos e não threads.
#TODO: Implementar protocolo de pacotes para comunicação entre processos.

low, normal, high = range(3)
load, segment, process = range(3)
stagename = ["ImageLoaded", "ImageSegmented", "ImageProcessed"]

class Pipeline(object):
    """
    Administração e controle de execução do pipeline de
    processamento em segundo plano. É necessária a utilização
    de uma instância de Communication para a interação com
    o pipeline.
    """
    _alive = True
    _queue = [[Queue() for i in xrange(3)] for j in xrange(3)]

    @classmethod
    def init(cls):
        """
        Inicializa a execução do pipeline de tarefas para
        o processamento paralelo das imagens.
        """
        cls.start(load, core.LoadImage)
        cls.start(segment, core.SegmentImage)
        cls.start(process, core.ProcessImage)

    @classmethod
    def stop(cls):
        """
        Finaliza a execução do pipeline e termina os
        threads de processamento.
        """
        cls._alive = False

    @classmethod
    @ThreadWrapper
    def start(cls, stage, function):
        """
        Inicializa um estágio do pipeline.
        :param stage Identificador do estágio.
        :param function Função a ser executada pelo estágio.
        """
        while cls._alive:
            for priority in [high, normal, low]:
                try:
                    comm, data = cls._queue[stage][priority].get(False)
                    comm.notify(stage, data, function(data))
                except Empty:
                    continue
                except:
                    print u"Erro no processamento do talhão!"
                    comm.notify(-1, data, {})

    @classmethod
    def push(cls, stage, priority, comm, data):
        """
        Adiciona uma tarefa para execução por um
        dos estágios do pipeline.
        :param stage Estágio alvo das tarefas.
        :param priority Prioridade de execução da tarefa.
        :param comm Instância de comunicação com Pipeline.
        :param data Lista de argumentos a serem passados ao pipeline.
        """
        cls._queue[stage][priority].put( (comm, data) )
