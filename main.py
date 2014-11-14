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
from segmentation import *
from component import *
from image import *
from event import *
from line import *
import __builtin__
import sys
import os

__builtin__.__path__ = os.path.dirname(os.path.realpath(__file__))
__builtin__.__author__ = "Rodrigo Siqueira <rodriados@gmail.com>"
__builtin__.__appname__ = "PSG - Tecnologia Aplicada"
__builtin__.__version__ = "0.3.1"

# TODO:     Feedback de execução e de erros. Mostra ao usuário que
#           o programa está executando corretamente e os erros que
#           ocorreram.

# TODO:     Correlacionar a imagem da janela com a imagem original,
#           tornando mais fácil a localização da área visualizada
#           na imagem original.

# TODO:     Redimensionar imagem para um tamanho fixo, e não para
#           uma proporção da imagem original como está sendo feito.

# TODO:     Transformar equações utilizadas para funções paramétricas
#           permitindo, assim, aumentar o leque de curvas que podem
#           ser descritas.

# TODO:     Retirar a execução do programa diretamente do campo
#           de drag-n-drop.

# TODO:     Ao soltar uma imagem, exibí-la no campo de drag-n-drop
#           e permitir a edição da imagem diretamente desse campo.

# TODO:     Adicionar ferramentas de edição de imagem na barra
#           horizontal inferior da janela.

# TODO:     Criação de um instalador para que as dependências do
#           programa sejam automaticamente instaladas, sem intervenção
#           manual.
def ShowImage(img):
    """
    Prepara a janela para mostrar todos os passos de
    execução do algoritmo.
    @param Image img Primeira imagem a ser mostrada.
    """
    global window
    window = ImageWindow(__appname__, img)
    
def AddImage(img):
    """
    Adiciona uma imagem a ser exibida na janela.
    @param Image img Imagem a ser adicionada.
    """
    global window
    window.append(img)
    
def ShowResult(pcento, metros):
    """
    Mostra um texto na imagem indicando o resultado
    obtido do processamento da imagem alvo.
    @param float pcento Porcentagem de falhas na imagem.
    @param float metros Metros de falhas na imagem.
    """
    global window    
    window.text("Falhas: %.2f metros (%d%%)" % (metros, pcento), (20, -50))

def SetHandles():
    """
    Configura o tratamento dos eventos disparados pelo
    núcleo de execução do programa.
    """
    Event.load = ShowImage
    Event.segment = AddImage
    Event.process = AddImage
    Event.result = ShowResult

def ProcessImage(imgaddr, distance):
    """
    Núcleo de execução do processamento de imagens. Esta
    função é a grande responsável pelo cálculo do resultado
    desejado do programa.
    @param str imgaddr Endereço da imagem alvo.
    @param float distance Distância entre linhas
    """
    img = Image.load(imgaddr).resize(.3)
    Event.load(img)
    
    seg = Segmentation().apply(img)
    Event.segment(seg)
    
    comps = Component.load(seg)
    
    if not seg.check(comps):
        comps = Component.load(seg)
    
    lines = Line.first(comps[1])
    lines.complete()
    finalimg = lines.show()
    Event.process(finalimg)
    
    name = imgaddr.rsplit('.', 1)
    finalimg.save(name[0] + ".processado." + name[1])

    pcento, metros = lines.error(distance)
    Event.result(pcento, metros)

__builtin__.PrImage = ProcessImage

if __name__ == '__main__':
    if len(sys.argv) == 3:
        SetHandles()
        ProcessImage(sys.argv[1], sys.argv[2] + " metros")
        
    else:
        from gui import AppMain
        SetHandles()
        app = AppMain()
        app.MainLoop()
    