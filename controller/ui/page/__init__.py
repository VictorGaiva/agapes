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

class Control(object):
    """
    Classe base para as classes controladoras
    de páginas.
    """

    class __metaclass__(type):
        """
        Metaclasse de Control. Permite utilizar
        os métodos de instância, estaticamente.
        """

        def __getitem__(cls, ptype):
            """
            Seleciona a classe de controle correta
            para cada tipo de página.
            :param ptype Tipo de página a ser criada.
            :return Control
            """
            return ptype.__control__

    def __init__(self, parent):
        """
        Inicializa uma nova instância.
        :param parent Controlador superior na hierarquia.
        :return Control
        """
        self.parent = parent
        self.parent.register(self)
        self.pg = None

    def bind(self, page):
        """
        Vincula uma página ao controlador.
        :param page Página a ser vinculada.
        """
        self.pg = page
