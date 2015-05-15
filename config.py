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
from os import path

#TODO: Criar objeto de configuração, que lê de arquivos as opções selecionadas.

root = path.dirname(path.realpath(__file__))
author = "Rodrigo Siqueira <rodriados@gmail.com>"
appname = "PSG - Tecnologia Aplicada / LIA - FACOM - UFMS"
version = "0.6"
wsize = (800, 600)
wid = 0
