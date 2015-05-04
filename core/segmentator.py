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
from .image import Image

from sklearn.neighbors import KNeighborsClassifier
import config
import numpy

class Segmentator(object):
    """
    Objeto responsável pela segmentação da imagem. É composto
    de métodos que possibilitam a binarização da imagem para
    processamento próximo e cálculo de falhas.
    """

    def __init__(self, x, y, k = 1):
        """
        Inicializa e cria uma nova instância do objeto.
        :param x Entradas de casos de treinamento.
        :param y Classes dos casos de treinamento.
        :param k Número de vizinhos mais próximos a ser considerado.
        """
        self.knn = KNeighborsClassifier(
            n_neighbors = k,
            warn_on_equidistant = False
        )

        self.knn.fit(x, y)

    @classmethod
    def train(cls, trainfile = config.root + "/trainset.txt", train = None):
        """
        Treina uma instância de Segmentator para aplicação
        do algoritmo de segmentação.
        :param trainfile Arquivo de casos de teste.
        :return Segmentator Nova instância
        """
        if train is not None:
            return cls(*train)

        x, y = [], []

        with open(trainfile, "r") as trainl:
            for line in trainl:
                l = line.strip().split(' ')
                x.append([int(l[0]), int(l[1]), int(l[2])])
                y.append(int(l[3]))

        return cls(x, y)

    def apply(self, image):
        """
        Segmenta a imagem alvo.
        :param image Imagem alvo de segmentação.
        :return Imagem segmentada de acordo com o treinamento dado.
        """
        shape = image.raw.shape[:2]
        image = image.tolab()
        image = numpy.reshape(image.raw, (shape[0] * shape[1], 3))

        mask = numpy.array(self.knn.predict(image), dtype = numpy.uint8)
        mask = numpy.reshape(mask, shape)
        
        return Image(mask)