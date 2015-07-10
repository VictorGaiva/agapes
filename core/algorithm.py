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
from controller.pipeline import segment, process, normal
from controller.pipeline.multistage import MultiStage
from controller import ThreadWrapper

class Algorithm(object):
    """
    Objeto responsável pela administração dos dados e da
    execução do algoritmo central do projeto.
    """

    def __init__(self, pwork):
        """
        Inicializa uma nova instância do objeto.
        :param pwork Colcha de retalhos a ser executada.
        :return Algorithm
        """
        self.patch = pwork.shred()
        self.pwork = pwork

    @ThreadWrapper
    def run(self, control, distance):
        """
        Executa o algoritmo.
        :param control Controlador da página.
        :param distance Distância entre as linhas de plantação.
        """
        #comm = MultiStage(normal, segment, process)
        comm = MultiStage(normal, segment, process, control = control)

        for i, p in enumerate(self.patch):
            p.select(0)
            comm.push(patch = p, distance = distance, id = i, address = control.pg.address)

        comm.consume()
