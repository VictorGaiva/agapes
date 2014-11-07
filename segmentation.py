#!/usr/bin/python
# -*- encoding: utf-8 -*-
from sklearn.neighbors import KNeighborsClassifier
from image import *
import numpy

class Segmentation(object):
    """
    Objeto respons�vel pela segmenta��o da imagem. � composto
    de m�todos que possibilitam a binariza��o da imagem para
    processamento pr�ximo e c�lculo de falhas.
    """

    def __init__(self, trainfile = None):
        """
        Inicializa e cria uma nova inst�ncia do objeto.
        @param str trainfile Nome do arquivo com casos de treino.
        """
        x, y = [], []
        
        if trainfile is None:
            trainfile = __path__ + "/trainset.txt"
        
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
        @param Image image Imagem alvo de segmenta��o.
        @return Image Imagem segmentada de acordo com o treinamento dado.
        """
        shape = image.raw.shape[:2]
        image = image.tolab()
        image = numpy.reshape(image.raw, (shape[0] * shape[1], 3))

        mask = numpy.array(self.knn.predict(image), dtype = numpy.uint8)
        mask = numpy.reshape(mask, shape)
        
        return Image(mask)