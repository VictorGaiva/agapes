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
from sklearn.neighbors import KNeighborsClassifier
from image import *
import config
import numpy

class Segmentation(object):
    """
    Objeto responsável pela segmentação da imagem. É composto
    de métodos que possibilitam a binarização da imagem para
    processamento próximo e cálculo de falhas.
    """

    def __init__(self, trainfile = None):
        """
        Inicializa e cria uma nova instância do objeto.
        @param str trainfile Nome do arquivo com casos de treino.
        """
        x, y = [], []
        
        if trainfile is None:
            trainfile = config.path + "/trainset.txt"
        
        with open(trainfile, "r") as trainf:
            for line in trainf:
                l = line.strip().split(' ')
                x.append([int(l[0]), int(l[1]), int(l[2])])
                y.append(int(l[3]))
        
        self.knn = KNeighborsClassifier(n_neighbors = 1, warn_on_equidistant = False)
        self.knn.fit(x, y)
            
    def apply(self, image):
        """
        Segmenta a imagem alvo.
        @param image Imagem alvo de segmentação.
        @return Image Imagem segmentada de acordo com o treinamento dado.
        """
        shape = image.raw.shape[:2]
        image = image.tolab()
        image = numpy.reshape(image.raw, (shape[0] * shape[1], 3))

        mask = numpy.array(self.knn.predict(image), dtype = numpy.uint8)
        mask = numpy.reshape(mask, shape)
        
        return Image(mask)