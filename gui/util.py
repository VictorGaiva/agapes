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

class Jar(object):
    """
    Jarro de dados. Armazena todos os dados passados para
    o objeto atraves dos métodos fornecidos e implementados
    pela classe.
    """

    def __init__(self, **kwargs):
        """
        Inicializa uma nova instância do objeto.
        :return Jar Nova instância criada.
        """
        self._jar = kwargs
        self._count = 0


    def __getattr__(self, name):
        """
        Recupera alguma informação contida no jarro.
        :param name Nome do ítem a ser recuperado.
        :return mixed Dado recuperado do jarro.
        """
        if name in self._jar:
            return self._jar[name]

        return None


    def __setattribute__(self, name, value):
        """
        Adiciona ou atualiza alguma informação ao jarro.
        :param name Nome do ítem a ser adicionado.
        :param value Novo valor do ítem.
        :return None
        """
        if name not in self._jar:
            self._count = self._count + 1

        self.__dict__[name] = value


    def __delattr__(self, name):
        """
        Remove alguma informação do jarro.
        :param name Nome do ítem a ser apagado.
        :return None
        """
        if name in self._jar:
            self._count = self._count - 1
            del self._jar[name]


    def __len__(self):
        """
        Conta a quantidade de elementos armazenados no jarro.
        :return int Quantidade de elementos armazenados.
        """
        return self._count


class HierarchicalJar(Jar):
    """
    Jarro de dados hierárquicos. Armazena dados em forma
    hierárquica, semelhante a uma árvore com galhos e
    folhas nomeadas.
    """

    def __init__(self, dtype = None, **kwargs):
        """
        Inicializa uma nova instância do objeto.
        :param dtype Tipo padrão dos dados inicializados implicitamente.
        :return HierarchicalJar
        """
        self._dtype = dtype if dtype is not None else HierarchicalJar
        super(HierarchicalJar, self).__init__(**kwargs)


    def __getattr__(self, name):
        """
        Recupera alguma informação contida no jarro.
        :param name Nome do ítem a ser recuperado.
        :return mixed Dado recuperado do jarro.
        """
        if name not in self._jar:
            self._jar[name] = self._dtype(_parent = self)
            self._count = self._count + 1

        return self._jar[name]


class Factory(object):
    """
    Objeto responsável pela inicialização de outros objetos
    de forma mais fácil e acessível.
    """

    def __init__(self, dtype):
        """
        Inicializa uma nova instância do objeto.
        :param dtype Tipo de objeto a ser inicializado.
        :return Factory
        """
        self._dtype = dtype
        self._kwargs = {}
        self._args = []


    def __call__(self, *args, **kwargs):
        """
        Método mágico de encapsulamento de Factory.create .
        :param args Argumentos de linha a serem utilizados.
        :param kwargs Argumentos nominais.
        :return mixed
        """
        return self.create(*args, **kwargs)


    def create(self, *args, **kwargs):
        """
        Inicializa uma instância do objeto alvo.
        :param args Argumentos de linha a serem utilizados.
        :param kwargs Argumentos nominais.
        :return mixed
        """
        return self._dtype(
            *args if args is not () else self._args,
            **kwargs if kwargs is not {} else self._kwargs
        )


    def createmany(self, count, *args, **kwargs):
        """
        Cria várias instâncias do objeto alvo.
        :param count Quantidade de instâncias a serem criadas.
        :param args Argumentos de linha a serem utilizados.
        :param kwargs Argumentos nominais.
        :return generator
        """
        return (
            self.create(*args, **kwargs)
                for i in xrange(count)
        )


    def setargs(self, *args, **kwargs):
        """
        Adiociona valores aos argumentos a serem utilizados por
        padrão pelas novas instâncias.
        :param args Argumentos de linha a serem utilizados.
        :param kwargs Argumentos nominais.
        :return Factory
        """
        self._kwargs = kwargs
        self._args = args

        return self
