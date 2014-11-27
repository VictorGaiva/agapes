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
    
    # Mapa e referências de todos os componentes. Instâncias
    # que são encapsuladas pelo objeto Map, que pode ser acessado
    # a partir de todos os módulos.
    map = None
    comp = None
    shape = None
    
    class __metaclass__(type):
        """
		Metaclasse de Map. Permite a criação de operadores mágicos em escopo
		estático permitindo, assim, acessar a classe como instância.
		"""
        
        def __getitem__(cls, index):
            """
			Acessa e retorna o elemento presente na posição dada
            pelo parâmetro index.
			@param int index Índice a ser explorado.
			@return Component
			"""
            return Map.comp[Map.map[index]]
    
    @classmethod
    def set(cls, map, comps):
        """
        Método responsável por modificar os valores apontados pelo
        mapa e pela lista de referências de componentes.
        @param Image map Mapa dos componentes.
        @param list comps Lista de componentes.
        """
        cls.map = map
        cls.comp = comps
        cls.shape = map.shape