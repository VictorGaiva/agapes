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
from .handler import Handler, Empty

class List(object):
    """
    Objeto responsável pelo armazenamento de manipuladores
    de eventos durante a execução do programa.
    """
    _hdlr = {}

    @classmethod
    def set(cls, ename, obj, callback):
        """
        Cria um manipulador de eventos de acordo com o nome
        dado sobre o objeto.
        :param ename Nome ou identificação do evento registrado.
        :param obj Objeto alvo do evento a ser registrado.
        :param callback Função de resposta ao evento.
        """
        cls._hdlr[ename, obj] = callback

    @classmethod
    def get(cls, ename, obj):
        """
        Recupera um evento através do nome de seu manipulador.
        :param ename Nome do evento a ser recuperado.
        :param obj Objeto alvo do evento a ser recuperado.
        :return list
        """
        if (ename, obj) in cls._hdlr.keys():
            return Handler(cls._hdlr[ename, obj])

        return Empty(ename, obj)

    @classmethod
    def unset(cls, ename, obj):
        """
        Remove o manipulador de um evento. Após a chamada
        desse método, o evento será totalmente destruído.
        :param ename Nome do evento a ser destruído.
        :param obj Objeto alvo do evento a ser destruído.
        """
        if (ename, obj) in cls._hdlr.keys():
            del cls._hdlr[ename, obj]
