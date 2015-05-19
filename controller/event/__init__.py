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
from .bind import Bind
from .post import Post
from .list import List

__all__ = [
    "Event", "Bind", "Post"
]

class Event(object):
    """
    Objeto responsável pela criação, administração e
    execução de manipuladores de eventos durante toda
    a execução do programa.
    """

    def __init__(self, ename, obj = None):
        """
        Criação de instância de evento.
        :param ename Nome ou identificação do evento.
        :param obj Objeto alvo do evento.
        :return Event
        """
        self._ename = ename
        self._obj = obj

    def bind(self, callback, *args, **kwargs):
        """
        Cria manipulador de evento de acordo com o nome
        dado sobre o objeto.
        :param callback Função de resposta ao evento.
        :param args Argumentos do manipulador.
        :param kwargs Argumentos nomeados do manipulador.
        """
        Bind(self._ename, self._obj).set(callback, args, kwargs)

    def unbind(self):
        """
        Remove manipulador de evento de acordo com o nome
        dado sobre o objeto.
        """
        Bind(self._ename, self._obj).unset()

    def post(self, *args, **kwargs):
        """
        Notifica os manipuladores do evento para que executem
        suas tarefas de acordo com os parâmetros dados.
        :param args Argumentos do manipulador.
        :param kwargs Argumentos nomeados do manipulador.
        :return mixed
        """
        return Post(self._ename, self._obj).send(*args, **kwargs)
