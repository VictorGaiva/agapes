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
from gui import InitGUI
from image import *
from event import *
from line import *
import __builtin__
import textwrap
import argparse
import os

__builtin__.__path__ = os.path.dirname(os.path.realpath(__file__))
__builtin__.__author__ = "Rodrigo Siqueira <rodriados@gmail.com>"
__builtin__.__appname__ = "PSG - Tecnologia Aplicada"
__builtin__.__version__ = "0.4"

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

def LoadImage(address):
    """
    Carrega uma imagem.
    @param str address Endere�o da imagem a ser carregada.
    @return Imagem Imagem carregada.
    """
    img = Image.load(address).resize(.3)
    Event.load.trigger(img)
    
    return img
    
def SegmentImage(image):
    """
    Executa a segmenta��o da imagem.
    @param Image Imagem a ser segmentada.
    @return ComponentList Lista de componentes.
    """
    img = Segmentation().apply(image)
    comps = Component.load(img)
    
    if not img.check(comps):
        comps = Component.load(img)
        
    Event.segment.trigger(img)
    return comps

def FindLines(comps):
    """
    Encontra as linhas de planta��o sobre a imagem.
    @param ComponentList comps Componentes encontrados.
    @return LineList Linhas encontradas.
    """
    lines = Line.first(comps[1])
    lines.complete()
    
    lineimg = lines.display()
    Event.process.trigger(lineimg)
    
    return lines, lineimg

def SaveImage(original, image):
    """
    Salva a imagem resultante.
    @param str original Endere�o da imagem original.
    @param Imagem image Imagem a ser salva.
    """
    name = original.rsplit('.', 1)
    image.save("{0}.processed.{1}".format(*name))

def GetResult(lines, distance):
    """
    Exibe o resultado do processamento.
    @param LineList lines Linhas encontradas na imagem.
    @param float distance Dist�ncia entre as linhas de planta��o.
    """
    porcento, metro = lines.error(distance)
    Event.result.trigger(porcento, metro)

def Process(imaddr, distance):
    """
    N�cleo de execu��o do processamento de imagens. Esta
    fun��o � a grande respons�vel pelo c�lculo do resultado
    desejado do programa.
    @param str imgaddr Endere�o da imagem alvo.
    @param float distance Dist�ncia entre linhas de planta��o na imagem.
    """
    SetHandles()
    image = LoadImage(imaddr)
    comps = SegmentImage(image)
    lines, lineim = FindLines(comps)
    
    SaveImage(imaddr, lineim)
    GetResult(lines, distance)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent("""\
            PSG - Tecnologia Aplicada.
            --------------------------
            Esta aplica��o � utilizada para contar a
            quantidade de falhas presente em uma planta��o
            de cana-de-a��car. S�o utilizadas imagens a�reas
            para a contabiliza��o das falhas presentes.
            """.decode('latin1'))
    )

    parser.add_argument(
        'image',
        metavar = 'image',
        type = str,
        nargs = '?',
        help = "imagem alvo da an�lise".decode('latin1')
    )

    parser.add_argument(
        'dist',
        metavar = 'dist',
        type = float,
        nargs = '?',
        help = "dist�ncia entre as linhas de planta��o".decode('latin1')
    )

    args = parser.parse_args()
    
    if args.dist is None or args.image is None:
        InitGUI(Process)
    else:
        Process(args.image, args.dist)
    