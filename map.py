#!/usr/bin/python
# -*- encoding: utf-8 -*-
class Map(object):
    """
    Objeto respons�vel pelo armazenamento e intermedia��o
    do mapa de componentes.
    """
    
    # Mapa e refer�ncias de todos os componentes. Inst�ncias
    # que s�o encapsuladas pelo objeto Map, que pode ser acessado
    # a partir de todos os m�dulos.
    map = None
    comp = None
    shape = None
    
    class __metaclass__(type):
        """
		Metaclasse de Map. Permite a cria��o de operadores m�gicos em escopo
		est�tico permitindo, assim, acessar a classe como inst�ncia.
		"""
        def __getitem__(cls, index):
            """
			Acessa e retorna o elemento presente na posi��o dada
            pelo par�metro index.
			@param int index �ndice a ser explorado.
			@return Component
			"""
            return Map.comp[Map.map[index]]
    
    @classmethod
    def set(cls, map, comps):
        """
        M�todo respons�vel por modificar os valores apontados pelo
        mapa e pela lista de refer�ncias de componentes.
        @param Image map Mapa dos componentes.
        @param list comps Lista de componentes.
        """
        cls.map = map
        cls.comp = comps
        cls.shape = map.shape