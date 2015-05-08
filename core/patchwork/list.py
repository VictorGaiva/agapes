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

class List(list):
    """
    Armazena uma lista de retalhos que atuam sobre uma
    imagem ou um patchwork.
    """

    def __init__(self, *patch):
        """
        Inicializa uma nova instância do objeto.
        :param patch Retalhos iniciais da lista.
        :return List
        """
        list.__init__(self, patch)

    @property
    def length(self):
        """
        Tamanho da lista armazenada.
        :return int
        """
        return len(self)

    def filter(self, function):
        """
        Filtra os elementos presentes na lista
        utilizando a função passada como critério de
        escolha. Os elementos que não satisfazem ao
        critério escolhido serão eliminados.
        :param function Função de filtragem da lista.
        """
        newl = filter(function, self)
        list.__init__(self, newl)