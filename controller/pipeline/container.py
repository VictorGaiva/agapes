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

class Container(object):
    """
    Armazena dados que podem ser utilizados como
    argumentos para as funções executadas nos
    estágios do pipeline.
    """

    def __init__(self, **initial):
        """
        Inicializa lista de argumentos.
        :param initial Argumentos iniciais.
        :return Container
        """
        self._raw = initial

    def __getattr__(self, item):
        """
        Localiza, acessa e retorna o valor de um
        argumento com o nome especificado.
        :param item Nome do dado a ser resgatado.
        :return mixed
        """
        return self._raw[item]

    def update(self, **data):
        """
        Atualiza a lista de argumentos com novos
        dados. Dados com chaves repetidas serão
        substituídos.
        :param data Novos dados a serem adicionados.
        """
        self._raw.update(data)