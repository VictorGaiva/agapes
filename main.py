#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
PSG - Tecnologia Aplicada

Este � um m�dulo utilizado para contagem de falhas em
planta��es de cana-de-a��car atrav�s do uso de imagens
a�reas capturadas por VANT's ou aparelhos similares.

Este arquivo � respons�vel pelo desenho da interface do
programa e tamb�m pela execu��o e apresenta��o dos
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

# TODO:     Feedback de execu��o e de erros. Mostra ao usu�rio que
#           o programa est� executando corretamente e os erros que
#           ocorreram.

# TODO:     Correlacionar a imagem da janela com a imagem original,
#           tornando mais f�cil a localiza��o da �rea visualizada
#           na imagem original.

# TODO:     Redimensionar imagem para um tamanho fixo, e n�o para
#           uma propor��o da imagem original como est� sendo feito.

# TODO:     Transformar equa��es utilizadas para fun��es param�tricas
#           permitindo, assim, aumentar o leque de curvas que podem
#           ser descritas.

# TODO:     Retirar a execu��o do programa diretamente do campo
#           de drag-n-drop.

# TODO:     Ao soltar uma imagem, exib�-la no campo de drag-n-drop
#           e permitir a edi��o da imagem diretamente desse campo.

# TODO:     Adicionar ferramentas de edi��o de imagem na barra
#           horizontal inferior da janela.

# TODO:     Cria��o de um instalador para que as depend�ncias do
#           programa sejam automaticamente instaladas, sem interven��o
#           manual.
def ShowImage(img):
    """
    Prepara a janela para mostrar todos os passos de
    execu��o do algoritmo.
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
    n�cleo de execu��o do programa.
    """
    Event.load = ShowImage
    Event.segment = AddImage
    Event.process = AddImage
    Event.result = ShowResult

def ProcessImage(imgaddr, distance):
    """
    N�cleo de execu��o do processamento de imagens. Esta
    fun��o � a grande respons�vel pelo c�lculo do resultado
    desejado do programa.
    @param str imgaddr Endere�o da imagem alvo.
    @param float distance Dist�ncia entre linhas
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
    