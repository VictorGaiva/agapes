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

class Map(object):
    """
    Objeto responsável pelo armazenamento e intermediação
    do mapa de componentes.
    """

    def __init__(self, img, comps):
        """
        Inicializa uma nova instância do objeto.
        :param img Imagem alvo do mapa.
        :param comps Todos os componentes encontrados.
        :return Mapa de componentes inicializado.
        """
        self.img = img
        self.comp = [None] + comps
        self.shape = self.img.shape

    def __getitem__(self, index):
        """
        Acessa e retorna o elemento presente na posição dada
        pelo parâmetro index.
        :param index Índice a ser explorado.
        :return Componente a ser acessado.
        """
        return self.comp[self.img[index]]
